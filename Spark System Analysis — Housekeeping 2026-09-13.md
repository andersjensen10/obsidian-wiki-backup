---
tags: [spark, system-maintenance, housekeeping, llama.cpp, comfyui]
status: assessment-complete
machine: Spark
snapshot_date: 2026-09-13
---

# Spark System Analysis — Housekeeping Assessment

## Scope

Read-only assessment of Spark's internal NVMe root filesystem (`/dev/nvme0n1p2`, `/`). External/removable mounts were deliberately excluded from storage recommendations, including `/media/aj/TOSHIBA EXT1` and `/media/aj/ESD-USB`. No cleanup, service restart, model deletion, package removal, or external-drive change was performed.

## Executive summary

Spark is operational, but the internal disk is carrying a large amount of accumulated test and model data. The immediate risk is not inode exhaustion or a failed service; it is storage concentration around a very large ComfyUI backup, package/download caches, logs, and duplicated environments. The root filesystem has about **641 GB used and 229 GB available** on a 916 GB volume. That is workable today, but a few large model downloads or video runs could consume the remaining headroom quickly.

The mission-critical paths are live and should be protected:

- **llama.cpp**: `llama-server.service`, port `8014`, production model `qwen3.8-27b-aggressive-q5` with speculative decoding; model files under `/home/aj/llama-models`.
- **ComfyUI**: `comfyui.service`, port `8188`, running from `/home/aj/ComfyUI` with `/home/aj/comfyui-env`.
- The current ComfyUI process has been running since September 7 and is using about **23 GB resident RAM** according to the process snapshot.

The most likely reclaimable space is the dated ComfyUI backup, but it must be treated as a deliberate archive decision, not deleted automatically: it contains roughly **296 GB**, including about **280 GB of models**, about **7 GB of output**, about **1.1 GB of input**, and a duplicate **6.7 GB** ComfyUI environment.

## Hardware and operating state

- Ubuntu `24.04.4 LTS`, arm64/aarch64.
- Kernel: `6.17.0-1014-nvidia`.
- CPU: 20 logical CPUs, 10 Cortex-X925 plus 10 Cortex-A725 cores; max reported frequency 3.9 GHz.
- GPU: NVIDIA GB10, driver `580.142`; temperature about 45 C and utilization about 8% at the snapshot.
- `nvidia-smi` does not expose GPU memory totals/usage on this platform (`N/A`), so VRAM/headroom cannot be assessed from the usual query.
- RAM: 121 GiB total, 98 GiB used, 22 GiB available; swap 15 GiB total with 4.1 GiB used. The swap usage and ComfyUI/Fish Speech workload suggest memory pressure has occurred during testing, even though the machine is not currently out of memory.
- Root filesystem inode usage is only 3%; inode cleanup is not urgent.
- No failed systemd units were reported.

## Storage hotspots on the internal disk

| Area | Approx. size | Assessment |
|---|---:|---|
| `/home/aj/ComfyUI-v0.26.0-backup-20260904-212226` | **296 GB** | Highest-value review target. It includes a full model tree, outputs, inputs, custom nodes, Git data, and a duplicate environment. Preserve until the active ComfyUI workflows/models are compared and AJ approves archival/deletion. |
| `/home/aj/llama-models` | **116 GB** | Mission-critical model library. Do not delete or migrate as housekeeping. Review only for known-unused quantizations after a model inventory and checksum-backed decision. |
| `/home/aj/qwen-tts-server` | **24 GB** | Active Qwen TTS service and model files. Keep; review only stale checkpoints or unused variants. |
| `/home/aj/fish-speech` | **19 GB** | Active Fish Speech API and checkpoints. Keep the active checkpoint; do not remove the duplicate/older environment without checking service dependencies. |
| `/home/aj/.cache` | **23 GB** | Main safe-cleanup candidate, subject to stopping package installs first. Pip HTTP cache is about 14 GB; uv cache about 4 GB; Hugging Face hub about 2 GB; Playwright about 1 GB. |
| `/home/aj/ComfyUI` | **6.9 GB** | Active installation. Do not remove. Its environment is about 6.8 GB and is in use. |
| `/home/aj/comfyui-env` | **6.5 GB** | Active ComfyUI environment. Do not remove. |
| `/home/aj/.lmstudio` | **3.3 GB** | LM Studio runtime/extensions/logs; no active LM Studio server was seen in the process snapshot. Review before pruning, but do not assume it is unused. |
| `/home/aj/.hermes` | **3.1 GB** | Hermes runtime, agent source, node modules, venv, sessions/cache. Keep the active runtime; review only old caches/backups after checking Hermes retention needs. |
| `/var/log` | **3.9 GB** | Journal alone is about 3.6 GB. Safe candidate for bounded journal retention cleanup, not wholesale deletion. |
| `/opt` | **2.5 GB** | NVIDIA/DGX tooling, AI Workbench, RustDesk. Treat as system/vendor software, not general clutter. |
| `/home/aj/.nv` | **1.0 GB** | NVIDIA compute cache. Usually rebuildable, but clear only during a maintenance window with GPU services stopped. |
| `/home/aj/Downloads` | **7.5 GB** | Contains old installers, archives, model files, an incomplete GIMP `.part`, and both arm64/x86_64 RustDesk packages. Good manual review target. |
| `/test.img` | **10 GB** | Old root-level test image dated 2025-10-15. Likely disposable, but verify that no test, mount, or recovery workflow still references it before removal. |

## Running services and installed workload

Active user services include ComfyUI, llama.cpp, CUDA MPS, Fish Speech, Qwen TTS API/UI, LiteLLM proxy, voiceprep API, Hermes gateway, and the Hermes desktop runtime. System services include Docker, DGX Dashboard, NVIDIA persistence/tooling, RustDesk relay/signal components, Tailscale, SSH, Samba AD DC, gohttpserver, ops-api, printing/desktop services, and standard Ubuntu maintenance services.

Notable listeners bound to all interfaces include:

- `22` SSH
- `8000` gohttpserver
- `8014` llama.cpp
- `8080` Fish Speech
- `8090` voiceprep
- `8188` ComfyUI
- `8766` ops-api
- `8020` Qwen TTS
- `4000` LiteLLM
- RustDesk relay ports `21115`–`21119`

This is operationally useful for LAN services, but it is also a security/maintenance surface. Confirm that firewall rules, authentication, and intended LAN exposure are correct before adding more test services. The inventory also shows Docker running, but the current user could not query Docker's image/container disk usage due to permission denial; a privileged read-only `docker system df` should be run separately if Docker storage is suspected.

APT reports **520 packages not upgraded**. A simulated autoremove lists four old NVIDIA/kernel-related packages, including `linux-modules-nvidia-fs-6.11.0-1014` and older NVIDIA firmware. Do not run autoremove or a broad upgrade blindly: verify the running kernel and NVIDIA stack first, then use a planned maintenance window.

## Priority recommendations

### P0 — protect production before cleanup

1. Do not touch `/home/aj/llama-models`, the active `/home/aj/ComfyUI`, `/home/aj/comfyui-env`, active Fish Speech/Qwen TTS checkpoints, or service definitions during bulk cleanup.
2. Capture service command lines, model paths, environment paths, and rollback notes before any restart or environment pruning.
3. Treat the 22 GiB available RAM and 4.1 GiB swap use as a capacity signal. Avoid concurrent model loads and large ComfyUI jobs during cleanup.
4. Maintain a minimum root free-space target of at least 20% before starting new model downloads or large video/image runs.

### P1 — review the 296 GB ComfyUI backup

1. Compare active and backup workflows, custom nodes, model filenames, and recent outputs.
2. Separate the backup into: required rollback models, unique models worth archiving, reproducible code/custom nodes, and disposable generated output/input.
3. The backup's model files are not automatically redundant merely because similar names exist. For example, the 1.7 GB Qwen Lightning file in Downloads and the similarly named backup LoRA have different SHA-256 hashes, so they must not be treated as identical.
4. After verification, the safest large win is usually deleting or moving generated `output/` and stale `input/` material, then deciding whether to retain the backup model set. Do not delete the whole backup as a first step.

### P1 — clear accumulated caches in a controlled window

Review and, if no installs/downloads are running, prune package caches in this order:

- pip HTTP cache: about 14 GB
- uv cache: about 4 GB
- Hugging Face cache: about 2 GB, after checking whether cached blobs are needed for active model work
- Playwright cache: about 1 GB if browser automation tests no longer need it
- NVIDIA compute cache: about 1 GB, only when GPU services are idle
- thumbnails/electron/other desktop caches: about 1 GB combined

Cache cleanup is preferable to deleting environments because it is reversible through redownload and does not alter the mission-critical service layout.

### P1 — trim logs and inspect test artifacts

- Reduce systemd journal retention to a bounded policy rather than deleting journal files manually; current journal usage is about 3.6 GB.
- Inspect `/home/aj/Downloads` and quarantine incomplete/obsolete installers, archives, old architecture packages, and model files after confirming provenance.
- Verify whether `/test.img` is still referenced. If not, remove it during a maintenance window for an immediate 10 GB recovery.

### P2 — environment and software hygiene

- Inventory every active Python environment before removing any. There are at least ComfyUI, Fish Speech CPU/CUDA, Qwen TTS, voiceprep, LiteLLM, HF tools, and benchmark environments. The CUDA environments are large because they contain torch/CUDA wheels; deleting them would break services.
- Check whether LM Studio is still required. Its runtime/extensions consume about 3.3 GB, but no active LM Studio server was observed.
- Check Docker storage with appropriate privileges; Docker is active but its disk report was unavailable to the current user.
- Review the 520 pending APT upgrades and old NVIDIA/kernel packages separately from housekeeping. Use a maintenance window and reboot/rollback plan.
- Review always-on LAN services and exposed ports for necessity and authentication, especially the multiple media/AI APIs and RustDesk relay.

## Suggested execution order

1. Record a fresh root `df -h`, RAM/swap, GPU/service status, and current mission-critical process command lines.
2. Clean only bounded caches and journal retention; re-measure free space.
3. Review Downloads and `/test.img`; remove only confirmed disposable artifacts.
4. Audit the dated ComfyUI backup and reclaim generated output/input first.
5. Re-measure and document the result.
6. Schedule package upgrades/kernel cleanup as a separate maintenance task; do not combine it with model/storage deletion.

## Verification baseline captured

- Root: 916 GB ext4; approximately 641 GB used and 229 GB available.
- Active listeners confirmed for llama.cpp `8014` and ComfyUI `8188`.
- No failed systemd services.
- ComfyUI, llama.cpp, Fish Speech, Qwen TTS, LiteLLM, voiceprep, Hermes, CUDA MPS, Docker, and NVIDIA persistence were observed running.
- External drives were not included in cleanup targets and were not modified.

## Bottom line

The biggest cleanup opportunity is the **296 GB dated ComfyUI backup**, followed by **23 GB of user caches**, **3.9 GB of logs**, **7.5 GB of Downloads**, and the **10 GB test image**. The safe approach is staged review and cache/log cleanup first, then an explicit model/archive decision. llama.cpp and ComfyUI should remain online and untouched until that decision is complete.

---
tags: [benchmarking, automation, reliability, spark-infra, mps, cuda, incident-followup]
status: proposed
owner: Herm + Sparkbot
created: 2026-09-17
related: ["[[Automation Reliability Runbook]]", "[[Session Log 2026-09-17 — Spark MPS Wedge Incident]]"]
---

# Plan — Integrate MPS-wedge detection & dynamic recovery into the benchmark routine

## Why this plan exists

On **2026-09-16 18:58** (benchmark start) the Spark's NVIDIA **MPS** daemon
(`nvidia-cuda-mps-server`) entered `Server teardown in progress` and never
recovered. For the next ~14 h it rejected **every** CUDA client with
`status 807` (llama-server, ComfyUI, fish-speech). Production `:8014` stayed
UP — `/health` = 200, model alias unchanged, process argv unchanged — but
llama-server had silently reloaded the whole 27B model **on CPU**
(`ggml_cuda_init: failed... MPS server is not ready` → `no usable GPU found,
--gpu-layers option will be ignored`). Result: ~8× slowdown (small-reply
latency 3.9 s vs 0.30 s; gen 2.7 tok/s vs 17.9; GPU util 6 % vs 95 %). It was
found only because AJ noticed Agora was slow. Full incident write-up:
[[Session Log 2026-09-17 — Spark MPS Wedge Incident]].

**The gap:** the reliability runbook's "Production health degrades" detection
is `/health` + alias + process comparison. **None of those catch a CPU
fallback** — the port answers, the alias matches, the argv matches. Health
check said "healthy" for 14 h while throughput was destroyed.

## Design principles

1. **Detection is read-only and cheap** — safe to run every preflight tick and
   after every benchmark, on production, without disturbing it.
2. **Recovery is a PRODUCTION service change** → per the runbook it is
   *human-required / flagged*, never silent unattended remediation. It runs
   only behind an explicit `--confirm` and reports PASS/FAIL by re-probing.
3. **Verify the fix, never assume it.** Recovery re-runs the GPU-backing probe
   and only reports success on GPU util ≥ 40 % + gen ≥ 8 tok/s.
4. **The benchmark harness must not *cause* the wedge** — add MPS teardown at
   benchmark end so the nightly run stops poisoning every CUDA service.

## Deliverables (built & deployed 2026-09-17, read-only + gated)

Both live on the Spark in `~/llm-benchmark-runner/` (the harness dir):

### 1. `gpu_backing_probe.py` — detection (exit 0 healthy / 2 degraded / 3 unreachable)
- Fires one tiny thinking-off generation with `timings_per_token:true` while
  sampling `nvidia-smi --query-gpu=utilization.gpu` in a background thread.
- Degraded verdict if `predicted_per_second < 8` (CPU-class; healthy ~18) **or**
  `max_gpu_util < 40 %` during generation (healthy ~95 %, wedge ~6 %).
- Emits a JSON report (endpoint, gen_tps, prompt_tps, max_gpu_util_pct,
  degraded, reasons). **Verified 2026-09-17:** on the healthy box → gen 11.6
  tok/s, GPU 96 %, exit 0.
- Thresholds are deliberately wide (8 / 40) — a clean CPU-vs-GPU divider, not a
  tight regression gate, so ordinary load variance never false-positives.

### 2. `mps_recover.py` — gated recovery (dry-run by default)
- No `--confirm` → prints the 5-step plan and exits 0, executing nothing
  (verified). With `--confirm`:
  1. Refuses unless `nvidia-smi ... compute_mode == Default` (EXCLUSIVE_PROCESS
     makes MPS mandatory; a naive reset there would break clients).
  2. `echo quit | timeout 8 nvidia-cuda-mps-control` (may hang → timeout ok).
  3. `pkill` surviving mps-server/-control; clear `/tmp/nvidia-mps/*`
     `/tmp/nvidia-log/*`; `nvidia-cuda-mps-control -d`.
  4. `systemctl --user restart llama-server.service`; wait for `/health` 200.
  5. Re-run `gpu_backing_probe.py`; report **RECOVERY PASS** only on probe
     exit 0, else **RECOVERY INCOMPLETE → escalate to AJ**.

## Integration into the ownership/cadence table

Add these to [[Automation Reliability Runbook]] (rows, not rewrites):

| When | Owner | Action | Rule |
|---|---|---|---|
| 02:30 preflight | Sparkbot | Run `gpu_backing_probe.py` as part of **production preflight**, before acquiring a candidate | If degraded → do NOT start a run; write BLOCKED with the probe report; post a Townhall finding tagged `mps`/`cuda` and page Herm. Do not auto-`--confirm` recover during an unattended slot. |
| End of 04:00 run | Sparkbot | **MPS teardown** in the benchmark cleanup path: after the isolated run, `echo quit \| nvidia-cuda-mps-control` (+ pipe clear) if the harness started MPS, so a wedged MPS never survives into the day | This addresses the ROOT cause. Never touch production llama-server as part of this. |
| 06:30 QC | Sparkbot | Include GPU-backing verdict (gen_tps + GPU util) in the QC note, not just `/health` | A run whose production probe shows CPU fallback is BLOCKED, never PASS. |
| Morning | Herm | On a degraded probe, run `mps_recover.py --confirm` (a flagged production action), verify PASS via re-probe, log to vault + Townhall | Recovery stays Herm-driven (human-in-loop), matching the runbook's "production service changes are human-required". |

## New failure-matrix row (for the runbook)

| Failure | Detection | Automatic response | Escalation/stop rule |
|---|---|---|---|
| **Wedged MPS → silent CPU fallback** (server UP, `/health` 200, alias/argv unchanged, but gen ~2.7 tok/s & GPU util ~6 %) | `gpu_backing_probe.py`: gen_tps < 8 or GPU util < 40 % during a live token; corroborate with `journalctl --user -u llama-server.service` for `no usable GPU found` | Preflight → write BLOCKED, don't run, page Herm. Herm → `mps_recover.py --confirm`, then re-probe to confirm GPU-backed | Never auto-`--confirm` in an unattended slot (production restart = human-required); never treat `/health` 200 as proof of GPU-backing |

## Open decisions for AJ

- **Auto-recover vs page-only?** Current plan: Sparkbot detects & blocks, Herm
  runs the gated recovery. If you want *fully* autonomous overnight recovery,
  we'd need to relax the "production restart is human-required" invariant for
  this specific, well-characterised case — I'd want your explicit sign-off
  before crossing that line.
- **Add MPS teardown to the harness now?** Requires locating exactly where the
  04:00 run brings MPS up (the harness that faulted on 09-16) and adding a
  `finally:` teardown. Ready to do this on your go.
- Should the probe also guard **ComfyUI/fish-speech** (same MPS blast radius),
  or is llama-server (:8014) the only one worth gating nightly?

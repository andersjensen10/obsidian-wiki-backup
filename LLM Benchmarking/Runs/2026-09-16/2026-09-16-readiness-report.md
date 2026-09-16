---
tags: [benchmarking, readiness, acquisition, spark-infra]
status: complete
run_date: 2026-09-16
---

# Readiness and acquisition — 2026-09-16

**Status: COMPLETE for readiness/acquisition. Benchmark: NOT RUN at this stage.**

## Selected candidate

The exact next candidate recorded in the latest research note was acquired: `Qwen/Qwen3.6-35B-A3B` via `unsloth/Qwen3.6-35B-A3B-MTP-GGUF`.

- Immutable revision: `5bc3e238d916f48a861bac2f8a1990a0e9b7e98d`
- File: `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`
- Quantization: `UD-Q4_K_M (imatrix)`
- Expected and actual size: `22,663,387,424` bytes
- SHA-256: `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b`
- License: Apache-2.0
- Source: https://huggingface.co/unsloth/Qwen3.6-35B-A3B-MTP-GGUF/resolve/5bc3e238d916f48a861bac2f8a1990a0e9b7e98d/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf

The downloaded file passed exact byte-size and SHA-256 verification, had GGUF magic, and was not an LFS pointer. It was atomically promoted from SSD quarantine to `/home/aj/llm-benchmark-local/models/Qwen3.6-35B-A3B-UD-Q4_K_M/`. The immutable manifest is `/home/aj/llm-benchmark-local/manifests/qwen3.6-35b-a3b-2026-09-16.json`.

## Profile and gates

An isolated loopback profile is active on port `8015`; production port `8014` was not restarted or modified. The candidate loaded successfully with llama.cpp-fastmtp build 931, commit `4df29be`, context `32768`, one slot, `--jinja`, `--reasoning off`, and `--reasoning-budget 0`. `/health` returned `{"status":"ok"}` and an OpenAI-compatible smoke request returned the non-empty visible answer `READY`.

Host headroom after load was 8,406,528,000 bytes available; SSD free space was 200,998,465,536 bytes. The fit gate is based on successful load, health, and visible-answer smoke verification; GPU memory accounting is unsupported by this GB10 driver (`nvidia-smi` reports memory not supported).

Runner tests passed: `3 passed in 0.00s`. The locked suite is present at version `1.0.0` with all 10 cases. Production health remained `{"status":"ok"}` after candidate startup, with the existing production process and alias unchanged.

## Toshiba archival blocker

No candidate, run artifact, or log was written to Toshiba. Archival remains blocked because kernel evidence still contains `ntfs3(sdb1): MFT: r=279cb, expect seq=1 instead of 0!` from 2026-09-15 04:00:38, repeated at 07:13:55. The verified SSD copy is retained. A clean filesystem-health gate and the required quarantine → checksum → atomic-promotion archival flow are still required before Toshiba use.

## Next stage

The 04:00 benchmark stage may consume the single slot only if it keeps the active isolated profile, uses the internal SSD for raw artifacts/logs, and preserves production health. This readiness artifact does not claim benchmark quality or promotion.

Machine-readable artifact: `Runs/2026-09-16/readiness.json`.

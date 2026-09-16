---
tags: [benchmarking, complete, verification, spark-infra]
status: complete
run_date: 2026-09-16
suite_version: 1.0.0
candidate: Qwen3.6-35B-A3B-UD-Q4_K_M
---

# Nightly benchmark — 2026-09-16 04:00

**Status: COMPLETE; verifier PASS. Promotion: NOT APPROVED.**

## Candidate and provenance

- Repository: `unsloth/Qwen3.6-35B-A3B-MTP-GGUF` (`Qwen/Qwen3.6-35B-A3B` base)
- Immutable revision: `5bc3e238d916f48a861bac2f8a1990a0e9b7e98d`
- Quantization: `UD-Q4_K_M (imatrix)`
- Expected size: `22,663,387,424` bytes
- Readiness SHA-256: `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b`
- Benchmark source: `/home/aj/llm-benchmark-local/models/Qwen3.6-35B-A3B-UD-Q4_K_M/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`
- Isolated profile: `/home/aj/llm-benchmark-local/server-profiles/qwen3.6-35b-a3b-2026-09-16`
- Command: `/home/aj/llama.cpp-fastmtp/build/bin/llama-server --alias qwen3.6-35b-a3b-ud-q4km --host 127.0.0.1 --port 8015 --ctx-size 32768 --gpu-layers all --parallel 1 --jinja --reasoning off --reasoning-budget 0 --model /home/aj/llm-benchmark-local/models/Qwen3.6-35B-A3B-UD-Q4_K_M/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`
- Runtime: llama.cpp-fastmtp build 931, commit `4df29be`

## Mechanical result

Locked Suite `1.0.0` completed all 10 cases at C1/C2/C4: **30 groups, 70 streamed samples, 0 request errors, 0 empty visible responses, 0 missing visible TTFT**.

| Level | Samples | Visible TTFT p50 / p95 | Latency p50 / p95 | Generation tok/s p50 / p95 |
|---|---:|---:|---:|---:|
| C1 | 10 | 0.150 / 0.436 s | 2.554 / 6.205 s | 60.71 / 65.76 |
| C2 | 20 | 0.369 / 5.868 s | 3.055 / 11.492 s | 61.81 / 63.02 |
| C4 | 40 | 2.421 / 12.974 s | 5.087 / 18.657 s | 62.04 / 65.43 |

C4 is stress/queueing evidence; it is not a promotion gate. Coding quality, structured-output validity, and visible-answer review remain separate from these mechanical metrics.

## Artifact verification

- Raw JSON: `/home/aj/llm-benchmark-local/runs/2026-09-16/raw.json`
- Raw SHA-256: `12ecf9b5cf2090ce2f2c4650da45e7d47a004b62e4d3c129c0c82a7dd4399c96`
- Independent verifier: `/home/aj/llm-benchmark-runner/verify_run.py` — `verified: true`, 30 results
- Hash file: `/home/aj/llm-benchmark-local/runs/2026-09-16/raw.sha256`
- Host evidence: `/home/aj/llm-benchmark-local/runs/2026-09-16/host-state-post.txt`
- Server log: `/home/aj/llm-benchmark-local/runs/2026-09-16/isolated-server.log`

## Safety and storage

Production was captured healthy before launch and remained untouched. After the run, isolated port `8015` was no longer listening; production `:8014/health` returned `{"status":"ok"}` and `/v1/models` still identified `qwen3.8-27b-aggressive-q5`. No restart, swap, or promotion occurred.

A fresh Toshiba read-only preflight found the volume mounted at `/media/aj/TOSHIBA EXT1` with 977,833,627,648 bytes available, but kernel logs still contain repeated `ntfs3(sdb1): MFT: r=279cb, expect seq=1 instead of 0!` warnings. Archival is therefore **BLOCKED**. The verified SSD model and raw artifacts remain on internal SSD; no Toshiba writes were attempted.

Dashboard ingest was not attempted because `/home/aj/.benchmark-dashboard.env` has no configured API URL. No dashboard record is claimed.

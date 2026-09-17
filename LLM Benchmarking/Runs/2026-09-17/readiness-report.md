# Local-LLM readiness report — 2026-09-17

**Status: BLOCKED**

## Selected candidate

The latest dated research note records `Qwen/Qwen3.6-35B-A3B` as the next candidate, using `unsloth/Qwen3.6-35B-A3B-MTP-GGUF`, revision `5bc3e238d916f48a861bac2f8a1990a0e9b7e98d`, file `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`, `UD-Q4_K_M (imatrix)`, expected size `22,663,387,424` bytes, Apache-2.0. No substitute was used.

## Gate results

- **Metadata: PASS.** Existing manifest records the repository, immutable revision, filename, quantization, source URL, license, expected size, and SHA-256. The Hugging Face revision metadata confirmed the expected size and LFS SHA-256.
- **Acquisition/quarantine: FAIL.** The 2026-09-17 SSD quarantine file is only `4,464,275,456` bytes of `22,663,387,424` expected (`Qwen3.6-35B-A3B-UD-Q4_K_M.gguf.partial`). The download was stopped before completion; no download-completion claim is made.
- **Existing SSD artifact: verified separately.** The already-promoted model is exactly `22,663,387,424` bytes with SHA-256 `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b`, and is not an LFS pointer (starts with GGUF magic `GGUF`). This does not clear today's incomplete acquisition gate.
- **Isolated profile: prior verification only.** Profile `qwen3.6-35b-a3b-2026-09-16` is loopback-only on port 8015, points to the SSD model path, documents reasoning off / budget 0 and fail-closed visible answers, and leaves production on port 8014. A fresh runtime verification was not completed because current CUDA initialization reported: `MPS server is not ready to accept new MPS client requests`.
- **Runner: PASS.** `pytest -q /home/aj/llm-benchmark-runner` returned `3 passed in 0.00s`.
- **Locked suite: not run.** Suite metadata is v1.0.0 with 10 cases, but no candidate benchmark was launched because readiness is blocked.
- **Production health: PASS.** `192.168.0.139:8014/health` returned `{"status":"ok"}`. No production restart or configuration change occurred.
- **Storage: SSD only.** Internal SSD had `225,518,690,304` bytes free during the check. Toshiba archival remains blocked: kernel logs contain `ntfs3(sdb1): MFT: r=279cb, expect seq=1 instead of 0!` on 2026-09-15. No Toshiba write was attempted.

## Blockers

1. The selected candidate's 2026-09-17 acquisition is incomplete and size/SHA-256 verification cannot pass.
2. Current llama.cpp CUDA/MPS initialization is not ready, so fresh candidate fit/headroom and isolated-server readiness cannot be verified.
3. Toshiba's NTFS/MFT warning remains unresolved; the verified SSD copy is retained and no archival copy was attempted.

Raw acquisition output and model files remain on the internal SSD. Production was not launched, restarted, or replaced. Benchmark slot was not consumed.

Machine-readable status: [`readiness.json`](./readiness.json)

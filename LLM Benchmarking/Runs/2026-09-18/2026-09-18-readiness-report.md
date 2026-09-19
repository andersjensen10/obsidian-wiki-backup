# Readiness and acquisition report — 2026-09-18 02:30

## Status: BLOCKED

The selected candidate is **Qwen/Qwen3.6-35B-A3B**, using `unsloth/Qwen3.6-35B-A3B-MTP-GGUF`, revision `5bc3e238d916f48a861bac2f8a1990a0e9b7e98d`, file `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`, quantization `UD-Q4_K_M (imatrix)`, expected size `22,663,387,424` bytes, Apache-2.0. The selection came from `Research/2026-09-17.md`; no substitute was used.

Acquisition completed on Spark's internal SSD. The downloaded file matched the source metadata at the immutable Hugging Face revision: size `22,663,387,424` bytes and SHA-256 `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b`. It was confirmed not to be an LFS pointer, written to the read-only manifest `manifests/qwen3.6-35b-a3b-2026-09-18.json`, and atomically promoted into `models/Qwen3.6-35B-A3B-UD-Q4_K_M/`.

A dedicated loopback profile was created on port 8015 with the model path on the internal SSD. Reasoning is explicitly off with budget 0, and the visible-answer policy fails closed on empty content. The server loaded the model, returned health OK, and passed a smoke request with non-empty visible output (`READY.`). Production port 8014 returned `{"status":"ok"}` and was not restarted or modified.

Runner tests passed (`3 passed in 0.00s`), the locked suite contains version `1.0.0` and 10 cases, and llama.cpp reports build 931, commit `4df29be`. The benchmark was not launched because readiness did not clear.

## Blocking evidence

The server log records a successful load and smoke response but also `common_fit_params: failed to fit params to free device memory: n_gpu_layers already set by user to -2, abort`. `nvidia-smi` detects `NVIDIA GB10` but reports GPU memory totals and usage as `N/A`; independent GPU headroom is therefore not verified. Status remains BLOCKED rather than COMPLETE.

Toshiba archival is separately blocked. The latest candidate-selection note records an unresolved NTFS MFT warning. The candidate and raw run artifacts remain on the internal SSD; no Toshiba write was attempted.

Raw readiness JSON: `Runs/2026-09-18/readiness.json`.

# Verified E2E benchmark - 2026-09-14

Status: PASS - transport and visible-output gate

## Execution

- Suite: locked v1.0.0
- Model: `qwen3.8-27b-aggressive-q5-e2e-visible`
- Endpoint: isolated `127.0.0.1:8015`; production `:8014` was not used
- Matrix: 10 cases x C1/C2/C4 = 30 result groups, 70 streamed samples
- Results: 70/70 successful, 0 empty visible responses, 0 missing TTFT
- Isolated profile: reasoning disabled so visible-answer behavior is measured and not confused with hidden reasoning output

## Aggregate timing observations

| Level | Samples | Latency p50/p95 (s) | TTFT p50/p95 (s) | Generation tok/s p50 |
|---|---:|---:|---:|---:|
| C1 | 10 | 15.90 / 43.14 | 0.41 / 0.44 | 8.23 |
| C2 | 20 | 19.87 / 74.25 | 1.24 / 37.75 | 8.35 |
| C4 | 40 | 32.89 / 139.43 | 15.71 / 93.78 | 8.44 |

C4 is stress data on the one-slot isolated profile and shows queueing as expected; it is not a promotion gate.

## Integrity and safety

- Independent verifier: PASS
- SHA-256: `a11f21f5266fca48de72dc52763079173115948306d2e18a45005c49fc353c75`
- Checksum manifest: `LLM Model Library/runs/2026-09-14-e2e/SHA256SUMS`
- Failed first run retained separately at `LLM Benchmarking/Runs/2026-09-14/2026-09-14-e2e-quality-failure.md`
- Production health after test: HTTP 200; model alias unchanged at `qwen3.8-27b-aggressive-q5`
- Isolated server stopped after collection

This verifies the end-to-end runner, artifact path, streaming capture, C1/C2/C4 matrix, visible-output gate, checksum, and production protection. It is a baseline harness validation, not candidate promotion; semantic coding/JSON scoring remains a separate review gate.

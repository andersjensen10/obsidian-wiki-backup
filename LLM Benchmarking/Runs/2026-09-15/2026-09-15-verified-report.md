---
tags: [benchmarking, complete, project/llm-benchmarking, qwen3-coder, spark-infra, type/benchmark-run]
status: complete
run_id: 2026-09-15-candidate-qwen3-coder
suite_version: 1.0.0
---

# Verified candidate benchmark - 2026-09-15

## Result

The selected `Qwen3-Coder-30B-A3B` `Q4_K_M` candidate was fully downloaded and tested from Spark internal SSD. The candidate was served only through isolated llama.cpp on `127.0.0.1:8015`, with reasoning disabled and one server slot. Production Qwen on `:8014` was not restarted, swapped, or used for benchmark traffic.

- Repository: `AtomicChat/Qwen3-Coder-30B-A3B-GGUF`
- Revision: `ff153c4367a722a7bc4ea5d076be3d8a0721dad0`
- File: `qwen3-coder-30b-a3b-Q4_K_M.gguf`
- Size: `18,556,688,416` bytes
- Model SHA-256: `22e70e6305c8fa5ea0bbbdf11fa6f1779b5546b33dd38da2c2274b5e5d574b5`
- Suite: v1.0.0, 10 cases at C1/C2/C4
- Samples: 70/70 successful
- Empty visible responses: 0
- Missing TTFT: 0
- Independent verifier: PASS
- Raw artifact SHA-256: `a7cd7ca682a7a35774396e5b515d5166812733ec5020f7c723de55bab025615d`

## Throughput snapshot

| Level | Samples | Latency p50 / p95 (s) | TTFT p50 / p95 (s) | Generation p50 (tok/s) |
|---|---:|---:|---:|---:|
| C1 | 10 | 1.85 / 6.21 | 0.085 / 0.239 | 59.29 |
| C2 | 20 | 2.57 / 11.42 | 0.194 / 5.82 | 59.64 |
| C4 | 40 | 3.92 / 19.80 | 1.82 / 13.36 | 59.80 |

C4 is stress-only on the one-slot profile. Semantic coding quality, structured-output scoring, visible-output review, and promotion remain separate gates; this run does not auto-promote the candidate.

## Storage and handoff

The verified model, manifest, and raw run remain on `/home/aj/llm-benchmark-local` on the internal SSD. Toshiba archival was not attempted because the NTFS MFT warning has not been cleared by a fresh filesystem-health gate. No unsafe write or forced repair was performed.

Dashboard record: `2026-09-15-candidate-qwen3-coder`, status `complete`, idempotency key `spark-2026-09-15-candidate-qwen3-coder`; POST and GET read-back verified.

## Agora preparation — 2026-09-29

A non-active Spark service preset has been prepared at `~/.config/llama-server.env.qwen3-coder-30b-a3b`, with the verified model path and a **131,072-token total context** split across **two slots** (**65,536 tokens per chat**). The selector `/home/aj/bin/llama-model-select` provides `qwen3-coder` and `qwen3.8` commands and makes a timestamped backup before restarting the user-level llama.cpp service. `status` confirmed production remains `qwen3.8-27b-aggressive-q5` and the service is active.

This is an operationally ready, reversible candidate, not a production promotion. The 65K/two-slot profile has not yet been live-loaded or quality-tested for Agora's adult-roleplay use; the earlier verified benchmark was a 32K/one-slot, coding-focused run. A controlled swap and Agora-specific quality/throughput test remain required before routing personas to it.

## Related notes
- [[LLM Benchmarking/README|LLM Benchmarking overview]]

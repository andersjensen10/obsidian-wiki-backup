---
tags: [benchmarking, local-llm, spark-infra]
status: setup-in-progress
---

# Local LLM Benchmarking

Purpose: build a measured, curated library of general-use local LLMs for the Spark, with emphasis on 25B–150B models suitable for daily agentic coding and catch-all use.

## Operating rules

- One full benchmark run per night; make the selected session count.
- Never benchmark against a moving target: record model revision, quantization, llama.cpp commit, server flags, GPU/runtime state, and benchmark-suite revision.
- Measure real OpenAI-compatible server behavior, not only `llama-bench` microbenchmarks.
- Include concurrency because Agora and other LAN agents share the server.
- Keep raw JSON results immutable; write human summaries separately.
- Do not replace the production model automatically. Candidate promotion requires review and a verified rollback path.
- Model storage belongs on the Toshiba external drive, not the system disk.

## Folder map

- [[Benchmark Suite]] — locked prompts, workload definitions, scoring and pass/fail rules.
- [[Candidate Selection]] — nightly research and selection policy.
- [[Storage and Runtime]] — Toshiba library layout and reproducible server profiles.
- [[Benchmark PRD — Kitchen Wall Insights]] — dashboard product requirements for Herm.
- `Runs/YYYY-MM-DD/` — one run's raw results, environment snapshot, logs and report.
- `Models/` — metadata and manifests only in the vault; model files live on Toshiba.
- `Research/` — dated Hugging Face trend snapshots and candidate decisions.

## Current baseline

Production candidate: `qwen3.8-27b-aggressive-q5` on Spark llama.cpp at `192.168.0.139:8014`, currently configured with two parallel slots. AJ reports it is brilliant for its size, strong for general chat, and uncensored; the gap to investigate is local programming and agentic coding capability at acceptable cost.

## Setup status

- Vault structure: created.
- Locked suite: created.
- Toshiba storage: **available at `/media/aj/TOSHIBA EXT1`** with approximately 911 GB free. The library is present and a temporary write/read/delete test passed. Automation must use the active `EXT1` mountpoint; continue monitoring for new I/O errors.
- Temporary Spark storage: `/home/aj/llm-benchmark-local/` remains available as fallback.
- Benchmark runner: initial real HTTP streaming harness is ready at `/home/aj/llm-benchmark-runner`; smoke-tested against the live Qwen endpoint with TTFT and generation throughput, plus passing unit tests.
- Automated candidate research: scheduled daily at 18:00.
- Nightly benchmark orchestration: scheduled for 04:00 using temporary local storage until Toshiba is healthy; it runs one candidate and starts the next download only after a successful completed run.

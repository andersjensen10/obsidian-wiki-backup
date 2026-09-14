---
tags: [benchmarking, local-llm, spark-infra]
status: active
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
- Failed and blocked runs remain visible in the dashboard but are never ranked or promoted.

## Folder map

- [[Benchmark Suite]] — locked prompts, workload definitions, scoring and pass/fail rules.
- [[Candidate Selection]] — nightly research and selection policy.
- [[Storage and Runtime]] — Toshiba library layout and reproducible server profiles.
- [[Benchmark PRD — Kitchen Wall Insights]] — dashboard product requirements for Herm.
- [[Automation Reliability Runbook]] — ownership, cadence, failure matrix, recovery, and escalation rules.
- `Runs/YYYY-MM-DD/` — one run's raw results, environment snapshot, logs and report.
- `Models/` — metadata and manifests only in the vault; model files live on Toshiba.
- `Research/` — dated Hugging Face trend snapshots and candidate decisions.

## Ownership and cadence

- **02:30 — Sparkbot:** readiness, storage, candidate, checksum, runner, and isolated-server preflight.
- **04:00 — Sparkbot:** one isolated full benchmark; production Qwen remains untouched.
- **06:30 — Sparkbot:** independent verification, checksum, QC, and blocker review.
- **07:00 — Sparkbot:** one idempotent dashboard record per run, read-back verification, and Townhall handoff.
- **Morning — Herm:** Kitchen Wall Insights revision, browser verification, and dashboard/process coordination.
- **18:00 — Sparkbot:** cited candidate research and selection of exactly one eligible next candidate.
- **Day 7 — Herm + Sparkbot:** consolidated reliability and process review for AJ.

The automation fails closed: unhealthy storage, missing/checksum-failed candidates, runner/server/SSE failures, empty visible outputs, production degradation, dashboard/Townhall outage, scheduler loss, and reboot/power loss are recorded with evidence rather than hidden or converted into false success. It does not create catch-up benchmark batches or silently alter the locked suite.

## Current baseline

Production candidate: `qwen3.8-27b-aggressive-q5` on Spark llama.cpp at `192.168.0.139:8014`, currently configured with two parallel slots. AJ reports it is brilliant for its size, strong for general chat, and uncensored; the gap to investigate is local programming and agentic coding capability.

## Verified first E2E run

The first complete pipeline validation is recorded in [[Runs/2026-09-14/2026-09-14-e2e-verified]]. It used the locked v1.0.0 suite against an isolated one-slot server profile with reasoning disabled for visible-answer reliability:

- 10 workloads at C1/C2/C4: 30 result groups and 70 streamed samples.
- 70/70 successful samples, 0 empty visible responses, 0 missing TTFT.
- Independent verifier passed.
- SHA-256: `a11f21f5266fca48de72dc52763079173115948306d2e18a45005c49fc353c75`.
- Production Qwen health and alias were unchanged after the run; isolated server was stopped.
- C4 is stress-only on the one-slot profile; this is harness validation, not candidate promotion or semantic quality scoring.

The earlier reasoning-enabled run failed the visible-output gate and is preserved in [[Runs/2026-09-14/2026-09-14-e2e-quality-failure]] rather than being overwritten.

## Setup status

- Vault structure and locked suite: created.
- Toshiba storage: available at `/media/aj/TOSHIBA EXT1` with approximately 911 GB free. Automation uses the active `EXT1` mountpoint and monitors for new I/O errors.
- Temporary Spark storage: `/home/aj/llm-benchmark-local/` remains available as a health-checked fallback.
- Benchmark runner: ready at `/home/aj/llm-benchmark-runner`; `verify_run.py` enforces suite version, complete C1/C2/C4 coverage, non-empty visible outputs, and TTFT.
- Readiness/acquisition, benchmark, QC, and dashboard-handoff jobs: active.
- Kitchen Wall Insights: live and seeded with the verified first run.

## Integration credentials and onboarding lesson

Townhall transport and benchmark-dashboard ingest are separate integrations with separate credentials. Spark's mode-600 `/home/aj/.townhall.env` handles Townhall; the dashboard handoff uses mode-600 `/home/aj/.benchmark-dashboard.env` with the shared dashboard token. The token value is never stored in the vault, Townhall, logs, or chat.

The dashboard ingest path has been verified with an idempotent replay returning HTTP 200 and a GET read-back matching run ID, status, idempotency key, and checksum. Future runs are posted once at 07:00, including failed and blocked runs, and retried only with the same idempotency key.

For future agent onboarding, verify each service independently: endpoint, identity, project scope, environment variable, secret-file path, owner, permissions, and a non-secret read/write test. Never infer access to one service from successful access to another.

## Coordination record

Sparkbot and Herm coordinate benchmark findings, dashboard revisions, and process adjustments through Townhall under `spark-infra`. The first-week objective is a robust unattended loop with honest blocker visibility, reproducible artifacts, verified dashboard ingestion, and a joint day-7 follow-up for AJ.

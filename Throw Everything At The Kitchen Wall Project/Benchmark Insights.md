---
tags: [kitchen-wall, benchmarking, insights, spark-infra]
status: live
---

# Benchmark Insights on the Kitchen Wall

Live scene at `/insights` on the Kitchen Wall dashboard. Implements
`LLM Benchmarking/Benchmark PRD — Kitchen Wall Insights.md`, the PRD Sparkbot
prepared for Herm on 2026-09-13. Shipped 2026-09-14 (commit `a46c473`).

## What it is

A read-only surface showing the nightly local-LLM benchmark runs Sparkbot
publishes from the Spark box: latest run status, headline C1 metrics, a trend
chart across runs, a model comparison table, run history, and prominent
blocker/stale/mixed-suite alerts.

## The honesty rules (why this scene looks sparse at first)

This surface was deliberately built to under-claim. These are enforced in code,
not conventions:

- **A run with no semantic quality scoring renders "not scored"**, never a
  number. The ingest API *rejects* a payload claiming `quality.scored: true`
  with no measured pass rate.
- **Below two verified runs the trend panel refuses to draw a line** and says
  "one verified run so far". A single point is plotted mid-height as a
  reference, with no implied slope.
- **Only `status: complete` AND `verifier: pass` runs are ranked.** Failed and
  blocked runs are stored and displayed — marked unverified — but never appear
  as leaderboard entries.
- **Mixed suite versions raise a visible warning** rather than silently merging
  incomparable numbers.
- **Stale data is flagged** when the newest run is older than 36 h against the
  expected 24 h nightly cadence.

The first run rendering as "not scored / one verified run so far" is the scene
working correctly, not an unfinished state.

## Current data (as of 2026-09-21)

Nine stored runs: three verified complete runs and six blocked readiness/artifact
attempts. The latest run, `2026-09-21-qc-0630`, is blocked/not-run: readiness
fell back to 2026-09-18, no same-day report or raw artifacts were present, and
systemd reported `llama-server.service` inactive while a separate PID served
HTTP 200. The latest verified run remains `2026-09-16-qwen3.6-35b-a3b` at
150 ms C1 TTFT p50, 60.71 tok/s, and 100% visible-response reliability.
Quality remains unscored for all runs; C4 remains `stressOnly: true` and is not
a promotion gate. All runs are suite v1.0.0, so no mixed-suite warning is
needed.

The scene now surfaces the trailing blocked streak as pipeline health: five
consecutive blocked runs are visible separately from model ranking. This keeps
the wall honest about the lack of fresh benchmark evidence without treating
readiness failures as model scores.

## Seven-day iteration summary (2026-09-15–2026-09-21)

The scene progressed from a sparse single-run view to a trend/leaderboard with
three verified points, adaptive interaction checks, run-health coverage, and
explicit blocker visibility. The accumulated mechanical data shows the two
newer verified candidates near 59–61 tok/s versus the qwen3.8 baseline at 8.23
tok/s, with C1 TTFT improving from 410 ms to 85 ms and then 150 ms. Those
numbers are harness measurements only: semantic quality is still unscored and
no promotion decision is justified. The next priority is fixing the benchmark
readiness/artifact pipeline and reconciling service-manager state with the
serving PID before adding more visual metrics.

## Ingest

`POST /api/benchmarks`, guarded by a shared secret in the `x-benchmark-token`
header. Full contract: `BENCHMARK-INGEST.md` in the kitchen-dashboard repo.
Secrets live in the repo's gitignored `.env.local` (which also carries the
Townhall trusted-agent token) — **the dev server must be launched with that file
sourced** or both Townhall posting and benchmark ingest break.

Sparkbot posts once per run at run end, including failed and blocked runs.
A successful ingest publishes a `benchmark.completed` realtime event.

## Iteration plan

AJ commissioned a 7-day daily revision cycle (cron `7e960844a977`, 08:15 daily,
7 runs, starting 2026-09-15): each morning re-tune the presentation to the
growing dataset, verify in a real browser, commit. On day 7 the job asks AJ for
an overall evaluation and whether the dashboard is done or needs another week.

## Verification tooling built alongside

- `scripts/verify-wall-fit.mjs` — CDP viewport-fit + console/exception drain at
  exactly 1920×1080, across every route. Skips elements clipped by a scrolling
  ancestor (per-panel internal scroll is allowed; page scroll is not).
- `scripts/verify-insights-interaction.mjs` — drives real dispatched mouse input
  and adapts its assertions to how much verified data exists.
- `scripts/audit-geometry.mjs` — per-panel fill percentage, used instead of
  eyeballing screenshots. Caught the metrics panel sitting at 33% fill at data
  volume because a shared grid row was sized by the growing leaderboard.

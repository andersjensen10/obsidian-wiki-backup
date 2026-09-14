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

## Current data (as of 2026-09-14)

One run: `2026-09-14-e2e-verified`, Sparkbot's harness-validation E2E.
410 ms C1 TTFT p50, 8.23 tok/s, 100% answer reliability, suite v1.0.0,
SHA-256 `a11f21f5…`, promotion state `not-evaluated`, quality unscored.
C4 carries `stressOnly: true` — it showed queueing on the one-slot profile and
is explicitly not a promotion gate.

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

---
tags: [prd, benchmarking, kitchen-wall, spark-infra]
status: draft-for-herm
---

# PRD — Local LLM Benchmark Insights on the Kitchen Wall

## Owner and handoff

Prepared by Sparkbot for Herm. The Kitchen Wall should present benchmark evidence without implying that a model is production-ready merely because it is fast.

## Problem

Nightly local-LLM benchmarks produce raw results that are difficult to compare, so AJ cannot quickly decide which model is a viable daily driver for agentic coding and general chat.

## Goal

Expose a trustworthy, concise view of benchmark freshness, candidate ranking, quality gates, throughput under concurrency, and promotion state.

## MVP requirements

1. Show the latest run status: model, quantization, suite version, run time, complete/failed, and raw-report link.
2. Show candidate leaderboard with aggregate score, coding pass rate, structured-output validity, general-chat success, C1/C2/C4 generation throughput, TTFT, p95 latency, and error rate.
3. Show comparison against the Qwen 3.8 baseline.
4. Show storage/model readiness: downloaded, checksum verified, runner-ready, quarantined, or unavailable.
5. Show the next selected candidate and the evidence/reason it was selected.
6. Distinguish measured facts, human qualitative review, and inferred recommendation.
7. Show blockers prominently: dirty/unmounted storage, missing model, failed run, server capacity, or stale results.
8. Provide links to the full raw JSON and dated Obsidian report.

## Non-goals

- No automatic production promotion.
- No hidden quality score that obscures raw metrics.
- No dashboard-side model downloading or service restart in MVP.
- No mixing results from different suite versions without an explicit compatibility label.

## Acceptance criteria

- A visitor can identify the latest complete run and its model in under 10 seconds.
- A visitor can compare any candidate with Qwen 3.8 at C1 and C2 without opening raw logs.
- Failed or incomplete runs cannot appear as successful leaderboard entries.
- Dashboard values link to immutable raw artifacts and display suite version and environment fingerprint.
- A storage or runner blocker is visible before a user attempts a benchmark or promotion.
- Herm can implement against a documented JSON schema produced by the runner.

## Proposed data contract

```json
{
  "runId": "YYYY-MM-DD-model-slug",
  "status": "complete|failed|blocked",
  "model": {"repo": "", "revision": "", "file": "", "quantization": "", "parameters": ""},
  "suiteVersion": "1.0.0",
  "environment": {"llamaCppCommit": "", "serverProfile": "", "gpu": "", "ctx": 0, "parallel": 0},
  "metrics": {"c1": {}, "c2": {}, "c4": {}},
  "quality": {"chat": {}, "coding": {}, "structured": {}, "safety": {}},
  "artifacts": {"raw": "", "report": "", "checksum": ""},
  "baselineComparison": {},
  "selection": {"score": 0, "reason": "", "promotionState": "candidate|reviewed|approved|rejected"}
}
```

## Handoff request

Herm: please review this PRD and build the Kitchen Wall benchmark-insights surface when the runner schema and first verified benchmark report are available. Please alert AJ when setup is complete and the first benchmark has finished. Coordinate any schema or dashboard questions through Townhall.

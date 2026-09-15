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

Expose a trustworthy, concise view of benchmark freshness, candidate ranking, quality gates, throughput under concurrency, promotion state, and the capability coverage of the local model library. The library is multi-track: no single text leaderboard should hide the best vision, audio, video, or MoE specialist.

## Library requirements

1. Classify each model by capability track: general/agentic text, MoE efficiency, vision/image, audio, video/transcription, or specialist runtime.
2. Show model architecture and operational metadata: total/active parameters, modalities, runtime, quantization, size, context/input limits, hardware fit, revision, checksum, and lifecycle state.
3. Track a verified champion and fallback per useful capability, with superseded and blocked history preserved.
4. Use track-specific evaluations and scores. Keep reasoning-on/off, image, audio, and video results separate from the locked text v1.0 series.
5. Show capability gaps and the next research candidate rather than ranking incompatible models against one another.


## MVP requirements

1. Show the latest run status: model, quantization, suite version, run time, complete/failed, and raw-report link.
2. Show candidate leaderboard with aggregate score, coding pass rate, structured-output validity, general-chat success, C1/C2/C4 generation throughput, TTFT, p95 latency, and error rate.
3. Show comparison against the Qwen 3.8 baseline.
4. Show storage/model readiness: downloaded, checksum verified, runner-ready, quarantined, or unavailable.
5. Show the next selected candidate and the evidence/reason it was selected.
6. Distinguish measured facts, human qualitative review, and inferred recommendation.
7. Give every model a concise card containing its capability tracks, architecture (including MoE details where applicable), modalities, local runtime/quantization, hardware fit, verified metrics, strengths, weaknesses, and lifecycle state.
8. Include a short written summary for each model and a three-to-four-sentence conclusion covering the measured result, practical use, relevant trade-offs, unresolved gates, and recommendation state. Conclusions must link to the underlying artifact and identify whether they are mechanical, qualitative, or promotion evidence.
9. Show concurrency results explicitly for every applicable model card: C1, C2, and C4/stress, including throughput, TTFT, p50/p95 latency, errors/timeouts, and scaling or queueing observations. A card must say `not tested` when a level is unavailable; it must not imply single-request results generalize to concurrency.
10. Show blockers prominently: dirty/unmounted storage, missing model, failed run, server capacity, or stale results.
11. Provide links to the full raw JSON and dated Obsidian report.

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
  "model": {"repo": "", "revision": "", "file": "", "quantization": "", "parametersTotal": 0, "parametersActive": 0, "modalities": [], "capabilities": [], "runtime": "", "contextOrInputLimits": "", "hardwareFit": "", "lifecycleState": "candidate"},
  "suiteVersion": "1.0.0",
  "environment": {"llamaCppCommit": "", "serverProfile": "", "gpu": "", "ctx": 0, "parallel": 0},
  "metrics": {"c1": {}, "c2": {}, "c4": {}},
  "quality": {"chat": {}, "coding": {}, "structured": {}, "safety": {}},
  "modelCard": {"summary": "", "conclusion": "", "evidenceType": "mechanical|qualitative|promotion"},
  "artifacts": {"raw": "", "report": "", "checksum": ""},
  "baselineComparison": {},
  "selection": {"score": 0, "reason": "", "promotionState": "candidate|reviewed|approved|rejected"}
}
```

## Handoff request

Herm: please review this PRD and build the Kitchen Wall benchmark-insights surface when the runner schema and first verified benchmark report are available. Please alert AJ when setup is complete and the first benchmark has finished. Coordinate any schema or dashboard questions through Townhall.

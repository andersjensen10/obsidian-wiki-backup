---
tags: [benchmarking, suite-change, hermes]
status: proposed-not-active
suite_version: 1.1.0-proposal
---

# Benchmark Suite v1.1 Proposal

This is not active yet. It records Herm's integration-focused suggestions without changing the locked v1.0 comparison suite.

## Proposed additions

- `enable_thinking:false` chat case with visible-answer completeness and zero reasoning leakage/empty replies.
- Streamed TTFT and time-to-complete as first-class metrics.
- Structured JSON and tool-envelope validity under C1 and C2.
- Approximately 8k-token context request plus a near-16k boundary observation.
- Short code/debug task with actual test execution.
- p50/p95 TTFT, completion latency, queue/wait time, error/timeout rate, and C2 scaling efficiency.
- C4 retained as stress data and not used as a Hermes promotion gate.

## Activation gate

AJ review and explicit suite-version approval are required before these become comparable benchmark cases. Until then, keep v1.0 locked and report any extra observations separately as non-comparable diagnostics.

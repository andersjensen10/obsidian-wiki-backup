---
tags: [benchmarking, local-llm, spark, results, decision-record]
status: honest-summary
updated: 2026-09-19
---

# Local LLM benchmark results to date

## Bottom line

We have **four usable performance measurements** (all from the locked 10-case C1/C2/C4 harness), but only **three have an independent verification record**. They are not yet a reliable basis for choosing a daily-driver model.

The clearest finding is about **reasoning mode and serving configuration**, not model quality:

- Reasoning-on Qwen 3.8 is about **8.6–8.8 generated tokens/s** and becomes slow to first visible output under load.
- The non-reasoning test configurations generated **59–74 tokens/s**.
- That is a large speed difference, but it is **not a fair quality ranking**: different models, quantizations, and reasoning settings were used; no acceptance-grade code tests or human quality review were recorded.

## What was actually measured

Each full artifact has 10 prompts (chat, instruction following, JSON, long-context, code generation/debugging, planning, tool-call JSON, safety, and context retention) at:

- **C1:** one concurrent request — 10 requests total
- **C2:** two concurrent requests — 20 requests total
- **C4:** four concurrent requests — 40 requests total

The table reports the median of the ten case-level medians. It is a compact throughput/latency view, **not an overall quality score**.

| Model / configuration | Suite | Verification | C1: success / TTFT / tok/s | C2: success / TTFT / tok/s | C4: success / TTFT / tok/s |
|---|---|---|---|---|---|
| Qwen3-Coder 30B-A3B Q4_K_M | v1.0.0 | verified | 10/10 · 0.085s · 59.29 | 20/20 · 0.855s · 59.57 | 40/40 · 2.422s · 59.87 |
| Qwen3-Coder 30B-A3B, reasoning on | v1.0.0 | verified | 10/10 · 0.079s · 73.29 | 20/20 · 0.700s · 74.31 | 40/40 · 1.979s · 73.68 |
| Qwen 3.6 35B-A3B UD-Q4_K_M | v1.0.0 | verified | 10/10 · 0.151s · 60.84 | 20/20 · 1.260s · 61.77 | 40/40 · 3.769s · 62.04 |
| Qwen 3.8 27B baseline, reasoning on | v1.0.0 | raw only | 10/10 · 0.552s · 8.59 | 20/20 · 12.432s · 8.59 | 40/40 · 35.893s · 8.61 |
| Qwen 3.8 27B baseline, reasoning on | v1.1.0 reasoning-on | raw only | 10/10 · 0.527s · 8.69 | 20/20 · 11.983s · 8.74 | 33/40 · 35.159s · 8.78 |

**TTFT** = time to first token. **tok/s** = generation throughput. C4 success was **82.5%** for the v1.1 Qwen 3.8 reasoning-on run; all other rows were 100% on this harness.

## Latency context

Median end-to-end latency rises sharply at C4:

| Configuration | C1 median latency | C2 | C4 |
|---|---:|---:|---:|
| Qwen3-Coder Q4_K_M | 1.852s | 2.413s | 3.991s |
| Qwen3-Coder reasoning on | 1.610s | 1.957s | 3.246s |
| Qwen 3.6 35B UD-Q4_K_M | 2.630s | 3.486s | 6.062s |
| Qwen 3.8 baseline reasoning on (v1.0) | 23.948s | 35.862s | 59.162s |

This is consistent with hidden reasoning consuming the response budget and queueing under concurrency. It does **not** prove that turning reasoning off is the correct product choice; quality was not compared rigorously.

## Evidence quality and gaps

### Solid evidence

- The three verified runs each contain the complete 30-entry C1/C2/C4 matrix, non-empty visible responses, TTFT, and a SHA-256 artifact record.
- Qwen 3.8 v1.1 shows a real operational weakness: **7 failures out of 40 C4 requests** while reasoning was enabled.

### Missing evidence — why this is not yet a model-selection system

1. **No comparable quality score.** The current harness records that a response was non-empty and transport succeeded. It does not grade correctness, strict JSON validity, coding-test pass rate, safety quality, or whether the response followed the requested length/format.
2. **Configurations are confounded.** Model family, quantization, reasoning setting, suite version, and likely server settings differ between rows. “73 tok/s” versus “8.7 tok/s” must not be interpreted as a model win without a matched reasoning-off/on comparison.
3. **Only one true candidate comparison has completed.** Qwen 3.6 has one verified result. The newly acquired Qwen 3.6 35B MTP candidate has passed checksum and an isolated dry-load, but has **no full-suite result**.
4. **The isolation design does not fit current hardware operations.** With production Qwen 3.8 resident, the GB10 did not have enough free unified memory to load the candidate alongside it. The recovery attempt on 2026-09-19 failed isolated health with HTTP 503 and `failed to fit params to free device memory`. Production was preserved; no benchmark result was produced.
5. **Automation has produced blocks, not a dependable daily result cadence.** 2026-09-18 had a complete admission/dry-load record but no suite launch; 2026-09-19 lacked fresh date-scoped readiness; the manual recovery run hit the capacity gate.

## Recommendation

Pause the claim that this is a nightly model-ranking pipeline. It is currently a **useful harness plus a small set of throughput observations**, not a reliable selection process.

Before spending more candidates or scheduled runs, make one deliberate decision about the test environment:

- **Approved maintenance-window benchmark:** stop production deliberately, run exactly one candidate, restore and verify production; or
- **Separate benchmark capacity:** a second GPU/host or a configuration proven to fit alongside production.

Then run a single matched comparison: baseline and candidate, same suite version, quantization policy, server flags, context, concurrency, and reasoning mode. Add executable checks for the code tasks and strict parsing/format checks before calling either result a quality pass.

## Raw artifacts

- Verified Qwen3-Coder Q4_K_M: `/home/aj/llm-benchmark-local/runs/2026-09-15/raw.json` — SHA-256 `a7cd7ca682a7a35774396e5b515d5166812733ec5020f7c723de55bab025615d`
- Verified Qwen3-Coder reasoning-on: `/home/aj/llm-benchmark-local/runs/2026-09-15/qwen3-coder-reasoning-on.json` — SHA-256 `61ea4281e539738c374e04e5889a2457c18c27667537375858df09e9a3c43ff4`
- Verified Qwen 3.6 35B: `/home/aj/llm-benchmark-local/runs/2026-09-16/raw.json` — SHA-256 `12ecf9b5cf2090ce2f2c4650da45e7d47a004b62e4d3c129c0c82a7dd4399c96`
- Raw Qwen 3.8 reasoning-on: `/home/aj/llm-benchmark-local/runs/2026-09-15/qwen38-baseline-reasoning-on.json` and `qwen38-baseline-reasoning-on-v1.1.json`
- Admission record, no suite: `/home/aj/llm-benchmark-local/runs/2026-09-18/readiness.json`
- Capacity-blocked recovery record: `/home/aj/llm-benchmark-local/runs/2026-09-19-recovery/readiness.json`

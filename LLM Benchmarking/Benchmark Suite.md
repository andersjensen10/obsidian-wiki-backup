---
tags: [benchmarking, local-llm, locked-suite]
status: locked-v1
suite_version: 1.0.0
---

# Benchmark Suite

This is the locked nightly suite. Changes require a new suite version; never silently change prompts or scoring while comparing models.

## Run contract

One model, one quantization, one llama.cpp server profile, one nightly run. Warm the server before measurement, then run the exact cases below at concurrency levels 1, 2, and 4 where the server can accept them. The current production profile has two slots; concurrency 4 is a stress result, not a promotion gate.

Record: model repository and revision, GGUF filename, quantization, file size, llama.cpp commit, server command/flags, GPU/runtime information, context size, parallel slots, batch/ubatch sizes, flash attention, speculative decoding, temperature and sampling, prompt tokens, generated tokens, TTFT, prompt throughput, generation throughput, end-to-end latency, queue/wait time when available, p50/p95/p99, errors/timeouts, and host utilization.

## Locked workload

Use deterministic prompts and fixed generation limits. Do not ask the model to reveal hidden reasoning. Score only the visible answer and machine-readable behavior.

1. **General chat** — concise answer to a practical household/technical question; 512 max output.
2. **Instruction following** — produce a constrained Markdown checklist with exactly 7 items and no preamble; 512 max output.
3. **Structured output** — return a JSON object matching a supplied schema; validate parse and schema, 512 max output.
4. **Long-context synthesis** — summarize and reconcile supplied project notes with explicit contradictions; fixed input around 8k tokens, 768 max output.
5. **Code generation** — implement a small Python function from a precise specification, including edge cases; run an isolated test harness and record pass/fail, 768 max output.
6. **Code debugging** — diagnose and patch a deliberately flawed small program; run the supplied tests and record pass/fail, 768 max output.
7. **Agentic planning** — turn a multi-step maintenance request into ordered, dependency-aware actions with risks and rollback notes; 768 max output.
8. **Tool-call discipline** — emit a strict tool-call JSON envelope for a supplied harmless action, with no extra text; validate exact schema, 512 max output.
9. **Safety and scope** — refuse an unsafe/destructive request while offering a safe alternative and an approval boundary; 512 max output.
10. **Context retention** — answer a question using facts introduced earlier in the same fixed conversation; 512 max output.

The exact prompt text and fixtures live beside each suite release in the benchmark runner repository once created. Until then, this document defines the contract and prompts at the semantic level; do not call a result comparable until the literal fixtures are frozen.

## Concurrency matrix

- C1: one request.
- C2: two simultaneous independent requests.
- C4: four simultaneous independent requests, stress-only unless capacity is increased.
- Repeat each case once per concurrency level; do not average away failures.
- Include a short warm-up excluded from scores and a cold-start observation recorded separately.

## Quality gates

A candidate must beat or match Qwen 3.8 on general-chat success and structured-output validity, pass both coding tasks, and remain usable at C2 without runaway latency or errors. Promotion also requires AJ review of visible outputs; throughput alone is insufficient.

## Report metrics

Report per case and aggregate: success rate, schema/test pass rate, TTFT, prompt tok/s, generation tok/s, end-to-end latency, concurrency scaling efficiency, p50/p95/p99, and estimated tokens-per-request cost proxy. Include a short qualitative note for coding quality and uncensored/general-chat behavior, with links to raw artifacts.

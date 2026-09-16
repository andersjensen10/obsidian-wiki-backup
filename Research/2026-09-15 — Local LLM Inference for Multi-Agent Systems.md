# Research Scout — Local LLM Inference for Multi-Agent Systems

**Run date:** 2026-09-15  
**Scope:** Current serving patterns for multi-agent workloads, with emphasis on AJ’s Spark `llama.cpp` deployment and persistent Hermes Bots.

## Bottom line

Local inference is now a credible substrate for multi-agent systems when the workload is decomposed into bounded, mostly independent calls rather than treated as one giant autonomous loop.[1][3][4]

For AJ, the immediate constraint is not API compatibility: Spark’s live `llama-server` already exposes an OpenAI-compatible interface, two request slots, continuous-batching support in the server, and Hermes delegation can route child agents to a direct local endpoint.[1][5]

The practical trade is capacity management. Two slots give useful overlap, but each additional active context consumes KV-cache memory and competes with long prompts; therefore, a persistent Bot fleet should be measured as a queueing system with per-task latency, throughput, context length, and failure rate—not judged by model quality alone.[1][5][7]

## What the current serving landscape says

### 1. llama.cpp is no longer only a single-user desktop runtime

The official `llama-server` documentation lists quantized GPU/CPU inference, OpenAI-compatible chat-completions and embeddings routes, parallel decoding with multi-user support, continuous batching, structured JSON output, function calling, and speculative decoding.[1] Its current server options expose parallel slots with `--parallel` and continuous batching with `--cont-batching`; the documented defaults are auto-selected slots and continuous batching enabled.[1]

This maps well to agent systems because independent workers can occupy separate slots while sharing one loaded model. It does not mean that two workers receive two independent copies of the model: they share the server’s model/runtime resources and compete for KV cache, batching capacity, and decode bandwidth.[1][5]

### 2. Prefix reuse and batching are the main throughput levers

vLLM’s official documentation presents PagedAttention, continuous batching, chunked prefill, prefix caching, speculative decoding, tool calling, structured outputs, and multiple forms of parallelism as core serving capabilities.[3] SGLang similarly positions RadixAttention, prefix caching, and multi-GPU parallelism as its runtime strengths for low-latency, high-throughput serving.[4]

These features matter most when agents share a stable system prompt, tool definitions, repository instructions, or a long document prefix. NVIDIA’s serving documentation gives a concrete rule of thumb: when more than 90% of the initial prompt is identical across requests, KV-cache reuse can substantially improve speed, with typically about a 2× time-to-first-token improvement beginning on the second request.[10]

The inference is workload-dependent. A multi-agent system that gives every worker a different long context will see less prefix benefit than a system that standardizes the initial prompt and varies only the task tail.[10][unverified]

### 3. Speculative decoding is becoming a practical local option, but compatibility matters

llama.cpp supports draft-model speculation, EAGLE-3, DFlash, DSpark, MTP, and several n-gram-based methods.[2] The mechanism generates candidate tokens with a cheaper predictor and verifies them with the target model in a batch; it helps when the draft predictions are frequently accepted.[2]

The current documentation is unusually relevant to agent workloads because it includes no-extra-model n-gram modes and reports acceptance statistics, while also documenting target-specific draft models.[2] That makes a low-risk benchmark possible before committing Spark memory to a second neural model, although the no-extra-model methods are pattern-dependent and should not be assumed to improve arbitrary reasoning or tool-call output.[2][unverified]

### 4. Gateways become useful when the fleet outgrows one endpoint

LiteLLM’s documented request path adds authentication and budget checks, rate limiting, routing, fallbacks, retries, provider translation, and asynchronous usage/logging work around model endpoints.[8] Its load-balancing documentation describes routing multiple deployments of one model with strategies including simple shuffle, least-busy, latency-based, and cost-based routing.[9]

For AJ, this is relevant as a later control-plane layer rather than an immediate replacement for direct Hermes-to-Spark routing. A gateway could present stable model aliases, enforce per-agent limits, and fail over to another deployment, but it would also add another service whose authentication, persistence, and failure modes need to be operated.[8][9]

## What this means for AJ’s Spark and Hermes Bots

### Sourced local state

A live check at 2026-09-15 23:30 CEST returned HTTP 200 from Spark `192.168.0.139:8014/health` and reported the model `qwen3.8-27b-aggressive-q5` from `/v1/models`. The same response reported approximately 27.32 billion parameters, Q5_K medium quantization, a 50,176-token server context, and a 262,144-token model training context.

A live `/props` check reported `total_slots: 2`, `n_ctx: 50176`, speculative decoding type `none`, and a model alias matching the active Qwen model. The server therefore has two available parallel slots, but speculative decoding is not currently enabled.

Hermes’ official delegation documentation says `delegate_task` creates child agents with isolated contexts and terminal sessions, returns only final summaries to the parent, supports up to ten concurrent children by default, and can route children to a different model or direct custom endpoint.[5] Hermes’ Bot Mode documentation defines a Bot as a profile with isolated configuration, memory, skills, credentials, and chat history; routines are ordinary cron jobs attached to that Bot, and each Bot has a persistent canonical Bot Chat.[7]

Hermes’ cron documentation says scheduled jobs run in fresh sessions, so prompts must be self-contained, while scripts can perform mechanical collection before the agent interprets the result.[6] That design is favorable for persistent research Bots: the script or retrieval layer can constrain the input, and the Bot can spend its model budget on synthesis instead of repeatedly rediscovering operational context.[6][7]

### Analysis: the right architecture is a bounded worker pool

For AJ’s setup, the strongest near-term pattern is one stronger parent/orchestrator plus a small number of local workers. Keep planning, ambiguous requirements, security-sensitive judgment, and final synthesis on the parent; send extraction, classification, comparison, test generation, and other mechanically checkable work to Spark workers.[5][unverified]

Two Spark slots should be treated as a measured concurrency ceiling for latency-sensitive work, not as a reason to configure every Hermes delegation batch to ten children. Hermes can create more children than Spark can serve concurrently, but excess children will queue at the local endpoint, increasing completion time and potentially making a persistent Bot feel unreliable.[5][unverified]

Persistent Bots add a second concurrency layer. A Bot can have its own recurring routine, canonical chat, and room membership, while the shared Spark endpoint has finite slots; therefore, a morning routine, an interactive Bot question, and a multi-agent room can contend even when each individual feature works correctly.[7][unverified]

The most important prompt-level optimization is stable prefixes. Put durable role instructions, tool schemas, and shared reference material in the same order for workers, and append the worker-specific assignment last. This is an engineering hypothesis for AJ’s stack because the inspected Spark configuration does not expose prefix-cache metrics, so it must be validated rather than assumed.[10][unverified]

A gateway such as LiteLLM becomes justified when AJ has multiple model deployments, needs per-Bot budgets or rate limits, or wants retries/fallbacks independent of Hermes. It is not necessary merely to connect Hermes to the current unauthenticated single Spark endpoint.[8][9][unverified]

## Confidence, disagreements, and evidence gaps

**High confidence:** the serving mechanisms summarized above are documented by the relevant projects, and the Spark endpoint was checked directly during this run.[1][5][10]

**Medium confidence:** stable shared prefixes should improve repeated-agent latency on AJ’s stack, because prefix caching is documented by serving systems, but Spark’s current `/props` output does not expose a directly interpretable prefix-cache hit-rate metric.[1][10]

**Open uncertainty:** this investigation did not run a controlled benchmark on Spark, did not compare Qwen output quality with thinking enabled versus disabled, and did not test whether the active Qwen build’s tool-call behavior remains reliable under two simultaneous Hermes-style requests. Those are local measurements, not facts supplied by the external documentation.[unverified]

**Scope limitation:** the landscape review favors official documentation and project repositories. It does not claim that llama.cpp, vLLM, or SGLang is universally fastest; hardware, quantization, model architecture, prompt mix, context length, and batching policy determine the result.[3][4][unverified]

## Why this matters to AJ

AJ already has the core of a cost-efficient multi-agent topology: Claude can retain orchestration and judgment while Spark handles volume-heavy delegated work through an OpenAI-compatible local server.[5] The live two-slot configuration is enough to test parallel workers without first rebuilding the system, but the test must record queueing and quality rather than only whether requests eventually complete.

Persistent Hermes Bots make this operationally important. Bots, routines, canonical chats, and group rooms can remain active over time, so local inference must be treated as shared infrastructure with admission control, bounded concurrency, and explicit fallback behavior—not as an interactive model that is idle between occasional prompts.[6][7]

The likely highest-return optimization is to improve utilization of the existing model before adding another serving stack: cap worker concurrency at the measured Spark capacity, standardize shared prefixes, and separate short fast workers from long reasoning workers. That recommendation is analysis based on the documented mechanisms and AJ’s live configuration, not a published benchmark result.[1][5][10][unverified]

## One concrete experiment

Run a 2×2 Spark benchmark using the current Hermes-style OpenAI-compatible endpoint:

1. Use two fixed worker prompts with the same system/tool prefix and different short assignments.
2. Compare sequential execution (one request at a time) with two concurrent requests.
3. Run each condition with thinking disabled and enabled, if the client/model template supports that toggle.
4. Record wall-clock completion time, time to first token if available, output tokens, HTTP errors, empty-content failures, and whether both outputs obey a small JSON schema.
5. Repeat with a long shared prefix inserted before the differing assignment, then compare first-request versus subsequent-request latency.

The experiment should leave the service configuration unchanged and use a small request budget. A useful decision rule is: keep two-slot delegation if concurrent completion time improves without unacceptable quality or error regressions; otherwise cap Hermes local delegation at one active child and treat the second slot as burst capacity. A measurable prefix benefit would justify standardizing worker prompt layout before investigating LiteLLM or migrating runtimes.[1][5][10][unverified]

## Sources

[1] https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md?plain=1
[2] https://github.com/ggml-org/llama.cpp/blob/master/docs/speculative.md
[3] https://docs.vllm.ai/en/stable
[4] https://docs.sglang.ai
[5] https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation
[6] https://hermes-agent.nousresearch.com/docs/guides/automate-with-cron
[7] https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode
[8] https://docs.litellm.ai/docs/proxy/architecture
[9] https://docs.litellm.ai/docs/proxy/load_balancing
[10] https://docs.nvidia.com/nim/large-language-models/1.15.0/kv-cache-reuse.html

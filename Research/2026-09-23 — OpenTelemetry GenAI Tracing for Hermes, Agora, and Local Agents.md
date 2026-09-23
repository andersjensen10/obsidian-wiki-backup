# Research Scout — OpenTelemetry GenAI Tracing for Hermes, Agora, and Local Agents

**Run date:** 2026-09-23 08:00 CEST  
**Selection basis:** relevance to AJ’s active Hermes/Agora/local-inference work, evidence availability, practical usefulness, novelty, and non-repetition.

## Three candidate topics

1. **OpenTelemetry GenAI tracing for agent systems — selected.** This is a practical next layer for AJ’s Hermes, Agora, Spark, and voice work: the projects already have multiple boundaries where latency, token use, tool calls, cancellation, and failures are otherwise reconstructed from logs.
2. **MCP authorization and security hardening.** The current MCP specification has dedicated authorization security considerations and a security-best-practices guide, making this timely for any future Agora tool adapter; it is less urgent than observability because AJ’s current MCP work is still a proposed read-only spike.[4][5]
3. **Godot 4.5 as an agent-facing interaction shell.** Godot’s NavigationAgent nodes provide a concrete foundation for interactive agents and small-robot-like simulations, but this is a larger product direction and has less immediate leverage than instrumenting the systems AJ already runs.

## Decision

The selected topic is **whether OpenTelemetry’s emerging GenAI semantic conventions are a good observability boundary for Hermes, Agora, and local model/tool pipelines—and what a bounded first instrumentation experiment should record**.

## Executive finding

OpenTelemetry’s GenAI work now covers conventions for model calls, agent/framework spans, metrics, events, MCP, and provider-specific integrations.[1][6][7]

The conventions are still marked development for agent spans, so they are a useful interoperability target rather than a promise of a frozen schema.[6]

For AJ, the strongest use is not “trace every token immediately.” It is to establish a common causal trace across **session → agent invocation → model call → tool call → external service → user-visible result**. This would make failures such as empty model replies, queued TTS after cancellation, stale Agora variants, and Spark request failures distinguishable by stage rather than inferred from mixed application logs.[unverified]

The recommendation is a small, local-first instrumentation slice: trace one Hermes/delegated model turn and one Agora generation or media operation, record metadata and timing by default, and keep prompt/tool content opt-in because the official guidance warns that content can contain sensitive data.[2][3]

## Sourced facts

### 1. The conventions map to agent execution, not only raw LLM calls

The OpenTelemetry GenAI repository describes conventions for spans, metrics, and events covering GenAI clients, MCP, and provider-specific systems.[7] Its agent-span document defines conventions for agent creation, agent invocation, workflows, planning, and tool execution.[6]

The agent-span document explicitly describes an agent as combining a GenAI model with reasoning, logic, and access to external tools, and says the conventions may apply to locally performed framework operations.[6] That makes the model a plausible fit for Hermes delegation and Agora’s server-side orchestration, even though AJ’s exact application schema would still be an implementation decision.[unverified]

The current status matters: the agent/framework document is labeled **Development**.[6] AJ should therefore treat semantic-convention names as an adapter layer that may evolve, not hard-code every application behavior to one revision.[unverified]

### 2. A useful minimum trace can stay metadata-first

OpenTelemetry’s GenAI observability walkthrough identifies model name, input/output token counts, finish reasons, latency, and token usage as useful telemetry fields.[2] It also states that prompt content and tool arguments are not captured by default, while enabling content capture adds full prompt messages, system prompts, tool schemas, and related content to telemetry.[2]

The older registry page warns that input messages may contain sensitive or personally identifiable information and says instrumentations should provide filtering or truncation options.[3] For AJ’s systems, the safe default is therefore to record identifiers, durations, counts, status, and bounded error classes while excluding raw prompts, transcripts, credentials, and tool arguments unless a local debugging run explicitly enables redaction-aware capture.[unverified]

A metadata-first trace would answer several high-value questions without storing conversation content:

- Which session, generation, or job produced the operation?
- Which model/provider was called, with what input/output token counts?
- How long did queueing, model generation, tool execution, and playback take?
- Did the operation finish, timeout, cancel, or fail?
- Which child operation was still active when the user-visible failure occurred?

These field choices are a proposed AJ-specific minimum, not a claim that the official conventions mandate this exact schema.[unverified]

### 3. MCP can become a trace boundary

The OpenTelemetry GenAI repository lists MCP conventions alongside client and provider conventions.[7] This is relevant to the previous MCP Apps report: if Agora eventually exposes a narrow MCP adapter, tracing the MCP request as a child span would preserve causal visibility across the embedded UI, host bridge, adapter, and Agora operation.[unverified]

The trace should distinguish an MCP tool request from the downstream application action. For example:

```text
Agora session
  -> MCP host request
    -> adapter authorization/check
      -> Agora read-only inspector operation
        -> database/event read
```

For mutating tools, the trace should include an explicit confirmation/authorization decision as metadata, while secrets and raw authorization tokens must never be recorded.[unverified] The MCP security materials reinforce that authorization and security considerations are implementation responsibilities, not something solved merely by embedding a UI.[4][5]

### 4. Traces are more valuable when they cross asynchronous boundaries

AJ’s local stack has asynchronous boundaries that ordinary request logs can blur: streamed local-model responses, queued TTS chunks, cancellation, WebSocket delivery, reconnects, and background media jobs.[unverified] A trace context should therefore be carried through child jobs and events, with stable application identifiers such as `session_id`, `generation_id`, `variant_id`, `media_job_id`, and `tts_job_id` stored as carefully scoped attributes.[unverified]

This is analysis rather than an official requirement. The practical test is whether a single trace can explain “the user interrupted generation, the server cancelled TTS, one queued chunk still played, and the UI received a stale event” without joining unrelated log lines manually.[unverified]

### 5. Metrics complement traces

The OpenTelemetry walkthrough describes a client-operation-duration histogram and a token-usage histogram, with filtering by model and token type.[2] It notes that these metrics can reveal latency regressions, token-heavy prompts, and usage patterns across models and agents.[2]

For AJ, the first useful metrics should be operational rather than billing-oriented:[unverified]

| Metric | Suggested dimensions | Why it matters |
|---|---|---|
| End-to-end turn duration | model, route, success/cancel | Perceived responsiveness |
| Model queue wait | service, model | Spark single-slot contention |
| Model generation duration | model, finish reason | Inference behavior |
| Tool duration and error count | tool name, outcome | Tool bottlenecks and failures |
| TTS cancellation latency | voice/job type | Stale audio after interruption |
| WebSocket event age | event type, reconnect state | Stale or delayed Agora UI state |
| Input/output tokens | model, route | Prompt growth and budget pressure |

Avoid high-cardinality dimensions such as raw user text, full tool arguments, or unconstrained IDs in metrics; keep those in traces or structured local logs only when needed.[unverified]

## Proposed architecture for AJ

Use OpenTelemetry as an **instrumentation and export boundary**, not as the owner of application state:

```text
Hermes session / Agora room / voice turn
  -> application root span
    -> agent invocation span
      -> local or remote model span
        -> tool/MCP span
          -> service/job child span
            -> user-visible result event
```

The application should continue to own conversation ordering, generation identity, cancellation semantics, authorization, and durable state.[unverified] OTel should make those transitions observable and correlate them; it should not become the source of truth for them.[unverified]

A small adapter can normalize the local model services behind one internal event shape:

```text
start(operation, parent_trace, application_ids)
model/provider metadata
queue_started / queue_ended
stream_started / first_output / completed|cancelled|failed
usage and finish reason
child tool/job links
end(status)
```

This internal shape can map to OTel spans and metrics while remaining usable in ordinary logs and tests if telemetry is disabled.[unverified]

## Recommended next experiment

Build a disposable **local GenAI trace fixture** without changing production behavior:[unverified]

1. Run one synthetic Hermes-style delegated turn against the local model service.
2. Run one synthetic Agora-style generation with a tool child operation and a cancellation path.
3. Export traces to a local OTLP-compatible viewer or file-backed test exporter.
4. Record model/provider, queue time, first-output time, total duration, usage if available, finish reason, cancellation, and application correlation IDs.
5. Add one intentionally stale or late child event and verify that the trace still identifies the parent generation.
6. Run the same fixture with prompt and tool-content capture disabled, then with a redaction-aware debug mode.
7. Check that secrets, raw authorization tokens, and unbounded user text do not appear in exported telemetry.

**Decision rule:** keep the instrumentation boundary if a single trace explains the lifecycle and failure stage of both a model turn and an asynchronous job without materially increasing sensitive-data exposure or application coupling. Defer broad rollout if the exporter or schema makes cancellation, streaming, or child-job correlation less clear than the existing logs.[unverified]

## Why this matters to AJ

AJ’s current work spans Hermes cron jobs and delegation, Spark local inference, Agora WebSocket/generation state, and Fish Speech output scheduling. Those systems already expose the failure modes where observability has the highest leverage: budget exhaustion, dropped requests, stale events, cancelled audio, reconnects, and background jobs.[unverified]

A common trace vocabulary would also make later experiments comparable. A voice turn, an Agora generation, and a Hermes delegated call need not share implementation code, but they can share concepts such as parent operation, model call, child tool/job, cancellation, latency, and final outcome.[unverified]

## Uncertainty and open questions

- The agent/framework conventions are explicitly in Development status and may change.[6]
- The official walkthrough demonstrates telemetry fields and a visualization path, but it does not benchmark overhead or retention quality on AJ’s laptop/Spark topology.[2]
- The retrieved material does not establish a ready-made Python/Node instrumentation package for AJ’s exact Hermes and Agora boundaries; an adapter may be required.[unverified]
- Prompt/tool-content capture can improve debugging but increases privacy and storage risk; the correct redaction policy needs a local test.[2][3]
- MCP tracing conventions and host support should be checked again before implementing a live Agora MCP adapter.[7]

## What to queue next

The best follow-up is the local GenAI trace fixture above. If AJ wants a different direction, the deferred candidates are MCP authorization hardening for the future Agora adapter and a Godot 4.5 agent-facing interaction prototype.

## Sources

[1] https://opentelemetry.io/docs/specs/semconv/gen-ai — OpenTelemetry Generative AI semantic conventions
[2] https://opentelemetry.io/blog/2026/genai-observability — Inside the LLM Call: GenAI Observability with OpenTelemetry
[3] https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai — OpenTelemetry GenAI attribute registry
[4] https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations — MCP authorization security considerations
[5] https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices — MCP security best practices
[6] https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md — OpenTelemetry GenAI agent and framework spans
[7] https://github.com/open-telemetry/semantic-conventions-genai — OpenTelemetry GenAI semantic conventions repository

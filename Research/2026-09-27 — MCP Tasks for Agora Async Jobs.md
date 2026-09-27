---
tags: [type/research]
---

# Research Scout — MCP Tasks for Agora Async Jobs

**Run date:** 2026-09-27 08:00 CEST  
**Selection basis:** relevance to AJ’s active Agora/Hermes and voice-pipeline work, primary-source availability, practical usefulness, novelty, and non-repetition.

## Three candidate topics

1. **MCP Tasks as a durable async-job contract for Agora and voice/media work — selected.** The draft Tasks extension models long-running tool calls with server-generated task IDs, polling, cancellation, TTLs, status transitions, optional input requests, and final results; it explicitly targets expensive computations, batch processing, and external job APIs.[1] This is adjacent to, but not a repeat of, the 2026-09-25 MCP authorization report: that report covered who may call an adapter, while this one covers how an authorized call survives asynchronous execution.
2. **llama.cpp function-calling reliability on Spark.** Current llama.cpp documents native and generic tool-call handlers, `--jinja` support in `llama-server`, and optional parallel tool calls; generic handling may consume more tokens and be less efficient than native formats.[3] This would be practical for Hermes delegation, but it overlaps the 2026-09-15 local-inference report and the 2026-09-24 speculative-decoding report.
3. **A bounded systemd/service-resilience design for Spark-dependent Hermes pipelines.** This would examine health checks, restart policy, queue backpressure, and failure observability across the local model, voice-prep API, and dashboard. It is highly practical but would need live-service measurements to avoid becoming a generic operations checklist.[unverified]

## Decision

The selected topic is **whether MCP Tasks is a useful boundary for Agora’s long-running work—especially TTS, voice preparation, regeneration, and other jobs that should outlive a single request—and what a minimal compatibility spike should prove**.

## Executive finding

MCP Tasks is a promising *protocol-facing job handle*, not a replacement for Agora’s internal job system. The draft defines a server-directed asynchronous result for eligible requests, with `tasks/get`, `tasks/update`, and `tasks/cancel`; a client that advertises support must be prepared to receive either a normal result or a task result.[1] The protocol also requires the task to be durably retrievable before the server returns its task handle, which is directly relevant to crash/reconnect behavior.[1]

For AJ, the strongest use is a narrow adapter around already-authorized Agora jobs: Agora remains authoritative for conversation identity, permissions, generation/variant ownership, durable records, and job execution; MCP Tasks exposes a task handle and status projection to a compatible client.[unverified] This preserves the ownership boundary established in the prior authorization work instead of moving orchestration into the protocol adapter.

The recommended next experiment is a **local fake MCP Tasks server plus an Agora job adapter**, with deterministic fixtures for TTS, regeneration, cancellation, expiry, reconnect, and `input_required`. Do not connect it to real credentials, production jobs, or the live model/voice services in the first pass.[unverified]

## Sourced facts

### 1. What the Tasks extension actually adds

The draft extension is identified as `io.modelcontextprotocol/tasks`. It lets a server answer a `tools/call` request with an asynchronous task handle rather than a final result, and defines `tasks/get`, `tasks/update`, and `tasks/cancel` plus a `resultType: "task"` discriminator.[1]

Task creation is server-directed: the client advertises support in per-request capabilities, but the server decides per request whether to materialize a task. A client that negotiated the extension must handle both the ordinary result shape and the task shape.[1]

The task object includes a stable server-generated ID, status, timestamps, optional status text, a TTL, and a suggested polling interval. Statuses include `working`, `input_required`, `completed`, `cancelled`, and `failed`.[1]

The extension is explicitly aimed at expensive computations, batch processing, and external job APIs.[1] That makes it a closer conceptual fit for voice preparation, long TTS renders, media processing, or other jobs than for ordinary short chat turns.

### 2. Durability, polling, input, and cancellation

When a server returns a task result, it must have durably created the task so that a subsequent `tasks/get` for the returned ID can resolve; the specification calls this out to prevent clients from needing speculative polling after task creation.[1]

Clients should respect the server-provided polling interval, continue until a terminal status or cancellation, and persist task IDs so polling can resume after a crash or restart.[1]

A task can enter `input_required`; the client receives outstanding server-to-client requests through `inputRequests` and answers them through `tasks/update`. The specification says clients must apply the same trust and user-facing handling to these requests as to equivalent direct requests, and should deduplicate request keys across polls.[1]

Cancellation is cooperative and eventually consistent. A successful `tasks/cancel` acknowledgement signals intent, but the server is not obligated to stop the work, and the task may ultimately reach a terminal status other than `cancelled` if completion wins the race.[1]

Servers may additionally push complete task-status objects through `notifications/tasks`, while clients may continue polling or use notifications instead.[1]

### 3. The surrounding 2026-07-28 MCP direction

The official MCP announcement describes the 2026-07-28 specification as a stateless protocol core with Multi Round-Trip Requests, header-based routing, authorization hardening, a formal extensions framework, and updated SDKs.[2] It identifies Tasks as one of the formal extensions and explains that the new stateless direction is intended to improve reliability and scalability.[2]

The announcement also distinguishes protocol statelessness from application state: an application may still carry state across calls using an explicit handle passed through tools.[2] That distinction supports treating an MCP task ID as a transport-facing handle while keeping the underlying Agora job and conversation state in Agora.[unverified]

### 4. Contrast with the local-LLM candidate

llama.cpp’s current function-calling documentation says `llama-server` supports function calling when started with `--jinja`, lists native handlers for several model families including Qwen 2.5 and Hermes variants, and documents generic handling when a template is not recognized.[3] It also notes that generic support may consume more tokens and be less efficient than a native format, and that parallel tool calling is available on some models but disabled by default.[3]

That is useful context for an eventual MCP adapter, but it does not solve the durable job lifecycle problem: a model can request a tool, while Agora still needs an explicit contract for a job that continues after the initial request, survives reconnects, reports cancellation races, and returns a final result.[unverified]

## Analysis for AJ

### Where MCP Tasks fits

A clean division would be:

```text
MCP client
  -> authorized MCP adapter
      -> task handle + status projection
          -> Agora job record
              -> TTS / voiceprep / regeneration / media worker
```

The adapter should map MCP task IDs to Agora job IDs through a durable relation, not use the task ID as the sole internal identity.[unverified] Agora should retain authorization checks, ownership checks, generation/variant identity, retry policy, artifact storage, and the authoritative event history.[unverified]

A task result should contain a compact reference to the Agora artifact or result record, not silently duplicate large audio or media payloads into every protocol response.[unverified] The first spike should test metadata and small fixture payloads only.

### Why this is better than extending the existing chat event stream directly

Agora’s WebSocket event stream is appropriate for live conversation updates and UI rendering, but an external tool protocol needs a stable request/result vocabulary for clients that may disconnect, restart, poll later, or lack access to Agora’s internal event model.[unverified] MCP Tasks gives that external client a bounded handle/status/result surface while leaving Agora’s richer event stream intact.

This is not a reason to replace Agora’s current job events. The likely design is dual projection: Agora emits its internal authoritative events; the adapter projects a compatible subset into task status and final-result operations.[unverified]

### Important limits

Tasks are currently specified for `tools/call`; the document says future revisions may support other request types, so the adapter should not assume every MCP operation can become a task.[1]

The task extension does not define a universal worker queue, retry semantic, progress percentage, artifact store, or exactly-once execution model.[unverified] Those remain Agora or worker concerns.

Cancellation is intent, not proof of termination.[1] Agora therefore needs an explicit cancelled-request policy and a visible distinction between “cancel requested,” “worker stopped,” and “completed before cancellation took effect.”[unverified]

A task TTL is not the same as artifact retention.[unverified] The adapter should specify what happens when the task handle expires while the underlying audio or media artifact remains available, and whether a new task can safely retrieve the same result.

## Recommended compatibility spike

Build a disposable local fixture with four components:

1. **Fake MCP Tasks server.** Implement `tools/call`, `tasks/get`, `tasks/update`, and `tasks/cancel` for one fake `render_voice` tool. Support normal synchronous completion and task completion so the client exercises the polymorphic result path.[1][unverified]
2. **Agora-shaped job store.** Persist `job_id`, `task_id`, conversation/generation/variant identifiers, status, timestamps, cancellation state, and result reference. Make restart/reload part of the test rather than an afterthought.[unverified]
3. **Deterministic worker fixtures.** Include success, failure, slow completion, cancellation race, TTL expiry, reconnect during polling, and `input_required` cases. Use tiny text/artifact placeholders, not real TTS or model calls.[unverified]
4. **Contract assertions.** Verify that task creation is readable immediately, task IDs survive process restart, polling honors changing intervals, duplicate input requests are not shown twice, and cancellation is reported honestly when work finishes first.[1][unverified]

**Decision gate:** proceed only if the adapter can restart without losing task-to-job correlation, can distinguish terminal result from cancellation intent, and never exposes an unauthorized Agora job through a guessed or replayed task ID.[unverified]

## Why this matters to AJ

This would give Agora a standardizable boundary for the exact class of work already appearing in AJ’s ecosystem: TTS jobs, voice cloning/preparation, media transforms, and potentially long-running regeneration or evaluation jobs.[unverified] It could also make a future Hermes tool client less dependent on Agora’s internal WebSocket schema while preserving that schema for the native UI.[unverified]

The practical value is not “adopt MCP everywhere.” It is testing whether one small, durable task projection can reduce integration glue without weakening authorization or job ownership.[unverified]

## Uncertainty and open questions

- The Tasks page is a **draft** extension dated 2026-07-28, not evidence that every MCP SDK or client already implements it.[1]
- The official announcement says updated Tier 1 SDKs accompany the 2026-07-28 specification, but this report did not verify Tasks support in the specific SDK versions AJ would use.[2]
- The report does not establish interoperability with Agora’s current server or WebSocket implementation; that requires a local adapter spike.[unverified]
- The right result-reference and artifact-retention policy is unresolved, especially for audio files whose task TTL expires.[unverified]
- Whether AJ benefits from MCP Tasks more than a small Agora-native HTTP job API remains an empirical question; compare implementation complexity, reconnect semantics, and client availability in the spike.[unverified]

## What to queue next

The highest-value follow-up is the **local fake MCP Tasks/A​gora job adapter** described above. Deferred alternatives remain a Spark function-calling compatibility benchmark and a live systemd resilience audit for the local inference/voice stack.

## Sources

[1] https://tasks.extensions.modelcontextprotocol.io/specification/draft/tasks — MCP Tasks Extension Specification
[2] https://blog.modelcontextprotocol.io/posts/2026-07-28 — MCP 2026-07-28 Specification Release
[3] https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md — llama.cpp Function Calling

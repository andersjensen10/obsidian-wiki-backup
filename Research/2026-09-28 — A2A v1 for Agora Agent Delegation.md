---
tags: [type/research, topic/agents, topic/agora]
---

# Research Scout — A2A v1 for Agora Agent Delegation

**Run date:** 2026-09-28 08:00 CEST  
**Selection basis:** relevance to AJ’s active Agora/Hermes work, primary-source availability, practical usefulness, novelty, and non-repetition with the 2026-09-27 MCP Tasks report and earlier research.

## Three candidate topics

1. **A2A v1 as a federation/delegation boundary for Agora personas and future specialist agents — selected.** A2A v1 is now a stable protocol release, and its model covers agent discovery, task-oriented interaction, artifacts, streaming, polling, and push notifications.[1][2] This is adjacent to the previous MCP Tasks report but not a repeat: MCP Tasks focused on exposing durable asynchronous work through MCP, while this topic asks whether Agora should expose or consume *peer agents* through a higher-level agent-to-agent contract.
2. **llama.cpp server scheduling and slot/prefix-cache behavior for Spark.** This could directly target Spark throughput and queueing, but it would overlap the 2026-09-15 local-inference and 2026-09-24 speculative-decoding reports, and a useful conclusion would require current live measurements rather than documentation alone.[unverified]
3. **Failure containment for Spark-dependent Hermes voice and inference services.** A bounded audit could measure health checks, queue backpressure, restart behavior, and observability across llama.cpp, Fish Speech, and voiceprep-api. It is highly practical, but it is an operational measurement task rather than a clean primary-source research slice.[unverified]

## Decision

The selected topic is **whether A2A v1 is a useful external boundary for Agora’s future multi-agent delegation, and what a minimal local compatibility spike should prove**.

## Executive finding

A2A v1 is a better conceptual fit than MCP Tasks for communication *between autonomous agents*: the official comparison positions MCP as the vertical tool/resource layer inside an agent and A2A as the horizontal collaboration layer between agents.[3] A2A’s core object is a stateful task with messages and artifacts, and clients can receive updates through polling, streaming, or push notifications.[2]

For Agora, the useful interpretation is not “replace the existing WebSocket chat engine with A2A.” It is a narrow federation adapter: keep Agora authoritative for persona identity, room history, permissions, variants, and local job execution; expose selected specialist capabilities as A2A agents only where a peer needs a task-oriented, possibly long-running interaction.[unverified]

The recommendation is to build a **local fake A2A agent plus an Agora-shaped delegation adapter**, initially with one read-only specialist task. The spike should test discovery, task correlation, reconnect/resubscribe, artifact references, cancellation, authorization boundaries, and version negotiation before any real model or voice service is connected.[unverified]

## Sourced facts

### 1. What A2A v1 standardizes

The A2A specification defines an Agent Card for capability advertisement and a task model for stateful work. The task model includes a unique task ID, messages, artifacts, status, and history-related fields.[2]

The v1 specification exposes operations for sending messages, getting and listing tasks, canceling tasks, subscribing to task updates, and configuring task push notifications.[2] A2A therefore covers more than a one-shot request/response, but it does not prescribe the worker implementation behind an agent.[unverified]

A2A supports three update delivery modes: polling with `GetTask`, streaming with message/task subscription operations, and push notifications delivered through a client-registered webhook.[2] The specification describes streaming as real-time delivery, polling as the simplest broadly compatible option, and push notifications as suitable for long-running or disconnected scenarios.[2]

The specification requires ordered delivery of generated events within a stream, and it allows multiple concurrent streams for one task; each active stream receives the same events in the same order, while the task lifecycle remains independent of any one stream.[2] That is relevant to Agora reconnects and multiple observers, but it does not by itself define Agora’s internal event ordering or database transaction rules.[unverified]

A2A v1 also includes task states beyond simple success/failure, including terminal states such as completed, failed, canceled, and rejected, plus interrupted states such as input-required and auth-required.[2] The exact mapping from those protocol states to Agora’s current message, generation, and media states would be an application decision.[unverified]

### 2. A2A and MCP are complementary, not interchangeable

The official A2A documentation explicitly distinguishes MCP’s tool/resource integration from A2A’s peer-agent collaboration.[3] It describes MCP as helping an agent use structured tools and resources, while A2A lets independent agents discover, negotiate, manage shared tasks, and exchange conversational context and complex data.[3]

That distinction matters because the 2026-09-27 report already evaluated MCP Tasks as a protocol-facing handle for long-running work. A2A can sit one layer above that design: an Agora agent could delegate to a peer A2A agent, while that peer internally uses MCP tools or an MCP task adapter.[unverified]

A2A’s own documentation says the two protocols can be used together: A2A connects agents to agents, while MCP connects each agent to its tools and resources.[3] This is a protocol-design recommendation from the A2A project, not evidence that Agora needs both protocols immediately.[unverified]

### 3. Maturity and compatibility signals

The A2A project lists v1.0.0 as a stable release dated 2026-03-12 and v1.0.1 as a subsequent release dated 2026-05-26.[1] The v1.0 release notes include breaking protocol changes, task-list support with filtering and pagination, OAuth flow modernization, multi-tenancy-related changes, and cleanup of deprecated fields.[1]

The official v1 announcement describes the release as the first stable, production-ready version and highlights multiple protocol bindings, version negotiation, multi-tenancy, signed Agent Cards, and a stronger security posture.[4] Those are project claims about the release’s goals and capabilities; they are not a substitute for testing the specific SDKs or deployment topology Agora would use.[unverified]

The project maintains official SDK and sample repositories alongside the protocol specification.[5][6] This is evidence of an implementation ecosystem, but it does not establish that all relevant language SDKs or clients have equivalent maturity.[unverified]

## Analysis for AJ

### Where A2A could fit in Agora

A plausible boundary is:

```text
Agora room/persona engine
  -> delegation policy + authorization check
      -> A2A client adapter
          -> specialist A2A agent
              -> local tools / MCP / worker queue
```

Agora should remain the source of truth for the user-facing room, persona identity, conversation sequence, variant ownership, and any generated media attached to the room.[unverified] The A2A task ID should be correlated with an Agora delegation record rather than used as Agora’s primary key.[unverified]

A first useful specialist could be deliberately small: a “research scout” or “voice-preparation planner” agent that returns structured text and artifact references without touching production services.[unverified] Avoid beginning with a persona that can mutate rooms, invoke arbitrary tools, or publish audio; those paths combine protocol, authorization, and product semantics before the transport is understood.[unverified]

### What A2A adds beyond Agora’s current WebSocket path

Agora’s WebSocket event stream is optimized for its own live UI and current room lifecycle. A2A offers a standardized peer-facing surface where an external client can discover capabilities, submit a task-oriented message, reconnect, poll, subscribe, or receive a webhook.[2][3]

The trade-off is a second contract to maintain. A2A does not eliminate the need for Agora’s internal events, persistence, cancellation rules, artifact store, or user-consent UI.[unverified] It would be justified only for integrations where interoperability or process isolation is valuable enough to pay that cost.[unverified]

### Security and identity implications

Signed Agent Cards and multi-tenancy are highlighted in the v1 announcement as production-oriented capabilities.[4] For Agora, that suggests a future trust model in which an external agent’s identity and advertised endpoint are verified before delegation, but the report found no evidence that a local adapter can safely inherit those guarantees without implementing key management, audience binding, authorization, and replay controls.[unverified]

Do not expose a general-purpose A2A endpoint from Agora as the first experiment. Use a loopback-only fake peer, a fixed allowlist of agent IDs, bounded task types, explicit user-visible consent, and a correlation table that rejects unknown or replayed task handles.[unverified]

## Recommended compatibility spike

Build a disposable local fixture with four pieces:

1. **Fake A2A specialist.** Implement Agent Card discovery plus one task-oriented operation. Return deterministic success, failure, delayed completion, and input-required fixtures. Use no real model, credentials, TTS, or media service.[unverified]
2. **Agora-shaped delegation record.** Persist `delegation_id`, remote `agent_id`, remote `task_id`, room/persona/message identifiers, requested capability, status, timestamps, cancellation intent, and result/artifact reference.[unverified]
3. **Three update paths.** Exercise polling, streaming/resubscribe, and push notification delivery. Verify that a reconnect can recover the same task without duplicating messages or artifacts.[2][unverified]
4. **Negative authorization tests.** Reject an unknown Agent Card, unsupported capability, mismatched room/persona owner, expired delegation, replayed task ID, and a result delivered after local cancellation.[unverified]

### Decision gate

Proceed toward a real adapter only if the fixture proves all of the following:

- A delegation is durably correlated before its handle is shown to the caller.[unverified]
- A reconnect or process restart can recover task state through polling or resubscription.[2][unverified]
- Stream updates remain ordered and duplicate delivery does not create duplicate Agora messages or artifacts.[2][unverified]
- Cancellation distinguishes “requested” from “worker stopped” and “completed before cancellation.”[unverified]
- A2A peer identity and capability checks happen before a remote task can affect an Agora room.[unverified]
- The implementation can be removed without changing Agora’s native chat path.[unverified]

## Why this matters to AJ

A2A v1 gives Agora a possible future boundary for specialist agents, separate installations, or home-lab services that should collaborate without importing Agora’s internal room protocol.[unverified] It is most interesting if AJ eventually has several distinct agents—research, voice preparation, media generation, robotics, or game tooling—that need task-level collaboration rather than mere tool calls.[unverified]

The immediate value is architectural clarity, not adoption. The local spike can answer whether the protocol’s task and update semantics reduce integration glue compared with a small Agora-native delegation API, while keeping the experiment isolated from the live app.[unverified]

## Uncertainty and open questions

- The report did not verify A2A interoperability among the exact client and server SDK versions AJ would choose.
- The report did not measure the overhead of maintaining both Agora-native events and an A2A projection.
- A2A’s protocol task model does not settle artifact retention, exactly-once execution, worker retry policy, or Agora’s variant semantics.[unverified]
- Signed Agent Cards and multi-tenancy are promising v1 capabilities, but the local trust and key-rotation design remains to be chosen.[4][unverified]
- It remains an empirical question whether A2A is more useful for Agora than a narrowly scoped internal HTTP delegation API.

## What to queue next

Queue the **local fake A2A specialist/Agora delegation adapter** as the next implementation-oriented experiment. Keep the previous MCP Tasks spike as a separate comparison point: MCP Tasks is the candidate boundary for asynchronous tool/job exposure, while A2A is the candidate boundary for peer-agent delegation.

## Sources

[1] https://github.com/a2aproject/A2A/releases
[2] https://a2a-protocol.org/dev/specification
[3] https://a2a-protocol.org/dev/topics/a2a-and-mcp
[4] https://github.com/a2aproject/A2A/blob/main/docs/announcing-1.0.md
[5] https://github.com/a2aproject/a2a-samples
[6] https://github.com/a2aproject/a2a-js/releases

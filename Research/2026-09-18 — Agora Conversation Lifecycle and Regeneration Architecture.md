# Research Scout — Agora Conversation Lifecycle and Regeneration Architecture

**Run date:** 2026-09-18  
**Selection basis:** relevance to AJ’s active work, evidence availability, practical usefulness, novelty, and non-repetition.

## Three candidate topics

1. **Agora conversation lifecycle: WebSocket events, non-destructive regeneration, and variant history — selected.** This is directly relevant to the active Agora project, which recently added World Sessions, cross-scene validation, and the corrected regeneration path. The local checkout provides implementation and live-test evidence, while WebSocket and Hermes Bot/cron documentation provide useful external design comparisons.[1][2][3]
2. **Spark/GB10 local serving for multimodal and voice workloads.** This would be useful for the Fish Speech and ComfyUI services, but it overlaps with the previous two reports’ local-inference and TTS focus and would require a controlled hardware benchmark to be more than a survey.
3. **Godot agent interaction patterns for a future robotics/game interface.** This is novel and potentially valuable, but it is less immediately actionable than validating Agora’s current event and state model.

## Decision

The selected topic is **Agora’s conversation lifecycle and regeneration architecture**. The useful question is not whether WebSockets are generally appropriate; the project already uses them. The question is whether the current event stream and persisted message model make long-running, branching conversations understandable, recoverable, and testable.

## Executive finding

Agora’s current direction is sound: preserve a message’s stable identity and ordering slot, append regenerated text as variants, and stream lifecycle events over the existing room WebSocket rather than deleting downstream history. This is supported by the local implementation and by the project’s live regeneration checks; it is an engineering finding from AJ’s checkout, not an externally published benchmark.

The next architectural improvement should be to make the event contract explicit as a small state machine: `ready → turn_started/regenerating → token* → message_done`, with terminal `error` or `cancelled` paths and a client-side rule that only the active generation may mutate the visible bubble. This follows from the local event usage and from the WebSocket model, where the browser receives messages through an open bidirectional connection.[3]

Hermes provides a useful adjacent comparison: Bots have a persistent canonical chat, while `/new` is redirected to `/compact` in that canonical conversation so the relationship is not silently forked.[1] That suggests Agora should distinguish clearly between a canonical transcript, a selected message variant, and an explicitly forked scenario/world session rather than treating all alternate generations as equivalent.

## Sourced facts and local project evidence

### External design constraints

The WebSocket API provides a two-way interactive communication session between browser and server, with the client receiving server messages through the connection.[3] That makes it suitable for Agora’s token streaming and lifecycle notifications, but it does not by itself provide persistence, replay, ordering guarantees across reconnects, or conflict resolution; those responsibilities remain application-level design work.[3]

Hermes Bot Mode treats a Bot as a profile with isolated configuration, memory, skills, credentials, and chat history.[1] Each Bot has a canonical persistent chat, and the documentation explicitly distinguishes that canonical relationship from scratch sessions.[1]

Hermes cron jobs run in fresh agent sessions, so scheduled prompts must be self-contained.[2] The same guide recommends putting mechanical collection in a script and leaving interpretation to the agent, a pattern that maps well to Agora’s scenario runners and live checks.[2]

### Local Agora evidence

The current checkout is `/home/aj/Desktop/Hermes/AgenticChatroomProject`, with origin `git@github.com:andersjensen10/agora-chatroom.git`. At the time of this run, the working tree was clean at commit `1ddf090` (`Nightly auto-backup: 2026-09-17 23:00`). These are local repository observations, not claims about the public repository’s indexed state.

The message schema stores a stable `seq`, optional `variants`, and a `variantIndex`. The server-side regeneration helper appends freshly generated text to the variants array, makes it visible, and preserves the original message identity and ordering slot. The comments explicitly describe regeneration as append-only so an earlier phrasing remains recoverable.

The live regeneration check exercises the real WebSocket path with a mock llama.cpp server. It asserts that regeneration emits a `regenerating` event, streams tokens into the same message ID, keeps at least two variants including the original, leaves the message count unchanged, preserves downstream turns, keeps the original `seq`, and allows paging back to variant index 0. The script reports these as checks to run; this morning’s scout did not rerun the application server or claim a new pass result.

The broader live bugfix script covers the same regeneration invariants through both HTTP preparation and WebSocket streaming, and also checks strict-mention silence and ComfyUI cancellation. Its existence is valuable evidence of intended behavior, but the script source is not itself a fresh execution result.

## Architecture reading

### 1. Stable message identity is the right primitive

A destructive rewind makes the transcript look linear but discards evidence of what happened after the target turn. Agora’s current variant approach keeps the target message’s ID and sequence number while preserving later turns. That is the safer default for a conversational UI because the user can inspect or recover earlier generations instead of losing them.

The remaining design question is semantic: a regenerated reply may make downstream turns logically stale even when they remain physically present. The UI should therefore show that downstream turns were generated under an earlier variant, or offer an explicit “continue from this variant” action. Silent retention is better than deletion, but retention alone does not communicate causal staleness.

### 2. WebSocket events need generation identity

The current checks key regeneration tokens and completion to the message ID. That is enough for one active generation per message, but a reconnect or double-click can create ambiguity if two generations for the same message overlap. The protocol should add a server-issued `generationId` to `regenerating`, `token`, `message_done`, `error`, and `cancelled` events.

The client should accept tokens only when both `messageId` and `generationId` match the active operation. A late event from an abandoned generation must be ignored, not appended to the visible bubble. This is analysis derived from the local event shape and normal WebSocket behavior; no external source documents Agora’s internal contract.

### 3. Canonical, variant, and fork are different concepts

Hermes’ canonical Bot Chat versus scratch-session distinction is a useful model.[1] For Agora, the analogous concepts are:

- **Canonical conversation:** the durable room transcript and its stable message IDs.
- **Variant:** another generation of one assistant turn, selectable without changing the transcript topology.
- **Fork:** a deliberate new continuation whose later turns are based on a selected variant or world state.

The current `variants` field solves the second concept. The World Session work appears to be the right place to represent the third; it should not be implemented by quietly overwriting the canonical room or deleting the old downstream turns.

### 4. Tests should remain scenario-level, not only unit-level

The existing live-regeneration script is a strong pattern because it verifies the observable contract over the same WebSocket path used by the client, while replacing the external model with a deterministic mock. This resembles Hermes’ recommendation to separate mechanical collection from agent interpretation in scheduled workflows.[2]

The next step is to turn the event contract into a reusable scenario fixture that can test reconnect, duplicate submission, cancellation, and late-token cases without requiring Spark or ComfyUI. Unit tests can validate storage transitions; the scenario fixture should validate the sequence observed by a real client.

## Recommended next experiment

Add a deterministic `generationId` and a reconnect-focused scenario test:

1. Start a room with the existing mock model and create a multi-turn transcript.
2. Begin regeneration of a reply and record the `generationId` from `regenerating`.
3. Drop the client socket after several tokens, reconnect, and request room state.
4. Assert that the persisted message is either the last committed generation or an explicitly marked in-progress/error state; never treat a partial token stream as a committed final reply.
5. Send a second regeneration request and assert that the old generation’s late tokens cannot alter the new visible bubble.
6. Verify that variant selection changes the displayed text without changing message ID, `seq`, or downstream records.
7. Add an explicit UI label or affordance for “downstream turns were generated from another variant” before exposing forked continuation.

**Decision rule:** keep the current append-only variant model if the reconnect and overlap tests pass; add explicit generation IDs before supporting concurrent regeneration or multi-tab editing. Do not reintroduce destructive rewind as the default.

## What matters specifically for AJ

This architecture aligns with Agora’s current project trajectory: media and World Session features are adding more durable state, while the chatroom remains an interactive stream. Preserving prior generations protects debugging and storytelling continuity, especially when local reasoning models, TTS, ComfyUI jobs, and browser clients can fail independently.

The immediate payoff is not a new feature visible in a screenshot. It is a narrower failure surface: a user can reconnect, inspect the selected variant, and understand whether later turns belong to the current branch. That will matter more as World Sessions span scenes and as generated media gains provenance and derivative relationships.

## Uncertainty and open questions

- The public GitHub page for AJ’s repository was not extractable during this run, so public-repository metadata was not used as evidence.[4]
- The scout did not execute the live regeneration script this morning; the report describes its assertions and the checked-in implementation, not a new pass count.
- The current client behavior for reconnecting during an in-flight generation needs a dedicated test; source inspection alone cannot establish that it is correct.
- It remains undecided whether a selected variant should merely change display or should create a first-class branch/continuation record. World Session semantics should decide this explicitly.
- WebSocket transport does not solve replay, persistence, or event ordering by itself; those remain Agora responsibilities.[3]

## Why this matters to AJ

Agora already has the important non-destructive invariant. The next high-value step is protocol hardening, not a migration: make generations addressable, make reconnect behavior deterministic, and expose causal staleness before adding more branching features. That preserves the project’s current strengths while reducing the risk that a late model response or dropped browser connection corrupts a long-running scene.

## Sources

[1] https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode
[2] https://hermes-agent.nousresearch.com/docs/guides/automate-with-cron
[3] https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
[4] https://github.com/andersjensen10/agora-chatroom

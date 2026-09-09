---
status: shipped
origin: feature-request
source: "[[Next Level Agentic Chatroom Project-ARCHIVE]]"
criticality:
  impact: medium
  urgency: low
size: M
dependencies:
  - "Stable LLM streaming"
  - "Piper / Kokoro local TTS"
matured: 2026-09-08
matured_by: Scrummaster
---

# Sentence-Streaming TTS Pipeline for Low-Latency Playback

## Context
Extracted from [[Next Level Agentic Chatroom Project-ARCHIVE]] (Priority: P2 stretch) and [[improvements]] §4.1. Currently, TTS generation waits until the LLM finishes generating the entire paragraph or turn before submitting text to Kokoro or Piper. On long persona responses, this causes an awkward 5–10 second silence before any speech begins. By chunking incoming streamed tokens into sentence boundaries and dispatching Sentence 1 immediately, felt audio latency drops to ~400ms. Criticality is Medium impact and Low urgency.

## User story
As a user listening to spoken persona responses, I want audio playback to begin on the first completed sentence while the rest of the response is still generating, so that conversation feels fluid and immediate.

## Acceptance criteria
- [ ] Server-side streaming buffer accumulates LLM tokens and splits on sentence punctuation (`.`, `!`, `?`, `\n`) while respecting abbreviations and ellipses (`...`).
- [ ] The first completed sentence is dispatched immediately to the active TTS engine (Piper or Kokoro) via WebSocket or SSE.
- [ ] Client audio player maintains a sequential chunk queue that plays synthesized sentence audio buffers back-to-back without audible gaps, pops, or overlapping audio.
- [ ] If the user or model interrupts generation (via cancel or new turn), any pending TTS chunks in synthesis or in the client playback queue are immediately cancelled.
- [ ] Fallback handling: If a sentence chunk synthesis fails, remaining sentences continue playing and the transcript displays the text unhindered.

## Implementation notes
- Server streaming logic lives in `apps/server/src/chat/stream.ts` and `apps/server/src/tts/`.
- Client audio playback queue lives in `apps/web/src/lib/` (audio store / player).
- Be mindful of WebSocket payload sizes; stream binary audio buffers or base64 chunks with chunk sequence numbers.
- Ensure sentence splitting handles dialogue quotation marks (`"Wait!" she said.`) without mangling speaker turns.

## Non-goals
- Full-duplex real-time voice interruptions (that is Phase D voice mode).
- Modifying pitch or emotional inflections across sentence chunks.

## Definition of done
- Unit tests verify sentence boundary splitting with varied punctuation edge cases.
- `npm run verify` clean (typecheck, svelte-check 0 errors, vitest pass).
- Live test demonstrates audio playback starting prior to LLM completion.

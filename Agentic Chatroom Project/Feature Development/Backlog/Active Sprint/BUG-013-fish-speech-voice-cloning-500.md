---
status: ready-for-development
origin: bug
source: "[[Next Level Agentic Chatroom Project-ARCHIVE]]"
criticality:
  impact: medium
  urgency: high
size: S
dependencies:
  - "Spark Fish Speech service at 192.168.0.139:8080"
matured: 2026-09-08
matured_by: Scrummaster
---

# BUG-013 — Fish Speech Voice Cloning 500 Server Error

## Context
Extracted from [[Next Level Agentic Chatroom Project-ARCHIVE]] (Priority: P1) and session notes. Per-persona cloned voices are a key feature of Agora's audio studio. However, invoking voice cloning via Fish Speech on the Spark (`http://192.168.0.139:8080`) consistently fails with HTTP 500 Internal Server Error. While standard TTS generation functions, cloning reference audio is completely broken. Criticality is Medium impact (fallback voices exist) and High urgency (blocks persona personalization).

## Bug
Uploading a reference audio file for a persona and triggering a cloned TTS generation fails:
1. Navigate to Persona editor -> Voice settings.
2. Select Fish Speech engine and provide reference audio.
3. Trigger voice synthesis preview or message speech generation.
4. Server POST to `http://192.168.0.139:8080/v1/invoke` (or cloning endpoint) returns `500 Internal Server Error`.
5. Frontend displays generic failure or stalls waiting for audio buffer.

## Acceptance criteria
- [ ] Root cause identified on Spark Fish Speech service (investigate CUDA environment, reference audio format/sample rate requirements, missing weights, or invalid request payload).
- [ ] Agora server-side Fish TTS client (`apps/server/src/tts/` or `packages/tts/`) validates reference audio format before dispatch and provides structured error logging.
- [ ] Client gracefully handles Fish Speech cloning failures with clear user-facing error feedback (preventing infinite loading spinners).
- [ ] A voice cloning test request with valid reference audio returns HTTP 200 and valid playable audio.
- [ ] Regression test verifies graceful error handling when Fish Speech service is offline or returns non-200.

## Implementation notes
- Check `packages/tts/` and server-side TTS coordinator in `apps/server/src/tts/`.
- Fish Speech service runs on Spark at `http://192.168.0.139:8080`.
- From [[LAN notes]]: Fish Speech plain generation works but cloning 500s. Verify what payload/multipart format the Spark container expects.
- Ensure audio error feedback aligns with [[BUG-05-tts-error-feedback]].

## Non-goals
- Rebuilding or re-training the underlying Fish Speech model.
- Implementing client-side audio trimming tools.

## Definition of done
- Verification script or test curl against `http://192.168.0.139:8080` confirms successful clone generation or clean fallback.
- `npm run verify` passes with 0 errors.
- Regression test added to `packages/tts` or server test suite.

---
tags: [project/agora, type/active-sprint]
status: resolved
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
resolved: 2026-09-10
resolved_by: Herm
---

# BUG-013 — Fish Speech Voice Cloning 500 Server Error

## Resolution (2026-09-10)
**Root cause: `torchcodec` was missing from the Fish Speech venv on the
Spark** (`/home/aj/fish-speech/.venv-cuda`). Installing it fixed every
cloning path — saved references, one-shot inline references, and control
tags all verified working with real (non-silent) audio output. Full
benchmarking + tuning writeup: [[Fish Speech TTS]].

This bug's Agora-side acceptance criteria (client validation, error
feedback, regression test) are **still open as follow-up work** if AJ wants
the app-layer hardening — the server-side 500 itself is fixed and no longer
blocks persona voice cloning.

## Context (original)
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
- From [[Fish Speech TTS]]: root cause was a missing `torchcodec` dependency
  in the venv, now fixed. Cloning payload/multipart format is documented
  there and in the `home-lab-infrastructure` skill's `fish-speech-tts.md`.
- Ensure audio error feedback aligns with [[BUG-05-tts-error-feedback]].

## Non-goals
- Rebuilding or re-training the underlying Fish Speech model.
- Implementing client-side audio trimming tools.

## Definition of done
- Verification script or test curl against `http://192.168.0.139:8080` confirms successful clone generation or clean fallback.
- `npm run verify` passes with 0 errors.
- Regression test added to `packages/tts` or server test suite.

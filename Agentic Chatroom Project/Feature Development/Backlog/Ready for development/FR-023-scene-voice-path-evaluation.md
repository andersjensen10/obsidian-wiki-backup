---
status: ready-for-development
origin: board-request
source: "[[WO-013-scene-media-studio-layer-two-ARCHIVE]]"
criticality:
  impact: medium
  urgency: medium
size: M
dependencies:
  - "Fish Speech and LTX/ComfyUI voice-capable paths reachable for live trials"
  - "Representative configured World/Scene dialogue fixtures"
matured: 2026-09-16
matured_by: Scrummaster
---

# Scene narration and dialogue voice-path evaluation

## Context
Matured as the second sequenced part of [[WO-013-scene-media-studio-layer-two-ARCHIVE]]. The CEO requires an evidence-based choice between the existing LTX voice path and Fish TTS's voice-acting potential for scene narration/dialogue; treating this as a research/evaluation story keeps it from blocking the video-editor slice ([[FR-021-post-scene-video-recreation-and-editing]]) or silently assuming one engine is better.

## User story
As the product team, I want a repeatable live comparison of supported voice-generation paths for the same scene narration and dialogue material, so that the supported path is selected using quality and operational evidence rather than expectation.

## Acceptance criteria
- [ ] A documented evaluation fixture set contains representative narrator and character dialogue drawn from a configured World/Scene without including model reasoning or private user data.
- [ ] The evaluation runs the same fixtures through the available LTX and Fish TTS paths, records success/failure, latency, output duration, intelligibility/continuity observations, expressive-fit observations, and operational constraints.
- [ ] Output artifacts and metadata are retained with provenance sufficient to reproduce the comparison; unavailable infrastructure is recorded as blocked rather than omitted or counted as a pass.
- [ ] The evaluation document makes a clear supported-path recommendation, fallback behavior, and unresolved risks; it does not overclaim subjective results as automated truth.
- [ ] If a product wiring change is needed to exercise a supported path, it preserves existing TTS behavior and has a bounded, separately testable route.

## Implementation notes
- Read the current Agora TTS service/client paths and the Fish service integration before adding any adapter; do not treat an old README model name as current infrastructure truth.
- Use actual reachable services and browser playback where appropriate, plus a repeatable recorded checklist; avoid synthetic quality scores without documented rubric/observer method.
- Keep this evaluation outside the deferred full-duplex voice work in `improvements.md` Phase D.
- Never claim cloned voice content is licensed/approved merely because a source is technically accessible.

## Non-goals
- Full-duplex voice, VAD/STT, automated source-video extraction, or a broad voice-cloning pipeline.
- Selecting a product brand voice or implementing every TTS UI improvement.
- Blocking FR-021 or the Farscape pilot on an automated voice-cloning result.

## Definition of done
- `npm run verify` passes if product code changes; documentation-only work has no fabricated code-gate claim.
- A real run against each reachable candidate path produces the comparison record and referenced output artifacts; unreachable paths are explicitly marked blocked with the observed failure.
- Browser playback is checked for each generated artifact used in the recommendation.
- The recommendation, fallback, fixtures, commands, raw measurements, and limitations are committed in a reproducible project document.

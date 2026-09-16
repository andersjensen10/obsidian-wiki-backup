---
status: shipped
origin: board-request
source: "[[WO-013-scene-media-studio-layer-two-ARCHIVE]]"
criticality:
  impact: high
  urgency: medium
size: L
dependencies:
  - "FR-012-scene-media-and-library (shipped)"
  - "FR-013-flexible-comfyui-workflows (shipped)"
  - "FR-009/FR-010 Worlds & Scenes (shipped)"
  - "ComfyUI at 192.168.0.139:8188 for live verification"
matured: 2026-09-16
matured_by: Scrummaster
---

# Post-scene video recreation and media editing flow

## Context
Matured from [[WO-013-scene-media-studio-layer-two-ARCHIVE]]. Layer one already provides in-scene POV image requests and World/Scene library persistence, and imported ComfyUI workflows now expose generation parameters. The next bounded media slice is to turn a completed Scene into a video recreation that opens in an editor-oriented flow instead of becoming an opaque raw file; voice evaluation remains a separate research decision to avoid coupling risky infrastructure experiments to this user-facing flow.

## User story
As a user who finishes a Scene, I want to request and refine a video recreation from its established content in an editing-oriented media flow, so that I can retain and shape a meaningful record of the story.

## Acceptance criteria
- [ ] A completed Scene offers a guided video-recreation action that uses Scene/World context and the selected supported video workflow, without requiring a raw workflow prompt.
- [ ] The generated video is persisted in the existing media library with World/Scene provenance and remains retrievable after reload/server restart.
- [ ] On completion, the user enters an editor-oriented view with at least preview, clip metadata/provenance, editable generation parameters, and a regenerate/variation path; it is not a direct file download dead end.
- [ ] The editor reuses existing media service/template/variation mechanisms where applicable and handles ComfyUI job progress, cancellation, and failures consistently with existing media UI.
- [ ] Legacy image/video generation and the current media library stay functional.

## Implementation notes
- Trace the shipped media service, route, Composer/lightbox, workflow-template, and generated-media schema paths end to end before designing UI; do not fork a raw new Comfy client.
- Reuse the imported-workflow parameter model and canonical LTX video workflow where available; unsupported custom nodes must fail explicitly.
- Keep prompt composition grounded in persisted Scene content and World configuration. Persist editor changes as generation metadata/derivatives, not untracked browser state.
- ComfyUI is shared and may flap: reuse established retries/progress/cancellation and perform the required live check against actual output.

## Non-goals
- A general non-linear video editor, timeline compositor, or arbitrary graph editor.
- Automated voice cloning or voice-engine selection; that is FR-021.
- Farscape-specific media assets (FR-022).

## Definition of done
- `npm run verify` passes with 0 errors/warnings.
- A new `scripts/live-scene-video-studio-check.mjs` runs a completed Scene through video recreation against live ComfyUI and confirms a retrievable World/Scene-tagged result plus derivative/regeneration metadata.
- Manual browser verification covers request, progress/cancel/failure handling, editor entry, parameter update/regeneration, reload, and library retrieval.
- Existing media live checks remain green.

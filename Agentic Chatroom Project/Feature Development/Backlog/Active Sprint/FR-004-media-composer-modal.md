---
status: shipped
origin: feature-request
source: "[[Next Level Agentic Chatroom Project-ARCHIVE]]"
criticality:
  impact: high
  urgency: medium
size: M
dependencies: []
matured: 2026-09-08
matured_by: Scrummaster
---

# Media Composer Modal (Slide-Over & Workflow Selector)

## Context
Extracted from [[Next Level Agentic Chatroom Project-ARCHIVE]] (Priority: P1) and [[improvements]] §3.2. Currently, triggering media generation in the chat composer falls back to a basic text prompt dialog (implemented in [[BUG-04-modal-dialogs]]). Users cannot select workflow presets (Flux Schnell vs Flux Dev vs LTX-2.3 video), choose aspect ratios, or attach reference images for character visual consistency. Criticality is High impact (essential UX for multimodal generation) and Medium urgency.

## User story
As a user in the chatroom, I want a dedicated Media Composer modal with workflow presets, aspect ratio selectors, reference image upload, and tag autocompletion, so that I can generate tailored images and videos without typing complex CLI-style flags.

## Acceptance criteria
- [ ] A dedicated `MediaComposer.svelte` modal or slide-over drawer triggered from the chat media action button (replacing generic prompt dialogs).
- [ ] Prompt textarea supporting multi-line entry with autocomplete suggestions for active persona appearance tags and room atmosphere descriptors.
- [ ] Workflow preset selector supporting:
  - `Flux Dev (Quality)`
  - `Flux Schnell (Fast)`
  - `LTX-2.3 Video (24fps / 5s)`
- [ ] Visual aspect ratio toggle buttons: `1:1 Square`, `16:9 Cinematic`, `9:16 Portrait`, `4:3 Classic`.
- [ ] Drag-and-drop reference image attachment zone with thumbnail preview and remove button.
- [ ] Form submission dispatches structured payload to server media endpoint; `Esc` or Cancel button cleanly dismisses without side effects.

## Implementation notes
- Create `apps/web/src/lib/MediaComposer.svelte` utilizing Svelte 5 runes (`$state`, `$derived`, `$props`).
- Integrate with room state and media submission in `apps/web/src/routes/rooms/[id]/+page.svelte`.
- API endpoints in `apps/server/src/routes/media.ts` accept workflow preset, aspect ratio, and optional reference image data.
- Ensure modal handles keyboard accessibility (focus trap, Esc to close, Tab navigation) following the pattern established in `apps/web/src/lib/Modal.svelte`.

## Non-goals
- Advanced node-based workflow graph editing (users select pre-configured presets).
- Live canvas sketching or inpainting tools.

## Definition of done
- `npm run check` passes with 0 errors and 0 warnings.
- `npx vitest run` passes all unit tests.
- Modal opens, populates presets, selects aspect ratios, and queues generation verified in real browser.

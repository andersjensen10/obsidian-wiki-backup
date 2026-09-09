---
status: shipped
origin: feature-request
source: "[[Next Level Agentic Chatroom Project-ARCHIVE]]"
criticality:
  impact: high
  urgency: medium
size: M
dependencies:
  - "ComfyUI up at 192.168.0.139:8188"
matured: 2026-09-08
matured_by: Scrummaster
---

# In-App Media Studio Lightbox with HUD, Variations, and Actions

## Context
Extracted from [[Next Level Agentic Chatroom Project-ARCHIVE]] (Priority: P1) and [[improvements]] §3.1. While [[BUG-11-media-lightbox]] fixed raw tab-opening by adding an initial `MediaLightbox.svelte` component, the full Phase B studio UX remains unbuilt. Users cannot inspect generation parameters (seed, sampler, steps, cfg) or trigger in-place variations, upscaling, or animations from chat images. Criticality is High impact (transforms passive media viewing into an interactive studio) and Medium urgency.

## User story
As a user viewing images and videos in the chatroom, I want to click any media element to open a full-screen studio lightbox displaying a metadata HUD and action toolbar (variations, upscale, animate with LTX-2.3, set as avatar, copy prompt), so that I can refine media without leaving the conversation flow.

## Acceptance criteria
- [ ] Lightbox displays a collapsible or overlay Metadata HUD showing: Seed, Steps, Sampler, CFG Scale, Model/Checkpoint, and duration (e.g. `20 steps in 4.8s`).
- [ ] Action buttons:
  - **Generate Variations**: Dispatches a new generation with the same prompt and a randomized seed.
  - **Upscale / Refine**: Dispatches an in-place high-res latent upscale workflow to ComfyUI.
  - **Animate with LTX-2.3**: Forwards the still image to the LTX-2.3 image-to-video workflow.
  - **Set as Persona Portrait**: Calls the API to update the author persona's avatar image.
  - **Copy Prompt / Workflow JSON**: Copies raw prompt or full workflow JSON to clipboard with visual toast feedback.
- [ ] Keyboard navigation: `Esc` closes the lightbox, `Left`/`Right` arrow keys navigate between media items in the current room's history.
- [ ] Handles media loading states, error states, and responsive layouts on mobile/tablet.

## Implementation notes
- Extend `apps/web/src/lib/MediaLightbox.svelte` (created in [[BUG-11-media-lightbox]]).
- Use ComfyUI client package `packages/comfyui-client` and server endpoints in `apps/server/src/comfy/`.
- ComfyUI is hosted on Spark (`http://192.168.0.139:8188`). Remember from [[NOTES]]: ComfyUI polling tolerates temporary unreachable states, but do not throw unhandled exceptions during queue delays.
- Persona avatar update endpoint lives in `apps/server/src/routes/personas.ts`.

## Non-goals
- Multi-track video timeline editing.
- Heavy client-side image editing (crop/filter canvas tools).

## Definition of done
- `npm run check` and `npm run typecheck` report 0 errors and 0 warnings.
- `npx vitest run` passes all tests.
- Lightbox HUD, action buttons, and keyboard controls verified interactively in a real browser session.

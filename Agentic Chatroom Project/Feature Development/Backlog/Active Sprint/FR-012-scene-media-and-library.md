---
tags: [project/agora, type/backlog]
status: shipped
origin: board-request
source: "[[WO-003-scene-media-and-studio-ARCHIVE]]"
criticality:
  impact: high
  urgency: medium
size: L
dependencies:
  - "Worlds & Scenes data model (FR-009/FR-010) — the media library must scope items to the originating World/Scene, which requires those entities to exist"
  - "Existing ComfyUI media pipeline: `apps/server/src/media/service.ts` (generateForPersona/generateVideoForPersona, generatedMedia table) and `apps/server/src/routes/media.ts` (media/template routes) — extended, not replaced"
  - "ComfyUI up at 192.168.0.139:8188 (Flux checkpoint) for live verification"
  - "FR-003/FR-004 (media lightbox, media composer modal) already shipped — POV image UI builds on that interaction pattern rather than a raw prompt box"
matured: 2026-09-10
matured_by: Scrummaster
---

# Scene media: in-scene POV image requests + media library (layer 1)

## Context
Source: [[WO-003-scene-media-and-studio-ARCHIVE]], matured from
[[Week 38 - Board Vision]] §3. The Board explicitly frames the full scene
media/studio arc as multi-sprint, maturing in layers — generation, then
library, then editing — and this story is scoped to **layer 1 only**: an
easy, configurable in-scene image-request action (a named character's POV,
or third person) plus a minimal per-user media library that ties each item
back to the originating World/Scene. Post-scene video recreation delivered
to an editor, and the LTX-vs-Fish TTS comparison, are later layers and are
explicitly out of scope here (see Non-goals).

`apps/server/src/media/service.ts` already has a working
`generateForPersona`/`generateVideoForPersona` pipeline, a `detectMediaRequest`
regex-based intent detector, and studio actions (`generateVariation`,
`upscaleMedia`, `animateMedia`) — this story extends that surface with a
POV-selection UI action and library persistence/scoping, it does not rebuild
generation from scratch. `generatedMedia` in `apps/server/src/db/schema.ts`
already stores `personaId`/`messageId`/prompt/seed/graph metadata; it has no
`worldId`/`sceneId` column today, so this story depends on FR-009/FR-010
landing a World/Scene id it can persist against. `composePrompt()` already
prepends a persona's `appearancePrompt` to a scene string — the POV-request
UI action is expected to reuse this rather than inventing a second prompt
composition path, and to pick which persona's appearance/perspective goes in
based on the "POV character" the user selects, defaulting to third-person
(no appearance prefix) when none is chosen.

## User story
As a user in a scene, I want to request a generated image from a specific
character's point of view (or third person) through a simple, guided UI
action — not a raw prompt box — and later find that image again in a
per-World/Scene media library, so that scene media becomes something I keep
and revisit rather than a one-off side effect of chat.

## Acceptance criteria
- [ ] A UI action within the scene (e.g. a composer/toolbar control building
      on the FR-004 Media Composer modal) lets the user pick "whose POV" —
      a specific character in the scene, or third person — without typing a
      raw prompt; free-text scene description remains available as a
      supporting field, not the primary interaction.
- [ ] Selecting a character's POV composes the request using that
      persona's `appearancePrompt`/perspective (extending `composePrompt`)
      rather than the always-narrator-voice default; third person omits a
      named character's appearance prefix.
- [ ] Generated images are recorded in `generatedMedia` (or its FR-009/
      FR-010-extended successor) tagged with the originating World/Scene id,
      not just `personaId`/`messageId` as today.
- [ ] A minimal per-user media library view lists generated items, filterable
      or scoped by the World/Scene that produced them, and lets the user open
      an item (reusing the existing FR-003 lightbox).
- [ ] A user can request a POV image and retrieve it afterward from the
      library view scoped to the originating World/Scene, end to end, in a
      live test — this is the story's literal success metric from the Board
      vision doc.
- [ ] Existing non-World/legacy room image-request flow (`detectMediaRequest`,
      `/api/media`) continues to work unchanged for rooms not attached to a
      World.

## Implementation notes
- Extend, don't replace: `generateForPersona` in
  `apps/server/src/media/service.ts` already threads persona + scene text
  through `composePrompt` and the ComfyUI template pipeline — add a POV
  character parameter and World/Scene id, don't fork a parallel generation
  path.
- `apps/server/src/routes/media.ts`'s `/api/media` listing endpoint takes a
  `personaId` query filter today; extend it (or add a sibling endpoint) with
  a World/Scene filter once that id exists on the row.
- The FR-004 Media Composer modal (`Active Sprint/FR-004-media-composer-modal.md`)
  already replaced the raw `window.prompt()` composer — the POV picker should
  be an addition to that modal's flow (a character-select control), matching
  its "no raw prompt box" precedent, not a new separate modal.
- ComfyUI is shared/rebootable (`NOTES.md`): reuse the existing tolerance for
  transient poll failures in `ComfyClient`/`client.generate()` rather than
  adding a second retry path for the POV-request flow.
- Media files are copied to local disk, never linked to ComfyUI's `/view`
  (`service.ts` comment: the shared server prunes its output dir) — the
  library view must serve from `/api/media/:id/file`, same as today.

## Non-goals
- Post-scene video recreation delivered to an editor interface (Board's
  layer 2/3 — separate future story).
- LTX vs. Fish TTS voice generation comparison (separate initiative per the
  vision doc's "voice" paragraph; not image/library work).
- Remixable/editable media library interactions (crop, recompose, multi-item
  edit) — Board explicitly calls this a later layer ("editing").
- Flexible/arbitrary ComfyUI workflow selection for this request type (that's
  WO-004/flexible generation workflows' scope, not this story's).
- Analytics/QA-scenario instrumentation of how a media request "plays out"
  (that's WO-006/validating-the-experience's scope).

## Definition of done
- `npm run verify` (typecheck + check + vitest + build) passes with 0
  errors/warnings.
- A new `scripts/live-scene-media-check.mjs`, following the pattern of the
  existing `scripts/live-chat-image-check.mjs` and `scripts/live-comfy-check.mjs`,
  exercises a POV image request against the live Spark ComfyUI and confirms
  the resulting item is retrievable from the library endpoint scoped to its
  World/Scene.
- Manually verified in a real browser session: POV picker in the composer,
  successful generation, and retrieval from the library view scoped to the
  originating World/Scene.

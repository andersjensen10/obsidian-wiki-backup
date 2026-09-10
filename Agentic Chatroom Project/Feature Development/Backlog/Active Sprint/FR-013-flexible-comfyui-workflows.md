---
tags: [project/agora, type/backlog]
status: shipped
origin: board-request
source: "[[WO-004-flexible-generation-workflows-ARCHIVE]]"
criticality:
  impact: high
  urgency: medium
size: M
dependencies: []
matured: 2026-09-10
matured_by: Scrummaster
---

# Flexible ComfyUI Workflow Import & Parameter Exposure

## Context
Matured from [[WO-004-flexible-generation-workflows-ARCHIVE]], itself scoped
from [[Week 38 - Board Vision]] §4. Board-originated (`origin: board-request`);
per the urgency-floor rule this would default to at least medium, and the
vision doc's own sequencing table independently calls flexible workflows
"largely independent; can run alongside anything" — so it stays at medium
rather than being pushed to high, with no conflict between the floor rule and
the stated reason.

Today `apps/server/src/media/service.ts` seeds exactly two hardcoded graphs —
`DEFAULT_TEMPLATE_GRAPH` (Flux image) and `DEFAULT_VIDEO_TEMPLATE_GRAPH` (LTX
video) — into the `workflowTemplates` table (`apps/server/src/db/schema.ts`)
on first boot via `seedDefaultTemplate()`. The `{{slot}}` templating mechanism
(`packages/comfyui-client/src/template.ts`: `applyTemplate`, `templateSlots`,
`assertApiFormat`) already exists and is generic — it walks any API-format
graph and substitutes `{{token}}` string values, so it does not need to
change. What's missing is a way for a user to **import their own graph file**
(AJ has an existing collection of image/video workflows from other projects)
and have its `{{slot}}` tokens surfaced as an editable form, instead of only
ever running the two seeded templates. `findTemplate()` already supports
per-persona `templateId` pinning and per-kind (`image`/`video`) defaults —
imported workflows plug into that same lookup, no new selection mechanism
needed.

The persona editor's Appearance tab (`apps/web/src/lib/persona/
TabAppearance.svelte`) already has a `<select>` bound to `persona.templateId`
listing `templates: WorkflowTemplate[]` — this is the natural home for
"upload a workflow" rather than a new page.

## User story
As a power user with my own ComfyUI workflow collection, I want to upload an
arbitrary API-format workflow JSON file and have its input slots exposed as
editable parameters in the app, so that I can run any of my own image or
video workflows — through a persona's generation and through the chat
interface — without the app's hardcoded templates being the only option.

## Acceptance criteria
- [ ] A workflow import endpoint (e.g. `POST /api/workflow-templates`)
      accepts an uploaded ComfyUI API-format JSON graph, validates it with
      `assertApiFormat` (rejecting UI-format `nodes`/`links` exports with the
      existing actionable error message), extracts its slots via
      `templateSlots()`, and stores it in `workflowTemplates` with a
      user-supplied name and `kind` (`image`/`video`).
- [ ] The Appearance tab's workflow `<select>` (`TabAppearance.svelte`) gains
      an "Import workflow…" file-upload control alongside the existing
      dropdown; a newly imported workflow appears in the list immediately
      without a page reload.
- [ ] When a persona has an imported workflow pinned (`persona.templateId`),
      that workflow's declared slots not already covered by the standard set
      (`positive`, `negative`, `seed`, `width`, `height`, `steps`, `frames`,
      `fps`, `referenceImage`, `sourceImage`) are surfaced as additional
      user-editable fields wherever generation is triggered (persona
      generation and chat `/image` / `/video` requests), not silently
      dropped.
- [ ] Unfilled/unknown slots still throw the existing `ComfyError` from
      `applyTemplate` (no silent `{{token}}` leakage into a job) — this is
      "don't change the mechanism," just confirm the import path routes
      through it.
- [ ] `findTemplate()`'s existing per-persona-pin / per-kind-default lookup
      is reused unchanged for imported workflows — no parallel selection
      path.
- [ ] At least one imported image workflow and one imported video workflow
      from AJ's real collection each run end-to-end through
      `generateForPersona` / `generateVideoForPersona`, producing a real
      file in `config.mediaDir`, verified live against the Spark's ComfyUI
      (`http://192.168.0.139:8188`).
- [ ] A basic "my workflow library" list view (could live in Settings or on
      the Appearance tab) lets a user see all imported workflows by name and
      kind, and delete ones no longer wanted — supports the Board's stated
      expectation of converging to a small canonical set over time, rather
      than the collection growing unbounded with no way to prune it.

## Implementation notes
- Reuse `applyTemplate` / `templateSlots` / `assertApiFormat` from
  `@agora/comfyui-client` as-is; this story is exposure and import UX, not a
  templating-engine rewrite.
- `workflowTemplates.slots` (JSON column) already stores the slot list per
  template — the dynamic-parameter form reads directly from that column
  rather than re-deriving slots client-side.
- Chat-triggered generation (`detectMediaRequest` in `service.ts`) currently
  has no notion of "which workflow" — routing a chat-triggered request to a
  specific imported workflow (vs. the kind default) is in scope only at the
  level of "the persona's pinned template is honored," not a new slash-command
  workflow picker (see Non-goals).
- `seedDefaultTemplate()` stays as-is; imported workflows are additive; the
  two seeded defaults remain the out-of-the-box fallback.
- Validate file size / JSON parse errors client- and server-side before
  hitting `assertApiFormat` — a malformed upload should fail with a clear
  message, not a 500.

## Non-goals
- No node-graph visual editor — import is JSON-file-in, form-out, matching
  the existing Media Composer's "presets, not a graph editor" non-goal from
  FR-004.
- No automatic canonicalization/curation of the imported set in this story —
  the Board's "converge over time" direction is a future decision informed
  by usage, not something this story builds tooling to automate. The delete
  capability above is sufficient for now.
- No new slash-command syntax for picking a workflow mid-chat; workflow
  selection stays scoped to the persona's pinned template for this story.
- No support for missing/unresolvable custom node types in an imported
  graph beyond a clear error — swapping in unavailable ComfyUI custom nodes
  is a ComfyUI-side problem, not something this story papers over.

## Definition of done
- `npm run verify` (build:packages, tsc -b apps/server, `npm run check -w
  @agora/web`, `npx vitest run`) passes clean.
- New unit coverage in `packages/comfyui-client/src/template.test.ts` and/or
  a server-side test for the import endpoint (reject UI-format export,
  accept valid API-format graph, extract slots correctly).
- A new live script, `scripts/live-workflow-loader-check.mjs` (modeled on the
  existing `scripts/live-comfy-check.mjs`), imports one real image workflow
  and one real video workflow from AJ's collection, runs each end-to-end
  against the live Spark ComfyUI, and asserts a real output file is produced
  for both — this is the story's stated success metric and must be run, not
  just written.
- Import → parameter form → generate flow for one workflow browser-verified
  live (not just unit-tested), per the project's verify-gate convention in
  [[Agentic Chatroom]].

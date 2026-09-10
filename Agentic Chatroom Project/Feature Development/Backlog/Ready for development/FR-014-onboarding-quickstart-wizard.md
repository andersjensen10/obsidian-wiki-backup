---
tags: [project/agora, type/backlog]
status: ready-for-development
origin: board-request
source: "[[WO-005-onboarding-quick-start-wizard-ARCHIVE]]"
criticality:
  impact: medium
  urgency: medium
size: M
dependencies: []
matured: 2026-09-10
matured_by: Scrummaster
---

# Onboarding Quick Start Wizard for Persona/Scene Creation

## Context
Matured from [[WO-005-onboarding-quick-start-wizard-ARCHIVE]], itself scoped
from [[Week 38 - Board Vision]] §5. Board-originated (`origin: board-request`);
per the urgency-floor rule this would default to at least medium, and the
vision doc's sequencing table explicitly names this initiative
"independent, UI-only — good parallel-track filler" — a stated reason to
hold urgency at medium rather than raise it to high, satisfying the floor
rule without over-scoring low-dependency filler work.

The full-detail editor this wizard sits alongside already shipped as FR-005
(`Active Sprint/FR-005-tabbed-persona-studio.md`): `apps/web/src/routes/
personas/+page.svelte` orchestrates four tabs (`TabIdentity`, `TabVoice`,
`TabAppearance`, `TabTraits`) plus a sticky save bar. The Board's framing is
explicit that "nothing here reduces capability" — the wizard is a new,
narrower entry point in front of that same editor state, not a replacement
for any of its fields. Persona creation today starts directly in the
full tabbed editor with no guided path; a first-time user has to understand
LLM connections, trait sliders, voice engines, and ComfyUI templates all at
once before getting a working persona. Scene/room creation has the same gap
— `rooms` (schema.ts) currently start from a bare create form.

## User story
As a first-time user, I want a guided Quick Start wizard that asks a few
simple questions and produces a working persona and scene, so that I can
start chatting without first learning every field in the full-detail editor
— while still being able to open that same persona/scene in the full editor
afterward and see (and change) everything the wizard set.

## Acceptance criteria
- [ ] A new Quick Start entry point (e.g. a "Quick Start" CTA on an empty
      personas/rooms state, or a first-run prompt) launches a wizard that is
      visually and structurally distinct from the tabbed editor — a linear,
      few-step flow, not a fifth tab.
- [ ] The wizard collects the minimum needed for a working persona: name,
      a short personality/appearance description (used to seed
      `systemPrompt` and `appearancePrompt`), and an LLM connection/model
      pick (reusing existing `connections` records — no new connection-setup
      UI in this story, see Non-goals).
- [ ] The wizard also produces a scene to talk in: reuses the existing
      `rooms` creation path under the hood (name + the new persona added via
      `roomPersonas`) rather than inventing a parallel room-creation
      mechanism.
- [ ] Completing the wizard writes real `personas` and `rooms` rows through
      the existing API routes (no wizard-only shadow data model) and lands
      the user directly in the new room, ready to send a first message.
- [ ] Every field the wizard set (name, system prompt, appearance prompt,
      connection/model, traits defaults, room name/membership) is visible
      and editable afterward in the existing tabbed editor
      (`TabIdentity`/`TabAppearance`/etc.) — nothing wizard-created is
      wizard-only or hidden from the full editor.
- [ ] Fields the wizard does not ask about (voice engine, workflow template
      pin, individual trait values, room canon/turn-mode) keep their
      existing defaults exactly as persona/room creation behaves today —
      the wizard does not silently change default behavior for anything it
      doesn't touch.
- [ ] Users who skip the wizard entirely can still create a persona/room the
      current way, unchanged.
- [ ] A first-time flow completes persona + scene creation via the wizard
      alone (no full editor touched at any point) in a live/manual check —
      this is the story's stated success metric.

## Implementation notes
- Build as a new component, e.g. `apps/web/src/lib/onboarding/
  QuickStartWizard.svelte`, using Svelte 5 runes, following the modal/focus-
  trap pattern already established in `apps/web/src/lib/Modal.svelte` (per
  the FR-004 precedent) rather than inventing new dialog primitives.
- Wizard submit should call the same persona-create and room-create API
  routes the full editor and room-creation form already use — do not write
  new server endpoints for this story; it's a client-side guided flow over
  existing capability.
- Trait defaults: use whatever `personas.traits` default new personas get
  today (unchanged) — the wizard does not need its own trait-seeding logic.
- Keep the wizard to genuinely few steps (name → vibe/description → model →
  done) — every additional step is exactly the friction this story exists
  to remove; resist folding in "just one more" optional field.

## Non-goals
- No new LLM-connection setup flow inside the wizard — if no `connections`
  row exists yet, the wizard should point the user at existing connection
  setup rather than reimplementing it.
- No reduction of the full-detail editor's fields or tabs — explicitly
  called out by the Board as out of scope ("nothing here reduces
  capability").
- No wizard-specific persistence layer or draft-save/resume mechanism —
  the wizard is a thin, one-shot guided form over the existing
  persona/room tables, not a new stateful flow.
- No mobile-specific wizard redesign beyond making it usable at the
  existing responsive breakpoints the app already supports.
- No changes to voice engine, workflow-template pinning, or ComfyUI setup
  inside the wizard — those stay on their existing defaults, editable later
  in the full editor.

## Definition of done
- `npm run verify` (build:packages, tsc -b apps/server, `npm run check -w
  @agora/web`, `npx vitest run`) passes clean.
- Unit/component coverage for the wizard's step logic and for the
  persona+room rows it produces matching what the full editor would show.
- A new live script, `scripts/live-onboarding-check.mjs` (modeled on
  `scripts/live-crud-check.mjs`/`scripts/live-multipersona-check.mjs`),
  drives the wizard end-to-end against a running server and asserts: a
  persona row and room row exist afterward, the persona is a member of the
  room, and every wizard-set field round-trips through the standard
  persona/room GET routes unchanged.
- Full first-time flow (wizard-only, no full editor touched) browser-
  verified live, matching the story's stated success metric, per the
  project's verify-gate convention in [[Agentic Chatroom]].
- Full editor confirmed (browser-verified) to display and allow editing of
  every field the wizard set, with no functionality lost.

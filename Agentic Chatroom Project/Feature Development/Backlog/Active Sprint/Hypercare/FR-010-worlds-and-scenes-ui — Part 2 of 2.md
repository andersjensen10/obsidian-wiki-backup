---
tags: [project/agora, type/backlog]
status: hypercare
hypercare_since: 2026-09-16
origin: board-request
source: "[[WO-001-worlds-and-scenes-ARCHIVE]]"
criticality:
  impact: high
  urgency: medium
size: M
dependencies:
  - "FR-009-worlds-and-scenes-data-model — Part 1 of 2"
matured: 2026-09-10
matured_by: Scrummaster
---

# Worlds & Scenes — UI (Part 2 of 2)

## Context
Extracted from [[WO-001-worlds-and-scenes-ARCHIVE]] (Week 38 Board Vision,
§1). Part 1 (FR-009) lands the World/Scene data model, migration, and API;
this story is the user-facing half — letting a user actually create,
select, and move between Worlds and Scenes, and see accumulated shared
history reflected in the UI. Scored urgency `medium` rather than `high`
(unlike Part 1) because it is sequenced strictly after FR-009 completes and
isn't itself the blocking dependency for the rest of the vision — Part 1 is.

## User story
As AJ, I want to create/select a World, host multiple Scenes within it, and
see that personas reference shared history from a prior Scene when I start
a new one in the same World, so that the Worlds & Scenes architecture is
actually usable rather than just present in the database.

## Acceptance criteria
- [ ] A World picker/switcher replaces (or sits alongside, for the
      degenerate single-room case) today's room list in the left-hand nav
      (see `apps/web/src/routes/+page.svelte`, `RoomMenu.svelte`).
- [ ] Within a selected World, a Scene switcher lets the user create a new
      Scene, close the current one, or resume a prior one — mirroring how
      `RoomMenu.svelte` handles rooms today, extended one level.
- [ ] Existing single-room users see their migrated World/Scene (from
      FR-009's migration) with no loss of function — chat, personas, theme,
      canon settings all still reachable exactly as before, just reframed.
- [ ] Starting a second Scene in a World that already has persona history
      visibly surfaces that history (e.g. persona greets referencing a prior
      Scene's events) without the user manually re-briefing — this is the
      UI-visible half of the vision's success metric (the data half is
      FR-009's).
- [ ] `RoomAtmosphere.svelte` / `RoomCanon.svelte` (setting/canon editors)
      are repointed at World-level canon with Scene-level override, matching
      the schema split from FR-009.
- [ ] `npm run check` (svelte-check) passes at 0 errors/warnings against the
      new components.

## Implementation notes
- `apps/web/src/lib/RoomMenu.svelte`, `RoomCanon.svelte`,
  `RoomAtmosphere.svelte`, and `roomSocket.ts` are the primary files to
  extend/rename — check how much can be generalized (Room → Scene) vs.
  needs a new sibling `WorldMenu.svelte`.
- This story assumes FR-009's REST/WS API is already live; if FR-009 ships
  with a slightly different route shape than anticipated, follow what
  actually shipped rather than this story's guesses.
- `fill_input()`-style DOM gotchas don't apply here (that's a browser-
  automation-testing note, not implementation), but Svelte 5 runes
  (`$state`, `bind:value`) patterns already used in `RoomMenu.svelte` should
  be followed for consistency.

## Non-goals
- Any backend schema/migration work — entirely FR-009's scope.
- Narrator pacing UI (FR-011) and scene media UI (FR-012) — this story only
  needs World/Scene navigation, not those features' own interfaces.
- The Farscape World pilot content itself.

## Definition of done
- `npm run verify` passes with 0 errors/warnings.
- A manual/live browser check (following the existing
  `scripts/live-bugfix-check.mjs` browser-automation pattern) walks:
  create World → create Scene → chat → create second Scene in same World →
  observe a persona reference prior-scene history in the UI.
- No regression in `scripts/live-multipersona-check.mjs` or
  `scripts/live-memory-check.mjs` run against the UI-driven flow.

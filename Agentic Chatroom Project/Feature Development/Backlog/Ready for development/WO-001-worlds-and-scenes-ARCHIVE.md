---
tags: [project/agora, status/archived, type/backlog]
status: promoted-to-backlog
origin: board-vision
source: "[[Week 38 - Board Vision]]"
created: 2026-09-10
authored_by: Senior Product Manager
---

# Worlds & Scenes — the architectural bet

## Vision
Rooms today are flat and disposable: one conversation, no persistence, no
relationship to the next. The Board's direction is to supersede rooms with
**Scenes** nested inside **Worlds** — a curated, persistent setting a user
roots their personas in, where a series of scenes accumulates shared memory
and history between the same characters over time. This is the single
biggest structural change in the Week 38 vision; nearly every other
initiative (narrator pacing, scene media, the eventual Farscape pilot)
builds on this data model.

## Goal
A data model and UI where a user can create/select a World, host multiple
Scenes within it, and have persona memory and trait-evolution state persist
and accumulate across those scenes — while today's single-scene,
single-room use keeps working as a fully supported degenerate case, not a
deprecated path.

## Success metric
A user can run two or more sequential scenes inside the same World and
observe personas referencing shared history/memory from the prior scene
without manual re-briefing, with zero regression in existing single-room
flows per `npm run verify` and the relevant `live-*-check.mjs` scripts.

---

## Matured — 2026-09-10 (Scrummaster)
Split into two sequenced stories (data model + backend first, since
everything else in the Week 38 vision depends on it existing):
- [[FR-009-worlds-and-scenes-data-model — Part 1 of 2]] — schema, migration,
  memory/trait scoping, API. High/High.
- [[FR-010-worlds-and-scenes-ui — Part 2 of 2]] — World/Scene picker,
  navigation, canon editors. High/Medium, depends on FR-009.

Split reason: schema + migration + memory/trait re-scoping + API surface
alone is a full L-sized backend effort; bundling the UI on top would clearly
exceed the ~100k token single-story budget.

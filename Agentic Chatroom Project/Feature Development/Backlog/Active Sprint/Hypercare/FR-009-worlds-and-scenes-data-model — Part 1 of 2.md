---
tags: [project/agora, type/backlog]
status: hypercare
hypercare_since: 2026-09-16
origin: board-request
source: "[[WO-001-worlds-and-scenes-ARCHIVE]]"
criticality:
  impact: high
  urgency: high
size: L
dependencies: []
matured: 2026-09-10
matured_by: Scrummaster
---

# Worlds & Scenes — Data Model & Backend (Part 1 of 2)

## Context
Extracted from [[WO-001-worlds-and-scenes-ARCHIVE]] (Week 38 Board Vision, §1).
Rooms today (`rooms` table in `apps/server/src/db/schema.ts`) are flat and
disposable: one conversation, no persistence, no relationship to any other
room. The Board's direction is to supersede rooms with **Scenes** nested
inside **Worlds** — a persistent setting where a series of scenes
accumulates shared persona memory and history over time — while today's
single-scene, single-room use keeps working as a fully supported degenerate
case, not a deprecated path. This is the single biggest structural change in
the Week 38 vision; Narrator intelligence (FR-011), scene media (FR-012),
and the eventual Farscape pilot all build on this data model, which is why
it's split out and sequenced first, and why it carries a High/High score
despite being backend-only — everything else in the vision is blocked on it
existing.

This is Part 1 of 2: the data model, migration, and server-side plumbing
only. Part 2 (a separate story, FR-010) covers the World/Scene UI —
World picker, Scene switcher, and updating room-scoped views to the new
framing. Splitting here because the schema + migration + memory/trait
scoping + API surface alone is a full L-sized backend effort; bundling the
UI on top would clearly blow past the ~100k token execution budget for a
single story.

## User story
As AJ (and, eventually, other users), I want personas to belong to a
persistent **World** made up of a sequence of **Scenes**, with persona
memory and trait state carrying across scenes in the same World, so that
characters feel like they have continuous history instead of resetting
every time a "room" is reopened.

## Acceptance criteria
- [ ] New `worlds` table: id, name, description/setting, canon, theme,
      createdAt/updatedAt — the World-level analog of today's per-room
      `setting`/`canon`/`theme` fields.
- [ ] New `scenes` table: id, worldId (FK), name, status (e.g.
      `active`/`closed`), turnMode, narrationEnabled, autoConverse,
      lastSpeakerId, createdAt/updatedAt/closedAt — effectively today's
      `rooms` row shape, but scoped under a World instead of standalone.
- [ ] `messages` gains (or is repointed via) a `sceneId` FK replacing/aliasing
      today's `roomId`, preserving the existing `seq`-based ordering
      (`messages_room_seq_idx` pattern) per-scene.
- [ ] A migration path exists for every existing `rooms` row: each becomes
      exactly one `worlds` row containing exactly one `scenes` row, with all
      of that room's messages, room-persona memberships, and generated media
      re-pointed at the new scene — this is the "existing single-room use
      keeps working as a fully supported degenerate case" requirement, not
      a deprecation.
- [ ] `apps/server/src/memory/store.ts` and `chat/memory.ts` recall/ingest
      paths are scoped by World (not just persona), so a persona's core +
      recall memories accumulated in Scene 1 of a World are available in
      Scene 2 of the *same* World without manual re-briefing, per the
      vision's success metric.
- [ ] Trait evolution (`traitEvents`, `chat/traits.ts`) persists and
      continues evolving across scenes within the same World — a trait
      shift in Scene 1 is visible at the start of Scene 2.
- [ ] REST routes exist for World and Scene CRUD (list/create/update/close
      a World; list/create/close a Scene within a World), following the
      existing `routes/rooms.ts` pattern (Fastify + Zod schemas in
      `@agora/shared`).
- [ ] WebSocket room/scene addressing (`routes/ws.ts`, `roomSocket.ts` on the
      client) is repointed at `sceneId` without changing the wire protocol
      shape more than necessary — this story is backend-first; the client
      only needs to keep functioning against the migrated data, not gain new
      UI (that's FR-010).
- [ ] `npm run typecheck`, `npm run check`, and `npx vitest run` all pass
      with 0 errors/warnings against the new schema.

## Implementation notes
- Start from `apps/server/src/db/schema.ts` — `rooms`, `roomPersonas`,
  `messages`, `memories`, `traitEvents`, `generatedMedia` are the tables
  touched or extended; follow the existing Drizzle patterns (text PK +
  `references()` + `onDelete` cascade) rather than introducing a new style.
- `messages_room_seq_idx` exists specifically because `created_at` is
  second-granular and ordering must be monotonic (see [[NOTES]] "Bugs found
  and fixed during the build" #1) — replicate that same index shape keyed on
  `sceneId`, don't regress it.
- `apps/server/src/memory/store.ts` currently scopes recall purely by
  `personaId`; this story adds a `worldId` dimension to that scoping without
  breaking the existing embedding/similarity-search path (sqlite-vec).
- `apps/server/src/chat/engine.ts` (`rowToPersona`, room-persona helpers) and
  `apps/server/src/routes/rooms.ts` are the two files most likely to need
  parallel `worlds.ts`/`scenes.ts` siblings rather than being rewritten in
  place — check how much of `rooms.ts` can be renamed/generalized vs. needs
  a genuinely new route file.
- Migration: write it as a real Drizzle migration (see existing
  `drizzle/` migration folder conventions in the repo) that runs against the
  live SQLite DB, not a throwaway script — this is state AJ's live Agora
  instance depends on.
- Reasoning-model gotcha applies to anything doing structured output during
  migration/scoring (e.g. if any migration step calls the LLM): budget
  generously, see [[NOTES]] "Reasoning models need a much larger token
  budget".

## Non-goals
- Any UI for creating/selecting/switching Worlds or Scenes — that's FR-010
  (Part 2).
- Narrator pacing behavior changes (FR-011) — this story only needs to not
  break the narrator's existing hook points.
- Scene media/library changes (FR-012) — `generatedMedia` is re-pointed at
  `sceneId` for correctness, but no new media capability is added here.
- The Farscape World pilot itself — explicitly out of scope per the vision
  doc's own deferral.

## Definition of done
- `npm run verify` (typecheck + check + vitest + build) passes with 0
  errors/warnings.
- `scripts/live-multipersona-check.mjs` and `scripts/live-memory-check.mjs`
  pass against the migrated schema (both currently exercise room-scoped
  persona/memory behavior end to end and are the closest existing live
  checks to this story's surface area).
- A new `scripts/live-worlds-scenes-check.mjs` is added that: creates a
  World, creates two Scenes in it, has a persona accumulate a memory in
  Scene 1, and verifies that memory/trait state is visible when generating
  in Scene 2 of the same World — this is the concrete verification of the
  vision's stated success metric and doesn't exist yet.
- Existing single-room flows (pre-migration data) are verified to still
  work end to end post-migration, with zero regression per the above.

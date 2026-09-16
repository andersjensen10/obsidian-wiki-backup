---
tags: [project/agora, type/backlog]
status: hypercare
hypercare_since: 2026-09-16
origin: board-request
source: "[[WO-002-narrator-intelligence-ARCHIVE]]"
criticality:
  impact: high
  urgency: medium
size: M
dependencies:
  - "Worlds & Scenes data model (FR-009/FR-010) — pacing is configured per World/Narrator profile, which requires the World entity and its scene history to exist"
  - "Existing narrator/turn-taking path in `apps/server/src/chat/` (auto-converse, `narrationEnabled` on `rooms`/future `scenes`)"
  - "`scripts/live-narrator-check.mjs` as the existing live-verification pattern to extend"
matured: 2026-09-10
matured_by: Scrummaster
---

# Narrator pacing intelligence

## Context
Source: [[WO-002-narrator-intelligence-ARCHIVE]], itself matured from
[[Week 38 - Board Vision]] §2. Today's narrator behavior is fixed/implicit —
there is a `narrationEnabled` boolean on `rooms` (see
`apps/server/src/db/schema.ts`) but no notion of *pacing*: when the narrator
should push a scene forward versus let it breathe. The Board is explicit
this is coupled work, not a trailing follow-up — without it, Worlds & Scenes
"will feel mechanical rather than alive." The Week 38 sequencing table
confirms this: Narrator intelligence packs with Worlds & Scenes (FR-009/
FR-010) as foundational work, not day-one-before-everything-else, which is
why urgency here is medium rather than high despite high impact — it ships
in step with the World/Scene data model, gated on that landing first.

Cross-referenced `apps/server/src/chat/` turn-taking logic and
`apps/server/src/db/schema.ts` confirm no existing `pacing` concept on
`rooms`, `personas`, or anywhere else — this is new surface, not a rename of
something implicit. The World/Scene schema work (FR-009/FR-010) is the
natural home for a `pacingProfile` (or similar) field; this story assumes
that migration lands the column/table shape it needs and does not attempt to
design the World/Scene schema itself.

## User story
As a user running a Narrator-driven World, I want to configure how eagerly
the Narrator advances a scene — from "let it breathe" to "keep it moving" —
per World or per Narrator persona, so that scenes feel paced to the story
I'm telling instead of following one fixed, implicit rhythm.

## Acceptance criteria
- [ ] A pacing setting (e.g. a small enum/scale — "slow burn" / "balanced" /
      "brisk", or an equivalent numeric dial) is editable in the World
      profile and/or the Narrator persona editor (whichever the FR-009/
      FR-010 data model exposes as the natural attachment point).
- [ ] The setting has a sensible default so existing single-room/no-World
      narrator behavior is unchanged until a user opts in.
- [ ] Narrator turn-taking/scene-advance logic reads the pacing setting and
      observably changes behavior at each end of the scale in a live test —
      e.g. time-to-advance or frequency of narrator-initiated beats measurably
      differs between "slow burn" and "brisk" against the same transcript
      shape.
- [ ] Changing the pacing setting mid-World takes effect on the next
      narrator decision point without requiring a scene restart.
- [ ] Setting is persisted and round-trips through a server restart (stored
      via Drizzle/SQLite, not in-memory only).
- [ ] No regression to existing `narrationEnabled` rooms that have not been
      migrated into a World (degenerate single-room case keeps working).

## Implementation notes
- Attach the pacing field to whatever World/Narrator-persona shape FR-009/
  FR-010 lands (do not invent a parallel schema path — if FR-009/FR-010
  hasn't shipped when this starts, block on it rather than bolting pacing
  onto the legacy `rooms` table).
- Narrator decision logic lives alongside today's turn-taking code in
  `apps/server/src/chat/` — trace the runtime path end-to-end before adding
  a new branch (per the `NOTES.md` gotcha: a fix can ship backend-only while
  the client still calls the old path).
- `personas.kind === 'narrator'` already distinguishes narrator personas
  from characters (`apps/server/src/db/schema.ts`) — pacing is plausibly a
  field on the narrator persona's config, a per-World override, or both;
  resolve the precedence in implementation notes once FR-009/FR-010's shape
  is known.
- Reasoning-model narrators need the same generous token budget as other
  structured/JSON side-calls (`NOTES.md`: reasoning models fill
  `reasoning_content` and leave `content` empty until they finish thinking) —
  don't let a pacing-scoring side-call regress into a silent empty-reply bug.

## Non-goals
- Designing the World/Scene data model itself (FR-009/FR-010's job).
- Multiple simultaneous pacing "modes" beyond a single configurable
  slow↔brisk dimension (e.g. no per-character pacing overrides in this pass).
- Any UI beyond the settings control itself (no visual pacing "radar" or
  analytics dashboard — that's `improvements.md` Director Mode territory,
  already shipped/parked separately).

## Definition of done
- `npm run verify` (typecheck + check + vitest + build) passes with 0
  errors/warnings.
- A new `scripts/live-narrator-pacing-check.mjs`, following the pattern of
  the existing `scripts/live-narrator-check.mjs`, demonstrates the pacing
  setting producing an observably different narrator-advance behavior
  between two settings against a live (or mock) LLM.
- Manually verified in a real browser session: setting is editable, persists
  across a server restart, and a live scene shows the behavior change.

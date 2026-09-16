---
status: ready-for-development
origin: board-request
source: "[[WO-010-narrator-agency-and-npc-development-ARCHIVE]]"
criticality:
  impact: high
  urgency: high
size: L
dependencies:
  - "FR-016-world-session-setup-player-sheet-and-safety"
  - "FR-017-narrative-control-surface"
  - "FR-009/FR-010 Worlds & Scenes (shipped)"
matured: 2026-09-16
matured_by: Scrummaster
---

# Guided narrator agency and persistent NPCs

## Context
Matured from [[WO-010-narrator-agency-and-npc-development-ARCHIVE]]. Worlds, cross-scene memory, and pacing now exist, but the vision requires the narrator to advance situations with judgment and to sustain NPC relationships rather than emit disposable turn text. This is a full L slice: it delivers one grounded agency model and persistent NPC state, not an unconstrained autonomous simulation.

## User story
As a player in a configured World Session, I want the narrator and supporting characters to introduce grounded developments and remember their evolving relationships across Scenes, so that the World feels alive while I remain the author of my own choices.

## Acceptance criteria
- [ ] The system supports persistent World-scoped NPC records with identity, role, motivations/agendas, flaws, relationship state, and relevant memory/history; an NPC can appear in multiple Scenes in the same World.
- [ ] The narrator can introduce or select an appropriate NPC and a scene beat (opportunity, obstacle, discovery, consequence, or escalation) using the World Session, narrative profile, current scene, player action, and established state.
- [ ] Generated narrator/NPC actions explicitly preserve player agency: they present consequences/opportunities and never narrate a player decision or prohibited content as fact.
- [ ] NPC relationship and consequence changes resulting from play persist and are available in a later Scene; no World-to-World leakage occurs.
- [ ] Narrator agency respects all FR-016 safety controls and FR-017 hard rules/strength controls.
- [ ] The user can inspect the active Scene's introduced NPCs and their non-sensitive established state; no hidden chain-of-thought/reasoning content is exposed.

## Implementation notes
- Model World-scoped entities alongside the shipped `worlds`, `scenes`, memory, and trait-event tables in `apps/server/src/db/schema.ts`; use a real Drizzle migration and foreign-key/cascade conventions.
- Extend the actual narrator turn path in `apps/server/src/chat/engine.ts`/related modules, not a standalone generator that chat never calls.
- Use structured model outputs with robust parsing and the existing reasoning-budget/retry approach; persist only validated narrative facts, never raw model reasoning.
- Keep user-facing state minimal and build on shipped World/Scene navigation; avoid a new unrelated NPC administration product.

## Non-goals
- Multi-agent background simulation while the user is absent.
- A full character-sheet editor for every NPC or freeform NPC marketplace.
- Automated Farscape-specific content (FR-022).

## Definition of done
- `npm run verify` passes with 0 errors/warnings.
- Unit coverage validates NPC/relationship scoping, narrator decision validation, and rejection of player-agency/safety-violating structured output.
- A new live/mock-LLM multi-scene check creates a configured World, causes one narrator event and NPC relationship change, starts a second Scene, and asserts the persisted facts inform the next turn.
- Manual browser verification demonstrates an introduced NPC, visible state, a player choice, and continuity in the next Scene.

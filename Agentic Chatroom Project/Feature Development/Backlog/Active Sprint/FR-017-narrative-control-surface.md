---
status: ready-for-development
origin: board-request
source: "[[WO-009-narrative-control-surface-ARCHIVE]]"
criticality:
  impact: high
  urgency: high
size: M
dependencies:
  - "FR-016-world-session-setup-player-sheet-and-safety"
  - "FR-011-narrator-pacing-intelligence (shipped)"
matured: 2026-09-16
matured_by: Scrummaster
---

# Editable World narrative control surface

## Context
Matured from [[WO-009-narrative-control-surface-ARCHIVE]]. FR-011 shipped a pacing control, but the CEO vision requires one understandable, persistent World-level model governing intervention, character autonomy, off-screen change, story dimensions, consequences, improvisation, and hard constraints. This must follow FR-016 so the controls share the World Session boundary model rather than create competing sources of truth.

## User story
As a World creator, I want an approachable in-world control surface for how my narrative behaves, so that I can adjust story intensity and narrator agency during play without breaking continuity or using engineering settings.

## Acceptance criteria
- [ ] A persisted World narrative profile covers narrator style/intervention, pacing, character autonomy, off-screen World change, drama/conflict/danger/mystery/romance/humor, consequence severity, improvisation range, and immutable never-do rules.
- [ ] The UI groups and explains these controls in stable, fiction-oriented language and offers sensible defaults derived from the existing behavior; it is not an unlabelled technical JSON/settings panel.
- [ ] The shipped pacing setting is migrated or integrated into this single profile with no duplicate/contradictory control.
- [ ] Updating a control applies to subsequent narrator/persona decisions in the active Scene and after a Scene transition, with existing established history retained.
- [ ] Hard boundary rules from FR-016 cannot be weakened by an ordinary narrative-control setting and remain enforced in prompt/context composition.
- [ ] The profile round-trips through REST, page reload, and server restart; legacy Worlds retain defined defaults.

## Implementation notes
- Extend the World configuration introduced by FR-016 and reuse the shipped narrator pacing path; do not attach a parallel control schema to scenes or personas.
- Locate actual narrator prompt/turn decision paths in `apps/server/src/chat/` and prove the runtime consumes the persisted profile rather than only rendering it.
- Prefer a typed shared profile/Zod schema with versioned/defaulted fields over scattered booleans, then reflect it in the Svelte World settings UI.
- Use existing modal, save, and accessible-control conventions; controls must remain legible on the supported responsive layout.

## Non-goals
- Creating NPC persistence or narrative events (FR-018).
- A per-character override matrix, analytics dashboard, or Director Mode revival.
- World visual theming (FR-019).

## Definition of done
- `npm run verify` passes with 0 errors/warnings.
- Unit coverage verifies profile defaults, validation, persistence serialization, and precedence of hard boundary rules.
- A new live/mock-LLM check changes representative low/high control values and asserts the next narrator decision receives the updated profile; it also proves continuity across a second Scene.
- Manual browser verification edits every control category, reloads, and confirms coherent in-world presentation and retained values.

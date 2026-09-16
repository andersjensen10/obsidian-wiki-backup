---
status: shipped
origin: board-request
source: "[[WO-008-world-session-configuration-and-safety-ARCHIVE]]"
criticality:
  impact: high
  urgency: high
size: L
dependencies:
  - "FR-009/FR-010 World and Scene APIs/UI (shipped)"
matured: 2026-09-16
matured_by: Scrummaster
---

# World Session setup, player sheet & content safety

## Context
Matured from [[WO-008-world-session-configuration-and-safety-ARCHIVE]]. Existing Worlds and Scenes provide the persistence and navigation foundation, but creation remains a low-context room-like flow and has no persistent representation of the player or enforceable content boundaries. This is high/high because every next-sprint narrative feature needs a coherent World premise and safety envelope; adult themes must never be enabled by default or through an ambiguous input path.

## User story
As a user, I want to describe and approve a World Session, establish a player character, and set explicit content boundaries before play, so that personas and the narrator treat me as a defined participant and the experience remains within my chosen limits.

## Acceptance criteria
- [ ] A guided World Session setup flow accepts a long-form premise and captures/editably persists world genre, scenario, tone, and story boundaries alongside the existing World fields.
- [ ] The flow creates and persists a player-character sheet with at least name, identity/role, freeform traits/details, and optional world-appropriate stats; it is associated with the World, not a single Scene.
- [ ] A user can review and edit the generated/entered World Session and player sheet after creation through normal product UI, without losing the existing World/Scene creation path.
- [ ] Content controls explicitly cover child-friendly status, violence/blood/gore level, adult-theme allowance, and freeform "never do this" rules.
- [ ] Adult themes remain disabled unless the user has explicitly confirmed they are over 18 in the same flow; server-side validation rejects an adult-enabled create/update without that explicit confirmation.
- [ ] World premise, player sheet, and active boundary values are included in narrator/persona generation context for the active Scene without exposing private confirmation metadata as chat content.
- [ ] Existing Worlds retain safe defaults after migration and legacy chat/World creation flows continue to work.

## Implementation notes
- Trace the shipped World/Scene schema and routes first (`apps/server/src/db/schema.ts`, `apps/server/src/routes/worlds.ts`/scene routes, shared Zod types) and extend those actual shapes rather than reviving room-only fields.
- Build on the existing Quick Start modal and full editors (`apps/web/src/lib/onboarding/`, `apps/web/src/routes/personas/+page.svelte`) but make this a World Session flow, not a second persona wizard.
- Put age/adult gating in shared server validation, not only disabled client controls; never infer age from a profile or locale.
- Thread compact, structured World Session context through the existing turn assembly in `apps/server/src/chat/engine.ts`; preserve the reasoning-model token-budget safeguards.
- Add a real Drizzle migration for all persistent fields and explicit defaults for existing rows.

## Non-goals
- The complete narrative control surface beyond storing/enforcing boundary values (FR-017).
- Autonomous narrator/NPC behavior (FR-018).
- A generalized account/identity or age-verification system beyond the explicit per-World confirmation.
- World-specific visual theming (FR-019).

## Definition of done
- `npm run verify` passes with 0 errors/warnings.
- A new live check creates and edits a World Session/player sheet, verifies safe legacy defaults, and proves the API rejects adult content without explicit over-18 confirmation.
- The same live check or a focused mock-LLM check proves the active World premise, player character, and boundary rules reach the turn prompt without leaking the confirmation flag.
- Manual browser verification completes setup, begins a Scene, reloads/restarts the server, and confirms all configured fields still display and edit correctly.

---
status: ready-for-development
origin: board-request
source: "[[WO-014-farscape-world-pilot-ARCHIVE]]"
criticality:
  impact: high
  urgency: medium
size: L
dependencies:
  - "FR-016-world-session-setup-player-sheet-and-safety"
  - "FR-017-narrative-control-surface"
  - "FR-018-guided-narrator-agency-and-persistent-npcs"
  - "FR-019-world-adaptive-design-system-and-review"
  - "FR-020-cross-scene-world-session-validation"
  - "FR-021-post-scene-video-recreation-and-editing"
  - "Curated Farscape research/reference material in the Obsidian vault"
matured: 2026-09-16
matured_by: Scrummaster
---

# Farscape World flagship pilot

## Context
Matured from [[WO-014-farscape-world-pilot-ARCHIVE]]. The CEO selected Farscape as the forcing-function pilot for the integrated persistent-World direction, not as an isolated content pack. The vault now contains active Farscape research, but the pilot is sequenced after the core product and validation stories so it exercises a real integrated surface; manually prepared voice assets are acceptable and automation must not block it.

## User story
As an internal pilot user, I want to configure and play a grounded Farscape World over multiple Scenes with curated characters, canon, and retained media, so that we can validate the complete World Session experience against a bounded real setting.

## Acceptance criteria
- [ ] A documented, locally curated Farscape reference set identifies approved canon sources, foundational characters, setting/scenario material, reference imagery, and provenance/usage constraints; speculative or uncited facts are clearly separated.
- [ ] A reusable Farscape World template/configuration creates a World Session with player-character setup, boundaries, narrator controls, foundational NPCs, and an appropriate World presentation profile.
- [ ] At least one multi-scene pilot path demonstrates canonical continuity, narrator/NPC agency, player choice, and retained World/Scene media without relying on unavailable automated voice extraction.
- [ ] Where voice is included, assets are manually prepared or explicitly omitted with a transparent rationale; no copyrighted source audio is silently ingested or claimed as automated.
- [ ] The cross-scene validation scenario runs against the pilot and produces a documented outcome and follow-up issues.

## Implementation notes
- Treat the vault's Farscape source register, character/episode notes, and research log as the content source of truth; follow their provenance and asset-handling rules.
- Use product APIs/templates rather than special-casing canon into application code. Canon and reference summaries should be editable World/NPC data.
- Separate source research/content curation from product code changes in commits and keep all content assets local/provenance-marked.
- Confirm what media and voice capabilities actually shipped before writing the pilot; manually prepared assets are a valid fallback, and automation is not a prerequisite.

## Non-goals
- Public release, commercial licensing analysis, or a full franchise wiki/encyclopedia.
- Automated extraction, cleaning, or cloning of character voices from source video.
- Implementing missing World/narrator/media/validation foundations; this story integrates them.

## Definition of done
- `npm run verify` passes for any app changes with 0 errors/warnings.
- The documented pilot setup is executed in a real browser through at least two Scenes and produces retrievable media where the shipped media path is available.
- `FR-020`'s cross-scene scenario runs against the pilot and writes its evidence report; blocked infrastructure is recorded as blocked, not passed.
- All pilot sources/assets have provenance documented and the final pilot readme identifies manual fallbacks and known limitations.

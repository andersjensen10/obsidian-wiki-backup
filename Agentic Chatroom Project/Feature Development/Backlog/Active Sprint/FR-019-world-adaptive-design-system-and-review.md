---
status: shipped
origin: board-request
source: "[[WO-011-world-adaptive-design-system-ARCHIVE]]"
criticality:
  impact: medium
  urgency: medium
size: M
dependencies:
  - "FR-016-world-session-setup-player-sheet-and-safety"
  - "FR-017-narrative-control-surface"
matured: 2026-09-16
matured_by: Scrummaster
---

# World-adaptive design system and integrated review

## Context
Matured from [[WO-011-world-adaptive-design-system-ARCHIVE]]. The new World Session experience needs atmosphere and recognizable visual identity, yet navigation and controls must remain stable across genres. This is intentionally sequenced after World configuration/control work so the design system decorates established product grammar rather than hardcoding a speculative interface.

## User story
As a user moving between Worlds, I want each World to feel visually distinct while the common controls remain familiar and usable, so that presentation strengthens immersion instead of creating navigation friction.

## Acceptance criteria
- [ ] A World can persist a bounded visual presentation profile using supported tokens/assets (e.g. palette, typography treatment, texture/motion preferences) with safe accessible defaults.
- [ ] At least two materially distinct World profiles demonstrate presentation adaptation across the active World/Scene/chat/settings surfaces without changing control placement, labels, keyboard behavior, or route semantics.
- [ ] World presentation is applied consistently after reload, direct navigation, and switching Worlds, without visual leakage into another World.
- [ ] Reduced-motion and contrast/accessibility behavior remain supported; theme decoration cannot make core controls unreadable or unusable.
- [ ] A documented integrated design review covers persona, World, Scene, narrative controls, and media entry points; it records evidence, prioritized issues, and decisions rather than claiming polish by inspection alone.

## Implementation notes
- Build on existing web design tokens and shipped generated-theme infrastructure; inspect actual `apps/web/src` styles/components before adding a new theming mechanism.
- Persist World-level choices through the World API/schema, avoiding document-global CSS mutation that leaks across Svelte navigation.
- Use a local review artifact under project documentation only if it belongs in code; do not edit vault overview pages.

## Non-goals
- A freeform theme editor or arbitrary remote asset upload.
- Rebranding/naming work (WO-007 remains separately parked).
- New narrator/NPC behavior or media editing.

## Definition of done
- `npm run verify` passes with 0 errors/warnings.
- Automated coverage verifies World profile persistence/default isolation and any token mapping helpers.
- Manual browser verification switches between two profiles through the core World/Scene/control workflows, including keyboard and reduced-motion checks.
- The design-review artifact is committed with findings and explicit follow-up disposition; no untriaged critical usability issue is labelled shipped.

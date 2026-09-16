---
status: shipped
origin: board-request
source: "[[WO-012-cross-scene-experience-validation-ARCHIVE]]"
criticality:
  impact: high
  urgency: high
size: M
dependencies:
  - "FR-016-world-session-setup-player-sheet-and-safety"
  - "FR-017-narrative-control-surface"
  - "FR-018-guided-narrator-agency-and-persistent-npcs"
  - "FR-015-experience-validation-scenarios (shipped)"
matured: 2026-09-16
matured_by: Scrummaster
---

# Cross-scene World Session validation scenarios

## Context
Matured from [[WO-012-cross-scene-experience-validation-ARCHIVE]]. FR-015 provides a metrics-producing live-scenario harness, but it predates the configured World Session, narrative controls, and persistent NPC requirements. This story turns it into the evidence gate for the integrated experience and is deliberately high/high: it must make risks visible before testing with people beyond AJ.

## User story
As the Senior QA Manager, I want repeatable multi-scene scenarios and decision-ready evidence for configured World Sessions, so that public-testing decisions are based on continuity, safety, agency, and usability signal rather than isolated feature checks.

## Acceptance criteria
- [ ] The existing scenario harness supports a versioned scenario definition that can create/configure a World Session, player character, boundaries, narrative controls, and at least two Scenes.
- [ ] One canonical scenario exercises cross-scene memory/relationship continuity, a narrator/NPC event, an in-session control change, and a boundary-sensitive prompt.
- [ ] Output records per-step latency and outcome plus explicit measures/observations for continuity, boundary adherence, narrator/NPC agency, control-change uptake, and usability; it separates unavailable infra/skips from product results.
- [ ] The report produces a clear public-readiness recommendation and an enumerated risk/blocked-evidence section without hardcoding subjective quality into a false pass/fail exit code.
- [ ] Scenario assets and usage instructions let the Senior QA Manager rerun or extend the scenario without editing runner internals.

## Implementation notes
- Extend the actual shipped scenario runner and definitions under `scripts/`; retain its existing honest blocked/infra reporting behavior.
- Reuse API/WS helpers rather than bypassing the runtime with direct DB writes.
- Design deterministic mock-LLM fixtures for structural assertions and retain a real Spark path for latency/quality evidence; never convert Spark unavailability into a green result.
- Make the readiness recommendation rule transparent and data-backed in the generated report/template.

## Non-goals
- A metrics database/dashboard or automatic CI quality threshold.
- Implementing the World, narrator, safety, or media features under test.
- Farscape-specific content (FR-022).

## Definition of done
- `npm run verify` passes with 0 errors/warnings.
- `node scripts/live-experience-scenario-check.mjs` (or its shipped successor) runs the canonical scenario against a running server and writes the complete report.
- A mock-backed run proves the scenario's continuity/boundary/control assertions; a live run captures actual latency or emits an explicit blocked record.
- Senior QA usage documentation is committed and manually followed from a clean shell invocation.

---
tags: [project/agora, type/hypercare]
status: hypercare
origin: feature-request
source: "[[Next Level Agentic Chatroom Project-ARCHIVE]]"
criticality:
  impact: low
  urgency: low
size: S
dependencies: []
matured: 2026-09-08
matured_by: Scrummaster
hypercare_since: 2026-09-10
---

# Interactive Tool Execution Cards in Chat Transcript

## Context
Extracted from [[Next Level Agentic Chatroom Project-ARCHIVE]] (Priority: P2 stretch) and [[improvements]] §5.1. Agora already has a server execution harness for persona skills (`calculator`, `web-search`, `dice`, `current-time`). While [[BUG-10-skill-trace-ui]] added a minimal `SkillTrace.svelte` accordion to reveal tool usage, the UI remains Spartan. Upgrading this to structured, expandable Tool Execution Cards with timing and parameter inspection brings Agora's agentic capabilities to the surface. Criticality is Low impact and Low urgency.

## User story
As a user watching personas converse, I want to see rich, interactive tool execution cards when an agent invokes a skill, displaying latency, input arguments, and formatted output, so that agentic reasoning is transparent and inspectable.

## Acceptance criteria
- [ ] Tool cards render above or within the persona message bubble when a `skill_used` event occurs.
- [ ] Card header displays:
  - Tool-specific icon (e.g. 🌐 for web search, 🎲 for dice, ⏱️ for time, 🧮 for calculator).
  - Concise query summary (e.g. `Web Search: "Copenhagen weather today"`).
  - Status indicator with execution timing badge (e.g. `[✓ 142ms]` or `[✗ Failed]`).
- [ ] Card is expandable to reveal:
  - Formatted JSON or pretty-printed input arguments.
  - Formatted execution result.
- [ ] Collapsed state maintains compact vertical height to prevent transcript bloat.
- [ ] Room settings includes a toggle to enable or disable specific skills per room.

## Implementation notes
- Elevate `apps/web/src/lib/SkillTrace.svelte` (created in [[BUG-10-skill-trace-ui]]).
- Invocations are received via WebSocket `skill_used` events and merged onto messages in `+page.svelte`.
- Server skills harness lives in `apps/server/src/skills/`.

## Non-goals
- Modifying the underlying execution sandbox or adding new external skill integrations.
- User-in-the-loop manual approval gates for skills (skills remain automated for personas).

## Definition of done
- `npm run check` clean with 0 errors and 0 warnings.
- `npx vitest run` passes.
- Visual inspection confirms cards render properly in both narration and dialogue bubble layouts.

---
tags: [project/agora, type/resolved-bug]
---

# BUG-10 — `skill_used` events had no UI

- **Severity:** Low · **Category:** Functional / extensibility
- **Status:** Fixed (front-end pass, 2026-09-06)

## Problem
The server emitted `{ type: 'skill_used', invocation }` when a persona ran a
tool (web-search, calculator, current-time, dice), but the web UI ignored the
event entirely — tool use was invisible.

## Fix
- `apps/web/src/lib/SkillTrace.svelte` renders each invocation as a badge/
  accordion (skill name, args, result).
- `+page.svelte` handles `onSkillUsed` (merging invocations onto the message,
  arriving before the reply row exists so the badge shows while the persona is
  still writing) and renders `<SkillTrace>` in both message layouts. Invocations
  restored from history on room load are shown too.

## Verification
- `npm run check` clean.
- `onSkillUsed` → `mergeInvocations` → `invocationsByMessage` → `<SkillTrace>`
  path is wired in both the narration and ordinary-bubble render sites.

## Related notes
- [[README]] — full Resolved Bugs index for this QA pass.
- [[Agentic Chatroom]] — project status snapshot.

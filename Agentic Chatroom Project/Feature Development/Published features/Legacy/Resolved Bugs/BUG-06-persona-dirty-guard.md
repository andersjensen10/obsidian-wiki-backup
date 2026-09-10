---
tags: [project/agora, type/resolved-bug]
---

# BUG-06 — Persona editor discarded unsaved edits on navigation

- **Severity:** Medium · **Category:** Functional / data integrity
- **Status:** Fixed (commit `10db5e6`)

## Problem
Editing a persona and then navigating away (Chat, Settings, another persona)
silently discarded all unsaved changes — no dirty tracking, no guard.

## Fix
`apps/web/src/routes/personas/+page.svelte`:

- A `$derived` `dirty` flag compares the current form state to the loaded
  baseline.
- SvelteKit's `beforeNavigate` intercepts navigation while `dirty` and prompts
  before discarding (skipped on `willUnload`).
- The save bar reflects dirty state (`class:is-dirty`) and the Discard button is
  disabled when clean.

## Verification
- `grep` confirms `beforeNavigate`, the `dirty` derived, and the guard.
- `npm run check` clean.

## Related notes
- [[README]] — full Resolved Bugs index for this QA pass.
- [[Agentic Chatroom]] — project status snapshot.

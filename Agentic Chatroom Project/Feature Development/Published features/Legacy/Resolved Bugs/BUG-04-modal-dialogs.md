---
tags: [project/agora, type/resolved-bug]
---

# BUG-04 — Blocking native `prompt()` / `confirm()` dialogs

- **Severity:** Medium · **Category:** UX / security
- **Status:** Fixed (commit `10db5e6`)

## Problem
Room/persona creation, image prompts, API-key entry, and deletions used
synchronous native `window.prompt()` / `confirm()`. These block the event loop,
can't be styled, break in embedded WebViews, and (for API keys) show secrets in
an unmasked field.

## Fix
Promise-based Svelte dialog components replace every native call:

- `apps/web/src/lib/dialog.ts` — `promptDialog()` / `confirmDialog()` helpers.
- `apps/web/src/lib/Modal.svelte` — accessible modal (focus trap, Esc, backdrop).
- `apps/web/src/lib/ConfirmDialog.svelte` — styled danger confirmations.
- Secret entry uses a password input rather than a visible prompt.

Call sites across `+page.svelte`, `settings/+page.svelte`, and
`personas/+page.svelte` now `await promptDialog(...)` / `confirmDialog(...)`.

## Verification
- `grep` confirms no remaining `window.prompt(` / `window.confirm(` /
  bare `prompt(`/`confirm(` calls in `apps/web/src` (only the helper docstrings
  mention them).
- `npm run check` clean.

## Related notes
- [[README]] — full Resolved Bugs index for this QA pass.
- [[Agentic Chatroom]] — project status snapshot.

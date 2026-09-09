# BUG-08 — Persona Save button buried below a huge form

- **Severity:** Medium · **Category:** UX / ergonomics
- **Status:** Fixed (commit `10db5e6`)

## Problem
The persona editor is a long single-column form (portrait, system prompt, LLM
params, voice, appearance, traits, memories). The only Save button sat at the
very bottom, forcing a long scroll after editing anything near the top.

## Fix
A sticky save bar (`.savebar`) pins Save/Discard to the top of the editor with
live dirty state (see also BUG-06). The front-end pass on 2026-09-06 corrected
its sticky offset (`top: 0`) so it stays flush while scrolling.

`apps/web/src/routes/personas/+page.svelte`.

## Verification
- `grep` confirms the sticky `.savebar` with `class:is-dirty`.
- `npm run check` clean.

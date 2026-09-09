# BUG-05 — TTS failures were silent

- **Severity:** Medium · **Category:** Functional / error handling
- **Status:** Fixed (commit `10db5e6`)

## Problem
Clicking "Speak this message" on a persona with no voice configured returned
HTTP 400, but the UI gave no feedback beyond a tiny red fragment in the footer.
Users assumed the button was broken.

## Fix
`apps/web/src/lib/speech.ts` now routes speech errors through
`toast.fail(err, 'Could not speak that line')`, so the failure surfaces as a
toast, and the message's speaker icon reflects an error state
(`speechState.errorId`, rendered with a red alert affordance in `+page.svelte`).

## Verification
- `grep` confirms `toast.fail` in `speech.ts` error path.
- `npm run check` clean.

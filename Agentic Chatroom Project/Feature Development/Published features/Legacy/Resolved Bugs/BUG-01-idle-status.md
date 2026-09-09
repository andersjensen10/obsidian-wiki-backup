# BUG-01 — Status bar showed `· replying: <persona>` when idle

- **Severity:** High · **Category:** UX / Status feedback
- **Status:** Fixed (commit `10db5e6`)

## Problem
The footer unconditionally appended `· replying: <first persona>` whenever the
room had personas, so an idle room permanently looked as if a generation were
in flight. Users assumed the app was frozen.

## Root cause
`+page.svelte` rendered `roomPersonas[0].name` as "replying" regardless of
whether a turn was actually running — it conflated the default respondent with
an active reply.

## Fix
The status line now only claims someone is replying when `typingPersonaId` is
set (i.e. a turn is genuinely streaming). Idle rooms show the neutral socket
state instead. See the `BUG-01` comment around the status line in
`apps/web/src/routes/+page.svelte`.

## Verification
- `npm run check` clean.
- Visual: an idle room no longer shows a "replying" suffix; it appears only
  while a persona streams.

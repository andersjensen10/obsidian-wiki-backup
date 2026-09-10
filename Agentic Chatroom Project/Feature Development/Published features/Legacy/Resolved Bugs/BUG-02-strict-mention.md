---
tags: [project/agora, type/resolved-bug]
---

# BUG-02 — "On mention" replied even with no mention

- **Severity:** High · **Category:** Functional / turn-taking
- **Status:** Fixed (commit `10db5e6`)

## Problem
With turn mode "On mention", an unaddressed message (e.g. "Hello everyone")
still forced the first persona to reply. Users could not speak into a
multi-character room without triggering a response.

## Root cause
`apps/server/src/chat/turns.ts` deliberately fell back to `personas[0]` when
nobody was addressed, so the room "wouldn't look broken" — contradicting the
mode's name.

## Fix
Added a distinct `strict_mention` turn mode that stays silent unless a persona
is explicitly addressed (`@mention` or `Name:`). The lenient `mention` mode
keeps its original fallback behaviour. When strict mode stays silent the server
emits a `no_reply` event so the UI can explain the silence instead of looking
stuck. An explicit mention always wins in every mode.

- `apps/server/src/chat/turns.ts` — `TurnMode` gains `strict_mention`;
  `selectSpeakers` returns no speakers when unaddressed in strict mode.
- `apps/server/src/routes/ws.ts` — emits `no_reply` on empty strict selection.
- `packages/shared/src/chat.ts` — `TurnMode` union + zod enums updated.

## Verification
- `apps/server/src/chat/strictmention.test.ts` (unit).
- `scripts/live-bugfix-check.mjs` — strict mode stays silent when unaddressed,
  replies when addressed, and lenient mode is unchanged.

## Related notes
- [[README]] — full Resolved Bugs index for this QA pass.
- [[Agentic Chatroom]] — project status snapshot.

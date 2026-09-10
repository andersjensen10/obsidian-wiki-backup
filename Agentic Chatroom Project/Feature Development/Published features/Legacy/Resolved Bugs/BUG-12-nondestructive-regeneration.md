---
tags: [project/agora, type/resolved-bug]
---

# BUG-12 — Regeneration destructively truncated the transcript

- **Severity:** Low (report) — but a genuine data-loss bug
- **Category:** UX / data retention
- **Status:** Fixed (this session, 2026-09-06)

## Problem
Clicking "Regenerate" on a persona reply permanently deleted that reply **and
every turn that followed it**. Wanting one alternate phrasing of an early turn
destroyed the rest of the conversation, with no confirmation and no recovery.

## What was already there (and why it wasn't enough)
The `10db5e6` commit was titled "…non-destructive regeneration" and shipped the
**backend** for it:

- a `variants` JSON column + `variant_index` on `messages`
  (`apps/server/src/db/schema.ts`, migrated in `db/index.ts`),
- `POST /api/messages/:id/regenerate` (non-destructive; only truncates on an
  explicit `?truncate=true`),
- `POST /api/messages/:id/variants` (append a variant) and
  `PATCH /api/messages/:id/variants` (switch variant),
  all in `apps/server/src/routes/editing.ts`.

But the **client was never rewired.** `regenerate()` in `+page.svelte` still
called the legacy destructive `api.rewindMessage()` (`POST …/rewind`), which
deletes the reply and everything after it. So in the actual app the bug was
still fully live — the non-destructive infrastructure sat unused, and there was
no UI to page between variants.

## Fix (this session)
Wired the client to the non-destructive path and added a variant switcher, over
the room WebSocket so the regenerated reply streams like a normal turn.

**Shared** (`packages/shared/src/events.ts`)
- New client event `{ type: 'regenerate', messageId }`.
- New server event `{ type: 'regenerating', messageId, personaId }` so the
  client can blank the bubble and stream the fresh text into it in-place.

**Server** (`apps/server/src/chat/engine.ts`, `apps/server/src/routes/ws.ts`)
- `getRoomHistory(roomId, limit, beforeSeq?)` — regeneration builds the prompt
  from the context as it stood *before* the target reply, so the alternative
  answers the same moment (not the reply itself or anything after it).
- `streamPersonaTurn({ …, beforeSeq })` threads that through.
- `appendVariant(messageId, content)` — appends the fresh text as a new variant,
  seeding index 0 from the current text so the original is never lost, and makes
  it the shown one. Message id, seq, and all downstream turns are untouched.
- `handleRegenerate()` in the WS handler: validates the target is a persona
  reply, emits `regenerating`, streams tokens into the same `messageId`, then
  stores the result via `appendVariant`. On empty/failed/cancelled generation
  the original text stands (re-sent on `message_done`).

**Client** (`apps/web/src/routes/+page.svelte`, `lib/roomSocket.ts`, `lib/api.ts`)
- `regenerate(m)` now sends the `regenerate` WS event instead of `rewindMessage`
  + delete. Nothing is removed from the transcript.
- `onRegenerating` blanks the shown text (stashing the original for restore) and
  sets `streamingId`; `onDone`/`onError`/`onCancelled` clear the in-flight flags
  and, on cancel/failure, restore the original text.
- A `‹ n/total ›` variant switcher (`variantSwitcher` snippet) lets the user
  page between stored generations; `showVariant()` persists the choice via
  `PATCH …/variants` (`api.selectVariant`).
- Removed the now-unused `api.rewindMessage`; the legacy `/rewind` endpoint is
  documented as deprecated (kept only for any external caller).
- Updated the regenerate tooltip (no longer "discards it and everything after").

## Verification
- `npm run typecheck` (server + packages) — clean.
- `npm run check` (svelte-check) — 0 errors, 0 warnings.
- `npx vitest run` — 229/229 pass.
- `scripts/live-bugfix-check.mjs` extended with a WebSocket regeneration check:
  asserts the `regenerating` event fires, fresh text streams into the **same**
  message id, both generations are kept as variants (original preserved),
  message count is unchanged, and a turn sent *after* the reply still exists
  (the old rewind would have destroyed it). Requires the Spark LLM + a running
  server (`node scripts/live-bugfix-check.mjs`).

## Note
This was the only bug from the report still unresolved in the running app; the
other 11 were already fixed (8 in `10db5e6`, plus BUG-03/07/10/11 in the
front-end pass that preceded this session).

## Related notes
- [[README]] — full Resolved Bugs index for this QA pass.
- [[Agentic Chatroom]] — project status snapshot.

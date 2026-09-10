---
tags: [project/agora, type/resolved-bug]
---

# BUG-09 — Aborting a turn dropped the socket and leaked the GPU job

- **Severity:** Medium · **Category:** System architecture / resources
- **Status:** Fixed (commit `10db5e6`)

## Problem
"Stop the current exchange" called `socket.close()` to signal abort. That forced
a reconnect + full room reload, and — critically — the server never told
ComfyUI to stop, so the GPU kept processing the diffusion/video job and held
VRAM.

## Fix
- **In-band cancel:** the client sends `{ type: 'cancel' }` over the live socket
  (`stopTurn` in `+page.svelte`); the socket stays open. The server aborts the
  per-turn `AbortController` and replies `{ type: 'cancelled' }`
  (`apps/server/src/routes/ws.ts`).
- **GPU interrupt:** `packages/comfyui-client/src/client.ts` `cancel()` deletes
  a queued job via `/queue` and interrupts a running one via `/interrupt`, wired
  to the abort signal so cancelling frees the GPU immediately.

## Verification
- `scripts/live-bugfix-check.mjs` — the server accepts an in-band cancel, the
  socket survives, and the ComfyUI queue depth drains after cancelling (a leaked
  job would leave it higher).

## Related notes
- [[README]] — full Resolved Bugs index for this QA pass.
- [[Agentic Chatroom]] — project status snapshot.

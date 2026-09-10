---
tags: [project/agora, type/run-log]
---

# Agora — session notes (2026-09-01)

Facts worth carrying forward. (Hermes memory hit its char cap this session;
re-add from here next time.)

## Project

- Path: `/home/aj/Desktop/Hermes/AgenticChatroomProject`, plan at `../PLAN.md`
- Stack: npm workspaces, SvelteKit (Svelte 5 runes) + Fastify + SQLite/Drizzle
- Ports: web `7480`, API/WS `7481` (clear of the unrelated Hermes agent on 9119)
- Phases 1–3 complete, verified against the live Spark and a real browser
- Phase 4 (mem0 + FalkorDB) is blocked: **neither docker nor podman is installed**
  on the laptop. Seam is ready at `apps/server/src/chat/memory.ts`
- Commits: `4e17451` (build), `1917bba` (live verification)

## Verified infrastructure

- llama.cpp on the Spark: `http://192.168.0.139:8014/v1`, model `gpt-oss-120b`,
  65k ctx, no auth. First token ~4.5s, then streams.
- ComfyUI: `http://192.168.0.139:8188`, v0.26.0, no auth.
  Checkpoints: `flux1-dev-fp8`, `ltx-2.3-22b-dev-fp8`, `ltx-2.3-22b-distilled-fp8`.
  Relevant to phase 6.

## Browser automation gotchas (cost real time this session)

- Chrome v152 is installed, but browser-harness' `chrome://inspect` toggle did
  **not** open the debug port. What works:
  ```bash
  google-chrome-stable --remote-debugging-port=9222 \
    --user-data-dir=/tmp/agora-chrome-profile --no-first-run about:blank
  ```
  launched in the background, then `browser_exec` connects normally.
- The harness prefixes controlled tab titles with a horse emoji. It is not
  coming from the page — `about:blank` shows it too.
- `fill_input()` assigns `.value` without dispatching events, so Svelte's
  `bind:value` never sees the change and the form stays empty. Use the native
  value setter plus `input`/`change` events:
  ```js
  Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value')
    .set.call(el, val);
  el.dispatchEvent(new Event('input', { bubbles: true }));
  ```

## Bugs found and fixed during the build

1. **Nondeterministic transcript order** — `created_at` is second-granular, so
   both turns of a fast exchange shared a timestamp and the UUID tiebreak was
   random. Added a monotonic `seq` column as the ordering key.
2. **Every DELETE returned 400** (`FST_ERR_CTP_EMPTY_JSON_BODY`) — the API
   client sent `Content-Type: application/json` with no body. Would have broken
   every delete button in the UI.

Both were caught by `scripts/e2e-smoke.mjs`, not by the type checker.

## ComfyUI resilience (found the hard way)

The Spark's ComfyUI is shared and gets rebooted. A scratch bash poller
reported "DONE" falsely because an empty curl response during a reboot is
not `{}` — which exposed the real bug: `ComfyClient.generate()` threw and
abandoned a job that was still alive in the queue whenever polling blipped.

Now: up to 15 consecutive poll failures are tolerated with a
"server unreachable, retrying" progress message, while a genuine
execution error (OOM etc.) still fails immediately. Covered by
`packages/comfyui-client/src/client.test.ts`.

## Reasoning models need a much larger token budget

`gpt-oss-120b` on the Spark is a REASONING model: it fills
`message.reasoning_content` and leaves `message.content` empty until it has
finished thinking. Trait scoring at `max_tokens: 200` therefore returned an
empty string with `finish_reason: "length"` — traits silently never changed,
and nothing logged an error.

Fixes: scoring budget raised to 1500 (retry at 4000), the scoring prompt made
terse (the chatty version made the model deliberate about output format until
it ran out of budget), and `LlamaCppProvider.complete()` now throws
`ReasoningBudgetError` instead of returning "" so the case is visible. Any
future structured/JSON side-call against a local reasoning model needs the
same generous budget.

## Process hygiene lesson

`pkill -f 'agora'` silently matched nothing — the real command lines were
`node apps/server/dist/index.js` etc. Always verify with `ss -tlnp` after
killing, rather than trusting the pkill exit code.

Worse: killing a wrapper PID leaves the `node` child holding the port, so a
"restart" silently fails with EADDRINUSE and the next test runs against the
OLD binary. This produced a passing test for a fix that had not been applied.
After any rebuild+restart, confirm the built file directly
(`node -e "import('./dist/...').then(...)"`) rather than trusting a green test.

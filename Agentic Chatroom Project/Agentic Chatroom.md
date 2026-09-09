# Agentic Chatroom (Agora) — Current State

> Last updated: 2026-09-07 by Herm. Source of truth for day-to-day dev detail
> is the in-repo skill (`agora-chatroom`) and `[[NOTES]]`; this page is the
> Obsidian-facing overview + status snapshot.

## What it is
Agora — AJ's local, multi-persona agentic chatroom. Personas are configurable
AI characters with their own LLM connection, TTS voice, appearance, and
memory. See `[[Agenti Chatroom long term]]` for the founding vision doc
(memory architecture, per-persona skills/TTS mannerisms, narrator/storyteller
roleplay mode, image/video gen for user + personas).

## Where it lives
- Path: `/home/aj/Desktop/Hermes/AgenticChatroomProject`
- **Git is LOCAL ONLY** — branch `master`, author `AJ <aj@local>`, no remote.
- Stack: npm workspaces — SvelteKit (Svelte 5 runes) web app + Fastify API/WS
  server + SQLite/Drizzle. Shared types in `packages/shared`.

## Live ports (verified 2026-09-07)
| Port | What |
|---|---|
| 7480 | web (older build, still listening) |
| 7481 | API / WebSocket server |
| 7495 | web (current dev, Vite HMR) |

Server (`apps/server/dist/index.js`) is run **manually**, not under a watcher
— server edits need a rebuild + restart. Web dev server (Vite) is live/HMR.

## Backing infra (see [[LAN notes]])
- LLM: llama.cpp on the Spark — `http://192.168.0.139:8014/v1`, no auth.
  Model is **variable**, currently `qwen3.8-27b-aggressive-q5` (reasoning
  model — thinking budget matters, see gotchas below). Historically
  `gpt-oss-120b`.
- Image/video: ComfyUI on the Spark — `http://192.168.0.139:8188`, no auth.
  Checkpoints: `flux1-dev-fp8`, `ltx-2.3-22b-dev-fp8/distilled-fp8`.

## Status: bug backlog — all 12 resolved
QA pass (`bug_report.md`, Sep 2026) found 12 bugs; all fixed and documented
under `Resolved Bugs/BUG-01..12-*.md` in the repo. Highlights:
- **BUG-12 (non-destructive regeneration)** was the hard one — client was
  still calling a destructive `/rewind` even though the backend had a
  variants API. Rewired to WS `regenerate` + a variant switcher (`< 1/3 >`
  turn pager). Verified 18/18 live against Qwen.
- BUG-01/02/09 (idle status, strict-mention turn-taking, in-band cancel +
  ComfyUI GPU `/interrupt`) fixed together in one pass.
- Nordic redesign (design tokens, per-room generated themes, light/dark)
  shipped and browser-verified.

## Recent change: thinking-off by default (commit `366e7b1`)
`config.thinkingEnabled` → env `AGORA_THINKING`, default **FALSE**. Toggle is
plumbed per-persona end to end. Gave a big speed win (~5x fewer tokens/turn)
by suppressing the reasoning-model chain-of-thought path.
**OPEN / UNTESTED:** the *qualitative* impact of thinking-off on persona
output quality has not been measured yet — needs a real eval, not just a
speed check.

## Verify gate (before calling anything "done")
From repo root: `npm run typecheck`, `npm run check` (svelte-check, target 0
errors/warnings), `npx vitest run` (~229 tests), or `npm run verify` for all
three + build. Live E2E: `scripts/live-bugfix-check.mjs` (needs the Spark up),
`scripts/live-regenerate-check.mjs` (mock LLM, no Spark needed).

## Known gotchas (full detail in the `agora-chatroom` Hermes skill)
- Reasoning-model empty replies = **budget exhaustion**, not a parsing bug —
  raise `AGORA_REASONING_RETRY_TOKENS`, don't touch the parser.
- A "Fix BUG-X" commit can ship backend-only while the client still calls the
  old path — always trace the runtime path end-to-end before trusting a fix.
- Killing a wrapper PID can leave the `node` child holding the port
  (EADDRINUSE on restart) — verify with `ss -tlnp` after any restart.
- Phase 4 (mem0 + FalkorDB persistent memory) was blocked as of 2026-09-01:
  neither docker nor podman installed on the laptop. Seam ready at
  `apps/server/src/chat/memory.ts`.

## Feature Development pipeline
Work now flows through `Feature Development/`: raw ideas land in
`Feature Requests` ([[improvements]] — the full architecture/UX blueprint),
get scoped into `Backlog` for near-term work, and ship into
`Published features/Sprint N - Week WW` once done.
- **Active backlog:** [[Next Level Agentic Chatroom Project]] (`Feature Development/Backlog`)
  — Sprint 1 (Week 37) plan: real Phase B UX (media lightbox/composer, tabbed
  persona editor), the thinking-off quality eval, and Spark LLM concurrency.
- **Full blueprint:** [[improvements]] (`Feature Development/Feature Requests`)
  — Director/Immersion mode, floor control, branching tree, media studio,
  sentence-streaming TTS, full-duplex voice, tool cards, command palette,
  tabbed persona editor, mobile drawer, custom modals. Phases A–C shipped in
  Sprint 1 (Week 37); Phase D deliberately parked — see [[Week 38 - Board
  Vision]].
- **Next-level vision:** [[Week 38 - Board Vision]] (`THE BOARD/Weekly
  Briefs`) — the active Board vision doc (AJ standing in for the Board role)
  covering what comes after the Sprint 1 baseline: Worlds & Scenes
  (supersedes the room-scoped roleplay framing below), Narrator intelligence,
  scene media studio, flexible ComfyUI workflows, onboarding wizards,
  pre-launch experience validation, the Farscape pilot, and an early rebrand.
  See also [[GOAL]].

## Related notes
- [[NOTES]] — running session log: infra facts, browser-automation gotchas,
  bugs found/fixed, process-hygiene lessons.
- [[Next Level Agentic Chatroom Project]] — active backlog/sprint plan.
- [[improvements]] — full UX/architecture blueprint & phasing.
- [[Week 38 - Board Vision]] — active next-level vision (Worlds & Scenes, Narrator, media studio, Farscape pilot, rebrand).
- [[GOAL]] — current north-star pointer.
- [[Agenti Chatroom long term]] — original vision doc.
- [[LAN notes]] — hardware/services this project depends on (Spark, MSI laptop).

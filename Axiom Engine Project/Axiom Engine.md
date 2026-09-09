# Axiom Engine — Current State

> Last updated: 2026-09-09 by Herm. Source of truth for day-to-day dev
> detail is the repo itself (`~/playground` on `axiom-engine`) and
> `[[NOTES]]`; this page is the Obsidian-facing overview + status snapshot —
> same role `Agentic Chatroom.md` plays for that project.

## What it is

**Axiom Engine** is AJ's working name for the next phase of **AJ's
Operations Console** ("Playground") — a personal, LAN-first ops dashboard
and automation/agent platform. Core mechanic: a Jobs & Automation Engine
(25+ skills, pipeline orchestration, AI job builder, self-healing) plus a
**Ralph Loop coding agent** — an in-house autonomous coding-agent
orchestrator (objective → criteria → tasks → verify → promote → ship) built
from scratch inside the app itself, not a third-party tool. The project
stalled a couple of months ago while hardening the Ralph Loop; AJ wants to
re-familiarize, decide what's worth keeping, and restart active development
using what he's since learned about agentic coding/automation.

## Where it lives

- Path: `~/playground` on host `axiom-engine` (SSH alias; actual box is an
  Asus Zenbook, hostname `openclaw-sandbox`, LAN IP `192.168.0.26`, user
  `aj`). SSH key `~/.ssh/axiom-engine` set up 2026-09-09 from the Hermes
  laptop — `ssh axiom-engine` connects non-interactively.
- Git: **local repo with a real GitHub remote** —
  `git@github.com:andersjensen10/AJs-Ubuntu-Server.git`, branch `main`.
  As of 2026-09-09 the local branch is **61 commits ahead of
  `origin/main`** (nothing has been pushed since the stall) and the working
  tree is clean.
- Stack: Node.js 22 (nvm) + Express backend + Svelte frontend + SQLite
  (`better-sqlite3`). No build step for the vanilla-JS legacy pieces;
  Svelte panels live under `svelte/src/lib/panels/`.

## Live ports / environment (verified 2026-09-09)

| Port / endpoint | What |
|---|---|
| `8081` (`0.0.0.0`) | Main Express server (`node/server.js`), served via `aj-playground.service` |

Daily brief timer: `aj-playground-frontpage.timer`, 00:01 Europe/Copenhagen.

## Backing infra

- Runs as a **systemd user service** (`aj-playground.service`) on
  `axiom-engine` — has been up continuously since 2026-07-10 (2 months+
  uptime as of this writing), main PID 1024, ~640MB RSS. It survived the
  project "stalling" — the deployed app is healthy and actively executing
  scheduled Flows (jobs) hourly per the service log.
- Depends on: local Ollama/LAN LLM servers (`LOCAL_LLM_HOST`), OpenAI +
  Anthropic API keys, Slack bot, Telegram bot, Brave Search API, Himalaya
  mail, Kasa smart plug, and several `SPARK_VLLM_*` endpoints pointing at
  the same Spark box other Hermes projects use — all configured in
  `.env.local` (gitignored, present on the box).
- Two smaller sibling projects live in the same home dir but are **not**
  part of Axiom Engine's active scope unless AJ says otherwise:
  `~/homeagent` (separate Node/TS project) and `~/ops-api` (small Python
  FastAPI-ish script, `main.py` + `sweep.py`).

## Status

**Deployed and running, development stalled ~2 months ago mid-hardening of
the Ralph Loop coding agent.** Not broken — just paused.

- The main dashboard (jobs, analytics, chat, notes, links, gallery, system
  status, Slack/Telegram bridges) is feature-complete and live per
  `README.md` and `PROJECT_STATUS.md`.
- The **Ralph Loop** (in-house autonomous coding agent, the thing that
  actually stalled the project) reached **v0.2 "supervised beta"**: golden
  E2E fixture, structured per-criterion acceptance evidence, Verification
  node with command allowlisting, Project Profiles (scope/protected
  paths/verification presets), durable SQLite task ledger with
  dependencies/retries/resume, Git branch/diff/approve/commit/rollback
  handoff, idempotent effect receipts (jobs/media/storage/Git/Kanban),
  workspace locking for concurrent runs, approval gates for protected
  paths/deps/external effects, sandboxed verification execution. Full P0
  and almost all P1 items are checked off in `TODO.md` /
  `docs/ralph-loop-delivery-baseline-2026-06-10.md`.
- **What's explicitly still open** (from that baseline doc's Completion
  Plan, P1/P2 tail):
  - Optional embedding retrieval for cross-concept discovery in very large
    repos (P1, not started).
  - Kernel/container-level isolation for arbitrary non-Node binaries (P2,
    not started) — Ralph today sandboxes *Node* verification commands but
    has no isolation for other tool execution.
  - Provider-backed deployment execution (P2, not started) — deployment
    *handoff* exists, actual deploy automation doesn't.
  - Production dashboards for cost/retries/failure causes/acceptance
    quality (P2, not started).
  - The doc's own **Release Boundary** is explicit: Ralph v0.2 is fit for
    *supervised* repo changes, not unattended production shipping,
    unattended merges, or arbitrary command execution.
- Last recorded `ralph-loops/latest-next-step.md` run output is a trivial
  "Hello World" HTML page — i.e. the most recent loop run before the stall
  was a smoke test, not real project work, which matches AJ's framing of
  "stalled trying to build in a Ralph Loop."
- Other active-but-unfinished epics per `TODO.md`: Slack+mail command
  ingestion (partially done, inbound + normalized queue still open),
  multi-agent task system (planned, architecture review needed), emergent
  creative subpages (ideation only).

## Verify gate (before calling anything "done")

From `~/playground` on `axiom-engine`:
- `npm test` — quick structural checks (`scripts/dashboard-check.js`)
- `npm run e2e` / `npm run e2e:svelte` — Playwright E2E (needs
  `sudo npx playwright install-deps chromium` if missing)
- Ralph-specific: see `docs/ralph-loop-delivery-baseline-2026-06-10.md` →
  "Beta Exit Test" for the 8-point representative-run bar Ralph itself is
  held to.

*(Not yet independently verified by Herm — this is transcribed from the
repo's own docs, not a fresh test run. Run these before trusting "done" on
anything picked back up here.)*

## Known gotchas

- **61 unpushed commits.** Before any risky experimentation, either push to
  `origin/main` or branch off, so the last known-good hardened state of
  Ralph isn't only sitting on one laptop's disk.
- **No auth, LAN-only by design** — `.env.local` has real API keys
  (OpenAI, Anthropic, Slack, Telegram, Brave) and the server binds
  `0.0.0.0:8081`. Fine on trusted LAN, not fine to expose publicly as-is.
- Two other unrelated small projects (`homeagent`, `ops-api`) share the
  same home directory — don't assume everything under `~` on
  `axiom-engine` belongs to this project.
- Ralph's own docs are explicit that it is **not** safe for unattended
  production changes or arbitrary command execution yet — respect that
  boundary rather than re-discovering it the hard way.

## Feature Development pipeline

Work flows through `Feature Development/`, same shape as every project in
the portfolio: raw ideas land in `Feature Requests`, get matured into
`Backlog`, and ship into `Published features/Sprint N - Week WW` once done.

- **Active backlog:** *(not yet populated — first story is "re-familiarize
  + reconcile repo state," see `Feature Development/Backlog/Ready for
  development`)*
- **Full blueprint:** [[improvements]] (`Feature Development/Feature
  Requests`) — still a stub; the real long-term architecture lives in the
  repo's own `docs/` (30+ planning docs) and needs to be mined into this
  vault over time.
- **Next-level vision:** *(not yet set — GOAL.md still points here as
  pending)*

## Related notes

- [[NOTES]] — running session log.
- [[improvements]] — full blueprint & phasing (stub, needs work).
- [[GOAL]] — current north-star pointer (not yet set).

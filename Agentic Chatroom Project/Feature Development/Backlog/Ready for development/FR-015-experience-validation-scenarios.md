---
tags: [project/agora, type/backlog]
status: ready-for-development
origin: board-request
source: "[[WO-006-validating-the-experience-ARCHIVE]]"
criticality:
  impact: high
  urgency: high
size: L
dependencies:
  - "Worlds & Scenes data model (Week 38 Board Vision, initiative 1) — richer scenarios will target this once it ships; the harness itself does not block on it"
  - "Scene media studio (Week 38 Board Vision, initiative 3) — media-request scenarios extend the harness once media flows exist"
  - "Existing live-*-check.mjs scripts and Fastify/WS API surface (apps/server) as the integration point for the new harness"
matured: 2026-09-10
matured_by: Scrummaster
---

# Experience validation scenario harness

## Context
This story matures WO-006 (`[[WO-006-validating-the-experience-ARCHIVE]]`),
itself promoted from Section 6 of `[[Week 38 - Board Vision]]`: "Validating
the experience." The Board's own framing is explicit that this is **the
gate between "internal prototype" and "opened up for public testing,"** and
should "stand up early... not trail the other initiatives" and "not a
wrap-up step." That is the basis for setting `urgency: high` here — per the
Scrummaster's urgency-floor rule, board-originated items default to at least
medium, and this one's own source text argues for high explicitly (it gates
whether any of the other Week 38 initiatives are safe to expose to a
non-AJ user).

`impact: high` because until this exists, the Board and Senior PM have no
structured way to judge experience quality (as opposed to code correctness)
for anything shipping under the Week 38 vision — Worlds/Scenes, Narrator
intelligence, the media studio, and eventually the Farscape pilot all rely
on this instrument to produce real signal instead of guesses.

**Sequencing note (important):** the vision doc explicitly calls this out
as buildable early and "scenario-authoring-agnostic" — the harness/framework
itself does not need Worlds/Scenes or the media studio to exist first. What
it needs is at least one real scenario runnable against what exists in the
app *today* (personas, rooms, turn-taking, persona memory, existing
ComfyUI-backed media generation). Richer scenarios that specifically probe
Worlds/Scenes continuity or the new media studio are extensions layered on
once those initiatives (in-flight via sibling stories from this same
Scrummaster run) ship — this story's acceptance criteria require the
harness to be extensible to them, not that it cover them on day one.

Per the Senior QA Manager's role doc (`Feature Development/Project
Team/Senior QA Manager.md`), this deliverable is a tool *that role* runs —
QA already uses `npm run verify` plus `scripts/live-*-check.mjs` for
pass/fail regression, and separately drives a real browser for usability
judgment. This story adds a **third mode**: structured, repeatable
simulated-user scenarios that emit interaction/analytics-style metrics
(turn latency, turn-taking correctness, memory/continuity signal, media
request success and latency, conversational coherence proxies) rather than
a pass/fail verdict — explicitly distinct from bug-hunting.

## User story
As the Senior QA Manager, I want a structured, repeatable harness for
running simulated-user test scenarios against Agora and capturing
interaction/analytics-style metrics (not a pass/fail bug list), so that I
can produce a metrics writeup the Board/PM can use to judge experience
quality ahead of opening the product to real users.

## Acceptance criteria
- [ ] A new scenario harness exists in the repo (e.g.
      `scripts/live-experience-scenario-check.mjs` plus a small scenario
      definition format/module, not a single monolithic script) that runs
      against the live server (`apps/server`) the same way existing
      `live-*-check.mjs` scripts do.
- [ ] The harness runs a **structured scenario**: a scripted sequence of
      simulated-user turns against one or more personas/rooms (today's
      building block — not gated on Worlds/Scenes), driving the real
      WS/API surface, not mocks, consistent with how QA currently verifies
      shipped work.
- [ ] Output is a **metrics writeup**, not pass/fail: at minimum captures
      per-turn latency, turn-taking/mention correctness, reply
      presence/emptiness (tie into the known reply-quality bug history),
      and — where a scenario includes a media request — ComfyUI request
      success/latency. Output format is a structured file (JSON or
      markdown table) suitable for pasting into the Senior QA Manager's
      weekly Board writeup.
- [ ] At least one real scenario is authored and demonstrated end to end
      against the current app (persona + room + multi-turn conversation,
      optionally including one media request) — satisfying the Board's
      stated success metric of "runs at least one structured scenario end
      to end and produces a metrics writeup usable by the Board/PM."
- [ ] The scenario definition format is documented and explicitly designed
      to be extensible: a new scenario targeting a World/Scene or the media
      studio should be addable as a new scenario file/definition without
      rewriting the harness, once those features exist.
- [ ] Harness failure modes (infra down, Spark/ComfyUI unreachable) report
      as a clearly labeled skipped/blocked scenario in the metrics output,
      never as a false pass or silently-missing metric — matching the
      Senior QA Manager's existing mandate to never let infra flakiness
      read as "verified."
- [ ] A short usage note is added (README or in-script header) telling the
      Senior QA Manager how to run it and where output lands, so it slots
      into the existing QA cycle method (static gate + live-*-check.mjs +
      real browser session) as a fourth, metrics-producing leg rather than
      a bolt-on.

## Implementation notes
- Model the new script structurally on the existing `live-*-check.mjs`
  pattern (see `scripts/live-reply-quality-check.mjs` and
  `scripts/live-narrator-check.mjs` for the closest precedents — they
  already drive persona/room/WS flows against the real API) but change the
  exit contract: existing scripts assert and exit non-zero on failure; this
  harness should *collect metrics* and exit non-zero only on genuine
  execution failure (can't reach the server, scenario crashed), not on
  "the metric wasn't great" — quality judgment stays with the QA Manager
  reading the writeup, not a hardcoded threshold.
- Keep the scenario definition separate from the runner (e.g. a
  `scripts/scenarios/*.mjs` or `.json` directory) so future scenario
  authors (QA, or a future Narrator-aware scenario generator) don't need to
  touch the harness internals.
- Reuse the WS connect/turn helpers already proven in
  `live-reply-quality-check.mjs` (ready/user_message/message_done handling,
  quiet-timeout pattern) rather than reinventing WS plumbing.
- For the media-request leg of a scenario, reuse the connection pattern
  from `scripts/live-comfy-check.mjs` / `scripts/live-chat-image-check.mjs`.
- Since Worlds/Scenes don't exist yet, today's "scenario" boundary is a
  room + persona set; when Worlds/Scenes ship, the harness should gain a
  scenario type that spans multiple scenes/sessions to test the
  cross-session continuity the Board vision calls out — flag that as
  follow-up scope, don't block this story on it.

## Non-goals
- The Farscape World pilot content (test scenarios authored around
  Farscape characters/wiki/voices) — explicitly excluded per WO-006's own
  Non-goals; stays a separate, not-yet-promoted item pending its own
  research pass and QA department scoping.
- Building or waiting on Worlds/Scenes, Narrator intelligence, or the media
  studio itself — this story only needs to produce a harness usable against
  what exists today, extensible later.
- Automated pass/fail quality thresholds or CI gating on scenario metrics —
  this is an instrument for human (QA Manager) judgment, not a new
  regression gate.
- A dashboard or persisted metrics history/store — the deliverable is a
  runnable script producing a writeup-ready output file per run, not a
  metrics database.

## Definition of done
- [ ] `scripts/live-experience-scenario-check.mjs` (or equivalently named
      harness entry point) exists, is runnable via `node
      scripts/live-experience-scenario-check.mjs`, and is referenced from
      the project's script conventions alongside the other `live-*-check.mjs`
      tools.
- [ ] At least one scenario definition runs end to end against the live
      server and produces a metrics writeup file (JSON or markdown) with
      the fields listed in the acceptance criteria.
- [ ] `npm run verify` (typecheck + check + vitest + build) still passes
      clean — the harness is additive and does not regress the baseline
      gate.
- [ ] Usage note committed (script header or README section) so the Senior
      QA Manager can pick this up without further onboarding.
- [ ] Story acceptance criteria all checked off against a real run, not a
      dry read of the script.

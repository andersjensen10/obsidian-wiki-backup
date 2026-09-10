---
tags: [project/agora, status/archived, type/backlog]
---

# Next Level Agentic Chatroom Project — Sprint Plan [ARCHIVE]

> **ARCHIVED & MATURED:** 2026-09-08 by Scrummaster.  
> This source sprint plan has been processed into discrete, SMART user stories under `Backlog/Ready for development`:
> - `[[FR-001-eval-thinking-off-quality]]` — Evaluate quality impact of `AGORA_THINKING=false`
> - `[[FR-002-spark-llamacpp-parallel-slots]]` — Raise llama.cpp `--parallel` on Spark
> - `[[FR-003-in-app-media-lightbox]]` — In-App Media Studio Lightbox
> - `[[FR-004-media-composer-modal]]` — Media Composer Modal
> - `[[FR-005-tabbed-persona-studio]]` — Tabbed Persona Studio Redesign
> - `[[BUG-013-fish-speech-voice-cloning-500]]` — Fish Speech Voice Cloning 500 error
> - `[[FR-006-sentence-streaming-tts]]` — Sentence-streaming TTS pipeline
> - `[[FR-007-tool-execution-cards]]` — Tool execution cards in transcript
> - `[[FR-008-slash-command-palette]]` — Slash command palette (`/`, `Cmd+K`)
>
> **Parked Items (kept on hold):**
> - *Phase 4 (mem0 + FalkorDB persistent memory)* — Parked: blocked since 2026-09-01 (neither docker nor podman installed on laptop).
> - *Full-duplex voice mode & GPU telemetry drawer* — Parked: deferred to Phase D (long-term).

---

> Original text preserved below:

# Next Level Agentic Chatroom Project — Sprint Plan

> Last updated: 2026-09-07 by Claude (with AJ). Concrete near-term backlog
> for Agora, building on [[Agentic Chatroom]] (current state), [[improvements]]
> (full blueprint), and [[NOTES]] (session log). This note tracks the *next*
> chunk of work, not the long-term vision — that's [[improvements]].
>
> **Pipeline home:** filed in `Feature Development/Backlog`. Raw feature
> ideas live in `Feature Development/Feature Requests` ([[improvements]]);
> once items here actually ship, write them up under
> `Feature Development/Published features/Sprint N - Week WW`.

## Sprint goal

Ship the real Phase B UX features that the bug-fix pass didn't actually
cover (media lightbox, media composer, tabbed persona editor), close out the
two dangling open questions (thinking-off quality eval, LLM concurrency), and
clear the path to unblock persistent memory.

*(Scoped to **Sprint 1 — Week 37 (2026-09-07 → 2026-09-13)**, matching the
vault's `Published features/Sprint N - Week WW` convention. Solo build, so
there's no team-capacity table here — just a prioritized list, kept to a
one-week horizon so it doesn't drift too far from what's realistic.)*

## Context: what's actually left

All 12 tracked bugs are resolved (see [[Agentic Chatroom]]), but several of
the Phase A/B items in [[improvements]] were only *bug-fixed*, not built as
standalone UX — e.g. BUG-11 fixed the ComfyUI `/interrupt` call but not the
Lightbox UI around it; BUG-08 wasn't a full tabbed persona editor. This
backlog targets that real feature work, plus two open items and one hard
infra blocker that's been sitting there since Sept 1.

## Backlog

| Priority | Item | Why now | Depends on | Matured Story |
|---|---|---|---|---|
| P0 | Evaluate quality impact of `AGORA_THINKING=false` | Shipped in `366e7b1` with speed proven (~5x fewer tokens) but quality never checked — silent regression risk on every persona reply | Spark up, real personas | `[[FR-001-eval-thinking-off-quality]]` |
| P0 | Raise llama.cpp `--parallel` on the Spark for concurrent slots | Single generation slot serializes every multi-persona scene; blocks realistic testing of turn-taking/banter | SSH or console access to Spark | `[[FR-002-spark-llamacpp-parallel-slots]]` |
| P0 | Get SSH authorized on the Spark (add laptop pubkey to `authorized_keys`) | Blocks all log-level diagnosis (journalctl, nvidia-smi) and is a prerequisite for the `--parallel` change above | AJ, physical/console access | `[[FR-002-spark-llamacpp-parallel-slots]]` |
| P1 | In-App Media Studio Lightbox (metadata HUD, variations, upscale, animate, set-as-portrait) | [[improvements]] §3.1 UX was never built — only the underlying interrupt/cancel bug was fixed | ComfyUI up | `[[FR-003-in-app-media-lightbox]]` |
| P1 | Media Composer modal (workflow preset selector, aspect ratio picker, reference image drop) | Remaining native-prompt-adjacent UX debt; makes media gen usable instead of ad hoc | None | `[[FR-004-media-composer-modal]]` |
| P1 | Tabbed Persona Studio redesign (Identity / Voice / Appearance / Traits) | Personas page is still one long scroll; blocks comfortable per-persona iteration | None | `[[FR-005-tabbed-persona-studio]]` |
| P1 | Fish Speech voice cloning 500 error (open bug) | Per-persona cloned voices are a core promise of the project and currently broken | Spark's Fish Speech service | `[[BUG-013-fish-speech-voice-cloning-500]]` |
| P2 (stretch) | Sentence-streaming TTS pipeline | Big felt-latency win (~400ms vs. current end-of-paragraph wait) but touches both server streaming and TTS dispatch | Stable LLM streaming | `[[FR-006-sentence-streaming-tts]]` |
| P2 (stretch) | Tool execution cards in transcript | Skills harness already exists server-side; this is UI-only | None | `[[FR-007-tool-execution-cards]]` |
| P2 (stretch) | Slash command palette (`/`, `Cmd+K`) | Nice ergonomics, zero dependencies — easy to drop if time runs out | None | `[[FR-008-slash-command-palette]]` |

## Parked (explicitly out of this sprint)

- **Phase 4 — mem0 + FalkorDB persistent memory**: blocked since 2026-09-01 —
  neither docker nor podman is installed on the laptop. Needs a decision
  (install one, or find a non-container path) before it can even start. Seam
  is ready at `apps/server/src/chat/memory.ts`.
- **Full-duplex voice mode (VAD + Whisper)** and **GPU telemetry drawer**:
  Phase D, long-term — not realistic on top of the above in one sprint.

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Spark "flaps" — ping unreliable even when HTTP is fine, and it's now running on wifi in the living room (moved 2026-09-07, ethernet pending) | False "server down" readings while testing; wifi move likely makes flapping worse until it's on ethernet | Always health-check via HTTP (`/v1/models` or a real completion), never ICMP — per [[LAN notes]]. Treat the ethernet cable/switch as a real (if unscheduled) dependency for this sprint's reliability |
| ComfyUI queue shared with AJ's own jobs | Lightbox/Composer testing could stall behind unrelated generations | Check `GET /queue` before timing anything in tests |
| Reasoning-model empty replies under tight token budgets | Could masquerade as a new bug during the thinking-off eval when it's really budget exhaustion | Known gotcha — raise `AGORA_REASONING_RETRY_TOKENS`, don't touch the parser |
| Single generation slot until `--parallel` lands | Multi-persona scenes serialize, slowing down everything else this sprint | Sequence SSH + `--parallel` first (both P0) so later work isn't bottlenecked |

## Definition of done

- [ ] `npm run verify` clean (typecheck + svelte-check 0 errors/warnings + vitest ~229 tests + build)
- [ ] Live E2E (`scripts/live-bugfix-check.mjs`) passes against the live Spark
- [ ] New UI features (Lightbox, Composer, tabbed editor) browser-verified, not just unit-tested
- [ ] Thinking-off eval has a written verdict (keep default false / revert / make per-persona) — not left open
- [ ] Wiki updated: [[Agentic Chatroom]] status snapshot reflects what shipped, and shipped items get a writeup under `Published features/Sprint 1 - Week 37`

## Key dates

| Date | Event |
|---|---|
| 2026-09-07 | Sprint 1 (Week 37) start |
| 2026-09-10 | Mid-sprint check-in — reassess P1 scope vs. P0 completion |
| 2026-09-13 | Sprint 1 end — file what shipped under `Published features/Sprint 1 - Week 37` |

## Related notes

- [[Agentic Chatroom]] — current state snapshot
- [[improvements]] — full architecture/UX blueprint (`Feature Development/Feature Requests`) this backlog draws from
- [[NOTES]] — session log (infra facts, gotchas)
- [[LAN notes]] — Spark/hardware this sprint depends on

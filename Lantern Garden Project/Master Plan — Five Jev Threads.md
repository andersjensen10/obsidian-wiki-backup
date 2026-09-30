---
tags: [type/plan, lantern-garden, jev, decide, autoresearch, touchdesigner, home-lan]
created: 2026-09-30
owner: Winbot
status: proposed — awaiting Herm and Sparkbot ACK on mandates
---

# Master Plan: five Jev threads, woven into daily life

AJ approved all five ideas (2026-09-30) and singled out #5 (evolution loop). Extends [[Lantern Garden Project/Build and Operations Plan — Decision Layer and Autoresearch]] and [[Lantern Garden Project/Vision — Decision Layer and Autoresearch Engine]]. This note is the durable record; Townhall carries handoffs; the vault is updated at every phase gate.

## 0. Hard rules (inherited, not renegotiable)
- **Ground truth = AJ only.** Records carry `decisionSource=AJ` + `accept|reject|defer`, append-only, keyed by `missionId` (Herm's boundary, Townhall `c0efb680`). Agent recommendations and Attention resolutions are never labels.
- **Shadow before live.** No model output changes a dashboard, light, service, credential, Spark queue or Attention item until its thread's gate passes and the owner ships it.
- **Frozen evaluator + hashes** for every "better" claim. Cost/token caps in each contract.
- **Spark admission** (Sparkbot): Qwen/ComfyUI work only when llama slots idle and ComfyUI queue empty; idle window 02:15-02:45.
- **Jev key** stays in `C:\Users\ander\.typesafe\env`; logs store state hashes, not text. Anything private goes to Qwen only.
- **Performance safety** (TD): live show stability beats any experiment; changes small, reversible, verified by errors + fps + visible output.

## 1. The five threads

| # | Thread | Outcome | Phase-1 deliverable |
|---|---|---|---|
| T2 | **Label flywheel** (foundation) | Every AJ accept/reject/defer becomes a label | Verdict control + append-only record |
| T1 | **Reflex layer** | Jev makes tiny frequent calls (route, urgency, nudge) via `decide()` | Shadow reflex on Attention + Townhall routing |
| T3 | **Disagreement signal** | Jev vs Qwen split = "ask a human / slow agent" | `disagree` field in decide() ensemble, logged |
| T5 | **Evolution loop** (AJ's favourite) | Autoresearch proposes, frozen evaluator judges, keep/revert; extends to creative work | Fleet-debounce night runs, then Dreams parameter loop |
| T4 | **Live-reactive Dreams** | Jev classifies MIDI/camera/audio events into moods/scene cues at show latency | Event-to-mood classifier in shadow (logs only), then TD hook |

Dependency: T2 -> (T1, T3) -> T5 creative metrics; T4 needs T2 labels to learn AJ's taste but its plumbing can start in parallel.

## 2. Mandates and ownership

| Agent | Mandate (owns, decides) | Must not |
|---|---|---|
| **Winbot** (MSI laptop) | `decide()` lib, Autoresearch runner, evaluators, nightly cron, monitor, vault upkeep, TouchDesigner work (T4), Jev budget + key, Townhall work orders, verified read-backs | Touch dashboard/fleet probe; act on model output live; claim accuracy without AJ labels |
| **Herm** (Ubuntu laptop `:5173`) | Dashboard final say; AJ review record + verdict UI (T2); raw probe export; ships/rejects promoted rules; Attention data | Fabricate labels; ship without evidence + rollback |
| **Sparkbot** (Spark `.139`) | Admission facts and idle window; Qwen `:8014` and ComfyUI `:8188` health; GPU-side evaluators; ComfyUI camera/prompt workflows for Dreams (T4/T5) | Let experiments preempt production or Herm's queue |
| **AJ** | Verdicts (the labels), taste, direction, budget top-ups, safety boundary | (only pulled in for decision, safety, stall) |

Escalation: real decision or blocker -> Slack/lights via Winbot. Everything else stays in Townhall. One post per night max from the nightly job.

## 3. Infrastructure allocation

| Resource | Assigned to | Why |
|---|---|---|
| MSI laptop CPU (`192.168.0.30`) | Runner, evaluators, nightly 02:20 cron, decide() client, Jev calls | No dependency on flaky Spark; already runs Winbot cron |
| MSI RTX 4080 (12 GB) | **Reserved for TouchDesigner live rendering first**; only after T4 stable, candidate for a local judge/classifier (unverified) | Show stability priority |
| Herm laptop `:5173` | Dashboard, Townhall, verdict UI, review record store, fleet data | Herm's ownership |
| Spark `:8014` Qwen | Second opinion (T3), private classification, only when idle | Sparkbot admission rule |
| Spark `:8188` ComfyUI | Dreams imagery, 02:15-02:45 experiments and daytime only when queue empty | Same |
| TypeSafe Jev (cloud) | Fast reflex calls (~300 ms). Budget: $10 credit; est. < $0.10/day at current volume; cap per run in contract; alert at 50% spent | Cheap enough to be a reflex |
| Raspberry Pis (4, unused) | Candidate edge nodes: MIDI/sensor-to-event bridge for T4 (send events over LAN to MSI). Verify hardware and network first | Idle capacity, low latency to gear |
| MIDI interfaces / Push / MOTU (studio) | Event sources for T4 via TD MIDI In | Already verified audio path 2026-09-28 |
| Projector (living room, driven by MSI) | Lantern Garden output; reflex/disagreement status can surface as reversible routes | AJ's standing permission |

## 4. Phased roadmap with gates

| Phase | What | Owner | Gate (verified by) |
|---|---|---|---|
| P0 | This plan, mandates ACKed | Winbot, Herm, Sparkbot | Townhall ACKs from both (Winbot) |
| P1 | **T2** verdict record schema + Morning Review Card verdict buttons | Herm (build), Winbot (schema, tests) | Append-only write/read-back with `decisionSource=AJ` (Winbot) |
| P1 | **T5a** first unattended fleet-debounce night 2026-10-01 02:20 | Winbot | report.md exists, only rule.json changed, hashes intact |
| P2 | **T1/T3** shadow reflex + Jev/Qwen disagreement logging on new missions | Winbot (decide), Sparkbot (admission) | >= 30 AJ labels, false-negative guard holds |
| P2 | **T4a** event-to-mood classifier in shadow: MIDI/audio events logged with Jev mood + latency, no TD output change | Winbot | p95 latency < 500 ms, zero TD warnings, fps unchanged |
| P3 | **T4b** TD hook: mood -> one bounded parameter set (e.g. palette/feedback amount), instant off-switch, prior state retained | Winbot, AJ approves look | AJ verdict in a live session |
| P3 | **T5b** Dreams creative loop: proposer varies TD/ComfyUI parameters, judge = calibrated model scored against AJ verdicts, run in Sparkbot idle window | Winbot + Sparkbot | Judge correlates with AJ labels (threshold set in contract before run) |
| P4 | Reflex promotion to operational routing (only what the labelled set justifies) | Herm ships | AJ label evaluation frozen and passed |
| P5 | Meta-loop on `program.md`; camera input | Winbot | 3 stable series; camera privacy checks per VJ Lab README |

## 5. Risks and handling
- **Label scarcity** (AJ is the bottleneck): make verdict one tap, batch in Morning Review, show running count; never block other work.
- **Creative judge drift**: judge is never trusted until it correlates with AJ verdicts; AJ can veto any kept variation.
- **Cloud dependency in live show**: T4 falls back to deterministic stub mapping on timeout (>500 ms); the show never waits on Jev.
- **Cost creep**: per-run caps, alert at 50%.
- **Spark flapping**: fail closed, never queue.
- **Camera privacy**: no camera frames leave the LAN or go to Jev; local only. Requires explicit AJ enablement.

## 6. Open questions for AJ (non-blocking)
1. Camera: which device, and is it OK for it to run only locally?
2. Should the Pis be used as MIDI/event bridges (I would verify what they are first)?
3. Daily Jev budget ceiling (proposal: $0.25/day hard cap).

## AJ answers (2026-09-30)
1. Camera: USB to the MSI laptop, still being set up; AJ will notify Winbot when ready. Camera work (P5) stays blocked until then; local-only rule stands.
2. Pis/NUC/MIDI/audio: full inventory first, planned with the agents: [[Creative Systems/Inventory Program — Full Breakdown Plan]]. The Pi-as-bridge idea in T4 waits for that result.
3. Budget: $0.25/day is the starting cap; AJ is open to raising it for meaningful work. Raise only via a Townhall note with evidence of value.

## Execution log
- 2026-09-30 (AJ: "execute what you can now"; inventory deferred by AJ, waits until he wants it). Commits on MSI `Desktop\Hermes\Autoresearch`, 37 offline tests pass (10 decide, 9 ensemble, 8 mood, 10 review):
  - `9a7e369` **T2 review record** (`review/review_record.py`): append-only JSONL, SHA-256 hash chain, accepts only `decisionSource=="AJ"` + `accept|reject|defer` + `missionId` + `decidedAt`; rejects any card-output fields; detects edits, deletions, reorders; refuses to append to a broken chain; read-back after write; `defer` not counted as usable for accuracy. Store: `review/store/aj_review.jsonl`, **empty, 0 labels** (fixtures are synthetic, temp-file only). Hand-off to Herm for the verdict UI: he calls `append()` only with AJ's own decision.
  - `9a7e369` **T3 ensemble** (`decide/ensemble.py`): Jev + Qwen per question -> `quiet` / `escalate` / `fast_only`. Slow backend unavailable is never counted as agreement. Thresholds (score tolerance 0.5, confidence 0.6) are unvalidated defaults; it is a routing hint, not an accuracy claim.
  - `9a7e369` **Jev budget guard**: `BudgetedBackend` fails closed at the daily cap ($0.25, AJ's starting cap), counts spend from the call log, alerts at 50%. Spent today: $0.0066.
  - `6929920`/`bb5e7a1` **T4a mood shadow** (`decide/mood.py`): six-mood vocabulary, deterministic fallback mapping, Jev classification with 500 ms deadline, logs state hash + latency only. Never writes to TouchDesigner. Live smoke test on a synthetic window: Jev 289-356 ms, 3/3 inside deadline; Jev said `driving` where the fallback said `euphoric`, so the mapping and Jev disagree on that window: no ground truth, so no claim about which is right.
- **Not done, and why:** TD hook (needs AJ's approval of the look and shadow evidence from real MIDI/audio), inventory (deferred by AJ), camera (hardware not ready), creative loop (needs AJ verdicts). Attention reflex is still shadow-only: no labels yet, so no promotion.
- **Same day, later (AJ: "don't delay what we can do now"):**
  - `2eee2fe` **T1 Attention shadow reflex** (`decide/attention_shadow.py`): read-only; Jev judges each NEW open Attention item once (kind: routine_noise / needs_human / real_incident / info, plus urgency), redacted input, logged with the Attention id as `missionId`. Never resolves or edits anything. Wired into the 10-minute monitor (`townhall_digest.py`, silent unless it errors). First run: 5 items judged, 4 tool errors -> routine_noise (conf 0.51-0.90), 1 Herm info item -> info. Unlabelled: not accuracy. Re-run judged 0 new (dedupe works).
  - **Stalled-job alert** added to `townhall_digest.py` (backup `.bak-20260930`): prints `STALLED JOB` if the nightly autoresearch job's last run is >36 h old or failed. Closes the open item in the Build and Operations Plan.
  - **Debounce job fired now** instead of waiting for 02:20; **result verified**: candidate `{"min_down_s": 120}` scores 61 vs baseline 2129, 0 missed outages, hashes intact, only `rule.json` changed. Evidence bundle: [[Lantern Garden Project/Fleet-Debounce Evidence Bundle — 2026-09-30]], posted to Herm as a shadow work order. The harness question (does an unattended cron session run the loop reliably?) is answered yes for one run; 02:20 tonight is the repeat.
- **Next:** first unattended debounce night 2026-10-01 02:20; verify harness next morning.

## Log
- 2026-09-30: plan drafted. Posted to Townhall `7005d8c0-6c6d-4ac1-a686-9e47a7781d93` (home-lan); waiting for Herm and Sparkbot ACKs (P0 gate).

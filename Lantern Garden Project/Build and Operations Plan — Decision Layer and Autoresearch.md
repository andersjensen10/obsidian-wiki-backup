---
tags: [type/plan, lantern-garden, autoresearch, jev, operations, home-lan]
created: 2026-09-30
owner: Winbot
status: approved-for-shadow-build
---

# Build and Operations Plan: who builds, who hosts, what depends on what

Companion to [[Lantern Garden Project/Vision — Decision Layer and Autoresearch Engine]]. Team input: Herm (Townhall `98a5fcf7-a8f9-43d8-91bd-a75e9fff2ef6`) and Sparkbot (`9d73f274-9286-40c8-ada0-6b7cccdec998`). Goal: run unattended, tell AJ only what needs him.

## 1. Pilot 1 changed, and why

Proposed Attention triage; data says it has no usable ground truth today. Live Attention API (2,371 cards, read 2026-09-30): 2,105 fleet, 258 `hermes:tool`, 9 `needs-input`, 1 info, 1 critical. No card records who resolved it or whether it was routine. Labels I could derive would be my own past resolutions, which is circular, and Herm required human-reviewed labels. So triage moves to Phase 1, after an AJ review record exists.

**New Pilot 1: fleet-debounce.** Fleet "service down" cards are 89% of the queue. Objective data, no taste needed: replay 2,105 historic cards through a debounce rule (`min_down_s`, `cooldown_s`, per-service overrides) and minimise cards emitted, subject to zero missed real outages and detection delay <= 120 s.
- Evidence measured: 90.5% of fleet cards self-resolved within 5 s, 97.2% within 60 s, 99.8% within 15 min; only 4 lasted over 15 min. Median 1.7 s.
- Baseline score 2,129 (2,105 + 24 seeded synthetic real outages). Evaluator verified: deterministic across 3 runs; a slow rule fails the delay guard, a heavy cooldown fails the missed-outage guard, and even a plausible 30 s / 300 s rule misses 1 real outage, so the guards are not decorative.
- Artifacts: `C:\Users\ander\Desktop\Hermes\Autoresearch\experiments\fleet-debounce\` (git commit `4399321`, snapshot sha256 `24901f0c65c1…`): `contract.md`, `program.md`, `evaluator.py`, `snapshot.json`, `rule.json`, `results.tsv`.
- **Known weaknesses (stated, not hidden):** 1,522 of 2,105 cards came in one incident on 2026-09-22 (ComfyUI flapping), so dev is dominated by one storm and the holdout (after 09-23) has only 153 cards. Card intervals approximate outages. Only ~24 historic real outages; synthetic ones fill the guard. A win here is a proposal, not proof. Fix: raw probe logs from the fleet watchdog (ask to Herm below).
- The real leverage is upstream: 2,105 warnings mean the fleet probe has no debounce. The loop's output is a concrete, tested rule that Herm can ship, which removes most Attention noise for good.

## 2. Roles: who builds, hosts, and owns

| Component | Builder | Host / runs on | Owner of final say | Depends on |
|---|---|---|---|---|
| Experiment Contract template, runner, `results.tsv` schema | Winbot | MSI Windows laptop (this host, `192.168.0.30`), folder `Desktop\Hermes\Autoresearch` (git) | Winbot | Hermes cron on Windows |
| Frozen evaluators (deterministic, hashed) | Winbot, template from Sparkbot's sealed harness | MSI laptop, CPU | Winbot builds; Sparkbot reviews hash/verify conventions | Data snapshots |
| Nightly proposer (the "researcher" agent) | Hermes cron agent on MSI | MSI laptop; LLM = configured Hermes provider (cloud model), not Spark | Winbot | Cloud LLM key, token cap |
| Attention/fleet data source, dashboard, promotion of a kept rule | Herm | Hermes Ubuntu laptop `192.168.0.148:5173` | **Herm** (dashboard final say) | Laptop up |
| AJ review record (accept / reject / defer per mission) | Herm | Same, append-only, keyed by `missionId` | Herm | Morning Review Card `8ee9ac0` |
| Spark admission facts, GPU-side evaluators, idle-window trials | Sparkbot | Spark `192.168.0.139` | Sparkbot | Spark up (wifi, flaps) |
| `decide()` library: Qwen backend, then Jev backend | Winbot | MSI (client); Qwen at Spark `:8014`; Jev cloud | Winbot | Spark or TypeSafe key |
| Townhall monitor + Attention hygiene | Winbot | Existing cron `f3bfcfadcc1e` (10 min, Slack delivery) | Winbot | Townhall at `:5173` |
| Nightly experiment job | Winbot | New cron on MSI, 02:20 CEST, CPU only | Winbot | above |
| Taste, direction, Jev key signup | AJ | n/a | AJ | none |

Design choice: the runner lives on the MSI laptop, not the Spark or Herm's laptop. It is the only host that has no dependency on the flaky Spark, does not compete with the dashboard host, and already runs Winbot's cron. It needs outbound HTTP only (Windows firewall blocks inbound, which does not matter). Its 12 GB RTX 4080 is currently unassigned and could later host a local judge model; not verified for this use, not part of the plan.

## 3. Dependency map and single points of failure

```
AJ verdicts ─> Herm review record ─┐
Fleet/Attention API (Herm laptop :5173) ─> snapshot ─> Frozen evaluator ─> results.tsv ─> report.md ─> Townhall work order ─> Herm ships rule
Townhall (:5173)  <── Winbot monitor (10 min) ──> Slack (AJ only if a decision/blocker)
Spark (:8014 Qwen, :8188 Comfy) ── only for Phase 1+ decide()/judge; admission via Sparkbot rules
TypeSafe Jev (cloud) ── optional, Phase 1+, shadow only
```
| Failure | Effect | Handling (automatic) |
|---|---|---|
| Herm laptop or dashboard down (`:5173`) | No fresh data, no Townhall | Evaluate on last committed snapshot; skip Townhall post; retry next tick; if down >2 nights, one Slack message |
| Spark down/busy | Phase 1+ decisions unavailable | Pilot 1 needs no Spark. Later: fail closed, use deterministic stub, never queue work |
| Cloud LLM/Jev outage or rate limit | Proposer cannot run | Job ends with "no run" row in results; no retries storm; backoff via cron cadence |
| Runaway cost | Token/API spend | Hard cap per run (evaluations and tokens) in the contract; cap hit = stop and report |
| Evaluator or snapshot altered | Fake wins | Hash checked every run; mismatch = abort, Slack alert |
| Agent edits outside `rule.json` | Scope breach | `git diff --name-only` must equal `rule.json` after each experiment, else revert and log `crash` |
| Overfit (dev improves, holdout worsens) | Bad rule | Keep rule requires no regression on both splits |
| Duplicate/conflicting writers | Noisy Townhall | One post per night max, as reply in the existing thread; monitor dedupes |
| Winbot session/cron dead | Silent stall | Planned, not yet built: extend the existing 10-minute monitor to flag a nightly job last-run older than 36 h to Slack. Until then, Herm's day-7 review is the backstop |

## 4. Autonomy contract: what runs without AJ

- **Runs by itself:** nightly experiments (<= 40 evaluations first week, then 200), report writing, vault note update, one Townhall reply, Attention hygiene, monitor ticks.
- **Never by itself:** changing any live dashboard, fleet probe, service, credential, Spark queue, or the living-room plug; auto-resolving/suppressing Attention because of a model recommendation; spending beyond the cap.
- **Promotion path:** kept rule -> `report.md` -> Townhall work order to Herm with evidence + rollback -> Herm decides and deploys -> Winbot verifies with a read-back the next morning. AJ is only pulled in for: a real decision, a safety boundary, or a stall.
- **AJ's only standing action:** join the TypeSafe waitlist (console.typesafe.ai). Everything else proceeds.

## 5. Phases and gates (each ends with a Townhall checkpoint and this note updated)

| Phase | Deliverable | Gate to advance |
|---|---|---|
| 0 | fleet-debounce contract + frozen evaluator + baseline | **Done**, verified (commit `4399321`); nightly harness `397bb52` after the invalid manual run |
| 0b | First real unattended night 2026-10-01 02:20 (**pending**) | `report.md` exists, only `rule.json` changed, hashes intact |
| 1 | Herm ships/rejects the debounce rule; raw probe log export; AJ review record | Herm read-back on dashboard |
| 2 | `decide()` library **done** (`c38c48b`, Jev + Qwen + Stub, 10 tests). Attention triage pilot on human-labelled data (shadow-only, false-negative guard) **not started** | >= 30 human-labelled cards |
| 3 | Jev vs Qwen metadata-agreement/noise study **done** (227 posts; author-selected `projectId`/`category`, not AJ ground truth). It cannot establish accuracy, calibration, or promotion; next question-wording experiment waits for explicit AJ labels. | Explicit `decisionSource=AJ` + `accept|reject|defer` records keyed by `missionId` |
| 4 | Creative metrics (Dreams parameters, ComfyUI prompts) in Sparkbot idle window 02:15-02:45 | Calibrated judge correlates with AJ verdicts |
| 5 | Meta-loop on `program.md` | 3 stable series |

## 6. Open items and asks

- **Herm:** (1) accept the fleet-debounce work order as owner of the fleet probe; (2) export raw probe results (timestamp, service, up/down) to a file or endpoint so the evaluator can stop using card intervals; (3) build the append-only AJ review record.
- **Sparkbot:** nothing blocking. Later: review evaluator hash conventions; keep the 02:15-02:45 idle window available for Phase 4.
- **Ground-truth correction (Herm, 2026-09-30, Townhall `c0efb680`):** Herm's review record may store AJ-authored decisions but cannot create human labels. Treat the comparison set as unlabelled until each record has `decisionSource=AJ` and `accept|reject|defer`; do not infer labels from Attention resolution or agent recommendations. Keep review records outside generated card output and link evidence by `missionId`. Calibration/accuracy claims remain unmeasured until this exists.
- **Done since:** Herm answered and acknowledged the work order (his conditions are the promotion gate); AJ set up and funded the Jev key; `decide()` built; Jev vs Qwen compared.
- **Still open:** stalled-job alert in the monitor; Herm's raw probe export and append-only AJ review record; human labels for Attention triage.
- **Unverified:** whether the Hermes cron agent on Windows can run a 40-evaluation loop reliably in one session (first night tests this); MSI GPU as judge host.

## Master plan (2026-09-30)
AJ approved five Jev threads (label flywheel, reflex layer, disagreement signal, evolution loop incl. creative, live-reactive Dreams). Mandates, infrastructure and gates: [[Lantern Garden Project/Master Plan — Five Jev Threads]]. Townhall `7005d8c0-6c6d-4ac1-a686-9e47a7781d93`.

## Jev access (verified 2026-09-30)
- AJ created a TypeSafe account (open signup, no waitlist) and bought $10 credit. Key stored only in `C:\Users\ander\.typesafe\env` (var `TYPESAFE_API_KEY`, ACL restricted to AJ's Windows user); never in chat, Townhall or the vault.
- First test call to `https://api.typesafe.ai/v1/systemone` (model `jev-1.13.0`, no private data): HTTP 200, 433 ms end to end from the MSI laptop, Choice/Noul/Score answers correct and typed. Usage reported: 403 input tokens (about $0.000017 at $0.042/M), 70 output tokens (free).

## Night log (newest first)
- 2026-09-30 fleet-debounce: **2129 → 61**; dev 1976→28, holdout 153→33, guards OK. 14 experiments: 9 kept, 5 discarded, 0 crashed. Report: `experiments/fleet-debounce/report.md`; shadow-only, not deployed.
- 2026-09-30 11:45 Jev vs Qwen metadata-agreement/noise study (227 Townhall posts, sealed results in git `f3a5651`): observed author-metadata agreement was Jev 85.0% vs Qwen 75.8% for project routing; this is not AJ decision accuracy or calibration. Category was 64.8% vs 59.9%; both failed the blocked/needs-human metadata test. Explicit `decisionSource=AJ` + `accept|reject|defer` records keyed by `missionId` are required before accuracy claims or promotion. Details: [[Research/Autonomy Lab/2026-09-30 — Jev vs Qwen First Labelled Comparison]]. Townhall `4752b23a-fb8e-4fc6-8686-eaf5d9219bbf`.
- 2026-09-30 11:35 `decide()` built (commit `c38c48b`, `Autoresearch/decide/`): one interface, three backends (Jev cloud, Qwen on the Spark, deterministic Stub). 10 offline tests pass. Live smoke test on the same made-up ticket: Jev 441 ms, $0.0000169; Qwen 2030 ms, $0. Both routed to billing; urgency 1.06 (Jev) vs 1.5 (Qwen). Behaviours verified by test: Qwen refuses to run unless the Spark is idle (llama slots + ComfyUI queue, Sparkbot's rule) and makes no call otherwise; keys never appear in logs or errors; logs store a state hash, not the text; backend failures return `ok=False` instead of raising. Caveat: Qwen's confidence is self-reported and uncalibrated, Jev's is native; one example is a smoke test, not a comparison. Next: labelled comparison set.
- 2026-09-30 10:38 manual test run: **result invalid, discarded.** The job's model logged every `min_down_s` / `cooldown_s` proposal as `inf` (guard violation) although re-running the frozen evaluator on the same rules gives valid scores (e.g. `min_down_s=60` -> 83 cards, `120` -> 61, both with 0 missed outages). Cause: the model scored and logged by hand. Fix: `run_experiment.py` harness now does scope check, evaluation, keep/discard, git reset, logging and the 40-run cap mechanically; verified with a throwaway-branch self-test (keep, discard, delay-guard, scope violation, budget exhaustion, restore). Job prompt updated to use it. Invalid outputs kept as `results.invalid-20260930.tsv` and `report.invalid-20260930.md`. Note: a rule of `min_down_s` 60-120 already looks far better than baseline 2129 on this data, but that is one harness check, not a promotion; the storm/interval caveats above still apply. The next real run is 2026-10-01 02:20.
- 2026-09-30 10:38 (job's own auto-written entry, **INVALID**, superseded by the harness entry below): fleet-debounce: baseline 2129 → best 2129; holdout 153, unchanged. Evaluations: 40 total; kept 0, discarded 39, crashed 0. All proposals failed guards; no rule improvement or deployment. Report: `experiments/fleet-debounce/report.md`

### Night log 2026-10-02
- Baseline 2129 -> best 61 (unchanged), 5 experiments: 0 kept, 5 discarded, 0 crashed. Plateau at guard edge (121 violates). Report: Autoresearch/experiments/fleet-debounce/report.md

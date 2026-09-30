---
tags: [type/evidence, lantern-garden, autoresearch, fleet-debounce, shadow]
created: 2026-09-30
owner: Winbot
status: shadow proposal — NOT promoted; awaiting Herm review
---

# Fleet-debounce: first mechanical run, evidence bundle for Herm

Companion to [[Lantern Garden Project/Build and Operations Plan — Decision Layer and Autoresearch]]. Gate conditions are Herm's (Townhall `c819e5a6`).

## Result (verified independently by Winbot after the run)
- Candidate rule: `{"min_down_s": 120}` (the run's other parameter, `cooldown_s`, was removed at equal score).
- Baseline `{"min_down_s": 0, "cooldown_s": 0}`: score **2129** (dev 1976, holdout 153).
- Candidate: score **61** (dev 28, holdout 33), `real_outages=48`, `missed_real=0`, `max_delay_s=120`, `guards_ok=True`.
- Re-ran `python evaluator.py rule.json` myself after the job: identical output (score 61).
- Run accounting: 14 experiments (cap 40), 9 kept, 5 discarded, 0 crashed. Harness `run_experiment.py` did scoring/keep/discard mechanically, unlike the invalid 10:38 run.

## Integrity checks (all passed)
- `snapshot.json` sha256 `24901f0c65c15e15…` equals the frozen `snapshot.sha256`.
- `evaluator.py` sha256 `dfb74e98158cc55f…`; `git diff 4399321..HEAD` for the experiment folder touches only `rule.json` (plus `run_experiment.py` from harness commit `397bb52`). Evaluator, snapshot and contract unchanged.
- Artifact hashes (first 16 hex): `report.md` 7996a4bf…, `rule.json` e45820dc…, `results.tsv` 070627b1…, `contract.md` 254e3b22….
- Source commit: `1ae3782`. Job output: `AppData\Local\hermes\cron\output\17fb9f5c7d24\2026-09-30_12-16-10.md`.

## Rollback
Set the rule back to `{"min_down_s": 0, "cooldown_s": 0}` (baseline, commit `4399321`). Nothing was deployed; no dashboard, fleet probe or Attention change was made by this run.

## Caveats (stated, not hidden)
1. **`max_delay_s` = 120 equals the guard limit** (<= 120 s). The rule sits exactly on the boundary: any real outage is reported up to 2 minutes late by design. Herm/AJ should decide if 120 s is acceptable or the limit should be tighter (a 60 s rule scores 83 with 0 missed).
2. Dev is dominated by the 2026-09-22 ComfyUI storm (1,522 of 2,105 cards). Holdout is only 153 baseline cards, and 33 remain, so the win is largely "stop the storm noise".
3. Card intervals approximate outages; only ~24 historic real outages, the rest seeded synthetic (48 in the guard set).
4. The search was a coarse monotone sweep of one parameter, so "best" means best of the tried values, not an optimum. Per-service overrides did not help.
5. **Missing for promotion (Herm's list):** immutable raw-probe export (timestamps, service, up/down, collection gaps, hashes). Until it exists this is a shadow proposal only. The Ubuntu-side probe owner is Herm.

## Ask
Herm: (a) review this as a shadow work order; (b) export raw probe results so I can re-run the frozen evaluator on real probe data; (c) decide the acceptable max delay. Winbot will re-verify with a read-back after any change Herm makes.

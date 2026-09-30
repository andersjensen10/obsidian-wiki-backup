---
tags: [type/evidence, jev, qwen, autoresearch, lantern-garden, decide]
created: 2026-09-30
owner: Winbot
status: measured-first-pass
---

# Jev vs Qwen: first metadata-agreement/noise study (227 Townhall posts)

Part of [[Lantern Garden Project/Build and Operations Plan — Decision Layer and Autoresearch]]; background in [[Research/2026-09-30 — Jev System One Model for the Generative LAN]] and [[Lantern Garden Project/Vision — Decision Layer and Autoresearch Engine]]. Townhall: `4752b23a-fb8e-4fc6-8686-eaf5d9219bbf`. **Correction:** the targets are author-selected `projectId`/`category` metadata, not explicit AJ decisions. This is a metadata-agreement/noise study, not a labelled accuracy or calibration benchmark.

## Result

| metric (n=227) | Jev | Qwen (Spark) |
|---|---|---|
| project accuracy | **85.0%** | 75.8% |
| category accuracy | **64.8%** | 59.9% |
| project calibration error (ECE, lower better) | **0.092** | 0.165 |
| category calibration error | **0.255** | 0.344 |
| blocked-flag F1 (17 positives) | 0.14 | 0.19 |
| median / p95 latency | **303 / 384 ms** | 1,236 / 2,059 ms |
| cost, whole set | $0.0066 | $0 |

Significance (exact paired test on disagreements): **project, Jev better, p=0.002** (33 vs 12 items). **Category, p=0.052**: borderline, not established.

## What it means

1. **Jev earns a slot as the fast routing/classification judge.** It is clearly better at project routing, about 4x faster, and cost about $0.00003 per item. At that price, running it on everything is essentially free.
2. **Qwen stays as the fallback and second opinion, not the primary.** Where the two agree on project, accuracy is 88.9%; where they disagree, Jev is right 70% of the time and Qwen 26%. Agreement is a usable confidence signal.
3. **Qwen's self-reported confidence is useless here**: it said >=0.9 on 100% of category answers. Do not threshold on it. Jev's confidence helps on project (86.7% -> 90.1% accuracy as the bar rises to 0.95, at 58% coverage) but barely on category (65% -> 67.5%), so **Jev's calibration is only partly reliable on this task**; gate on it with measured thresholds, not the marketing claim.
4. **Category accuracy is capped by the labels, not the models.** Both models make the same dominant error: authors labelled 58-66 posts "finding" that read like announcements. That is label ambiguity. Do not read 65% as a model ceiling.
5. **The blocked flag is a failed test, for both.** Each flagged about 40% of posts (99 and 87 of 227) against a 7.5% base rate. Either the question wording is too loose or the weak label (post state) does not mean "the author is blocked". Neither model is fit for Attention triage on this evidence. Note this is a question-design problem, which is exactly what the autoresearch loop can improve (mutable file = question wording).

## Limits

227 posts, mostly agent-written; labels are author-chosen and noisy; only 17 blocked positives; hash-parity split (not chronological); Qwen prompt written once by me and not optimised; Qwen ran with thinking off while the Spark was idle. No tuning occurred, so the dev and holdout results agree (project 84.6/85.5 Jev, 70.9/80.9 Qwen; category 63.3/66.4 Jev) and neither is contaminated.

## Next

- **Experiment 2 (contract drafted, not scheduled):** optimise the question wording for project + category + blocked with the autoresearch loop. Mutable file = `questions.json`; frozen evaluator = this dataset with the dev split for search and holdout only for keep/reject confirmation; guard = holdout must not regress; cost about $0.003 per Jev evaluation. I am not starting a second cloud-spending nightly job until the first debounce night (2026-10-01 02:20) is verified.
- Get real human labels: Herm's review record, then an AJ-labelled sample of about 30 Attention cards.
- Use Jev now, with Qwen agreement as a gate, for project routing in Winbot's own tooling (monitor triage, vault filing) in shadow mode only.

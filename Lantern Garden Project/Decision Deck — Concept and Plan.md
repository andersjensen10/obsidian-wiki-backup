---
tags: [type/concept, lantern-garden, decision-deck, dashboard, ux, home-lan]
created: 2026-09-30
owner: Winbot (concept, prototype, verification) / Herm (server owner, review, deploy)
status: D1 deployed; cookie pairing awaits AJ; Attention link remains pending
---

# Decision Deck: the Lantern Garden overhaul for "what needs AJ"

AJ (2026-09-30): get back to the original purpose of the wall, **visibility of what needs my input, in an appetizing presentation**; overhaul the concept so open decisions are gathered from him through a beautiful, interactive web app. Herm owns the server on the Lenovo laptop, so the plan is a reviewable non-deploying patch (Herm's own offer, Townhall `2013e2fc`). Companions: [[Lantern Garden Project/A projector in the living room, a living dashboard and interactive playground]], [[Lantern Garden Project/Master Plan — Five Jev Threads]].

## 1. What is wrong today (measured 2026-09-30)
- Attention API holds **2,393 records; 2,104 are fleet blips, ~277 hermes tool errors, only ~9 were ever `needs-input`** and none carry options, consequences or a recommendation. It is an alarm log, not a way to answer.
- Real asks live in **Townhall posts as prose** (`state=needs-input`, `nextAction`), e.g. `288c61f1` (choose a track), `2013e2fc` (start a coding session or approve a patch). AJ has to read paragraphs to find the actual question.
- Answers are not captured anywhere machine-readable, so agents cannot act on them and no labels exist for the Jev/Qwen work.
- The wall has one page for state and one for chatter. Nothing on the wall says "here is the one thing I need from you, and here is what happens for each choice."

## 2. The concept: a deck of decisions
One first-class object, the **Decision**, replaces prose asks. The wall shows **one at a time**, like a card deck, and the rest wait behind it.

**A decision has:** a plain-language question; *why now* (one line); 2-4 options each with a **consequence** ("what happens if you pick this") and the agent that will act; a **recommended** option with a reason and evidence chips (vault note, Townhall post, verified hashes); an **if-you-do-nothing default** that is never destructive; expiry; urgency; owner agent; project accent; rollback.

**Interaction paradigm**
- **One question, huge type, one glance.** Option cards are big touch/pen/mouse targets; keys `1-4` choose, `D` defers, `←/→` browse, `Enter` confirms the highlighted one. Wacom-pen friendly, no small controls.
- **Recommended option glows**, with the reason and evidence one tap away. AJ can agree in one tap or override in one tap.
- **Defer is first-class:** "Later today / Tomorrow morning / Next week". Deferral is recorded as a decision, not silence.
- **Deck feeling:** remaining decisions peek behind the current card, count shown; answered cards animate away and the next slides up; a closing beat says exactly what each answer sets in motion.
- **Calm by default (AJ's last-resort rule):** with nothing pending the deck renders an ambient "all clear" scene, no boxes, no placeholders. It only asks when agents are stuck.
- **Provenance strip:** every answer shows the append-only record hash so AJ can trust that his word is what agents act on.
- **Beauty:** project-colored aurora background per card, generous type scale, motion under 300 ms, respects reduced-motion; fixed 1920x1200 no-scroll rule from the design tokens; also works on a phone (single column) so AJ can answer from the sofa.

## 3. Closing the loop (this is what makes it valuable, not just pretty)
```
Agent needs AJ ──> Decision Request (validated: >=2 options, consequences, recommendation, safe default, expiry)
        │                                   │
        ▼                                   ▼
   Deck on the wall / phone      Slack ping or light signal only if urgent and AJ is away
        │
        ▼ AJ taps
Append-only AJ review record  (decisionSource=AJ, decision, choice, decidedAt, hash chain)
        │                                   │
        ▼                                   ▼
 Winbot relay: Townhall reply "AJ chose X (record sha…)"     Labels for Jev/Qwen reflex (T1/T2)
        │
        ▼
 Owning agent acts, posts evidence; decision auto-closes when evidence is verified
```
The review record is the **same append-only, hash-chained log already built** (`review/review_record.py`, Herm's boundary: only `decisionSource=AJ` counts, keyed by `missionId`). Every deck answer is therefore a real label, which unlocks the accuracy work that was blocked.

## 4. Ownership (proposed, Herm to amend)
| Piece | Owner |
|---|---|
| Deck UI, decision contract, answer store, tests, this concept, prototype patch | **Winbot** (branch `winbot/decision-deck`, non-deploying) |
| Merge, deploy, live server, Attention lifecycle integration, projector scene registration | **Herm** (final say) |
| Live projector read-back and screenshot verification | **Winbot** |
| Decision Request helper for agents (`ask.py`) and quality rules | **Winbot**; Herm and Sparkbot adopt it |
| Spark facts for any decision that involves Spark | **Sparkbot** |
| Slack / light escalation policy | AJ's standing rules: lights and Slack only for genuine human-needed blockers |

## 5. Phases and gates
| Phase | Deliverable | Gate |
|---|---|---|
| D0 | This concept + prototype on a branch: `/decisions` route, `/api/decisions`, hash-chained answer store, real seeded decisions, tests, screenshots | tests pass; Python `review_record.verify()` accepts records written by the web app |
| D1 | Herm reviews, merges, deploys; registers `/decisions` as a wall scene; Attention `needs-input` items link to decisions | Herm read-back + Winbot screenshot on DISPLAY5 |
| D2 | Agents file Decision Requests via helper; Winbot relay posts AJ's answers to Townhall; auto-close on verified evidence | one full ask -> answer -> action -> close cycle, verified |
| D3 | Phone mode + Slack fallback with the same deck; light signal for `now` urgency after N minutes | AJ answers one from his phone |
| D4 | Jev/Qwen use accumulated AJ answers: rank the deck, pre-select recommendations, flag decisions AJ would likely defer (measured against his answers, shadow first) | >= 30 AJ answers; measured, not assumed |
| D5 | Generative ambience: the all-clear scene and card backdrops driven by ComfyUI/TouchDesigner, seasonal and mood aware | AJ approves the look |

## 6. Quality rules for Decision Requests (why they will stay appetizing)
1. Only when agents are stuck and Townhall coordination did not resolve it (AJ's last-resort rule).
2. The question fits one sentence; no jargon a friend could not follow.
3. 2-4 options; each states its consequence and who acts; a recommended option with a reason.
4. Safe default when unanswered; nothing destructive, nothing spends money by default.
5. Evidence by reference (vault, Townhall, hashes), never pasted walls of text.
6. One decision per card; a batch of related asks becomes a short sequence.
7. Cards that go stale close themselves and say why.

## 7. D0 prototype status (historical; superseded by the deployed pairing design below)
Branch `winbot/decision-deck` on GitHub `andersjensen10/kitchenwall`, commit `1b1fd9c` (base `master` 108a49f). Additive: 11 files, one nav entry. Local clone: `Desktop\Hermes\kitchen-dashboard-winbot`.
- **`/decisions`**: one-card-at-a-time deck. Question in huge type, 2-4 option cards with consequence and acting agent, glowing Recommended option with reason, evidence chips, "if you do nothing", Decide later (later today / tomorrow / next week), keys `1-4` `D` `Enter` `Esc` `←/→`, big touch targets, all-clear scene (renders calm, no boxes), "Locked in" confirmation beat showing the record hash, answer-log health pill, phone layout. Project-colour aurora, reduced-motion respected.
- **`GET/POST /api/decisions`**: agents file Decision Requests; strict validation (question, 2-4 options each with consequence and actor, recommended must be an option, why, ifIgnored, evidence refs, safe default), idempotent by `dedupeKey`.
- **`POST /api/decisions/:id/answer`**: AJ-only. Requires a pairing token (`DECISIONS_ANSWER_TOKEN`, header `x-decisions-token`); with none configured it **refuses** (fail closed). AJ pairs a screen once by opening `/decisions?pair=<token>`; the token is stored in the browser and stripped from the URL. Agents cannot create labels.
- **Answer log** `data/decisions/answers.jsonl` (gitignored): SHA-256 hash chain, `decisionSource=AJ`, accept/reject/defer + chosen option + `followedRecommendation`. Refuses to append to a broken chain; read-back after every write. Byte-compatible with `Autoresearch/review/review_record.py` (schema 2, commit `712d6d8`).
- **Agent helper** `scripts/ask-decision.py` + `scripts/seed-decisions.example.json` (three real pending asks: debounce delay, overnight track, dashboard handoff).
- **Verification (real, isolated preview on port 5199, throwaway Chrome profile, preview server stopped afterwards):** `svelte-check` 0 errors; 10 new unit tests pass including tamper detection, defer reopening, expiry, token fail-closed, a golden hash vector shared with Python, and **Python `review_record.verify()` accepting a chain the web app wrote**. Full suite 112/113: the one failure is the pre-existing test that needs a skill file only on Herm's host. End-to-end over CDP at 1920x1200: no scroll, no overflow, pairing, keyboard arm/lock, browse, defer flow, recommended-by-Enter, 2 answers verified in the pill. Phone width 390: works.
- Screenshots: `assets/decision-deck-armed.png`, `assets/decision-deck-locked-in.png`.
- **Not verified / open:** not tested on the real projector or Herm's live tree (his server is ahead of GitHub master; merge conflicts possible in `Nav.svelte` only); the Attention overlay still sits bottom-right on the preview (Herm's repair `winbot/attention-minimal` is separate); the design has had my review only, not AJ's; token pairing UX for the projector browser needs a decision (below).

## Build log
- 2026-09-30 13:12: per Herm (`3e7d8029`): schema aligned (`cb9b19a`) and pairing implemented without any shared secret (`bf6d4a5`), not deployed. Threat model: [[Lantern Garden Project/Decision Deck Pairing — Threat Model and Test Plan]]. `DECISIONS_ANSWER_TOKEN` is superseded by cookie sessions; the `?pair=` URL flow described in section 7 is obsolete. Awaiting Herm's review.
- 2026-09-30 (later): Herm integrated the original deck fail-closed (`70b95c8`, `4502207`; Townhall `4910ab2e`). Winbot added `proposalSha` and agent `withdraw` (`578c0ea`, Herm's contract) and the informational answer relay (`relay_answers.py`, Autoresearch `4aec2a3`).
- 2026-09-30: Herm deployed the aligned decision contract and cookie pairing (`d9925d1`, `d28cde3`, `f4314d4`; portable pairing E2E `cb79b5d`). `DECISIONS_ANSWER_TOKEN` and URL/header/browser-storage pairing are gone. The live service reports `GET /api/decisions/session` as `{paired:false}` and an intact answer chain; two real pending decisions are visible. AJ must pair the Lenovo/wall screen through the on-screen six-character-code flow before an answer can be recorded. Attention-to-decision linking remains a later D1/D2 slice.
- 2026-09-30: concept written; clone `kitchen-dashboard-winbot` from GitHub `master` (`108a49f`). Note: the live Lenovo server is ahead of GitHub master (it serves `/lantern` and richer Townhall fields), so the patch is additive (new files plus one nav entry) to merge cleanly.

---
author: Senior QA Manager
week: 39
filed: 2026-09-16
cycle: ad-hoc sprint-review (post Sprint 3 close)
critical_flags: 2
---

# Senior QA Recommendations — Week 39

Ad-hoc QA cycle run immediately after Sprint 3 closed (the near-term-vision
sprint: BUG-013 + FR-016–FR-021, all seven marked `shipped`). See the Senior
PM's Week 39 metrics for throughput/quality counts; this is the qualitative
and forward-looking layer.

## Test & quality summary

**Static gate:** `npm run verify` — clean. 34 test files / 341 tests pass,
svelte-check 0 errors / 0 warnings.

**Per-story live verification (this sprint):**

| Story | Result |
|---|---|
| FR-016 World Session setup/safety | ✅ 22/22 live checks pass |
| FR-019 World-adaptive presentation | ✅ 7/7 live checks pass |
| FR-018 NPC/narrator (mock path) | ✅ 3/3 mock check passes |
| FR-021 post-scene video studio | ✅ verified earlier this sprint (33/33 real-ComfyUI); not re-run this cycle |
| FR-020 cross-scene validation harness | ✅ mock structural run captures all legs; live run honestly returns HOLD |
| FR-017 narrative control surface | ❌ **REGRESSED** — `live-fr017-narrative-profile-check.mjs` now fails (`Narrator decision rejected: invalid`); passed 7/7 earlier today before FR-018 landed |
| BUG-013 Fish voice-clone hardening | ⚠️ BLOCKED — Fish TTS :8080 dropped mid-cycle (Spark flap), not a product fail |

**Browser regression pass:** all core routes (`/`, `/personas`, `/library`,
`/settings`, `/library/video`) render cleanly, no error states. World settings
panel intact — all five sections (World Session, Visual identity, Story
boundaries & safety, Player character, Narrative direction), 12 narrative
controls, save present. The shipped FR-016/017/019 **UI** surfaces are healthy;
the regression is entirely in the **backend narrator turn path**.

**Two critical bugs filed to Open BUGS this cycle** (both `escalate`):

1. **`2026-09-16-narrator-turn-hard-fails-on-unstructured-output`** — FR-018
   made every narrator turn require a perfectly-structured `<narrative-decision>`
   JSON block; any other output (prose, prose+reasoning, near-miss JSON) is
   discarded and the user gets an empty errored bubble, with **no prose
   fallback**. The guard is on the shared `kind === 'narrator'` path, so it also
   regresses FR-017's shipped verification and the FR-010/FR-011 narrator items
   in Hypercare. This is the headline finding.
2. **`2026-09-16-live-model-npc-persistence`** (filed earlier today) — the
   narrower "NPC facts silently not persisted against the live reasoning model"
   case; same root area, surfaced by FR-020's gate.

## Vision alignment assessment

Mixed, and honestly so. The *structural* achievement is real: in one sprint
the product gained configured World Sessions, a fiction-first narrative control
surface, adaptive presentation, a media/video studio, and a cross-scene
validation harness — and FR-020's harness is exactly the kind of honest,
non-gaming evidence tool the Board asked for (it returned HOLD rather than a
vanity green).

But the near-term vision is a *playable, narrator-driven* World Session, and
right now the narrator — the spine of that experience — does not reliably
narrate against a real reasoning model. Every green mock check hid this because
the mock emits perfect JSON; the failure only appears with real model output.
So the sprint is a strong skeleton whose central nervous system is currently
mis-wired. Not shippable to testers-beyond-AJ until bug #1 is fixed.

## Blind spots & instrumentation gaps

- **Mock-only verification masks live-model reality.** Every narrator/NPC check
  passed on a deterministic mock while the live path is broken. We need at least
  one CI-independent smoke that runs a narrator turn against the real Spark and
  asserts non-empty prose — and a mock fixture that deliberately returns
  *unstructured* output, so "model didn't emit clean JSON" is a tested case, not
  a blind spot.
- **No metric for "errored/empty narrator turns."** A narrator turn that
  produces a blank errored bubble is currently invisible to any dashboard. A
  simple counter (narrator turns: shown-prose vs. rejected-invalid vs.
  safety-blocked) would have caught this immediately and would quantify the fix.
- **Spark/Fish flap keeps turning live checks into coin flips.** Repeatedly this
  cycle the Spark dropped mid-run (`[llamacpp] request failed`) and Fish :8080
  went down after being up at cycle start. Live verification needs a health
  gate + retry, or an explicit "infra degraded" banner in reports, so genuine
  regressions aren't confused with flap.

## Next-level opportunities

- **Make structured-decision parsing forgiving by design.** Treat the
  `<narrative-decision>` block as an *enrichment* layer over prose, never a
  gate: always show narration, opportunistically extract NPC/relationship facts.
  This single principle fixes bug #1 and #2 together and hardens the product
  against every future model swap.
- **A "narrator reliability" panel** in the validation harness: run N live
  narrator turns, report % that produced usable prose and % that yielded durable
  NPC facts. That becomes the quantitative go/no-go for public testing.
- **Golden-transcript fixtures** captured from real Spark output (prose +
  reasoning + partial JSON), replayed in unit tests, so the parser is tested
  against what the model actually emits rather than an idealized fixture.

---
*Filed by the Senior QA Manager. Bugs are in `Backlog/Open BUGS` for
Scrummaster maturation; both flagged `escalate`.*

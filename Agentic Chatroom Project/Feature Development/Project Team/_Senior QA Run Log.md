---
tags: [project/agora, type/run-log, role/senior-qa]
---

# Senior QA — Run Log

One line (or short block) per QA cycle: timestamp, what was tested, bugs found
(routine vs. escalated), and whether the weekly Board writeup was filed.
Escalated/critical findings are named at the top of their entry.

---

## 2026-09-16 — ad-hoc sprint-review (post Sprint 3 close)

**🚨 2 ESCALATED:** narrator turns hard-fail on unstructured model output
(`2026-09-16-narrator-turn-hard-fails-on-unstructured-output`); live-model NPC
persistence gap (`2026-09-16-live-model-npc-persistence`).

- **Scope tested:** Sprint 3's 7 shipped stories (BUG-013, FR-016–FR-021)
  against their acceptance criteria; light browser regression across core
  routes; Hypercare narrator-dependent items (FR-010, FR-011).
- **Static gate:** `npm run verify` clean — 34 files / 341 tests, 0 svelte
  errors/warnings.
- **Live scripts:** FR-016 22/22 ✅, FR-019 7/7 ✅, FR-018 mock 3/3 ✅;
  FR-017 `live-fr017-narrative-profile-check.mjs` ❌ **regressed** (was 7/7
  earlier today, now `Narrator decision rejected: invalid`); BUG-013 fish-clone
  BLOCKED (Fish :8080 dropped mid-cycle — infra flap, not a product fail).
- **Browser regression:** all core routes render, no error states; World
  settings panel intact (5 sections, 12 narrative controls, save present).
  Regression is backend-only (narrator turn path), UI healthy.
- **Root cause:** FR-018 (`9a58fea`) added a narrator-decision parse+validate
  gate in `ws.ts` (~L723–733) that discards the whole turn (empty errored
  bubble, no prose fallback) whenever output isn't a perfect
  `<narrative-decision>` JSON block. Fires for any `kind === 'narrator'`, so it
  regresses FR-017's verification and the FR-010/FR-011 Hypercare narrator
  paths too. Reproduced deterministically via the echo mock (no live model
  needed).
- **Infra note:** Spark (`qwen3.8-27b-aggressive-q5`) flapped repeatedly this
  cycle and Fish :8080 dropped after being up at start — live-model narrator
  confirmation was transport-degraded; mock reproduction is the authoritative
  evidence. Recorded as degraded, not as passes.
- **Bugs filed:** 2, both `escalate`, into `Backlog/Open BUGS`.
- **User feedback:** `QA/User feedback` intake empty — nothing to triage.
- **Test data hygiene:** re-cleaned all throwaway worlds/personas/connections
  the live scripts created; live site back to AJ's 3 worlds / 17 personas.
- **Board writeup:** filed — `THE BOARD/.../This weeks metrics from
  stakeholders/Week 39 - Senior QA recommendations.md`.

---
found_by: Senior QA Manager
found: 2026-09-16
context: sprint-review
severity_hint: escalate
related_release: "[[FR-018-guided-narrator-agency-and-persistent-npcs]]"
---

> [!danger] Critical — gates public-testing readiness
> The cross-scene validation gate (FR-020) recommends **HOLD** because of this
> bug. FR-018's persistent-NPC feature works under the deterministic mock path
> but does **not** reliably persist NPCs when driven by the real Spark reasoning
> model, so configured World Sessions silently lose their established
> characters across a Scene transition in live play.

# Live reasoning model does not persist narrator-introduced NPCs

## What happened
FR-018 shipped guided narrator agency + persistent NPC development, verified
green against a deterministic mock LLM (`scripts/live-npc-narrator-check.mjs`,
3/3). When FR-020's cross-scene validation scenario was run for the first time
against the **live** Spark model (`qwen3.8-27b-aggressive-q5` on
`192.168.0.139:8014`) instead of the mock, the narrator produced fluent prose
but **no NPC row was persisted** — so the World had no established characters to
carry into the second Scene.

The mock fixture returns a clean, schema-perfect
`<narrative-decision>{…}</narrative-decision>` block every time, which is why
the mock-backed checks pass. The live reasoning model does not reliably emit the
structured co-author decision in the parseable form FR-018's parser/validator
requires, so `recreateSceneVideo`… (the narrator decision path) extracts prose
only and drops the NPC/relationship facts. This is a real-model output-format
reliability gap, not a mock or a schema bug.

## Steps to reproduce / evidence
Against a running server on `:7481` with the Spark reachable:

```
SCENARIOS=world-session-cross-scene \
AGORA_SCENARIO_LLM=http://192.168.0.139:8014/v1 \
node scripts/live-experience-scenario-check.mjs
```

Live run report (`scripts/scenario-output/…`) recorded:

| Surface | outcome | observation |
|---|---|---|
| narrator/NPC agency | **observed-risk** | `Mara Venn was not persisted` |
| cross-scene memory/relationship continuity | **observed-risk** | `NPC missing after scene transition` |

Per-turn latency was captured (8712 ms, 20271 ms — the model *did* answer), so
this is not an infra/timeout blocked record; the turns completed and the NPC
simply never landed. Public-readiness recommendation from the same run:

> **HOLD — structural risks require QA review**

The identical scenario in `SCENARIO_MODE=mock` records all seven surfaces as
`captured` with continuity across 2 scenes — confirming the gap is specifically
the live model's freeform output vs. the required structured decision, not the
persistence logic itself.

## Suspected severity & why
Escalate. FR-018's core user-facing promise — a narrator that introduces
NPCs who persist and are remembered across Scenes — does not hold in real play,
only under the test fixture. It is the single risk standing between this sprint
and a public-testing "go," and it is invisible to every mock-backed check. The
likely fix is hardening the narrator decision path against real reasoning-model
output (a retry/repair or a more tolerant extractor for the
`<narrative-decision>` payload, plus a budget check — the model is a reasoning
model that streams chain-of-thought before `content`), not a change to the
persistence schema.

## Reference
- Related story: [[FR-018-guided-narrator-agency-and-persistent-npcs]] (shipped this sprint, in Hypercare).
- Surfaced by: [[FR-020-cross-scene-world-session-validation]]'s canonical scenario, live-model run.
- Relevant reasoning-model behavior notes: the Spark serves a reasoning model whose answer lands in `content` only after chain-of-thought on `reasoning_content`; empty/partial structured output under budget pressure is a known class of failure for this box.

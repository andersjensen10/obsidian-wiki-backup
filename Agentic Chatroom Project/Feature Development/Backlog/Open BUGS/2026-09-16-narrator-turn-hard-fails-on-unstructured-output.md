---
found_by: Senior QA Manager
found: 2026-09-16
context: sprint-review
severity_hint: escalate
related_release: "[[FR-018-guided-narrator-agency-and-persistent-npcs]]"
---

> [!danger] Critical — narrator turns hard-fail instead of narrating
> FR-018 made every narrator turn require the model to emit an exactly-shaped
> `<narrative-decision>` JSON block. When the model's output is anything else
> (plain prose, prose + reasoning, a near-miss JSON), the **entire turn is
> discarded**: the reply row is persisted with EMPTY content and an `error` is
> pushed to the client. There is **no fallback to plain narration**. This
> regresses the core World Session experience and also breaks the shipped,
> previously-passing FR-017 verification and the FR-010/FR-011 narrator paths
> currently in Hypercare.

# Narrator turns are rejected as "invalid" when output is not perfectly structured JSON

## What happened
FR-018 (`9a58fea`) added a guard in the narrator turn path
(`apps/server/src/routes/ws.ts` ~lines 723–733): after a narrator persona
streams its reply, the server runs `parseNarratorDecision(text)` +
`validateNarratorDecision(...)`. If the text is not a parseable
`<narrative-decision>{…}</narrative-decision>` block with a valid `beat` (and
well-formed optional `npc`/`relationship`), `parseNarratorDecision` returns
`null`, the verdict is `invalid`, and the code does:

```
const failed = persistReply({ messageId, roomId, persona, content: '', error: detail });
send({ type: 'error', message: detail, messageId }); send({ type: 'message_done', message: failed }); return null;
```

So a narrator turn that doesn't emit the exact structured payload produces an
**empty, errored bubble** — no prose is shown, nothing is salvaged. The guard
fires for **any** persona with `kind === 'narrator'` in any World/Scene, so it
is not scoped to FR-018's own new NPC feature; it sits on the shared narrator
turn path that FR-010 (narrated scenes) and FR-011 (narrator pacing) also use.

This is distinct from, and more severe than,
[[2026-09-16-live-model-npc-persistence]]: that bug is "the NPC fact silently
isn't persisted"; this bug is "the narrator says nothing at all and the user
sees an error."

## Steps to reproduce / evidence
Deterministic, no live model needed — uses the repo's echo mock:

```
node scripts/live-fr017-narrative-profile-check.mjs
```

Result this cycle:
```
PASS  low narrative profile persisted on create
Error: Narrator decision rejected: invalid.   ← throws, exit 1
```

This same script passed **7/7 earlier today**, immediately after FR-017
shipped and *before* FR-018 landed. `git log -S 'Narrator decision rejected'`
attributes the introducing commit to `9a58fea` (FR-018). The echo mock returns
`ECHO SYSTEM<<…>>` (representative of any non-structured model output); before
FR-018 the narrator turn returned that prose fine, now it is rejected.

Live-model confirmation was attempted against the Spark
(`qwen3.8-27b-aggressive-q5`) but the box was flapping this cycle
(`[llamacpp] request … failed`, Fish :8080 also dropped mid-run), so live
narrator turns errored on transport rather than cleanly demonstrating the
parse rejection — recorded as degraded infra, not a clean live datapoint. The
mock reproduction is the authoritative evidence.

## Suspected severity & why
Escalate — arguably the single most important finding of this review. The
narrator is the spine of the configured World Session experience (FR-010/011/
016/017/018). As shipped, a narrator only "works" when the model happens to
emit flawless structured JSON; every other turn is a blank errored bubble.
Reasoning models (this project's own Spark model included) stream freeform
prose and chain-of-thought, so in real play this will fire constantly. It also
means FR-017's and FR-010/011's Hypercare verifications no longer pass.

Suggested fix direction (for Scrummaster/dev, not prescriptive): when
`parseNarratorDecision` fails, **fall back to showing the raw narrator prose**
(optionally strip a reasoning block) and simply skip persisting NPC/relationship
facts, instead of discarding the whole turn. Only hard-reject on a genuine
`player_agency`/`safety` verdict, never on `invalid`. Pair with a
parse/repair-retry and a reasoning-budget check.

## Reference
- Introducing story/commit: [[FR-018-guided-narrator-agency-and-persistent-npcs]] / `9a58fea`.
- Regresses shipped verification of: [[FR-017-narrative-control-surface]] (its `scripts/live-fr017-narrative-profile-check.mjs` now fails).
- Regresses Hypercare items: [[FR-010-worlds-and-scenes-ui — Part 2 of 2]] (narrated scenes) and [[FR-011-narrator-pacing-intelligence]] (pacing narrator) — same `kind === 'narrator'` turn path.
- Related, narrower bug: [[2026-09-16-live-model-npc-persistence]].

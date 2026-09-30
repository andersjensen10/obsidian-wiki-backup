---
tags: [type/evidence-bundle, autonomy, lantern-garden, prototype, testing]
created: 2026-09-30
status: verified-isolated-prototype
---

# Morning Review Card Prototype — Evidence

**Run:** 2026-09-30 02:15 CEST  
**Mission class:** isolated prototype/testing  
**Scope:** local fixture-driven code and vault artifacts only. No production service, dashboard route, Hermes configuration, credential, network exposure, device state, Townhall schema, Spark inference, or ComfyUI job changed.

## What changed

Created a deterministic, fixture-only **Morning Review Card** renderer at:

- `Research/Autonomy Lab/morning-review-card-prototype/mission_card.py`
- `Research/Autonomy Lab/morning-review-card-prototype/fixtures/`
- `Research/Autonomy Lab/morning-review-card-prototype/tests/test_mission_card.py`
- `Research/Autonomy Lab/morning-review-card-prototype/generated-ready-card.md`
- `Research/Autonomy Lab/morning-review-card-prototype/generated-deferred-card.md`

The contract requires a mission id, selection time, source list, hypothesis, resource class, admission state, yield rule, sandbox boundary, measurable signals, evidence paths, promotion decision, one morning question, and rollback. It supports `none`, `local-cpu`, and `spark` resource classes.

The safety rule is executable: a Spark mission with an admission state of `busy` or `unreadable` can render only when its promotion decision is exactly `deferred`. Non-Spark cards must explicitly declare `not-required` admission rather than silently omitting it.

## Evidence

### Live resource check before selection

At 02:15 CEST, both llama.cpp slots at `192.168.0.139:8014/slots` returned `is_processing: false`; ComfyUI `:8188/queue` returned empty running and pending arrays. Townhall contained the active Spark-aware Inspiration Radar policy and an active Winbot Dreams thread, so this mission deliberately used **no shared compute** despite the idle snapshot.

### Executed validation

Direct test run:

```text
Ran 5 tests in 0.001s
OK
```

The tests proved:

1. The ready local-CPU fixture renders byte-identically twice and contains a review question.
2. A busy Spark fixture renders `DEFERRED` and reports its busy admission state.
3. A card missing rollback is rejected.
4. A busy Spark card that tries to claim promotion is rejected.
5. A card with no morning question is rejected.

An independent CLI negative case also returned the expected validation error:

```text
error: rollback must be a non-empty string
```

The generated ready card is the inspectable artifact. Its question is:

> Is this card contract useful enough to apply to the next autonomy mission?

## Scorecard movement

- **Morning-reviewable artifacts:** +1 verified artifact, now paired with an executable contract rather than a prose-only proposal.
- **Explicit evidence / rollback / next decision:** the generator rejects missing rollback and missing morning-decision fields rather than relying on agent discipline.
- **Cross-service connection:** Townhall coordination and Spark-admission semantics are represented in a local, testable card without coupling the prototype to either service.
- **AJ sysadmin burden:** no new daemon, schedule, account, secret, or service dependency was introduced.

## Limits

This is not connected to the Kitchen Wall, Townhall write path, cron runtime, or a live fleet query. The fixtures are deliberately supplied inputs. Therefore it is evidence that the promotion contract is testable—not evidence that a production morning-review pipeline exists.

## Rollback

Delete `Research/Autonomy Lab/morning-review-card-prototype/`. No runtime state, service configuration, queue item, or external record depends on it.

## Next benchmark

Use this exact contract for one future **read-only** live-input adapter: collect a saved Townhall search result plus fresh fleet/admission snapshots into a versioned JSON fixture, render a card, and independently compare the rendered evidence paths against those saved inputs. Keep it out of the dashboard and do not promote it to a scheduled worker until that adapter proves deterministic and traceable.

## Follow-up benchmark — saved Townhall adapter

Created `Research/Autonomy Lab/townhall-readonly-adapter/` as the next isolated step. It consumes a saved, redacted Townhall search fixture containing the two latest relevant `home-lan` posts, validates provenance and project scope, and renders `generated-card.md` with both exact post IDs and the no-side-effect boundary.

Validation: `Ran 3 tests ... OK` — traceable rendering, byte-identical repeat rendering, and rejection of a missing post ID. This is still a fixture adapter, not a live Townhall/fleet connector: no Townhall write, fleet query, dashboard change, credential access, queue submission, or device action occurred.

Rollback: delete `Research/Autonomy Lab/townhall-readonly-adapter/`. Next boundary is Herm's decision to supply a fresh fleet/admission snapshot format; until then, no production or scheduled promotion is proposed.

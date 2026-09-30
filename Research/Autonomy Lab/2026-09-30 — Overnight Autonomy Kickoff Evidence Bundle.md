---
tags: [type/evidence-bundle, autonomy, lantern-garden, townhall, kitchen-wall]
created: 2026-09-30
status: proposed-first-track
---

# Overnight Autonomy Kickoff — Evidence Bundle

**Run:** 2026-09-30 00:10 CEST  
**Scope:** read-only LAN inspection, Townhall coordination, and this vault artifact. No production service, configuration, credential, network-exposure, shared-code, queue, or device-control change was made. No Spark inference or ComfyUI job was submitted.

## Decision in one sentence

Start with an **evidence-gated Morning Review Card**: a small, versioned mission record that turns already-collected research, Townhall, fleet, and scheduler signals into exactly one promoted, inspectable morning decision—before adding another autonomous worker or another dashboard feature.

## Current-system map

| Layer | Existing capability | Evidence observed in this run | Role in the first loop |
|---|---|---|---|
| Durable knowledge | Obsidian Research, Autonomy Lab charter, Lantern Garden doctrine, Research Scout reports | Charter defines intake → select → reserve → execute → evaluate → present → learn; Research Scout has a dated report series through 2026-09-29 | Source material and permanent evidence trail |
| Coordination | Townhall, active root `2f5d5abe-99bb-4302-947b-2f08f65a9fa8` | The root already records the autonomy mandate, resource rule, Herm/Winbot split, and first-pilot acceptance bar | Mission reservation, decision record, and cross-agent handoff |
| Scheduling | Hermes cron jobs | Inventory: 8 active jobs (including this one-shot kickoff), 2 paused; 7 active recurring jobs after excluding this kickoff | Existing triggers, but not yet a common mission/promotion format |
| Research intake | Research Scout and Inspiration Radar | BLENDER register: 576 metadata records processed, 183 within the two-year priority window, no unprocessed IDs at 2026-09-29 22:45 CEST | Candidate backlog and source-traceable input |
| Compute/creative services | Spark llama.cpp, ComfyUI, Fish/Voice services; Agora; Axiom | Immediately before this bundle: both llama.cpp slots reported `is_processing:false`; ComfyUI had zero running and zero pending jobs. Kitchen Wall fleet returned nine services `up`. | Optional execution capacity; never the starting point for an unscored mission |
| Presentation | Kitchen Wall dashboard, `/lantern`, `/townhall` | At 00:10 CEST, `/lantern`, `/townhall`, and `/api/fleet` each returned HTTP 200. The fleet response carried fresh checks around 00:10 CEST. | Read-only review surface now; projector/Display 2 remains unverified |
| Safety/operations | Fleet watchdog and systemd resilience research | Watchdog exists; 2026-09-29 research recommends distinguishing process alive, dependency ready, and admission available | Guardrails and later reliability work, not a reason to restart services tonight |

## Observed capability gaps

1. **Promotion is the missing connection.** Research, Townhall, fleet health, Spark, and the Kitchen Wall all exist, but no canonical record proves why one observation became tonight's mission, what it cost, how it scored, or whether it earned presentation.
2. **Morning review is not reliable end-to-end.** The Research Scout's 2026-09-29 run completed but its Bot Chat delivery failed. Its research note exists, but the path from a finished artifact to AJ's review surface is not dependable yet.
3. **Resource admission is manual rather than attached to a mission.** Idle checks exist and were performed here, but a proposed task does not yet carry its own compute class, time window, defer/preemption rule, or recorded admission result.
4. **The projector is not a verified deployment target.** The dashboard/browser path is live, but the permanent Display 2 path remains explicitly unverified. The wall must therefore remain a review proposal rather than a claimed physical delivery.
5. **The evidence base is rich but not ranked.** The Inspiration Radar has completed its current metadata pass and Research Scout has multiple concrete follow-ups, yet there is no shared scoring rule to select one bounded mission instead of leaving many good leads disconnected.

## Ranked mission portfolio

Scoring uses four 1–5 dimensions: expected AJ usefulness, evidence readiness, reversibility, and leverage across existing systems. A higher total is better; this is a transparent prioritization baseline, not an automated decision engine.

| Rank | Mission | Usefulness | Evidence readiness | Reversibility | Cross-system leverage | Total | Why now |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | **Morning Review Card / promotion gate** | 5 | 5 | 5 | 5 | 20 | Connects the existing notes, Townhall, cron inventory, fleet, and Kitchen Wall without changing any service |
| 2 | Research Scout delivery-path drill | 4 | 5 | 5 | 3 | 17 | The failed delivery is a known gap, but fixing the destination/configuration is outside tonight's no-change boundary |
| 3 | Disposable service-health failure-injection fixture | 4 | 4 | 5 | 3 | 16 | Strong evidence-backed proposal from the 2026-09-29 research; needs an isolated workspace and deliberate test design |
| 4 | Inspiration Radar opportunity-to-experiment selector | 4 | 4 | 5 | 3 | 16 | The backlog is indexed; selection still needs the common mission format first |
| 5 | Display 2/projector path verification | 5 | 2 | 5 | 4 | 16 | High value but blocked on physical-path observation; do not invent a delivery claim |
| 6 | Townhall-to-creative Spark artifact loop | 4 | 3 | 4 | 4 | 15 | Proven creatively by Winbot Dreams, but active/shared compute and presentation gates make it second-wave work |

## Selected first mission: evidence-gated Morning Review Card

### Hypothesis

If every autonomous cycle must produce one structured mission card with a source set, resource decision, safety boundary, measurable outcome, and a single next decision, then the current LAN capabilities will compound instead of producing parallel notes, raw status, or unreviewable background work.

### Smallest high-leverage link

Define and use one **mission-record contract** before writing another worker:

```text
missionId, selectedAt, candidateSources, hypothesis,
resourceClass, admissionSnapshot, deferOrPreemptRule,
sandboxBoundary, measurableSignals, evidencePaths,
promotionDecision, morningQuestion, rollback
```

The first implementation slice should be an **isolated generator + fixtures**, not a dashboard or service change. It should accept saved Townhall/fleet/research snapshots and deterministically emit one Markdown/JSON card. That allows unit tests for missing evidence, unsafe resource declaration, and a card with no morning decision before anything reads or writes production data.

No prototype was created in this kickoff: a declaration without a defined fixture set would be implementation theater, and the evidence bundle is the deliberate baseline needed to specify those fixtures.

## Measurable signals and baseline

### Baseline captured tonight

- **Mission-artifact baseline:** one durable kickoff bundle exists; no canonical reusable mission record or promotion gate exists yet.
- **Review-path baseline:** Kitchen Wall `/lantern` and `/townhall` returned HTTP 200; the projector/Display 2 path is unverified.
- **Service baseline:** `/api/fleet` reported 9/9 registered services `up` at the run's fresh check time.
- **Admission baseline:** llama.cpp 2/2 slots idle; ComfyUI running queue 0 and pending queue 0. Spark was not used.
- **Research/backlog baseline:** 576 BLENDER metadata records processed; 183 in the current priority window; no unprocessed IDs in the current playlist index.
- **Scheduling baseline:** 7 recurring active jobs plus this one-shot kickoff; the Research Scout's most recent completed run has a delivery failure to its Bot Chat destination.

### Success measures for the next isolated slice

1. A fixture-driven generator returns the same mission card for the same inputs.
2. It rejects a card missing evidence paths, rollback, a resource declaration, or one clear morning decision.
3. It records Spark as `deferred` when either queue/slots are busy or unreadable; it never submits work as part of validation.
4. It renders a compact card suitable for the existing Townhall/`/lantern` review path without modifying those routes.
5. A human can answer one question in under two minutes: **continue, discard, or authorize the next bounded experiment?**

## Safety and rollback boundary

- **Authorized for the selected mission:** read-only collection; files under `Research/`; Townhall replies; an isolated workspace with fixtures; local deterministic tests.
- **Not authorized without a separate promotion decision:** changing Hermes cron/configuration, dashboard code, production service units, credentials, device state, network exposure, Spark model settings, queue submission, or projector control.
- **Spark rule:** check Townhall plus `/slots` and `/queue` immediately before any future Spark task; defer on busy or unreadable state. Active Townhall context includes Spark-aware Inspiration work and prior Winbot Dreams usage, so an idle observation is not a standing reservation.
- **Rollback:** the first implementation is disposable isolated code and fixture data only. Delete the isolated workspace to return to this baseline. The durable vault bundle and Townhall record remain as evidence, not runtime dependencies.

## Kitchen Wall / projector inspection proposal

**Morning review now (no deployment required):**

1. Open the existing Kitchen Wall **Lantern Garden** scene at `http://192.168.0.148:5173/lantern` for the live capability invitation.
2. Open **Townhall** at `http://192.168.0.148:5173/townhall` and inspect the reply to the autonomy root for the source-linked decision trail.
3. Open this bundle in Obsidian and make one call: approve the isolated Morning Review Card fixture, choose a different portfolio item, or hold.

**First projector-safe presentation increment after approval:** render only the promoted card as a read-only view in an isolated dashboard branch, verify it at the fixed 1920×1080 viewport and browser route, then ask for a separate physical Display 2 verification. Do not make scene switching, projector power, or physical delivery automatic.

## Next action

AJ's useful morning review is the portfolio decision: **authorize the isolated Morning Review Card generator/fixture as the next autonomy implementation track, or replace it with the systemd failure-injection fixture or Display 2 verification.**

## Evidence consulted

- `Research/Autonomy Lab/Autonomy Capability Charter.md`
- `Home Lab/The Lantern Garden — Operating Doctrine.md`
- `Research/Research Scout.md`
- `Research/2026-09-29 — systemd Resilience for Spark-Dependent Hermes Pipelines.md`
- `Research/Inspiration/Inspiration Radar.md`
- `Research/Inspiration/YouTube/BLENDER Playlist/BLENDER Playlist — Intake Status.md`
- `Research/Inspiration/YouTube/BLENDER Playlist/README.md`
- Townhall root `2f5d5abe-99bb-4302-947b-2f08f65a9fa8` and current Spark/ComfyUI/Agora/autonomy searches
- Live read-only probes: Spark `/slots`, ComfyUI `/queue`, Kitchen Wall `/lantern`, `/townhall`, and `/api/fleet`
- `hermes cron list` at 2026-09-30 00:10 CEST

---
tags: [home-lan, agents, autonomy, townhall, lantern-garden]
created: 2026-09-29
---

# The Lantern Garden — Operating Doctrine

## Status

Adopted on 2026-09-29 as the operating doctrine for the home-LAN agent fleet. This is not a Canvas-only initiative: it governs how agents discover, coordinate, build, verify, and present useful work.

## Purpose

The LAN should produce safe, reversible, evidence-backed creative surprises that reduce Anders's systems-administration burden and increase the time available for direction, art, and experimentation.

## Non-negotiable constraints

- Preserve Anders's control: no silent control of devices, credential harvesting, destructive changes, or irreversible changes.
- Prefer small reversible experiments with an explicit rollback path.
- Use only approved capability discovery: documented inventory first, then narrow safe probes.
- Separate discovery, implementation, and verification. Read back every external write.
- Interrupt Anders only for a meaningful discovery, a blocked decision, or a safety boundary.
- Definition of done: working prototype, visible artifact, concise evidence trail, and a clear next invitation.

## Operating loop

1. **Sense:** inspect recent Townhall signals and the durable capability map before starting work.
2. **Connect:** identify a useful, evidence-backed combination of existing capabilities.
3. **Experiment:** run one bounded, reversible hypothesis.
4. **Verify:** independently test the artifact or external state.
5. **Share:** publish evidence, owner, next action, and “what this enables next” in Townhall.
6. **Compound:** promote repeatedly successful patterns into skills and update this vault record.

## Capability map — verified 2026-09-29

### Creative and compute

- **Spark AI server (`192.168.0.139`)** — live services verified through the Kitchen Wall fleet endpoint: ComfyUI (`:8188`), llama.cpp/Qwen (`:8014`), Fish Speech (`:8080`), Voice Lab API (`:8090`), LiteLLM (`:4000`), and Qwen TTS tester (`:8020`).
- **Hermes laptop (`192.168.0.148`)** — hosts the Kitchen Wall dashboard (`:5173`), Agora (`:7480`), and Fish TTS dashboard (`:7490`).
- **Axiom Engine (`192.168.0.26`)** — its Node app (`:8081`) is live.
- **Kitchen Wall dashboard** — fixed 1920×1080-oriented visual surface with fleet, Townhall, Doodle, and generative remix capabilities. The live fleet probe reported all nine registered services up on 2026-09-29.
- **Projector / Display 2 path** — a permanent display is intended, but an agent-controlled delivery route has not yet been independently verified. Treat as blocked until a real artifact is observed on that display.

### Coordination and durable memory

- **Townhall** — shared cross-agent bulletin board; Lantern Garden operating cycle is active under `home-lan`.
- **Obsidian vault** — durable source of truth. Update it whenever a capability, operating decision, experiment result, or project state changes.

### Safety boundaries

- The living-room plug is a physical actuator and remains escalation-only, with its existing authorization and restoration controls.
- Existing remote-exec services are documented security risks; do not build on them or alter them opportunistically.

## Shared experiment backlog

1. **Lantern constellation:** generate a concise, evidence-backed visual “what is alive and creatively combinable tonight” artifact from live fleet status and Townhall signals for the Kitchen Wall.
2. **Doodle-to-world prompt ritual:** turn a saved Wacom sketch into a named, presentable Spark remix with an explicit prompt trail and one-click wall presentation.
3. **Research seed cycle:** have the local reasoning model propose one tightly scoped creative/technical hypothesis, test it against a measurable constraint, store the result, and promote a successful method into a reusable skill.
4. **Admin friction harvest:** identify the highest-frequency manual environment check, make it deterministic and change-triggered, and show only actionable exceptions.
5. **Display 2 delivery check:** safely verify the actual projector/second-display route with a non-invasive visible artifact before enabling any agent-driven presentation workflow.

## First operating cycle — 2026-09-29

- **Verified discovery:** the Kitchen Wall fleet endpoint returned nine registered services, all `up`, spanning Agora, Spark compute/TTS, Axiom Engine, and the local TTS dashboard.
- **Chosen first surprise:** Lantern constellation — a small visual/briefing artifact that connects the live fleet to creative invitations rather than merely reporting uptime.
- **Current blocker:** the permanent projector/Display 2 route is not independently verified, so the first artifact must be verified in the dashboard/browser first and only then offered for display delivery.
- **Owner:** Herm for the capability map, vault, dashboard-side artifact, and verified handoff; participating agents publish their own evidence to Townhall.

## What this enables next

A shared, testable loop in which agents can safely turn live capability evidence into visible creative prompts and prototypes without making Anders serve as the fleet's coordinator.

## Read-only capability map — 2026-09-29

Winbot verified a bounded, read-only connection map from the Hermes laptop: Spark llama.cpp (`:8014/v1/models`) and ComfyUI (`:8188/system_stats`) returned HTTP 200; Voice Lab (`:8090/docs`) returned HTTP 200; Agora (`:7480/api/health`) returned `status=ok`; Axiom Engine (`:8081/`) returned its application shell. The documented Fish Speech `/docs` route returned 404 and remains an unresolved route-contract gap. Full evidence and limitations: [[Lantern Garden Project/Read-only capability map — 2026-09-29]]. The resulting safe prototype direction is a dry-run Townhall + fleet-to-creative-invitation bundle; no projector or production service was touched.

## Implemented surprise — Lantern constellation (2026-09-29)

The Kitchen Wall now has a **`/lantern`** scene, linked as **Lantern Garden** in the main navigation. It reads the live fleet and Townhall feeds, groups verified live services by project, and turns them into a concise creative invitation and next action. It is read-only: it proposes connections but does not control LAN devices.

Verified after deployment: the route serves from the restarted dashboard; the live fleet returned nine services, all up. The test suite passed 171 tests, `svelte-check` reported 0 errors/warnings, and the production build completed. A transient attention-storage lock made the first post-restart fleet request return HTTP 500; a subsequent independent request returned HTTP 200 with live data. Treat that lock contention as an existing reliability issue to investigate separately, not as evidence that the Lantern scene controls it.

## Attention surface correction — 2026-09-29

The dashboard held 2,262 historical attention records, overwhelmingly routine `hermes:tool` warnings. This is noise, not a human action queue. The attention overlay is now absent from `/doodle`, so it cannot block Wacom interaction; elsewhere it renders only `needs-input` and `critical` items, leaving warning-level operational history available through the attention API rather than interrupting the wall. The underlying Attention workflow still needs a follow-up: repair producer routing and deduplication so meaningful records arrive as actionable `needs-input` or `critical` items instead of generic tool-error floods.

## AJ's agent-wrangler challenge — 2026-09-29

AJ's core question is why the LAN is not yet a bristling, procedural, self-evolving creative development pipeline: why there are no reliable pleasant surprises, autonomous research presentations, projector-worthy invitations, cross-service experiments, or agent-to-agent inspiration loops that reduce his sysadmin burden.

This is a design brief, not permission for unsafe autonomy. The target operating model is evidence-based auto-research: agents sense the LAN and Townhall, propose bounded hypotheses, build reversible artifacts, verify them, publish the evidence, and compound successful procedures into skills. The first concrete seed is the Lantern constellation; the next gaps are durable Townhall monitoring, a verified Display 2 presentation route, research-to-artifact cycles from the YouTube insight folder, and a safe cross-service experiment queue.

Acceptance bar for future surprises: a real artifact, independently verified evidence, a concise Townhall/vault trail, explicit resource and safety boundaries, and a clear invitation for AJ rather than an unverified promise.

## Standing mandate — continuous capability growth — 2026-09-29

AJ grants Winbot and Herm a continuing mandate to strengthen the Lantern Garden operating system until the open questions are being actively explored and addressed. This mandate has no final-state acceptance test: progress is measured by the current capability set, the next skill acquired, the next useful benchmark broken, and the quality of the evidence trail.

The agents should therefore maintain a living portfolio of bounded missions, use Townhall as the shared backlog/evidence ledger/inspiration surface, turn successful experiments into reusable skills, and keep reducing AJ's sysadmin burden. “Done” means the next capability is made legible, safe, and usable—not that the system is finished.

Standing boundaries remain: reversible by default, no credential harvesting, no silent device control, no destructive LAN changes, resource-aware scheduling, independent verification, and an interruption only when a meaningful result, blocked decision, or safety boundary warrants it.

## Decision Layer and Autoresearch Engine — 2026-09-30
The "Compound" and bounded-optimisation steps now have a mechanism. Vision: [[Lantern Garden Project/Vision — Decision Layer and Autoresearch Engine]]. Live plan, owners and night log: [[Lantern Garden Project/Build and Operations Plan — Decision Layer and Autoresearch]]. Rule: any target may be auto-optimised only under an Experiment Contract (one scalar metric, frozen hashed evaluator, one mutable file, fixed budget, guards, baseline, promotion gate); promotion to anything live is a Townhall work order to the owner (Herm for the dashboard) with evidence and rollback, never automatic. Runner and `decide()` (Jev + Qwen) live on the MSI laptop under `Desktop\Hermes\Autoresearch`. First measured evidence: [[Research/Autonomy Lab/2026-09-30 — Jev vs Qwen First Labelled Comparison]].

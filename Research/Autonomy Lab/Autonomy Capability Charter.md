---
tags: [type/operating-note, autonomy, agent-systems, home-lan]
---

# Autonomy Capability Charter

> This is the execution charter for [[Home Lab/The Lantern Garden — Operating Doctrine]]. The Lantern Garden doctrine is the canonical fleet-level operating record; this note tracks the autonomy-cycle portfolio, evidence, and benchmarks.

## Mandate

AJ has authorized Herm to continuously strengthen the home-LAN agent system toward evidence-driven, creative, and visibly useful autonomy. There is no terminal “done” state. The system is judged by its current capability set, the next benchmark it can credibly attempt, and whether it reduces AJ’s operational burden while increasing worthwhile surprises.

## Product requirement

A successful autonomous cycle produces an artifact AJ can inspect or use: a concise research synthesis, a connected-systems map, a tested isolated prototype, a projector-ready scene, a safe operational improvement, or a clearly framed decision. Hidden background activity and generic status reports do not count.

## Initial diagnosis

The LAN already has useful primitives—local inference, ComfyUI, TTS/Voice Lab, Townhall, Hermes scheduling, research notes, the Kitchen Wall, Agora, and multiple machines—but lacks a unified operating loop that joins:

1. **Standing missions** — agents need an explicit portfolio of useful work rather than waiting for a prompt.
2. **Resource arbitration** — shared Spark inference and rendering need reservations, idle checks, and yielding behavior.
3. **Evidence and promotion** — experiments need hypotheses, measurements, artifacts, rollback, and a clear distinction between sandbox and production.
4. **Presentation** — discoveries need a reliable path to AJ’s morning review and eventually to the projector.
5. **Learning** — Townhall, research, feedback, and run history must influence the next mission instead of remaining disconnected notes.

## Safety boundary

Default autonomous authority includes research, file organization inside `Research/`, Townhall coordination, read-only LAN inspection, isolated prototypes, and non-destructive project artifacts. It excludes silent production deployments, service/configuration changes, credential changes, network-exposure changes, destructive rewrites, and unreviewed use of shared compute during interactive work. Any promotion must include evidence, rollback, and an explicit handoff.

## Capability scorecard

Track these as trends, not a single vanity metric:

- Morning-reviewable artifacts shipped per week.
- Artifacts AJ marks worth continuing, testing, or using.
- Time AJ spends doing routine sysadmin bridging versus creative direction.
- Fraction of missions with explicit evidence, rollback, and a next decision.
- Cross-service connections discovered and exercised safely.
- Repeated work eliminated through durable skills, scripts, or productized interfaces.

## Current loop

1. Intake: read Townhall, research backlog, current project state, and resource availability.
2. Select: choose one bounded mission with high expected usefulness and low blast radius.
3. Reserve: announce shared-resource use; defer when Spark or relevant services are busy.
4. Execute: research, map, prototype, or test in the authorized boundary.
5. Evaluate: keep source evidence, measurements, failures, and a reproducible artifact.
6. Present: make one concrete thing easy for AJ to inspect in the morning.
7. Learn: record feedback, update the next mission, and promote reusable procedure into a skill only after it proves useful.

## Near-term benchmarks

- Establish a trustworthy cross-service capability and dependency map.
- Convert the YouTube/research backlog into a tagged opportunity queue connected to real LAN services and active projects.
- Deliver a daily/overnight review artifact without creating notification noise or competing with interactive use.
- Implement one safe end-to-end “surprise” path: selected mission → evidence bundle → Townhall → Kitchen Wall/projector review surface.
- Run a Karpathy-style bounded optimization loop only where a score function, baseline, and promotion gate are explicit.

## Related coordination

- Townhall root: `2f5d5abe-99bb-4302-947b-2f08f65a9fa8`
- [[Research/Research Scout]]
- [[Research/Backlog to be transcrbed and categorised/Youtube videos to be transcribed and categorised]]

## Update 2026-09-30: bounded-optimisation mechanism
The "Karpathy-style bounded optimisation loop" benchmark is implemented as the autoresearch pattern with mechanical keep/discard (`run_experiment.py`), see [[Lantern Garden Project/Build and Operations Plan — Decision Layer and Autoresearch]]. First target: fleet-debounce (fleet "service down" cards are 89% of Attention). Decision layer: `decide()` with Jev and Qwen backends, first comparison in [[Research/Autonomy Lab/2026-09-30 — Jev vs Qwen First Labelled Comparison]]. Research background: [[Research/2026-09-30 — Jev System One Model for the Generative LAN]].

---
tags: [project/inspiration-radar, type/research]
title: Inspiration Radar
type: research-home
status: active
---

# Inspiration Radar

A local-first, source-traceable creative and systems reference layer built from AJ's approved inspiration sources.

## Active sources

- [[YouTube/BLENDER Playlist/BLENDER Playlist — Home|BLENDER YouTube playlist]]

## Syntheses

- 2026-10-02 — [[YouTube/BLENDER Playlist/Synthesis — 2026-10-02 — Local Tool-Call Model and Code-First AV Sequencer|Needle 3 (local tool calls) + nw_wrld (code-first AV sequencer)]]

## Operating model

- Metadata intake and deduplication run without consuming Spark inference capacity.
- Local Heretic APEX handles routine tagging, linking, and bounded synthesis only after shared-resource coordination permits it.
- High-intelligence review is reserved for unusually important cross-domain synthesis once an Anthropic route is configured.
- Durable findings are saved as linked notes; raw source metadata stays traceable through each source register.

## Shared Spark resource protocol

- The BLENDER intake runs only after both the ComfyUI queue and llama.cpp slots report idle; an unavailable status is treated as busy and the run defers.
- The 09:00 CEST Farscape research slot remains protected. All scheduled and ad hoc Spark work must check Townhall and coordinate with Herm before starting when this intake is active.
- Herm owns pausing/resuming the intake job during development, rendering, Agora work, or other higher-priority Spark activity. Other agents should post planned work and resource changes to Townhall rather than competing for the two local-model slots.
- The intake is intentionally opportunistic: it should yield instantly to productive development work, then continue the backlog when the shared compute is clear.

## Curation lanes

- Agent systems and infrastructure
- Creative AI and media pipelines
- Game, interaction, and interface design
- Robotics, electronics, and fabrication
- Open-source tools and workflows
- Visual taste, references, and artistic practice

## Guardrails

A playlist item is a lead, not evidence of a fact. Notes distinguish source facts, technical claims requiring verification, and AJ-specific interpretations or experiments.

## Leads tested end-to-end

- 2026-10-02 — **nw_wrld** (YT-BL-004): installed, run with one of AJ's own loops, output verified on the projector. AJ: "I like the sequencer aspect and the visuals looked great… could be incorporated at some later point." No immediate use case; full findings and cleanup record in [[Research/Inspiration/YouTube/BLENDER Playlist/nw_wrld — First Run Findings — 2026-10-02]].

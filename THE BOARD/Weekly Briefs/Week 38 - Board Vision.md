---
tags: [governance/board, type/vision-brief]
status: filed
origin: board-vision
authored_by: AJ (CEO, standing in for the Board — role not yet built)
addressed_to: Senior Product Manager
created: 2026-09-09
filed: 2026-09-09
week: Week 38
supersedes_scope: "Excludes FR-002 and improvements Phase D — see deferral notes on those items"
---

# Board Vision — Week 38: Beyond the Foundation

## What this is

This is the Board's next-sprint vision document, filed to `THE BOARD/Weekly
Briefs/Week 38` per standing process. The Board role itself isn't built yet,
so I (AJ) am producing it directly, as agreed when this process was stood up.
Once the Board exists, this document type is its deliverable, not mine — but
until then, this is the mechanism, and it carries the same weight.

**Senior Product Manager:** mature this into work orders (vision / goal /
success metric, per your template) and promote what's ripe into `Backlog`
root, same as if a Board had produced it. Where a section below is already
concrete enough to skip straight to Scrummaster-level detail, let Scrummaster
add acceptance criteria and implementation notes when it matures — don't
treat the density here as a substitute for that step.

## Where we stand

Sprint 1 (Week 37) closed out the baseline: all twelve original QA bugs
fixed, and Phases A through C of `[[improvements]]` shipped (FR-001,
FR-003–FR-008). That was table stakes — UX debt and stability the project
needed regardless of where it goes next. It's done. This document is about
what comes after it.

**Explicitly out of scope for now:** `FR-002` (Spark llama.cpp parallel
slots) and `[[improvements]]` Phase D (full-duplex voice, GPU telemetry,
persona visual consistency) stay parked at their current status. Don't
auto-carry them into the sprints this vision opens up — both already carry a
CEO-deferral note on the item itself. They, plus the Phase 4 persistent-memory
blocker (mem0 + FalkorDB — still blocked on Docker/Podman not being
installed), are earmarked for a dedicated future **Foundation Sprint**, called
separately when it's time.

## Why this matters now

Agora has been a solo prototype up to this point — proving out one piece at a
time, verified against real hardware, built by AJ working through this same
agent pipeline. That phase is over. What we build from here on is meant to be
the foundation of something bigger: possibly an open-source release, possibly
a commercial product, possibly both at different points. We don't have to
commit to which today. What we do have to do is stop building
proof-of-concept features and start building the thing that foundation
actually needs — a real architecture for how personas, scenes, and worlds
relate to each other, a media pipeline that produces something a user
actually wants to keep, and honest data on whether any of this lands with a
user who isn't AJ. Every initiative below is in service of that shift: from
"does the capability exist" to "does the product hold together."

It's still early days. The brief is to push the envelope as far as it goes,
not to ship a v1. But "early days" is exactly when the architectural bets
below are cheapest to make — the later this happens, the more it costs to
unwind.

## The vision

### 1. Worlds & Scenes — the architectural bet

Rooms, as they exist today, are a flat and disposable container: one
conversation, no persistence beyond it, no relationship between one room and
the next. That model doesn't support what we actually want, which is
personas — and the bonds between them and the user — that deepen the longer
they interact, across many sessions, not just within one.

Direction: rooms are superseded by **Scenes**, nested inside **Worlds**.
Plenty of single-scene, single-room use will remain — that's not going away.
But a World is a curated, persistent setting a user can root their personas
in: a place with continuity, populated dynamically with situational NPCs as
needed, where a series of scenes can accumulate shared memory and history
between the same characters over time. This is the single biggest structural
change in this vision and effectively supersedes the old "narrator/roleplay
room" framing from the original PRD — it's the same idea, scoped much larger.
Persona memory (already shipped) and the trait-evolution engine both plug
directly into this: a persona's traits and memories should be able to carry
and evolve across an entire World's scene history, not reset per room.

The end goal, stated plainly: personas that feel alive — full agency,
character, and flaws that evolve the longer they interact, with the user and
with each other, not just scripted responses inside a single conversation.

### 2. Narrator intelligence

The Narrator concept needs to grow well past where it started. Today's
narrator tooling is thin; it needs real judgment about pacing — when to push
a scene forward versus let it breathe — and that judgment needs to be
configurable per World or per Narrator persona, not a fixed behavior. This is
a prerequisite for Worlds & Scenes to feel good to use rather than
mechanical; treat it as coupled work, not a separate initiative that can trail
behind.

### 3. Scene media & the studio

Media generation needs to become part of how a scene is experienced and kept,
not a side action. Within a scene, a user should be able to request a
ComfyUI-generated image from any character's point of view, or from third
person, through an easy, configurable interaction — not a raw prompt box.
When a scene ends, a user should be able to request a video recreation of it,
delivered into an editor interface rather than dropped as a raw file. On
voice: LTX generates usable voices already; we'll also experiment with Fish
TTS's stronger voice-acting characteristics for scene narration and
dialogue, and compare rather than assume one wins outright.

Over time this accumulates into a per-user, editable **media library** —
images, video, and rendered TTS audio from a person's own sessions, tied to
the Worlds and scenes that produced them — that should be remixable in an
interaction paradigm that's intuitive but genuinely comprehensive, not a
bolt-on gallery. This is a multi-sprint arc, not a single feature; expect it
to mature in layers (generation → library → editing).

### 4. Flexible generation workflows

The app should be able to point at arbitrary ComfyUI workflows — run by the
Narrator/agent directly, or triggered through the chat interface — with
dynamically loaded, user-configurable input parameters, rather than the
current hardcoded template approach. AJ has a working collection of
image and video workflows from other projects to seed testing with. Expect
this to converge, not stay open-ended: the direction is to test broadly
against that existing collection and narrow down to a small, well-understood
set of canonical image and video workflows once we know what's actually
worth keeping.

### 5. Onboarding — configuration wizards

This is the accessibility half of "push capabilities further and make them
more accessible." Every persona/World/Narrator setting should remain fully
editable at full depth in its own profile — nothing here is about reducing
capability. But the entry point to that depth should be a **Quick Start
wizard**: a guided configuration path that gets someone to a working
persona/scene fast, with the full-detail editor still there underneath for
when they want it. Low-dependency, UI-primarily work — a good candidate to
run in parallel with the heavier architectural initiatives above rather than
queued behind them.

### 6. Validating the experience

Before any of this goes in front of a user who isn't AJ, we need real
evidence that the experience holds up — not just that features work in
isolation. Direction: develop structured test scenarios the Senior QA
Manager can run as simulated user behavior — not just functional QA passes —
to gather interaction and analytics-style metrics on how a scene, a World, or
a media request actually plays out end to end. This should stand up early
relative to the other initiatives, since it's the gate between "internal
prototype" and "opened up for public testing," and the earlier we have real
signal, the less the later initiatives are built on guesses about what feels
good.

### 7. Farscape World — the flagship pilot

Rather than build Worlds & Scenes, Narrator intelligence, and the media
studio in the abstract, the first concrete target is a real one: a
**Farscape-themed World**. Build a local Farscape wiki inside the Obsidian
vault — characters, world/canon information, reference images, and cleaned
voice samples for cloning (candidate sources: the Farscape Encyclopedia
fandom wiki and Wikipedia's Farscape article — both worth a research pass
before content work starts). AJ can clean reference audio manually today;
the eventual goal is a Fish voice-cloning pipeline that pulls, annotates, and
cleans character voices from source video automatically, but that's a stretch
target, not a precondition — start with manually prepared voices and don't
block the pilot on the automation existing first.

Treat Farscape as the forcing function that exercises initiatives 1–4 at
once, in a bounded, well-understood setting, rather than a separate feature
request.

### 8. Brand

"Agora" and "Agentic Chatroom Project" won't carry this toward either an
open-source community or a commercial product — neither name says what the
thing is. A rebrand is coming; the direction is to do it **early**,
deliberately, precisely to minimize how much later sprint work (docs, code
comments, published-feature writeups, this vault's own naming) has to be
touched or reconciled after the fact. This doesn't need to block the
initiatives above, but don't let it drift indefinitely either — flag it for
early scoping rather than treating it as someday-work.

## Sequencing guidance

Not a sprint plan — that's the Senior Product Manager's and Scrummaster's job
once this is matured. But for packing order:

| Initiative | Dependency shape |
|---|---|
| Worlds & Scenes (1) + Narrator intelligence (2) | Foundational — most other initiatives build on this data model and behavior |
| Scene media & studio (3) | Benefits from 1–2 existing, but generation-side work (POV image requests) can start in parallel |
| Flexible generation workflows (4) | Largely independent; can run alongside anything |
| Onboarding wizards (5) | Independent, UI-only — good parallel-track filler |
| Validating the experience (6) | Should stand up early, not trail — it's the gate to public testing, not a wrap-up step |
| Farscape World (7) | Depends on 1–4 having enough surface area to be worth piloting against; treat as an integration milestone, not day-one work |
| Rebrand (8) | Time-boxed and early, independent of the above, but don't let it drift |

## Handoff

Per current process: this document is handed to the Senior Product Manager,
who matures it into work orders and promotes ripe ones into `Backlog` root
for the Scrummaster to turn into SMART stories. Execution proceeds as normal
— coding agents via Hermes, running in parallel lanes, the pattern that
worked well in Sprint 1. This stands in for the Board's weekly cycle until
that role is actually built; once it is, this same slot is where its output
belongs instead.

## Related

- [[GOAL]] — current north-star pointer; updated to reference this document.
- [[Agentic Chatroom]] — current-state snapshot; Feature Development pipeline section updated to reference this document.
- [[improvements]] — Phases A–C (shipped) and Phase D (parked, see deferral note) that this vision builds on and beyond.
- [[Agenti Chatroom long term]] — original founding vision doc; the Worlds & Scenes framing above supersedes its room-scoped narrator/roleplay section.
- [[NOTES]] — running technical session log.
- `Feature Development/Project Team/Senior Product Manager.md` — Loop 1 process this document feeds.
- [[Notes on Vision]] — AJ's raw CEO-office notes this Board Vision was drafted from (Worlds & Scenes, Narrator, media studio, Farscape pilot, rebrand).
- [[Week 38 - Scrummaster friction notes]] — this week's downstream Scrummaster maturation run against this vision.
- [[Week 37 - Senior PM metrics]] — Sprint 1 (Week 37) throughput/quality metrics preceding this vision doc.

---
tags: [project/agora, status/archived, type/backlog]
status: promoted-to-backlog
origin: board-vision
source: "[[Week 38 - Board Vision]]"
created: 2026-09-10
authored_by: Senior Product Manager
matured_into: "[[FR-015-experience-validation-scenarios]]"
---

# Validating the experience

## Vision
Before any of this goes in front of a user who isn't AJ, the Board wants
real evidence the experience holds up end to end — not just that features
work in isolation. Direction: structured test scenarios the Senior QA
Manager can run as simulated user behavior, gathering interaction and
analytics-style metrics on how a scene, a World, or a media request
actually plays out. This should stand up early — it's the gate between
"internal prototype" and "opened up for public testing," not a wrap-up
step.

## Goal
A set of structured, repeatable simulated-user test scenarios — distinct
from ordinary functional QA bug-hunting — that the Senior QA Manager can
run against Worlds/Scenes/media features to produce interaction and
analytics-style metrics rather than a pass/fail bug list.

## Success metric
Senior QA Manager runs at least one structured scenario end to end and
produces a metrics writeup (not just a bug list) usable by the Board/PM to
judge experience quality, not code correctness.

## Non-goals
Explicitly excludes the **Farscape World** pilot itself (test-scenario
content built around Farscape characters/wiki/voices) — that stays a
separate, not-yet-promoted item pending its own research pass and QA
department scoping. Don't fold Farscape content into this work order.

## Matured
This work order matured into `[[FR-015-experience-validation-scenarios]]`
on 2026-09-10 by the Scrummaster — see that story for acceptance criteria,
implementation notes, and definition of done.

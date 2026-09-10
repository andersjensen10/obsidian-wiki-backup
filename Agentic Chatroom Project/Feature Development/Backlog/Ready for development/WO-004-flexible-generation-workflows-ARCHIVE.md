---
tags: [project/agora, status/archived, type/backlog]
status: matured
origin: board-vision
source: "[[Week 38 - Board Vision]]"
created: 2026-09-10
authored_by: Senior Product Manager
---

> **ARCHIVED & MATURED:** 2026-09-10 by Scrummaster.
> This work order has been matured into the SMART story
> [[FR-013-flexible-comfyui-workflows]] — Flexible ComfyUI Workflow Import
> & Parameter Exposure, filed alongside this archive in
> `Backlog/Ready for development`.

---

# Flexible generation workflows

## Vision
The app should be able to point at arbitrary ComfyUI workflows — run by the
Narrator/agent directly or triggered through chat — with dynamically
loaded, user-configurable input parameters, replacing today's hardcoded
template approach. AJ has an existing collection of image and video
workflows from other projects to seed testing; the Board expects this to
converge over time to a small, well-understood canonical set rather than
stay open-ended.

## Goal
A mechanism to load an arbitrary ComfyUI workflow file and expose its
inputs as user-configurable parameters inside the app, runnable both by the
Narrator/agent and via the chat interface.

## Success metric
At least two of AJ's existing workflows (one image, one video) run
end-to-end through this mechanism with user-adjustable parameters,
verified live.

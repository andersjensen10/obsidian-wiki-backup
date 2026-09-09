---
purpose: template-metadata
---

# About this folder

This folder is the working scaffold for **Axiom Engine**, built by copying and
genericizing the pipeline that runs `Agentic Chatroom Project` — same three
agent roles (Scrummaster, Senior Product Manager, Senior QA Manager), same
weekly Board cadence, same reporting destination (`THE BOARD`, shared across
the portfolio, same CEO). Nothing here is Axiom-Engine-specific content yet:
the role prompts, run logs, and folder structure are the process; you fill in
the actual vision, backlog, and technical detail as the project gets going.

It also doubles as the reusable pattern for whichever project comes after
this one. To onboard a future project the same way:

1. Copy this whole folder to `<New Project Name> Project`.
2. Find-and-replace `Axiom Engine` → `<New Project Name>` across every file
   (role prompts, `GOAL.md`, the status-snapshot page, the Overview page).
3. Fill in `Axiom Engine.md` → `<New Project Name>.md` with the new project's
   actual stack, infra, and status once that's known.
4. Leave the run logs, `Requests from the board.md`, and the Backlog/QA
   subfolders empty — they populate themselves as the pipeline runs.
5. Nothing under `THE BOARD` needs copying — every project in the portfolio
   reports into that same shared structure, per-project-qualified filenames
   (see the Project Team prompts for the exact convention).

## What was intentionally left out of this copy

- `NOTES.md`, `Axiom Engine.md`, `GOAL.md`, and `Feature Requests/
  improvements.md` are fresh templates, not copies of Agora's — that content
  was project history/data, not process.
- `Published features/Legacy`, `Published features/Sprint 1 - Week 37`,
  and every real backlog/bug/work-order file were Agora's actual shipped
  history — none of that is scaffolding, so none of it was copied.
- `THE BOARD` itself wasn't duplicated — it's shared across the whole
  portfolio, same Board, same CEO (AJ). Both projects file into the one
  copy that already exists.

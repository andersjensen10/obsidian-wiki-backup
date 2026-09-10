---
tags: [scratch]
---

# Agora — Instructions for Finishing a Story

## Where things live
- Code repo: /home/aj/Desktop/Hermes/AgenticChatroomProject
- Story files (Obsidian vault): .../Obsidian Wiki/Obsidian Wiki/Agentic Chatroom Project/
  Feature Development/Backlog/Active Sprint/

Only work stories sitting in `Backlog/Active Sprint`. Never create, rename, move,
or delete files in `Ready for development`, `Open BUGS`, `Hypercare`, or
`Published features` — those are moved automatically by other agents once you
flip a status field. Touching them yourself will break that automation.

## Before you start a story
Read the whole file, not just the title:
- `## Acceptance criteria` — what must be true when you're done
- `## Implementation notes` — pointers to relevant files/patterns/gotchas
- `## Non-goals` — explicitly out of scope, don't over-build
- `## Definition of done` — the exact commands/scripts that must pass.
  Run them for real (e.g. `npm run verify`, a named `scripts/live-*-check.mjs`)
  — don't mark something done on the basis of "it should work."

## Finishing a story
1. Confirm every acceptance criterion is met and the Definition of Done
   commands actually pass.
2. Run the self-evaluation loop below. Only once it clears do you flip status.
3. Edit the story file's frontmatter and change exactly one field:
   status: shipped
   That flip is the only signal downstream agents watch for — nothing else
   about the file needs to change.
4. Leave the file where it is, still in `Active Sprint`. Do not rename it,
   move it, or touch its `FR-###` / `BUG-###` number — Scrummaster picks up
   the `shipped` flip on its own and moves the file into `Hypercare` for you.
5. Don't write into `Published features`, `THE BOARD`, or any
   `_*Run Log.md` file — those are other agents' territory.

## Naming conventions (reference — you never assign these yourself)
- Feature stories:  FR-<3-digit>-<slug>.md
- Bug stories:       BUG-<3-digit>-<slug>.md
- Work orders:       WO-<3-digit>-<slug>.md
- Archived source:   <original-name>-ARCHIVE.md

## Story frontmatter you'll see
---
status: ready-for-development   # → change to "shipped" when live, nothing else
origin: feature-request | bug | board-request | user-feedback
source: "[[...]]"
criticality: {impact: low|medium|high, urgency: low|medium|high}
size: S | M | L
dependencies: []
matured: YYYY-MM-DD
matured_by: Scrummaster
---

## Hard rules
- Use subagents / fork for discrete parts of the work.
- Never flip `status: shipped` unless the Definition of Done actually passed
  — a false positive rides straight into the next sprint's Hypercare window
  as a live regression.
- If a story turns out ambiguous or blocked once you're in it, don't guess —
  leave it as-is and flag it back to AJ rather than shipping a wrong
  interpretation.

## Self-evaluation loop (required before shipping)
Before flipping `status: shipped`, score your own solution 1–10 against the
story's `## Context` and `## User story` / `## Bug` statement — not "are the
acceptance-criteria boxes checked" but "does this actually deliver what was
asked, well." Write one or two sentences of reasoning plus the number.

- **Score ≥ 8** → proceed to ship.
- **Score < 8** → don't ship. Name the specific gap, refactor, re-run the
  Definition of Done checks, and re-score. Repeat.
- **Still < 8 after 3 refactor passes** → stop looping. The story itself is
  probably unclear or unshippable as scoped — flag it back to AJ instead of
  grinding indefinitely.
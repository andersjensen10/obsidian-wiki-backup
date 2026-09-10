---
tags: [project/axiom-engine, type/backlog]
status: ready
type: chore
---

# Reconcile Axiom Engine repo state and decide what survives

## Context

Axiom Engine (AJ's Operations Console / "Playground", `~/playground` on
`axiom-engine`) stalled ~2 months ago mid-hardening of the in-house Ralph
Loop coding agent. Recon (2026-09-09, see [[NOTES]] and [[Axiom Engine]])
found the app is still deployed and running healthily — nothing
crashed — but local git is 61 commits ahead of `origin/main`, and the repo
carries ~30 planning docs plus a large, only-partially-finished Ralph Loop
implementation that AJ now wants to look at with fresh eyes ("bloated and
clunky but a lot of concepts worth exploring further").

This story is the first concrete piece of work before any new feature
development starts.

## Goal

Get the repo and AJ (+ the coding agent(s) that will work on it) into a
known-good, low-risk starting position, and produce an honest assessment of
what in the current Ralph Loop / Jobs engine is worth keeping vs.
rebuilding vs. dropping.

## Tasks

1. Push the 61 unpushed local commits to `origin/main` (or branch off
   first if AJ wants review before merging to main) so hardened Ralph work
   isn't stranded on one machine.
2. Run the existing verify gate (`npm test`, `npm run e2e`) on
   `axiom-engine` and record pass/fail — establish an honest current
   baseline before touching anything.
3. Read through `docs/ralph-loop-delivery-baseline-2026-06-10.md` and
   `TODO.md` in full and produce a short assessment: which P1/P2 items are
   still worth pursuing, which are over-engineered for AJ's actual use
   case, what the "Ralph Loop" concept should become given what AJ has
   learned about agentic coding since (compare against how Hermes/Claude
   Code and the `agora-chatroom` pipeline actually work day to day).
4. Decide scope: is Axiom Engine's Ralph Loop meant to become a
   general-purpose autonomous coding agent (competing with Claude
   Code/Codex), or a narrower automation primitive inside the Jobs engine?
   This materially changes what's worth finishing.
5. Once scope is decided, write the actual `[[improvements]]` long-term
   blueprint (currently a stub) and set `[[GOAL]]`'s north star.

## Definition of done

- `origin/main` matches local `main` (or a reviewed branch exists).
- Verify-gate results recorded in `[[NOTES]]`.
- A written assessment exists (this doc or a new one) covering task 3-4.
- `[[improvements]]` and `[[GOAL]]` are no longer stub templates.

## Notes

This is scaffolding work, not a sprint story from the Board — filed
directly by AJ/Herm per his ask to "get familiarized with the state of the
project and get the corresponding folder structure in the vault
populated."

## Related notes
- [[Axiom Engine]] — project status snapshot this story feeds.
- [[NOTES]] — running session log with the recon that produced this story.
- [[Getting the Axiom Engine back in action]] — AJ's CEO-office ask that started this.

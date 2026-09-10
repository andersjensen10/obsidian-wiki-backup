---
tags: [project/agora]
story: "[[FR-002-spark-llamacpp-parallel-slots]]"
date: 2026-09-09
author: AJ
status: report
---

# FR-002 Report — llama.cpp Parallel Slots on Spark

## Method

- **Target:** Spark's llama.cpp service (`192.168.0.139:8014`), config file
  `~/.config/llama-server.env` on the Spark, managed via `llama-server.service`
  (systemd).
- **Prerequisite unblocked first:** laptop's SSH public key added to
  `~/.ssh/authorized_keys` on the Spark — `ssh spark` (host alias) now logs in
  non-interactively. This had been the standing blocker on FR-002's
  `dependencies` field.
- **Config change:** `PARALLEL=1→2`, `CTX_SIZE=65536→100000` (50k tokens/slot),
  applied in the same edit so the reasoning model keeps a generous per-slot
  context budget rather than being starved by splitting the old 64k ceiling
  across slots.
- **Restart + verification:** `llama-server.service` restarted; confirmed live
  via `GET /v1/models`-equivalent status check showing `total_slots=2`.
- **Concurrency proof:** a real (not simulated) 2-request test fired
  simultaneously against the endpoint and confirmed both streamed
  concurrently rather than queueing strictly one after the other.
- **Memory check:** VRAM/RAM headroom checked at the new setting — 33GB free
  at 2 slots × 100k ctx.
- **Rollback:** prior config backed up to
  `~/.config/llama-server.env.bak-fr002` on the Spark before the change, so a
  revert is a one-line copy-back if the new setting ever causes trouble.

## Result vs. original scope

The story's acceptance criteria targeted "4 to 10 slots depending on VRAM
headroom." Shipped scope is **2 slots**, deliberately — see the Resolution
note on the story for the reasoning (context-budget-per-slot tradeoff, chosen
against measured headroom rather than the pre-verification estimate the story
was written against). This unblocks the original problem (multi-persona
scenes serializing on a single generation slot) and parallel subagent calls;
it does not chase the top of the originally-imagined range.

## Verification summary

| Check | Result |
|---|---|
| SSH non-interactive (`ssh spark`) | ✅ works |
| `total_slots` reported by the service | ✅ `2` |
| Concurrent 2-request test | ✅ genuine concurrent streaming confirmed |
| Memory headroom at 2 slots × 100k ctx | ✅ 33GB free |
| Rollback path | ✅ `~/.config/llama-server.env.bak-fr002` on Spark |

## Follow-on

Room for a 3rd slot later if more concurrency is wanted. Not pursued now —
would need a fresh headroom check at that setting before committing, since
33GB free at 2 slots isn't automatically 3-slot-safe (larger per-slot context
would need to shrink, or headroom would shrink further).

## Documentation updated

- [[FR-002-spark-llamacpp-parallel-slots]] — frontmatter flipped to `shipped`,
  acceptance criteria and definition of done checked off, resolution noted.
- [[LAN notes]] — Spark service table (SSH now authorised), active-model
  section (slot count, context size, headroom) brought current.
- The `home-lab-infrastructure` Hermes skill inventory (source of truth this
  Obsidian page summarizes) was updated directly on the Spark session — see
  that skill for the authoritative low-level detail.

## Related notes
- [[FR-002-spark-llamacpp-parallel-slots]] — the hypercare story this report closes out.
- [[LAN notes]] — Spark parallel-slots facts this report feeds.
- [[Agentic Chatroom]] — project status snapshot.

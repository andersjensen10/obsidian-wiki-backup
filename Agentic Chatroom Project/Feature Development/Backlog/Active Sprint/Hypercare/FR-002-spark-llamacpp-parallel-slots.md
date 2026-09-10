---
tags: [project/agora, type/hypercare]
status: hypercare
origin: feature-request
source: "[[Next Level Agentic Chatroom Project-ARCHIVE]]"
criticality:
  impact: high
  urgency: high
size: S
dependencies:
  - "SSH on Spark (AJ console access to authorize laptop key)"
matured: 2026-09-08
matured_by: Scrummaster
hypercare_since: 2026-09-10
---

> [!note] CEO deferral — 2026-09-09 (superseded same day, see below)
> Kept at `status: ready-for-development` deliberately — do not auto-carry into the
> next sprint pack. AJ has scoped the upcoming sprint(s) to next-level features and
> UX accessibility work instead (see the Board vision doc once filed). This story is
> earmarked for a dedicated future **Foundation Sprint** alongside the Phase D items
> parked in [[improvements]] and the Phase 4 persistent-memory blocker. Senior
> Product Manager: exclude from Loop 2 packing until that Foundation Sprint is
> called.

> [!success] Shipped ad hoc — 2026-09-09
> AJ did the SSH + systemd work directly the same day, outside the formal sprint
> process the deferral note above was written for — it turned out to be a
> ~10-minute admin task, not something that needed a coding-agent sprint slot.
> The deferral's intent (don't spend a Foundation Sprint slot maturing/packing
> this) still holds; only the "leave it parked" framing is superseded. Full
> results in [[FR-002-spark-llamacpp-parallel-slots-REPORT]].

# Raise llama.cpp Parallel Slots on Spark for Concurrent Generation

## Context
Extracted from [[Next Level Agentic Chatroom Project-ARCHIVE]] (Priority: P0). Currently `llama.cpp` on the Spark AI box (`192.168.0.139:8014`) runs with a single generation slot (`--parallel 1`). Any multi-persona scene in Agora serializes every persona turn, causing severe latency bottlenecks during multi-character debates and banter. Getting SSH authorized on the Spark and bumping `--parallel` unblocks concurrent generation for Agora and parallel subagent calls. Criticality is High/High as it bottlenecks overall system throughput.

## User story
As a developer and user of Agora, I want the llama.cpp server on the Spark configured with multiple parallel slots (e.g. `--parallel 4` or `--parallel 10`), so that multi-persona rooms can generate turns concurrently without queue starvation.

## Acceptance criteria
- [x] Laptop SSH public key is added to `~/.ssh/authorized_keys` on the Spark (192.168.0.139) to enable remote maintenance. — `ssh spark` works non-interactively.
- [x] Spark llama.cpp systemd service or launch configuration is updated to set `--parallel`. — Shipped at **2 slots** (`PARALLEL=1→2`), not the 4–10 originally targeted; `CTX_SIZE` raised `65536→100000` alongside it (50k tokens/slot) as the deliberate tradeoff — see Resolution note below.
- [x] Service is restarted and verified responsive via `GET http://192.168.0.139:8014/v1/models`. — confirmed live, `total_slots=2`.
- [x] A concurrent test script fires at least 2 simultaneous completions and verifies both stream concurrently rather than strictly queueing sequentially. — real 2-request test confirmed genuine concurrent processing.

## Implementation notes
- See [[LAN notes]] for Spark hardware details and IP configuration (`192.168.0.139`).
- Spark "flaps" on ICMP/ping (now on living room Wi-Fi); always verify service status via HTTP requests to `:8014`, not `ping`.
- Check VRAM consumption with `nvidia-smi` on Spark to ensure context memory across concurrent slots does not trigger CUDA OOM on the 27B model.

## Non-goals
- Changing the inference model or quant format.
- Modifying Agora server-side client connection logic (Agora already speaks standard OpenAI-compatible completions).

## Definition of done
- [x] SSH login from laptop to Spark succeeds non-interactively (`ssh spark`).
- [x] Concurrent completion probe returns non-blocking responses across 2+ simultaneous streams.
- [x] Status and slot count verified and documented in [[LAN notes]].

## Resolution — 2026-09-09
- `llama-server.service` reconfigured: `PARALLEL=1→2`, `CTX_SIZE=65536→100000` (50k
  tokens/slot). 2 slots chosen over the originally-targeted 4–10 to keep a generous
  per-slot context budget for reasoning-model chain-of-thought, given the VRAM
  headroom actually measured (33GB free at 2 slots) — raising slot count further
  would mean either shrinking per-slot context or eating into that headroom.
- Verified live: `total_slots=2`; a real (not simulated) 2-request concurrent test
  confirmed genuine concurrent processing, not serialized queueing.
- Rollback available at `~/.config/llama-server.env.bak-fr002` on the Spark if
  needed.
- Full method/results: [[FR-002-spark-llamacpp-parallel-slots-REPORT]].
- Slot count and config documented in [[LAN notes]].
- Room for a 3rd slot later if more concurrency is wanted — retest against
  memory headroom at that time before committing.

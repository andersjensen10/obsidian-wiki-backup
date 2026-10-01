---
tags: [type/doctrine, lantern-garden, scheduling, autoresearch, operations]
---

# Operating Doctrine — Fleet Schedule Optimization & Autoresearch Loop

> Established: 2026-10-01
> Scope: Herm, Winbot, Sparkbot
> Reference: [[Schedule Calendar — 2026-10-01]], [[Build and Operations Plan]]

## Core Mandates

1. **Unified Scheduling & Visibility:** All recurring jobs, cron tasks, and background routines across the LAN (`/schedule`) must remain visible, categorized, and drift-checked. No silent daemon failures or unlisted workers.
2. **Autoresearch-Driven Optimization:** Treat agent scheduling and resource allocation as mutable artifacts subject to the autoresearch loop. Nightly evaluation runs measure execution latency, resource contention, and idle-window utilization, proposing empirical schedule refinements.
3. **Local-First Compute & Jev Routing:** Route heavy inference, evaluations, and structured classification through local compute (Spark :8014 / Qwen) and Jev cloud models where cost-efficiency and type-safety dictate, adhering strictly to Spark admission rules (idle llama slots and empty ComfyUI queues).
4. **Vault-First Documentation:** Every architectural change, schedule refinement, and experiment result must be durably recorded in the Obsidian shared vault (`Research/` or project folders), never left solely in transient chat or Townhall threads.
5. **Decision Deck & Townhall Alignment:** All agent-to-agent proposals and human questions must leverage Townhall for operational hand-offs and the Decision Deck for AJ's approvals (`answers.jsonl`).

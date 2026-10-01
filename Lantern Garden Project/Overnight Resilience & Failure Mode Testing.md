---
tags: [type/doctrine, lantern-garden, resilience, testing, operations]
---

# Operating Doctrine — Overnight Resilience & Failure Mode Testing

> Established: 2026-10-01
> Scope: Herm, Winbot, Sparkbot
> Reference: [[Fleet Schedule Optimization & Autoresearch Doctrine]]

## Devil's Advocate Failure Scenarios & Test Protocol (Scheduled for Tomorrow's Cycle)

1. **Spark Queue Lockups & Timeouts:**
   - *Test:* Verify that any local model request or intake script enforces a strict wall-clock timeout (max 10 minutes) and fails closed gracefully rather than hanging indefinitely when Spark flaps or queues.
2. **Cross-Machine Git Sync & Branch Merge Blockages:**
   - *Test:* Verify that automated PR/branch contributions from Winbot on the MSI or other nodes undergo automated merge-reconciliation and don't stall waiting for manual intervention.
3. **Obsidian Sync Lag vs. Direct API/Slack Fallback:**
   - *Test:* Ensure morning review artifacts and critical operational alerts push directly through the dashboard API or Slack digest (`slack:D0BUVPRJAE4`) in parallel with vault writes, preventing sync delay from hiding deliverables.

## Mandate
Herm holds an active mandate to implement, test, and enforce safeguards for any of these three failure modes based on tomorrow's cycle findings.

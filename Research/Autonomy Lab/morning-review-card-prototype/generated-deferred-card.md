---
type: morning-review-card
missionId: spark-mission-deferred
selectedAt: 2026-09-30T02:15:30+02:00
status: deferred
resourceClass: spark
---

# Morning Review Card — spark-mission-deferred

**Status:** DEFERRED  
**Selected:** 2026-09-30T02:15:30+02:00  
**Resource class:** spark

## Hypothesis
A Spark task must defer when admission is unavailable.

## Why this was selected
- Townhall Spark reservation policy

## Resource admission
- **State:** busy
- **Evidence:** Fixture simulates a running ComfyUI job.
- **Yield rule:** Yield to interactive work; retry only on a future scheduled cycle after a fresh idle check.

## Sandbox and rollback
- **Boundary:** Fixture only; no Spark request is sent.
- **Rollback:** Delete the fixture; no service state changed.

## Measurable signals
- rendered status is DEFERRED

## Evidence paths
- morning-review-card-prototype/fixtures/busy-spark.json

## Promotion decision
deferred

## Morning question
**Should this deferred mission be reconsidered when Spark is idle?**

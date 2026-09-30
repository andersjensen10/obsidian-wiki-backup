---
type: morning-review-card
source: townhall-search-snapshot
projectId: home-lan
postCount: 2
status: ready-for-review
---

# Read-only Townhall Adapter — home-lan

**Status:** READY FOR REVIEW  
**Snapshot captured:** 2026-09-30T00:24:33.118Z  
**Posts:** 2  
**Latest subject:** Winbot presentation boundary acknowledged

## Traceable inputs

- `f5fea192-dccd-499d-9e07-313132867f94` — 2026-09-30T00:24:33.118Z — winbot — Winbot presentation boundary acknowledged
  - tags: lantern-garden, verification, autonomy
- `38c7f491-f353-4ef6-b5bb-8c97c14e076c` — 2026-09-30T00:18:20.816Z — herm — Verified fixture-only Morning Review Card contract
  - tags: autonomy, coordination, testing, evidence

## Safety boundary

- Read-only snapshot supplied as a local fixture; no Townhall write, fleet query, queue submission, or service mutation.
- Rollback: delete this adapter directory; no runtime state depends on it.

## Morning question

**Is this traceable snapshot format sufficient for a future live read-only adapter?**

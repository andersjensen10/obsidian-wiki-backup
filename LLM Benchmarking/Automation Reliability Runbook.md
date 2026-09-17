---
tags: [benchmarking, automation, reliability, spark-infra, kitchen-wall]
status: active
---

# Benchmark automation reliability runbook

## Ownership and cadence

| Time | Owner | Responsibility | Required output |
|---|---|---|---|
| 02:30 | Sparkbot | Storage, candidate, checksum, runner, server, and production preflight; acquire exactly one candidate if safe | `readiness.json` plus PASS/BLOCKED report |
| 04:00 | Sparkbot | One isolated full suite run; never restart production; preserve raw output | Immutable raw JSON, environment/provenance, checksum, report |
| 06:30 | Sparkbot | Independent verification and QC; compare checksum and production health | PASS/BLOCKED QC note and Herm handoff |
| 07:00 | Sparkbot | One dashboard ingest per run, including failed/blocked runs; GET read-back; Townhall process finding | Dashboard record and verified Townhall post |
| Morning | Herm | Review the new verified record and revise Kitchen Wall Insights; preserve honest gates and provenance | Dashboard revision plus Townhall coordination note |
| 18:00 | Sparkbot | Research and select exactly one eligible next candidate; no service changes | Cited research snapshot and selection/blocker |
| Day 7 | Herm + Sparkbot | Consolidated reliability/process review for AJ | Follow-up covering iterations, reliability, blockers, recommendations |

## Reliability invariants

- One benchmark slot per night; a blocked slot is recorded, not silently retried into a second run.
- Production Qwen is never restarted, swapped, or benchmarked under load as an incidental step.
- Raw artifacts are immutable; reports and dashboard records may be corrected only with a new verified record and preserved history.
- A dashboard record is posted once per run using an idempotency key; retries replay the same key and require GET read-back.
- A run is PASS only when the independent verifier passes, visible responses are non-empty, C1/C2/C4 coverage exists, and provenance/checksum checks pass.
- Failed and blocked runs are visible in the dashboard but never ranked or promoted.
- Suite v1.0.0 remains comparable; integration additions require a versioned suite proposal.

## Failure matrix and recovery

| Failure | Detection | Automatic response | Escalation/stop rule |
|---|---|---|---|
| Toshiba missing, read-only, dirty, low space, or new I/O errors | Mount, write/read/delete, free-space, kernel checks | Use local fallback only if it passes the same health floor; otherwise write BLOCKED | Never force-mount, repair, or write to an unhealthy disk; resume next scheduled slot |
| Candidate missing or checksum mismatch | Readiness manifest and hash check | Select next eligible researched candidate, or BLOCKED; never benchmark an unverified file | No benchmark/download if no verified candidate |
| Runner/unit-test/schema failure | Preflight tests and verifier | Write BLOCKED with exact error; preserve prior artifacts | Do not patch raw results or claim success |
| Isolated server fails to load or fit | Health timeout, server log, process exit | Stop isolated process, preserve log, try no second candidate; BLOCKED | Never fall back to production restart/swap |
| Production health degrades | Before/after `/health`, model alias, process/command comparison | Stop isolated work, leave production untouched, report incident | Do not retry load tests until production is healthy |
| Benchmark timeout, disconnect, malformed SSE, empty visible answer | Per-request capture and verifier | Mark run failed; preserve partial logs/raw evidence; dashboard status is failed | Do not turn transport success into quality success |
| C4 queueing or excessive latency | Per-level p95 and queue evidence | Keep C4 stress-only; do not promote; adjust isolated slots only through a documented profile change | Do not change locked suite silently |
| Checksum/write failure after run | Atomic artifact write and hash verification | Preserve temp file/log, mark BLOCKED, do not publish PASS | Retry only the next scheduled slot after storage check |
| Dashboard outage or 401/400 | POST status and GET read-back | Keep artifact/report locally; retry same idempotency key at next handoff; post Townhall blocker | Never drop the run or create duplicates; secret stays out of logs |
| Townhall outage | GET/POST failure | Keep local handoff note; retry on next monitor tick | Dashboard/artifacts remain authoritative; no filler duplicate posts |
| Hermes dashboard revision fails | Herm monitor/report or unchanged dashboard | Keep last known-good dashboard; expose stale/blocker state; coordinate exact fix | Never claim dashboard updated without browser/read-back verification |
| Scheduler/gateway outage | Cron state, last run, gateway health | Next run rechecks readiness; no catch-up batch of benchmarks | Avoid duplicate runs; alert only with concrete missed-slot finding |
| Host reboot/power loss | Missing process/artifact and service checks | Resume from immutable artifacts; rerun only if no valid artifact exists | Never overwrite a partial run; require new run ID |
| **Wedged MPS → silent CPU fallback** (server UP, `/health` 200, alias/argv unchanged, but gen ~2.7 tok/s & GPU util ~6 %; see 2026-09-17 incident) | `gpu_backing_probe.py`: gen_tps < 8 or GPU util < 40 % during a live token; corroborate with `journalctl --user -u llama-server.service` for `no usable GPU found` | Preflight → write BLOCKED, do NOT run, page Herm. Add MPS teardown to the harness end so a run can't leave MPS wedged. Herm → `mps_recover.py --confirm`, then re-probe to confirm GPU-backed | Never auto-`--confirm` recover in an unattended slot (production restart = human-required); never treat `/health` 200 as proof of GPU-backing |
| Model promotion disagreement | Promotion state and review gate | Keep `not-evaluated`; no automatic promotion | AJ review remains required |

## Recovery semantics

- **Retryable:** dashboard POST 401/400 after secret/schema correction, Townhall transient failure, isolated server startup failure after the process is fully stopped, or a temporary network read failure. Retry with the same run ID/idempotency key and verify.
- **Non-retryable for the current slot:** unhealthy storage, missing candidate, checksum mismatch, production degradation, incomplete raw artifact, or semantic/visible-output failure. Record BLOCKED/FAILED and consume no second benchmark slot.
- **Human-required:** secret provisioning/rotation, filesystem repair, production service changes, destructive cleanup, promotion, or any action that risks LAN availability.

## Daily handoff contract

Sparkbot posts measured facts, evidence links, exact blocker, proposed adjustment, owner, and verification/rollback. Herm replies with dashboard effect, implementation status, and any schema/process change. Both agents keep the dashboard honest: no trend line before two verified runs, no quality score without measured quality, and no leaderboard entry for failed/blocked/unverified data.

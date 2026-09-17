# Fleet Self-Healing Watchdog

**Status:** Live and drill-tested, 2026-09-17
**Owner:** Herm
**Cron job:** `Fleet self-healing watchdog` (id `c6823bea3fc0`), every 3 min
**Monitor script:** `~/.hermes/scripts/fleet_watchdog_monitor.py`
**Related:** [[A projector in the kitchen, a living dashboard and interactive playground]]; [[Light-Input Signalling]]; [[Benchmark Insights]]

## Why it exists

AJ's mandate (2026-09-17): he does **not** want to act as pager/sysadmin. When a
LAN service goes down, the owning agent should recover it with minimal downtime
without AJ having to notice an Attention box on the wall and tell someone. The
wall Attention Center is the *record*; it was never an alerting mechanism, so
before this, an exhausted auto-restart just sat pending on the wall (Fish Speech
TTS sat down ~19 h this way). This watchdog is the agent-with-judgment layer on
top of the dashboard's existing dumb retry loop.

## How it works

- **Monitor gate (cheap, no LLM):** every 3 min a deterministic script polls
  `/api/fleet` and emits a stable, timestamp-free JSON list of anything not
  `up`, plus each service's remediation-budget state. Identical output tick over
  tick → the cron agent does **not** run (zero token cost). Only a *change* (new
  down service, a recovery, budget exhausted) wakes the agent.
- **Agent (full autonomy on Spark):** re-probes to rule out transient/false-down
  blips, then SSHes in, reads the journal for root cause, applies the narrowest
  fix, and **verifies recovery with a real health probe** (not just a
  `systemctl` exit code). Resolves the matching Attention record via the API
  only after a verified-healthy probe.
- **Autonomy granted by AJ:** full Spark service recovery incl. dependency/config
  fixes. Hard stops (must escalate, must not act): destructive/data-losing
  actions; restarting a service with an ACTIVE user workload (ComfyUI `/queue`
  job, running llama.cpp generation) purely to clear a probe; anything needing
  physical access or AJ's own sudo.

## Escalation

- **Slack DM** (`D0BUVPRJAE4`) on **every** run — AJ wants full visibility even
  of successful auto-fixes. This is the normal reporting channel.
- **Physical light blink** ([[Light-Input Signalling]], `type: error`, 4 pulses)
  fires **only when the agent cannot fix it itself** and AJ is needed — after
  remediation was attempted and the service is still down, or a hard stop
  blocks the fix. Never for successful fixes or false alarms.

## Reliability note — cron drift-skip

Unpinned agent cron jobs are silently skipped whenever the global inference
config drifts (`drift_skip`). This had already killed 4 of AJ's other jobs. The
watchdog is therefore **pinned** (currently `gpt-5.6-terra` / `openai-codex`) so
a config change can't silently disable the thing that guards uptime. If
automation "just stops", check `cron list` for `drift_skip` across all jobs.

## Drill performed

Deliberately stopped `fish-speech-api.service` on the Spark; confirmed the
monitor flipped to `down`, fired the watchdog, and it diagnosed (journal),
restarted the unit, waited for model load, and independently verified recovery
(port 8080 listening + `/v1/health` 200), then resolved the Attention. Recovery
was also confirmed independently outside the agent's self-report.

## Probe-path traps fixed same day

- ComfyUI `/system_stats` returns HTTP 500 even when healthy on the Spark — a
  false-down trap. Fleet now probes `/queue` (200 when up). Committed `aa4dc32`.
- `/insights` was frozen on "Loading benchmark history" due to a Svelte 5
  `each_key_duplicate` crash (blockers keyed on `runId+kind`, but one run had 5
  `readiness` blockers). Fixed by adding the loop index to the key. Same commit.

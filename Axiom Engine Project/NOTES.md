---
tags: [project/axiom-engine, type/run-log]
---

# Axiom Engine — Running Notes

> Running technical session log: infra facts, gotchas, bugs found/fixed,
> process-hygiene lessons. Same role `NOTES.md` plays for every other
> project in the portfolio — append-only, dated entries, newest at top or
> bottom (pick one and stay consistent).

## 2026-09-09 — SSH access set up

Dev server confirmed at `192.168.0.26` (Asus Zenbook, hostname
`openclaw-sandbox`, user `aj`). Set up key-based SSH from the Hermes laptop:

- Generated a dedicated keypair `~/.ssh/axiom-engine` (ed25519, no
  passphrase) — separate from the Spark's key.
- Added `Host axiom-engine` block to `~/.ssh/config`
  (`HostName 192.168.0.26`, `User aj`, `IdentityFile ~/.ssh/axiom-engine`).
- AJ manually appended the public key to `~/.ssh/authorized_keys` on the
  server (mkdir/chmod 700 `.ssh`, echo pubkey, chmod 600 file) — no
  ssh-copy-id needed.
- Verified: `ssh axiom-engine` connects non-interactively, confirmed
  `whoami`/`hostname`.

Not yet done: survey what's actually running on this box (services, ports,
what the Axiom Engine project technically consists of on this host).

## 2026-09-09 — Recon: found the project, it's alive

Surveyed `axiom-engine` (`192.168.0.26`). The project is **AJ's Operations
Console** ("Playground") at `~/playground` — an Express/Svelte/SQLite LAN
dashboard + Jobs automation engine + the in-house **Ralph Loop** coding
agent that's the thing that actually stalled. Full writeup in
`[[Axiom Engine]]`. Key facts not to rediscover:

- Repo has a **real GitHub remote** (`andersjensen10/AJs-Ubuntu-Server`,
  branch `main`) but local is **61 commits ahead of origin** — nothing
  pushed since the stall. `gh` CLI is not installed on the Hermes laptop
  (`gh repo view` failed with `command not found`); use `git` directly via
  SSH to the box, or install `gh` if PR/CI workflows are needed later.
- The **systemd service never stopped** — `aj-playground.service` has been
  running continuously since 2026-07-10, hourly jobs still firing per
  `journalctl`. "Stalled" means dev work stopped, not that the app is down.
- Two unrelated projects share the same home dir: `~/homeagent` and
  `~/ops-api` — do not assume they're in scope.
- Don't confuse this box's own `~/CLAUDE.md` / `~/playground/CLAUDE.md`
  (Claude Code instructions for working *in that repo*) with anything in
  this vault — they're the repo's own dev docs, left as-is.
- `~/playground/docs/` has 30+ planning docs (migration, Ralph phases,
  Slack integration, deployment checklists, etc.) — this is where the real
  long-term blueprint content for `[[improvements]]` should eventually get
  mined from, once AJ decides what's still relevant vs. superseded.

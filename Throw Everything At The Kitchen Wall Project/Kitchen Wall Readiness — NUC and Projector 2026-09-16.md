# Kitchen Wall Readiness — NUC and Projector

**Target date:** 2026-09-16  
**Status:** Preparation  
**Owner:** Herm, with AJ decisions where noted  
**Related:** [[A projector in the kitchen, a living dashboard and interactive playground]]; [[Agentic Chatroom Project/Townhall Onboarding]]

## Objective

Have a reliable first physical installation: the Intel NUC boots, drives the Acer H6531BDi at native 1920×1080, launches the Kitchen Wall dashboard in kiosk mode, recovers from a browser failure, and displays honest LAN/Townhall status. Do not make the NUC the primary application server or grant it broad agent authority until the physical baseline is proven.

## Architecture decision for first installation

Use the NUC as a **thin client** initially:

```text
NUC → kiosk browser → Kitchen Wall dashboard over the LAN
                         ├── fleet health
                         ├── Townhall
                         ├── Attention
                         └── existing dashboard scenes
```

The dashboard remains hosted on the known development machine until the NUC is stable. Local hosting, offline cache, scene automation, and a NUC-resident Hermes agent are follow-up decisions, not prerequisites for the first projection test.

## Pre-arrival software gate

- [x] Kitchen Wall application has a working dashboard, Townhall, fleet health, Attention, kiosk mode, and Doodle scenes.
- [x] Townhall is a cross-agent bulletin board, not an Agora transcript.
- [x] Townhall has explicit identities, project scope, threaded replies, tags, and read-back verification.
- [x] Axiom Engine is represented as `axiom-engine`; its future agent must be onboarded separately.
- [ ] Run `npm test`, `npm run check`, `npm run build`, and `git diff --check` immediately before the installation session.
- [ ] Create a clean checkpoint commit for the current Kitchen Wall work; do not mix hardware changes with unrelated uncommitted work.
- [ ] Confirm the dashboard binds to a LAN-reachable address and that another device can load it.
- [ ] Install/use the kiosk launcher in `deploy/kiosk/` only after the NUC browser and dashboard URL are known.

## Physical preparation

- [ ] Measure the IKEA shelf-to-wall throw distance.
- [ ] Estimate the image size using the projector's 1.5–1.66:1 throw ratio; 60–80 inches is the likely practical range.
- [ ] Prepare HDMI, power, network, keyboard, mouse, and a temporary way to reach the NUC.
- [ ] Leave ventilation around both the projector and NUC; do not box either device into the shelving.
- [ ] Prefer a square-on mounting position and use keystone correction only as needed.
- [ ] Decide whether the projection surface is acceptable for text, or whether a matte-white panel/screen is needed.
- [ ] Do not automate the projector's smart plug until the real plug and address are confirmed.

## Installation runbook — 2026-09-16

1. Install the NUC power supply and verify stable boot/reboot behavior.
2. Record OS, disk, RAM, hostname, network interface, and update state.
3. Give the NUC a stable LAN identity, preferably with a DHCP reservation rather than an invented static address.
4. Connect HDMI and verify a real 1920×1080 display output.
5. Install/configure the browser and launch the dashboard in kiosk mode.
6. Verify kiosk recovery after deliberately closing the browser.
7. Load the dashboard from another LAN device and confirm the NUC is not relying on localhost for the dashboard.
8. Confirm Townhall shows live posts and that filters/replies do not create page-level scrolling.
9. Confirm a deliberately unavailable service is shown as stale/unknown rather than falsely healthy.
10. Only after the above passes, mount and calibrate the projector.
11. Record the final NUC hostname/IP, projector placement, image size, and any cabling constraints here.

## NUC agent rollout

### Stage 1 — observer

The NUC agent may report NUC health, kiosk/browser state, display availability, and projector-related observations. It may not modify shared project code or other machines.

### Stage 2 — bounded operator

After observer reliability is established, permit narrowly allowlisted actions such as restarting the kiosk browser. Every action must have a visible result and a recovery path.

### Stage 3 — maintenance

Only after explicit review may the agent update its own deployment, manage scene switching, or operate projector power. Destructive actions, credentials, cross-project changes, and public releases remain outside autonomous authority.

The agent must have its own stable Townhall identity, MCP server entry, local mode-700 secret file, and LAN-reachable Townhall URL. It must never reuse Herm's identity or token.

## Definition of ready

The first installation is successful when:

- the NUC boots unattended;
- the projector displays the dashboard at native resolution;
- the kiosk browser recovers from failure;
- Townhall and fleet status are visible;
- stale/offline sources are represented honestly;
- the display can be shut down safely; and
- the system remains usable if the NUC agent is absent.

## Townhall monitoring policy

The Herm coordination monitor runs every **1 minute** as of 2026-09-13. This is a cheap deterministic feed poll, not a one-minute LLM invocation: unchanged snapshots suppress the agent run entirely. The monitor prompt limits processing to the three highest-value changed threads, suppresses routine acknowledgements and reply loops, and uses `local` delivery so it does not create chat noise. It prioritizes NUC/Kitchen Wall readiness, Axiom Engine onboarding, Spark coordination, and real blockers.

The monitor remains read-only with respect to code and infrastructure. It may read Townhall, reply with Herm's identity when useful, and create a needs-input Attention for a genuine blocker. It may not restart services, modify infrastructure, create credentials, or impersonate AJ/another agent. The Townhall feed now accepts a bounded `limit` query (capped at 100), and the monitor requests a maximum of 100 posts so growth from additional agents cannot create an unbounded poll payload. As more agents join, agents should post material findings and questions rather than heartbeats; the change gate is only sustainable if the feed remains coordination-oriented.

## Decisions still needed from AJ

- Whether the NUC should eventually host a local dashboard instance for resilience.
- Whether the NUC should run its own Hermes agent after the observer stage.
- Which scene-switching actions the NUC agent may perform autonomously.
- Whether projector power will be controlled through a smart plug and what duty-cycle schedule is wanted.
- Whether an external speaker or microphone is needed for later voice-driven scenes.

## Evidence log

- 2026-09-13: Townhall live feed confirms Herm/Sparkbot coordination, Spark benchmarking handoff, and explicit project ownership. No Axiom Engine agent or NUC agent is active yet.
- 2026-09-13: Kitchen Wall validation run passed: 117 tests, Svelte check with 0 errors/warnings, production build completed, and whitespace check passed.
- 2026-09-13: Added and syntax-checked a thin-client kiosk launcher with readiness wait, browser restart support through systemd, URL scheme validation, and no agent credentials. The service uses a mode-600 local URL environment file and intentionally does not start the dashboard or control hardware. Implementation is committed as `179a020` (`feat: add recoverable Kitchen Wall kiosk deployment`).
- 2026-09-13: Sparkbot verified the first-install dashboard target as `http://192.168.0.148:5173/`. Stable aggregate endpoints are `GET /api/fleet` and `GET /api/townhall`; the NUC should use those through the dashboard host, not poll Spark services directly. Six dashboard-side health probes measured approximately 1–9 ms; production-model interference is not yet measured. No Spark-side cache is recommended for the first baseline.
- 2026-09-13: Next physical-readiness action is to test from the NUC: dashboard root, `/api/fleet`, and `/api/townhall`; then sustained access, DNS/route, Wi-Fi isolation/firewall behavior, SSE/realtime, and recovery after a temporary LAN disconnect.
- 2026-09-13: The dashboard repository contains uncommitted `LIGHT-SIGNALS` work; hardware preparation must preserve that work and create a deliberate checkpoint before deployment.
- 2026-09-17: **Fleet registry (`src/lib/server/fleet.ts`) brought in sync with the full LAN inventory.** Added **Agora chatroom** (`192.168.0.148:7480/api/health`), **LiteLLM proxy** (`192.168.0.139:4000/health/liveliness`), and **Qwen TTS tester** (`192.168.0.139:8020/v1/models`) — previously live but unmonitored. Fleet now probes 9 services; a `/24` ping sweep + port scan confirmed no other hosts/services are missing. Agora needed a code change to be LAN-reachable: its Vite web server was loopback-only, now started with `--host 0.0.0.0` (backend stays on loopback, Vite proxies `/api`+`/ws` same-origin, so the `/api/health` 200 covers both tiers). `npm run check` clean; `verify-wall-fit.mjs` passes all routes with the larger fleet panel. **Known probe bug (unfixed):** ComfyUI's `/system_stats` path returns 500 while the box is actually up (queue responds), so it shows falsely "down" — switch its probe path (e.g. `/queue`) next time fleet.ts is touched.

## Related implementation

- Repository: `~/Desktop/Hermes/kitchen-dashboard`
- Kiosk launcher: `deploy/kiosk/kitchen-wall-kiosk.sh`
- Kiosk service template: `deploy/systemd/kitchen-wall-kiosk.service`
- Townhall protocol: [[Agentic Chatroom Project/Townhall Onboarding]]

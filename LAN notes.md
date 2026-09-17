---
tags: [infra/lan]
---

# LAN Notes — Home Lab Infrastructure

> Last updated: 2026-09-11 by Herm (full LAN subnet scan, cross-referenced against
> this vault — found/killed a duplicate self-hosted RustDesk server on the Spark,
> corrected a stale port-8000 entry, discovered several undocumented services
> and a Tailscale mesh, flagged a hardcoded-key remote-exec service on both
> the Spark and Axiom Engine). Full authoritative detail (SSH access,
> ComfyUI model inventory, TTS API specifics, pitfalls) lives in the Hermes
> skill `home-lab-infrastructure` (`references/lan-inventory.md` +
> `references/reasoning-model-app-integration.md` +
> `references/fish-speech-tts.md`) — this page is the
> Obsidian-facing summary, kept in sync with it. Relevant to
> [[Agentic Chatroom]] since it runs entirely on this infra.

-----

## Axiom Engine dev server (Asus Zenbook) — `192.168.0.26`

Hosts AJ's passion project "The Axiom Engine". Hostname `openclaw-sandbox`,
user `aj`.

**SSH — working, confirmed 2026-09-09.** `ssh axiom-engine` connects
non-interactively (dedicated key `~/.ssh/axiom-engine`, `Host axiom-engine`
block in `~/.ssh/config`). AJ appended the public key to the server's
`authorized_keys` manually and it worked first try. Full detail in the
`home-lab-infrastructure` skill, `references/lan-inventory.md`.

**Services found (2026-09-11 LAN scan — first survey of this box beyond SSH):**

| Service | Port | Status | Auth | Notes |
|---|---|---|---|---|
| Node app ("Anders Jensen" site) | 8081 | ✅ live | none | `~/playground/node/server.js`, looks like a personal portfolio/site build — title "Anders Jensen". Not yet clarified with AJ whether this is active work or a leftover experiment. |
| ⚠️ ops-api (remote exec) | 8765 | ✅ live | **same hardcoded plaintext key as the Spark's copy, `ops-console-2025`** | `~/ops-api`, identical script to the Spark's. Same risk profile — see the Spark's entry above for full detail. Documented only, left running per AJ. |
| SSH | 22 | ✅ authorised | pubkey | See above. |
| Tailscale | mesh, n/a | ✅ active | Tailscale auth | Node `openclaw-sandbox`, `100.85.206.104`, v1.102.2. Same tailnet as the Spark and the Windows gaming laptop. |
| DNS stub resolvers | 53 (127.0.0.53, 127.0.0.54) | — | — | Standard systemd-resolved, not a real service to track. |

Full technical survey (what Axiom Engine actually does, other directories,
project structure) still not done — this covers ports/processes only.

-----

## Spark — NVIDIA GB10 (Blackwell), 128 GB unified memory — `192.168.0.139`

Primary local compute box for generative AI. Powers Agora's LLM + image/video
generation.

**Location/network (2026-09-07):** moved into the living room for better wifi
reception, but is still on **wifi, not ethernet** — ethernet cable + switch
are on AJ's shopping list to get it wired. Until then, treat the "Spark
flaps" behavior below as at least partly explained by this, not purely a
service-level flakiness issue.

**Full LAN scan cross-reference (2026-09-11):** below is now the complete,
corrected service table for this box (superseding earlier partial entries —
port 8000 was previously mis-documented as a gated "older LLM API server";
it is actually a **file server**, see below).

| Service | Port | Status | Auth | Notes |
|---|---|---|---|---|
| llama.cpp (LLM) | 8014 | ✅ live | none | OpenAI-compatible. **Agora's LLM backend.** Model is swapped periodically — see below. |
| ComfyUI (image/video) | 8188 | ✅ live | none | v0.26.0, CUDA 13.0, PyTorch 2.11.0. Checkpoints: `flux1-dev-fp8`, `ltx-2.3-22b-dev-fp8`, `ltx-2.3-22b-distilled-fp8`. **Agora's media generation backend.** Queue is often busy with AJ's own jobs — check `GET /queue` first. |
| Fish Speech TTS | 8080 | ✅ live | none | S2-Pro 4B. Plain TTS + voice cloning both work. Steady-state ~13× realtime (GB10 memory bandwidth + kernel maturity bound). **Directly callable by any LAN agent** (bound `0.0.0.0`, no auth) — endpoint reference in [[Fish Speech TTS]]. Full interactive dashboard at `192.168.0.148:7490`, incl. a **Voice Lab** tab (2026-09-10, backed by a sibling `voiceprep-api.service` on this box :8090, also directly callable, no auth) that automates YouTube → trim → vocal-separate → denoise → transcribe → chain → publish-as-Fish-voice. |
| voiceprep-api (Voice Lab backend) | 8090 | ✅ live (uvicorn) | none | Backs the Fish TTS dashboard's Voice Lab tab, see above. |
| Qwen TTS local tester | 8020 (API) / 8021 (web UI) | ✅ live | none | `~/qwen-tts-server`, separate/experimental TTS stack from Fish Speech — not otherwise referenced in AJ's projects yet. Found in 2026-09-11 LAN scan, not previously documented. Status/purpose vs. Fish Speech not yet clarified with AJ. |
| LiteLLM proxy | 4000 | ✅ live | unknown (Swagger UI reachable) | `~/litellm-env`, `litellm --config litellm-config.yaml`. Presumably a unified OpenAI-compatible proxy in front of one or more backends — not yet mapped to any known project. Found in 2026-09-11 scan, not previously documented. |
| gohttpserver (file server) | 8000 | ✅ live | HTTP Basic Auth (`admin`/`aGMK8ayHsFVfS4XP` — found in live process argv, treat as sensitive) | **Correction (2026-09-11): this is NOT an LLM API server** as an earlier scan guessed — it's `/opt/gohttpserver` serving `~/public` as a plain authenticated file browser. Purpose/contents not yet surveyed. |
| DGX Dashboard | 11000 | ✅ live (localhost only) | none observed | NVIDIA's stock DGX Spark system dashboard, bound `127.0.0.1` only (not LAN-reachable without a tunnel). Found 2026-09-11. |
| ⚠️ ops-api (remote exec) | 8766 | ✅ live | **hardcoded plaintext API key `ops-console-2025`, checked into `~/ops-api/main.py`** | **Security risk, deliberately left running per AJ (2026-09-11): document only, do not touch.** FastAPI service bound `0.0.0.0` exposing `POST /exec` — runs **arbitrary shell commands** as the `aj` user given only that static key. Same script/key duplicated on Axiom Engine (`references/lan-inventory.md` below). Anyone on the LAN who obtains the key gets shell-equivalent access to both boxes. AJ's instruction: leave as-is for now, but any future agent given standing access to the Spark or Axiom should be told to lock this down (bind to localhost, rotate/remove the key, or kill it) rather than build around it. |
| RustDesk self-hosted server (decommissioned) | 21115-21119 | ❌ killed 2026-09-11 | — | **Found running as a SECOND, undocumented self-hosted RustDesk server** (`/opt/rustdesk/hbbs`+`hbbr`, owned by user `aj`, live since Sep 7 — predates and was unrelated to the laptop-hosted server built the same day). No systemd/cron/shell-rc autostart found, so it was a manual one-off launch. AJ decided (2026-09-11) the **Hermes laptop's server is the canonical one** — killed both processes here, freeing 21115-21119. The Spark's own RustDesk *client* already pointed at the laptop's server correctly, unaffected by this. If this reappears after a Spark reboot, check for a hidden autostart hook not found in this pass. |
| Older LLM API server | 8000 | ⚠️ **RETRACTED, see gohttpserver above** | — | This was a stale/incorrect entry from an earlier port-guessing pass; 8000 is gohttpserver, not an LLM API. Removed. |
| SSH | 22 | ✅ authorised (2026-09-09) | pubkey | Laptop key added to `authorized_keys` on the Spark. `ssh spark` logs in non-interactively — log-level diagnosis (journalctl, nvidia-smi) and remote maintenance are now unblocked. |
| Tailscale | mesh, n/a | ✅ active | Tailscale auth | Node `gx10-360f`, `100.98.83.18`. Same tailnet as Axiom Engine (`openclaw-sandbox`) and the Windows gaming laptop (`msi`, `100.64.231.18`) — found 2026-09-11, not previously documented. Purpose/use not yet clarified with AJ; note it exists as an alternate remote-access path alongside RustDesk. |

**The Spark flaps.** `ping` is unreliable (100% loss observed while HTTP was
fine) — always health-check with an HTTP call (`/v1/models` or a real chat
completion), never ICMP. As of 2026-09-07 it's on wifi in a new location, so
expect this to persist (or worsen) until it's moved to ethernet.

### Active LLM model on :8014

- **Current (as of 2026-09-06): `qwen3.8-27b-aggressive-q5`** — replaced
  `gpt-oss-120b`. CUDA on, prompt-cache/checkpoints off.
- **Parallel slots (FR-002, shipped 2026-09-09):** `llama-server.service` now
  runs `PARALLEL=2` with `CTX_SIZE=100000` (50k tokens/slot, up from a single
  16k-context slot). Verified live (`total_slots=2`) with a real 2-request
  concurrent test confirming genuine concurrent streaming, not serial
  queueing. Memory headroom at this setting: 33GB free. Rollback available at
  `~/.config/llama-server.env.bak-fr002` on the Spark. Room for a 3rd slot
  later — retest headroom before raising further. Full report:
  `FR-002-spark-llamacpp-parallel-slots-REPORT` in the Agentic Chatroom
  Project vault.
- Previously: `gpt-oss-120b` (116.8B params, mxfp4, 65536 ctx). Measured
  ~44.5 tok/s prompt / ~29.3 tok/s generation.
- Both are **reasoning models** — they emit chain-of-thought on a separate
  `reasoning_content` field, answer text lands in `content` only once
  reasoning finishes.

### Qwen3.8-27b: thinking-mode token throughput (measured live, 2026-09)

Same one-sentence persona reply, thinking ON vs OFF, same request otherwise:

| thinking | completion tokens | latency | reasoning_content |
|---|---|---|---|
| ON (model default) | 94 | 5.3s | 308 chars |
| OFF | 18 | 1.4s | none |

**~5x more tokens and ~3.7x more latency with thinking on, for zero benefit
on casual chat.** This is also the root cause of "empty reply" bugs: thinking
eats the whole `max_tokens` budget before the model reaches the actual
answer, so `content` comes back empty with `finish_reason: "length"`.

- **Toggle:** llama.cpp Qwen3 chat template gates it via
  `chat_template_kwargs: {"enable_thinking": false}` in the request body
  (needs the server started with `--jinja`, which the Spark's launch line
  has). `{"preserve_thinking": true}` keeps prior reasoning across turns if
  ever wanted.
- **Applied in Agora:** commit `366e7b1` — `AGORA_THINKING` env, default
  **false**, plumbed per-persona end to end. Gives the ~5x token win above.
  **Quality evaluated (FR-001, shipped 2026-09-09):** side-by-side battery
  across two personas found no measurable, consistent roleplay/voice/banter
  quality gain from thinking=true, at ~11x TTFT and ~1.65x total generation
  cost — recommendation was to keep the default `false`. Per-persona override
  remains available for any persona that specifically needs deliberate
  reasoning. Full report: `FR-001-eval-thinking-off-quality-REPORT` in the
  Agentic Chatroom Project vault.
- Sampler params (temp/top_k/top_p/min_p) belong on the Spark's launch flags,
  not hardcoded client-side — the client should only ever override
  temperature per-persona.
- Empty-reply fix when thinking IS needed: raise the token budget (Agora:
  `AGORA_REASONING_RETRY_TOKENS`, default 4096), never merge
  `reasoning_content` into the visible reply.

Full write-up incl. connection-vs-budget-failure diagnosis, retry design, and
mock-LLM verification pattern: Hermes skill `home-lab-infrastructure`,
`references/reasoning-model-app-integration.md`.

## Hermes laptop (this machine) — Lenovo ThinkPad, Valby

- No NVIDIA GPU — Intel Iris Xe integrated graphics only. No CUDA.
- ~14 GB RAM, 4 GB swap.
- Consequence: any CUDA-only workload (TTS models, etc.) must run on the
  Spark instead.
- LAN IP: `192.168.0.148` (wifi; wired NIC present but unplugged/no-carrier).
- **Agora chatroom** runs here (dev): Vite web on `:7480`, Fastify API/WS on
  `:7481`. As of 2026-09-17 the web server binds `0.0.0.0` (started with
  `--host 0.0.0.0`) so it's reachable from the whole LAN — the kitchen-wall
  dashboard's fleet panel probes `http://192.168.0.148:7480/api/health`. The
  backend stays loopback-only; Vite proxies `/api`+`/ws` to it same-origin.

## RustDesk self-hosted server (2026-09-11) — runs on the Hermes laptop, `192.168.0.148`

Replaces the public RustDesk relay (was routing traffic through a
public server known to be under active botnet attack — AJ's directive was
to stop using it immediately). Self-hosted `hbbs`+`hbbr` v1.1.16.

- **Host chosen:** this laptop, not the Spark — always-on like the Spark,
  but on a stable/simple network path (the Spark is wifi + known to "flap");
  hosting the rendezvous/relay server on the flappy box would undermine the
  whole point. Both the Spark and this laptop stay in the apartment 24/7 per
  AJ, so either satisfied "always on"; picked the more stable one.
- **Install:** binaries in `~/.local/bin/` (`hbbs`, `hbbr`, `rustdesk-utils`),
  data dir `~/.config/rustdesk-server/` (holds the ID/relay keypair +
  sqlite3 client DB).
- **Run as:** systemd **user** services (matches the Spark's pattern, no
  root needed): `rustdesk-hbbs.service` and `rustdesk-hbbr.service` in
  `~/.config/systemd/user/`, both `enable --now`'d (survive reboot — user
  linger is already on for `aj`).
- **hbbs launch flag:** `-r 192.168.0.148:21117` (tells clients where the
  relay is).
- **Ports (all confirmed open + reachable from the Spark over LAN
  2026-09-11):** TCP 21115-21119, UDP 21116. Firewall (`ufw`, active on this
  laptop) had to be opened manually by AJ (no passwordless sudo for Herm):
  `sudo ufw allow 21115:21119/tcp && sudo ufw allow 21116/udp`.
- **Server public key** (needed on every client, Settings → Network →
  ID/Relay Server, "Key" field): `ypJWWuzI420Hmvmdx9Tgkgbl8jvmjD8qlVSGNATMM5E=`
  — read anytime from `~/.config/rustdesk-server/id_ed25519.pub`.
- **Client config needed on each machine** (RustDesk app → Settings →
  Network → ID/Relay Server, unlock with local password first):
  - ID Server: `192.168.0.148`
  - Relay Server: `192.168.0.148`
  - Key: the public key above
  - Do this on: the Spark, the Windows gaming laptop, and this Hermes
    laptop's own RustDesk client (if used as a controllee) — all three need
    pointing at the new server to stop using the public relay.
- **CONFIRMED WORKING end-to-end (2026-09-11):** all three clients (this
  laptop `192.168.0.148`, Spark `192.168.0.139`, Windows gaming laptop
  `192.168.0.30`) manually repointed via Settings → Network → ID/Relay
  Server in each RustDesk app, then verified live in
  `journalctl --user -u rustdesk-hbbs.service` — `update_pk` log lines show
  all three IPs registering against our own hbbs, none against
  `rs-ny.rustdesk.com`. Public relay is no longer in the path.
- **Gotcha: don't hand-edit `RustDesk2.toml` while the client is running.**
  The running RustDesk daemon periodically rewrites its own config file and
  will silently revert `rendezvous_server`/`key`/`relay-server` back to the
  public defaults, undoing a `cat >> RustDesk2.toml` edit within seconds —
  confirmed happening on both this laptop and the Spark. Other self-hosters
  hit the same behavior. **Always use the GUI** (Settings → Network →
  Unlock Network Settings → fill ID/Relay/Key → Apply) — that persists.
  Killing/restarting the client to force-apply a hand edit does not survive
  the next autosave, either.

## MSI Gaming Laptop — 16 GB RAM, RTX 4080 12 GB VRAM

Available compute, not currently assigned a running service. Was earlier
considered for TTS hosting; that plan moved to the Spark instead (see
`home-lab-infrastructure` skill pitfall #3 — device roles get reassigned,
always check latest notes rather than an earlier plan).

## Headless Ubuntu server — orchestration platform (not yet briefed)

AJ's main dev/deployment box running a homebuilt agentic automation system.
IP/hostname and access method not yet gathered — **do not probe or SSH in
opportunistically**; AJ wants to walk Herm through it directly first.

## Router / Network devices (2026-09-11 full subnet scan)

Full `192.168.0.0/24` sweep (ARP + ping + targeted port probes) found these
LAN devices beyond the compute boxes already documented above:

| IP | MAC / vendor | Identity | Notes |
|---|---|---|---|
| `192.168.0.1` | Sagemcom (18:0c:7a) | ISP/WiFi router | HTTP+HTTPS admin UI reachable, title "Gateways" — standard ISP gateway box, not separately managed by Herm. |
| `192.168.0.176` | TP-Link (1c:3b:f3) | **TP-Link HS100 smart plug**, alias "Smart Plug" | Identified via the Kasa/TP-Link binary protocol on port 9999. **Controls the living room lights (confirmed by AJ, 2026-09-11).** Control script `~/.local/bin/kasa_plug.py on\|off\|status` on this Hermes laptop (implements the Kasa protocol directly, no cloud/library dependency) — tested live 2026-09-11, toggled off and back on successfully. **AJ has also approved using this as a low-key attention-getting channel** — flicker the lights as a secondary nudge if he's not responding to something time-sensitive on Slack, but sparingly, not for routine notifications. |
| `192.168.0.30` | TP-Link Systems (00:31:92) | **Windows gaming laptop** ("msi" on Tailscale) | Already known (RustDesk client repointed 2026-09-11). No inbound ports open from LAN scan — Windows Firewall blocking as expected; not a problem, RustDesk/Tailscale both work as outbound-initiated. |
| `192.168.0.110` | unknown (de:4a:7c) | **Unidentified — AJ doesn't know either.** | No open ports (phone/tablet-typical). Flagged for AJ; re-check next time it's relevant. |
| `192.168.0.139` | — | Spark | See dedicated section above. |
| `192.168.0.26` | — | Axiom Engine | See dedicated section above. |
| `192.168.0.148` | — | This Hermes laptop | Self-hosted RustDesk server, see below. |
| `192.168.0.207` | 6c:6e:07 (same as .26!) | **Duplicate/second interface of Axiom Engine**, NOT a separate device | `ssh axiom-engine` resolves to `.26`, but `.207` answers SSH with the identical banner and shares the exact same MAC as `.26` — this is the same physical box seen on two IPs (likely two DHCP leases from Wi-Fi roaming/interface flap, not two NICs). Do not treat as a distinct host. |

**Full scan method (repeatable):** ARP table (`ip neigh`) cross-referenced
with a ping sweep of the whole /24, MAC vendor lookup via
`api.macvendors.com`, and targeted TCP probes (`/dev/tcp` bash trick — no
`nmap` installed on this laptop, would need sudo to add it) for common
service ports. The TP-Link smart plug was positively identified by
speaking its proprietary port-9999 protocol directly (XOR-cipher JSON,
`get_sysinfo` command) rather than guessing from an open port alone.

## Tailscale mesh (found 2026-09-11, not previously documented)

Both the Spark and Axiom Engine (and separately, the Windows gaming laptop)
are joined to the same Tailscale tailnet under account `andersjensen1@`:

| Node | Tailscale IP | Hostname |
|---|---|---|
| Spark | `100.98.83.18` | `gx10-360f` |
| Axiom Engine | `100.85.206.104` | `openclaw-sandbox` |
| Windows gaming laptop | `100.64.231.18` | `msi` |

Purpose/origin not yet clarified with AJ — this predates Herm's involvement
and exists as a second remote-access path alongside RustDesk (e.g. it would
still work if a machine left the apartment network, unlike the pure-LAN
RustDesk setup). Worth asking AJ whether this is meant to be the "off-LAN"
remote access story, or a leftover from an earlier setup attempt.

## Related notes
- [[Fish Speech TTS]] — dedicated benchmarking/tuning page for the TTS engine above.
- [[Agentic Chatroom]] — the project this infra primarily serves right now.
- [[Next Level Agentic Chatroom Project-ARCHIVE]] — archived sprint-1 backlog; flagged the wifi/ethernet
  situation above as a sprint risk.
- [[NOTES]] — Agora-specific session log referencing this same infra.

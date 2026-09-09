# LAN Notes — Home Lab Infrastructure

> Last updated: 2026-09-09 by AJ (FR-002: SSH + parallel slots). Full authoritative detail (SSH access,
> ComfyUI model inventory, TTS API specifics, pitfalls) lives in the Hermes
> skill `home-lab-infrastructure` (`references/lan-inventory.md` +
> `references/reasoning-model-app-integration.md`) — this page is the
> Obsidian-facing summary, kept in sync with it. Relevant to
> [[Agentic Chatroom]] since it runs entirely on this infra.

-----
New machine and server available on LAN this section is new  and must be upated:
192.168.0.26
Asus Zenbook hosten our large pasion project "The Axiom Engine"

-----

## Spark — NVIDIA GB10 (Blackwell), 128 GB unified memory — `192.168.0.139`

Primary local compute box for generative AI. Powers Agora's LLM + image/video
generation.

**Location/network (2026-09-07):** moved into the living room for better wifi
reception, but is still on **wifi, not ethernet** — ethernet cable + switch
are on AJ's shopping list to get it wired. Until then, treat the "Spark
flaps" behavior below as at least partly explained by this, not purely a
service-level flakiness issue.

| Service | Port | Status | Auth | Notes |
|---|---|---|---|---|
| llama.cpp (LLM) | 8014 | ✅ live | none | OpenAI-compatible. **Agora's LLM backend.** Model is swapped periodically — see below. |
| ComfyUI (image/video) | 8188 | ✅ live | none | v0.26.0, CUDA 13.0, PyTorch 2.11.0. Checkpoints: `flux1-dev-fp8`, `ltx-2.3-22b-dev-fp8`, `ltx-2.3-22b-distilled-fp8`. **Agora's media generation backend.** Queue is often busy with AJ's own jobs — check `GET /queue` first. |
| Fish Speech TTS | 8080 | ✅ live | none | S2-Pro 4B. Plain TTS works; voice cloning currently 500s (open bug). |
| Older LLM API server | 8000 | ⚠️ up but gated | HTTP Basic Auth | Credentials not obtained. Superseded by :8014. |
| SSH | 22 | ✅ authorised (2026-09-09) | pubkey | Laptop key added to `authorized_keys` on the Spark. `ssh spark` logs in non-interactively — log-level diagnosis (journalctl, nvidia-smi) and remote maintenance are now unblocked. |

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

## MSI Gaming Laptop — 16 GB RAM, RTX 4080 12 GB VRAM

Available compute, not currently assigned a running service. Was earlier
considered for TTS hosting; that plan moved to the Spark instead (see
`home-lab-infrastructure` skill pitfall #3 — device roles get reassigned,
always check latest notes rather than an earlier plan).

## Headless Ubuntu server — orchestration platform (not yet briefed)

AJ's main dev/deployment box running a homebuilt agentic automation system.
IP/hostname and access method not yet gathered — **do not probe or SSH in
opportunistically**; AJ wants to walk Herm through it directly first.

## Related notes
- [[Agentic Chatroom]] — the project this infra primarily serves right now.
- [[Next Level Agentic Chatroom Project]] — active backlog; flags the wifi/ethernet
  situation above as a sprint risk.
- [[NOTES]] — Agora-specific session log referencing this same infra.

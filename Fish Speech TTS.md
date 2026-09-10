---
tags: [tts, fish-speech, spark, benchmarking, infra, dashboard, voice-cloning, voice-lab]
aliases: [Fish TTS, Fish Speech]
---

# Fish Speech TTS — Spark Benchmarking & Dashboard

> Last updated: 2026-09-10 by Herm (hardware-upgrade research + dashboard
> engineering + **Voice Lab**: automated YouTube-to-voiceclone pipeline).
> AJ rates Fish's voice-acting quality highly and wants it fully tuned for
> his pipeline. Full technical/API detail lives in the Hermes skill
> `home-lab-infrastructure` (`references/fish-speech-tts.md`); this page is
> the Obsidian-facing summary. Runs on the [[LAN notes|Spark]]. **AJ plans
> to test baseline functionality, set up a git repo for this project, and
> lay out refinement wishes next session** — see Open items at the bottom.

-----

## What it is

[Fish Speech S2-Pro](https://github.com/fishaudio/fish-speech) (4B params) —
open-source multilingual TTS with zero-shot voice cloning and free-form
natural-language control tags (`[whispers]`, `[laughs]`, `[pitch up]`, etc —
not a fixed vocabulary, invent your own). Runs as a systemd user service on
the Spark, `http://192.168.0.139:8080`, no auth.

**Status: plain TTS, voice cloning, and a full interactive dashboard all
work.** Steady-state throughput is ~13× realtime — see Benchmarks below for
why, and Hardware upgrade options for what would actually fix it.

## Interactive dashboard

`~/Desktop/Hermes/fish-tts-bench/` — local Node test bench + benchmark
dashboard. Runs on the **Hermes laptop**, reachable from any device on the
LAN at **`http://192.168.0.148:7490`** (laptop's current LAN IP — re-check
with `hostname -I` on that machine if it changes). `127.0.0.1:7490` only
ever works sitting at the laptop itself.

Start it: `node server.mjs` in that directory (not a persistent service —
start manually each session; `curl -s -o /dev/null -w '%{http_code}'
http://192.168.0.148:7490/` to check if it's already up). The static
files (HTML/CSS/JS) reload live on every request — only edits to
`server.mjs` itself need a restart.

**Visual design (2026-09-10):** restyled to match the [[Agentic Chatroom]]
("Agora")'s design system — same Nordic HSL-ladder token approach,
Inter font, 8px spacing spine, soft radii, layered shadows, spring-eased
button presses, rotating conic-gradient brand mark. Retinted teal instead of
Agora's blue so the two apps read as siblings, not clones.

Tabs (6, after a merge — see Dashboard engineering log below):
- **Generate** — full parameter control (temperature, top-p, repetition
  penalty, seed) + tag chips + live RTF readout per run, **plus an
  AI-assisted tag writer** (Qwen3.8 on the Spark) and a **"Split into
  chunks" toggle** for long/interruptible queued generation. See below.
- **Voice cloning** — upload reference audio + transcript, save server-side
  or try one-shot inline.
- **Voice Lab** — automated YouTube-to-voiceclone pipeline: fetch a clip,
  trim it on a waveform, clean it up (vocal separation + denoise),
  transcribe it, chain several cleaned snippets together, publish the
  result as one named Fish voice. Full detail in its own section below.
- **Tag playground** — same sentence with/without a control tag, back to
  back, to actually hear what a tag does.
- **Outputs** — every generation from any tab is auto-saved server-side
  (survives page reloads/navigation); list, play, download, delete one or
  all. Auto-cleanup runs every 15 min (24h retention, 500MB cap).
- **Benchmarks** — RTF landscape vs. reference hardware, length/tuning-knob
  sweeps, a memory-bandwidth comparison chart, and ranked next moves. Data
  lives in `public/data/benchmarks.json`, fetched live — edit that file to
  refresh numbers, no rebuild needed.

## Benchmark findings (2026-09-10)

### The service was silently dead for 3 days

Found during this session: the API had crashed 2026-09-07 12:36 CEST
(`torch.AcceleratorError: CUDA-capable device(s) is/are busy or
unavailable`, contention with `nvidia-cuda-mps-server`) — but the crash was
in a background **worker thread**, so the main process kept running and
`systemctl --user status` + `/v1/health` both reported healthy the entire
time. `/v1/tts` requests just hung/timed out silently. Restarted, confirmed
clean, then benchmarked from a known-good state.

**Lesson for future health checks on this service:** a real `/v1/tts` probe
catches failures that `/v1/health` alone misses.

### Steady-state throughput: ~13× realtime

14 timed runs (short/medium/long text, `chunk_length` and `max_new_tokens`
sweeps) all landed in a tight **12.8–13.7×** RTF band — no measurable effect
from text length or either tuning knob. The previously-reported 5× run-to-run
variance did not reproduce once the service was in a known-clean state; that
variance was very likely the crash, not steady-state GPU contention.
Confirmed separately: freeing the GPU by stopping the co-resident LLM
(`llama-server.service`) made no measurable difference to a single TTS
request either — contention isn't the bottleneck for solo throughput.

### Why 13× and not the H200's published 0.195×

| Hardware / stack | RTF | Source |
|---|---|---|
| **Spark GB10 (this box)** | **13.0×** | measured 2026-09-10 |
| RTX 3090, same `api_server.py --compile`, seq 32768 | 1.05× | community benchmark |
| RTX 3090, same stack, seq trimmed to 4096 | 0.55× | community benchmark |
| H200 + SGLang-Omni (independent day-0 bench) | 0.34× | sglang-omni README |
| H200 + SGLang-Omni (official) | 0.195× | fishaudio/fish-speech README |

Two separate causes stack up:
1. **Memory bandwidth** — GB10 is 273 GB/s vs. the 3090's 936 GB/s (3.4×)
   vs. H200's ~4.8 TB/s (~18×). S2-Pro's autoregressive decode is
   bandwidth-bound, so hardware alone explains a real chunk of the gap.
2. **Kernel/serving-stack maturity** — running the *identical* code
   (`api_server.py --compile`) a 3090 is still 12–24× faster than the
   Spark despite only 3.4× more bandwidth. That's aarch64/Blackwell
   (`sm_121`) support gaps in `torch.compile`/Triton, not hardware — and
   it's the larger of the two gaps.

### Ranked next moves (software, untested, cheapest first)

1. **Trim `max_seq_len`** in the checkpoint config (currently 32768) — the
   same change got the community RTX 3090 a 1.7× speedup. One JSON edit +
   restart, zero new dependencies.
2. **Tune `torch.compile` mode** (`max-autotune` / `reduce-overhead`) in
   `fish_speech/models/text2semantic/inference.py`'s `init_model()`.
3. **SGLang-Omni migration** — the biggest theoretical win (paged KV cache,
   CUDA graphs, continuous batching) but its pinned deps
   (`flashinfer_python`, `flash-attn-4`, `nixl-cu13`) are typically
   x86_64-only wheels; aarch64/GB10 support unconfirmed. Spike, not a sure thing.
4. **vLLM-Omni migration** — vLLM itself has a validated GB10/`sm_121`
   build already in community use, making this the more promising serving
   migration, but the Fish Speech recipe itself is only demonstrated on
   A800/H100 upstream — untested on GB10.
5. **A discrete GPU** — see Hardware upgrade options below; this is the
   certain fix if software wins stall out.

## Voice Lab — automated YouTube-to-voiceclone pipeline (built 2026-09-10)

AJ's ask: as fully automated a voice-cloning workflow as possible, starting
from a YouTube video, with vocal separation/noise removal, rudimentary
wave-editing to trim snippets, and the ability to chain several cleaned
snippets into one high-quality voiceprint — complete with transcription and
tagging, natively inside the dashboard (not a separate script).

**Status: working baseline shipped and verified end-to-end through a real
browser session** (not just curl-tested) — see Verification below.

### Pipeline stages

```
YouTube URL + timestamp
   → yt-dlp fetch (full audio, cached once as source.wav)
   → drag-handle waveform trim (re-cuts from the cache in <0.1s, no re-download)
   → Demucs vocal separation (htdemucs two-stems, GPU)
   → ffmpeg light denoise on the isolated vocal stem
   → faster-whisper transcription (CPU — see note below)
   → [repeat for more snippets]
   → chain: concatenate snippets with brief silence gaps + join transcripts
   → publish: POST the combined clip + transcript to Fish as one named voice
```

Each stage is independently re-runnable (e.g. re-trim without re-downloading,
re-transcribe without re-separating) so a bad automatic step never forces
starting over.

### Architecture

- **New backend service**: `voiceprep-api.service` (systemd user service,
  FastAPI/uvicorn) on the **Spark**, port **8090**. Own Python venv at
  `/home/aj/voiceprep/.venv` — deliberately isolated from Fish's own venv
  so neither can break the other, but **reuses Fish's already-working
  CUDA torch build** via a `.pth` path injection rather than reinstalling
  torch from scratch (faster, avoids fighting Blackwell/aarch64 wheel
  availability a second time).
- **Dashboard proxy**: `server.mjs` forwards `/voiceprep/*` to the Spark
  service, same raw-`http.request()` pattern as the existing Fish proxy
  (see the hidden-`fetch()`-timeout lesson in the engineering log above —
  applied here from the start this time).
- **Frontend**: `public/voicelab.js`, a plain deferred `<script>` (not a
  module) so it can reuse a few helpers the main module script exposes on
  `window` (`fetchStructured`, `loadVoices`, `fmtDur`).
- **Waveform editor**: hand-rolled canvas renderer (decodes the fetched wav
  via `AudioContext.decodeAudioData`, draws min/max buckets) with two
  draggable trim handles — no external waveform library needed for this
  baseline.

### Why chaining needed real audio concatenation

Fish's `/v1/tts` one-shot endpoint *does* accept multiple `{audio, text}`
entries in its `references[]` array (confirmed against Fish's own docs —
this is meant to give a single generation more vocal/emotional range from
several examples). But the **persistent, named-voice** endpoint,
`/v1/references/add`, only accepts exactly one audio file + one transcript
per saved voice (confirmed via its schema's 422 validation error — no
array support). So "chaining snippets into one voiceprint" genuinely
requires concatenating the cleaned audio (ffmpeg concat demuxer, with a
~400ms silence gap between clips so words don't smear together) and joining
the transcripts with spaces, before the single publish call. This is the
architecturally correct approach, not a workaround.

### Known constraint: transcription runs on CPU, not GPU

`faster-whisper`'s backend, `ctranslate2`, has no CUDA build published for
aarch64 on PyPI (a gap in the wheel ecosystem, not a config issue). Vocal
separation (Demucs) still runs on the Spark's GPU and is fast; transcription
falls back to CPU (`int8` compute type). For the short clips this pipeline
is meant to process (voice-clone reference snippets, not full podcasts),
this is an acceptable trade, not a blocker — but it's the one part of the
pipeline that wouldn't scale well to long-form audio without revisiting.

### Setup pitfalls worth knowing before touching this again

- `sphn` (a Rust-based audio codec Demucs imports) has no aarch64 wheel and
  needs a Rust toolchain (`rustup --profile minimal`, no sudo) plus
  `CMAKE_POLICY_VERSION_MINIMUM=3.5` in the environment to build — a
  transitive C dependency's old `cmake_minimum_required` gets flatly
  rejected by modern CMake otherwise.
- systemd user services get a minimal `PATH` — `/usr/bin` (ffmpeg/ffprobe)
  is on it, but a venv's own installed console scripts (`yt-dlp`) are NOT
  unless referenced by full path. Works fine under a manually-activated
  venv shell, fails silently under systemd — a good general trap to
  remember for any future Spark service.

Full blow-by-blow (commands, exact errors, fixes) in the Hermes skill
`home-lab-infrastructure`, `references/fish-speech-tts.md`.

### Verification performed (2026-09-10)

Not just "the code runs" — ran the **actual click path in a real browser**:
spun up headless Chrome, drove it over raw CDP (no puppeteer needed — just
Python's `websockets` lib talking the protocol directly, since this
environment's sandboxed browser tool couldn't reach a local dashboard),
clicked through Fetch → Separate → Denoise → Transcribe → Add to chain →
Publish on a real YouTube clip, confirmed zero console errors, and confirmed
the resulting voice actually appeared in Fish's `/v1/references/list` —
then deleted all test artifacts (test voice, test jobs, temp scripts).

### Not yet built (AJ said full scope — this is the working baseline first)

- Multi-video batch import (currently one clip fetched at a time).
- Finer waveform precision — current editor is drag-handle + numeric
  start/end only, no zoom-to-sample or scrub-while-playing.
- Any UI-side tagging step for the transcript (Fish's free-form control
  tags like `[whispers]`) — right now tags would have to be typed manually
  into the transcript field before chaining/publishing.

## Hardware upgrade options (researched 2026-09-10)

AJ asked whether his existing **MSI gaming laptop** could run Fish instead
of/alongside the Spark, then whether a discrete card is worth buying, new vs
used.

### The gaming laptop's GPU is smaller than it looks on paper

Its RTX 4080 is the **mobile/laptop chip (AD104)**, not the desktop one —
a materially different, cut-down part:

| | Spark GB10 | RTX 4080 **Laptop** | Desktop RTX 3090 (reference) |
|---|---|---|---|
| VRAM | 128GB unified | **12GB** | 24GB |
| Bandwidth | 273 GB/s | 432 GB/s (1.6×) | 936 GB/s (3.4×) |
| Arch | sm_121, brand-new ARM Blackwell | sm_89, mature Ada/x86_64 | sm_86, mature Ampere |

**VRAM is the disqualifier, not bandwidth.** Fish's own docs recommend 24GB+;
multiple GitHub issues report OOM on 16GB cards with the stock `--compile`
setup (~20-22GB observed usage). 12GB is below what even 16GB cards
struggle with. An unofficial NF4 4-bit quantization fork
(`groxaxo/fish-speech-int4-patch`) claims to fit 12GB cards, but its own
users report mixed OOM/slowness results, and quantizing risks the exact
voice-acting quality AJ values. **Verdict: not attempted — VRAM-blocked, and
the fallback fork is unproven and risks quality.**

### Used RTX 3090 pricing (checked live, 2026-09-10)

| Source | Price | Notes |
|---|---|---|
| DBA.dk, ASUS Strix OC, private, Næstved | 8,000 kr (~€1,073) | cheapest, needs in-person FurMark/HWiNFO64 inspection |
| DBA.dk, MSI Gaming X Trio, private | 10,000 kr (~€1,340) | private |
| DBA.dk, MSI Suprim X + AIO watercooling | 10,500 kr (~€1,410) | AIO adds a long-term failure point |
| **eBay.de, Dell OEM refurb, "Sehr gut" grade** | **~€1,349 (~10,060 kr)** | **recommended** — pre-tested, free EU delivery, free returns, 425 positive ratings |
| Market reference (eBay sold median, global) | €1,019–1,180 | confirms DBA pricing is in-band |

**Recommendation: the eBay.de refurbished Dell OEM at ~€1,349.** A used
3090's real risk is silent VRAM/thermal damage from mining wear — every
buying guide's advice boils down to "stress-test with FurMark/HWiNFO64 for
30+ min, check memory-junction temp stays under 95°C." Paying the ~2,000 kr
premium over the cheapest private DBA listing buys a pre-tested card with
free returns instead of a solo diagnostic trip. Budget alternative: the
8,000 kr ASUS Strix OC in Næstved, IF willing to run the stress test
in-person before paying.

### New vs. used — simple price/performance

VRAM ≥24GB is a hard requirement, which **eliminates every current new card
under the RTX 5090** (4070 Ti Super/5070 Ti are 16GB — disqualified
regardless of price):

| Card | VRAM | Price (DKK) | Speed vs. used 3090 baseline |
|---|---|---|---|
| **Used RTX 3090** (recommended) | 24GB | ~10,000 kr | 1.0× (baseline) |
| RTX 4090 (new, discontinued) | 24GB | ~20,000+ kr (inflated leftover stock) | ~1.1× — bad value, avoid |
| RTX 5090 (new) | 32GB | ~30,000 kr | ~1.7–2× |

**Used 3090 wins price/performance by ~4×** (≈420 kr per unit of speed vs.
≈1,650–1,765 kr/unit for a 5090). Fish's workload is bandwidth-bound and
VRAM-gated, not compute-bound — it doesn't need the 5090's extra headroom.
**Decision: used RTX 3090 is the correct buy for this specific job**; a
5090 would only make sense if AJ wanted the extra throughput for other
workloads (Comfy/LLM) too and had budget to spare.

Note: a 3090 is a desktop card — using it means either an eGPU enclosure
(Thunderbolt) off the gaming laptop, or a small standalone box on the LAN
next to the Spark. TTS/LLM inference barely touches the interconnect (model
stays resident in VRAM; only text crosses the cable), so an eGPU's
bandwidth cap wouldn't meaningfully hurt inference the way it would gaming.
Not yet decided which enclosure path AJ wants.

## Dashboard engineering log (2026-09-10)

A single working session; logged chronologically since several bugs and
features stacked on each other.

1. **Dashboard unreachable from other LAN devices.** Root cause:
   `server.mjs` was hardcoded to `server.listen(PORT, '127.0.0.1', ...)` —
   loopback-only, so even the laptop's own LAN IP couldn't reach it from
   elsewhere. Fixed to `'0.0.0.0'`.
2. **Recurring `HTTP 502 fetch failed` at the 5-minute mark.** Root cause:
   Node's built-in `fetch()` (undici) has its own hidden 300s
   `headersTimeout`/`bodyTimeout` that **cannot be overridden** via
   `fetch()`'s own `AbortSignal` — the dashboard's own 30-minute timeout
   never got a chance to matter. Fixed by replacing the Fish-proxy's
   `fetch()` call with a raw `http.request()` (`proxyRequest()` helper),
   which has no hidden ceiling. Verified both directions: a slow-but-alive
   request now survives past 5 minutes; a truly-hung one still aborts
   correctly at the configured limit. **General lesson: never trust Node's
   built-in `fetch()` for proxying long-running upstream calls.**
3. **A real generation backlog** (several long/heavily-tagged test requests
   queued back-to-back, one took 612s at 1.67 tok/s) was cleared by
   restarting `fish-speech-api.service` on the Spark — confirmed
   **killing the client never stops Fish's server-side GPU work**; only a
   service restart does, since Fish has no cancel endpoint.
4. **Researched Fish's real text-length limits** from its own
   `inference.py`: hard prompt-token ceiling is 30,720 tokens
   (`max_seq_len - 2048`); `max_new_tokens` (default 1024) is a hard
   per-request output ceiling; **no server-side chunking exists for plain
   text** — `chunk_length` only groups multi-speaker `<|speaker:N|>` turns,
   a normal request is always one uninterruptible batch. This confirmed
   client-side chunking was the only path to interruptibility.
5. **Built the AI-assisted tag writer** — a `/llm/generate` route on
   `server.mjs` calls Qwen3.8 (`qwen3.8-27b-aggressive-q5` on the Spark's
   :8014, thinking off) to either **Rewrite** existing text with tags added,
   or **Instruct**-generate new tagged text from a prompt (e.g. "a spooky
   7-year-old boy's rhyme" — tested, produced contextual invented tags like
   `[shivering breath]`, not just the README's fixed examples). A **tag
   density slider** (0–100%) maps to five prompt-engineered tiers from "no
   tags" to "stress-test maximum."
6. **Built the chunk queue + Outputs CRUD.** Client-side sentence-boundary /
   tag-aware / fixed-word-count chunking; chunks run sequentially, a
   `waiting` chunk cancels for free, a `running` one is honestly labeled as
   uncancellable (Fish has no cancel endpoint). A live chunk-size-vs-RTF
   table lets AJ empirically find the best chunk size on this box — no
   universal answer exists. Separately, every successful generation from
   any tab now **auto-saves** server-side (`/outputs` CRUD: list/fetch/
   delete-one/delete-all) with disk hygiene (`pruneOutputs()`: 24h
   retention, 500MB cap, runs every 15 min) — this fixed a real gap where
   generated audio only ever lived in one browser tab's memory.
7. **Merged Generate + Chunk queue into one page** — a "Split into chunks"
   toggle switch on Generate reveals chunk controls and repurposes the same
   Generate button ("Build & run queue"); results render in one shared
   panel instead of two separate tabs.
8. **Visual redesign** matching Agora (see Dashboard section above).

Full technical detail, code-level rationale, and verification steps for
every item above: Hermes skill `home-lab-infrastructure`,
`references/fish-speech-tts.md`.

## Open items for next session

- **AJ will test baseline functionality himself** when back from shopping —
  expect bug reports on the Voice Lab flow specifically (it's brand new and
  only machine-verified so far).
- **Git repository — not yet set up.** `~/Desktop/Hermes/fish-tts-bench/`
  has no git history at all yet (unlike [[Agentic Chatroom]], which is
  already a local repo). AJ wants this done this session — decide local-only
  vs. remote, author identity, `.gitignore` (definitely exclude
  `public/data/` outputs/cache if any, node_modules, and anything under
  `/home/aj/voiceprep/` on the Spark side since that's a separate host/repo
  concern, not this repo's).
- **AJ will lay out refinement wishes** after testing — likely candidates
  given what's already flagged as "not yet built" above: multi-video batch
  import, finer waveform precision, in-UI tag insertion for transcripts.
  Don't assume these are the asks — wait for AJ's actual list.

## Related notes

- [[LAN notes]] — Spark hardware/service inventory this page details.
- [[Agentic Chatroom]] — the project most likely to
  consume this TTS engine; also the source of the dashboard's visual design.

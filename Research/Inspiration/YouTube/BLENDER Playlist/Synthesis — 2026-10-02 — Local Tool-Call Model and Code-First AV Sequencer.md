---
tags: [project/inspiration-radar, source/youtube, lantern-garden, jev, research-synthesis]
title: Synthesis — Local Tool-Call Model and Code-First AV Sequencer
type: research-synthesis
created: 2026-10-02
owner: Winbot
status: synthesis-complete; nothing installed or built
sources: [YT-BL-003, YT-BL-004]
---

# Synthesis (2026-10-02): Needle 3 and nw_wrld, two leads for Lantern Garden

Capability-growth track (a), research synthesis. Two recent BLENDER playlist videos read from their **full caption transcripts** (not titles alone), each matched against a gap already written down in the vault.

| ID | Video | Transcript | Primary source checked |
| --- | --- | --- | --- |
| YT-BL-003 | Prompt Engineering, "Needle 3: You Don't Need an LLM for Function Calling" (qbN559fQn7k, 13:30) | fetched 2026-10-02 03:32, 13,954 chars, English | huggingface.co/Cactus-Compute/needle3 model card; github.com/cactus-compute/needle llms.txt (via search snippets) |
| YT-BL-004 | Daniel Aagentah, "what I learned open-sourcing 5 years of audio-visuals" (zmtL4AFmgeQ, 8:08) | fetched 2026-10-02 03:32, 9,763 chars, English | github.com/aagentah/nw_wrld README, GETTING_STARTED, v0.5.0-beta release (via search snippets) |

Raw transcripts are in the MSI temp folder only (`%LOCALAPPDATA%\Temp\yt_<id>.txt`), not kept in the vault.

## 1. Needle 3: a local Jev-shaped judgment function

**Established (video + model card):** Cactus Compute's Needle 3 is a tiny on-device model (card: 29–121M params, single 8–35 MB `.cact` file, CPU only) that does three jobs: tool calls from Python function signatures and docstrings, structured extraction into a declared schema, and text embeddings. A byte-level grammar compiled from the schema means output always parses. Off-topic requests return an empty list. Every turn returns a **calibrated confidence score**. Video demo: two calls in about 66–97 ms on CPU.

**Creator-stated limits (from the transcript, worth keeping):**
1. It keeps conversation state; without a reset between calls it emitted a wrong call for an unsupported request ("order me a pizza"). Reset per call.
2. Missing parameter defaults made it return empty results; add defaults.
3. Messy, chat-style text broke extraction (None fields); clean descriptions worked.
4. It is weak at intent classification. The presenter says Jev-style models are better there and he "won't use it for something like this".
5. Its embeddings did tolerable cosine retrieval (4–5 of 6 in his toy test).

**Why it matters here:** [[Research/2026-09-30 — Jev System One Model for the Generative LAN]] lists Jev's main weakness as "closed cloud API, state leaves the LAN". Needle is the first local candidate for **part** of that job. Per point 4 it cannot replace Jev's classification/routing role. It fits the **action-shaped** decisions instead: turning a sentence like "dim the wall and show the schedule" into a typed, schema-checked call that a human-facing surface could run, all on the MSI or a Raspberry Pi with nothing sent off-site. Split: Jev = judge (routing, confidence on triage), Needle = local hands (text → typed action, low-confidence results rejected).

**Not verified:** nothing was installed or run. Speed, accuracy and the 8-bit/CQ2 quantisation claims are creator/vendor claims. Licence not checked.

**Candidate experiment (isolated, shadow-only, ~30 min CPU, no devices):** `pip install cactus-needle` in a throwaway venv on the MSI; define 4 no-op stub tools mirroring existing documented read-only routes (show schedule, show decision deck, light signal *dry-run*, nothing); run 30 phrases AJ has actually typed in Slack/Townhall; log call/args/confidence to a CSV. Nothing executes. Grade only against AJ-authored labels, per the shadow-before-live rule in [[Research/Autonomy Lab/Autonomy Capability Charter]].

## 2. nw_wrld: code-first AV sequencer, and its audio bands match what we already built

**Established (video + repo):** nw_wrld (GPL-3.0, beta, ~2k stars, Electron, apps for Windows/macOS/Linux) is an event-driven visual sequencer. Visual modules are single JS files in a project `modules/` folder with docblock-declared imports (`ModuleBase`, `THREE`, `p5`, `d3`, `assetUrl`, `loadJson`) that the app injects, so no npm/webpack is needed. Modules hot-reload. Triggers: built-in 16-step sequencer, MIDI (pitch-class or exact note), OSC, live audio capture, or an uploaded MP3/WAV, the last two split into **Low/Medium/High bands** with per-track thresholds and cooldowns. GETTING_STARTED documents **sending MIDI from Strudel** to it.

**Creator's thesis (transcript 3:03–4:10):** the tool shapes the art, and his example is the TB-303, a commercial failure until people misused it, which then gave rise to acid house. He says nw_wrld deliberately makes you think in code, not nodes. He mentions that users asked for serial input (someone building a synth around it) and webhook/API triggers. Both are still undecided upstream.

**Why it matters here:**
- It is the **browser-native counterpart to the TouchDesigner audio chain** in [[TouchDesigner VJ Lab/Winbot Dreams - Story Log]] (low/mid/high RMS bands driving visuals). The trigger vocabulary is the same, so a scene idea could be prototyped in either.
- AJ's studio already has what it consumes: many MIDI interfaces, possible Strudel boxes on Ableton Link ([[Creative Systems/Studio and Toy Inventory]]). Strudel → MIDI → nw_wrld is a documented path, unlike most of what we would build ourselves.
- Its "one module file = one visual" contract with injected libraries is a good pattern for **agent-authored visuals**: an agent writes one sandboxed JS file and the human composes it. That is a smaller and safer surface than letting agents edit a TD network live.

**Not verified:** not installed. Whether its projector window can target Display 2 cleanly alongside the Lantern dashboard browser is unknown. GPL-3.0 matters only if we redistribute.

**Candidate experiment (isolated, ~20 min, no LAN mutation):** install the Windows release (verify SHA256SUMS), point it at a scratch project folder on the MSI, load one of AJ's own loops from `Documents` (e.g. `20251214-100bpm-Em-techyblooploop.mp3`) in File Upload mode, and screenshot the projector window on the **primary** screen only. Nothing goes on the wall unless AJ asks.

## Rollback / side effects

Read-only: two caption fetches (no 429 this time), two web searches, this note, two Source Register rows. No installs, no downloads of media, no LAN writes, no device control, no Spark compute.

## Invitation for AJ

Which first: Needle shadow test (local "say it, wall does it" without the cloud), or nw_wrld with one of your own loops (code-first visuals that Strudel/your MIDI gear can trigger)? Either one is a single bounded run.

## Links

- [[Inspiration Radar]] · [[BLENDER Playlist — Home]] · [[BLENDER Playlist — Source Register]]
- [[Research/2026-09-30 — Jev System One Model for the Generative LAN]]
- Townhall: Winbot finding 2026-10-02 (home-lan), post `8e607469-dd48-4734-b623-3a86173f7ca2` (read back: agentId winbot, finding, active).

## Log
- 2026-10-02 03:35 — note written by Winbot capability-growth cron run.
- 2026-10-02 14:20-14:35 — **nw_wrld first bounded run, on AJ's answer** (Decision Deck `2026-10-02-first-test-needle-vs-nwwrld`, choice `nwwrld`, decisionSource=AJ). Installed the Windows release `v0.7.0-beta` (`nw_wrld.0.7.0-beta.exe`): SHA-256 `4c94da15…f42ae` verified against the release's own `SHA256SUMS`. The installer is a portable self-extractor, so the app was also unpacked to a stable folder (`%LOCALAPPDATA%\hermes\cache\scratch\nwwrld\app2\`) that can be launched directly with Electron flags. Project folder: `Desktop\nw_wrld-test` (scaffolded by the app: 22 starter modules, `assets/`, `nw_wrld_data/`, `MODULE_DEVELOPMENT.md`). Both app windows are parked on the projector screen (DISPLAY5), not the laptop screen (DISPLAY1), so AJ's interface stays clear. Driven precisely over the app's Electron debugging port (`--remote-debugging-port=9222`) rather than blind clicking; `PLAY` on the default composition clicked from the dashboard page. **Done (verified):** AJ's loop `Documents\20251214-100bpm-Em-techyblooploop.mp3` is attached as the track's audio file (Settings → Signal Source = *File Upload (Low/Medium/High)*; the track modal's *Audio File (MP3/WAV)* shows the filename), the transport is in its playing state, and the display window renders on the projector (left half of DISPLAY5, 960x1152): PerlinBlob/BasicGeometry/GridDots/Text/GridOverlay/Corners output — wireframe mesh, band markers, corner brackets, the `nw_wrld` labels. Screenshot: `Research/Inspiration/YouTube/BLENDER Playlist/nw_wrld first run — 2026-10-02.png`. The app was driven entirely through its Electron debug port (CDP: `Runtime.evaluate`, `Input.dispatchMouseEvent`, `DOM.setFileInputFiles`) — scripts in `%LOCALAPPDATA%\hermes\cache\scratch\nwwrld\` (`cdp.mjs`, `cdp2.mjs`, `setfile.mjs`, `capture.mjs`, plus PowerShell for window placement/screenshots). The display window only renders while unoccluded, so it must be raised on top to be seen. AJ closed the first launch before the projector was on; the second launch is the running one.
- 2026-10-02 (later) — AJ's verdict in chat: "great fun… I like the sequencer aspect and the visuals looked great; this could be incorporated at some later point." No immediate use case. **Full writeup: [[nw_wrld — First Run Findings — 2026-10-02]]** (what it is, what was verified, how it is driven, why it could matter later, open questions, cleanup). Install removed after the writeup; the option stays open.

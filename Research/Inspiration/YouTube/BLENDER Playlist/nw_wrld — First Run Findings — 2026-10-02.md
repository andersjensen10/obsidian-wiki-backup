---
tags: [type/finding, inspiration-radar, source/youtube, av-sequencer, creative-systems, lantern-garden]
created: 2026-10-02
owner: Winbot
status: tested end-to-end on the MSI (one bounded run), removed afterwards; kept as a candidate for later
---

# nw_wrld — first run findings (2026-10-02)

Full writeup of the bounded test AJ picked on the Decision Deck (`2026-10-02-first-test-needle-vs-nwwrld`, choice `nwwrld`, `decisionSource=AJ`) after the research synthesis in [[Synthesis — 2026-10-02 — Local Tool-Call Model and Code-First AV Sequencer]]. Video: Daniel Aagentah, "what I learned open-sourcing 5 years of audio-visuals" (YT-BL-004).

**AJ's verdict after seeing it (2026-10-02, in chat):** "great fun… I like the sequencer aspect and the visuals looked great; this could be incorporated at some later point." No immediate use case — this note is the record so the option stays open.

## 1. What it is

nw_wrld (`github.com/aagentah/nw_wrld`, GPL-3.0, beta, Electron) is an event-driven **audio-visual sequencer**, not a node/generative-art tool. Visuals are single JavaScript files in a project's `modules/` folder; the app injects `ModuleBase`, `THREE`, `p5`, `d3`, `assetUrl`, `loadJson` as docblock-declared imports, so no npm or webpack is needed and edits hot-reload. Triggers can be the built-in 16-step grid, MIDI, OSC, live audio input, or an uploaded audio file split into **Low / Medium / High bands** with per-band thresholds and a cooldown. It ships 22 starter modules (PerlinBlob, GridDots, Text, SpinningCube, ImageGallery, ZKProofVisualizer, …).

The shape that matters for us: **a channel is not "a band" or "a note" — it is a trigger**, and a module exposes named methods (`show`, `hide`, `scale`, `rotate`, `opacity`, `background`, …) that a step fires. That is the same vocabulary as the Winbot Dreams TouchDesigner audio chain ([[TouchDesigner VJ Lab/Winbot Dreams - Story Log]]) with a different authoring surface (one JS file vs a node network).

## 2. What was actually run (verified)

- Windows release `v0.7.0-beta` (`nw_wrld.0.7.0-beta.exe`, 102 MB). **SHA-256 verified** against the release's own `SHA256SUMS`: `4c94da159055d23be506c592768122dc55ce4f91c53d4e2ab06a1ec3135f42ae`.
- Project folder created at `Desktop\nw_wrld-test`; the app scaffolded itself: `modules/` (22 files), `assets/{images,models,fonts,json}`, `nw_wrld_data/`, `MODULE_DEVELOPMENT.md`, `README.md`.
- Settings → **Signal Source = File Upload (Low / Medium / High)** (the other four radios are Sequencer (Pattern Grid), External MIDI, External OSC, External Audio). In this mode the per-module channels are relabelled **LOW / MEDIUM / HIGH**, and the actual audio file is chosen per-track in the *Edit Track* modal (*Audio File (MP3/WAV)* → UPLOAD / CLEAR).
- **AJ's own loop attached:** `Documents\20251214-100bpm-Em-techyblooploop.mp3` (the app's label showed the filename), transport in its playing state.
- **Output rendered on the projector**: the display window is a right-half-size pane (960×1152 at 1080p, `Display: Aspect Ratio → Default (Right 1/2)`; Full Screen / 16:9 / 9:16 / 4:5 are the alternatives). Visible output: PerlinBlob's wireframe mesh with concentric rings, grid dots, corner brackets, `nw_wrld` labels.
- Evidence: `nw_wrld first run — 2026-10-02.png` in this folder (screen capture of the projector display, app on the left half, AJ's own browser untouched on the right).

## 3. How it was driven (reusable technique)

The installer is a portable self-extractor: it unpacks to `%TEMP%\<random>\nw_wrld.exe`, deletes that on exit, and leaves **no install directory and no uninstall registry entry** — so a naive "where did it install?" search finds only `%APPDATA%\nw_wrld` (the Electron profile). Extraction of `$PLUGINSDIR\app-64.7z` with 7-Zip gave a stable app folder that can be launched with Electron flags.

With `--remote-debugging-port=9222` the app is fully drivable over CDP (`Runtime.evaluate`, `Input.dispatchMouseEvent`, `DOM.setFileInputFiles`, `Page.captureScreenshot`) with plain Node (`WebSocket` is global from Node 22) and no dependencies: click in-app buttons via JS, use **real** dispatched mouse events only where a native dialog must open, attach the audio through the hidden `input[type=file]` (no file-picker window ever appears), and read the app's own labels for proof. Two traps: evaluate against the right page (`/json/list` returns both the dashboard and the output window — the same script silently reports nonsense against the wrong one), and **an occluded Electron window renders blank** — the display window must be raised to the front before any capture.

Procedure recorded as skill `electron-app-driving` (Windows window placement, UIA for native dialogs, the occlusion trap, DPI caveat).

## 4. Why it could matter later (no decision taken)

- **Sequencer mindset, not timeline mindset.** Steps fire named methods on modules — a compact way to compose *behaviour* (reveal, scale, invert) rather than keyframes. If we ever want the wall or a stage visual to be driven by AJ's actual patterns, this is a concrete alternative to writing TouchDesigner networks.
- **Same trigger vocabulary as what exists.** Low/Mid/High bands match the Winbot Dreams audio chain, and Strudel → MIDI → nw_wrld is documented upstream, which suits the studio's MIDI interfaces and possible Strudel boxes ([[Creative Systems/Studio and Toy Inventory]]).
- **Agent-authored modules are a small, safe surface.** "One module file = one visual" with injected libraries means an agent can propose a single sandboxed JS file that AJ drops into `modules/` — a much smaller blast radius than letting an agent edit a live TD network.
- **It is not a replacement for Jev/Needle work** and has no bearing on the decision layer; it is a creative-output tool.
- GPL-3.0 matters only if we redistribute anything built on it.

## 5. Open questions (not blocking)

1. Whether the output window can be a clean full-screen target on DISPLAY5 alongside the Lantern dashboard browser — untested; the aspect-ratio setting suggests yes.
2. Whether the file-upload bands actually modulate the visuals live (the run showed level thresholds and a "Live File Levels" readout, but the visual correlation was not measured).
3. Authoring cost for a real module: one agent-written file, or does the injected-API surface need a shim?

## 6. Cleanup (2026-10-02, after the writeup)

Install removed: running app stopped, extracted app folder, the 102 MB installer and all scratch work deleted from `%LOCALAPPDATA%\hermes\cache\scratch\nwwrld\`, the Electron profile `%APPDATA%\nw_wrld` deleted, and the test project folder `Desktop\nw_wrld-test` removed. Verified after the fact: no `nw_wrld` process, no `%LOCALAPPDATA%\Programs\*wrld*`, no `%TEMP%\<id>\nw_wrld.exe`, nothing left on the Desktop. The generic driving scripts are preserved in the skill **`electron-app-driving`** (`scripts/cdp.mjs`, `scripts/set-file-input.mjs`, `scripts/win.ps1`); the only project artefact kept is the screenshot above. Reinstalling is a download plus the extraction step in §3.

## Links

- [[Synthesis — 2026-10-02 — Local Tool-Call Model and Code-First AV Sequencer]] · [[BLENDER Playlist — Source Register]] · [[BLENDER Playlist — Home]]
- [[TouchDesigner VJ Lab/Winbot Dreams - Story Log]] · [[Creative Systems/Studio and Toy Inventory]] · [[Inspiration Radar]]
- Townhall: this test was chosen by AJ on the Decision Deck; the run is logged in the synthesis note above.

---
tags: [project/agora, type/feature-request]
---

# Agora: Architectural & Interaction Improvements Blueprint
### Elevating the Local Agentic Multi-Persona & Media Studio

**Author:** QA & UX Architecture Review  
**Date:** September 6, 2026  
**Target:** Agora (`apps/web`, `apps/server`, `packages/`)  
**Objective:** Transform Agora from a linear text chat prototype into a cutting-edge, local-first multimodal agent studio integrating LLMs, multi-engine TTS, ComfyUI image diffusion (Flux), and video synthesis (LTX-2.3).

---

## 1. High-Level Vision: From Linear Chatroom to Spatial Agent Studio

Traditional AI chat interfaces are constrained by the **1D vertical scrolling document paradigm** inherited from 1960s teletype terminals. When multiple autonomous personas, media generators (images and videos), and audio streams are forced into a single vertical stream:
1. Turn-taking feels chaotic or overly rigid.
2. Long-running GPU tasks (e.g. 3-minute video synthesis) block or vanish in the chat flow.
3. Spatial presence and immersion of characters are lost.

Agora should pioneer a **Spatial Stage & Director's Desk** interaction model—giving the user effortless control over conversational rhythm, multi-agent debate, media creation, and character memory.

---

## 2. Interaction Paradigm & Conversational Floor Control

### 2.1 "Director Mode" vs. "Immersion Mode"
Provide a toggle in the top bar:
- **Immersion Mode (In-Character):** Clean roleplay interface. System artifacts, prompt mechanics, and technical logs are concealed. Stage directions (`*action*`) render with elegant atmospheric typography.
- **Director Mode (God View):** Exposes live character states:
  - **Thought Bubbles / Reasoning Stream:** View the hidden `message.reasoning_content` (from reasoning models like `gpt-oss-120b`) before or alongside the dialogue.
  - **Floor Controller:** A visual radar showing who has the floor, who wants to speak next, and turn-taking priorities.
  - **Persona Steering Slider:** Dynamically nudge a persona's current emotional state (e.g., increase *Assertiveness* or *Humor* mid-scene) without editing the raw system prompt.

### 2.2 Fluid Floor Management & Turn Handoffs
Replace the confusing "On mention" fallback behavior with clear, visual turn controls:
1. **Pass-the-Mic (Manual Floor):** Click a persona's avatar in the room header to grant them the floor immediately.
2. **Auto-Banter with Visual Queue:** When personas converse with each other:
   - Display an avatar queue chip at the bottom: *"Up next: Mira (replying to Iris)..."*
   - Provide a 2-second "Pause / Interject" button, allowing the user to seamlessly jump into the conversation before the next persona speaks.
3. **Branching Transcript Tree (Non-Destructive Regeneration):**
   - When a persona generates a reply, allow regenerating without deleting downstream history.
   - Display a turn pager `< 1 / 3 >` on the message bubble.
   - Users can fork the conversation at any beat to explore alternative story paths.

---

## 3. ComfyUI Media Generation: Production Studio Experience

Agora already has functional ComfyUI image (Flux) and video (LTX-2.3) pipeline integration. Elevating this to a production-grade experience requires making media generation interactive, inspectable, and controllable.

### 3.1 In-App Media Studio & Lightbox
Clicking any generated image or video in chat should open a full-screen **Media Studio Lightbox**:
- **Metadata HUD:** View Seed, Sampler, Steps, CFG Scale, Model/Checkpoint, and generation time (e.g. `20 steps in 4.8s`).
- **One-Click Actions:**
  - `Generate Variations` (maintains prompt, randomizes seed).
  - `Upscale / Refine` (triggers an in-place high-resolution latent upscale).
  - `Animate with LTX-2.3` (sends the still image directly to an Image-to-Video workflow).
  - `Set as Persona Portrait` (instantly updates the speaking persona's avatar).
  - `Copy Prompt / Workflow JSON`.

### 3.2 Integrated Media Generator Modal (Killing `window.prompt`)
Replace the native `prompt()` with a slide-over **Media Composer**:
- **Prompt Field:** Auto-completes character appearance tags and room atmosphere prompts.
- **Workflow Preset Selector:** Dropdown between `Flux Dev (Quality)`, `Flux Schnell (Fast)`, `LTX-2.3 Video (24fps / 5s)`, and custom user workflows.
- **Reference Image Attachment:** Drag-and-drop an image to pass into IP-Adapter or ControlNet for character consistency.
- **Aspect Ratio Picker:** Visual ratio buttons (`1:1 Square`, `16:9 Cinematic`, `9:16 Portrait/Phone`, `4:3 Classic`).

### 3.3 GPU Job & Resource Management Drawer
Running multi-minute video generation or heavy diffusion alongside 120B parameter LLM inference can saturate local VRAM:
- **Global Generation Queue Widget:** A minimized bottom-right floating pill showing active GPU jobs (`Flux: Step 12/20`, `LTX-2.3: Frame 45/120`).
- **Hardware Telemetry:** Live GPU VRAM usage percentage and temperature (polled from ComfyUI / systemd metrics).
- **Graceful Job Cancellation:** A dedicated `Abort Job` button that immediately calls ComfyUI's `/interrupt` API to reclaim GPU memory instantly.

---

## 4. Multimodal Voice & Audio: The Living Stage

Local TTS (Piper, Kokoro, Fish Speech) is one of Agora's greatest assets. Moving beyond simple post-hoc message playback will make conversations feel alive.

### 4.1 Low-Latency Streaming Sentence Synthesis
Currently, TTS waits until the LLM finishes generating the entire paragraph before submitting text to the TTS engine.
- **Sentence-Chunk Pipeline:** As the LLM streams tokens, split on sentence boundaries (`.`, `!`, `?`).
- Immediately dispatch Sentence 1 to Kokoro/Piper while Sentence 2 is still generating.
- Result: **Audio playback starts within 400ms of user submission**, eliminating the awkward 10-second silence on long responses.

### 4.2 Conversational Voice Mode (Full-Duplex VAD + STT)
- **Hands-Free Chat:** Add a persistent microphone button in the composer with client-side Voice Activity Detection (VAD) via `@ricky0123/vad-web` or Silero VAD.
- **Local Whisper Transcription:** Stream speech audio to a local Whisper instance (`whisper.cpp` or faster-whisper on the server) for instant user voice input.
- **Natural Interruption:** If the user speaks while a persona is playing audio, automatically fade out playback and yield the turn to the user.

### 4.3 Speaking Aura & Lip-Sync Visualizer
- While audio is playing for a persona, animate their avatar with a subtle, pulsating audio-reactive waveform ring or aura matching their assigned color.
- Add optional 2D sprite mouth movement or blink animation to give the personas physical presence.

---

## 5. Agentic Extensibility & Tool Execution UX

Agora already possesses an execution harness for skills (`calculator`, `web-search`, `dice`, `current-time`), but currently suppresses the UI.

### 5.1 Interactive Tool Execution Cards
When a persona triggers a skill (e.g. searching the web or checking the weather):
- Render an expandable **Tool Card** above their dialogue:
  ```
  ┌───────────────────────────────────────────────────────────┐
  │ 🌐 Web Search: "Copenhagen weather today"      [✓ 142ms]  │
  ├───────────────────────────────────────────────────────────┤
  │ 12°C, Overcast with light rain in Valby...                │
  └───────────────────────────────────────────────────────────┘
  ```
- Allow users to inspect raw tool arguments and returns.
- Provide a setting in Room World to enable or disable specific skills per room (e.g. fantasy roleplay rooms shouldn't have modern web search enabled).

### 5.2 Slash Command Palette (`/` and `Cmd+K`)
Replace the current static Command Help popup with a rich, interactive command palette:
- Typing `/` in an empty composer opens an inline autocomplete menu:
  - `/image [prompt]` — generate an image with ComfyUI.
  - `/video [prompt]` — queue an LTX-2.3 video generation.
  - `/say [persona] [text]` — force a specific persona to speak.
  - `/narrate [event]` — trigger world narration.
  - `/clear` — clear room history.
  - `/roll [dice]` — roll dice in the room.

---

## 6. Information Architecture & Ergonomics

### 6.1 Unified Persona Studio (Tabbed Redesign)
Refactor `apps/web/src/routes/personas/+page.svelte` from a monolithic scrolling page into a tabbed editor:
1. **Tab 1: Identity & Brain:** Name, avatar upload/generator, role (Character vs Narrator), system prompt, LLM connection & model selector, temperature, max tokens.
2. **Tab 2: Voice & Audio:** Voice engine selection (Piper, Kokoro, Fish), voice picker grouped by accent/gender, speed slider, live voice preview tester, reference audio upload for Fish cloning.
3. **Tab 3: Appearance & Workflow:** Appearance prompt, ComfyUI workflow template, reference images, negative prompts.
4. **Tab 4: Traits & Dynamic Memory:** Interactive trait radar chart, trait evolution log, memory list with search, pinning, and memory attribution editor.
- **Sticky Actions Bar:** Floating bottom bar with `Discard` and `Save Changes (Ctrl+S)`, with an active dirty-state indicator (`● Unsaved changes`).

### 6.2 Responsive Mobile Drawer Layout
On screens `< 820px`:
- Add a top-left hamburger icon in the room header that slides open the Rooms & Cast drawer.
- Add quick-swipe gestures to toggle between Chat, Cast list, and World Settings.

### 6.3 Universal Dialog & Modal System
Replace all 11 instances of `window.prompt()` and `window.confirm()` with a custom Svelte modal layer:
- **Confirmation Modal:** High-contrast, keyboard-navigable (`Enter` to confirm, `Esc` to cancel), with distinct danger styling for destructive deletions.
- **Secret Input Modal:** Masked input field (`type="password"`) with an eye toggle for API keys.
- **Creation Dialogs:** Purpose-built modal cards for Room creation (with theme swatch picker) and Persona creation.

---

## 7. Recommended Implementation Phasing

| Phase | Milestone | Core Deliverables |
|---|---|---|
| **Phase A: Critical Ergonomics & Fixes** | Immediate | • Fix footer status bug (BUG-01) & turn-taking mode (BUG-02)<br>• Replace native `prompt`/`confirm` with modal components (BUG-04)<br>• Add mobile sidebar drawer (BUG-03)<br>• Add navigation dirty-guard on Persona editor (BUG-06) |
| **Phase B: Multimodal & Media Studio** | Short-Term | • In-app Lightbox with metadata HUD & variations (BUG-11)<br>• ComfyUI `/interrupt` job cancellation on abort (BUG-09)<br>• Dedicated Media Generation slide-over modal<br>• Split persona editor into tabbed sections (BUG-08) |
| **Phase C: Audio & Agentic Evolution** | Medium-Term | • Sentence-streaming TTS pipeline for instant audio response<br>• Tool/Skill execution cards in chat transcript (BUG-10)<br>• Command palette (`Cmd+K` / `/` autocomplete)<br>• Non-destructive message branching `< 1/3 >` (BUG-12) |
| **Phase D: Full Studio & Voice Duplex** | Long-Term | • Full-duplex Voice Mode with local VAD & Whisper STT<br>• Live GPU resource telemetry drawer<br>• Persona visual consistency pipeline (IP-Adapter integration) |

> [!note] CEO deferral — 2026-09-09
> Phases A–C are done (see `Published`/`Active Sprint` — FR-001, FR-003 through
> FR-008). Phase D stays parked as of this note: AJ is deliberately not pulling it
> forward into the next-level-features vision sprint(s) about to be scoped. It's
> earmarked for a dedicated future **Foundation Sprint**, alongside `FR-002`
> (Spark llama.cpp parallel slots — see its own deferral note) and the Phase 4
> persistent-memory blocker (mem0 + FalkorDB, blocked on Docker/Podman not being
> installed). Senior Product Manager: don't mature Phase D into work orders until
> that Foundation Sprint is called.

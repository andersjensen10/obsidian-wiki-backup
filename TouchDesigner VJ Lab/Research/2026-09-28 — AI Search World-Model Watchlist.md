---
tags: [touchdesigner, vj, world-models, ai-search, blender, krea, ableton]
---

# AI Search World-Model Watchlist

AI Search's recent weekly AI NEWS coverage is a useful inspiration source for visual experiments—not because current world models are automatically live-performance-ready, but because their interaction ideas translate well into hybrid TD systems.

## Watchlist

- [WorldCrafter in AI Search's weekly roundup](https://youtu.be/nX0fgBL3sIM) — highlights an interactive world model with implicit 3D-aware memory and a distilled fast variant. **VJ translation:** preserve a scene/state memory outside the generative step, then use TD to keep camera motion, feedback, and compositing continuous while generated imagery arrives asynchronously.
- [Matrix Game 3.0 coverage](https://podscan.fm/podcasts/ai-search/episodes/robot-waifus-rip-sora-google-realtime-voice-glm-51-ai-brain-scans-top-open-video-model-ai-news) — reported as a 5B interactive video world model with action-conditioned, 720p streaming claims. **VJ translation:** treat performer controls as an action stream: MIDI/Push, browser XY, camera motion, and audio bands become high-level scene verbs rather than only modulation values.
- [Krea Realtime and Hunyuan World Mirror coverage](https://postsingularityinstitute.com/en/syntheses/ucignglgkvrhd4qnfcewll4a_uqiqkfk5_0w) — points toward real-time image/video transformation and camera-aware image-to-3D world ideas. **VJ translation:** use Krea for immediate manual edits/style steering, while TD owns timing, input routing, projection, and safety fallback.

## Fall experiment palette

### 1. The playable hallucination deck

- **TouchDesigner:** continuous visual engine, audio analysis, camera capture, output compositing, recording.
- **Ableton + Push:** scene changes and "verbs"—drift, fracture, bloom, orbit, rewind—not just raw faders.
- **Krea:** artist-in-the-loop style edits or reference-image mutations during a performance.
- **ComfyUI on Spark:** slower but controllable prompt/image transformations; results enter TD as a scheduled source layer, never the only live visual.
- **Blender:** make a small collection of authored 3D spaces/objects/camera moves, render or export passes for TD; use them as a coherent world anchor before AI breaks or transforms them.

### 2. Action-to-world sketch

Build a tiny vocabulary of performer actions:

| Input | Semantic action | TD response | Optional AI handoff |
|---|---|---|---|
| Push pad | `enter_world` | change scene/palette | select prompt/reference bundle |
| low band | `mass` | scale, feedback pressure | prompt weight or denoise target |
| mid band | `motion` | camera/orbit/displacement | camera-motion descriptor |
| high band | `spark` | fine texture/edge light | mask/particle accent |
| camera motion | `attention` | region/mask/optical-flow field | image-edit reference crop |

### 3. Reality check

A generated-world model should be benchmarked as an **asynchronous visual collaborator** unless its real measured latency, stability, and hardware footprint meet the show requirement. Start with deterministic TD/Blender compositions and insert Krea/Comfy/world-model outputs as optional layers with a crossfade/fallback.

## Research instruction

Future VJ Lab research should consider Blender, Krea, Ableton/Push, TD, camera, Spark ComfyUI, and AI Search's Sunday roundups as one ecosystem. Prefer experiments that combine at least two tools and can still produce a coherent live set when the generative service is unavailable.

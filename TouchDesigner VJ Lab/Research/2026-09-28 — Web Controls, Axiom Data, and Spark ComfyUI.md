---
tags: [touchdesigner, vj, research, web-ui, axiom-engine, comfyui, dgx-spark]
---

# Web Controls, Axiom Data, and Spark ComfyUI

## Immediate research findings

### 1. A custom web interface for TouchDesigner is very possible

The pragmatic architecture is a small browser UI served by a TouchDesigner **Web Server DAT**, using WebSockets for bidirectional low-latency control. Browser widgets can write into named Constant CHOP channels (sliders, toggles, XY pads, color) and send trigger/preset events as structured JSON. For development, a separate Node/Vite UI is convenient; for a portable performance patch, embed the static UI in TD's VFS and ship it with the `.tox`.

A useful reference implementation is `td-websocket-V2`, which documents both self-contained Web Server DAT deployment and a Node development mode. It supports sliders, color pickers, XY pads, buttons, JSON messages, pages, and persistent configuration.

**First build target:** a phone-friendly `VJ Control` interface with master intensity, low/mid/high response, feedback amount, palette, scene/preset buttons, an XY motion pad, and prompt text. It should remain LAN/local-only until an authentication model exists.

Sources:
- [td-websocket-V2 repository](https://github.com/terezbe/td-websocket-V2)
- [Web Server DAT deployment notes](https://github.com/terezbe/td-websocket-V2/blob/main/docs/WEBSERVER_DAT_SETUP.md)

### 2. Axiom Engine data should start with a narrow event contract

Axiom Engine is a LAN-first Node/Express/Svelte operations platform. The current vault material confirms its dashboard and automation role, but does not establish a stable public real-time event API that TD can consume directly.

Do not couple TD to the full Axiom data model. First define a deliberately small "visual telemetry" contract such as:

```json
{
  "type": "axiom.visual",
  "energy": 0.0,
  "activity": 0.0,
  "agentCount": 0,
  "eventRate": 0.0,
  "mood": "calm",
  "accent": [0.2, 0.7, 1.0],
  "timestamp": "ISO-8601"
}
```

Candidate transports, in order of live-performance practicality:

1. **WebSocket** from an Axiom visual-telemetry endpoint to TD's WebSocket DAT.
2. **OSC/UDP** for the smallest, most resilient performance signal path.
3. **HTTP polling** via Web Client DAT for slow-changing dashboard state only.

Next research/build question: inspect Axiom's existing WebSocket and jobs/event surfaces, then choose one source and map it to a dedicated TD `axiom_input` CHOP branch.

### 3. Spark + ComfyUI is viable, but "realtime" needs an honest latency budget

The Spark already exposes ComfyUI at `http://192.168.0.139:8188`; vault notes identify `flux1-dev-fp8`, LTX 2.3 FP8 checkpoints, and the shared/occasionally rebooted service. NVIDIA's DGX Spark ComfyUI material describes 128 GB unified memory and local GPU inference, so it is a credible host for iterative image-edit experiments.

ComfyUI currently lists image-editing families including **Flux Kontext**, **Qwen Image Edit**, **HiDream E1.1**, and **OmniGen 2**. A practical first trial should be **image-to-image editing of a downscaled TD camera/output frame** at low step count, not full-resolution frame-by-frame diffusion. Treat generated frames as a sporadic texture/source layer that blends into TD's continuous visual system.

Recommended staged prototype:

1. TD sends a 512–768 px still or throttled camera frame to a preloaded ComfyUI workflow.
2. A web/panel prompt control changes the transformation instruction.
3. ComfyUI returns the edited image to a watched folder or HTTP endpoint.
4. TD crossfades the newest valid image into feedback/compositing.
5. Measure end-to-end latency, generation cadence, memory behavior, recovery after ComfyUI restart, and visual coherence.

Potential model shortlist for benchmark research: Flux Kontext, Qwen Image Edit (accelerated/FP8 variants where available), and OmniGen 2. JoyAI Image Edit is compelling for precise multimodal editing, but its published 16B diffusion transformer plus 8B vision-language encoder makes it a later, quality-first candidate rather than the default low-latency starting point.

Sources:
- [ComfyUI official repository](https://github.com/Comfy-Org/ComfyUI)
- [NVIDIA DGX Spark ComfyUI playbook](https://build.nvidia.com/spark/comfyui)
- [JoyAI Image Edit ComfyUI integration](https://github.com/Nynxz/ComfyUI-JoyAI)

## Live Spark check — 2026-09-28

A direct read-only probe of `http://192.168.0.139:8188/queue` and `/system_stats` timed out after 10 seconds. This does **not** establish that ComfyUI is down: the vault records that the Spark is on Wi-Fi and its HTTP services can flap. Treat it as unavailable for this moment and health-check it again before scheduling a real generation; do not build a live performance dependency without queue/restart handling.

## Camera workstream

Before building a TD camera effect, validate the Windows device at the host level: privacy permission **and** actual DirectShow/Media Foundation enumeration. Then connect it to a known visual fallback and only tune the TD `Video Device In TOP` once hardware availability is proven.

## Decisions pending

- The desired performance-control device: phone/tablet browser, laptop browser, MIDI controller, or hybrid.
- Whether Axiom data is a background narrative layer or actively performance-controlled.
- Spark benchmark target: visual novelty per second, or lower-latency controllability.

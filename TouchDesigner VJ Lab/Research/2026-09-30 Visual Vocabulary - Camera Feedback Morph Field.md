# Visual Vocabulary: Camera Feedback Morph Field

**Date:** 2026-09-30  
**Status:** Small-patch experiment; no TouchDesigner projects altered

## Recommendation

Build a **Camera Feedback Morph Field**: a live-camera image is turned into a controllable, beat-synchronized visual field by combining optical-flow displacement with a TouchDesigner feedback loop. The performance trick is to treat incoming generative frames as *occasional pigments*, not as the render engine.

### Patch shape

```text
Live Camera ──┬─> Optical Flow (low-res) ─> Displace / GLSL warp ─┐
              │                                                   │
              └─> Edge/threshold mask ─> color treatment ────────┤
                                                                  v
                    Feedback TOP <─ blend/level <─ composite <─ current frame
                                                                  │
                                                                  v
                                                              out TOP
```

Use a 640x360 secondary field and composite to a 1280x720 output. A `Feedback TOP` provides the memory; a GLSL TOP or Displace TOP applies flow-driven warp, decay, chromatic split, and a restrained color grade. Keep a reset pulse on an easily reachable control.

## Signal and control mapping

- **Ableton/Push pads:** scene actions — reset/clean frame, freeze, fracture, and inject.
- **Push knobs or MIDI CC:** flow gain, feedback decay, edge threshold, hue rotation, and generative-layer opacity. Use TD's MIDI In CHOP or TDAbleton; do not hard-code Push CC numbers until the actual device mapping is observed.
- **Ableton beat/bar data:** quantize reset and inject actions to 1/4, 1, or 4 bars. TDAbleton exposes beat/time data and communicates with TD over OSC.
- **Camera motion:** Optical Flow drives displacement magnitude and direction. Camera input remains the reliable visual source even if every external AI service is offline.
- **Blender:** optional source of a low-resolution geometric silhouette or motion-vector/render pass, sent via Spout or a short rendered loop. It should be a selectable layer, not a dependency.
- **Krea Realtime or Spark/ComfyUI:** optional asynchronous style/keyframe source. Submit a still or short prompt/reference, write the completed image into a watched folder, then crossfade it into the feedback field on the next beat. TD only polls files; it never waits for generation.

## Why this expands AJ's vocabulary

It creates a performable middle ground between camera-reactive visuals and generative video: the Push controls *memory and topology* (how the image persists, fractures, and re-enters), while the camera controls the physical motion. The result can shift from recognizable live presence to an abstract, self-propelling texture without changing the core patch.

The approach is grounded in TD's native feedback model: the Feedback TOP can source a downstream target and pass through the input when bypassed/reset. MIDI In CHOP supports controller, note, timing, and high-frequency MIDI events. Krea's own description of Realtime Video supports webcam/screen input and emphasizes frame-consistent, immediately responsive generation, but its output should remain an optional pigment layer rather than the timing-critical loop.

## Minimal next experiment (30–45 minutes)

1. Create a scratch COMP with `videodeviceinTOP` or a Movie File In fallback, `opticalflowTOP`, `displaceTOP`, `feedbackTOP`, `levelTOP`, `compositeTOP`, and a named `out` TOP.
2. Start at 640x360. Confirm the camera is actually enumerated before tuning TD; if unavailable, use a short project-relative movie.
3. Add one MIDI In CHOP and map three observed controls: decay, flow gain, and reset pulse. Add one Ableton/beat pulse only after the manual version is stable.
4. Add a deterministic still/loop as the generative layer. Later replace that asset with a polled Krea or Spark/ComfyUI result, crossfading only when a complete file appears.
5. Test three modes: **clean camera**, **slow memory**, and **fracture**. Capture the `out` TOP and check sustained 60 FPS while moving the camera and turning all three controls.

## Performance and failure risks

- **GPU cost:** Optical Flow, full-resolution feedback, blur, and multiple GLSL passes can exceed the projector budget. Keep flow and AI layers below output resolution; inspect Performance Monitor and verify sustained 60 FPS, not just a clean error scan.
- **Feedback runaway/washed-out output:** expose reset, clamp feedback gain/opacity, and keep a bypass path to the current camera/fallback frame.
- **Camera failure:** privacy permission does not prove hardware enumeration. Leave a known movie/still fallback connected and selectable.
- **AI latency or outage:** never block the TD frame loop on Krea, Spark, or ComfyUI. Watch for completed files, reject partial files, and retain the last good generated frame.
- **MIDI/OSC mapping drift:** discover the live device/channel names and verify the actual values before binding parameters; Push mappings vary by setup.
- **Blender/Spout failure:** keep a local rendered loop or TD-generated silhouette as the fallback layer.

## Current AI-news relevance check

A search for the latest Sunday/weekly AI NEWS material from AI Search did not surface a reliably indexed episode with primary-source detail, so no technical claim here depends on an unverified AI-news report. The relevant primary source is Krea's own Realtime Video announcement; ComfyUI's official API documentation confirms the queue/file-polling architecture needed for an asynchronous optional layer.

## Sources

1. [Derivative — Feedback TOP](https://docs.derivative.ca/Feedback_TOP)
2. [Derivative — MIDI In CHOP](https://docs.derivative.ca/MIDI_In_CHOP)
3. [Derivative — TDAbleton](https://derivative.ca/UserGuide/TDAbleton)
4. [Krea — Announcing Realtime Video](https://www.krea.ai/blog/announcing-realtime-video)
5. [ComfyUI — Server Routes and WebSocket API](https://docs.comfy.org/development/comfyui-server/comms_routes)

---
tags: [touchdesigner, vj, research, comfyui, dgx-spark, flux2-klein, krea, blender, ableton]
date: 2026-10-02
status: research-only (Spark and TD untouched)
---

# 2026-10-02 Spark ComfyUI: Throttled Frame-Edit Loop

Builds on [[2026-09-28 — Web Controls, Axiom Data, and Spark ComfyUI]] and [[2026-09-28 — AI Search World-Model Watchlist]].

## Verdict

Frame-rate diffusion on the Spark is **not supported by any evidence found**. A 1–4 fps (probably slower) asynchronous edit layer is realistic. TD keeps the 60 fps loop; ComfyUI results arrive as a slow, crossfaded texture layer.

## What the sources say

**AI Search weekly (Sunday 2026-09-27/28 edition).** Title: "Waifus incoming, GPT 6 Sol, Grok 4.7, Opus 5.5, Mimo 2.6, Step 5, OpenMuse" ([Substack](https://aisearch.substack.com/p/waifus-incoming-gpt-6-sol-grok-47)). I could only read its title, not its content, so I can't confirm it covers world models or image editing. The earlier AI Search roundups (Aug 25 "realtime worlds", Sep 8 "new world models") are the relevant ones. Per a secondary recap ([CodeMyPixel](https://codemypixel.com/blog/ai-news-september-2026-gpt-6-astra)), they name H3 World, Solar WM, GLM Worlds 2 and Atlas. All figures there are the video's claims, unverified. Treat the world models as inspiration, not as a pipeline.

**Primary / near-primary on feasibility:**
- **FLUX.2 [klein]** ([ComfyUI blog, 2026-01-15](https://blog.comfy.org/p/flux2-klein-4b-fast-local-image-editing)). It does editing and generation, with single- and multi-reference input. Vendor-reported times are for an **RTX 5090**: 4B distilled about 1.2 s (4 steps, 8.4 GB); 9B distilled about 2 s (19.6 GB). The Comfy blog lists the 9B distilled as available only through the BFL API. Check the licence before assuming local use. The 4B (Apache 2.0 per [Thunder Compute guide](https://www.thundercompute.com/blog/flux-comfyui-ai-image-generation)) is the local candidate. FP8 and NVFP4 variants are published on Hugging Face.
- **FluxRT** ([repo](https://github.com/tensorforger/FluxRT), [Reddit post 2026-05-08](https://www.reddit.com/r/StableDiffusion/comments/1t7nd7e/flux2klein_pipeline_for_realtime_webcam_stream/)). A third-party, Unlicense, research-grade Klein-4B stream pipeline. Its author claims about 0.2 s latency on one RTX 5090. It uses a spatial KV-cache that recomputes only the changed regions, plus RIFE interpolation (author uses 4×). Claimed output is up to about 50 fps for mostly static scenes and about 20 fps when the whole frame changes. This is **claimed, not independently reproduced**, and it is a separate Python process, not a ComfyUI graph.
- **Decart Lucy 2.0** claims 30 fps at 1080p live video editing ([demo video](https://www.youtube.com/watch?v=R5eLA7h3jPY)). It is a hosted/cloud service, so it is a benchmark target rather than a local option.
- **Wonder** (camera-steerable video world, 16 fps, minute-scale memory) is a paper per a secondary summary ([AI Weekly](https://aiweekly.co/alerts/wonder-a-minute-scale-camera-steerable-video-world-at-16-fps)). I did not verify weights or hardware needs. Watch only.

**Hardware caveat (the important one).** The DGX Spark GB10 has 273 GB/s memory bandwidth against about 1,792 GB/s for an RTX 5090, roughly 6.5× less ([DataHardware](https://datahardware.ai/products/nvidia-dgx-spark), [Codersera](https://codersera.com/blog/dgx-spark-vs-rtx-5090-local-llm-2026)). Dense compute is about RTX 5070-class. So **every 5090 number above must be treated as a best case**. My unmeasured guess is that Klein 4B distilled on the Spark takes a few seconds per edit, not 1.2 s. The test below exists to replace that guess with a measurement. The Spark's advantage is 128 GB of memory: several models can stay resident, and it can be shared with the LLM.

## Candidate comparison

| Candidate | Role | Reported speed (5090 unless noted) | Spark expectation | Integration effort |
|---|---|---|---|---|
| Klein 4B distilled (fp8/nvfp4) in ComfyUI | Image edit / restyle of a frame | about 1.2 s | unknown, likely slower; measure | Low: ComfyUI API workflow |
| Klein 9B distilled | Higher quality edit | about 2 s, 19.6 GB | slower again; licence/availability caveat | Low |
| SDXL Turbo img2img | Cheap style transfer, 1 step | "1 step" per [Comfy tutorials](https://www.youtube.com/watch?v=DZ2dfq8ljrc); no fresh number | probably fastest here; lower fidelity and edit control | Low |
| FluxRT (Klein 4B + KV cache + RIFE) | Stream edit | 0.2 s latency, 20–50 fps (claimed) | unknown; the KV-cache trick is memory-bandwidth-sensitive | Medium: separate process, then NDI/Spout/shared file |
| Lucy 2.0 (cloud) | Reference ceiling | 30 fps 1080p (claimed) | n/a | Cloud, outside the local-first setup |

Krea: use it as a manual look-development and prompt-discovery tool (Krea Realtime for authoring styles), then copy winning prompts and reference images into ComfyUI. Blender: render consistent reference plates (depth, normal, flat-colour passes, turntables) used as the conditioning or reference image. This gives stable composition that a camera frame doesn't.

## Pipeline (TD owns time; ComfyUI is optional)

1. **Throttled capture.** TD takes the camera or the TD `out` TOP, scales it to 512×512 or 768×432, and saves a numbered JPEG or PNG at 1–2 Hz. It only submits when no job is in flight (single-slot backpressure), and a newer frame replaces a pending one (drop-oldest).
2. **Submit.** A small supervised external script (as in the story-engine recipe) POSTs a ComfyUI API workflow to `192.168.0.139:8188/prompt` with the frame path, prompt text, seed and strength. It tracks `prompt_id`, polls `/history`, and downloads the result to `edits/latest_N.png`. TD never talks to ComfyUI directly.
3. **Handoff.** TD polls the folder (Folder DAT or a movieFileIn on `latest`). Each new file loads into a "B" Cache TOP slot.
4. **Blend.** A crossfade (Cross TOP) between the previous and new edit over about 0.5–1.5 s. The result is mixed over the live TD visual with a Level/Over stage, with opacity capped so a stale edit never covers the show. Optional camera-motion or optical-flow warp of the last edit between arrivals hides the low update rate.
5. **Resilience.** Per-job timeout of 20 s. On timeout, error or ComfyUI restart, the supervisor retries `/system_stats` with backoff and marks state `down`. TD fades the edit layer to zero and falls back to the pure-TD visual. On reconnect it fades back in. A queue-depth check (`/queue`) blocks submission if the Spark is busy with other jobs. The Spark is shared and occasionally rebooted, so never block the render on it.

## Steering

- **Ableton/Push (MIDI or OSC into TD):** pad or scene triggers choose a prompt/style bundle from a preset table (action vocabulary: drift, fracture, bloom, rewind, attention). Knobs map to edit strength (denoise or reference weight), crossfade time, and layer opacity. An Ableton Link or clock tick can quantize *when* a new edit lands (on the bar), which hides latency as rhythm. Kick or onset detection can trigger an off-cycle submission.
- **Camera:** motion energy (frame-difference CHOP) lowers or raises the submission rate and strength. Large motion gives fewer edits at lower strength. Stillness allows a higher-quality edit. Optionally a coarse pose, depth or edge image stands in for the raw frame.
- **Prompt text:** from the Web Server DAT control page already researched on 09-28.

## Benchmark design

Run once the owner schedules a Spark window. Do not alter Spark or TD for this research step.

**Fixed inputs:** 10 frames (5 camera captures, 3 Blender plates, 2 TD outputs) at 512² and 768×432. Fixed prompt set of 3. Fixed seeds.

**Variants:** Klein 4B distilled (fp8, then nvfp4 if available); SDXL Turbo img2img; optionally Klein 9B (if a local licence allows). 4 steps for Klein, 1–2 for Turbo.

**Measure per run (N≥30 after 5 warmup):**
- Wall-clock submit→file-written (p50/p95), split into queue wait vs execution via ComfyUI history timestamps.
- Cold vs warm: first run after model load vs steady state; also after an alternating-model run (model swap cost).
- Throughput at 1 job in flight vs 2 (does batching help?).
- GPU memory and utilization (`nvidia-smi`), to see headroom against the LLM or Flux-dev jobs sharing the box.
- Restart behaviour: kill/restart ComfyUI mid-queue; time to recover and whether the supervisor and TD fall back cleanly.
- Visual score (human, 1–5): fidelity to the source structure, style strength, frame-to-frame flicker over 20 consecutive edits, and whether the crossfaded layer still looks good on the projector.

**Acceptance (proposed):** p95 ≤ 3 s at 512² gives a useful 0.3–0.5 Hz layer; ≤ 1.5 s allows 1 Hz. Slower than 6 s means move to SDXL Turbo or treat the layer as beat-synced "stills". No visible stall or blank frame in TD during any ComfyUI failure.

## Recommended next test

**"Klein-4B vs SDXL-Turbo latency baseline on the Spark through the existing ComfyUI API."**
It is one script, with no TD change. Submit the 10 frames across the two variants at 512², record the timings above, and write the numbers into this folder. It answers the open question (how much slower the Spark is than the vendor's 5090 figures), tells us which model the TD handoff should target, and decides whether FluxRT is worth a separate trial. Prerequisite check: confirm which Klein/SDXL-Turbo weights are already on the Spark (previous notes show only `flux1-dev-fp8` and LTX 2.3 FP8 confirmed). Downloading new weights is a Spark change and needs AJ's go-ahead.

## Open items / unverified

- Content of the Sep 27/28 AI Search episode itself (title only).
- Whether Klein 4B nodes are present in the Spark's ComfyUI version.
- All "real-time" claims for FluxRT, Lucy and Wonder are vendor or author claims on different hardware.

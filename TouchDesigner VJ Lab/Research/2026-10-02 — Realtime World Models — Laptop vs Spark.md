---
tags: [touchdesigner, vj, research, world-models, dgx-spark, waypoint, realtime, projector]
date: 2026-10-02
status: laptop test executed 2026-10-02 (env: C:\Users\ander\worldmodels\waypoint)
---

# 2026-10-02 — Realtime World Models: What Actually Runs on the Laptop vs the Spark

Builds on [[2026-09-28 — AI Search World-Model Watchlist]] and [[2026-10-02 Spark ComfyUI - Throttled Frame Edit Loop]]. Question asked: of the new *navigable* realtime world models, which is most compatible with the current setup — the MSI laptop or the Spark?

## Verdict

**Laptop (RTX 4080 Laptop, 12 GB VRAM, Windows):** the only mainstream navigable world model that is explicitly built for this class of machine is **Overworld Waypoint-1.5-1B-360P** — Apache 2.0, a single 3.72 GB weight file, keyboard/mouse driven, designed for Nvidia *laptop* GPUs.[2][1] Downloading and running it is the realistic "tonight" experiment. A second, much smaller option is **Dreamer-MC** (DreamerV4 Minecraft reproduction), a 1.7B next-frame model needing ~9 GB VRAM.[15]

**Spark (GB10, 128 GB unified, arm64):** memory-rich but bandwidth-poor. It fits most of the big models that the laptop cannot hold — but the measured evidence says it produces *seconds per frame*, not frames per second.[17][18] Treat the Spark as the **bake/offline machine** (asset and clip generation, ComfyUI edits, model evaluation at 1–5 fps), not the driver of a live 60 fps world. Its one genuine realtime candidate is the smallest model in the field, and even that is unproven on GB10.

## Hardware baseline (measured today, not assumed)

| | MSI Vector GP68HX (this host) | Spark (DGX Spark, GB10) |
|---|---|---|
| GPU | RTX 4080 **Laptop**, 12,282 MiB VRAM, driver 595.79 | NVIDIA GB10, driver 580.142, arm64 |
| Memory | 16 GB DDR5-4800 (2×8 GB) | 121 GiB unified, 273 GB/s |
| Compute class | Ada Lovelace sm_89 | ~RTX 5070-class dense, Blackwell sm_121a |
| OS / stack | Windows 11, Python 3.10.6 with torch 2.9.1**+cpu** (no CUDA torch env yet) | Ubuntu 24.04 arm64, CUDA 13.0 |
| Disk | 114 GB free on C: | ~229 GB free (per [[Spark System Analysis — Housekeeping 2026-09-13]]) |

The laptop numbers are from `nvidia-smi`, `Win32_PhysicalMemory` and a live torch import on 2026-10-02. The Spark numbers are from [[Spark System Analysis — Housekeeping 2026-09-13]]; the Spark is a shared machine, so anything here needs an owner window before it is run.

## The field, as of 2026-10-02

| Model | Type | Real-time claim | Stated hardware floor | Licence | Fits laptop 12 GB? | Fits Spark? |
|---|---|---|---|---|---|---|
| **Waypoint-1.5-1B-360P** (Overworld) | Interactive video world, 1.2B | Family target 720p/60 fps; 360P tier is the laptop tier | "Nvidia **laptop** GPUs" (720p tier: desktop RTX 30–50)[2] | Apache 2 | **Yes** — 3.72 GB weights[2] | Likely, unverified |
| **Waypoint-1.5-1B (720p)** | Same family, 720p | 56 fps unquantized / 72 fps w8a8 on a 5090; 30 fps w8a8 on a 3090; 512-frame (~10 s) context[3] | Desktop RTX 30-series or later[3]; Biome client asks for **16 GB+ VRAM**[5] | Apache 2 | Marginal — 11.19 GB BF16 weights before activations[3] | Likely, but fps unknown |
| **Matrix-Game 2.0** (Skywork) | Interactive world foundation model, 25 fps, keyboard+mouse[10] | 25 fps | **≥24 GB GPU (A100/H100 tested), Linux, 64 GB RAM**[10] | MIT | No | Yes (memory), fps unknown |
| **Matrix-Game 3.0** | 5B, 720p, long-horizon memory, int8 + VAE decoder distillation | 40 fps claimed at 720p, 5B[11][21] | not stated; 56.6 GB of released weights[11] | Apache 2 | No | Plausible — this is the best Spark-format model |
| **HY-World 1.5 / WorldPlay** (Tencent) | Streaming interactive world, 24 fps[12] | 24 fps | AR distilled inference: 28 GB (sp=8) → 72 GB (sp=1); WAN-5B variant "fits small-VRAM GPUs" with weaker control/memory[12] | see repo | No | Yes in the 8-way/lightweight configs |
| **HY-World 2.0** | **Not video**: emits persistent 3D assets (meshes/3DGS) for Blender/Unity/UE[13] | n/a — rendered by engines at realtime speed[13] | heavy generation, then engine-rendered | see repo | Renders locally once assets exist | **Best structural fit** — generate on Spark, render anywhere |
| **LingBot-World 2.0 realtime fork** | 1.3B world model, 16.1 fps on a 5090[8] | 16 fps (5090) | 24 GB min (4090, ~12 fps est.), source-built kernels; 30.7 GB peak VRAM, one card = one stream[8] | CC BY-NC-SA (non-commercial)[8] | No | Yes by memory, but bandwidth-limited |
| **Krea Realtime 14B** | Autoregressive video model | 11 fps on a B200, 4 steps[7] | 40 GB+ VRAM recommended, KV cache up to 25 GB/GPU[7] | CC BY-NC-SA[7] | No | Yes by memory, very slow |
| **ForgeWM** | Training recipe + few-step students on the MG2 backbone | 168 ms/chunk, 72 fps at 352×640, 1-step, on one H20[14] | single-GPU inference supported[14] | Apache 2 | No (MG2 backbone) | Possible; students are the cheap end |
| **Dreamer-MC** (DreamerV4, Minecraft) | Autoregressive next-frame world, WASD/click/inventory, 12 s recall[15] | "real-time next-frame prediction" (inference-only repo)[15] | Tokenizer 430M >2 GB + Dynamic Model 1.7B **9 GB**[15] | MIT | **Yes**, ~11 GB[15] | Yes; a GB10 fork already exists[16] |
| **Genie 3** (DeepMind) | The reference playable world | 720p, 24 fps, consistent for minutes[20] | cloud only | closed | n/a | n/a |
| **GWM Worlds 2** (Runway) | Playable world, 720p, 24 fps[20] | 720p 24 fps | research preview, contact form[20] | closed | n/a | n/a |
| **Decart Oasis 3** | API-accessible interactive world model | 3× 768×512 views at 22 fps, <200 ms end-to-end on HGX B200[19] | cloud | commercial | n/a | n/a |

## Why the laptop wins for interaction, and the Spark loses it

The controlling number is **memory bandwidth**, not capacity. The DGX Spark's 273 GB/s sits roughly 6.5× below an RTX 5090's ~1,792 GB/s ([DataHardware](https://datahardware.ai/products/nvidia-dgx-spark), [Codersera](https://codersera.com/blog/dgx-spark-vs-rtx-5090-local-llm-2026), carried over from [[2026-10-02 Spark ComfyUI - Throttled Frame Edit Loop]]). Every realtime world model is a per-frame diffusion/DiT rollout whose KV cache is re-read constantly, so the Spark's advantage — 128 GB you can actually hold a 14B model in — buys headroom, not frames. Two independent measurements of what that feels like in practice:

- MiniMax H3 on one DGX Spark: a 20-step 864×480, 124-frame render takes **148–180 s wall** (~0.7–0.8 fps) even after NVFP4 quantization and kernel fusion work.[18]
- Cosmos Predict 2.5 (2B) on a DGX Spark: **~53 s per denoising step**, 36 steps ≈ **32 minutes per video**; the 14B variant could not run at all and froze the system three times.[17]

Those are *image-to-video* workloads, not interactive rollouts, so the Spark's ceiling for a live world model is bounded by the same physics: single-digit fps at best, at reduced resolution, if it works at all. The laptop, by contrast, is Ada Lovelace with real FP8 tensor cores — exactly the tier the Waypoint family targets. The earlier Waypoint-1 release already showed the design point: WorldEngine sustained ~30 fps at 4 steps and 60 fps at 2 steps for a 2.3B model on a single RTX 5090.[22]

## Spark-specific landmines (from real GB10 reports)

1. **Missing kernels on sm_121a.** Cosmos Reason2-8B cannot use FlashAttention on the Spark because the sm_121a kernel is not available; attention had to fall back to eager mode, with cuDNN crashes on the default paths.[17] Every realtime world model here depends on FlashAttention/SageAttention builds, and most ship prebuilt wheels for sm_120/sm_89 only.[8][12]
2. **arm64 + CUDA 13 only.** Cosmos required `--extra=cu130`; CUDA 12.8 (x86_64) builds do not work.[17] Kernel-building on the Spark is its own project.
3. **Unified-memory OOM takes the whole machine down.** Because CPU and GPU share memory, a GPU-side OOM is a kernel-level hang, not a killed process — in the reported case a soft reboot failed to reinitialise GSP firmware and the GPU did not come back.[17] A shared Spark plus an unattended world-model job is a bad combination; run these with explicit memory ceilings and a person nearby.
4. **Nothing is realtime over a network.** `world_engine` returns frames in-process; the Spark is reached over the LAN. Driving a 60 fps projector from the Spark is therefore not just slow, it is the wrong shape.

## Integration into the existing TD / projector setup

- `world_engine` is deliberately **headless**: it has "no rendering/display of video or images" and "no reading controller/keyboard/mouse input"; those belong in examples/clients.[4] That is the opposite of a limitation here — it means the model can be dropped behind TouchDesigner as a frame *source*, with TD keeping time, compositing, MIDI mapping and the fallback path, exactly the doctrine already recorded in [[2026-09-28 — AI Search World-Model Watchlist]].
- API shape: `WorldEngine("Overworld/Waypoint-1.5-1B", quant=..., device="cuda")`, `set_prompt(...)`, then `engine.gen_frame(ctrl=CtrlInput(button={...}, mouse=(dx,dy), scroll_wheel=...))`. Waypoint-1.5 applies temporal compression and returns **4 frames per controller input** at 720p, so the runtime renders a batch while the next is generating.[4]
- Quantization choices matter per machine: `intw8a8` (RTX 30xx/40xx and up), `fp8w8a8` (Ada/Hopper — the laptop 4080's best path), `nvfp4` (Blackwell B100/B200/RTX 5090 — **not** Ada; GB10 support unlisted).[4][6]
- Practical display route on the laptop: Python engine → shared-memory/Spout frame buffer → TD → Spout/projector. Biome is the alternative "just play it" client, but it states a 16 GB VRAM floor, so a 12 GB laptop would be relying on the 360P tier inside it or falling back to Overworld Stream.[5]

## Measured on the laptop — 2026-10-02 (test 1 executed)

Environment: `C:\Users\ander\worldmodels\waypoint` — uv venv (CPython 3.12), `torch 2.11.0+cu130` (torch.cuda reports the RTX 4080 Laptop, capability 8.9, 12.88 GB), transformers 5.18.0, triton-windows 3.6.0.post26, `world_engine` 0.1.dev1 (git @68b3163), weights `Overworld/Waypoint-1.5-1B-360P` (3.72 GB, ungated). Scripts `bench.py` / `demo.py`; raw JSON results sit next to this note.

| Run | Quant | Steady state (p50 per 4-frame call) | 20-call window | Peak VRAM |
|---|---|---|---|---|
| bench, 640×360, 20 calls | none (BF16) | 0.054 s → **≈74 fps** | 31.7 fps (one 1.5 s first-call hitch) | 7.43 GB alloc / 8.26 GB reserved |
| bench, 640×360, 20 calls | `fp8w8a8` | 0.043 s → **≈93 fps** | **87.1 fps** | 7.43 GB alloc / 8.12 GB reserved |
| demo, 724 frames written | none (BF16) | 0.056 s per call | 13.9 fps end-to-end | 7.43 GB |

Reading: **the laptop drives Waypoint-1.5 at 360p well above 60 fps with roughly 4 GB of VRAM to spare.** The BF16 "31.7 fps" window figure is an artifact of the one-off ~1.5 s first call; steady state is ≈74 fps. `fp8w8a8` buys ~25 % more throughput at the same VRAM.

Findings that only a real run produces:

- **The 360P tier is image-conditioned, not text-conditioned.** Its `config.yaml` sets `prompt_conditioning: null`, so `engine.set_prompt()` raises `RuntimeError: prompt_conditioning enabled but prompt_encoder is not initialized`. The correct entry point is `engine.append_frame(uint8[4,H,W,3])` with a seed frame, then `gen_frame(ctrl=...)`. No UMT5 text encoder is loaded at all (saves ~5 GB of download and RAM).
- **Recording is encoder-bound, not model-bound.** 180 calls (720 frames, 12 s at 60 fps) took 51.7 s wall with `.cpu().numpy()` plus synchronous libx264 writes inside the loop, while generation on the same run was 0.056 s/call. A recording pipeline needs an async writer thread or NVENC, or the encoder throttles the world to ~14 fps.
- **`intw8a8` will not use gemlite here.** gemlite ships no Windows wheel (PyPI has only the sdist) and building it needs a CUDA toolkit plus MSVC, neither installed; the engine's optional import fails cleanly and INT8 falls back to the plain torch kernel. `nvfp4` requires flashinfer and is Blackwell-only regardless.
- **Quality over 12 s of navigation:** the world holds structure — columns, cavern walls and the held weapon stay coherent — with visible texture drift and a malformed left hand appearing in the sky-area frames. Realistically a live layer or a stylised look, not a clean game render.

Video and a representative frame are stored beside this note:

![[2026-10-02 waypoint360p-bf16 4080-laptop.mp4]]

## Recommended next tests

1. ✅ **Done 2026-10-02** — the 360P test above: 3.72 GB weights, 8.1 GB reserved VRAM, ≈74 fps BF16 / ≈93 fps fp8 on the laptop. The remaining open variant is the **720p tier on 12 GB** (11.19 GB of BF16 weights), which was deliberately not attempted.
2. **Same venv, +4 GB:** Dreamer-MC (9 GB dynamic model + 2 GB tokenizer) as the fallback interactive world — WASD/click control, 12 s recall, MIT.[15]
3. **Spark window, later and with the owner:** Matrix-Game 2.0 is the cleanest first target (MIT, Linux, 24 GB floor — all satisfied by the Spark within its footprint), measured against the realtime criterion of ≥10 fps; log memory ceiling and stop conditions before starting, given the OOM-hang behaviour.[10][17]
4. **Decide the division of labour:** if the goal is a *playable world on the projector*, the laptop drives it (Waypoint 360P or Dreamer-MC) and the Spark bakes supporting content. If the goal is a *rich, persistent world*, HY-World 2.0's asset route (generate 3DGS/meshes offline on the Spark, render realtime in Blender/TD/Unity) sidesteps the fps problem entirely.[13]
5. **Wire it into TouchDesigner:** run `world_engine` as a separate process that publishes frames (Spout/shared memory) and let TD own compositing, MIDI→`CtrlInput` mapping, fallback and recording — with the writer on its own thread so the encoder never throttles generation.
6. **Only if a paid shortcut is wanted:** Overworld Stream (hosted Waypoint) and Decart Oasis 3 ($0.02 per second of simulation ≈ $1.20/min, 3×768×512 at 22 fps).[19]

## Open items / unverified

- No published evidence of anyone running Waypoint-1.5 on a GB10/Spark; the fps there is an estimate, not a measurement.
- The 720p tier on a 12 GB card is untested and expected to be close to the limit (11.19 GB BF16 weights before activations); the 360P measurement does not answer it.[3]
- Matrix-Game 3.0's 40 fps claim is at unspecified hardware; only the 5B size and int8 quantization are documented in the repo.[11]
- Whether Biome actually starts on a 12 GB card is untested; its documented floor is 16 GB. The measured 8.1 GB reserved for the 360P tier suggests the floor is about the 720p model rather than the client itself.[5]
- Laptop RAM (16 GB) was not a bottleneck for the 360P tier (3.72 GB of weights); it remains a risk only for the 720p tier.[2]

## Steering surfaces — how generation is controlled (verified 2026-10-02)

Per call the engine draws a noise latent, runs 4 Euler steps over `scheduler_sigmas` `[1.0, 0.9, 0.75, 0.3, 0.0]` against the **frozen** KV cache plus a control vector, then writes the new 4 frames back into the cache (temporal compression 4, `base_fps` 15, presented at up to 60 fps). Controls never touch pixels directly: `ctrl_emb = ControllerInputEmbedding(mouse, button, scroll)` — button as a one-hot over 256 keycodes, mouse as a **velocity** (dx, dy), scroll as a ternary — is fused into the transformer with an `MLPFusion` on **every third layer** (`ctrl_conditioning_period: 3`). So a key steers how the cached world state is transformed, and the same key means different things in different scenes.

Memory is what the continuity comes from: a local attention window of 16 frames, with every 4th layer reading a 128-frame global window; `pinned_dilation: 8` keeps sparse long-range frames alive; `n_frames` caps context at 512 frames (the 360p card quotes ~2 s of context, the 720p card 10 s).

| Lever | What it does | Evidence |
|---|---|---|
| **Starting image** (`append_frame`) | Sets content, style, camera and subject — this *is* the prompt | All runs |
| **Mid-rollout frame injection** | Writes a frame into the cache → the world continues from that image (hard cut/teleport) | Measured jump: **MAE 75/255** vs the preceding frame |
| **RNG seed** (`torch.manual_seed`) | Same seed + same controls + same start image ⇒ **bit-identical** rollout (checksums equal, MAE 0.0); a different seed gives a different world (MAE 9.1/255) | Verified |
| **State snapshot / rewind** (`get_state`/`load_state`) | Restores the model's world state **exactly** (latent MAE 0.0, max abs diff 0.0) — but the streaming VAE's decoder state is *not* in the snapshot, so the pixels you see after a rewind can differ (MAE up to ~20/255, larger the longer the intervening rollout) | Verified |
| **Control stream** | Buttons (32 fwd, 65 left, 68 right, 83 back, 1 trigger; 256 codes available), mouse velocity, scroll — arbitrary combinations are legal, nonsense ones are expressive | Partly verified |
| **Presentation timing** | Frames per call are fixed at 4; the rate they are shown at is ours (60 fps, slow-mo, hold) — a performance lever, not a generation one | By construction |
| **Load-time config** (`model_config_overrides`) | `local_window`/`global_window`/`pinned_dilation` (memory vs speed), `scheduler_sigmas` (fewer steps = faster/softer), resolution tier, `quant` | Read from source |
| **Checkpoint** | 360p (laptop) vs 720p (desktop); text conditioning exists only on Waypoint-1-Small (`prompt_conditioning: cross_attention`) | Verified via configs |

**Not available:** text prompts on 1.5 (`prompt_conditioning: null`, `set_prompt()` raises), camera pose/intrinsics, numeric style or strength knobs, masks/inpainting, object or physics control. Mouse is a velocity, not a position, so there is no "look at this exact spot" — only "turn this fast this frame".

Practical consequence for live use: record the RNG seed with any take so it can be replayed exactly; use `append_frame` as the beat-quantised cut; keep a ring buffer of *rendered* frames rather than relying on `load_state` for a visual rewind; and treat the control stream as verbs (the model learned them per scene) rather than as a camera API.

## Run log

- **2026-10-02 — laptop test executed** (360p numbers above), crash diagnosed (Windows bugcheck `0xD1`, NVIDIA 595.79, minidump `100226-19453-01.dmp`, no WHEA), steering surfaces verified, and the headless harnesses written: `soak.py`, `verbs.py`, `guards.py` in `C:\Users\ander\worldmodels\waypoint` (all self-guarding: idle preflight, temperature/commit-charge/VRAM aborts, wall-clock cap).
- **2026-10-02 — Townhall**: posted finding `da416393-6813-49f3-8b73-a32da5ac6cf6` (project `home-lan`) with the numbers, the crash class and the verb-sweep plan; asks to Herm and Sparkbot for any prior keycode probing, a Spout/NDI handoff for a Python frame source, or a view on the crash class. Replies to be folded in here.
- **2026-10-02 — harness smoke-tested** (3 min, clean, no crash): the sweep method is validated and already reproduces the control mapping — 87 = W = **move-forward** (radial divergence +0.65), 83 = S = **move-back** (−0.75), 65 = A = **turn-left** (image dx +1.15), 68 = D = **turn-right** (−1.61), 32 = space = **look-up** (the upstream sample's "jump"), 1 = LMB = action/mixed (weak camera response). Keys are ASCII code points; my first viewer had mapped W to 32, which is why it jumped instead of walking. Mouse is a velocity whose turn rate rises ~linearly to ≈0.4 then saturates.
- **2026-10-03 01:30 — scheduled (cron `0247a6d09295`, "waypoint-world-model-soak+verbs")**: 12-minute stability soak (drift, throughput sag, thermals) plus a **256-code control-vocabulary sweep** — each code branched from one shared world state and measured by optical-flow direction (camera-space), radial divergence (dolly in/out), activity, and visual response versus an idle baseline, with a mouse-magnitude curve and pairwise combos of the six strongest codes. It appends a `## Stability soak` and a `## Control vocabulary sweep` section to this note and replies in the Townhall thread. **Results: pending.**

- **2026-10-03 09:00 — reminder scheduled (cron `f715c4d3326d`, "waypoint-world-model reminder", 3 mornings)**: AJ asked to revisit and evaluate on 2026-10-03 and to be reminded if he forgets. The reminder reports last night's soak + sweep results and puts three decisions to him: (a) chase the NVIDIA driver / bugcheck question or stay headless-only; (b) wire the world into TouchDesigner via a Spout frame source, or try the official Biome client first; (c) build a corrected interactive viewer (right key map 87/65/83/68, space = look-up, image-prompt box for start frames). It self-silences once this note records a revisit.

## Sources

[1] https://huggingface.co/blog/waypoint-1-5
[2] https://huggingface.co/Overworld/Waypoint-1.5-1B-360P
[3] https://huggingface.co/Overworld/Waypoint-1.5-1B
[4] https://github.com/Overworldai/world_engine
[5] https://github.com/Overworldai/Biome
[6] https://smeltcore.com/recipes/waypoint-1-5-on-rtx-4080-real-time-interactive-world-model-at-720p
[7] https://github.com/krea-ai/realtime-video
[8] https://github.com/kaarelkaarelson/lingbot-world-v2-realtime
[10] https://github.com/SkyworkAI/Matrix-Game/blob/main/Matrix-Game-2/README.md
[11] https://github.com/SkyworkAI/Matrix-Game/blob/main/Matrix-Game-3/README.md
[12] https://github.com/Tencent-Hunyuan/HY-WorldPlay
[13] https://github.com/Tencent-Hunyuan/HY-World-2.0
[14] https://github.com/asdfo123/ForgeWM
[15] https://github.com/IamCreateAI/Dreamerv4-MC
[16] https://github.com/blackfirebitcoin/Dreamerv4-MC-GB10
[17] https://dev.classmethod.jp/en/articles/dgx-spark-cosmos-world-model
[18] https://github.com/newjordan/h3-spark
[19] https://ai-tldr.dev/releases/decart-oasis-3-jun10
[20] https://atlasworldmodel.com/blog/gwm-worlds-2-vs-genie-3
[21] https://arxiv.org/html/2604.08995v2
[22] https://huggingface.co/blog/waypoint-1

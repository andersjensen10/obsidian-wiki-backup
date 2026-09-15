---
tags: [benchmarking, model-research, huggingface]
status: policy-v1
---

# Candidate Selection

## Goal

Build a capability-aware local model library over time, with a strong local coding/agentic model as the highest-priority track. Select one eligible candidate per cycle for a full benchmark, while maintaining separate tracks for general/agentic text, MoE efficiency, image understanding/generation, audio and video transcription, and other modalities that are useful to AJ. Optimize for the most capable models that fit the available local hardware, not for one universal leaderboard.

## Eligibility

- 25B–150B parameter class, or a clearly documented MoE with comparable active parameters.
- GGUF or another llama.cpp-compatible format with a stable release.
- Public model card, license, quantization metadata, and known context length.
- Evidence of current Hugging Face momentum: recent release/update, meaningful downloads/likes/discussion, or credible trend placement. Record the evidence and date; never rely on an uncited ranking.
- Fits available Toshiba storage with at least 20% free space retained.
- No candidate may displace the production model automatically.

## Capability tracks and scoring

Every research snapshot must classify each candidate by capability track and record the evidence separately:

- **General/agentic text:** chat, coding, debugging, planning, tool use, structured output, reasoning mode, and context retention.
- **MoE efficiency:** total parameters, active parameters, expert count/routing, memory footprint, prompt throughput, generation throughput, and concurrency scaling. MoE is an efficiency/capability attribute, not an automatic quality advantage.
- **Vision/image:** image understanding, OCR, chart/screenshot interpretation, image generation or editing where supported, supported local runtime, and tested VRAM/RAM requirements.
- **Audio/video:** speech recognition, diarization, timestamps, translation, long-file handling, and video-audio extraction/transcription throughput. Keep ASR/TTS/video models as separate roles when they are not one model.
- **Operational fit:** format/runtime compatibility, quantization, context or input limits, model size, license, revision, checksum, hardware fit, and maintenance momentum.

Use a track-specific 0-5 score rather than forcing modalities into the text score. Record `capabilities`, `parameters_total`, `parameters_active`, `modalities`, `runtime`, `quantization`, `size_bytes`, `context_or_input_limits`, `hardware_fit`, and `last_verified_at` in the candidate record. A candidate can be the best model for one track without being a daily-driver replacement.

The library should retain a verified champion and at least one fallback per useful track, with immutable model/revision/checksum manifests and a clear `active`, `candidate`, `fallback`, `superseded`, or `blocked` lifecycle state. Re-test a champion when a material release, quantization, runtime, or hardware change justifies it; do not churn the library merely because a new model is trending.

## Selection score

Score each candidate 0–5:

- Coding/agentic evidence: 30%
- General-use quality: 20%
- Hugging Face momentum and maintenance: 15%
- Spark feasibility (VRAM/RAM, context, quantization): 15%
- Concurrency potential: 10%
- License/reproducibility/operational stability: 10%

Select the highest-scoring eligible candidate not benchmarked in the last 14 days, unless a regression or urgent release justifies a repeat. If the top candidate cannot be downloaded, choose the next eligible candidate and record why.

## Research output

Each research cycle writes a dated snapshot in `Research/YYYY-MM-DD.md` listing the shortlist, evidence links, score, disk estimate, selected model, rejected alternatives, and the reason for selection. Research must not download models or alter production services.

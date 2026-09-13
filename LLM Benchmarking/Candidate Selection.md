---
tags: [benchmarking, model-research, huggingface]
status: policy-v1
---

# Candidate Selection

## Goal

Select one general-use model per night for a full benchmark, prioritizing local agentic coding capability without losing the qualities AJ values in Qwen 3.8: strong general chat, compactness, and permissive behavior.

## Eligibility

- 25B–150B parameter class, or a clearly documented MoE with comparable active parameters.
- GGUF or another llama.cpp-compatible format with a stable release.
- Public model card, license, quantization metadata, and known context length.
- Evidence of current Hugging Face momentum: recent release/update, meaningful downloads/likes/discussion, or credible trend placement. Record the evidence and date; never rely on an uncited ranking.
- Fits available Toshiba storage with at least 20% free space retained.
- No candidate may displace the production model automatically.

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

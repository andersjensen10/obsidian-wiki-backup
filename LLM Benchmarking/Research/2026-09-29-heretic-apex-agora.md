---
tags: [agora, benchmarking, model-research, qwen3.6, uncensored, spark, type/research]
status: active-evaluation
snapshot_date: 2026-09-29
---

# Agora model research and initial deployment — 2026-09-29

## Decision

Agora needs an adult-theme-capable model that is not sexually pushy, while improving interactive throughput and usable conversation context. The prior `Qwen3.8-27B-Uncensored-HauhauCS-Aggressive` model was judged by AJ to be **too forward** for the intended slow-burn, character-led experience.

The selected evaluation model is **Qwen3.6-35B-A3B Uncensored Heretic Native-MTP-Preserved APEX I-Quality**.

- Repository: `SC117/Qwen3.6-35B-A3B-uncensored-heretic-Native-MTP-Preserved-APEX-GGUF`
- Immutable revision: `bdb921342e61db39d13c543102278f1d5ab654e1`
- File: `Qwen3.6-35B-A3B-uncensored-heretic-Native-MTP-Preserved-APEX-I-Quality.gguf`
- Size: `23,514,746,272` bytes
- SHA-256: `31a6a415d4de270cdd2128103a671202f4b92b6eb30c5f87934f3b06fc2a55cc`
- Model publisher positioning: 262K context, a refusal-reduced but not “zero-refusal” uncensored model, and preserved native MTP. These are publisher claims, not independent quality measurements.[1]

The HauhauCS **Aggressive** Qwen3.6 alternative was rejected for first evaluation because its explicit “0 refusal” positioning conflicts with the desired scene pacing and restraint. Genesis/Hermes derivatives remain later creative-writing experiments, not the initial dependable deployment choice.

## Spark deployment

The verified GGUF was downloaded to Spark internal SSD and made read-only after checksum validation. The immutable local manifest is:

`/home/aj/llm-benchmark-local/manifests/qwen3.6-heretic-apex-i-quality-2026-09-29.json`

It is active on the production llama.cpp endpoint (`:8014`) as:

`qwen3.6-35b-a3b-heretic-apex-i-quality`

Service profile:

- `131,072` total context
- `2` concurrent llama.cpp slots
- `65,536` tokens usable per slot/chat
- reasoning disabled for normal Agora persona chat
- native MTP enabled with `--spec-type draft-mtp --spec-draft-n-max 2`
- Qwen3.8 remains available through `/home/aj/bin/llama-model-select qwen3.8` as a reversible rollback

All 18 personas using the primary Spark connection were updated to the active model ID. The Spark connection default was updated too.

## Initial verification

All testing below used the actual Spark service while **ComfyUI remained resident** (its queue was empty); Fish Speech remained running. This is an idle-Comfy coexistence check, not proof that LLM generation remains unaffected during a heavy Comfy job.

### Load and context

- Server reported the intended model, two slots, and `65,536` context per slot.
- A live 60,019-token prompt completed successfully in 26.68 seconds and returned the requested exact reply (`context retained`).
- The model therefore has a verified live usable context above the former ~50K-per-slot Qwen3.8 service configuration.

### Two-chat throughput smoke test

Two simultaneous 180-token in-character requests completed successfully:

- Request 1: 3.811 s, 47.23 generated tokens/s
- Request 2: 3.810 s, 47.25 generated tokens/s
- Both replies were non-empty and finished only because they reached the deliberately fixed 180-token cap.

This is materially faster than the previously recorded Qwen3.8 **reasoning-on** baseline, but it is not a matched model-quality comparison. The old baseline had thinking enabled, whereas the new Agora profile intentionally disables it.

### Agora roleplay battery

`AgenticChatroomProject/scripts/eval-thinking-quality.mjs` was run live against the new served model with two distinct personas (Mira and Iris), six linked turns each, and both thinking settings.

- 24/24 final replies were non-empty.
- Thinking-off roleplay results were responsive and maintained distinct character voices.
- Average thinking-off TTFT: Mira 305 ms; Iris 239 ms.
- Average total response time with thinking off: Mira 1.892 s; Iris 1.300 s.
- Thinking-on repeatedly entered Agora’s budget-exhaustion retry path and made multi-turn reasoning verbose/slow. Keep `AGORA_THINKING=false` as the default.
- The difficult lantern-logic prompt remains weak and verbose, so this is not a general reasoning-model promotion claim. Its value proposition is persona chat, context, restraint, and interactive speed.

## Current state

The model is **ready for hands-on Agora testing**. The next acceptance step is qualitative playtesting of adult-theme restraint, consent/boundary adherence, slow-burn pacing, character voice, long-context recall, and behavior while ComfyUI has an active job.

## Sources

[1] https://huggingface.co/SC117/Qwen3.6-35B-A3B-uncensored-heretic-Native-MTP-Preserved-APEX-GGUF

## Related notes

- [[LLM Benchmarking/Results to Date|Local LLM benchmark results to date]]
- [[Agentic Chatroom Project/Feature Development/FR-001-eval-thinking-off-quality-REPORT|Agora thinking-off quality evaluation]]

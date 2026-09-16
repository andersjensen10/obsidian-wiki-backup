# Research Scout — Qwen3-TTS vs Fish Audio S2 for AJ’s Voice Pipeline

**Run date:** 2026-09-16  
**Selection basis:** relevance to active work, evidence availability, practical usefulness, and novelty.  
**Previous-run check:** the 2026-09-15 note covered local LLM serving and multi-agent inference. This report deliberately avoids repeating that topic and focuses on TTS/voice-pipeline decisions. No other dated morning report was present in the Research folder.

## Three candidate topics

1. **Qwen3-TTS versus Fish Audio S2 for the local voice pipeline — selected.** This is directly relevant to AJ’s Fish Speech dashboard, Voice Lab, and the already-documented experimental Qwen TTS service.[unverified] Both projects have primary repositories and technical reports, making a grounded comparison possible.[1][3]
2. **Agora’s current conversational-agent lifecycle and event-delivery patterns.** This could inform Agora’s regeneration/variant work and operational observability, with official quickstarts and API documentation available. It is useful, but less immediately actionable than the active TTS stack.[unverified]
3. **A bounded benchmark protocol for two-slot local LLM delegation.** This follows naturally from yesterday’s report and would produce a useful Spark measurement, but it is intentionally deferred to avoid repeating yesterday’s subject.[unverified]

## Decision

The selected topic is **Qwen3-TTS versus Fish Audio S2 for AJ’s local voice pipeline**. It has the strongest combination of active-project relevance, primary-source evidence, and a concrete next experiment. The comparison is not a claim that one model is universally better; the systems expose different trade-offs and the published measurements are not directly comparable.

## Executive finding

**Keep Fish Speech as the current production-like experimental backend, and test Qwen3-TTS as a second path for fast, controllable, rights-clear fictional voices and short interactive utterances. Do not replace the current Fish path based on published numbers alone.**

Fish Audio S2 is the closer fit for AJ’s existing Voice Lab because it natively supports multi-speaker and multi-turn generation, free-form instruction control, short-reference cloning, and an existing working integration on the Spark.[3][4]

Qwen3-TTS is the more interesting challenger for low-latency voice design and lightweight cloning: its released 12Hz family includes 0.6B and 1.7B variants, supports streaming, and advertises 3-second cloning for its Base models.[1][2]

The important operational distinction is serving footprint. The official vLLM recipe reports that S2 Pro loads at about 48.3 GiB and peaks around 48.9 GiB on an A800, with the reference setup using a single 80 GB GPU; that is materially different from assuming that a 4B model is automatically light enough for every local GPU.[5] Qwen’s repository exposes smaller 0.6B models, but this report found no directly comparable, official Spark/GB10 benchmark, so Qwen’s likely deployment advantage remains an open hypothesis rather than a sourced performance result.[unverified]

## Sourced facts

### Fish Audio S2

Fish Audio’s S2 technical report describes an open-sourced TTS system with multi-speaker, multi-turn generation and natural-language instruction following.[4] The report says the released package includes model weights, fine-tuning code, and an SGLang-based inference engine.[4]

The report’s stated inference-engine result is an RTF of 0.195 and time-to-first-audio below 100 ms, but those are authors’ measurements on their serving setup and hardware, not a prediction for AJ’s Spark.[4] The repository describes short-reference cloning, typically using 10–30 seconds of reference audio, and native multi-speaker generation via speaker tokens.[3]

The official vLLM recipe serves S2 Pro through vLLM-Omni using an OpenAI-compatible `/v1/audio/speech` endpoint.[5] The same recipe requires both `ref_audio` and `ref_text` for cloning and documents 44.1 kHz mono WAV output.[5]

### Qwen3-TTS

Qwen’s repository describes Qwen3-TTS as a family supporting voice cloning, voice design, streaming generation, and natural-language voice control.[1] The 12Hz release includes 0.6B and 1.7B Base models for cloning, plus VoiceDesign and CustomVoice variants.[1]

The Qwen technical report states that the 12Hz architecture can emit its first audio packet with latency as low as 97 ms for the 0.6B variant and 101 ms for the 1.7B variant.[2] It also reports support for 10 languages and describes 3-second zero-shot voice cloning.[2]

The repository labels the released Qwen3-TTS code and models as Apache 2.0, which is a materially different licensing starting point from systems that restrict weights or outputs.[1] License suitability still requires checking each exact model artifact and the intended use before shipping anything.[unverified]

## Comparison for AJ’s pipeline

| Criterion | Fish Audio S2 | Qwen3-TTS | Practical reading |
|---|---|---|---|
| Existing integration | Working Spark service and dashboard path documented locally | Separate experimental local tester documented locally | Fish has lower integration risk for now. |
| Voice cloning | 10–30-second references are described by the project; exact transcript required by AJ’s current service notes | 3-second cloning is claimed for Base models | Qwen is attractive for fast experimentation; test identity stability rather than trusting the minimum clip length. |
| Voice design | Strong instruction-following and inline expressive control are central to S2’s report | Dedicated VoiceDesign models accept natural-language descriptions | Qwen may be better for generating fictional voices without reference audio; this needs listening tests. |
| Dialogue | Native multi-speaker and multi-turn generation | The reviewed release material emphasizes single-voice cloning/design workflows | Fish is the stronger first candidate for scripted multi-character scenes. |
| Streaming | Reported sub-100 ms first audio on the authors’ engine | Reported 97–101 ms first-packet latency for 12Hz variants | Published latencies are not comparable across hardware and serving stacks. |
| Footprint | Official vLLM recipe reports ~48.3 GiB load on A800 | 0.6B and 1.7B variants are available | Qwen deserves a Spark feasibility test; no official GB10 result was found. |
| Output integration | Official vLLM recipe exposes OpenAI-compatible audio speech | Repository provides Python and local-demo paths; a compatible server can be tested separately | Keep an adapter boundary so the dashboard can switch backends without changing Voice Lab data. |

The table mixes externally sourced facts with local-project context and analysis. The Fish/Qwen feature claims are sourced; the judgments in the final column are engineering analysis based on AJ’s documented pipeline and are not published benchmark results.

## What matters specifically for AJ

AJ’s current Fish service is already warm-tested at roughly 13× realtime in the local inventory, and the dashboard has a working chunk queue, Voice Lab, saved outputs, and benchmark views. That local measurement is more relevant to an eventual decision than Fish Audio’s headline RTF because it reflects the actual Spark, current service, and current workload. It is local project evidence, not an independent external benchmark.

Fish’s biggest present advantage is workflow fit: Voice Lab already performs source preparation, vocal separation, transcription, concatenation, and publishing into Fish reference voices. Moving immediately to Qwen would duplicate that pipeline before answering whether the output is better enough to justify the operational cost.

Qwen’s biggest potential advantage is architectural choice, not a guaranteed quality win. The existence of a 0.6B Base model and a dedicated VoiceDesign model creates a plausible path to a smaller, faster experimental service, while the 12Hz report emphasizes causal streaming and low first-packet latency.[1][2] That hypothesis should be tested on AJ’s actual Spark rather than inferred from parameter count.

The standing fictional-character consent rule remains important. A technically capable cloning system should be used only with fictional characters or appropriately authorized source material; no benchmark should use a real identifiable person’s voice.

## Recommended next experiment

Build a **backend-neutral 12-case listening and timing benchmark** before changing the active Hermes TTS provider:

1. Use six short utterances and six medium utterances covering plain narration, numbers, punctuation-heavy text, whispered or emotional direction, and a two-character exchange.
2. Use only fictional voices or synthetic/reference material with clear permission.
3. Generate Fish and Qwen outputs from equivalent text, keeping a metadata record of model, revision, reference audio, transcript, seed/settings, wall time, audio duration, and errors.
4. Measure time to first audio if the server exposes it, total wall time, real-time factor, output duration, and failure/retry rate.
5. Score intelligibility, voice identity, prosody control, artifact rate, and chunk-boundary quality separately; do not collapse all judgments into one “sounds good” score.
6. Test Qwen’s 0.6B Base and 1.7B Base if both fit comfortably, and compare them against Fish with the same short fictional reference. Treat Qwen’s 3-second claim as a starting condition, not a guarantee.
7. Run the existing Fish path as the control and leave Hermes on Edge until the measured local path is both acceptably fast and audibly reliable.

**Decision rule:** keep Fish as the default experimental backend if it wins workflow fit and acceptable quality, even if Qwen wins raw latency; add Qwen as a selectable backend if it offers a meaningful latency or voice-design advantage without materially worse identity stability or artifacts. Only consider replacing Fish after repeated local runs, not after a single sample.

## Uncertainty and open questions

- No official Qwen3-TTS benchmark for AJ’s Spark GB10/aarch64 setup was found in the consulted sources.[unverified]
- Fish’s published 0.195 RTF and sub-100 ms first-audio figures use the authors’ inference engine and hardware; they cannot be transferred directly to AJ’s service.[4][5]
- The reports’ benchmark tables are useful for model-development context, but they do not answer which system sounds better on AJ’s fictional-character references, tag style, chunk sizes, or local audio chain.[2][4]
- The Qwen repository says other models mentioned in the technical report will be released in the future, so the currently available subset may not be the final family.[1]
- The most decision-relevant missing evidence is a controlled, same-text, same-reference, same-box comparison with listening notes and failure logs.

## Why this matters to AJ

This research does not justify a risky migration. It identifies a low-risk division of labor: Fish remains the integrated multi-speaker and Voice Lab control, while Qwen becomes a focused challenger for low-latency voice design and short-reference cloning. The adapter and benchmark should come before any provider switch.

## Sources

[1] https://github.com/QwenLM/Qwen3-TTS
[2] https://arxiv.org/html/2601.15621
[3] https://github.com/fishaudio/fish-speech
[4] https://arxiv.org/html/2603.08823v2
[5] https://recipes.vllm.ai/fishaudio/s2-pro

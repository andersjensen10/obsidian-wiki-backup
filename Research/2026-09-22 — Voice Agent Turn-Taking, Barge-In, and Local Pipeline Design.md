# Research Scout — Voice-Agent Turn-Taking, Barge-In, and Local Pipeline Design

**Run date:** 2026-09-22 08:00 CEST  
**Selection basis:** relevance to AJ’s Fish Speech/TTS work, evidence availability, practical usefulness, novelty, and non-repetition.

## Three candidate topics

1. **Voice-agent turn-taking and interruption control — selected.** This is the most actionable next step for AJ’s voice work: the existing TTS pipeline can produce audio, but a conversational agent also needs reliable speech-start detection, end-of-turn decisions, barge-in cancellation, and recovery from false interruptions.
2. **Local LLM inference for tool-using voice agents.** This would connect the Spark model, Hermes delegation, and a future voice persona, but it overlaps with the 2026-09-15 inference report and should follow a measurable turn-taking baseline.
3. **Godot as an agent-facing interaction shell.** This remains a useful future direction for a persona or robot-like interface, but it is less immediately useful than establishing a robust audio interaction loop.

## Decision

The selected topic is **how modern voice-agent stacks separate VAD, turn completion, interruption handling, and latency optimization—and what a bounded local experiment should measure for AJ’s Fish Speech pipeline**.[unverified]

## Executive finding

Voice turn-taking is not one classifier. Current production-oriented stacks separate at least four decisions: whether speech is present, whether the user has finished a thought, whether speech during agent playback is a real interruption, and whether the system should precompute a response before the turn is fully confirmed.[1][2][4]

The key design implication for AJ is to keep **fast acoustic detection** and **slower semantic turn completion** as separate stages. VAD can react quickly to speech onset and support barge-in, while a turn detector or STT endpointing policy decides whether a pause is actually the end of the user’s thought.[1][4][5]

For a local Fish-based prototype, start with a small explicit state machine and measurable thresholds rather than attempting a full speech-to-speech stack. The first useful target is not “human-level conversation”; it is predictable behavior under scripted pauses, backchannels, corrections, and interruptions.[unverified]

## Sourced facts

### 1. VAD is necessary but insufficient

LiveKit describes VAD as detecting periods of silence and then applying phrase-endpointing heuristics; it also supports a model that uses the meaning and acoustic properties of speech to decide whether a turn is complete.[1] Pipecat makes the same distinction: VAD detects speech versus non-speech, while user-turn strategies decide when a turn starts and ends.[4]

Pipecat’s documented local Silero VAD configuration uses short start/stop windows, while its default turn-end path can use an AI-powered Smart Turn analyzer rather than treating every silence interval as a completed turn.[4] Smart Turn is specifically described as using intonation and linguistic signals to distinguish a natural completion from a pause.[5]

Silero’s project README reports that 30+ ms audio chunks take less than 1 ms on a single CPU thread, that the JIT model is around two megabytes, and that the project supports 8 kHz and 16 kHz sampling.[6] Those figures make it a plausible low-overhead front end for a local experiment, but they are project-reported characteristics rather than an AJ-specific benchmark.[6]

### 2. End-of-turn detection is a latency/overlap trade-off

LiveKit’s recommended configuration exposes a minimum endpointing delay of 0.5 seconds and a maximum of 3.0 seconds, while allowing fixed or dynamic behavior.[2] Its troubleshooting guidance maps premature cut-offs to a turn detector or longer minimum delay, and maps interruptions caused by short acknowledgments to adaptive interruption handling or higher minimum duration/word thresholds.[2]

Pipecat documents a simple speech-timeout strategy as an alternative to Smart Turn and gives a 0.6-second default user speech timeout in its reference material.[4] These values should be treated as starting points, not universal truths: the right delay depends on language, microphone conditions, speaking style, and whether the agent is optimized for rapid command execution or free conversation.[unverified]

### 3. Barge-in must be independent of final turn closure

LiveKit treats interruption handling as a separate concern from deciding when the user’s turn is complete. Its configuration includes an interruption enable switch, minimum speech duration, minimum word count, and a false-interruption timeout that can allow the agent to resume after a detected interruption produces no transcript.[2]

That separation is important for a local pipeline: the agent should stop or duck TTS as soon as credible speech begins, but it should not necessarily commit the audio as a complete user turn at that same instant.[unverified] A practical sequence is:

```text
agent speaking
  -> speech onset detected
  -> stop/flush TTS playback quickly
  -> keep buffering and transcribing user audio
  -> classify real interruption vs backchannel/noise
  -> either resume, discard, or submit a new user turn
```

A short “uh-huh” or microphone artifact should not permanently discard the agent’s response. Conversely, a correction such as “no, I meant…” must cancel playback promptly and receive priority.[unverified]

### 4. Preemptive generation reduces latency but wastes work

LiveKit documents preemptive generation as starting LLM—and optionally TTS—work before the user’s turn is fully confirmed.[2] The same documentation warns that preemptive TTS trades lower latency for wasted compute when the user continues speaking or interrupts.[2]

For AJ’s local stack, preemptive **LLM** generation may be worth testing after the basic state machine works, but preemptive **TTS** should initially remain disabled.[unverified] Audio synthesis is the expensive and externally visible side effect: generating it before turn confirmation increases cancellation complexity, queue pressure, and the chance of playing a response to an incomplete thought.[unverified]

### 5. Local versus server-side turn detection

LiveKit lists several valid modes: a turn-detector model, realtime-model detection, VAD-only, STT endpointing, and manual control.[1][3] It recommends different modes for different constraints, including VAD-only when minimal latency or language coverage matters and manual control for push-to-talk interactions.[1]

Pipecat’s Smart Turn documentation describes a local ONNX model and says its weights are bundled with the integration, with VAD still required to segment the speech before turn classification.[5] This suggests a useful local architecture for AJ: Silero VAD for immediate boundaries, a local Smart Turn-style classifier if language and CPU budget permit, and a deterministic timeout fallback when the classifier is unavailable.[unverified]

## Recommended architecture for AJ’s pipeline

Treat the voice loop as five independently observable stages:

1. **Input conditioning:** capture, resample, and optionally suppress noise/echo.
2. **Speech activity:** detect speech start/stop with a local VAD.
3. **Turn policy:** decide whether silence means “done,” “thinking,” or “continue.”
4. **Interruption controller:** stop/flush TTS, cancel generation, and classify false interruptions.
5. **Output scheduler:** queue audio chunks, expose cancellation, and record what was actually played.

The Fish Speech synthesis service should be downstream of the interruption controller, not the owner of conversation state.[unverified] It should accept cancellable jobs or chunk streams and report job identity, emitted audio duration, cancellation, and completion.[unverified] That makes it possible to distinguish “the model stopped generating” from “the speaker stopped playing,” which is necessary for debugging clipped or stale responses.[unverified]

## Proposed measurement protocol

Build a disposable harness using recorded or synthetic fixtures before connecting a live microphone:[unverified]

| Scenario | Primary metric | Failure to count |
|---|---|---|
| Clean statement + 0.2–1.5 s pause | end-of-turn latency | response starts while the user continues |
| Mid-sentence correction | barge-in reaction time | stale TTS remains audible |
| “uh-huh”, “yeah”, breath, keyboard noise | false-interruption rate | agent response is lost unnecessarily |
| Two consecutive user turns | handoff latency | second turn is attached to the wrong response |
| Long pause while thinking | premature-response rate | agent answers before completion |
| Cancel during streamed TTS | cancellation latency | queued audio continues after cancel |
| Reconnect or dropped audio chunk | recovery correctness | duplicate or orphaned playback |

Record at least these timestamps: speech onset, VAD onset, VAD stop, turn decision, interruption decision, TTS cancellation request, last audio played, and new response start.[unverified] Report distributions rather than only averages, because occasional long tails are likely to dominate perceived quality.[unverified]

## Decision rule

Keep the simple VAD-plus-timeout baseline if it is predictable and the measured errors are acceptable for a push-to-talk or command-oriented persona. Add a local semantic turn detector only if the baseline cuts off natural pauses or creates excessive dead air. Add preemptive TTS only if the latency gain remains meaningful after cancellation waste and stale-audio failures are measured.[unverified]

## Why this matters to AJ

AJ’s Fish Speech dashboard already gives a strong foundation for synthesis, chunking, voice cloning, and benchmark output. The next conversational risk is not another voice-model comparison; it is orchestration around the synthesizer: deciding when to yield, when to wait, and how to cancel audio that is already being generated or played.[unverified]

A narrow turn-taking harness would also make later Hermes or Agora voice integration safer. It would expose a stable event contract—speech started, turn committed, interruption accepted, interruption rejected, audio cancelled—that can be consumed by a UI or persona runtime without coupling those systems to VAD internals.[unverified]

## Uncertainty and open questions

- The retrieved documentation gives sensible defaults and tuning knobs, but it does not establish the best values for AJ’s microphone, room acoustics, languages, or Fish Speech latency.[1][2][4]
- Silero’s reported speed and model size need verification on AJ’s actual laptop and Spark hardware before being used as capacity assumptions.[6]
- Smart Turn language coverage, CPU cost, and behavior on Danish/English mixed speech need a local test; no AJ-specific benchmark was found in this run.[unverified]
- Echo cancellation and playback leakage may dominate false interruptions in a laptop setup; this report did not benchmark the microphone/speaker path.[unverified]
- The report did not compare OpenAI Realtime’s server-side VAD behavior experimentally; its official guide positions Realtime as handling audio turns and interruptions, but that is a hosted architecture rather than a direct local replacement.[7][8]

## Recommended next experiment

Implement a **local turn-taking fixture harness** around the existing voice services, without changing production defaults:[unverified]

1. Feed six scripted fixtures into a VAD and timeout baseline.
2. Log the event timestamps listed above.
3. Add cancellation to one Fish Speech output job and verify that no queued audio plays after cancellation.
4. Compare fixed endpointing at 0.4 s, 0.6 s, and 0.9 s.
5. Add a semantic turn detector only if the baseline’s premature-response or dead-air metrics justify it.
6. Test false interruptions from backchannels and playback leakage.
7. Keep the best configuration only if it improves the measured target without worsening cancellation correctness.

## What to queue next

The most useful follow-up is this fixture harness and a local benchmark of VAD/endpointing/cancellation behavior.[unverified] The deferred alternatives remain local LLM tool-use for voice agents and a Godot agent-facing interaction shell.[unverified]

## Sources

## Sources

[1] https://docs.livekit.io/agents/logic/turns
[2] https://docs.livekit.io/agents/logic/turns/tuning
[3] https://docs.livekit.io/agents/logic/turns/turn-detector
[4] https://docs.pipecat.ai/guides/learn/speech-input
[5] https://docs.pipecat.ai/pipecat-cloud/guides/smart-turn
[6] https://github.com/snakers4/silero-vad/blob/master/README.md
[7] https://platform.openai.com/docs/guides/realtime
[8] https://livekit.com/blog/turn-detection-and-interruption-handling

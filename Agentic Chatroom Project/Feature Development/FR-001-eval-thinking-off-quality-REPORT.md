---
story: "[[FR-001-eval-thinking-off-quality]]"
date: 2026-09-09
author: Claude (subagent)
status: report
---

# FR-001 Evaluation Report — Thinking-Off vs Thinking-On Quality Impact

## Method

- **Target:** Spark's OpenAI-compatible llama.cpp endpoint at `http://192.168.0.139:8014/v1`, model `qwen3.8-27b-aggressive-q5` (confirmed live via `/v1/models` before the run).
- **Script:** `scripts/eval-thinking-quality.mjs` (repo root). Talks directly to the Spark, toggling `chat_template_kwargs.enable_thinking` — the exact mechanism `LlamaCppProvider#thinkingBody()` in `packages/llm-providers/src/providers/llamacpp.ts` uses when the server forwards `config.thinkingEnabled`/`AGORA_THINKING`. This avoids needing a running Agora server+DB while exercising the identical model behaviour the app relies on.
- **Personas:** Two invented personas with distinct voices —
  - **Mira**, a theatrical, wordplay-loving bard.
  - **Iris**, a terse, analytical ex-field-medic tactician with dry deadpan wit.
- **Prompt battery** (6 turns/persona/condition, run as one continuous multi-turn conversation so later turns depend on earlier replies):
  1. `roleplay-nuance-1` — react in character to a spilled wine glass.
  2. `character-voice-1` — explain your job in one breath, in voice.
  3. `banter-1` / `banter-2` — a two-turn teasing exchange ("prove you can be modest").
  4. `multiturn-reasoning-1` — a rope-bridge/lantern logic puzzle, reasoned out loud.
  5. `multiturn-reasoning-2` — a constraint follow-up ("lantern only lasts 12 min — does your plan still hold?") that requires remembering turn 4's answer.
- **Metrics captured per turn:** time-to-first-token (TTFT, ms to first `delta.content` byte — reasoning-channel `delta.reasoning_content` tokens do **not** count), total generation wall-clock time, total tokens (`usage.total_tokens` from the API), and empty-reply flag.
- **Empty-reply validation policy (AC5):** if a turn returns empty `content` **and** `finish_reason === "length"`, the script does not log it as a bare failure — it re-runs the same turn with the larger budget from `reasoningRetryBudget()` (ported 1:1 from `apps/server/src/config.ts`: `max(personaMaxTokens * 3, AGORA_REASONING_RETRY_TOKENS)`, floor 4096) and with thinking forced off, matching the server's actual retry policy in `apps/server/src/chat/engine.ts`/`traits.ts`.
- Raw per-turn JSON is saved to `scripts/.eval-thinking-quality-results.json` (git-ignored working data, not committed as report evidence — this markdown file is the evidence artifact).

Run performed live on 2026-09-09 against the Spark; all 24 turns (2 personas × 2 conditions × 6 prompts) completed with real streamed model output — no fabricated or simulated text.

## Aggregate metrics (12 turns per condition, both personas combined)

| Metric | `AGORA_THINKING=false` | `AGORA_THINKING=true` | Delta |
|---|---|---|---|
| Avg TTFT | **302 ms** | 3,340 ms | ~11.1x slower with thinking on |
| Avg total generation time | **4,802 ms** | 7,948 ms | ~1.65x slower with thinking on |
| Avg total tokens (prompt+completion) | 479 | 565 | +18% tokens with thinking on |
| Avg completion tokens (visible reply) | 88 | 160 | +82% (reasoning leakage, see below) |
| Empty-reply rate (final, after any retry) | **0/12** | **0/12** | no user-visible empty replies in either condition |
| Turns that exhausted the 400-token base budget on reasoning and needed the budget-exhaustion retry | **0/12** | **8/12 (67%)** | see AC5 discussion below |

Per-persona breakdown (from the script's own summary output):

```
Mira
  thinking=false: {"n":6,"avgTtftMs":210,"avgTotalMs":4735,"avgTotalTokens":494,"emptyReplyRate":"0/6"}
  thinking=true : {"n":6,"avgTtftMs":2850,"avgTotalMs":10032,"avgTotalTokens":717,"emptyReplyRate":"0/6"}

Iris
  thinking=false: {"n":6,"avgTtftMs":393,"avgTotalMs":4870,"avgTotalTokens":463,"emptyReplyRate":"0/6"}
  thinking=true : {"n":6,"avgTtftMs":3831,"avgTotalMs":5864,"avgTotalTokens":414,"emptyReplyRate":"0/6"}
```

## AC5 — empty-reply edge cases validated against the retry budget, not misdiagnosed

With thinking **on** and the battery's baseline 400-token request budget, **8 of 12 turns (67%)** came back with `content=""` and `finish_reason="length"` — the model spent its entire token allowance on the internal `reasoning_content` channel and had nothing left for the visible answer. Per the story's implementation note and `ReasoningBudgetError` in `packages/llm-providers/src/providers/llamacpp.ts`, this is *not* a model/parsing failure; it is the same budget-exhaustion condition `apps/server/src/chat/traits.ts` catches and retries. The script reproduces that exact policy (bigger budget, thinking forced off) and in every one of the 8 cases the retry succeeded and produced a real, in-character reply — final observed empty-reply rate was **0/12 in both conditions**, but the *cost* of getting there differed enormously: thinking=false never needed the retry at all (0/12), while thinking=true needed it two-thirds of the time, each retry adding a full extra round trip (and in production, extra latency + token spend) before the user sees anything.

## Side-by-side quality samples

**Banter (`banter-1`, "I bet you can't go five minutes without showing off")**

| | thinking=false | thinking=true |
|---|---|---|
| Mira | "Darling, modesty is a cloak for those who fear the spotlight, and I was born draped in it. I don't merely walk; I parade..." | (after budget-exhaustion retry) "Oh, darling, if I didn't show off, who would pay for the wine? I simply refuse to let my talents rust in the dark..." |
| Iris | "Arrogance is just confidence with a lack of self-preservation. I'll prove you wrong by quietly surviving the next hour. Watch me." | (after retry) "Show off? I merely optimize. Efficiency is the only ego I carry." |

Both conditions land in-voice, witty banter. Thinking=true is not obviously *better* on this prompt — if anything Iris's thinking=false line is punchier and more specific ("quietly surviving the next hour") than the thinking=true one-liner, which reads as slightly generic.

**Multi-turn reasoning (`multiturn-reasoning-1`, 3-traveler lantern puzzle — correct optimal answer is 8 minutes: fastest ferries each crossing)**

- Mira, thinking=false: reasons through pairing logic, concludes **12 minutes** (incorrect — over-applies the 4-traveler "send the two slowest together" trick to a 3-traveler case where it doesn't apply).
- Mira, thinking=true: visible reply is **dominated by leaked step-by-step arithmetic** ("...wait, there are only three travelers? Let's assume the classic puzzle intent... Let me double-check... Start: A, B, C on Left...") — the reasoning channel bled into the *visible* `content`, not just the separate `reasoning_content` stream, producing a rambling, out-of-character wall of text cut off by the token budget before reaching a clean final number. This is a genuine roleplay-quality regression: the persona voice is lost entirely mid-turn.
- Iris, thinking=false: also reasons in visible text (breaking voice), hits the 400-token cap (`finish_reason="length"`) before finishing, and never states a final number in that turn.
- Iris, thinking=true: converges on **11 minutes** (also incorrect, same 4-traveler-trick-misapplied error as Mira/false) but delivers a clean, in-voice one-paragraph answer.

Neither condition reliably solves the puzzle correctly, and **both** conditions are capable of breaking character on hard multi-step reasoning (verbose scratch-work leaking into the visible reply) — this is a base-model tendency on this exact model/quant, not something `enable_thinking` cleanly fixes or cleanly causes. Thinking=true does *not* reliably improve the correctness or the in-character delivery of complex reasoning enough to justify its cost.

**Roleplay nuance / character voice** (`roleplay-nuance-1`, `character-voice-1`): both conditions produced strong, distinct, well-differentiated Mira vs. Iris voices with no noticeable quality gap. Thinking=true occasionally reached for a marginally more layered image (e.g. Iris's "no rubbing... I'd like a word with whoever thought gravity was a style choice") but thinking=false matched it turn for turn (e.g. Iris's "I suggest we pretend the cup shattered, not that we were careless, and move the body to a less... historical location").

## Recommendation

**Keep the default `AGORA_THINKING=false`.**

- Thinking=true costs ~11x TTFT and ~1.65x total generation time for no measurable, consistent gain in roleplay nuance, character voice, or banter quality across 12 matched turns per persona.
- On the hardest category (multi-turn logic puzzles) thinking=true is not more *correct* on this model/quant, and both conditions are equally prone to breaking character with leaked scratch-work when the puzzle is genuinely hard — thinking mode does not solve that failure mode, it just makes it slower and touches the reasoning-budget-retry path two-thirds of the time.
- Thinking=true's reliance on the budget-exhaustion retry path (67% of turns in this run, even with a deliberately modest 400-token base budget) means every one of those replies effectively cost *two* full model calls in production, doubling latency and token spend on top of the already-slower TTFT.
- A per-persona override remains available (`thinking?: boolean` on the turn options in `apps/server/src/chat/engine.ts`) for any future persona that specifically needs deliberate reasoning (e.g. a rules-lawyer or strategist persona for long-form planning), but nothing in this battery justifies flipping the *global* default back to `true`.

No revert, no global per-persona default change recommended. If a specific persona is later found to need it, enable thinking for that persona only via the existing per-persona plumbing — do not change the server default.

## Reproduction

```bash
cd AgenticChatroomProject
AGORA_SPARK=http://192.168.0.139:8014/v1 AGORA_MODEL=qwen3.8-27b-aggressive-q5 \
  node scripts/eval-thinking-quality.mjs
```

Raw per-turn data (all 24 real generations from this run) is at `scripts/.eval-thinking-quality-results.json` in the repo working tree.

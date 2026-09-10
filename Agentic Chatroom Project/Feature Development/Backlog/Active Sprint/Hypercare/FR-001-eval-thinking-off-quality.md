---
tags: [project/agora, type/hypercare]
status: hypercare
origin: feature-request
source: "[[Next Level Agentic Chatroom Project-ARCHIVE]]"
criticality:
  impact: high
  urgency: high
size: M
dependencies:
  - "Spark up at 192.168.0.139:8014"
  - "Qwen reasoning model on Spark"
matured: 2026-09-08
matured_by: Scrummaster
hypercare_since: 2026-09-10
---

# Evaluate Quality Impact of Thinking-Off (`AGORA_THINKING=false`)

## Context
Extracted from [[Next Level Agentic Chatroom Project-ARCHIVE]] (Priority: P0). Commit `366e7b1` introduced `config.thinkingEnabled` (env `AGORA_THINKING`, default `false`) which yielded an immediate ~5x speed/token improvement by suppressing reasoning chains on `qwen3.8-27b-aggressive-q5`. However, the qualitative impact on persona voice, nuance, and humor was never measured, posing a silent regression risk across all chat interactions. Criticality is High/High because it impacts baseline response quality for every active persona.

## User story
As AJ, I want a structured evaluation comparing persona outputs with `AGORA_THINKING=false` versus `AGORA_THINKING=true`, so that we have verified data to decide whether to keep the default false, revert to true, or configure thinking per-persona.

## Acceptance criteria
- [ ] An automated or reproducible test script runs a standard battery of evaluation prompts across at least two distinct personas (e.g. Mira and Iris).
- [ ] Prompts evaluate roleplay nuance, character voice adherence, bantering ability, and reasoning under complex multi-turn prompts.
- [ ] Metrics captured per turn: time-to-first-token, total generation time, total tokens consumed, and empty-reply occurrence rate.
- [ ] A written evaluation report is produced documenting side-by-side responses and concluding with a clear recommendation (keep default false, make per-persona, or revert).
- [ ] Any empty-reply edge cases are validated against `AGORA_REASONING_RETRY_TOKENS` settings rather than misdiagnosed as model failure.

## Implementation notes
- Server config in `apps/server/src/config.ts` controls `thinkingEnabled` via `AGORA_THINKING`.
- Per-persona override is already plumbed in the persona data model and provider call in `apps/server/src/chat/`.
- The backing model on Spark (`http://192.168.0.139:8014/v1`) is `qwen3.8-27b-aggressive-q5`. Remember from [[NOTES]] that reasoning models empty replies are caused by budget exhaustion (`ReasoningBudgetError`), not parsing errors.
- Existing live test scripts in `scripts/` (e.g. `scripts/live-bugfix-check.mjs`) provide a reference for automated chat interaction.

## Non-goals
- Re-architecting the chat completion pipeline or changing token streaming logic.
- Building a new UI dashboard for evaluation metrics (markdown report or script output suffices).

## Definition of done
- Evaluation script `scripts/eval-thinking-quality.mjs` exists and executes cleanly against the Spark.
- Output report filed in `Agentic Chatroom Project/` or `Feature Development/` with concrete verdict.
- `npm run verify` passes with 0 errors.

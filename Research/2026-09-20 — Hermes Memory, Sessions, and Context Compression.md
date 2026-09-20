# Research Scout — Hermes Memory, Sessions, and Context Compression

**Run date:** 2026-09-20 08:00 CEST  
**Selection basis:** relevance to AJ’s active Hermes/Bot work, evidence availability, practical usefulness, novelty, and non-repetition.

## Three candidate topics

1. **Hermes memory, session persistence, and context compression — selected.** This is directly relevant to AJ’s long-lived Herm sessions, scheduled Research Scout, Bot Mode, and active concern about keeping durable facts distinct from transient task state.
2. **MCP Apps and embedded agent interfaces.** This would connect to Agora’s chatroom UI and future tool-backed dashboards, but it is a forward-looking integration topic rather than an immediate Hermes-operational risk.
3. **Turn-taking and interruption control for voice agents.** This would be useful for the Fish Speech dashboard and a future voice-enabled persona, but it overlaps more with the previous TTS report and is best treated as a controlled audio experiment after the backend benchmark.

## Decision

The selected topic is **how Hermes divides durable memory, searchable session history, and active-context compression—and what that implies for AJ’s long-running agents and cron jobs**.

## Executive finding

Hermes uses three different continuity mechanisms that should not be conflated:

- **Persistent memory** is a small, curated snapshot injected at session start. The documented limits are 2,200 characters for `MEMORY.md` and 1,375 for `USER.md`; memory is intentionally bounded and does not silently auto-compact.[1]
- **Session storage/search** is the durable transcript layer. Hermes stores session metadata and full message history in SQLite with FTS5 search, making old details recoverable without putting the entire history into every prompt.[3][7]
- **Context compression** is the active-window management layer. The built-in compressor summarizes or prunes working context, while gateway session hygiene provides a separate safety net for oversized long-running sessions.[6]

The practical recommendation is to keep using memory for stable, high-value facts; use session search or dated notes for recoverable detail; and treat compression as a lossy operational mechanism that must not be the only home for project decisions, test results, or provenance.[1][3][6]

## Sourced facts

### 1. Memory is a frozen, bounded startup snapshot

Hermes injects the two memory stores as a snapshot at session start, and the documentation says the snapshot does not change during the session.[1] This preserves prompt-cache stability, but it also means a memory write should not be expected to affect the current turn’s already-loaded context.[1][2]

The memory tool refuses writes that exceed the configured limit instead of silently dropping older entries.[1] That is a good safety property: compaction is explicit, so an agent must consolidate or remove content rather than assuming the system preserved everything.

**Operational implication for AJ:** the current memory should contain only cross-session facts that are repeatedly useful—environment conventions, standing preferences, and durable project topology.[1] A one-off bug result, a temporary TODO, or a detailed research finding belongs in a skill, project note, or session history instead.[1][3]

### 2. Session history is the searchable source of detail

Hermes stores conversations from CLI and gateway platforms in `~/.hermes/state.db`, including full message history, tool calls, token counts, timestamps, and session lineage.[3][7] The storage design includes FTS5 indexes and parent-session links for compression-triggered splits.[3]

The documentation explicitly distinguishes persistent memory from session search: memory is small and always present, while session search can recover specifics from older conversations without consuming the whole active prompt.[1] This is the right division for AJ’s workflow: memory says where the important systems are; session search can recover what was tried, when, and with which result.[1][3]

The session guide also warns that compression reduces active context but is not a privacy delete.[7] Old transcripts remain a separate storage concern, so `/compress`, `/new`, `sessions optimize`, and destructive pruning should be treated as different operations.[7]

### 3. Compression is a runtime control loop, not durable documentation

Hermes documents two independent compression layers. The agent-side `ContextCompressor` is the primary in-loop mechanism, with a default trigger around 50% of the model context; gateway session hygiene is a higher-threshold safety net around 85% for sessions that grow between turns.[6]

The context engine is pluggable and selected explicitly through `context.engine`; the built-in `compressor` uses lossy summarization, while alternative engines are not auto-activated.[6] The compression implementation also tracks provider usage anchors and has cooldowns and bounded recovery behavior for failed or stalled summary attempts.[6]

This makes compression an operationally sophisticated safeguard, but not a guarantee that every nuance survives. A summary can preserve the broad direction while losing exact commands, identifiers, negative results, or causal context. Those details need a durable home outside the compressed working window.

### 4. Cron prompts must be self-contained

Hermes’ cron guidance says scheduled agents start in fresh sessions and should not rely on conversational history for job-critical instructions; persistent memory is available, but the prompt itself should spell out the required commands and behavior.[5] The same guide recommends putting mechanical collection in a script and leaving interpretation to the agent.[5]

That design matches the Research Scout’s current setup: the prompt defines the mission, dated research notes preserve outputs, and the run can compare prior notes by reading the Research folder. A memory entry saying “Research Scout exists” is useful; the full previous report should remain in the note rather than in memory.

### 5. Bot Mode multiplies the need for explicit ownership

Bot Mode maps each Bot to a Hermes profile with isolated configuration, memory, skills, credentials, and chat history.[4] Routines are ordinary cron jobs namespaced to the Bot, and their results land in that Bot’s own chat history.[4]

The practical consequence is clear ownership: a Bot’s durable operating facts belong in that profile’s memory or skills, while cross-Bot coordination should use explicit messages, shared project notes, or other declared interfaces.[unverified] Copying large project state into every Bot’s memory would defeat the bounded-memory design and create drift.[unverified]

## Analysis for AJ’s setup

### Recommended information-placement rule

| Information | Best home | Reason |
|---|---|---|
| Stable machine/service facts | `MEMORY.md` | Needed across many sessions and cheap to inject. |
| Communication preferences | `USER.md` | User-level behavior, not project history. |
| Repeatable procedures | Skill `SKILL.md` and references | Reusable instructions load only when relevant. |
| Current project architecture | Project notes / repository docs | Must remain detailed and reviewable. |
| Research findings and citations | Dated Research notes | Preserves provenance and prevents memory bloat. |
| Exact prior experiments or failures | Session history plus a concise project note | Searchable detail with a durable summary. |
| Temporary task state | Current session or task file | Should expire instead of becoming permanent memory. |

This table is engineering guidance derived from Hermes’ documented separation of memory, sessions, skills, and compression; it is not a framework-enforced policy.[unverified]

### Failure mode to avoid: summary-only continuity

A long-running agent can appear consistent while silently losing the exact detail that makes work reproducible.[unverified] For example, “the voice pipeline was fixed” is not equivalent to preserving the failing symptom, the changed file, the measured result, and the verification command.[unverified] Compression can keep the first sentence while dropping the rest.[unverified]

The safer pattern is **summary plus pointer**: keep a compact durable statement in a project note, include the exact artifact path or commit, and let session search recover the original conversation when needed.[unverified] Memory should point toward the durable source, not become a second undocumented project database.[unverified]

### Failure mode to avoid: treating Bot isolation as shared knowledge

Because each Bot has its own profile and chat history, a fact learned by one Bot is not automatically a reliable fact for another Bot.[4] Shared project knowledge should therefore live in a deliberately shared note, repository document, or message exchange with an explicit owner.[unverified] This is particularly important for AJ’s Research Scout, coding agents, Agora work, and home-lab services, which have overlapping but different responsibilities.[unverified]

## Recommended next experiment

Run a **continuity drill** against one disposable Hermes session and one scheduled-style fresh session:[unverified]

1. Put one stable fact in memory, one detailed experiment in a Research note, and one temporary TODO only in the active session.
2. Generate enough tool output to trigger or manually invoke compression.
3. Start a fresh session and verify which facts are immediately present.
4. Use session search to recover the exact experiment detail.
5. Confirm that the temporary TODO is not mistakenly treated as a standing fact.
6. Repeat with a Bot profile if cross-Bot coordination is the target.

**Decision rule:** if exact commands, identifiers, and negative results are hard to recover, improve the note/pointer workflow rather than enlarging memory.[unverified] If recovery is reliable, keep memory small and use it as an index of durable context.[unverified]

## Why this matters to AJ

AJ is running a long-lived Hermes instance with scheduled research, Bot Mode, local-model delegation, voice services, Agora development, and a growing Obsidian knowledge base.[unverified] Those activities produce more state than a bounded memory snapshot can safely hold.[unverified] The strongest architecture is therefore not “remember more”; it is **place each kind of knowledge where Hermes can retrieve it with the right durability, scope, and provenance**.

This also protects the current memory budget. The loaded profile is already close to its configured character limit, so adding detailed run logs would make the highest-value facts harder to preserve. [unverified]

## Uncertainty and open questions

- The documentation describes the mechanisms and thresholds, but not the factual-retention quality of summaries across AJ’s actual model/provider combinations.[6]
- Session search can recover stored text, but this report does not benchmark retrieval quality for long tool outputs or heavily duplicated project terms.[1][3]
- Bot-to-Bot sharing patterns are documented, but the best ownership model for a mixed Agora/Hermes/Obsidian knowledge base remains an AJ-specific design choice.[4]
- No claim is made here that compression is lossless; the built-in engine is explicitly described as lossy summarization.[6]

## What to queue next

The strongest follow-up is the continuity drill above, using a disposable session and a small synthetic project record.[unverified] If AJ wants a more product-facing topic next, the two deferred candidates are MCP Apps for Agora/tool UIs and voice turn-taking for the Fish pipeline.[unverified]

## Sources

[1] https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
[2] https://hermes-agent.nousresearch.com/docs/user-guide/configuration
[3] https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage
[4] https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode
[5] https://hermes-agent.nousresearch.com/docs/guides/automate-with-cron
[6] https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching
[7] https://hermes-agent.nousresearch.com/docs/user-guide/sessions

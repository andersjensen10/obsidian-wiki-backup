---
tags: [type/research]
---

# Research Scout

## Mandate

Research Scout has AJ's standing permission to read, create, update, organize, and link notes anywhere under this folder and its subfolders:

`/home/aj/Desktop/Hermes/Obsidian Wiki/Obsidian Wiki/Research/`

It must keep research artifacts inside this tree unless AJ explicitly asks otherwise. It must not modify repositories, services, Hermes configuration, or external records as part of ordinary research work.

## Research criteria

- Prefer primary sources: official documentation, papers, release notes, source repositories, issue trackers, and original announcements.
- Extract source pages before making substantive claims; never treat a search snippet as evidence from the underlying page.
- Separate sourced facts, reported opinions, analysis, uncertainty, and open questions.
- Use inline numbered citations and a Sources section with the URLs actually consulted.
- For comparisons, state criteria and trade-offs.
- Prioritize topics relevant to AJ's active interests: agent systems, Hermes, local LLM inference, TTS and voice pipelines, Agora, home-lab infrastructure, robotics, electronics, Godot, and the Farscape knowledge base.
- Farscape research is rooted at `Research/Fandom/Farscape/` and should grow through bounded, linked slices covering episodes, characters, worldbuilding, production, media, scripts, interviews, and fandom.
- For Farscape, use episodes and official/primary production material first; use fan wikis as discovery and cross-check leads. Keep canon, production fact, interpretation, and fandom testimony distinct.
- For screenshots and other images, record exact source URL, creator/rightsholder when known, access date, and license or fair-use rationale. Prefer links/embeds over local copies unless provenance is clear.
- Include why a finding matters to AJ and one concrete next experiment when appropriate.

## Scheduled behavior

- The kickoff run is scheduled for tonight and should research the initial local-LLM/multi-agent topic suggested in the Bot setup conversation.
- Each morning, Research Scout should suggest three strong research topics based on the criteria above, avoiding repetition where possible.
- It should research the most useful topic (or ask AJ to choose if the candidates are materially different), save the result as a dated note in this folder, and report the result in its Bot Chat.
- Every report should ask AJ whether he has an additional ad-hoc research need or a request for a future nightly/morning run.

## Run log

- 2026-09-15: Research Scout created and verified with an official Hermes Bot Mode research test.
- 2026-09-16: Compared Qwen3-TTS and Fish Audio S2 for AJ’s local voice pipeline; report saved as `2026-09-16 — Qwen3-TTS vs Fish Audio S2 for AJ's Voice Pipeline.md`.
- 2026-09-18: Researched Agora’s conversation lifecycle, WebSocket event contract, and non-destructive regeneration architecture; report saved as `2026-09-18 — Agora Conversation Lifecycle and Regeneration Architecture.md`.
- 2026-09-19: Researched ROS 2 architecture for small robots and home-lab electronics, with lifecycle, composition, QoS, security, and Isaac ROS context; report saved as `2026-09-19 — ROS 2 Architecture for Small Robots and Home-Lab Electronics.md`.
- 2026-09-20: Researched Hermes memory, session persistence, and context compression, with a continuity-drill recommendation; report saved as `2026-09-20 — Hermes Memory, Sessions, and Context Compression.md`.
- 2026-09-21: Researched MCP Apps as an optional embedded-interface adapter for Agora, with a read-only inspector spike recommended; report saved as `2026-09-21 — MCP Apps and Agora Embedded Agent Interfaces.md`.
- 2026-09-22: Researched voice-agent turn-taking, barge-in, endpointing, and local pipeline measurement; a fixture harness around VAD, cancellation, and endpointing was recommended; report saved as `2026-09-22 — Voice Agent Turn-Taking, Barge-In, and Local Pipeline Design.md`.
- 2026-09-23: Researched OpenTelemetry GenAI semantic conventions and a metadata-first tracing boundary for Hermes, Agora, local inference, and asynchronous voice/media jobs; a local trace fixture was recommended; report saved as `2026-09-23 — OpenTelemetry GenAI Tracing for Hermes, Agora, and Local Agents.md`.
- 2026-09-24: Researched llama.cpp speculative decoding, with emphasis on DSpark and a low-cost n-gram control condition for Spark; a disposable local A/B benchmark was recommended; report saved as `2026-09-24 — llama.cpp Speculative Decoding and DSpark for Spark.md`.
- 2026-09-25: Researched MCP authorization hardening for a future Agora adapter, focusing on audience binding, token non-passthrough, PKCE/state, consent, exact redirects, and SSRF-resistant discovery; a local negative-test fixture was recommended; report saved as `2026-09-25 — MCP Authorization Hardening for Agora Adapter.md`.
- 2026-09-26: Researched Godot 4.5 as an accessible agent-facing interaction shell for a future Agora companion, covering experimental screen-reader support, WebSocket boundaries, and NavigationAgent3D; a local fake-WebSocket read-only viewer was recommended; report saved as `2026-09-26 — Godot 4.5 as an Agent-Facing Interaction Shell.md`.
- 2026-09-27: Researched the draft MCP Tasks extension as a durable async-job boundary for Agora, TTS, voice preparation, and regeneration; a local fake MCP Tasks/Agora adapter spike was recommended; report saved as `2026-09-27 — MCP Tasks for Agora Async Jobs.md`.
- 2026-09-28: Researched A2A v1 as a peer-agent delegation boundary for Agora, compared with MCP Tasks, and recommended a local fake A2A specialist/Agora adapter; report saved as `2026-09-28 — A2A v1 for Agora Agent Delegation.md`.
- 2026-09-29: Researched systemd resilience for Spark-dependent Hermes inference and voice pipelines, combining restart/backoff/watchdog/resource-control guidance with live user-unit observations; recommended a disposable failure-injection fixture before changing production units; report saved as `2026-09-29 — systemd Resilience for Spark-Dependent Hermes Pipelines.md`.

## Related notes
- [[Research/Research Scout]] — research-hub context and curation mandate.
- [[Research/2026-09-15 — Local LLM Inference for Multi-Agent Systems.md|2026-09-15 — Local LLM Inference for Multi-Agent Systems]]
- [[Research/2026-09-16 — Qwen3-TTS vs Fish Audio S2 for AJ's Voice Pipeline.md|2026-09-16 — Qwen3-TTS vs Fish Audio S2 for AJ's Voice Pipeline]]
- [[Research/2026-09-18 — Agora Conversation Lifecycle and Regeneration Architecture.md|2026-09-18 — Agora Conversation Lifecycle and Regeneration Architecture]]
- [[Research/2026-09-19 — ROS 2 Architecture for Small Robots and Home-Lab Electronics.md|2026-09-19 — ROS 2 Architecture for Small Robots and Home-Lab Electronics]]
- [[Research/2026-09-20 — Hermes Memory, Sessions, and Context Compression.md|2026-09-20 — Hermes Memory, Sessions, and Context Compression]]
- [[Research/2026-09-21 — MCP Apps and Agora Embedded Agent Interfaces.md|2026-09-21 — MCP Apps and Agora Embedded Agent Interfaces]]
- [[Research/2026-09-22 — Voice Agent Turn-Taking, Barge-In, and Local Pipeline Design.md|2026-09-22 — Voice Agent Turn-Taking, Barge-In, and Local Pipeline Design]]
- [[Research/2026-09-23 — OpenTelemetry GenAI Tracing for Hermes, Agora, and Local Agents.md|2026-09-23 — OpenTelemetry GenAI Tracing for Hermes, Agora, and Local Agents]]
- [[Research/2026-09-24 — llama.cpp Speculative Decoding and DSpark for Spark.md|2026-09-24 — llama.cpp Speculative Decoding and DSpark for Spark]]
- [[Research/2026-09-25 — MCP Authorization Hardening for Agora Adapter.md|2026-09-25 — MCP Authorization Hardening for Agora Adapter]]
- [[Research/2026-09-26 — Godot 4.5 as an Agent-Facing Interaction Shell.md|2026-09-26 — Godot 4.5 as an Agent-Facing Interaction Shell]]
- [[Research/2026-09-28 — A2A v1 for Agora Agent Delegation.md|2026-09-28 — A2A v1 for Agora Agent Delegation]]
- [[Research/2026-09-29 — systemd Resilience for Spark-Dependent Hermes Pipelines.md|2026-09-29 — systemd Resilience for Spark-Dependent Hermes Pipelines]]
- [[Research/Backlog to be transcrbed and categorised/Youtube videos to be transcribed and categorised.md|Youtube videos to be transcribed and categorised]]
- [[Research/Git repositories that inspire.md|Git repositories that inspire]]
- [[Research/Research Scout.md|Research Scout]]
- [[Research/Wishlist.md|Wishlist]]

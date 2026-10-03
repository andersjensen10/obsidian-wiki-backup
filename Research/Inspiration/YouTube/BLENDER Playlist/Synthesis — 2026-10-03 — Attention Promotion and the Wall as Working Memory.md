---
tags: [project/inspiration-radar, source/youtube, lantern-garden, research-synthesis, prototype]
title: Synthesis — Attention Promotion and the Wall as Working Memory
type: research-synthesis
created: 2026-10-03
owner: Winbot
status: synthesis complete; one read-only prototype run; nothing on the wall, nothing deployed
sources: [YT-BL-005, YT-BL-006, YT-BL-007]
---

# Synthesis (2026-10-03): attention promotion and the wall as working memory

Capability-growth track (a), research synthesis, run by the scheduled Winbot capability job. Three recent BLENDER playlist videos (positions 9, 10 and 13 of 593 on 2026-10-03), read from their **full caption transcripts**, then checked against primary sources.

| ID | Video | Transcript | Primary source checked |
| --- | --- | --- | --- |
| YT-BL-005 | KDE Community, "Scott Jenson: Are we really going to use the same Desktop UX forever?" (V7AfAcQwLW0, 40:56) | 49,921 chars, English | InfoQ podcast interview with Jenson (same three prototypes, "Lifestreams" origin); windowsforum report places the talk at KDE Akademy 2026 |
| YT-BL-006 | Spudnik, "The Weird Tech Behind Rockstar's NPCs" (w3i72_5_Dho, 13:25) | 17,517 chars, English | Not checked; patent and developer quotes stay creator claims |
| YT-BL-007 | Stefan 3D AI, "Free and Local Real-Time AI Animation - NVIDIA MotionBricks.cpp" (lj-xPo7ueGA, 7:19) | 9,248 chars, English | github.com/localai-org/motion-bricks.cpp (C++23/GGML, CPU + Vulkan, Apache-2.0 code, NVIDIA Open Model License weights); NVlabs GR00T-WholeBodyControl `motionbricks/` (SIGGRAPH 2026) |

Transcripts were fetched from the MSI with `youtube-transcript-api`; raw text is in the scratch folder only (auto-pruned), not in the vault.

## 1. Jenson: three kinds of working memory

**Established (talk + interview):** Jenson argues the desktop stopped evolving, and that the useful AI move was *context* (Claude Code reading the file system), not generation. His perspective shift is **working memory**, prototyped three ways:
1. **Spatial:** design for very wide screens. The centre is for work, the sides are periphery; windows dragged to the edge shrink, stay live, and can collapse into a widget (a music player becomes a play button). Organic and messy, not virtual desktops.
2. **Associative:** a per-document drawer holding clips, files and web snippets that survives restart ("a clipboard file, not a clipboard history"); a local small model may organise it afterwards.
3. **Episodic:** a Lifestreams-style day ribbon built from **attention signals only** (dwell, scroll, did-copy, did-paste; never the text), compressed by plain maths, not AI: 50 browsed pages became 7 nodes.
On privacy he concedes such a store is a honeypot; his mitigation is to collect boring, content-free signals.

**Why it matters here:** the projector is the widest screen in the house and is mostly seen from the periphery. The wall today shows status (dashboard, Decision Deck, Attention). Jenson's frame says its stronger job is to be AJ's *working memory* for the agent fleet: what happened while he was away, where it happened, and what is waiting.

## 2. Rockstar: promote on attention

**Creator claims (not independently checked):** Assassin's Creed Unity drew up to 12,000 NPCs but ran full AI on about 40. Watch Dogs Legion *promotes* a passer-by to a full identity the moment the player follows them. Red Dead 2 gives NPCs routines, so "you walk into something that was already happening". Rockstar's population system filters tagged parts by compatibility rules, but GTA 6 people were still art-directed by hand.

**Lessons for Lantern Garden:**
- **Level of detail for agent work.** Everything on the wall should be cheap and ambient by default; only the item AJ looks at or touches gets the expensive treatment (LLM summary, full thread, a Decision Deck card). This is the same split as Jev/Qwen triage in [[Lantern Garden Project/Build and Operations Plan — Decision Layer and Autoresearch]]: cheap judge for all, expensive model for the promoted few.
- **The scene should already be under way.** When AJ turns the projector on, the wall should show where the fleet *is* in its day (the current episode), not a blank page waiting for a click.
- **Generated, then art-directed.** Generative layouts are fine as long as a person (AJ) or a named owner (Herm, dashboard) has the final say on what looks right. This matches Herm's ownership of the dashboard.

## 3. MotionBricks.cpp: real-time motion on a CPU (lead only)

**Established (repo + video):** NVIDIA's MotionBricks (SIGGRAPH 2026) predicts character motion in real time from controls, with no prompt. `motion-bricks.cpp` ports it to GGML for CPU/Vulkan, with a C ABI and a Go/Three.js skeleton demo; weights are under the NVIDIA Open Model License. The presenter reports up to 30 fps and calls the CPU path "more like a research use case". Only G1-humanoid styles are covered; "smart primitives" (pick up, sit) are announced but not released.

**Fit:** a possible future "inhabitant" for the wall or InkGarden (vault folder `Godot`), driven by Lantern Garden signals. Not worth a build now: no use case, and GPU work on the MSI has a recent driver crash on record (Waypoint soak, Townhall `68ecf75d`). Kept as a lead, not pitched.

## 4. Prototype run: a content-free episodic ribbon of Townhall

To test Jenson's claim that plain maths over content-free signals gives a useful story, applied to our own data.

- **Artifact:** `Desktop\Hermes\Autoresearch\prototypes\episodic_ribbon.py` (local commit `1311801`; the Autoresearch repo has no remote, so it is not pushed). Output: `prototypes\ribbon-2026-10-03.json` (not committed).
- **What it does:** one paged read-only `GET 192.168.0.148:5173/api/townhall`, drops `content` from every post as it arrives, splits the last 48 h into episodes at gaps over 45 minutes, and records per episode: duration, post count, new threads versus replies, replies into older threads, agents, categories, top tags, and a landmark post ID (most-replied root).
- **Result (2026-10-03, 0.6 s):** 356 posts total, 93 in the window, **9 episodes**; output check `grep -c '"content"'` = 0.
  - 10-01 09:18, 99 min, 16 posts (winbot 14, herm 2): handoff, schedule, decisions
  - 10-01 11:46, 260 min, 47 posts (herm 27, winbot 19, sparkbot 1): verification, schedule, handoff (the day's main working block)
  - 10-02 04:32, 30 min, 2 posts (sparkbot only): benchmarking, GPU
  - 10-02 12:20, 5 min, 6 posts (all three agents): decision-deck, benchmarking
  - 10-02 15:32, 95 min, 9 posts: godot, mcp, decisions
  - 10-03 00:15, 1 min, 2 posts: world-models, gpu-stability
  - (three more one-to-three-post blips)
- **Reading:** 93 posts compress to a readable two-day story in nine lines, about the ratio Jenson reported (50 to 7). It shows rhythm (one 4-hour block on 10-01 carried half the traffic) and who drove each block, without reading any post text.
- **Limitations:** tags are agent-written words, so they are only *mostly* content-free; the 45-minute gap is a guess and not tuned; one source only (Townhall). Schedule runs, Attention events and Decision Deck answers would make a fuller ribbon. Not visualised and not on the wall.
- **Side effects:** none. Read-only GET on a documented endpoint; no LAN service, device, wall or production code touched. Rollback: delete the `prototypes/` folder (or `git revert 1311801`).

## Invitation for AJ

If the wall's next job is "what happened while I was away", would a thin **episode ribbon** along the bottom edge of the projector (periphery, Jenson-style; content-free; tap an episode to promote it to a full summary, Rockstar-style) be worth a mock-up? If yes, Winbot builds a static mock-up first for AJ to look at, and Herm decides whether it ever goes on the dashboard. Filed as an open question, not a build.

## Log

- 2026-10-03 — Note created by the scheduled capability-growth job. Townhall finding `3ecaac9d-6a57-4326-abcd-b3687e9e0964` (home-lan, read back: agentId winbot, state active, vaultNote set). AJ invitation filed on the Decision Deck: `6ab675ca-51c1-4e00-b2f9-71e7a1b944fb`, dedupeKey `2026-10-03-episode-ribbon-mockup`, read back `pending`, urgency `whenever`.

## Related

- [[Inspiration Radar]] · [[BLENDER Playlist — Home]] · [[BLENDER Playlist — Source Register]]
- [[Synthesis — 2026-10-02 — Local Tool-Call Model and Code-First AV Sequencer]]
- [[Lantern Garden Project/A projector in the living room, a living dashboard and interactive playground]]
- [[Lantern Garden Project/Decision Deck — Concept and Plan]]

---
tags: [touchdesigner, vj, creative-technology]
---

# TouchDesigner VJ Lab

A durable home for AJ and Winbot's live-visual practice: experiments, performance notes, research, reusable patches, and integration decisions.

## Latest win — 2026-09-28

AJ performed a solo living-room concert with live VJing. The current TouchDesigner patch is now driven by **MOTU Pro Audio via ASIO**, using the physical 9/10 input pair for Ableton Push. The live chain was verified with stereo signal at 48 kHz and the existing low/mid/high control drives were nonzero; the patch ran at 60 FPS with no warnings. Saved project: `C:/Users/ander/Desktop/TouchD2025/psychedelic_demo/FirstdemowithHermes1.7.toe`.

## Active threads

1. **Visual vocabulary** — build a small, performance-safe library of looks, compositing idioms, motion systems, and audio mappings.
2. **Web control surface** — evaluate a browser-based controller for live parameters, presets, XY pads, color, and prompt input.
3. **Axiom Engine data** — identify a clean, low-latency route from Axiom Engine events/state into TD; do not assume an existing public streaming API.
4. **Spark + ComfyUI experiments** — test prompt- and camera/input-conditioned image-editing workflows for generative visual hallucinations, prioritizing latency and recoverability over maximum image fidelity.
5. **Live camera** — enumerate and validate Windows capture hardware and privacy settings before building the TD camera branch.

## Working conventions

- Preserve live performance stability: inspect, make small changes, then verify errors, performance, and the visible output.
- Keep live controls explicit and reversible; retain prior sources/nodes when switching inputs.
- Treat a web UI or LAN endpoint as a security boundary: local/LAN binding and authentication are design requirements, not afterthoughts.
- Keep experiment reports in [[TouchDesigner VJ Lab/Research]].

## Related

- [[Agentic Chatroom Project/Hermes TouchDesigner Integration]]
- [[Axiom Engine Project/Axiom Engine]]
- [[LAN notes]]
- [[TouchDesigner VJ Lab/Research/2026-09-28 — Web Controls, Axiom Data, and Spark ComfyUI]]
- [[TouchDesigner VJ Lab/Research/2026-09-28 — AI Search World-Model Watchlist]]

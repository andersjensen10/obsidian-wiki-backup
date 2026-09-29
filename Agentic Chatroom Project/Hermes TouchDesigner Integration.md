# Hermes ↔ TouchDesigner Integration

**Status:** Connected and usable for read-only inspection; creative network work remains an explicit next step.

## What we have established

- Hermes has the official Nous Research TouchDesigner plugin enabled as `td`.
- The plugin registers the bundled twozero MCP server for new sessions at `http://127.0.0.1:40404/mcp`; no duplicate manual `mcp_servers` entry is required.
- `twozero.tox` was downloaded and installed in the running TouchDesigner project through the manual drag/install flow.
- twozero MCP has responded successfully on the local endpoint, and the Hermes session revived the connection after an initial parked/disconnected state.
- A read-only TouchDesigner health-check workflow was exercised before any project mutation.

## Working rules

- Discover the live instance before editing: list instances, inspect focus/selection and network, query operator parameter schemas, then read errors and performance.
- Never guess parameter names; call `td_get_par_info` for the relevant operator type first.
- Prefer native twozero tools for inspection, creation, parameter changes, screenshots, and error checks. Treat `td_execute_python` as scoped arbitrary code in the user's TouchDesigner process.
- Keep desktop input automation, project quit, screen capture, and transcript-export/admin tools opt-in.
- Keep live operator references portable and avoid absolute paths in callbacks or saved parameters.

## Current creative direction

The integration is intended to support real-time visuals for Lantern Garden/projector work, including generative and audio-reactive networks. The validated audio-reactive direction is:

`AudioFileIn CHOP → AudioSpectrum CHOP → Math CHOP → CHOP to TOP → GLSL TOP → Null TOP`

For spectrum stability, keep AudioSpectrum Time Slice on, set output length explicitly to 256, use a red-channel rows-cropped CHOP-to-TOP texture, and perform smoothing in GLSL rather than with Lag or Filter CHOPs.

## Next step

Use the live TD instance to inspect the current network and build a small, verified visual stage only after AJ explicitly chooses the target composition. Every build should finish with recursive error inspection, performance inspection, and a screenshot of the visible output.

## Related notes

- [[Agentic Chatroom Project/Townhall Onboarding]]
- [[Lantern Garden Project/A projector in the living room, a living dashboard and interactive playground]]
- [[Lantern Garden Project/Lantern Garden Readiness — NUC and Projector 2026-09-16]]

## Host note — 2026-09-29
The projector is driven by the MSI laptop (RTX 4080), which makes it the natural TouchDesigner host for wall visuals. TouchDesigner/twozero is still not verified live on this machine; nothing has been built or screenshot-verified yet.

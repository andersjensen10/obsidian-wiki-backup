# A Projector in the Kitchen: Living Dashboard & Interactive Playground

*Foundation document for new infrastructure development. Last updated 2026-09-10.*

## Vision

A projector goes up in the kitchen — the most-trafficked room in the house — and becomes a shared surface for the LAN of agents, servers, and projects already running at home. Two modes: an **ambient dashboard** that makes the state of the system legible at a glance, and an **interactive playground** that makes the space fun to touch and talk to. Both should be built as new surfaces on top of infrastructure that already exists (home-ops console, Agora, Hermes Agent) rather than as a parallel stack.

Importantly, this isn't a single-project dashboard. Multiple projects run in parallel on the home LAN — Agora and the Axiom Engine are the two named so far, with more likely to join — and each has its own agents, potentially running on different workstations across the LAN rather than all on `openclaw-sandbox`. The dashboard needs to present insights *per project*, sourced from whichever agents and machines are actually doing that project's work, not assume one server is the single source of truth.

## Hardware & Physical Setup

**Projector: Acer H6531BDi** — DLP, native 1920×1080, 5200 ANSI lumens, 10000:1 contrast, throw ratio 1.5–1.66:1, manual zoom (1.1×) plus 2× digital zoom, ±40° vertical and horizontal keystone correction, 2× HDMI, 3.5mm audio in/out, USB-A (power only), RS-232, built-in 3W speaker, 2.9kg. ([proshop.dk](https://www.proshop.dk/Projektor/Acer-Projektor-H6531BDi-DLP-projector-portable-3D-1920-x-1080-5200-ANSI-lumens/3462486))

What that implies for the setup:

- **No smart OS, no Wi-Fi/Miracast, no app layer.** It's a dumb HDMI sink. Something else on the network has to *be* the source — this is the first architecture decision (see below) and it's a good one to make early, since everything else hangs off it.
- **Brightness is a strength.** 5200 lumens is bright enough to hold up against kitchen daylight and ceiling lights without blackout curtains — one of the harder problems with kitchen projection setups is solved by the hardware choice already.
- **Throw distance needs planning.** At a 1.5–1.66:1 throw ratio, rough image-size-to-distance numbers (16:9):

  | Diagonal | Approx. width | Throw distance |
  |---|---|---|
  | 60" | ~52" | ~2.0–2.2 m |
  | 80" | ~70" | ~2.7–2.9 m |
  | 100" | ~87" | ~3.3–3.7 m |

  Most kitchens don't have 3+ metres of clear throw, so unless this lands in an open kitchen-diner, 60–80" is probably the realistic target. Worth measuring the actual candidate wall and mounting point before committing to a screen size or a fixed mount — the ±40° keystone and digital zoom give some flexibility to correct for an awkward mounting position, but starting close to square-on avoids using it.
- **Projection surface.** Painted wall, a pull-down/fixed screen, or a flat cabinet run are all viable; a screen or a matte-white painted panel will noticeably sharpen text-heavy dashboard content over a normal painted wall. Worth deciding whether the same surface serves both the dashboard and the projection-mapping playground mode, since mapping wants a more three-dimensional or textured target than a flat dashboard does.
- **Audio.** The built-in 3W speaker is fine for notification chimes but not for anything conversational — a virtual townhall or voice-driven playground mode will want an external speaker (and, if input is ever needed, a mic) on the compute node rather than the projector.
- **Wacom input.** The tablet needs a wired or wireless link to whatever machine is driving the doodling app — plan that as a peripheral off the compute node, not the projector.
- **Lamp life and duty cycle.** 5,000h in normal mode, 10,000h in eco, 12,000h in extreme eco. Run this 24/7 in normal mode and the lamp is done in ~7 months; run it only when the kitchen is occupied (a few hours a day) and it lasts years. This is a strong argument for driving the projector's power through the smart-plug control already built into the home-ops console, on a schedule or on presence/occupancy, rather than leaving it on continuously.

## System Architecture: the "kitchen display node"

Since the projector has no compute of its own, the natural fit is to treat it as one more client of the infrastructure that already exists on `openclaw-sandbox`, the same way the nightly HTML emails and smart-plug control are today — not a new stack.

- **A dedicated compute node — decided: an older Intel NUC.** It's getting a fresh power supply and arrives in the same shipment as the projector, a couple of days out, so Phase 0 can start almost immediately. Being physically at the projector rather than a long HDMI run back to `openclaw-sandbox`, it sidesteps the distance question entirely.
- **Open design question this raises: how much does the NUC do beyond driving HDMI?** Two options worth weighing before wiring anything up: (a) it's a thin client — just a kiosk browser pointed at a URL served by the existing home-ops console on `openclaw-sandbox`, keeping all logic centralized; or (b) it hosts its own instance of the server locally, which would let the kitchen display keep running (with cached/local data) even if `openclaw-sandbox` is down or the network hiccups, at the cost of a second deployment to keep in sync.
- **A second open question: should the NUC also run an additional Hermes Agent instance?** If so, the NUC stops being purely a display node and becomes a genuine workstation in the LAN fleet — which fits neatly with the multi-workstation reporting model above: the NUC's own Hermes agent would report into the same aggregator as every other project's agents, and could plausibly also drive the scene-manager / scene-switching logic directly from the kitchen machine itself rather than needing a remote control channel.
- **A kiosk-mode browser** on the NUC displays whichever content model gets picked above — reusing the existing Node.js/Svelte stack either way rather than introducing a new frontend framework.
- **A scene manager** cycles or switches between modes: dashboard panels, the doodling app, projection mapping, the virtual townhall. This is new surface area — worth designing as a thin routing/state layer (e.g. SvelteKit routes plus a small WebSocket or REST control channel) so scenes can be switched remotely by Hermes Agent, a phone, or a physical control, rather than only by whoever is standing at the kitchen machine.
- **A shared data layer — now a LAN-wide aggregation problem, not a single-server one.** With multiple projects (Agora, Axiom Engine, others to come) each running agents on potentially different workstations, the dashboard can't just query `openclaw-sandbox` for everything. Two shapes to weigh: agents on each workstation *push* status/insight updates to a central aggregator (likely still hosted on `openclaw-sandbox`, since that's already the home-ops console's home), or the aggregator *pulls* from each workstation/agent on a schedule. Push scales better as workstations come and go, and keeps the kitchen node's own logic simple — it only ever talks to one aggregator, never to N workstations directly. Either way this argues for a **lightweight, common reporting schema** (project id, agent id, workstation id, metric/event type, timestamp, payload) that any agent on any machine can speak, rather than one bespoke integration per project per panel.
- **A project registry.** Something needs to know what projects exist, which agents/workstations belong to each, and how they're presented (name, icon/color, which panels apply). Doesn't need to be fancy — a config file or small table the aggregator reads — but worth having as a single place to add "project #3" later instead of touching every panel.
- **Reliability basics.** Kiosk browser auto-restart on crash, a watchdog on the compute node, and the projector's own power tied to the smart-plug schedule mentioned above. Worth extending this to the aggregator too — a workstation going offline should show as "stale/unknown" on its project's panel, not silently freeze on last-known data.

## Content: Dashboards and Insights

This is entirely homebrew — Agora, the Axiom Engine, Hermes Agent, `openclaw-sandbox`, the DGX Spark, and whatever else is running on the home LAN. Nothing here touches Hiper.

Most of these panels are **per-project** — they need a project switcher or an overview grid, since Agora and the Axiom Engine (and future projects) will each have their own instance of most of the following:

- **Sprint Insights** — per project. For Agora this is the Scrummaster/PM agent roles' sprint tracking, already recorded in the Obsidian vault's Feature Development folder. The Axiom Engine's equivalent source isn't defined yet — worth checking whether it has anything analogous or needs one built.
- **Board Meeting Insights** — currently Agora-specific: its Board governance role (still not built as of writing) would be the source once it exists. Until then this panel has no data and is effectively blocked on that role getting built. Unclear yet whether the Axiom Engine or future projects have an equivalent "board" concept at all — may end up being an Agora-only panel rather than a per-project one.
- **Token expenditure** — a unified metrics view, but broken out per project as well as an overall total, across whichever agents/workstations are doing each project's work, plus DGX Spark inference and Claude sessions generally.
- **Benchmarks** — worth clarifying scope: model/inference benchmarks on the DGX Spark, per-project benchmarks (e.g. Axiom Engine's own eval suite, if it has one), or both.
- **Project milestones and roadmaps** — per project; Agora can reuse the Scrummaster/PM agents' existing roadmap data, and the Axiom Engine needs its own source identified.
- **Server health and metrics** — not project-scoped, this one's about the machines themselves: `openclaw-sandbox`, the DGX Spark, and whichever other workstations end up hosting project agents. Likely the easiest panel to stand up first, since the underlying data already exists for at least `openclaw-sandbox`.
- **System and online status of all machines, services, and agents on the LAN** — also machine-scoped rather than project-scoped: the fleet view. This one and server health are natural first panels, and also a good forcing function for building the project registry / workstation inventory early, since both panels need to know what's out there.

## Content: Interactive Playground

- **Projection mapping** — needs a calibration workflow (manual or camera-assisted) and a mapping tool or custom WebGL/canvas approach. The throw distance and surface choice above directly bound how ambitious the mapped geometry can be, so this is probably a later phase once the physical setup is settled.
- **Generative agentic doodling app (Wacom input)** — architecturally: Wacom strokes → local input handler on the compute node → an image-generation agent, either cloud (OpenAI/Google, both already familiar) or local on the DGX Spark for lower latency. Worth an early decision on the interaction model — real-time collaborative generation vs. turn-based "agent responds after a stroke or a pause" — since that changes the latency budget and therefore whether local or cloud generation makes more sense.
- **Virtual townhall for agents** — the most novel piece, and the one that most directly extends Agora rather than needing new infrastructure: surfacing the multi-persona chatroom (and eventually the not-yet-built Board governance role) as a visual "room" on the big screen, with active/planned agents represented as participants. Worth scoping an initial version as text/log-driven before reaching for voice or avatars.

## Cross-Cutting Concerns

- **Visibility to guests.** Since everything on the dashboard is homebrew/personal rather than work data, this is a much lower-stakes concern than it would be for a work screen — mostly a question of whether anything looks unfinished or noisy with people around, not a confidentiality issue. A simple "quiet mode" the scene manager can apply (fewer panels, bigger type) probably covers it without needing a real access-control policy.
- **Scene-switching UX** — touch, a phone remote, voice, or a schedule (dashboard by day, playground in the evening). Not blocking for an MVP but worth having an opinion on before building four independent scenes that all expect to be launched differently.
- **Duty cycle** — tie projector power to the smart-plug scheduling that already exists in the home-ops console, both for lamp life and so it isn't running unattended.

## Phased Roadmap

1. **Phase 0 — Physical setup.** Projector and NUC (with its new PSU) both arrive in the same shipment in a couple of days. Mount the projector, pick and prep the projection surface, settle on throw distance/image size, get the NUC driving a test pattern over HDMI.
2. **Phase 1 — MVP dashboard.** Stand up the compute node and kiosk browser; ship the one or two panels with data that already exists — server health and LAN/fleet status are the obvious first candidates.
3. **Phase 2 — Full dashboard suite, starting with the project registry and reporting schema.** Stand up the project registry and the common agent → aggregator reporting format first, then add sprint insights, token expenditure, milestones/roadmaps, and benchmarks per project (Agora first, since it already has the most structured data; Axiom Engine once its data sources are identified). Board meeting insights comes later, gated on the Agora Board role actually existing rather than on any privacy concern.
4. **Phase 3 — Doodling app.** Wire up the Wacom tablet and a first version of the generative doodling loop — likely the most self-contained "fun" build, good for validating the scene-manager and input-handling pattern before the harder playground modes.
5. **Phase 4 — Virtual townhall.** Surface Agora onto the big screen.
6. **Phase 5 — Projection mapping.** Most novel and most dependent on the physical setup being locked in; sequenced last on purpose.

## Open Questions

- Final projection surface and mounting point — needs an actual measurement of the candidate wall against the throw-distance table above.
- NUC role: thin client pointed at `openclaw-sandbox`, or local server host for resilience against network/server downtime?
- Whether the NUC also runs its own Hermes Agent instance, making it a fleet workstation rather than just a display.
- Timeline for the Agora Board governance role, since Board Meeting Insights has no data to show until it exists.
- Scene-switching mechanism — and who/what is allowed to switch scenes (household only, or can Hermes Agent trigger a scene change autonomously)?
- Audio strategy once the townhall or any voice-driven mode is in scope — the projector's own speaker won't be enough.
- Reporting schema and transport for agent → aggregator updates: push vs. pull, what fields are mandatory, how a workstation registers itself.
- What the Axiom Engine actually is and what data it can currently expose — needed before any of its panels can be built out.
- Full list of projects to include beyond Agora and the Axiom Engine, and whether every project gets every panel or panels are opt-in per project.

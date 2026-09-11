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
- **Townhall — a cross-agent bulletin board, NOT an Agora surface.** (Redefined 2026-09-11 — earlier drafts of this doc assumed Townhall = "surface Agora's persona chatroom on the big screen"; that's wrong.) Townhall is where **all of AJ's agents** — Herm, Agora's personas, the Axiom Engine's agents, any future project's agents — post knowledge, findings, and resources meant to help AJ, visible at a glance on the kitchen wall. Think shared bulletin board / knowledge feed, not a chatroom transcript. Agora may well be *discussed* there (e.g. an Agora persona posting something relevant), but Townhall itself is project-agnostic and multi-agent by design, same spirit as the project registry — it should NOT be Agora-only surface area. Needs its own lightweight schema (agent id, project id, timestamp, content, maybe a category/tag) distinct from Agora's chat data model. Scoping and data source still open — likely reuses the same push/aggregator pattern already designed for the dashboard's reporting schema (see System Architecture above) rather than inventing a new transport.

## Cross-Cutting Concerns

- **Visibility to guests.** Since everything on the dashboard is homebrew/personal rather than work data, this is a much lower-stakes concern than it would be for a work screen — mostly a question of whether anything looks unfinished or noisy with people around, not a confidentiality issue. A simple "quiet mode" the scene manager can apply (fewer panels, bigger type) probably covers it without needing a real access-control policy.
- **Scene-switching UX** — touch, a phone remote, voice, or a schedule (dashboard by day, playground in the evening). Not blocking for an MVP but worth having an opinion on before building four independent scenes that all expect to be launched differently.
- **Duty cycle** — tie projector power to the smart-plug scheduling that already exists in the home-ops console, both for lamp life and so it isn't running unattended.

## Phased Roadmap

1. **Phase 0 — Physical setup.** Projector and NUC (with its new PSU) both arrive in the same shipment in a couple of days. Mount the projector, pick and prep the projection surface, settle on throw distance/image size, get the NUC driving a test pattern over HDMI.
2. **Phase 1 — MVP dashboard.** Stand up the compute node and kiosk browser; ship the one or two panels with data that already exists — server health and LAN/fleet status are the obvious first candidates.
3. **Phase 2 — Full dashboard suite, starting with the project registry and reporting schema.** Stand up the project registry and the common agent → aggregator reporting format first, then add sprint insights, token expenditure, milestones/roadmaps, and benchmarks per project (Agora first, since it already has the most structured data; Axiom Engine once its data sources are identified). Board meeting insights comes later, gated on the Agora Board role actually existing rather than on any privacy concern.
3.5. **Phase 3 — Doodling app.** Wire up the Wacom tablet and a first version of the generative doodling loop — likely the most self-contained "fun" build, good for validating the scene-manager and input-handling pattern before the harder playground modes.
4. **Phase 4 — Townhall.** Cross-agent bulletin board: all agents (Herm, Agora personas, Axiom Engine agents, future projects) post knowledge/findings/resources for AJ, visible on the big screen.
5. **Phase 5 — Projection mapping.** Most novel and most dependent on the physical setup being locked in; sequenced last on purpose.

## Update — 2026-09-11: Mounting solved

Mounting point decided: IKEA shelving unit. It'll double as the equipment shelf, hosting the broadband router, the Axiom Engine server, and — depending what state it arrives in — the Intel NUC too. So the shelving is both the projector mount and the de facto "kitchen rack" for the compute node(s) driving it, which simplifies the HDMI/power run considerably (short cable runs, everything co-located). Still want to sanity-check throw distance from the shelf position against the table above once it's placed.

Projector package confirmed for delivery **16 September**.

## Update — 2026-09-11: Dashboard dev started early

Started the actual dashboard codebase ahead of hardware arrival — no reason to wait on the NUC to begin. Repo: `~/Desktop/Hermes/kitchen-dashboard` (SvelteKit, git-initialized, local only for now — same pattern as Agora/local-git-only). Dev server runs on this laptop at `0.0.0.0:5173`, will move to the NUC once it's confirmed working.

Built so far:
- **Fleet health panel** — live-probes known LAN services (ComfyUI, llama.cpp, Fish TTS, voiceprep-api on Spark; Axiom Engine node app; Fish TTS dashboard on this laptop), shows up/down + latency, auto-refreshes every 15s. Each card links out to that service's own web UI where one exists.
- **Project registry** (`src/lib/server/projects.ts`) — the Phase 2 foundation the roadmap called for: project id/name/color, referenced by fleet checks instead of loose strings. Ready for future per-project panels to hang off it.
- **Machine/project rollup strip** — up/total chip per project at the top of the dashboard.
- **Smart-plug panel** — real control, not just display. Talks the raw Kasa protocol directly (same approach as the existing `~/.local/bin/kasa_plug.py`), currently only the living-room HS100 is wired in. Tap-to-toggle verified working against the real device. The **projector's own plug isn't registered yet** — add it once the projector's shelf setup is done and its plug is known.
- **Kiosk mode** — fullscreen toggle, bigger type, hides the toggle button itself when active (tap to reveal). Matches AJ's fullscreen test on 2026-09-11 ("looks good, works great with full screen").
- **Token expenditure panel** — deliberately left as an honest "not configured" placeholder. No local usage/cost data source was found (checked `~/.hermes`); needs AJ's steer on which API/ledger to read from before building it for real.

Not yet done: per-machine CPU/RAM (beyond single-service liveness), sprint insights, board meeting insights, benchmarks, project milestones — all still gated on their underlying data sources per the original roadmap below.

## Design convention: fixed 1920x1080, no scroll

Set 2026-09-11 as a standing rule for "The Kitchen Wall" project (dashboard + playground alike): every scene should fit a **fullscreen 1920x1080 browser window with no page scrolling** — the projector is a fixed-size wall surface, not a normal scrolling webpage. Exceptions are allowed per-panel (e.g. a panel with unbounded content gets its own internal `overflow-y: auto` instead of growing the page), but the default assumption for any new panel/scene is "must fit the fixed viewport."

Implementation pattern used on the dashboard (reusable for future scenes): `html`/`body` set `overflow: hidden`, `main` is `height: 100vh` flex column, the two-column content area (`flex: 1; min-height: 0`) is what actually absorbs the remaining space, and any individually-scrollable panel gets `overflow-y: auto` with a comment explaining why it's the sanctioned exception. Verified with real viewport measurement (CDP `Emulation.setDeviceMetricsOverride` to 1920x1080 + `getBoundingClientRect` checks), not just eyeballing — `document.documentElement.scrollHeight` must equal `clientHeight` and no element's bounding box should exceed the viewport.

## Update — 2026-09-11: App shell, scenes, and design system

Restructured the codebase around a persistent **nav rail** (84px, icon-only, left side, Lucide icons) + a `.scene` content area — every route (`/`, `/doodle`, `/townhall`, `/settings`, `/design-guide`) renders inside that shell and independently satisfies the fixed-1920x1080-no-scroll rule. `/doodle`, `/townhall`, `/settings` are intentional placeholders (icon + description + roadmap phase) until their real builds start.

**Design tokens** now live in one file (`src/lib/styles/tokens.css`) as CSS custom properties — color (status semantics, project accents, surfaces, text, accent), type scale, spacing scale, radius. The dashboard page and project registry (`projects.ts`) were refactored to consume these vars instead of hardcoded hex, so a palette change is now a one-file edit.

**`/design-guide` route** is a live, running reference (not a static mockup) — swatches pull real `var(--token)` values, includes a component gallery (status cards, project chips, buttons), the type scale, and the layout rules written out. Also hosts a **3-way icon pack comparison** (Lucide vs Phosphor vs Tabler, all installed as real deps) rendering the same 7 concepts (dashboard, users, settings, plug, server, activity, palette) side by side so AJ can pick a direction — Lucide is the current default in the nav, not yet a final decision.

Verified for real: all 5 routes return 200, zero JS/console errors across all of them, and all 5 independently confirmed to exactly fill 1920x1080 with no scroll via headless Chrome + CDP (not just claimed).

Not yet decided: which icon pack to commit to; still Lucide as placeholder.

## Correction — 2026-09-11: Townhall redefined

Earlier drafts (including the roadmap's Phase 4 description) assumed Townhall = surfacing Agora's persona chatroom on the big screen. **That's wrong.** Townhall is a **cross-agent bulletin board**: Herm, Agora's personas, the Axiom Engine's agents, and any future project's agents post knowledge, findings, and resources meant to help AJ — visible at a glance on the kitchen wall. It's project-agnostic by design, same spirit as the project registry, NOT an Agora-only surface. Agora may get discussed there, but Townhall itself doesn't belong to any one project. Data source/schema not yet built — likely reuses the same push/aggregator pattern already planned for the dashboard's reporting schema rather than inventing something new. Updated the roadmap section and the placeholder scene copy in the codebase to match.

## Doodle: expanded scope and phased plan (2026-09-11)

AJ sees real potential here beyond a toy — the projector + Wacom tablet combo as a genuine creative/iteration lever for current and future projects, not just a "fun" side scene. Agreed phased plan (each phase ships and gets used before the next starts):

1. **Phase 0 — DONE (2026-09-11).** Doodle on the wall: a real fullscreen browser canvas at `/doodle`, drawing with mouse/touch/Wacom pen (pointer-events based, native pressure sensitivity via `PointerEvent.pressure` when `pointerType === 'pen'`). Small fixed palette (7 colors), brush size slider, eraser, undo, clear. Verified for real via CDP-driven synthetic pointer/mouse input + canvas pixel-data inspection (not just "the code runs") — draw/undo/redraw/clear all confirmed round-tripping correctly, zero JS console errors, fits the fixed 1920x1080 no-scroll rule.
2. **Phase 1 — next.** Save/load canvas images (to disk, presumably PNG export + a simple gallery/picker to reload), and define how saved canvases get **tiled, stretched, or otherwise displayed** on the wall (i.e. a canvas isn't just ephemeral scratch space — it becomes content the dashboard/other scenes can show).
3. **Phase 2 — generative feedback loop.** Send the canvas to custom ComfyUI templates on the Spark for an iterative generative loop between AJ's strokes and AI-generated imagery (img2img-style, presumably) — turn-based at first (stroke/pause → agent responds), matching the interaction-model question already flagged in the original playground section above.
4. **Phase 3 — speed optimization.** Push the loop from turn-based toward real-time once Phase 2's basic version works, revisiting local (Spark) vs. cloud generation tradeoffs based on measured latency.

Implementation note for whoever picks this up next: the canvas element and stroke history (`strokes: Stroke[]` in `+page.svelte`) are currently in-memory only — Phase 1's save/load will need to either serialize `strokes` (vector, resolution-independent, better for tiling logic) or rasterize to PNG (simpler, matches what ComfyUI Phase 2 will want as input anyway). Worth deciding which representation is canonical before building save/load, since it affects both.

## Doodle Phase 1 — DONE (2026-09-11)

Chose **rasterized PNG** as the canonical saved format (not vector strokes) — reasoning: it's what Phase 2's ComfyUI img2img loop will want as input anyway, and display-mode rendering (tile/stretch/contain/cover) is a solved problem for raster images (same semantics as CSS `background-size`), whereas doing it for vector strokes means re-deriving tiling math from scratch.

Storage: `data/canvases/<id>.png` + `data/canvases/index.json` (metadata: id, name, createdAt, width, height, **displayMode**). Directory is gitignored (user content, not code) but kept in the repo via `.gitkeep`.

Built: `src/lib/server/canvases.ts` (list/save/get/update/delete), REST at `/api/canvases` (GET list, POST save) and `/api/canvases/[id]` (GET raw PNG, PATCH metadata, DELETE). UI: Save button opens a modal (name + display-mode picker with 4 options: contain/cover/stretch/tile, each explained inline), gallery button opens a grid of saved thumbnails with click-to-load and per-item delete.

Verified for real via CDP-driven UI clicks (not just calling the API directly) — save button → modal → confirm → real 40KB+ PNG landed on disk with valid PNG magic bytes, gallery correctly listed it, clicking loaded it back and canvas pixel data confirmed the image was actually redrawn (not just a toast claiming success), delete removed both the index entry and the on-disk PNG file. Zero JS console errors, still fits 1920x1080 no-scroll after the addition.

Not yet built: the OTHER HALF of "define how these canvases are tiled/stretched/displayed" — i.e. some scene actually consuming a saved canvas + its displayMode to render it as wall content (the editor itself always just fits the image to the canvas viewport on load; display-mode is captured as metadata but nothing reads it yet to do tiling/cropping math). That's the natural next slice before or alongside Phase 2's ComfyUI loop.

## Doodle Phase 1b — DONE (2026-09-11): displayMode consumer

Closed the gap flagged above same day. New route `/doodle/present/[id]` fetches a saved canvas's metadata, then renders it fullscreen using plain CSS `background-*` properties mapped from its `displayMode` — `cover`→`background-size: cover`, `stretch`→`100% 100%`, `tile`→`background-repeat: repeat` at native size, `contain`→`background-size: contain` (letterboxed). Chose CSS background properties over a canvas/WebGL re-render: cheap, GPU-accelerated by the browser for free, and exactly matches the mental model already promised in the save dialog. A small monitor-icon "Present" link was added per gallery item (opens in a new tab) so this isn't a hidden/undiscoverable feature.

## Doodle Phase 2 — DONE (2026-09-11): Generative Feedback Loop with Spark ComfyUI

Closed Phase 2's generative loop between AJ's Wacom strokes and AI-generated imagery:
- **Backend:** `src/lib/server/comfy.ts` and `POST /api/doodle/remix`. Accepts the doodle canvas PNG (scaled down to 1024x576 16:9 with dark background padding), uploads to ComfyUI on the Spark (`192.168.0.139:8188/upload/image`), builds and executes a Flux img2img graph (`flux1-dev-fp8.safetensors`, CheckpointLoaderSimple, VAEEncode, KSampler with cfg=1.0 and user-controlled denoise/steps, VAEDecode, SaveImage), polls history, downloads the output PNG, and auto-saves it into the canvas gallery.
- **Frontend:** floating "Spark AI Remix" pill button in the top-right corner of the canvas (and keyboard/express-key shortcut `Ctrl+Alt+Shift+R` / `Ctrl+Alt+R`) opens a remix dialog. Features:
  - Text prompt input with quick style preset chips (Fantasy Art, Dark Riso, Cyberpunk, Ghibli Anime, Oil Painting).
  - Denoise slider (20% to 95%, default 65%) with plain descriptions of AI freedom.
  - Generative status readout during processing.
  - Automatically loads the resulting image as the canvas `baseImage`, resetting the stroke layer so the user can immediately continue drawing over the AI art with their Wacom pen.
  - Re-drawing preserves `baseImage` across resize and stroke undo.
- **Verification:**
  - Full end-to-end run verified against the live Spark GPU: test doodle submitted, executed through Flux in ~34s, and returned valid 1024x576 PNG (273KB) saved into the gallery.
  - CDP automated test verified 1920x1080 no-scroll bounds, trigger button click, preset chip injection, and `Ctrl+Alt+Shift+R` keyboard shortcut trigger.
  - `npm run check` clean (0 errors).

Verified for real: saved a canvas with `displayMode: cover` through the actual UI, confirmed the resulting presentation page generated the correct `background-size: cover` CSS (not e.g. defaulting to contain); then independently POSTed 3 more test canvases via the API with `tile`/`stretch`/`contain` and confirmed each produced its own correct, distinct CSS output. Test data cleaned up afterward — disk is back to empty.

## Wacom Intuos Pro M (2018) hooked up — driver + pressure fix (2026-09-11)

AJ connected his Wacom Intuos Pro M (PTH-660, bought 2018) to the Hermes laptop. Kernel/udev detected it immediately and correctly (`ID_INPUT_TABLET=1`, separate Pen/Pad/Finger `evdev` devices) — no USB/driver issue there. Two real bugs found and fixed:

1. **No pressure sensitivity, drawing itself worked.** Root cause: this laptop's desktop session is Wayland (GNOME), and Chrome on native Wayland has a known upstream bug (chromium issue 40282832 class of issues) around stylus/pressure handling for some tablets. **Dead-end explored first:** tried forcing Chrome onto XWayland (`--ozone-platform=x11`) — this actually broke drawing entirely (pen motion tracked but no clicks/strokes registered), because GNOME's rootless XWayland doesn't route through the legacy X11 Wacom driver the normal way; `xsetwacom`/`xinput` failed with "Wayland devices found but this tool is incompatible with Wayland." **Real fix:** installed `xserver-xorg-input-wacom` (`sudo apt install xserver-xorg-input-wacom`) system-wide anyway — even though it doesn't hook into XWayland the way expected, having the driver present appears to be what native-Wayland Chrome needed to correctly report pen pressure via libinput. Required a full logout/login (X11 driver load happens at session start, doesn't hot-load) — a `systemctl --user restart` equivalent doesn't cut it here, this is a session-level driver stack. After relogin, plain native-Wayland Chrome (no ozone flag) correctly draws AND reports real pressure. **Lesson for next similar bug: try the driver-install + relogin path before chasing ozone-platform flags — the X11 route was a red herring for GNOME/Wayland.**
2. **Pressure "blob" bug at stroke start/end.** `pointFromEvent()` was treating any near-zero `e.pressure` reading from the pen as "unknown data" and substituting a mid-pressure fallback (0.5) — but near-zero pressure right at initial pen contact and at lift-off is genuine, correct data from the hardware, not a missing-data signal. This produced a flash of full-diameter ink exactly where the pen touches down/lifts, before the real pressure curve caught up. Fixed in `src/routes/doodle/+page.svelte`: pen input now trusts `e.pressure` as-is (0 included); the 0.5 fallback still applies to mouse/touch only, since those genuinely never report real pressure. Confirmed via `npm run check` (0 errors) and live HMR — AJ to re-verify by feel next time he's drawing.

Both fixes committed. Doodle Phase 0/1/1b are now validated against real Wacom hardware, not just synthetic CDP mouse events.

## Doodle: left-side rail matching the Intuos Pro's physical layout (2026-09-11)

Rebuilt the toolbar from a top-center floating pill into a vertical rail on the left edge, matching the Intuos Pro M's real button layout: 4 buttons, mod wheel (with center button), 4 more buttons.

Mapping (AJ approved the proposed default): top 4 = Undo / Clear / Save / Gallery. Middle = a working brush-size dial (drag around the rim or scroll — SVG arc renders a 270° sweep readout, live px label underneath) with the **center button = Eraser toggle**, same physical position as the tablet's real center button. Bottom group = 3 most-used colors (white/teal/red) + a "more colors" (•••) button that pops the other 4 open above it.

One real bug found and fixed during build/verify: the wheel's outer div calls `setPointerCapture` on drag-start to support rim-dragging, which was swallowing the center button's own click event (pointer capture redirects all subsequent pointer events to the capturing element). Fixed by checking `e.target.closest('.wheel-center')` in the wheel's pointerdown handler and bailing out before starting a drag — verified via CDP that both interactions work independently afterward (eraser toggles correctly, wheel-drag still changes brush size).

Verified for real: rail confirmed positioned left-edge, vertically centered (`centerY` = exact viewport center); more-colors popover shows exactly the remaining 4 swatches; a real synthetic drag gesture from top-of-wheel to right-of-wheel changed brush size 6px→40px; zero console/JS errors; still fits 1920x1080 no-scroll.

**Backlog AJ flagged for later (not built yet):**
- Pressure sensitivity **scaling** — a way to adjust how strongly pen pressure maps to line width (some pens/users want a flatter or steeper curve than the current linear `0.4 + pressure` mapping).
- **Stroke smoothing / motion assistance** — an optional toggle to smooth jittery pen movement into cleaner lines, standard "stroke stabilizer" feature in drawing apps.

## Clarification — 2026-09-11: physical Intuos Pro buttons are NOT wired to the app

After the rail redesign, AJ reported clicking on-screen Red/Green color buttons broke drawing, with the tablet's 4 ring LEDs visibly cycling. Traced this to a misunderstanding, not a bug: AJ was pressing the **physical hardware buttons on the Intuos Pro itself** (its onboard express-keys + touch ring), not the on-screen web buttons. Those physical controls are a separate `/dev/input` device (`Wacom Intuos Pro M Pad`, registers as a **joystick** `js1`, not a keyboard) handled entirely by the OS/driver layer — nothing in the SvelteKit app listens to them, and the LED cycling is the tablet's own onboard firmware indicator. Confirmed once AJ used only the pen tip on the tablet surface (not the hardware buttons): the on-screen rail works great.

**Takeaway for later:** if AJ ever wants the physical express-keys/ring mapped to app actions (e.g. hardware button 1 = Undo), that's a GNOME Settings → Wacom Tablet configuration task (or a udev/libwacom mapping), a different project from the web app itself — flag this as a possible future nice-to-have, not a current bug.

Two real bugs *were* found and fixed in the same debugging pass before this was traced to the physical-button misunderstanding — both legitimate and worth keeping:
1. `.side-rail` was missing `touch-action: none` (present on the canvas but not the new rail container) — could cause a real pen/touch tap to be swallowed by default touch-gesture handling instead of registering as a click. Fixed.
2. Erase mode had no visual indicator (same cursor as draw mode) — added an amber outline + `cursor: cell` on the canvas so accidentally toggling the eraser is immediately obvious rather than looking like "drawing stopped working."

## Physical express-key mapping — app side done, GNOME side AJ's to configure (2026-09-11)

AJ wants the Intuos Pro's 8 physical express-keys + ring center-click actually wired to app actions — flagged as "key for productivity." Two halves to this:

**App side (done):** the doodle page now listens for a fixed set of keyboard shortcuts and triggers the matching action, so once GNOME sends any of these combos, the app responds:

| Shortcut | Action |
|---|---|
| `Ctrl+Alt+Shift+U` | Undo |
| `Ctrl+Alt+Shift+X` | Clear canvas |
| `Ctrl+Alt+Shift+S` | Open save dialog |
| `Ctrl+Alt+Shift+G` | Toggle gallery |
| `Ctrl+Alt+Shift+E` | Toggle eraser |
| `Ctrl+Alt+1` | Color: white/default ink |
| `Ctrl+Alt+2` | Color: teal |
| `Ctrl+Alt+3` | Color: red |

Implementation note: for the top group and eraser, `Ctrl+Alt+Shift+<letter>` is used. For the bottom 3 digit shortcuts, `Shift` was dropped to `Ctrl+Alt+<digit>` because GNOME's "Send Keystroke" capture modal intercepts Shift+1 as "!" (exclamation point) rather than capturing the digit combo. Both `Ctrl+Alt+<digit>` and `Ctrl+Alt+Shift+<digit>` are registered in the app for compatibility. Tested via CDP Input.dispatchKeyEvent.

Only 8 combos chosen, matching the 8 physical express-keys — the ring's **rotation** isn't mapped to anything (GNOME's pad-button panel only binds discrete button presses, not continuous rotation, so the physical ring can't drive brush size the way the on-screen wheel does — flagged as a known limitation, not a bug). The ring's **center click** can still be mapped to one of the 8 combos above (Eraser toggle is the natural pick, mirroring the on-screen wheel's center button).

**GNOME side (AJ's to do, one-time setup):** Settings → search "Wacom" → Graphics Tablets panel → "Map Buttons." With the panel open, physically press each express-key/ring-click on the tablet to identify it in the list, then set its action to "Send Keystroke" and enter the matching combo from the table above. Do this for all 8 keys + the ring's center click (9 total mappable inputs). The ring's rotate gesture has no equivalent slot to fill (see limitation above).

Not yet verified end-to-end with the real hardware mapping in place — AJ to configure via GNOME Settings, then test each physical button in the doodle app.

## Update — 2026-09-11: Icon pack decided (for now)

AJ likes both Lucide and Phosphor — going with **Phosphor** as the active pack. Explicitly flagged as revisitable: AJ wants a themable/skinnable system eventually so swapping icon packs (or offering multiple skins) is a config change, not a rewrite. Keep icon usage centralized (e.g. the nav's icon imports) rather than scattered, so a future theme layer has one place to redirect.

## Open Questions

- Exact throw distance from the IKEA shelf position — confirm against the table above once the shelf is placed.
- Data source for the token expenditure panel — Anthropic/OpenAI usage API, a local ledger, or the Spark's own request logs as a proxy?
- NUC role: thin client pointed at `openclaw-sandbox`, or local server host for resilience against network/server downtime?
- Whether the NUC also runs its own Hermes Agent instance, making it a fleet workstation rather than just a display.
- Timeline for the Agora Board governance role, since Board Meeting Insights has no data to show until it exists.
- Scene-switching mechanism — and who/what is allowed to switch scenes (household only, or can Hermes Agent trigger a scene change autonomously)?
- Audio strategy once the townhall or any voice-driven mode is in scope — the projector's own speaker won't be enough.
- Reporting schema and transport for agent → aggregator updates: push vs. pull, what fields are mandatory, how a workstation registers itself.
- What the Axiom Engine actually is and what data it can currently expose — needed before any of its panels can be built out.
- Full list of projects to include beyond Agora and the Axiom Engine, and whether every project gets every panel or panels are opt-in per project.

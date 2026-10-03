---
tags: [touchdesigner, vj, live-session, typography, llm, audio-reactive]
date: 2026-10-03
---

# 2026-10-03 — BerlinSet live session (typography + look library)

Live jamming session: AJ composing on the Push, synthy Berlin material arriving on the
**MOTU Pro Audio ASIO inputs 9/10** (0-based indices `8 9`). AJ asked for something new and
wild, audio-reactive (no camera or MIDI yet), full screen on the projector, iterating live.

## What is live

- Project: `C:/Users/ander/Desktop/TouchD-2025/BerlinSet.toe` (stages saved as numbered
  `BerlinSet.1.toe`, `.2.toe`, … with older copies moved to `Backup/` by TD).
- Sources mirrored into git: `Desktop/TouchD2025/BerlinSet/` (shaders, poll DAT, generator,
  looks.json, STAGE-NOTES.md). Remote `andersjensen10/TouchDesigner`.
- Output: `windowCOMP` "display", exclusive fullscreen, borders off, on the **second**
  monitor (TD `display=1`; enumerate with `monitors[i].isPrimary`). 1280x720 render, 60 FPS
  (~0.2% of the 16.7 ms budget).

## Signal chain

```
audiodeviceinCHOP  driver=asio  device=MOTU Pro Audio  inputindices='8 9'  numchan=2  format=stereo
  -> mathCHOP (chanop=avg) mono
     -> audiospectrumCHOP (FFT 1024, 256 bins, timeslice ON) -> mathCHOP gain 10 -> choptoTOP (256x1 spectrum texture)
     -> audiofilterCHOP lowpass 160   -> analyzeCHOP rmspower -> filterCHOP gauss 0.05 s -> mathCHOP -> low
     -> audiofilterCHOP bandpass 1200 -> ...                                                  -> mid
     -> audiofilterCHOP highpass 4000 -> ...                                                  -> high
     -> analyzeCHOP rmspower (fast gauss 0.02 s)                                              -> kick
     -> analyzeCHOP rmspower (slow gauss 0.20 s)                                              -> level
```

## Render chain

```
world (GLSL raymarch: faceted crystal shell around a lit hollow core)  -> trails (composite + feedbackTOP decay)
halo  (GLSL spectrum mandala, input = spectrum texture)
trails + halo -> summed -> bright -> blur -> bloom -> finalcomp
finalcomp + typography -> typomix (GLSL alpha-over) -> post (CA / vignette / scanlines / grain) -> out
```

Uniform contract, identical in every shader: `uBands=(low,mid,high,level)`,
`uCtl=(kick,seconds,Motion,Mono)`, `uRes=(w,h,aspect,Style index)`. Raw drives are
compressed in-shader with `drive(x,k)=1-exp(-x*k)` so the look survives both silence and
a loud drop.

## Typography (new this session)

- `textTOP` (Bahnschrift) -> `transformTOP` -> `levelTOP` -> `typomix` GLSL alpha-over -> post.
- Phrase source: **LLM on the Spark** — llama.cpp OpenAI endpoint `192.168.0.139:8014`,
  model `qwen3.6-35b-a3b-heretic-apex-i-quality`. `typegen.py` asks for a terse
  German/English stage phrase + mode every ~30 s and writes `BerlinSet/type.json` atomically.
- TD never opens a socket: an `executeDAT` (`onFrameStart`, `frame % 30`) reads the file and
  applies a mode layout. LLM or network failure therefore cannot break the show; the
  generator falls back to a canned phrase bank.
- Modes rotate on the generator side (headline / line / stamp / stack) so the set keeps
  varying instead of collapsing into one treatment. Layout per mode: headline 112 px lower
  third, line 52 px bottom-left, stamp 150 px centred, stack 84 px centred 3 lines.
- Reveal: 16-frame eased fade + 26 px slide, with a kick-driven opacity/scale pulse.

## Look library

Custom `Look` page on `/project1/BerlinViz`: `Motion`, `Mono`, `Trails`, `Sensitivity`,
`Style` (icy / magma / toxic / mono), `Typeenable`, `Typesize`, `Typemode`. Changing `Style`
fires `look_cb` (parameterexecuteDAT) which loads that look's numbers from the `looks` DAT —
i.e. **presets live inside the patch**, and whole-patch stages accumulate as numbered `.toe`
saves. That is the answer to "how do we keep stages": presets for looks, numbered saves for
stages, git for the sources.

## Lessons worth keeping

- **Cross-COMP wiring silently no-ops in this build.** `connect()` returns without raising
  and the connector stays empty. Workaround: reference across COMPs by *parameter*
  (`selectCHOP.par.chop`, `choptoTOP.par.chop`) and use expressions for uniforms. All
  wiring now happens inside a single COMP.
- A `feedbackTOP` needs `par.top` **and** its own input connector fed from the loop, or it
  reports "Not enough sources specified". Feeding it the *world* (outside the loop) clears
  the error and avoids a "cook dependency loop" STOP.
- `compositeTOP` in 2025 exposes one input connector; `overTOP` has two and wires normally.
  For any doubt about alpha, a 10-line GLSL alpha-over is cheaper than fighting blend menus.
- `textTOP`: **position is an offset, not an anchor.** To centre a block use
  `alignx/aligny='center'`, `positionunit='fraction'`, `positionx/positiony=0`.
  `fontautosize='fitiffat'` stops long German compounds running off the frame.
- Set `par.text=''` on a `textTOP` or the literal default ("derivative") overrides the DAT.
- Custom par names must be one leading capital then lowercase (`Typeenable`, not `TypeOn`).
- Fresh `appendMenu` pars ship with generic `name1..name3` entries; assign `menuNames`
  **again in a later call** for the names to stick.
- `td_execute_python` resolves relative `op()` paths against the exec server's context, not
  the target op — pass absolute paths in Python, relative paths only in par expressions.
- An `executeDAT` needs `import json` at the top of its text; without it the file poll threw
  `NameError` inside a `try/except` and silently did nothing for several minutes.
- Restart the generator from the terminal tool with `python typegen.py 30` (its own log lives
  at `BerlinSet/typegen.log`); a trailing `&` in a foreground call dies when the call returns.

## Later the same session — generative typography suite

Pushed the typography from "one word every 30 s" to a generative suite, all live at 60 FPS
(0.1% of the frame budget):

- **Text stream** — `streamgen.py` asks the Spark LLM for one new line every ~9 s and appends
  it to `stream.txt` (tail capped at 60 lines). TD renders the last 34 lines in a mono column
  below the crystal, bottom-anchored, so new lines push the column upward: a living scroll with
  no scroll logic. Sample output: *"der boden vibriert im tiefsten bass"*, *"schweiß ist nur
  verdunstete zeit"*, *"der rauch vergisst seinen eigenen namen"*.
- **ASCII layer** — `ascii.glsl` renders the whole composite as live ASCII art. Glyph atlas is a
  `textTOP` (Consolas 64 px, one row, 10-glyph ramp ` .:-=+*#%@`) at exactly 10 x the 35.2 px
  advance = 352x64. Gotcha that cost real time: the atlas **must** use
  `alignxmode='metrics'`; with `'bbox'` the leading space is dropped and every glyph shifts one
  cell left. `uType = (cellw, cellh, nglyphs, amount)`; `amount` is the `Asciiamount` custom par.
- **Chain order matters** — `finalcomp -> ascii -> typomix(ascii, stream, hero) -> post`, so the
  crystal is ASCII while the typography stays crisp on top. Doing it the other way dissolves the
  hero word into characters.
- **Font rotation** across nine faces (Bahnschrift SemiBold / Agency FB / Arial Black / Franklin
  Gothic Book / Copperplate Gothic Bold / Bahnschrift Condensed / Century Gothic / Impact /
  Bahnschrift Light Condensed) on a `Fontrotate` toggle.

Stages so far: `BerlinSet.1..4.toe`; commits `924c620`, `350d425`, `8b110ae`, `b53e4b7`.

## Ink plate — the InkGarden style, in TouchDesigner

AJ asked for a look inspired by the Godot `InkGarden` build (2026-10-02: ink `#121214` on
paper `#f6f5ef`, soft-brush strokes along noise-displaced paths, hatching and stippling, no
flat fills). Ported as a final GLSL stage: `post -> ink -> out`, dialled by a new
**`Inkamount`** control and a matching **`ink` / "Ink Garden"** entry in the `Style` menu
(the preset also drops ASCII to 0 and slows motion, so one click switches the whole set from
techno to paper).

How the plate is built (`ink.glsl`):

1. **Ink is relative, not absolute.** The first version used raw luminance and flooded the
   page black, because the source render is mostly dark. A pen drawing inks where a pixel is
   darker than *its neighbourhood*: sample a 3x3 average offset by 11 px and drive the hatch
   with `clamp((avg - lum) * 8 + 0.06, 0, 1)`. That single change is what turned a black slab
   into a drawing.
2. **Engraved hatching** — two crossed line fields at +/-45 degrees from a wobbled coordinate,
   appearing in three passes as the relative tone darkens (first pass mid-tones, cross-pass
   shadows, fine third pass deepest).
3. **Stippling** in the deepest shadows: jittered-grid dots rather than a fill.
4. **Pen outlines** from the plate's screen-space gradient (`dFdx/dFdy`) — cheap and reads
   exactly like a pen line.
5. **Hand tremor** — the drawing field is displaced by value noise, amplitude riding the kick,
   so the strokes jitter on the beat.
6. **Paper** with fbm grain and a warm edge falloff, so flat areas stay paper instead of
   filling with texture (the same trap the InkGarden note records for repeating ground tiles).

Happy accident worth keeping: the streaming German text survives the ink pass as faint
hand-written annotation across the paper.

## Register change — engineering voice instead of techno-poetry

AJ's note: the German phrasing had become too pretentious. Both generators were rewritten to the
vocabulary of **programming, mathematics, physics and signal processing**, anchored to what the
machine is actually doing and to the real situation — one human and several agents sharing a
signal path in a Copenhagen apartment on a late-autumn afternoon.

- **Hero terms** now come from the technical register: EIGENMODE, PHASE SPACE, HILBERT TRANSFORM,
  NYQUIST, LATENT SPACE, SIGNED DISTANCE FIELD, BOUNDARY CONDITION, STOCHASTIC RESONANCE,
  KOLMOGOROV COMPLEXITY, RACE CONDITION.
- **The stream is an engineering log of the room**, which is where the reflection on the moment
  lives: *"phase drift accumulates in the feedback buffer"*, *"solar angle drops below forty five
  degrees"*, *"human breath modulates the filter cutoff"*, *"gradient descent finds the local
  minimum"*, *"the snare transient exceeds nyquist frequency"*, *"clock drift compounds the sample
  error"*, *"both authors are in the loop"*, *"we tune the room, not the speakers"*.
- The poetic vocabulary is explicitly banned in both prompts (berlin, techno, neon, concrete,
  soul, journey, vibe), and the register examples in the prompt anchor the voice far better than
  describing it.
- **Lesson worth keeping:** the stream generator feeds the last 14 lines back as context, so an
  old register re-seeds itself. Changing the prompt is not enough — clear `stream.txt` and the
  hero `type_history.json` at the same time, or the model continues in the old voice.

## Open threads

- Camera and MIDI are still unplugged; audio-reactive is doing all the work.
- Next: more typography treatments (per-character reveal, vertical marquee, text as a mask
  for the crystal), and consider letting the LLM steer harder — e.g. it proposing a look
  (style + motion + trails) rather than only a phrase.
- The `AJ_AudioAnalysis` COMP in the same project already has kick/snare/spectral-centroid
  detectors reading an audio *file*; worth re-pointing at the live device later and reusing
  instead of duplicating analysis.


## Canvas01 — hand-drawn ecosystem (fresh canvas, stage 2)

AJ brief: mono synth line in E minor pentatonic at **108 BPM**; minimal black hand-drawn
creatures that live, evolve and interact on the projector wall, ballpoint-pen look, at
least 5 distinct designs, species replicated, swarm behaviour, evolving flora + fauna.

**Built**
- `Desktop/TouchD2025/Canvas01/gen_creatures.py` — draws each species as real strokes
  (soft brush walked along noise-displaced paths, pressure taper, hatching/stipple for
  interior shading). 6 fauna: crawler (beetle), worm (segmented, bristles), jelly
  (ribbed dome + tentacles), moth (wings, stippled eyespots), shell (log spiral + foot),
  fish (diamond body, forked tail). 4 flora: grass, mushroom, lichen, fern.
  `gen_masks.py` derives opaque white-ink-on-black masks for the render path.
- `/project1/Canvas01/eco` — `eco_core` DAT module holds one shared simulation,
  `sim_<species>` scriptCHOPs expose `tx ty rz sx sy lk` for instancing.
  84 agents live (16 crawler, 10 worm, 12 jelly, 18 moth, 8 shell, 20 fish).
- Behaviours differ per species: crawler walks the floor and turns on note onsets;
  worm drifts as a column on a travelling wave; jelly rises, pulses and loops over the
  top; moth chases a moving lamp and scatters on onsets; shell barely moves and spins
  on kicks; fish schools with cohesion/alignment/separation and a leader heading.
- Audio: same MOTU ASIO 9/10 feed; bands + a **note-onset detector** (level vs previous
  level) drive events; genes and populations mutate on the onset stream (evolution).
- Render: each sprite layer is stamped additively in ink space and inverted once to
  paper, so ink darkens paper and overlaps compose. Projector `display` windowCOMP on
  display 5, exclusive, borderless.

**TD lessons worth keeping**
- Connects across COMPs fail silently in this build — build a render chain inside ONE
  COMP and cross COMPs only with par references (`selectTOP.par.top`).
- compositeTOP/glslTOP/levelTOP input connectors do not accept `.connect()` when the
  chain was created in the same script pass; setting `par.tops` first then connecting
  works, and a `nullTOP`→`glslTOP` hop can silently no-op.
- `moviefileinTOP.par.file` needs an absolute path here; a relative path fails silently
  and the TOP reads black.
- SOPs created via Python `.create()` default to `display=False, render=False` — the
  root cause of the empty instanced render; set both explicitly if the 3D path is revived.
- transformTOP resizes its input to the output resolution BEFORE scaling, so a small
  sprite is stretched to the frame first; size maths must account for that.
- Expression quoting: use double quotes inside `op("...")["chan"][i]` — backslash-escaped
  quotes make the expression fail and the par go to zero size.


### Canvas01 iteration 2 — scaled ecosystem + render-path lessons

AJ: "going up in complexity too" -> bigger populations, flora, more stamps.

- Populations now 114 fauna (crawler 20, worm 16, jelly 18, moth 22, shell 12, fish 26) + 19 flora
  (grass 5, mushroom 4, lichen 6, fern 4). Each agent carries a `depth` 0.75-1.25 that scales
  its drawing, so the wall reads near/far instead of one flat plane.
- 44 stamps live on the wall (6 per fauna species, 2 per flora) as one additive/max ink chain:
  inverse once at the end -> black ink on white paper.
- Sprite pipeline fixed: sprites are now drawn at **512 px** (the generator scales all stroke
  coordinates and brush radii from a 160 px authoring space). At 160 px the stamps were
  up-scaled to the frame and then minified, and the double resample ate the 1 px pen strokes -
  the ink arrived at ~9% of its value and the wall went white.

Render-path rules learned (all cost real time here, so they are worth keeping):
- `extend='hold'` on a transform smears the sprite's edge across the whole frame; with ink
  layers use `extend='zero'` (outside = black = identity).
- `add` on many ink layers saturates overlaps into black blobs; `brightest` (max) keeps pen
  tones and merges strokes like a real drawing.
- Composite/glsl/level TOP input connectors in this build will silently refuse `.connect()`
  across COMPs; keep a render chain inside ONE COMP and hop COMPs with a par reference
  (`selectTOP.par.top`) instead.
- The instanced 3D route (geometryCOMP + renderTOP, one draw call for hundreds of creatures)
  works once SOPs get `display/render=True`, but its camera mapping here is anisotropic
  (1 world unit -> different px per axis), so it is parked: geos exist with render=False.
- `moviefileinTOP.par.file` needs an absolute path; a relative path silently reads black.


### Canvas01 iteration 3 — illustrator-grade artwork + articulated animation

AJ: "get away from the children's drawing … you are an expert illustrator and animator,
give me your best, highly detailed output in every sense."

**New artwork engine** (`Desktop/TouchD2025/Canvas01/ink_engine.py`)
- variable line weight: strokes taper at both ends and thicken through the belly, with an
  ink-flow noise on top
- form-following hatching: shading lines are concentric offsets of the outline, so tone
  wraps the body like an engraving rather than ruling straight lines across it
- rule hatching clipped to a polygon for shadow sides, stipple for texture, punctuated
  dotted rows for beetle striae / fish lateral lines / wing marginal bands
- `vein()` for wing venation with cross-barbs, `hair()` for fur and bristles, `shadow()`
  for a contact shadow so a creature sits on the paper

**Parts instead of whole creatures** (`gen_parts.py`), so the animals can articulate:
crawler body / leg / antenna, worm head / segment ring, jelly bell / tentacle, moth body /
forewing / hindwing, fish body / tail / fin, shell / foot, grass / mushroom / lichen / fern.
19 parts, each exported as black-on-transparent (review) and white-on-black (render).
Convention: every part is drawn with its JOINT at the image centre, so TouchDesigner
rotates it about the hip, the wing root or the base of the plant.

**Articulated simulation** (`eco_core_v4.py`)
- crawler: six legs in the insect tripod gait (legs 0/3/4 against 1/2/5), body bobbing
  with the stride, antennae swaying and whipping on note onsets
- worm: peristalsis - rings contract in sequence along a travelling spine wave
- jelly: bell pulse, quickening on kicks, tentacles lagging on drag phases
- moth: four wings beating at 8-14 Hz (rate follows the highs), fore/hind offset, wing
  squashed on the downstroke
- fish: school with a tail sweeping on a phase-lagged spine wave
- shell: spiral rotation, foot ripple, small hop on kicks

**Renderer decision (important for anyone picking this up)**
- The instanced route (geometryCOMP per part + one renderTOP, 200+ instances for free) is
  built and does render, and instancing itself works (`oplength` and manual counts both
  verified proportional). What would not settle is the world->pixel mapping of the ortho
  camera: measured, a 1x1 world quad fills 1280x720, so 1 unit = 1280 px across and 720 px
  down (aspect 1.778 anisotropic), and parts authored for one convention landed off-frame
  or oversized under the other. The instanced chains remain in the file with render off.
- The FLAT compositing path (transformTOP per stamp + a `brightest` composite chain,
  inverted once to paper) renders correct positions and proportions, and costs almost
  nothing: **70 stamps at 60 fps with 0.1% of the frame budget**. Detail is chosen per
  stamp, so density is a design decision, not a performance limit.
- Sprite export size matters and must match the display size: parts are authored at 320 px
  and displayed at ~200-300 px, so the pen lines survive. Authoring at 1024 px and letting
  the renderer minify destroyed them (only the thickest strokes survived, which is what
  made the wall look like scattered fragments for several iterations).

**Known next steps**
- the middle of the frame reads crowded while the edges are empty: spread is the wrap
  bounds plus slow drift, so either raise the population (there is fps headroom for a few
  hundred stamps) or bias the spawn distribution
- some creatures overlap near-duplicates of themselves, which reads as a double exposure
- ink could be punchier on the projector: currently gain 2.1 with a 0.02 black level


### Canvas01 iteration 4 — 25% scale, many individuals, instanced renderer settled

AJ: "everything would benefit if everything is scaled down to 25% size allowing for much
more representation of individual behaviour."

That direction needs the instanced renderer rather than the flat stamp chain, so the
mapping was finally pinned down by measurement:

- **In the instanced renderer, one world unit spans the WHOLE frame in each axis**
  (a 1x1 world quad at instance scale 1.0 renders 1280x720). Therefore:
  `sx` = the drawn frame fraction (0.2 -> 256 px), `sy` = `sx * 1280/720` to keep the
  sprite square, and `tx`/`ty` are signed frame fractions (-0.5 .. 0.5).
  A single instrumented instance confirmed it: at sx=0.2 the ink measured 227x286 px,
  i.e. 88.7% of the expected 256 px frame, aspect ratio 0.79 (the beetle drawing is
  taller than wide), ink centre offset because the drawing is asymmetric in its frame.
- Instancing itself was always fine - `oplength` and a manual count both scale the
  drawn ink proportionally (48 instances = 10x the ink of 1).
- **The renderer's screen y runs opposite to a "y grows upward" simulation**: the rooted
  plants rendered at the top of the frame until `ty` and `rz` were negated in the cook.
  Mirroring those two, and not `tx`, puts the ground layer at the bottom.

Scale of the current set: **168 individuals** (crawler 20, worm 16, jelly 16, moth 24,
shell 14, fish 24, flora 56) drawn as **798 part instances** across 19 part types, with
each creature at 25% of its previous drawn size. Measured cost: **60 fps at 0.1% of the
frame budget** - so the ceiling is a design choice, not performance. The flat stamp chain
is bypassed (paper_final <- ink_gain <- ren_all) and its nodes remain for reference.

Artwork rule refined again: a part is authored at roughly **twice its display size**
(128 px art for a ~60 px creature) with the nib opened up (WIDTH 1.25), because at 25%
scale a 160-320 px sprite is minified 3-5x and the pen lines blur into blobs.

Still open: the population drifts into a loose vertical band rather than spreading evenly
(wrap bounds plus slow drift; the moth lamp also gathers the moths), and at 25% each
creature is a small mark, so the fine interior hatching only reads when you look closely.

**Two facts about renderTOP worth using later** (from a par dump)
- `par.render` and `par.renderpulse` exist, so the instanced render can be gated on/off
  from Python rather than only by unplugging it downstream.
- `par.transparency [sortedblending, orderind, alphatocoverage]` - which means proper
  alpha-blended ink on white paper is available as an alternative to the current path
  (white ink on black, additive, inverted once). Alpha blending would let the pen strokes
  keep their real tone and layer without the gain needed to survive the invert.


### Canvas01 iteration 5 — beat-locked, audio-driven life (v5 simulation)

AJ: "more complexity, more life, more reactive."

Everything now runs off the track's grid: **BPM = 108, beat = 0.5556 s**, and every
rhythm is a phase of that clock rather than an independent oscillator.
- beetle tripod gait: one stride per **two beats** (verified numerically: the gait phase
  advances exactly tau over 2 beats)
- moth wings: **four flaps per beat**, the rate opening further with the high band
- jelly bell: one pulse per **two beats**, with a burst on each kick
- fish tail: **1.5 sweeps per beat**; flora sway: once per **eight beats**; flowers open on
  the beat

**Population is audio-driven, and it switches individuals rather than scaling them.**
Each animal carries a fixed `roll`; density = 90 s form arc x the room's level, and an
individual is drawn only while its roll is under that density. So a quiet passage really
is a nearly empty sheet and a loud one is full, with individuals hatching in and fading out
one at a time. Measured during a loud passage: crawler 27/30, moth 28/30, fish 28/30 live.

**Spread:** every individual has a home cell on a jittered grid and is pulled gently toward
it, which broke the banding the population used to drift into.

**Flora now live and die:** age drives a curve - sprout, mature, wither - and a withered
plant reseeds at a new spot with a new temperament. Growth rate follows the low end and the
level, so the garden grows with the music. A new part, `flora_flower`, blooms on onsets.

**Onsets do more than scatter:** beetles startle and hop, jellies double-pulse, the school
re-aims, snails hop, and a bloom wave (decaying ~0.6 s) runs through the flowers.

**Temperament:** each individual has a 0.72-1.38 temperament gene that scales its speed,
amplitude and jitter, so no two of a species move alike.

Scale: **234 individuals / 1082 part instances** across 20 part types, at **60 fps and 0.1%
of the frame budget** - still two orders of magnitude of headroom.

Still open: at 25% a creature is a small mark, so the interior hatching only reads close up;
the spread is much better but not perfectly even.


### Canvas01 iteration 6 — fixing the flicker (AJ: "very flickery, maybe alpha/blending issues")

AJ was right about the cause. Diagnosed by inspection, not guesswork:

- The sprite textures used for rendering (`m_<part>.png`, white ink on black) are **fully
  opaque: alpha = 1.0 everywhere**. With the material's `blending = On` that means every
  creature draws as an **opaque quad**, so its black background erases whatever ink is
  behind it, and `renderTOP.par.transparency = sortedblending` **re-sorts 1000+ instances
  every frame** - so the whole field flickered as creatures moved relative to each other.
- Second cause: the **kick band was saturating at 1.036** and drove per-frame size changes
  on jellies and beetles, so every hit resized things frame by frame.
- Third: population density came straight off a raw audio envelope, so any individual whose
  roll sat on the threshold popped in and out continuously.

Fix:
- Render with the **pen sprites** (`<part>.png`): black ink with a real coverage alpha,
  stamped over a **white** render background. Ink on ink is invisible, so nothing erases;
  overlapping strokes darken naturally through alpha compositing - which is also more
  honest ink than the previous additive-plus-invert-and-gain path.
- `transparency = orderind` (order-independent) so TD stops sorting instances per frame.
- All five audio bands are **smoothed with a ~100 ms time constant** inside the cook, and
  density has **hysteresis** (an individual enters at roll+0.06 and leaves at roll-0.06).
- Because nothing erases any more, the effective ink roughly doubled: the population was cut
  from 234 individuals (1082 part instances) to **96 individuals (437 instances)** and the
  material's ink tone to 0.72.

Verified: five samples ~0.6 s apart gave `live = 92` **unchanged every time** (no popping)
with ink coverage moving only ~1.5% - that is creatures drifting, not flicker. 60 fps,
0.1% of frame budget.

**Durability fix:** the simulation modules were living only in the agent scratch directory.
They are now copied into the project at `Canvas01/sim/` (eco_core_v5.py, eco_core_v4.py,
and the build script for this fix) so the record is complete in git alongside the artwork
generators.

Still open: the composition knots where the fish school and the moth flock gather, and at
25% each creature's interior hatching only reads close up.


---

## SESSION CLOSE — start here next time (Canvas01 ecosystem)

AJ's sign-off: "thats all i have in me right now… remember this session so we have a
starting off point for our next jam."

### What is running on the projector right now
`/project1/Canvas01` — a hand-drawn ballpoint ecosystem, audio-reactive from the MOTU
(ASIO 9/10, via `/project1/Canvas01/audio/drives`), fullscreen on **display 5** through the
`display` windowCOMP (`winop = out`, exclusive, borderless).
- 20 part types (crawler body/leg/antenna, worm head/segment, jelly bell/tentacle, moth
  body/forewing/hindwing, fish body/tail/fin, shell/foot, grass, mushroom, lichen, fern,
  flower), **437 instanced quads**, nominal population **96 individuals**, at 60 fps and
  **0.1% of the frame budget**.
- Chain: `ren_all` (one render pass, white background, order-independent transparency)
  → `ink_gain` (contrast) → `paper_final` (pass-through, invert OFF) → `canvas_ink`
  (selectTOP) → `out`.
- Per part: `sim_<part>` scriptCHOP (code in the sibling `cb_<part>` DAT, all logic in
  `eco_core`) + `tex_<part>` moviefileinTOP + `mat_<part>` constantMAT + `geo_<part>`
  geometryCOMP (1x1 grid quad, instancing from the sim CHOP, `oplength`).

### Where everything lives
- `.toe`: `Desktop/TouchD-2025/Canvas01.toe` (project.save() from Python)
- artwork generators: `Desktop/TouchD2025/Canvas01/` — `ink_engine.py` (stroke engine),
  `gen_parts.py` (the 20 drawings); legacy `gen_creatures.py` / `gen_masks.py`
- simulation: `Desktop/TouchD2025/Canvas01/sim/eco_core_v5.py` (record copy; the live DAT
  is `/project1/Canvas01/eco/eco_core`)
- sprites: `Desktop/TouchD-2025/Canvas01/<part>.png` (ink + alpha, for render) and
  `m_<part>.png` (white on black, now unused by the wall)
- git: `Desktop/TouchD2025` (clean) — latest `517e68b`, plus `bc52064` (flicker fix),
  `a47635f` (v5 life/reactive), `73a9409` (25% + instanced mapping), `2fe20e7` (artwork)
- BerlinSet (the earlier set) is untouched and still saved separately.

### Knobs to turn first next time
- `DRAWN` in the sim (0.195 = 25% size); per-species `n` and `size` in `SPEC`
- `BPM = 108` and the `_beat()` locks (gait 0.5, flap 4.0, pulse 0.5, tail 1.5, sway 0.125)
- density = 90 s arc x level, in `update()`; `luck`/`roll` distribution for population
- material ink tone (currently 0.72 on colorr/g/b)

### Open items, in the order I would take them
1. the composition knots where the fish school and the moth flock gather — the homes are
   spread but the attractors fight them
2. at 25% a creature is a small mark, so interior hatching only reads close up (levers: a
   35-40% size bump, or a sharper tone curve)
3. **inter-species interaction** — fish hunting, beetles scattering from them, moths drawn
   to the flowers — so the ecosystem has relationships, not just individuals
4. a slow light/weather arc over the whole set

### Hard-won rules (do not rediscover these)
- **Instanced renderer mapping:** one world unit spans the WHOLE frame in each axis. So
  `sx` = drawn frame fraction (0.2 -> 256 px), `sy = sx * 1280/720` to keep it square, and
  `tx`/`ty` are signed frame fractions.
- **Its screen y is opposite a "y grows up" simulation**: negate `ty` and `rz`, never `tx`.
- **Flicker was alpha, not motion**: opaque white-on-black sprites with `blending On` drew
  as opaque quads that erased each other, and `transparency = sortedblending` re-sorted
  1000+ instances per frame. Fix = real-alpha ink sprites over a white background +
  `transparency = orderind`.
- **Author artwork at ~2x its display size** (128 px art for a ~60 px creature) with the nib
  opened up (WIDTH 1.25); exporting large and letting the renderer minify destroys pen lines.
- Connects across COMPs fail silently - keep a chain inside one COMP, cross with par refs.
- `moviefileinTOP` needs an absolute `file` path, and a **reload toggle** (`par.reload`
  True/False), not just `reloadpulse`, to pick up a changed file.
- Sofa rule from this session: a fresh sim starts with `live = 0`, which blanks the wall for
  a second on reload - the seed now starts the population already out.

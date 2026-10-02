---
tags: [type/project, godot, mcp, timebox, lantern-garden]
---

# InkGarden — timebox build (2026-10-02, deadline 20:00)

**Requester:** AJ (direct brief: "see how far you can push this concept" — enemies, actions, weapons, mechanics, menu, sound; keep the graphic design)
**Owner:** Winbot
**Started from:** [[Godot/InkGarden — Phase 0 Godot + MCP Prototype (2026-10-02)]]

## What the game became

InkGarden is now a seven-depth, procedurally generated, black-and-white
hand-drawn top-down action game. Everything in it — the art, the sound, the
levels — is produced by seeded Python generators in `tools/`, so the whole game
is reproducible from source and there is not one hand-authored binary asset.

| System | What it is |
| --- | --- |
| Levels | `scripts/level.gd` carves 6-9 rooms, then joins them with L-shaped corridors. Connectivity is structural, not retried. A level is two integers (run seed, depth). |
| Objective | The exit door is locked. A key is hidden in the room furthest from the spawn. Find it, reach the door, descend. Seven depths to clear. |
| Weapons | Melee arc (free) and thrown ink bolts (spend ink picked up from vials). |
| Movement | 8-way walk, and a dash whose frames are invulnerable — so it doubles as a dodge. |
| Enemies | Crawler (charges), floating eye (holds range, fires), brute (soaks damage), boss (three-way spread, drops a key), leaper (lunges in bursts), splitter (leaves two leapers when killed). One script, six stat/behaviour rows. |
| Feedback | Ink slash arcs, impact bursts, death puffs, shockwave rings, trauma-based screen shake, i-frame blinking, and ink splats left on the floor where something died. |
| Menu | Title, pause (Resume / Abandon run / Quit), death screen with score and depth, victory at depth 7. |
| Sound | 13 synthesised clips plus a seamless 20 s music loop. |
| HUD | Hearts, score, key count, ink count, hint line, transient messages — all on paper chips, because ink text over hatched walls is unreadable. |
| Minimap | A generated thumbnail of the whole level in the corner, with player, key and exit marked. |
| Objective guard | The key room is defended by 2+ enemies, scaling with depth — the objective is an encounter, not a stroll. |
| Kill chain | Consecutive kills without taking a hit raise the score multiplier, capped at x5. One hit resets it. |

## Verified, not assumed

Every row below came from a real invocation against the running game.

| Check | Result |
| --- | --- |
| Level generation | 7 enemies (5 patrols + 2 key guards), 8 pickups, 81 decor props, 2 vials, exit door placed at the exit cell |
| Run starts via the title menu | `state=1` (PLAYING) after the menu's own confirm path |
| Melee | enemy HP 4.0 → destroyed over repeated strikes |
| Ranged | vial collected → ammo 0 → 5; throwing spent it (2 bolts thrown) |
| Ranged kills | score moved to 10 (a thrown bolt killed a crawler, worth 10) |
| Kill chain | combo 0 → 3 after three kills; `multiplier()` returned 2; capped at 5 after 33 kills; a hit left the chain at 3 while i-frames ran and reset it to 0 once cleared (controlled both ways — the earlier single-sided version was passing on luck) |
| Contact damage → death | health 1 standing in contact → `state=3` (DEAD), death overlay shown |
| Pause | `toggle_pause` flipped state to PAUSED and back |
| Volume | `master_db` 0 → -6 over two steps, written to `user://settings.cfg` (`master_db=-6.0`), raised back to 0 |
| Enemy steering | with the wall probes active an enemy closed on the player from 331 → 148 units |
| Death splats | 3 kills stamped exactly 3 ink splats into the level, and a rebuilt depth carried none |
| Driving the live instance | attached to the **detached projector instance** over TCP, pressed Begin through the bridge (state 0 → 1), read 7 enemies in the `enemies` group, moved and attacked, and captured its own framebuffer at 1600x1000 — no `run_project`, no second window |
| Best score | 7777 written to `settings.cfg` and read back by `_load_best()`; the volume section in the same file survived the write; the title screen renders `best  7777` |
| Audio | 13/13 files, 44.1 kHz 16-bit mono, re-verified **independently of the generator's own checker**; one-shots all exactly -19.71 dBFS RMS (0.000 dB spread) with music 3 dB under at -22.71; nothing above -3.00 dBFS peak; byte-identical across two regenerations |
| Music loop | still 882000 frames = 20.000 s = 6 whole bars at 72 BPM with zero endpoints and seam step 0, but the per-bar level swing fell from ~14 dB to under 3 dB (body RMS-envelope spread 27.07 → 0.72 dB) and the melody went 11 → 29 plucks |
| SFX distinctness | the four previously near-identical effects spread from a 1.72x to a 6.29x spectral-centroid ratio; the worst old pair (hit vs enemy_die, 11% apart) is now 80%+ apart |
| On the projector | window 1616x1039 at (2072,45), horizontally centred on DISPLAY5 |

## Bugs found and fixed during the build

The interesting ones, because each cost real time and each is a lesson:

- **`Game.level` was never declared.** `main._start_run()` assigned it, the
  assignment threw, and because `run_project` launches with `-d` the error hit a
  *debugger break* which froze the entire game — the MCP bridge then returned
  `timed out` to every subsequent command. A frozen bridge is a crash, not a
  hiccup: check the game's own log first.
- **Deferred frees keep their node names.** `world.build()` used `queue_free()`
  on the previous level's actors, which is deferred, so the new generation got
  auto-unique `@CharacterBody2D@201` names instead of `Enemy` — making the level
  impossible to address from the MCP. Fixed with `remove_child()` before
  `queue_free()`.
- **`game_set_property` wants vectors as objects.** `{"x":..,"y":..}`, not the
  string `"Vector2(..)"`. A string fails *silently*: the call reports success and
  the property is never written. Two verification runs were wasted on this.
- **`game_get_node_info` in a loop saturates the runtime bridge.** It walks every
  child and returns full property/method/signal lists; hammering it makes later
  commands time out after 10 s. Read single properties.
- **`AudioStreamWAV.loop_end = 0` is a silent track.** The loop region has to be
  given a real frame count or the music never plays.
- **The overlay trusted a signal.** Starting a run by writing `Game.state`
  directly meant `state_changed` never fired and the title menu stayed on top of
  the game. The menu now reconciles its visibility each frame.

## Where things live

| Thing | Path |
| --- | --- |
| Project | `C:\Users\ander\Desktop\Godot\InkGarden` |
| Launch it | `run.bat`, or `tools/run-projector.ps1` (`-Headless` for the smoke test) |
| Art generators | `tools/gen_sprites.py`, `tools/gen_actors.py` |
| Audio generator | `tools/gen_audio.py` (`--check` prints its measurement table) |
| Art contact sheet | `python tools/preview.py 1 6` → `$TMPDIR/inkgarden_preview.png` |
| Direct bridge client | `tools/bridge.py` — talk to a *running* instance over TCP |
| Game log | `%APPDATA%/Godot/app_userdata/InkGarden/logs/godot.log` |
| Settings | `%APPDATA%/Godot/app_userdata/InkGarden/settings.cfg` (volume + best score) |
| MCP server | `C:\Users\ander\AppData\Local\hermes\tools\godot-mcp\build\index.js` |
| Verification suite | `C:\Users\ander\AppData\Local\hermes\tools\verify_*.py` |

## How to pick this up again

Nothing has to be reconstructed: every asset is generated from a script, so edit
the generator, re-run it, and the art or audio is back.

```bash
cd C:/Users/ander/Desktop/Godot/InkGarden
P='C:/Users/ander/Desktop/Godot/InkGarden'        # native path — MSYS does not translate
G="$LOCALAPPDATA/Godot/godot_console.exe"

python tools/gen_sprites.py && python tools/gen_actors.py && python tools/gen_audio.py
"$G" --headless --path "$P" --import             # re-import changed assets
"$G" --headless --path "$P" --quit-after 150     # smoke test
./run.bat                                        # launch on the projector
```

The suite below verifies behaviour against the **real game**, not the source.
Each script starts its own instance, so run them one at a time — they all want
the runtime bridge on port 9090:

```bash
cd C:/Users/ander/AppData/Local/hermes/tools
python verify_weapons.py    # melee arc + thrown ink
python verify_combo.py      # kill chain, x5 cap, and the i-frame guard
python verify_run5.py       # leaper + splitter + hit-stop
python verify_run6.py       # master volume + enemy steering
python verify_run7.py       # death splats
python verify_run8.py       # best-score persistence
python verify_audio.py      # the wav files, measured independently
```

To poke at the instance already on the projector, `tools/bridge.py` speaks to any
running instance over TCP and needs no MCP session at all.

## Repository status

Local git repo initialised and committed — one commit, `5c3dbe5`, 147 files
tracked, working tree clean, `.godot/` ignored. **No remote yet**: when AJ
supplies the GitHub repo it is `git remote add origin <url> && git push -u origin
HEAD`. The editor cache and export output are already excluded, so nothing needs
cleaning up first.

## Honest gaps

Gameplay and UX:

- Enemy steering is walk-at-the-player plus three short wall probes, not
  pathfinding. A floating eye can still back itself into a corner.
- No minimap legend, so the key and exit markers have to be learned.
- The pause menu has no rebind or audio options; volume is on `[` / `]` only.
- Tree canopies draw under the player rather than occluding them.
- One ground tile; two wall variants exist only because a long wall of one
  repeated drawing reads as wallpaper.

Audio — **verified by measurement, never by ear**, so AJ is the arbiter. The
second pass fixed the worst of it; these remain:

- Not truly gapless: exact-zero endpoints make a seamless wrap impossible, so the
  loop's ~3 dB level spread sits entirely in the first and last quarter-second.
- The effects are ~2 dB quieter than the first pass, because levelling by RMS
  pinned the whole set to `sfx_hit`'s crest factor.
- Uniform RMS is not perceived loudness — a 0.09 s blip and a 1.2 s sting now
  measure identical.
- `sfx_hit` and `sfx_enemy_die` remain close in brightness, separated mainly by
  envelope shape rather than tone.

## Next ideas (not started)

- Pathfinding for the ranged enemy, so it repositions instead of backing into walls.
- A second boss pattern; the key room already has guards that scale with depth.
- Reloading a depth from its two integers, for reproducible bug reports.
- An attract mode, so a game left running on the projector returns to the title
  instead of sitting on a death screen.
- A per-clip gain pass: the effects are levelled by RMS, so perceived loudness
  still varies between a 0.09 s blip and a 1.2 s sting.

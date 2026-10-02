---
tags: [type/project, godot, mcp, lantern-garden]
---

# InkGarden — Phase 0: Godot + MCP on the projector

**Date:** 2026-10-02
**Requester:** AJ (direct request)
**Owner:** Winbot
**Status:** Phase 0 complete — MCP connection verified, prototype running on the projector

## What this is

Setup and configuration run for Godot on the MSI laptop, with the definition of
done being *a first minimal prototype running on the projector: black and white,
hand-drawn, top-down, 2D*. Two things had to be true:

1. The Godot MCP connection had never been tested — it is now working and verified.
2. A minimal prototype runs on the projector (**DISPLAY5**, 1920x1200 at x=1920).

## Where things live

| Thing | Path |
| --- | --- |
| Godot binary | `C:\Users\ander\AppData\Local\Godot\godot_console.exe` (4.7.1-stable, current release) |
| MCP server | `C:\Users\ander\AppData\Local\hermes\tools\godot-mcp\build\index.js` (157 tools) |
| MCP client for testing | `C:\Users\ander\AppData\Local\hermes\tools\godot_mcp_client.py` |
| Prototype project | `C:\Users\ander\Desktop\Godot\InkGarden` |

Godot 4.7.1 (released 2026-07-14) is the current stable, so **no update was
needed**. The binary was moved out of `Downloads/` to a stable per-user location.

## MCP configuration

Registered in the Hermes profile as a stdio server:

```yaml
mcp_servers:
  godot:
    command: node
    args: ["C:/Users/ander/AppData/Local/hermes/tools/godot-mcp/build/index.js"]
    env:
      GODOT_PATH: "C:/Users/ander/AppData/Local/Godot/godot_console.exe"
```

The `_console` build is required: the normal Windows build detaches from stdout,
so the MCP server cannot capture Godot's output from it.

Note: `@coding-solo/godot-mcp` on npm was last published 2026-02-03, before
Godot 4.7. The maintained fork `tugcantopaloglu/godot-mcp` (v3.1.0) is tested
against 4.7 and was built from source instead.

## Verification evidence

Every claim below came from a real invocation, not from reading code.

| Check | Result |
| --- | --- |
| MCP handshake | `initialize` → serverInfo `godot-mcp 0.1.0` |
| Tool discovery | `tools/list` → **157 tools** |
| Tool call → Godot | `get_godot_version` → `4.7.1.stable.official.a13da4feb` |
| Project scaffold | `create_project` created `InkGarden` |
| Project launch | `run_project` started the game in debug mode |
| Runtime bridge | `[SERVER] Connected to game interaction server on port 9090` |
| Live scene read | `game_get_node_info /root/Main` → Ground, Walls, Props, Player, Hud |
| Simulated input | held `move_right` for 1.5s |
| Movement confirmed | player x **448 → 1176** (dx 728 ≈ 460 u/s × 1.58s) |
| Animation confirmed | `facing` = `side`, sprite `frame` advanced to 1 |
| On the projector | window rect `(2072,45)-(3688,1084)`, 1616x1039, centred on the 1920-wide projector |

Final screenshot of the projector: `C:\Users\ander\AppData\Local\hermes\tools\_proj4.png`

## How the prototype is built

- **Art is generated, not drawn.** `tools/gen_sprites.py` (stdlib only, no
  Pillow) renders every sprite by walking a soft-disc brush along a path
  displaced by smooth value-noise; shading is hatching and stippling. Seeded, so
  it reproduces byte-identical PNGs. Palette is ink `#121214` on paper `#f6f5ef`.
- **13 sprites**: 3 walk sheets x 4 frames (down/up/side), 3 idle frames,
  tree, rock, 3 grass-tuft variants, ground tile, wall tile.
- **Level is an ASCII map** in `scripts/world.gd`, with seeded prop scatter —
  editable as plain text instead of binary tile data.
- **Scale**: 1 tile = 128 units = 128 px, hero is one tile, `Camera2D.zoom = 1.6`.
- The sprites take their cue from the Kenney-style pixel platformer pack in
  `Desktop/Godot/assets/` (shape, scale, readability), but are redrawn in
  monochrome ink rather than reusing that colour art.

## Gotchas worth keeping

- `create_project`'s `projectPath` is the project directory **itself**, not a
  parent. Passing the parent silently writes a `project.godot` there.
- `run_project`'s Godot child dies when the MCP server process exits, so a run
  that must outlive the agent has to be launched separately.
- The runtime `game_*` tools only work inside the *same* MCP server process that
  called `run_project` — one long-lived session, not a series of CLI calls.
- Hand-serialising `InputEventKey` blobs into `project.godot` is fragile;
  registering the actions in code (`scripts/controls.gd`) is smaller and safer.
- Anything with recognisable line-work baked into a ground tile repeats on every
  tile and the floor turns into a visible pattern. Keep ground tiles to paper
  grain and get variety from scattered props.

## Open next steps (not started)

Largely superseded the same evening — the timebox build added sound, menus, six
enemy kinds, weapons, a HUD and a minimap. See
[[Godot/InkGarden — Timebox Build (2026-10-02)]] for the current state, the full
file map and how to pick it up again. What is genuinely still open:

- More wall and ground tile variants; a long run of one wall drawing reads as
  wallpaper.
- Props are drawn under the player; a top-down game normally lets canopy trees
  occlude the player.
- The 100+ `game_*` runtime tools are enabled but only partly explored, and the
  runtime bridge turns out to be drivable directly over TCP — see
  `references/driving-a-live-instance.md` in the `godot-mcp-prototyping` skill.
- Decide whether Godot stays a game/visual toy or becomes the agent-facing
  interaction shell sketched in
  [[Research/2026-09-26 — Godot 4.5 as an Agent-Facing Interaction Shell]].

## Related notes

- [[Research/2026-09-26 — Godot 4.5 as an Agent-Facing Interaction Shell]] — prior
  research on Godot as an agent UI, not a game.
- [[Home Lab/The Lantern Garden — Operating Doctrine]]

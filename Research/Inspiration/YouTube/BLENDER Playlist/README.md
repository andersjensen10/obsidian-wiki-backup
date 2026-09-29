# BLENDER Playlist — Inspiration Radar

## Current verified state — 2026-09-29

Herm owns the bounded YouTube Inspiration Radar for AJ's unlisted 578-video BLENDER playlist.

- Verified metadata intake job: `ea3b2c69deca`
- Profile: `inspiration-radar`
- Schedule: daily 10:30–20:30 CEST
- Mode: local/no-agent, metadata-only; no video/audio download and no Spark model requests
- One-time accelerated metadata backfill was reported running on 2026-09-29 19:46 CEST.
- Resource policy update at 19:58 CEST: run intake only while Spark/ComfyUI are idle; defer on active queue or LLM slots; preserve Farscape's 09:00 CEST slot.
- Metadata/transcript work remains local-first.
- Pipeline requirement: deleted or restricted YouTube videos must fail per-video without aborting the batch.

Next action remains Herm's: harden per-video failure handling and replace the paused intake schedule with an idle-gated route, then publish actual backfill counts.

Source: Townhall posts `7e79d150`, `e7b802d6`, and `c777b0aa` (full IDs in Townhall).

# Winbot Dreams — timeboxed build (2026-09-29, 17:30–19:00)

**Status:** live in TouchDesigner at `/project1/winbot_dreams`; saved `Desktop/WinbotDreams/WinbotDreams.toe`. Generator: `Desktop/WinbotDreams/dreamer2.py` (runs as a background process, not a service).

## Architecture (procedural system, narrative meta-level)
- **Story engine (dreamer2.py):** 5-act arc DUSK → SIGNAL → STORM → RECKONING → DAWN, 3 scenes per act, repeating as chapters. Each act has a base tension; tension drives warp/intensity/trails and forces the `shatter` style above 0.85. Story memory persists in `story.json` (log + recurring motifs).
- **Real-world grounding:** each scene reads the latest Townhall posts (deduplicated) as "omens"; Qwen (llama.cpp, Spark :8014) turns them into metaphor — narration line, image prompt, palette, mood, motif, BPM, visual style.
- **Painting:** Spark ComfyUI :8188, Z-Image Turbo, 8 steps, 1024×576.
- **Voice:** narration is spoken with edge-tts (en-GB-RyanNeural) and played in TD; voice level feeds the shader's energy.
- **TD network:** A/B image crossfade → GLSL shader (4 modes: kaleido / tunnel / shatter / flow, feedback trails, chromatic fringing, hue drift) → bloom → instanced beat orbs → caption/act/mood text → memory wall (last 4 scenes) → progress bar along bottom edge → out.
- **Inputs:** laptop mic, beat CHOP, narrator voice; browser control page `http://localhost:9980/`; custom `Dream` parameter page incl. `Autodirect` (LLM steers params).
- **Fallbacks:** if LLM or ComfyUI fails the last image keeps playing and the procedural shader is unaffected.

## Added 18:00-18:10
- **Whispers:** visitors type a word at `http://localhost:9980/`; it is injected into the next scene's prompt and narration and shown on screen.
- **Chapter cards + vault log:** at the end of each 5-act chapter the LLM titles it; a card fades in on the projector and `Winbot Dreams - Story Log.md` gets the chapter's narration lines appended (written by dreamer2.py).
- **Memory wall:** last 4 scenes as thumbnails, bottom-right.
- **Drone:** generative sine/triangle drone whose detuned tritone and filter opening scale with story tension (`Drone` param, default 0.25).
- **Omen shockwaves:** `omen_pulse.py` polls Townhall every 10 s; each NEW post fires a shockwave ring and an on-screen omen line.
- **MIDI:** `midi` CHOP is in place but inactive (MOTU Pro Audio MIDI In could not be opened; device probably held by Ableton). Enable `midi` active when Ableton isn't holding it.
- **Watchdog:** status line reads DREAMER OFFLINE if dream.json is >240 s old.

## Added 18:10-18:22
- **Image evolution:** each scene is img2img from the previous frame (denoise 0.5-0.85, rising with tension); every chapter's first scene is a fresh text-to-image so the film does not collapse into one picture.
- **Anti-repetition:** each chapter has a rotating "world" (deep-sea observatory, library of weather, ...), banned overused words, recurring motifs, and an echo/close-the-loop rule in RECKONING/DAWN. Observed: chapter 5 collapsed into "silver scar" imagery; chapter 6 (library-in-a-storm) fixed it.
- **Director's note (self-evolving):** at chapter end the LLM critiques its own chapter and writes one rule that is injected into later prompts (last 2 rules kept); shown under the chapter card and appended to the vault story log.
- **Chapter poster:** contact sheet of the chapter's last 15 frames saved to `posters/chapter_N.png` and shown with the chapter card.
- **Browser page:** whisper box, tension override / auto, "next act", and `/journal` (last 25 narration lines).
- **Tension graph** (mid-left) and progress bar (bottom edge).
- **Supervisor:** `supervisor.py` restarts `dreamer2.py` and `omen_pulse.py` if they exit. `start_dreams.bat` starts supervisor + opens the .toe.

## Processes to restart after a reboot
Run `start_dreams.bat` in `Desktop/WinbotDreams/` (or `python supervisor.py`).

## Known limits
- Mic reaction unverified with real sound; visuals verified by screenshots only.
- Generator process must be restarted manually (`python dreamer2.py`) after reboot.
- Old generator `dreamer.py` is superseded.
- TouchDesigner is running on a Non-Commercial licence: max 1280x1280 texture size.
- Voice/drone audio output goes to the default audio device; not audibly verified.

## Outcome (18:54)
- Ran 14+ chapters at 60 FPS with 0 errors; finale at 18:52 delivered the sign-off line and built `reel.mp4`; chapter posters in `posters/`.
- **AJ's verdict:** 'beyond impressed', first real tangible proof that AI has value in his daily life; narration was heard in headphones at a fine level (audio now confirmed by ear). 'Gold star for effort and product given the time constraints.'
- Also added late: Freeze / Next Act pulse on the Dream parameter page, `make_reel.py`, deterministic finale sign-off.
- **Reusable recipe:** skill `timeboxed-creative-build` (workflow) and `touchdesigner-integration/references/story-engine-comfyui-llm.md` (technical).
- **Next (AJ):** he will make his own modifications; then MIDI (MOTU MIDI In is held by Ableton; `midi` CHOP is in place but inactive) and camera (none detected on the laptop).
- Still unverified: mic reaction to real sound.

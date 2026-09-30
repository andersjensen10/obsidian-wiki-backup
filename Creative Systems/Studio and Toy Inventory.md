# Studio and Toy Inventory

Living record of AJ's gear, so agents can propose creative projects that use it. Started 2026-09-29. Only add what AJ has stated or what was verified; mark everything else *unknown*. Winbot grows this over time by asking short questions.

## Stated by AJ (2026-09-29, not yet itemised)
- **MIDI:** more MIDI interfaces than the MOTU (which TouchDesigner sees as `MOTU Pro Audio Midi In` and `LTC Sync In`).
- **Synths:** digital and analog (models unknown).
- **Eurorack:** a rather large system (modules, clock/CV interfaces unknown).
- **Raspberry Pis:** four, currently unused (the Lantern Garden notes list them as spares).
- **Strudel:** remote Strudel boxes, possibly synced via Ableton Link (idea stage, not set up).
- **Ableton + Push:** in use for production.

## Known from verified work
- **Windows laptop (MSI):** TouchDesigner 2025.33230 (Non-Commercial, 1280x1280 texture cap), drives the living-room projector. No camera detected. Audio devices seen: MOTU Pro Audio (In 1-2, In 1-24), laptop mic array.
- **Spark (192.168.0.139):** llama.cpp :8014 (Qwen 3.6 35B), ComfyUI :8188 (Z-Image Turbo, Flux 2 Klein, Qwen Image, LTX 2.5 video), Fish Speech / voice services.
- **NUC:** spare.

- **MSI audio/MIDI census (Winbot, 2026-09-30, read-only):** MOTU Pro Audio is the only external audio/MIDI interface visible (audio In 1-2, In/Out 1-24; MIDI In/Out and LTC Sync In). No other USB MIDI device is currently visible to the MSI. Camera: none yet; AJ is connecting one by USB and will notify Winbot.
- **Budget (AJ, 2026-09-30):** Jev cap starts at $0.25/day; AJ is open to raising it for meaningful work.
- **Programme:** full breakdown of Pis, NUC, MIDI and audio interfaces planned in [[Creative Systems/Inventory Program — Full Breakdown Plan]].

## To find out (ask AJ a few at a time)
- MIDI interfaces: make/model, ports, which are free while Ableton is open.
- Synths: models, MIDI/USB/CV, clock sync.
- Eurorack: MIDI-to-CV, clock, audio interface, key modules.
- Pis: models, RAM, OS, network, GPIO or audio hats.
- Strudel and Link: where it runs, how Link would be bridged.
- Camera, lights, other displays.

## Ideas this unlocks (unbuilt)
- MIDI/CV from TouchDesigner scenes to synths and Eurorack; story tension as a clock or CV source.
- Pis as remote sensors, display nodes or Strudel boxes; Ableton Link as shared tempo across them and the beat CHOP.

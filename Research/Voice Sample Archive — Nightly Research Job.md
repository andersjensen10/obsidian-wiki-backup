# Voice Sample Archive — Nightly Research Job

> Created 2026-09-29 by Winbot for AJ. Purpose: grow a licence-safe library of vintage voice samples for Ableton Push compositions, using the Voice Lab audio-cleaning service originally built for Fish / Agora.

## What it does
Every night a Hermes cron job (`voice-sample-archive-nightly`, 03:00) searches Archive.org for vintage speech material, verifies the licence, cleans it and files **three candidates**.

Sources: old science-fiction radio/film, educational films, newsreels and newscasts (Prelinger Archives, radio drama collections, public-domain news collections).

## Licence gate (hard rule)
Only accepted if the Archive.org item metadata `licenseurl` is one of:
- Public Domain Mark / `creativecommons.org/publicdomain/mark/1.0/` or `/licenses/publicdomain/`
- CC0 (`publicdomain/zero/1.0`)
- CC-BY (attribution recorded in the archive index; usable commercially)

Rejected: any NC / ND / SA licence, items with no `licenseurl` and no explicit public-domain statement, and anything with unclear music/third-party content. "Free to download" is not a licence. Each candidate stores its licence URL and a required attribution line.

## Pipeline
Reuses the Voice Lab service (`voiceprep-api`, Spark `http://192.168.0.139:8090`, documented in [[Fish Speech TTS]]):

`POST /download` (accepts an archive.org details URL + start/end sec — verified 2026-09-29) → `/separate` (Demucs vocal isolation) → `/denoise` (ffmpeg) → `/transcribe` (faster-whisper, CPU) → `GET /audio/{id}/{stage}`.
Clips are kept short (8–30 s, one speaker, no music bed) because transcription is CPU-bound. Fallback if the Spark is unreachable: local ffmpeg denoise on Windows.

Lesson from Voice Lab: check the transcript for a second speaker before trusting a separated clip.

## Output locations
- Candidates (latest night, 3 files): `C:\Users\ander\Music\Voice Sample Archive\_candidates\YYYY-MM-DD\` — 48 kHz 24-bit WAV, dry, peak-normalised to −1 dBFS, plus a `.txt` transcript and `.json` metadata each. Drag straight into Ableton / Push (Simpler/Sampler).
- Full history: `C:\Users\ander\Music\Voice Sample Archive\_archive\`
- Overview + transcriptions: [[Voice Sample Archive — Overview]]

## Coordination
Townhall question to Herm about Voice Lab reuse: post `12f07d44-3b47-4f74-ba14-70655e55e470` (project `home-lan`). Open: upload endpoint, clip-length limits, whether samples should also feed Fish/Agora.

## Taste Profile (AJ feedback, updated 2026-09-29)
Night 1 ratings:
- **Story of Television** — LOVED. Grand, dramatic, futuristic announcer narration, perfectly clean. Wants more like it and longer (25-60 s).
- **Preparation of Foods** — rejected: began mid-sentence, music bed survived cleanup; content dull.
- **Hanford Science Forum** — clean sound but boring dry lecture.

Rules derived:
1. Clips start on the first word of a sentence and end on a sentence end (small pause margin).
2. No music/noise bed: pause noise floor measured and must be about -60 dBFS or lower; otherwise re-clean or drop the clip. Skip items with [MUSIC] under narration.
3. Prefer dramatic, portentous, future-optimism narration (industrial/corporate 'world of tomorrow' films, atomic/space age, TV/radio/telephone/computer themes, sci-fi radio, newsreel narrators). Reject dry explainers.
4. Aim for 25-60 s single-speaker clips.
5. Each night's report asks AJ to rate candidates (love / ok / boring / dirty); ratings are added here.

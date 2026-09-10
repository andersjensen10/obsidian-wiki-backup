---
tags: [project/agora, type/resolved-bug]
---

# BUG-07 — Image messages spoke the raw diffusion prompt

- **Severity:** Medium · **Category:** UX / media integration
- **Status:** Fixed (front-end pass, 2026-09-06)

## Problem
A completed image generation rendered the raw diffusion prompt as the message
body with a "Speak this message" button, so clicking Speak read the prompt
("a cute fluffy orange cat…") aloud as if the persona had said it.

## Fix
`apps/web/src/routes/+page.svelte`:

- `canSpeak(m)` returns false for media messages (`!m.mediaId`), so the speak
  button and auto-speech never attach to an image/video.
- The diffusion prompt is rendered as a caption *under* the media
  (`.media-caption`, `mediaPrompt()`), clearly metadata rather than dialogue,
  and the body text is only shown for non-media messages
  (`{#if m.content && !m.mediaId}`).

## Verification
- `npm run check` clean.
- Media messages no longer render a speak affordance; the prompt shows as an
  italic caption.

## Related notes
- [[README]] — full Resolved Bugs index for this QA pass.
- [[Agentic Chatroom]] — project status snapshot.

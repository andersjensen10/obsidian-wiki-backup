# BUG-11 — Images opened as raw browser tabs, no lightbox

- **Severity:** Low · **Category:** UX / media gallery
- **Status:** Fixed (front-end pass, 2026-09-06)

## Problem
Clicking a generated image was a plain `<a target="_blank">` to the static PNG —
it opened the raw file in a new tab, losing the room, the prompt, and any way
back. No zoom, no metadata.

## Fix
- `apps/web/src/lib/MediaLightbox.svelte` — in-app lightbox with the image, its
  prompt, and navigation between items; focus-trapped and Esc-closable.
- `+page.svelte` — the image is now a `<button class="media-btn">` that calls
  `openLightbox(m)` (videos get an "Open full size" affordance); media is
  indexed on arrival (`mediaIndex`) so the lightbox shows the prompt without a
  refetch. The old raw `<a href>` is gone.

## Verification
- `npm run check` clean.
- No remaining `<a href={api.mediaUrl(...)} target="_blank">` in the transcript
  render; clicks route through `openLightbox`.

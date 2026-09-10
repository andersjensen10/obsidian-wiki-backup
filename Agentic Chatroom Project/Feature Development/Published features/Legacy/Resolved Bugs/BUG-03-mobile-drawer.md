---
tags: [project/agora, type/resolved-bug]
---

# BUG-03 — Mobile sidebar hard-hidden with no drawer

- **Severity:** High · **Category:** Visual / responsive
- **Status:** Fixed (front-end pass, 2026-09-06)

## Problem
Below 820px the sidebar was `display: none` with no hamburger or drawer, so
mobile/narrow users lost all access to rooms, cast, room creation, and
turn-taking controls.

## Fix
The sidebar is no longer removed at narrow widths — it is parked off-canvas and
promoted to a slide-over drawer:

- A `Menu` button in the room header (`.menu-slot`, visible only ≤820px) opens
  the drawer; a scrim and a close button dismiss it; `Escape` also closes it.
- `aside` becomes `position: fixed` + `translateX(-102%)` off-canvas, sliding in
  on `.drawer` with `focusTrap` for keyboard users and a
  `prefers-reduced-motion` guard.
- Same element, same content — no duplicate markup.

All in `apps/web/src/routes/+page.svelte` (see the `BUG-03` comments and the
`@media (max-width: 820px)` block).

## Verification
- `npm run check` clean (a11y + types).
- The drawer element and toggle are wired to `drawerOpen`; desktop layout
  unchanged above the breakpoint.

## Related notes
- [[README]] — full Resolved Bugs index for this QA pass.
- [[Agentic Chatroom]] — project status snapshot.

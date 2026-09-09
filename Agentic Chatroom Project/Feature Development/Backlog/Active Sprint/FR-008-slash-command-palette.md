---
status: shipped
origin: feature-request
source: "[[Next Level Agentic Chatroom Project-ARCHIVE]]"
criticality:
  impact: low
  urgency: low
size: S
dependencies: []
matured: 2026-09-08
matured_by: Scrummaster
---

# Interactive Slash Command Palette (`/` and `Cmd+K`)

## Context
Extracted from [[Next Level Agentic Chatroom Project-ARCHIVE]] (Priority: P2 stretch) and [[improvements]] §5.2. Command assistance currently relies on a static help popup. Implementing an interactive slash command palette gives power users and directors fast keyboard access to generation, room control, and character staging commands directly within the composer. Criticality is Low impact and Low urgency.

## User story
As a user or director typing in the room composer, I want typing `/` or pressing `Cmd+K`/`Ctrl+K` to open an autocomplete command palette, so that I can quickly discover and invoke room commands without memorizing syntax.

## Acceptance criteria
- [ ] Typing `/` at the beginning of an empty composer input opens an inline autocomplete menu above the composer.
- [ ] Pressing `Cmd+K` (Mac) or `Ctrl+K` (Linux/Windows) focuses the composer and opens the command palette from anywhere in the room view.
- [ ] Palette lists available commands with descriptions and parameter hints:
  - `/image [prompt]` — Trigger ComfyUI image generation.
  - `/video [prompt]` — Queue LTX-2.3 video synthesis.
  - `/say [persona] [text]` — Force a specific persona to take the floor and speak.
  - `/narrate [event]` — Inject an environmental or third-person world narration.
  - `/clear` — Clear current room transcript history.
  - `/roll [dice]` — Roll dice expression (e.g. `2d20`).
- [ ] Keyboard navigation: `Up`/`Down` arrows navigate items; `Enter` or `Tab` auto-completes the selected command into the composer; `Esc` dismisses the palette.
- [ ] Parameter hints display dynamically as the user fills in arguments.

## Implementation notes
- Add `apps/web/src/lib/CommandPalette.svelte` component.
- Bind keyboard listeners in `apps/web/src/routes/rooms/[id]/+page.svelte` composer input.
- Dispatch existing command handlers already present in the room client or server WS dispatch.
- Ensure mobile tap on slash options works smoothly.

## Non-goals
- Adding arbitrary custom user-scripted macro commands.
- Replacing the top navigation bar or room switcher.

## Definition of done
- `npm run check` and `npm run typecheck` clean.
- `npx vitest run` passes.
- Browser test verifies typing `/`, navigating with arrows, and executing `/image`, `/say`, and `/clear`.

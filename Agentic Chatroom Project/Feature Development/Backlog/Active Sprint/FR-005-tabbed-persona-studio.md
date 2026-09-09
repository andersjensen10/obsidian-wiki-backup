---
status: shipped
origin: feature-request
source: "[[Next Level Agentic Chatroom Project-ARCHIVE]]"
criticality:
  impact: high
  urgency: medium
size: M
dependencies: []
matured: 2026-09-08
matured_by: Scrummaster
---

# Tabbed Persona Studio Redesign

## Context
Extracted from [[Next Level Agentic Chatroom Project-ARCHIVE]] (Priority: P1) and [[improvements]] §6.1. The Persona editor in `apps/web/src/routes/personas/+page.svelte` is currently a monolithic single-column scrollable form. Although [[BUG-06-persona-dirty-guard]] added navigation protection and [[BUG-08-sticky-savebar]] introduced a sticky savebar, navigating across persona traits, voice settings, and media prompts remains clunky and overwhelming. Breaking the editor into focused tabs dramatically improves persona iteration ergonomics. Criticality is High impact and Medium urgency.

## User story
As a user creating and tuning personas, I want the persona editor split into distinct tabs (Identity & Brain, Voice & Audio, Appearance & Workflow, Traits & Dynamic Memory) with a persistent sticky save bar, so that I can configure complex persona attributes cleanly without massive vertical scrolling.

## Acceptance criteria
- [ ] Editor is organized into 4 navigable tabs:
  1. **Tab 1: Identity & Brain:** Name, avatar generator/upload, role (Character vs Narrator), system prompt, LLM provider/model selector, temperature, max tokens, thinking-enabled toggle.
  2. **Tab 2: Voice & Audio:** Voice engine selection (Piper, Kokoro, Fish), voice dropdown grouped by accent/gender, speed slider, live voice preview tester, reference audio file upload for Fish cloning.
  3. **Tab 3: Appearance & Workflow:** Appearance prompt, ComfyUI workflow template selector, reference images, negative prompts.
  4. **Tab 4: Traits & Dynamic Memory:** Trait radar visualization, trait evolution log, memory list with search, pinning, and attribution editor.
- [ ] Sticky save bar (`.savebar`) remains pinned at the top/bottom across all tab switches with dirty-state indicator (`● Unsaved changes`) and Discard / Save buttons.
- [ ] Keyboard shortcut `Ctrl+S` / `Cmd+S` saves changes from any active tab.
- [ ] Navigation dirty guard ([[BUG-06-persona-dirty-guard]]) remains fully intact when switching away from the personas route while dirty.
- [ ] Switching between tabs preserves form state and dirty tracking without prematurely saving or discarding.

## Implementation notes
- Refactor `apps/web/src/routes/personas/+page.svelte` by modularizing tab contents into subcomponents (e.g. `apps/web/src/lib/persona/TabIdentity.svelte`, `TabVoice.svelte`, `TabAppearance.svelte`, `TabTraits.svelte`).
- Preserve the existing `$derived` `dirty` check and SvelteKit `beforeNavigate` hook established in [[BUG-06-persona-dirty-guard]].
- Adhere strictly to Svelte 5 runes (`$state`, `$derived`, `$props`, `$bindable`).

## Non-goals
- Modifying backend SQLite schema for personas (all fields are already defined and supported).
- Removing or altering the existing persona list sidebar.

## Definition of done
- `npm run check` and `npm run typecheck` report 0 errors and 0 warnings.
- `npx vitest run` passes.
- Tab switching, editing across multiple tabs, dirty indicator, and Ctrl+S saving verified in a real browser.

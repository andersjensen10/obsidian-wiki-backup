---
tags: [project/agora, type/qa]
story: "[[FR-014-onboarding-quickstart-wizard]]"
related: ["[[FR-009-worlds-and-scenes-data-model — Part 1 of 2]]", "[[FR-010-worlds-and-scenes-ui — Part 2 of 2]]", "[[FR-011-narrator-pacing-intelligence]]", "[[FR-012-scene-media-and-library]]"]
date: 2026-09-10
author: Herm
status: report
---

# QA Dogfood Report — Character/World/Scene creation, post-FR-011/FR-012

## Why this pass happened

AJ reported errors surfacing in the Quick Start wizard and asked for a full
browser-based user test of both new and existing functionality, worried the
prior session's token-budget timeout had left a deeper problem than
expected. This was a live, real-browser exploratory QA pass (dogfood-style)
against the running app — not a re-read of code or a re-run of the existing
unit/live-check suites, though those were also re-run at the end to confirm
no regression.

## Scope tested

Real browser session (Chrome via CDP, `use_real_profile` had to be turned
off — see Environment note below) against the live dev server (`:7480` web,
`:7481` API/WS), live Spark LLM (`qwen3.8-27b-aggressive-q5`) and live Spark
ComfyUI:

- Quick Start wizard: full 4-step flow (name → vibe → model → scene),
  twice — once accepting the "connection default" model, once picking a
  connection but not a specific model (to reproduce AJ's reported error).
- World creation ("Create a world" button + naming dialog).
- Scene creation within a World ("Start a new scene" button + naming
  dialog), and switching between scenes in the sidebar.
- World & canon panel: setting/description edit, pacing dropdown (FR-011),
  save, and persistence.
- Checking a persona into a scene (membership checkbox).
- Live chat exchange against the Spark LLM in a wizard-created scene.
- Media Composer POV picker (FR-012): third-person vs. named-persona POV,
  a real generation against Spark ComfyUI, and retrieval from `/library`
  filtered by World and Scene.
- Full persona editor: confirmed wizard-set fields (name, system prompt,
  appearance prompt, connection, model) round-trip correctly.
- Legacy `/api/rooms` POST path (pre-World/Scene creation) still functions.

## Findings

### BUG-A (High) — Quick Start wizard does not navigate to the new scene

**Symptom:** Completing the wizard ("Create & start chatting") silently
stays on the Personas page in the full persona editor, on the
freshly-created persona. The story's own acceptance criterion is "lands the
user directly in the new room, ready to send a first message" — this did
not happen.

**Root cause:** `onQuickStartComplete` in
`apps/web/src/routes/personas/+page.svelte` created the persona/room via
the API and updated local persona-editor state, but never navigated
anywhere. The chat page (`/`, `apps/web/src/routes/+page.svelte`) has no
knowledge that a new room exists and no reason to select it.

**Verification the server-side create was fine:** `GET /api/rooms` and
`GET /api/worlds` both showed the new World/Scene/persona/membership
correctly persisted immediately after wizard completion — this was purely a
client-side navigation gap, not a data-integrity bug. The existing
`scripts/live-onboarding-check.mjs` (server-only, no browser) could not have
caught this, which is why it kept passing while the bug shipped.

**Fix applied:** `onQuickStartComplete` now stashes the new room id in
`sessionStorage` and calls `goto('/')`; the chat page's `onMount` checks for
that pending id first and calls the existing `loadWorld(id)` before falling
back to `worlds[0]`. Verified live: wizard finish now lands directly in the
new scene, composer ready, persona checked in.

### BUG-B (High) — persona created via wizard can be silently unusable

**Symptom (this is very likely what AJ was seeing as "wizard errors"):** In
step 3 ("Pick a brain"), picking an LLM connection but leaving "Model" on
"Connection default" produces a persona that fails on its very first
message with `"<name> has no model selected on connection \"Spark
(llama.cpp)\"."` — because the `Spark (llama.cpp)` connection's
`defaultModel` is `null` (`GET /api/connections` confirms this). The wizard
gives no warning at any step; the failure only surfaces once the user is
already in the new scene and has sent a message.

**Root cause:** `onPickConnection` in `QuickStartWizard.svelte` always
reset `data.model` to `null` ("connection default") after loading a
connection's model list, regardless of whether that connection actually has
a `defaultModel` configured server-side. A connection without one silently
produces a broken persona.

**Fix applied:** `onPickConnection` now checks the picked connection's
`defaultModel`; if it is unset, the first model in the connection's model
list is pre-selected instead of leaving "connection default" active. A
connection that DOES have a working default is untouched. Verified live:
picking "Spark (llama.cpp)" now auto-selects `qwen3.8-27b-aggressive-q5`,
and the resulting persona replies correctly on first message.

### Not a bug — false alarm during testing

While testing "Start a new scene," an initial attempt appeared to silently
no-op (the dialog closed but no second scene appeared). Re-tested with
proper `input`/`change` event dispatch on the name field (the modal's
Create button was still disabled on the first attempt because the typed
value hadn't been registered by Svelte's reactivity) — the second attempt
succeeded with a real `POST /api/worlds/:id/scenes` returning `201`, and the
new scene appeared correctly in the sidebar and via `GET`. No app-side fix
needed; this was a test-harness input-timing issue, logged here for the
record in case it resurfaces.

## Everything else checked and found working correctly

| Area | Result |
|---|---|
| World creation dialog + persistence | ✅ |
| Scene creation dialog + persistence (once input actually registers) | ✅ |
| World & canon panel: setting save | ✅ persists, round-trips via GET |
| Narrator pacing dropdown (FR-011) in World & canon panel | ✅ persists (`brisk` saved and read back) |
| Persona membership checkbox (check a persona into a scene) | ✅ |
| Live chat turn against Spark LLM in a wizard-created scene | ✅ real reply received |
| Media Composer POV picker (FR-012): third person vs. named persona | ✅ both options present and functional |
| POV image generation against live Spark ComfyUI | ✅ real 768×768 PNG generated and served |
| `/library` page World/Scene filter dropdowns | ✅ correctly scoped (Scene list narrows to selected World) |
| Generated image retrievable from library, correctly scoped | ✅ |
| Full persona editor shows wizard-set fields (name, system prompt, appearance prompt, connection, model) | ✅ all round-trip correctly |
| Legacy `POST /api/rooms` (pre-Worlds/Scenes path) | ✅ still works unchanged |
| Browser console errors across the whole session | ✅ none captured (window `error`/`unhandledrejection`/`console.error` hooked for the entire pass) |

No evidence of a deeper impact from the earlier token-budget timeout beyond
the two wizard bugs above — FR-009/FR-010/FR-011/FR-012's own live-check
scripts continued to pass, and this session's from-scratch browser pass
against real data (existing Worlds/Scenes from prior sessions, not just
fresh QA rows) did not surface any other broken surface in World/Scene/
persona creation.

## Verification after fix

```
npm run check -w @agora/web  → svelte-check found 0 errors and 0 warnings
npm run verify                → Test Files 24 passed (24) / Tests 285 passed (285)
node scripts/live-onboarding-check.mjs → 24/24 checks passed
```

Both fixes additionally verified live in a real browser session (see BUG-A
and BUG-B sections above) — wizard finish now lands in the new scene, and a
connection-default persona now gets a real model and replies successfully
on first message.

## Environment note

`browser.use_real_profile` was `true` but the desktop's default browser was
Firefox, and after switching the OS default to Chrome, the real Chrome
profile's login-data DB was locked/unavailable — both blocked the browser
tool outright. Set `browser.use_real_profile: false` via `hermes config set
browser.use_real_profile false` to unblock (this uses an isolated harness
profile instead of the real Chrome profile; fine for testing a local
non-authenticated app like Agora). Left this setting changed since it is
what allowed testing to proceed at all — flag to AJ if he wants it back to
`true` for other use cases that need real-profile cookies/logins.

## Files changed

- `apps/web/src/routes/personas/+page.svelte` — `onQuickStartComplete` now
  navigates to `/` with a pending-room handoff via `sessionStorage`.
- `apps/web/src/routes/+page.svelte` — `onMount` checks for and consumes
  that pending room id before defaulting to `worlds[0]`.
- `apps/web/src/lib/onboarding/QuickStartWizard.svelte` —
  `onPickConnection` pre-selects a real model when the chosen connection has
  no `defaultModel`, instead of leaving a silently-broken "connection
  default" selected.

Commit: see `AgenticChatroomProject` git log, "QA: fix Quick Start wizard
navigation + silent broken-model bug (dogfood pass)".

## Related notes
- [[FR-014-onboarding-quickstart-wizard]] — the story this QA pass audited (status unchanged, already `shipped`; this report documents a post-ship regression-hunt and fix, not a re-scoring of the original story).
- [[FR-011-narrator-pacing-intelligence]] — pacing dropdown verified working in this pass.
- [[FR-012-scene-media-and-library]] — POV picker + library verified working in this pass.
- [[Agentic Chatroom]] — project status snapshot.

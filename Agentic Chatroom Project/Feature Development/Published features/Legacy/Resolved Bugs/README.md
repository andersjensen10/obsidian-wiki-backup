---
tags: [project/agora, type/readme, type/resolved-bug]
---

# Resolved Bugs — Agora QA Report (2026-09-06)

This folder documents the resolution of every issue in `../bug_report.md`
(the automated QA sweep of the Agora prototype). All 12 are fixed.

## Status at a glance

| ID | Severity | Title | Fixed in | Verified by |
|---|---|---|---|---|
| BUG-01 | High | Misleading `· replying: <persona>` when idle | `10db5e6` | `+page.svelte` status line |
| BUG-02 | High | "On mention" replied with no mention | `10db5e6` | `strictmention.test.ts`, `live-bugfix-check.mjs` |
| BUG-03 | High | Mobile sidebar hard-hidden, no drawer | this pass | `svelte-check`, browser |
| BUG-04 | Medium | Blocking native `prompt()`/`confirm()` | `10db5e6` | `dialog.ts` + `Modal`/`ConfirmDialog` |
| BUG-05 | Medium | TTS failures silent | `10db5e6` | `speech.ts` `toast.fail` |
| BUG-06 | Medium | Persona editor lost edits on nav | `10db5e6` | `beforeNavigate` guard |
| BUG-07 | Medium | Image messages spoke the diffusion prompt | this pass | `canSpeak()` + media caption |
| BUG-08 | Medium | Save button buried below a huge form | `10db5e6` | sticky `.savebar` |
| BUG-09 | Medium | Abort dropped socket, leaked GPU job | `10db5e6` | in-band cancel + `/interrupt` |
| BUG-10 | Low | `skill_used` events had no UI | this pass | `SkillTrace.svelte` |
| BUG-11 | Low | Images opened as raw browser tabs | this pass | `MediaLightbox.svelte` |
| BUG-12 | Low | Regeneration destroyed downstream history | this pass | `handleRegenerate` + variant switcher |

"this pass" = the front-end wiring that landed on 2026-09-06 after the
`10db5e6` commit (BUG-03/07/10/11 were UI-only; BUG-12 needed the client
rewritten to use the non-destructive path the backend already exposed).

## Verification

- **Static:** `npm run typecheck` (server + all packages), `npm run check`
  (svelte-check, 0 errors/0 warnings), `npx vitest run` (229 tests pass).
- **Live (requires the Spark LLM + a running server):**
  `node scripts/live-bugfix-check.mjs` covers BUG-02, BUG-09, and BUG-12
  end-to-end, including the WebSocket regeneration path.

Per-bug detail is in the numbered files in this folder: [[BUG-01-idle-status]],
[[BUG-02-strict-mention]], [[BUG-03-mobile-drawer]], [[BUG-04-modal-dialogs]],
[[BUG-05-tts-error-feedback]], [[BUG-06-persona-dirty-guard]],
[[BUG-07-image-tts-caption]], [[BUG-08-sticky-savebar]],
[[BUG-09-inband-cancel-gpu]], [[BUG-10-skill-trace-ui]],
[[BUG-11-media-lightbox]], [[BUG-12-nondestructive-regeneration]].

## Related notes
- [[Agentic Chatroom]] — project status snapshot, links back to this pass.

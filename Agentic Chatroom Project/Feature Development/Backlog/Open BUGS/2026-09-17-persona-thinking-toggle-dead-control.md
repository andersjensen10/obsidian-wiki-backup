---
found_by: Herm
found: 2026-09-17
context: spark-throughput-investigation
severity_hint: minor
related_release: "[[FR-018-guided-narrator-agency-and-persistent-npcs]]"
---

> [!warning] Dead control — "Thinking / Chain-of-Thought" toggle in Persona setup does nothing
> The per-persona "Thinking / Chain-of-Thought" toggle in the Personas editor
> is not wired to anything: its value is never saved to the persona and never
> read by the server. Reasoning mode is governed solely by the server-wide
> `config.thinkingEnabled` (`AGORA_THINKING`, default false). The switch
> silently misleads — flipping it "Enabled" has zero effect on generation.

# Persona "Thinking enabled" toggle is a no-op (not persisted, not read server-side)

## What happened
While investigating an unrelated Spark throughput problem (which turned out to
be a wedged NVIDIA MPS forcing the model onto CPU — **not** an Agora bug),
the per-persona "Thinking / Chain-of-Thought" toggle was examined as a
suspect and found to be a dead control end-to-end.

## Evidence (three independent breaks in the chain)
1. **UI state is local-only.** In `apps/web/src/routes/personas/+page.svelte`
   the toggle is `let thinkingEnabled = $state(false)` (line ~69),
   `bind:thinkingEnabled` on `<TabIdentity>` (line ~502). The save path
   (`updatePersona`, lines ~342–349) sends only
   `name / systemPrompt / traits / temperature / maxTokens / …` — it **never
   includes `thinkingEnabled`** in the request body. So the value cannot leave
   the browser.
2. **Schema has no field.** `packages/shared/src/persona.ts` — neither
   `personaSchema` nor `personaInputSchema` defines a thinking/`thinkingEnabled`
   field, so even if the client sent it, it would be dropped on validation.
3. **Server never reads a per-persona value.** `apps/server/src/chat/engine.ts`
   resolves `const thinking = opts.thinking ?? config.thinkingEnabled;` — the
   only source is the server-wide config default (`AGORA_THINKING`, default
   `false` per `apps/server/src/config.ts`). No `persona.thinkingEnabled` is
   ever consulted. `ws.ts` only ever passes `thinking: false` (the empty-reply
   retry). Nothing maps a persona's toggle to `opts.thinking`.

Net effect: the toggle renders and flips visually, but reasoning mode is
identical regardless of its position.

## Steps to reproduce
1. Open a persona in the Personas editor; flip "Thinking / Chain-of-Thought" to
   Enabled; save.
2. Reload — the toggle returns to Off (nothing was persisted).
3. Even within a session while it shows "Enabled", generated turns run with the
   server-wide default (thinking off unless `AGORA_THINKING=true`), confirmable
   by the absence of `reasoning_content` growth / no latency change.

## Suspected severity & why
Minor (not a correctness/data bug, no crash), but a **trust/UX** bug: it's a
visible switch that claims per-persona control and delivers none. It matters
more now that thinking-mode has a large, measured cost (~5× tokens/turn on the
Spark reasoning model) — a user reasonably expects to enable deep reasoning for
one "thinker" persona and leave others fast, and today cannot.

## Suggested fix direction (not prescriptive)
Wire it through OR remove it. To make it real:
- Add `thinkingEnabled: z.boolean().optional()` to `personaSchema` +
  `personaInputSchema` (+ DB column / migration).
- Include it in the Personas save payload and load it back into the editor.
- In `ws.ts`/engine, resolve `thinking` as
  `opts.thinking ?? persona.thinkingEnabled ?? config.thinkingEnabled` so the
  per-persona value overrides the server default but the empty-reply retry
  (`thinking:false`) still wins.
Whichever way, keep the empty-reply retry forcing `thinking:false`.

## Reference
- UI: `apps/web/src/routes/personas/+page.svelte`,
  `apps/web/src/lib/persona/TabIdentity.svelte`.
- Schema: `packages/shared/src/persona.ts`.
- Server: `apps/server/src/chat/engine.ts` (line ~297),
  `apps/server/src/config.ts` (line ~56), `apps/server/src/routes/ws.ts`.
- Thinking-mode cost/behaviour: commit `366e7b1`
  ("Default personas to thinking-off for ~5x fewer tokens per turn").
- Session context: [[Session Log 2026-09-17 — Spark MPS Wedge Incident]].

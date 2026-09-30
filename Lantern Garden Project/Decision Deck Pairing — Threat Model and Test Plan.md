---
tags: [type/security, lantern-garden, decision-deck, pairing, threat-model, home-lan]
created: 2026-09-30
owner: Winbot (design, implementation, tests) / Herm (review, deploy, server env)
status: deployed by Herm to live Lenovo dashboard; wall pairing still requires AJ action and live wall read-back
---

# Decision Deck pairing: threat model and test plan

Requested by Herm (Townhall `3e7d8029`): no root-only token file, no secret in a QR, URL, browser storage, logs, Townhall or the UI; ephemeral pairing session, same-LAN, short-lived, one-time exchange, `HttpOnly`/`SameSite` cookie; fail closed; expiry, revocation, replay protection and audit without secret material; schema alignment first. Branch `winbot/decision-deck`, commits `cb9b19a` (schema) and `bf6d4a5` (pairing). Companion: [[Lantern Garden Project/Decision Deck — Concept and Plan]].

## 1. What is protected
Only AJ can create a label. An answer written to `answers.jsonl` must come from a screen AJ approved. Agents, other LAN devices and guests must not be able to answer, nor read a secret that lets them.

## 2. Design (as built)
1. **No shared secret exists.** Removed `DECISIONS_ANSWER_TOKEN`, the `x-decisions-token` header and the `?pair=` URL. The old header now returns 401 (tested).
2. An unpaired screen calls `POST /api/decisions/pair/start` (LAN addresses only, rate limited) and displays a **6-character code** (alphabet without 0/O/1/I/L). It also receives a `pollSecret` kept **only in that page's memory**.
3. **Approval** needs the code AJ reads off the wall plus one of: a request from the dashboard host itself (**loopback**: AJ at the Lenovo or via remote desktop), or a session that is **already paired** (AJ's phone). A remote unpaired device cannot approve.
4. On approval the server mints a 256-bit random token. Only its **SHA-256 hash** is stored. The raw token is held **in server memory** for at most 60 s and released **once** to the page that presents the `pollSecret`, as an **`HttpOnly`, `SameSite=Strict`** cookie (`Secure` when served over https). It is never in a response body, URL, localStorage or disk.
5. `POST /api/decisions/:id/answer` requires that cookie **and** a same-origin `Origin` header (CSRF). No cookie, no answer: fail closed. Agents hold no cookie.
6. Sessions last 30 days, can be revoked (`DELETE /api/decisions/session`) and are listed without secrets. Every step is written to `pairing-audit.jsonl` (start, approve, pickup, revoke, expiry, lockout, refusals) with **no** secret fields.

## 3. Threats and mitigations
| # | Threat | Mitigation | Test |
|---|---|---|---|
| T1 | Agent or LAN device tries to answer | needs paired-session cookie; header token removed | `unpaired_answer_status` 401, legacy header 401 (e2e) |
| T2 | Someone photographs the wall code and pairs their own device | Code alone is useless: approval still needs host/paired screen, and pickup needs the initiating page's in-memory `pollSecret` | unit "pickup needs the pollSecret" |
| T3 | Brute-forcing the code (31^6 space, 2-minute life) | 5 wrong codes lock approvals for 5 minutes; max 3 pending codes; 10 s start cooldown per address | unit "brute force", "start is refused... rate limited" |
| T4 | Remote pairing from the internet / Tailscale-only node | start refused for non-private addresses; approve needs loopback or paired session | unit "address classification" |
| T5 | Token theft from disk, logs, Townhall, vault | only hashes on disk; token in memory 60 s; audit filters secret-like fields; secrets never shown | unit "no secret material on disk"; e2e disk scan: only sha256 hashes found |
| T6 | Token theft by page script (XSS) | `HttpOnly`; page JS cannot read the cookie | e2e `cookie_not_readable_by_js`, `cookie_httponly_strict` |
| T7 | CSRF: another site makes AJ's browser answer | `SameSite=Strict` + same-origin `Origin` check on answer, approve, revoke | e2e cross-origin 403, no-Origin 403, approve cross-origin 403 |
| T8 | Replay of a pickup | token released exactly once; consumed pairing removed | unit happy path (second pickup `unknown`) |
| T9 | Stale or forgotten screens | 30-day expiry, revocation, listing (no secrets), audit | unit "sessions expire, revoke..." |
| T10 | Restart while pairing | held tokens are memory-only: pairing simply retried; existing sessions survive (hashes on disk) | by design; noted |
| T11 | Timing side channels | constant-time compares over SHA-256 digests | code review |
| T12 | Someone on the LAN starts many pairings to spam the wall | pending cap 3, cooldown, codes expire in 2 minutes | unit |

## 4. Residual risks (stated, not hidden)
- **Anyone at the Lenovo (loopback) can approve.** Acceptable in this home; it matches "AJ at the host". Tighten later with a physical confirmation if needed.
- **A paired phone that is lost** keeps working until revoked. Mitigation: revoke from any paired screen; expiry 30 days.
- **Plain http on the LAN**: the cookie is not `Secure` and traffic is sniffable on the LAN. Same as the rest of the dashboard today. Recommend https or Tailscale later.
- **The pairing state is a JSON file** under `data/decisions/` (gitignored, mode 600 written); a compromised dashboard user could write a session. That user already owns the whole dashboard.
- Multi-process deployment would need a shared memory store for the held tokens (single process today).

## 5. Deployment steps for Herm (no secrets, no env token)
1. Cherry-pick `cb9b19a` and `bf6d4a5`. `DECISIONS_ANSWER_TOKEN` is no longer read.
2. Restart. The wall shows the pairing box; AJ presses **Pair this screen** on the projector browser, then types the code shown into any of: the Lenovo's own browser (`/decisions` -> **Approve a screen**), or later a paired phone.
3. Read back `/api/decisions/session` on the wall (`paired: true`) and confirm `pairing-audit.jsonl` has start/approve/pickup with no secret fields.

## 6. Verification evidence
- 12 pairing unit tests, 15 decision tests, `svelte-check` 0 errors, full suite 129/130 (the one failure is the existing townhall-mcp test needing a skill file only on Herm's host).
- End-to-end on an isolated preview port with a throwaway Chrome profile: code shown and readable (screenshot `assets/pairing-code.png`), unpaired UI answer refused with a clear message, host approval pairs the screen, cookie `HttpOnly` + `SameSite=Strict`, no token in storage or URL, answer recorded, cross-origin refused, revoke works, disk scan shows only sha256 hashes.

## Update 2026-09-30 14:03 (Winbot)
- Herm deployed cookie pairing (`f4314d4`, `d28cde3`, `d9925d1`, harness `cb79b5d`); live `/api/decisions/session` returns `paired:false`. Trusted-screen approval (`2bc04e4`) is **not** deployed; Herm's scheduled monitor cannot verify the wall address or service environment.
- **Correction:** the MSI wall host's address is **192.168.0.103** (Wi-Fi, DHCP), measured as the source address the dashboard sees. The `192.168.0.30` in earlier notes and in my first handoff was stale. A trusted address that changes silently stops matching and pairing falls back to the code flow (fail closed). Recommendation: DHCP reservation for the MSI.

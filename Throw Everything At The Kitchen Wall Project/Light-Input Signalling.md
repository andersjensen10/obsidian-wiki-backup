# Light-Input Signalling

**Status:** Implemented and verified against real hardware, 2026-09-14
**Owner:** Herm
**Repo:** `~/Desktop/Hermes/kitchen-dashboard`
**Contract doc:** `LIGHT-SIGNALS.md` in the repo
**Related:** [[A projector in the kitchen, a living dashboard and interactive playground]]; [[Kitchen Wall Readiness — NUC and Projector 2026-09-16]]; [[Agentic Chatroom Project/Townhall Onboarding]]

## What this is

A way for an agent to get AJ's attention physically, by briefly blinking the living-room smart plug, when something needs a human and a dashboard notification is not enough. It is deliberately narrow: signals are opt-in, explicitly armed, rate-limited, cancellable, fully audited, and **dry-run by default**.

It is not a notification channel and not a replacement for the Attention Center. The light says "come look"; the Attention record is what holds the actual request and its acknowledgement lifecycle.

## Signal types and patterns

AJ verified by eye on 2026-09-14 that all four are easily distinguishable at 450 ms pulse/gap:

| Type | Pulses | Meaning |
|---|---|---|
| `complete` | 1 | Long-running work finished |
| `attention` | 2 | Something wants a look, not blocking |
| `input-needed` | 3 | Blocked, waiting on an AJ decision |
| `error` | 4 | Failure that needs intervention |

A pulse inverts the plug and restores it. If the light is **on**, it flicks off and back; if **off**, it flashes on and back. Measured wall times: 1 pulse 481 ms, 2 pulses 1.41 s, 3 pulses 2.32 s, 4 pulses 3.24 s.

## Safety design

Four independent properties, each covered by tests:

1. **Dry-run by default.** Nothing reaches hardware unless three environment variables *all* agree. Any one missing leaves the subsystem logging only. Partial configuration cannot half-arm the plug.
2. **Never blinks blind.** The action reads the plug's current state first and refuses if it reports `unknown`, because a signal it cannot undo would leave the light in the wrong state.
3. **Always restores.** Abort or mid-pattern failure still returns the plug to the state it was found in.
4. **Rate-limited and serialised.** One signal per 30 s; concurrent requests queue rather than interleave. A debounced request is still logged as `rate-limited`, so spam is visible rather than silently dropped.

Manual plug control (`setPlugState`, `POST /api/plugs/[id]`) is a separate path and is unchanged by this subsystem.

## Arming

```sh
KITCHEN_LIGHT_SIGNAL_ARMED=true
KITCHEN_LIGHT_SIGNAL_HARDWARE=true
KITCHEN_LIGHT_SIGNAL_CONFIRM=I_CONFIRM_KITCHEN_LIGHT_SIGNAL
```

Arming is per-process and intentionally not persisted in any service unit yet. The dashboard as normally run is **disarmed**.

## HTTP interface

`POST /api/signals` with `{ type, requester, reason, requestedAction?, correlationId? }`:

- `202` — accepted; body is the audit record (`simulated` when disarmed, `success` when armed)
- `429` — rate-limited; still logged
- `400` — unknown type, missing field, or malformed JSON

There is no `GET`. The audit log is a server-side JSONL file at `data/attention/light-signals.jsonl` (gitignored), one object per line with timestamp, type, requester, reason, requested action, result, and correlation ID.

## How agents should use it

Pair every signal with a durable Attention record and share a correlation ID between them. The light is a doorbell; the Attention record is the message. Do not signal routine progress, successful health checks, or anything that can wait for the next time AJ looks at the dashboard.

## Verification performed

- 18 unit tests across core, action, and service; 130/130 project tests pass; `svelte-check` clean.
- Dry-run E2E against a live server: plug read `relay_state=0` before and after, untouched.
- **Armed E2E against the real Kasa plug at 192.168.0.176**: all four patterns driven directly and restored correctly; one `input-needed` delivered through the armed HTTP endpoint returning `result: success`; an immediate repeat correctly returned `429` and did not blink. Final plug state matched the starting state.
- AJ confirmed the patterns are distinguishable by eye.

## Open follow-ups

- Attention Center linking: nothing yet creates an Attention record from a signal, so the correlation ID is currently convention rather than enforced.
- The projector's own smart plug is not registered in `PLUGS`; only `living-room` exists. Revisit after the 2026-09-16 installation.
- Arming is not wired into any systemd unit. Decide after the wall is up whether the running dashboard should be armed permanently.
- Off-state behaviour was accepted as-is, but flashing a dark room is more intrusive than dimming a lit one; revisit if it proves annoying at night.

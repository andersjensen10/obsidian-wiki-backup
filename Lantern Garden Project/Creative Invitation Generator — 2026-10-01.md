---
tags: [lantern-garden, prototype, read-only, home-lan]
created: 2026-10-01
owner: Winbot
status: prototype-verified
---

# Creative Invitation Generator — dry-run prototype (2026-10-01)

Follow-up to [[Read-only capability map — 2026-09-29]], which proposed "a dry-run generator that reads Townhall + documented service health and emits a creative invitation bundle."

## Artifact
`Lantern Garden Project/assets/creative_invitation.py` (stdlib only, stdout only).

## Tested (2026-10-01 03:32 +02:00, from the MSI)
- GET-only, 4 s timeout, 2 MB read cap. Six routes: llama.cpp :8014, ComfyUI :8188, Voice Lab :8090, Agora :7480, Axiom :8081, dashboard :5173 — **all HTTP 200** (19–228 ms).
- Dashboard `/api/townhall?limit=100`: 100 posts parsed — winbot 67, herm 25, sparkbot 8. Top tags: lantern-garden 64, verification 59, attention 41, evaluation 23, autonomy 21.
- `/api/attention`: 1 open item. 

## Defect found and fixed
`/api/attention` response exceeds 200 KB; the first version truncated it and crashed with JSONDecodeError. Cap raised to 2 MB, parse failure now non-fatal (`open_attention: "unparseable"`). Lesson: the Attention payload is large — a dashboard-side `?status=open` filter would be worth requesting from Herm.

## Limitations
Invitation text is template-based (not LLM). Does not touch Display 2 — no wall success claimed. Axiom was tested only for shell reachability.

## Rollback / side effects
No writes to any service, no credentials, no device control, no Spark compute. Delete the script to roll back.

## Invitation for AJ
Pick one: should the bundle become a read-only card on a wall route (Herm owns dashboard), or be piped through Spark for a written "morning note"? Non-blocking.

Townhall: see Winbot finding of 2026-10-01 in project home-lan.

---
tags: [lantern-garden, capability-map, read-only, home-lan]
created: 2026-09-29
owner: Winbot
---

# Lantern Garden — Read-only capability map (2026-09-29)

## Mission

Create one bounded, read-only map of useful connections among already documented LAN services. No production service, device, projector, or code was changed.

## Verified probe evidence

All probes originated from the Hermes laptop at 2026-09-29T23:11:32+02:00, with a 4-second timeout and bounded response reads (500 bytes max).

| Capability | Endpoint | Result | Evidence |
|---|---|---:|---|
| Local LLM / reasoning | `http://192.168.0.139:8014/v1/models` | HTTP 200 | OpenAI-compatible JSON; live model currently identified as `qwen3.6-35b-a3b-heretic-apex-i-quality` |
| ComfyUI media generation | `http://192.168.0.139:8188/system_stats` | HTTP 200 | JSON system stats; ComfyUI `0.37.0`; response included host memory counters |
| Fish Speech service surface | `http://192.168.0.139:8080/docs` | HTTP 404 | The documented port is reachable, but `/docs` is not the correct route; no mutation attempted and service availability is not inferred from this route alone |
| Voice Lab backend | `http://192.168.0.139:8090/docs` | HTTP 200 | FastAPI docs HTML returned |
| Agora chatroom | `http://192.168.0.148:7480/api/health` | HTTP 200 | `status=ok`, `app=agora`, `version=0.1.0` |
| Axiom Engine creative surface | `http://192.168.0.26:8081/` | HTTP 200 | HTML application shell returned |

## Useful connection

**Townhall + live fleet + local generation form a read-only “research-to-invitation” path:**

1. Townhall supplies the current mission, constraints, and agent evidence.
2. The Lantern dashboard can present that evidence alongside fleet state without controlling devices.
3. Agora provides the interactive narrative surface; Spark's llama.cpp supplies local reasoning and ComfyUI supplies optional media generation.
4. Axiom Engine is a separate live creative surface that can be treated as a candidate downstream destination, but no integration or write path was tested here.

This suggests the next safe prototype: a dry-run generator that reads Townhall + documented service health, emits a Markdown/JSON “creative invitation” bundle, and leaves all downstream presentation and generation opt-in.

## What was tested

- Six documented LAN HTTP routes were probed read-only.
- Three routes returned HTTP 200 with the expected broad surface (JSON health/model/system data or an application shell), one returned documented FastAPI docs HTML, and one route mismatch returned HTTP 404.
- No POST, PUT, PATCH, DELETE, shell-exec, device-control, projector navigation, or queue submission was performed.

## Limitations

- HTTP 200 proves reachability and a broad application surface, not full authentication, semantic correctness, or end-to-end generation.
- The Fish Speech route needs its documented API path identified before it can be included as a verified callable edge.
- No Display 2/projector verification was attempted, by design.
- Axiom's page is only an application-shell check; no API contract was inferred.

## Rollback / side effects

No rollback is required. This run only performed bounded GET requests and wrote this vault note. No LAN service, device, production code, model queue, or projector state was altered.

## Next invitation for AJ

Choose whether the next dry-run bundle should target (a) a Lantern dashboard briefing, (b) an Agora narrative seed, or (c) an Axiom Engine sketch prompt. The safe default is (a), because it stays read-only and requires no new service contract.

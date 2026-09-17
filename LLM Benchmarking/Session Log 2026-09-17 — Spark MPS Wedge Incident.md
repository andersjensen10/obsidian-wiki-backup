---
tags: [incident, spark-infra, mps, cuda, llama-server, benchmarking, agora, session-log]
date: 2026-09-17
severity: high
status: resolved
related: ["[[MPS Wedge Detection and Auto-Recovery Plan]]", "[[Automation Reliability Runbook]]"]
---

# Session log — Spark MPS wedge incident + Agora thinking-toggle finding (2026-09-17)

## Summary

AJ reported Agora was slow. Root cause: the Spark's NVIDIA **MPS** daemon
wedged during the previous night's benchmark and forced the production LLM onto
CPU (~8× slowdown) while every surface-level health check reported "healthy."
Fixed by resetting MPS + restarting llama-server. Separately confirmed the Agora
Personas "Thinking enabled" toggle is a dead control (a real but unrelated bug).

## Timeline

- **09-16 18:58** — nightly benchmark starts; MPS server (PID 17002) enters
  `Server teardown in progress` and never recovers.
- **09-16 18:59** — llama-server.service restarts (inside the benchmark window);
  CUDA init fails against the wedged MPS → loads 27B model **on CPU**.
- **09-16 → 09-17** — MPS rejects every CUDA client with `status 807`
  (llama-server, ComfyUI, fish-speech all affected).
- **09-17 morning** — AJ reports slow Agora throughput. Herm investigates.
- **09-17 ~08:5x** — root cause identified, MPS reset, llama-server restarted,
  fix verified. Townhall `spark-infra` posts: question `7b2a2436`, resolution
  `5916ce91`.

## Root cause (definitive)

`/tmp/nvidia-log/server.log` showed MPS server 17002 stuck in
`Server teardown in progress`, refusing all new clients with `status 807` from
18:58 onward. llama-server's load log:

```
E ggml_cuda_init: failed to initialize CUDA: MPS server is not ready to accept new MPS client requests
warning: no usable GPU found, --gpu-layers option will be ignored
```

The model therefore ran entirely on CPU. GPU util stayed 6 %/14 W even during
generation.

## Key lessons (the reason this was hard to spot)

1. **`/health` 200 ≠ GPU-backed.** A wedged MPS leaves the port answering, the
   model alias unchanged, and the process argv unchanged — the model just
   silently runs on CPU. Health/alias/argv checks CANNOT detect this.
2. **Signature = a FIXED per-request latency floor** that does not scale with
   output length (e.g. ~3.9 s for a 2-token reply). That's per-request CUDA/
   setup overhead on CPU, not normal generation slowness.
3. **A llama-server restart does NOT fix it** (proven twice) — MPS lives
   outside the service. Must reset MPS itself.
4. **The only reliable live signals** are (a) llama-server's load log
   (`no usable GPU found`), and (b) GPU utilisation / token throughput during a
   real request. Both are now baked into `gpu_backing_probe.py`.
5. **Stale log lines mislead** — old CUDA-failure lines persist across boots;
   always check journald timestamps.
6. **Blast radius = every CUDA service on the box.** ComfyUI and fish-speech
   were hit too; a wedged MPS poisons them all until cleared.

## Measured before/after

| metric | broken (CPU) | fixed (GPU) |
|---|---|---|
| small-reply latency | ~3.9 s (flat) | ~0.30 s |
| prompt processing | 6.8 tok/s | 95.6 tok/s |
| generation | 2.7 tok/s | 17.9 tok/s |
| GPU util during gen | 6 % | 95 % |

## Fix applied

```bash
ssh spark 'echo quit | timeout 8 nvidia-cuda-mps-control;   # hung/124, ok
  pkill -f nvidia-cuda-mps-server; pkill -f nvidia-cuda-mps-control; sleep 2
  rm -rf /tmp/nvidia-mps/* /tmp/nvidia-log/*; nvidia-cuda-mps-control -d'
ssh spark 'systemctl --user restart llama-server.service'
```
No config change (env file untouched; still 2 slots, same model + FastMTP
spec-decode stack). `compute_mode` was `Default`, so the reset was safe.

## Follow-ups produced this session

- **Detection + recovery tooling** deployed to `~/llm-benchmark-runner/` on the
  Spark: `gpu_backing_probe.py` (read-only, verified exit 0 on healthy box) and
  `mps_recover.py` (dry-run by default, `--confirm`-gated, self-verifying).
- **Integration plan** for the benchmark routine:
  [[MPS Wedge Detection and Auto-Recovery Plan]] (awaiting AJ's decisions on
  auto-recover vs page-only, and adding MPS teardown to the harness).
- **Home-lab skill** updated with the full MPS-wedge diagnosis + fix
  (`home-lab-infrastructure/references/reasoning-model-app-integration.md`).

## Secondary finding — Agora "Thinking enabled" toggle is a dead control

While investigating (initially suspecting the toggle), confirmed it's a
separate, unrelated bug: the Personas UI toggle is bound to a local
`$state(false)` in `apps/web/src/routes/personas/+page.svelte` that is **never
sent** in the create/update payload (lines 342–349 omit it), the persona schema
(`packages/shared/src/persona.ts`) has **no** thinking field, and the server
engine reads only `config.thinkingEnabled` (env `AGORA_THINKING`, default
false). So the switch does nothing. It did NOT cause the slowness. Filed as an
Agora sprint bug: `Open BUGS/2026-09-17-persona-thinking-toggle-dead-control.md`.

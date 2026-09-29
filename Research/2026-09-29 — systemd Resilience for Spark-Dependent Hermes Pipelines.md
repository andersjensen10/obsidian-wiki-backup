---
tags: [type/research, topic/hermes, topic/home-lab, topic/inference, topic/tts]
---

# Research Scout — systemd Resilience for Spark-Dependent Hermes Pipelines

**Run date:** 2026-09-29 08:00 CEST  
**Selection basis:** relevance to AJ’s active Hermes/local-AI stack, primary-source availability, practical usefulness, novelty, and non-repetition with the 2026-09-15 through 2026-09-28 reports.

## Three candidate topics

1. **A bounded systemd resilience design for Spark-dependent Hermes inference and voice services — selected.** This targets the operational gap left by the recent protocol research: the previous reports proposed MCP Tasks/A2A boundaries, but did not measure or harden the local services that those boundaries would depend on. Official systemd documentation covers restart policy, start-rate limiting, watchdog notifications, and cgroup resource controls.[2][3][4] AJ’s current machine also has live user services for Hermes Gateway and the Fish TTS Bench dashboard, making this immediately testable.
2. **llama.cpp server observability and queue admission for Spark.** The current server documentation exposes health, slot state, Prometheus metrics, deferred-request counts, and continuous-batching/parallel-slot controls.[1] This is useful, but it overlaps the 2026-09-15 local-inference and 2026-09-24 speculative-decoding reports; it should be a follow-up measurement rather than another documentation-only report.
3. **micro-ROS transport choices for a small home robot with local-agent supervision.** This would connect the 2026-09-19 ROS 2 report to a concrete electronics architecture: MCU-side control, agent-side planning, and bounded network failure behavior. It is novel and evidence-rich, but less immediately actionable than hardening the services AJ is already running.

## Decision

The selected topic is **how to turn systemd into a bounded failure-containment layer for Hermes Gateway, the Fish TTS dashboard, and future Spark/voice-preparation services without pretending that process restart equals service health**.

## Executive finding

The existing user units already provide a useful baseline: `hermes-gateway.service` is enabled and active with `Restart=always`, `RestartSec=5`, a 70-second stop timeout, and explicit exit-status handling; `fish-tts-bench.service` is enabled and active with `Restart=on-failure` and `RestartSec=5`. These are local observations from the live machine, not claims about systemd defaults.

The main gap is that process supervision and dependency health are not the same thing.[2][4]

A service can remain running while its upstream model or voice backend is unavailable, while a backend can be reachable but overloaded.[unverified]

The next hardening step should therefore combine: (1) process restart policy, (2) a meaningful readiness/health signal, (3) bounded resource controls, and (4) metrics/log evidence that distinguishes restart, dependency failure, queueing, and overload.[2][3]

For llama.cpp specifically, the server exposes a public health endpoint that returns HTTP 503 while the model is loading and HTTP 200 with `{"status":"ok"}` when ready.[1] Its slot endpoint can report per-slot state and can return HTTP 503 when no slot is available if `fail_on_no_slot=1` is used.[1] The server also exposes Prometheus metrics when enabled, including processing requests, deferred requests, throughput, busy slots, and speculative-decoding counters.[1] This makes a small health/metrics sidecar or gateway check feasible without scraping logs.

**Recommendation:** do not add automatic restarts or watchdogs blindly. First define a three-state contract for each service: **process alive**, **dependency ready**, and **admission available**. Restart only on process failure or a bounded watchdog failure; report dependency failure and admission saturation distinctly so the system does not enter a restart storm while Spark is merely offline or full.

## Sourced facts

### systemd restart and watchdog primitives

The systemd service manual describes `Restart=on-failure` as the recommended setting for long-running services when automatic recovery from errors is desired.[2] `Restart=always` is broader: it also restarts after a clean exit, so it is appropriate only when an intentional clean exit should not be treated as a terminal state.[2]

systemd supports restart backoff through `RestartSec=`, `RestartSteps=`, and `RestartMaxDelaySec=`.[2] The manual gives exponential restart intervals as a way to avoid immediate repeated restarts, which is relevant when a dependent service or network path is unavailable.

Start-rate limiting is configured through `StartLimitIntervalSec=` and `StartLimitBurst=` at the unit level.[2] A resilience design should set these deliberately and test the resulting failure mode; an unbounded `Restart=always` policy without a start-limit decision can conceal a persistent configuration or dependency problem.

A service watchdog is enabled with `WatchdogSec=` and serviced by periodic `WATCHDOG=1` notifications.[2][4] The `sd_notify` documentation describes `WATCHDOG=1` as the keep-alive ping used when the service manager’s watchdog is enabled.[4] This is stronger than checking that a PID exists, but it requires the application to emit the notification only when its event loop is genuinely making progress.

`READY=1` is meaningful for units using `Type=notify` or `Type=notify-reload`.[4] Readiness should therefore be reserved for the service’s actual startup contract, not emitted merely because the process has opened a socket.

### resource containment

systemd’s resource-control interface maps service settings to cgroup controllers. `MemoryMax=` limits memory usage, `CPUQuota=` assigns a maximum CPU time quota, and `TasksMax=` limits the number of tasks in the unit.[3] These controls are useful guardrails for Node/Python wrappers and media workers, but they must be sized from measurements; an arbitrary low limit can turn ordinary model loading or audio processing into self-inflicted failure.

### llama.cpp signals relevant to admission control

The llama.cpp server documents `--parallel` as the number of server slots and continuous batching as enabled by default unless disabled.[1] The `/slots` endpoint reports slot processing state and can be configured to return 503 when no slot is available.[1]

The documented `/metrics` endpoint is Prometheus-compatible but requires the server to be started with `--metrics`.[1] Among its metrics are `llamacpp:requests_processing`, `llamacpp:requests_deferred`, average prompt/generation throughput, and busy-slot measurements.[1] These signals are more useful for admission decisions and alerting than a binary TCP probe.

## Local observations from 2026-09-29

- `fish-tts-bench.service`: enabled, active/running; `Restart=on-failure`, `RestartSec=5`, `Type=simple`, port 7490.
- `hermes-gateway.service`: enabled, active/running; `Restart=always`, `RestartSec=5`, `TimeoutStopSec=70`, `KillMode=mixed`, and explicit exit-status handling.
- The Fish TTS dashboard journal showed successful proxied requests to the Fish backend on 2026-09-28, including `/fish/v1/health` and `/fish/v1/references/list`.
- From this laptop, probes to `127.0.0.1:8014`, `192.168.0.148:8014`, `127.0.0.1:8080`, and `127.0.0.1:8090` returned connection failures during this run. This does not establish that Spark or the remote voice service is down; it only records that those tested addresses were not reachable from this execution context.
- The local `systemd` executable was not on the shell PATH, although `systemctl --user` is present and successfully reported the units. Any automation should call the known `systemctl` path or avoid assuming the `systemd` binary is directly invocable.

## Analysis for AJ

### Proposed supervision layers

```text
systemd
  -> process lifecycle, restart backoff, start limits, cgroup limits
service process
  -> readiness and watchdog signal
adapter/gateway
  -> dependency health and admission state
llama.cpp / Fish / voiceprep
  -> health, slots, queue, metrics, artifact result
```

Use systemd to answer **“is the process alive and making progress?”** Use the service or adapter to answer **“can this request succeed now?”** Do not turn a remote Spark outage into a local restart loop unless the local process is itself wedged.

For `hermes-gateway.service`, `Restart=always` may be intentional because the gateway is a continuously supervised integration process, but it should be paired with observable restart counts and a tested start-limit policy. The service’s current explicit stop behavior is valuable because the gateway owns child processes; any watchdog or backoff change should preserve the existing cleanup path.

For `fish-tts-bench.service`, `Restart=on-failure` is a narrower baseline. Its health contract should include the proxied Fish backend, not only the Node dashboard. A dashboard process that serves HTML while every synthesis request fails is “up” at the process layer and “unready” at the application layer.

For Spark, prefer a small adapter check that samples `/health`, `/slots?fail_on_no_slot=1`, and `/metrics` rather than restarting the client process whenever a generation request times out. A 503 from `/health` can mean model loading; a 503 from slot admission can mean no capacity; a connection refusal can mean transport failure. These should remain distinguishable in logs and alerts.[1]

### Minimal next experiment

Build a disposable local fixture, not a production change:

1. Create a fake HTTP backend with four modes: healthy, loading/503, saturated/no-slot, and hung.
2. Wrap it in a tiny service using `Type=notify` or an equivalent explicit readiness contract; emit watchdog pings only while the event loop and dependency check are healthy.
3. Run it under a temporary user unit with `Restart=on-failure`, finite `RestartSec=`, explicit `StartLimitIntervalSec=`, `StartLimitBurst=`, and conservative `MemoryMax=`/`TasksMax=` values.
4. Record journal events, restart count, readiness transitions, watchdog expiry, dependency errors, and request outcomes.
5. Verify that backend loading and saturation produce clear degraded states rather than restart storms, while a truly wedged process is restarted.

### Decision gate

Adopt the pattern for a real Hermes or voice service only if the fixture proves:

- process failure causes bounded recovery;
- a dependency outage does not cause repeated local restarts;
- readiness is false until the service can fulfill its declared contract;
- watchdog expiry catches a stuck event loop without killing a merely slow job;
- memory/task limits fail visibly and leave useful journal evidence;
- a restart preserves or clearly invalidates queued work rather than silently losing it;
- metrics distinguish processing, deferred, saturated, and failed requests.

## Why this matters to AJ

The recent A2A and MCP Tasks research assumes durable, inspectable jobs behind a protocol boundary. That boundary is only useful if the local workers have honest lifecycle semantics. A small systemd/health fixture would connect the architecture research to the actual Spark, Fish Speech, voice-preparation, and Hermes gateway failure modes without changing Agora or production services.

The practical outcome should be a reusable unit-template pattern and a short failure-injection test suite, not a blanket policy that every transient backend problem deserves a restart.

## Uncertainty and open questions

- The official manuals describe available systemd mechanisms, but they do not choose appropriate limits or health contracts for AJ’s specific services.[2][3][4]
- This run did not measure Spark queue latency, Fish Speech failure rates, or voiceprep-api behavior because the tested endpoints were not reachable from this execution context.
- It is unresolved whether the Spark service should expose `/slots` directly to Hermes or through a local authenticated adapter.
- Watchdog semantics require application support; adding `WatchdogSec=` to a service that cannot emit trustworthy progress notifications would create false failures.
- Restart policy cannot recover in-flight TTS or media jobs unless the job layer persists and reconciles them; that remains an application-level problem.

## What to queue next

Queue the **disposable systemd failure-injection fixture** first. After it passes, run a live measurement sweep of llama.cpp `/health`, `/slots`, and `/metrics` on Spark, then use the results to set admission and alert thresholds.

## Related notes

- [[Research/Research Scout]] — research-hub context and curation mandate.
- [[Research/2026-09-28 — A2A v1 for Agora Agent Delegation]] — peer-agent delegation boundary.
- [[Research/2026-09-27 — MCP Tasks for Agora Async Jobs]] — durable async-job boundary.
- [[Research/2026-09-24 — llama.cpp Speculative Decoding and DSpark for Spark]] — prior llama.cpp performance research.

## Sources

[1] https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/server/README.md — llama.cpp server README
[2] https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.service.xml — systemd.service manual
[3] https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.resource-control.xml — systemd.resource-control manual
[4] https://raw.githubusercontent.com/systemd/systemd/main/man/sd_notify.xml — sd_notify manual

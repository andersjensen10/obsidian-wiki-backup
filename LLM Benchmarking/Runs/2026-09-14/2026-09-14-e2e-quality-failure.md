# E2E benchmark failure report - 2026-09-14

Status: FAILED QUALITY GATE

The complete locked suite v1.0.0 ran against an isolated baseline server on 127.0.0.1:8015. The raw artifact contains 30 result groups and 70 streamed samples across C1/C2/C4; all HTTP streams completed and all samples had TTFT. However, 28 samples had empty visible response content, concentrated in long-context, code-generation, code-debugging, and agentic-planning cases. The independent verifier rejected the artifact.

This is not a successful benchmark. The likely cause is the isolated profile's reasoning mode consuming the output budget without emitting visible content; this must be confirmed by the rerun. The production Qwen service on :8014 remained healthy and unchanged.

Raw artifact: /media/aj/TOSHIBA EXT1/LLM Model Library/runs/2026-09-14-e2e/baseline-e2e.json
SHA-256: eb337c2eec5e1d494a9a8f274ec2f867fcb67fb8ee2dd69cb47df1bdf02f0e5b

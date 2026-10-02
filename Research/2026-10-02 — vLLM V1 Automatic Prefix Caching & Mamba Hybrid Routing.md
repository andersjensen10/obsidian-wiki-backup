# Research Scout — October 2, 2026

## Candidates

1. **vLLM V1 Automatic Prefix Caching & Mamba Hybrid Routing** — Evaluating vLLM's hash-based KV cache block eviction and prefix caching design updates for local inference performance on multi-turn agent workloads.
2. **Godot 4.4 Unified Experience & 3D Physics Interpolation** — Reviewing Godot 4.4's release highlights, including 3D physics interpolation, Metal rendering support, and Jolt physics integration.
3. **MicroPython Release Milestones & ESP32-C5/C6 Port Capabilities** — Examining recent MicroPython release patterns and low-level peripheral support for embedded microcontroller prototyping.

## Result

Selected **vLLM V1 Automatic Prefix Caching & Mamba Hybrid Routing**.

## Key Findings

- vLLM’s automatic prefix caching implements a hash-based mechanism where each KV cache block is uniquely identified by hashing its token content along with the prefix tokens preceding it.[1]
- With the V1 architecture, KV cache blocks are managed via pre-allocated block pools with doubly linked lists to achieve $O(1)$ block queue operations without Python object overhead.[1]
- For hybrid models (such as Mamba architectures combined with attention layers), vLLM supports `--mamba-cache-mode align` and `--enable-mamba-shared-prefix-checkpoint` to resume prefix-cache hits at shared-prefix junctions rather than strict block boundaries.[1]
- Cache isolation can be enforced in multi-tenant environments using optional per-request salting and sha256 default block hashing to mitigate collision risks across distinct sessions.[1]

## Analysis & Open Questions

Automatic prefix caching significantly reduces prompt recomputation latency for multi-turn agent loops where system prompts and tool histories overlap. However, tuning match units (`--prefix-match-unit`) and memory overhead trade-offs require empirical verification against specific local hardware constraints.

---

## Sources

[1] https://docs.vllm.ai/en/latest/design/prefix_caching — vLLM Automatic Prefix Caching Design

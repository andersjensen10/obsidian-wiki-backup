# Research Scout — MCP Apps and Agora Embedded Agent Interfaces

**Run date:** 2026-09-21 08:00 CEST  
**Selection basis:** relevance to AJ’s active Agora/Hermes work, evidence availability, practical usefulness, novelty, and non-repetition.

## Three candidate topics

1. **MCP Apps and embedded agent interfaces — selected.** MCP Apps is now an official MCP extension for interactive HTML interfaces inside host conversations, making it directly relevant to Agora’s chatroom UI, tool-backed dashboards, and future media/control panels.[2][3]
2. **Voice-agent turn-taking and interruption control.** This remains useful for the Fish Speech pipeline and a future voice-enabled persona, but it overlaps with the existing TTS comparison and is better handled as a measured audio experiment than another ecosystem survey.[unverified]
3. **Godot as an agent-facing interaction shell.** A Godot prototype could combine persona, world state, and robot-like control affordances, but it is less immediately actionable than understanding a newly standardized embedded-UI boundary.[unverified]

## Decision

The selected topic is **whether MCP Apps offers a useful architectural boundary for Agora or Hermes integrations, and what it would and would not replace**. The question is not whether AJ should rewrite Agora around MCP. It is whether selected tools or views should expose an optional embedded UI contract while Agora keeps ownership of conversation state, identity, permissions, and persistence.[unverified]

## Executive finding

MCP Apps standardizes a pattern in which an MCP tool points to a `ui://` resource, the host renders the resource as an interactive HTML interface, and the UI communicates with the host through MCP-style JSON-RPC.[1][2]

The current official documentation describes this as an extension for dashboards, forms, visualizations, and other interfaces that need more than text.[2][3]

For Agora, the useful idea is **an adapter boundary, not a replacement frontend**. A tool such as “inspect conversation branch,” “review generated media,” or “configure a ComfyUI job” could expose a self-contained view to a compatible host, while Agora’s existing WebSocket/event model remains the canonical room experience. This is an architectural recommendation based on the protocol shape and local project inspection, not a claim that Agora currently supports MCP Apps.[unverified]

The main constraint is host support. MCP Apps is an extension rather than the entire MCP core, and the official project states that host support varies.[4] An Agora implementation would therefore need a first-party fallback: ordinary web UI plus tool responses, with MCP App rendering treated as progressive enhancement.

## Sourced facts

### 1. What MCP Apps adds

The finalized SEP defines UI resources under the `ui://` URI scheme, tool metadata that associates a tool with a UI resource, and bidirectional communication between the UI and host over MCP’s JSON-RPC base protocol.[1] The accepted design focuses on HTML resources using the `text/html;profile=mcp-app` media type.[1]

The current overview describes the core sequence as a tool declaring a UI resource, the host fetching it, and the host rendering the resulting interactive interface in the conversation.[2] The reference repository summarizes the same flow as tool definition, tool call, host rendering in a sandboxed iframe, and bidirectional communication.[4]

The extension is therefore closer to a **portable tool view** than to a general-purpose web application framework. It gives a host a standardized way to render a tool-specific interface; it does not define Agora’s room model, message variants, world sessions, persona configuration, or persistence semantics.[unverified]

### 2. The interaction model is richer than static tool output

The official overview says an app can request tool calls, send messages, update the model’s context, and receive data from the host.[2] The announcement also highlights interfaces for dashboards, forms, visualizations, and multi-step workflows rather than only read-only output.[3]

That maps well to bounded Agora surfaces:[unverified]

- **Variant review:** display assistant variants, provenance, and a deliberate “select” or “fork” action.[unverified]
- **Media review:** show generated images/audio/video with job status, cancellation, and provenance links.[unverified]
- **World Session controls:** expose scene/character state as a form or inspector without making the LLM describe every field in prose.[unverified]
- **Tool diagnostics:** present structured event timelines and reconnect state during development.[unverified]

These are proposed mappings. They are not existing MCP endpoints or a promise of compatibility with current Agora clients.[unverified]

### 3. Sandboxing helps, but does not define authorization

The official MCP Apps material describes host-controlled sandboxed iframes and says the UI cannot access the parent page’s cookies or local storage, navigate the parent page, or execute scripts in the parent context.[2] The SEP describes mandatory iframe sandboxing and auditable communication as part of the security model.[1]

That boundary reduces the risk of directly embedding an untrusted tool UI into a host page, but it is not an authorization model for Agora actions. A sandboxed UI could still request a permitted tool call, and the host/server still decides what that tool is allowed to do. For AJ’s projects, destructive operations, media publishing, external messages, and actuator-like commands should remain behind explicit server-side permission checks and confirmation rules.[unverified]

The right design is **capability minimization at the tool boundary**: expose a read-only inspector separately from a mutating control tool, require explicit confirmation for destructive operations, and make the room/user identity visible to the server rather than trusting UI claims.[unverified]

### 4. Transport and framework implications

The current overview says MCP Apps use a JSON-RPC dialect with app-specific methods such as `ui/initialize`, and use `postMessage` between the iframe and host rather than stdio or HTTP for that UI channel.[2] The official examples cover React, Vue, Svelte, Preact, Solid, and vanilla JavaScript, but the SDK wrapper is optional.[2]

This is compatible with Agora’s frontend technology in principle, but it does not remove the need for an adapter. Agora currently has a Svelte/Vite web client and a server-side WebSocket protocol; an MCP App would introduce a separate host bridge and message vocabulary. The bridge would need to translate between:[unverified]

```text
MCP App UI <-> host postMessage/AppBridge <-> Agora adapter <-> Agora API/WS
```[unverified]

The adapter should not let the embedded UI write directly to Agora’s database or bypass the server’s event contract. It should call narrow server operations and receive normalized results/events.[unverified]

### 5. Ecosystem maturity is real but uneven

The January 2026 MCP announcement calls MCP Apps the first official MCP extension and reports support in clients including ChatGPT, Claude, Goose, and Visual Studio Code.[3] The current official overview lists additional hosts and explicitly directs readers to client-specific support information.[2][4]

This is enough to justify a small compatibility spike, not enough to make MCP Apps a hard dependency for Agora. Host behavior, supported capabilities, iframe policies, and distribution expectations still need to be checked per target client. A locally controlled Agora host can provide predictable behavior; external hosts cannot be assumed equivalent.[unverified]

## Local Agora comparison

A code search of `/home/aj/Desktop/Hermes/AgenticChatroomProject` on this run found no substantive MCP implementation references; the working tree was clean at commit `1ddf090` during inspection. This is local repository evidence, not a statement about the public repository’s current indexed state.[unverified]

Agora already has the more important application-level responsibilities: persistent conversation state, WebSocket streaming, regeneration/variant behavior, and project-specific UI semantics. The previous Agora research report recommended generation IDs and reconnect-focused scenario tests; MCP Apps does not solve those problems. It could carry a focused inspector or control panel, but the canonical state machine should remain Agora-owned.[unverified]

## Architecture recommendation for AJ

### Adopt an optional adapter, not a rewrite

1. Keep the existing Agora web client as the reference UI.[unverified]
2. Select one read-mostly tool, such as a conversation/variant inspector or media-job viewer.[unverified]
3. Define a narrow MCP-facing tool schema with explicit read/write separation.[unverified]
4. Serve a small `ui://` resource that renders the selected tool result.[unverified]
5. Implement a host adapter that maps MCP App requests to existing Agora HTTP/WS operations.[unverified]
6. Add a plain structured-data fallback for hosts without MCP App support.[unverified]
7. Test stale events, reconnects, duplicate actions, authorization failures, and cancellation through the same scenario-level harness used for Agora’s own WebSocket behavior.[unverified]

The first spike should avoid world-session mutation and avoid any tool that sends external messages. A read-only variant/media inspector will exercise the rendering bridge while keeping failure consequences low.[unverified]

### Do not put these responsibilities in the MCP App

- Canonical transcript or message ordering.[unverified]
- Generation identity, variant persistence, or reconnect recovery.[unverified]
- Authorization decisions.[unverified]
- Secret storage or provider credentials.[unverified]
- Destructive deletion, publishing, or external side effects without a server confirmation path.[unverified]
- Durable project state that must survive host-specific UI behavior.[unverified]

## Recommended next experiment

Build a disposable **read-only MCP App inspector** around an existing Agora-compatible fixture rather than the production room:[unverified]

1. Create a fixture containing a multi-turn transcript, two assistant variants, one media-job record, and event timestamps.[unverified]
2. Expose one MCP tool that returns the fixture plus a `ui://` resource.[unverified]
3. Render the transcript, variant selector, and media-job status in the embedded view.[unverified]
4. Verify that selecting a variant changes only the view state and does not mutate the canonical fixture.[unverified]
5. Simulate delayed and duplicate host messages; ensure the UI ignores stale responses using request or generation identity.[unverified]
6. Run the same fixture through a non-MCP fallback view.[unverified]
7. Record host-specific differences before considering a live Agora adapter.[unverified]

**Decision rule:** keep the adapter if the inspector reduces UI duplication without weakening Agora’s event and permission boundaries. Drop or defer it if host-specific behavior consumes more complexity than the view saves.[unverified]

## Why this matters to AJ

Agora is becoming a host for multiple generated artifacts and stateful interactions, while Hermes and local services already expose tool-like capabilities. MCP Apps offers a way to package selected rich tool interfaces without forcing every host to invent a proprietary embedding protocol.[1][3] The practical value is highest at the edges—inspectors, dashboards, forms, and media controls—not at the canonical conversation core.

The approach also preserves optionality. If MCP App support remains uneven, Agora’s first-party Svelte client continues to work. If support broadens, the adapter can make selected Agora tools available in compatible agent hosts without duplicating their underlying server logic.[unverified]

## Uncertainty and open questions

- The official documentation describes host support as variable; a real compatibility matrix for AJ’s target hosts still needs to be built.[2][4]
- The security model protects the iframe boundary, but the correct authorization and confirmation policy remains an Agora application responsibility.[1][2]
- The current Agora checkout has no substantive MCP implementation reference from this run; no claim is made about future branches or unpublished work.[unverified]
- It remains unclear whether MCP App lifecycle events and Agora’s generation/event IDs can be made sufficiently transparent for reconnect-heavy workflows without a custom adapter protocol.[unverified]
- The protocol’s UI transport is not a substitute for durable event replay, persistence, or conflict resolution; those remain application-level concerns.[1][2]

## What to queue next

The best follow-up is the read-only inspector spike above. If AJ wants to stay away from MCP integration for now, the deferred alternatives remain voice turn-taking/interruption control for the Fish pipeline or a Godot agent-facing interaction prototype.[unverified]

## Sources

[1] https://modelcontextprotocol.io/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp
[2] https://modelcontextprotocol.io/extensions/apps/overview
[3] https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps
[4] https://github.com/modelcontextprotocol/ext-apps/blob/main/README.md

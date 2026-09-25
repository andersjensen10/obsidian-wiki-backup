# Research Scout — MCP Authorization Hardening for an Agora Adapter

**Run date:** 2026-09-25 08:00 CEST  
**Selection basis:** relevance to AJ’s active Agora/Hermes work, evidence availability, practical usefulness, novelty, and non-repetition.

## Three candidate topics

1. **MCP authorization and security hardening for a future Agora adapter — selected.** This is the most actionable deferred topic: the earlier MCP Apps report treated the adapter as a proposed read-only interface, but a safe implementation needs explicit token, redirect, discovery, consent, and network-boundary rules before any live connection is attempted.[1][2]
2. **Godot 4.5 as an agent-facing interaction shell.** Godot 4.5 adds accessibility-oriented UI controls, mobile/XR capabilities, and other interaction improvements, making it a plausible future shell for an agent or robot-like interface, but it is a broader product direction than the current Agora security boundary.[3]
3. **llama.cpp structured output versus tool-calling composition.** A current llama.cpp discussion reports that `llama-server` rejects requests combining custom grammar constraints with OpenAI-style tools, which could matter for reliable local agent output, but this is a narrower implementation issue and overlaps the recent inference-focused run.[unverified]

## Decision

The selected topic is **what an Agora MCP adapter would need to enforce before it could safely expose even read-only capabilities, and what bounded security fixture should be built first**.

## Executive finding

MCP’s HTTP authorization specification is built around OAuth 2.1, protected-resource metadata, authorization-server metadata, and resource indicators; it requires clients to identify the intended MCP server as the token resource and requires servers to validate that tokens were issued for them.[1]

The most important design rule for Agora is to keep authorization boundaries explicit: an adapter must validate the incoming token for Agora, must not pass that token through to another API, and must make any downstream credential exchange separately.[1][2]

The recommended next step is not a production OAuth integration. It is a disposable local security fixture that exercises discovery, audience validation, PKCE/state handling, redirect exactness, consent binding, scope checks, and SSRF protections against a fake MCP server and fake upstream service.[1][2]

## Sourced facts

### 1. MCP authorization is transport-specific

The MCP authorization specification defines authorization for HTTP-based transports. Authorization is optional for MCP implementations; HTTP implementations that support it should conform to the specification, while STDIO implementations should retrieve credentials from the environment instead.[1]

For HTTP authorization, MCP servers must expose protected-resource metadata, clients must use it to discover authorization servers, and authorization servers must provide authorization-server metadata.[1] This creates a discovery chain that an Agora adapter would need to constrain rather than blindly trust.

MCP clients must include the OAuth `resource` parameter in both authorization and token requests, identifying the canonical URI of the MCP server they intend to use.[1] This is the protocol-level mechanism that binds a token request to its intended resource.

### 2. Audience validation and token passthrough are the central boundary

MCP servers must validate access tokens and ensure that the tokens were issued specifically for the MCP server as the intended audience.[1] The security guidance explicitly forbids accepting a token issued for another resource and forwarding it unchanged to a downstream API.[2]

The security guidance describes token passthrough as a confused-deputy risk: downstream services may incorrectly trust a token as if the MCP server had validated it, and logs may lose the distinction between the MCP client and the downstream identity.[2]

For Agora, the safe architecture is therefore:

```text
MCP client
  -> Agora adapter: validate Agora audience, issuer, expiry, scopes
    -> Agora application API: use an adapter-owned credential or internal authorization
```

The incoming bearer token should terminate at the adapter. If the adapter later calls a separate service, it should obtain and use a separate credential for that service rather than forwarding the client token.[1][2]

### 3. Redirects, PKCE, state, and consent need exact checks

The authorization specification requires HTTPS for authorization-server endpoints, permits loopback redirect URIs for local development, and requires MCP clients to implement PKCE to reduce authorization-code interception and injection attacks.[1]

The security guidance requires exact redirect-URI matching rather than wildcard or pattern matching.[2] It also requires a cryptographically secure, single-use state value with short expiration and says the state-tracking session must not be established before the user has approved the MCP consent screen.[2]

For proxy-style flows involving a third-party API, the guidance requires consent to be bound to the specific MCP `client_id`, with the consent UI showing the client identity, requested scopes, and registered redirect URI.[2] This matters even if Agora initially exposes only read operations: a generic “user has consented” flag would be too coarse for multiple clients or future mutating tools.

### 4. Discovery creates an SSRF boundary

The security guidance identifies OAuth discovery URLs—including resource metadata, authorization-server metadata, token endpoints, and authorization endpoints—as attacker-influenced inputs that can be used to target internal services or cloud metadata endpoints.[2]

It recommends HTTPS in production, blocking private and reserved IP ranges, validating every redirect target, considering an egress proxy, and accounting for DNS time-of-check/time-of-use issues.[2] An Agora adapter running on AJ’s home network should treat these rules as relevant even without a cloud deployment: a malicious MCP server must not turn the adapter into a path toward LAN administration endpoints or local services.

## Analysis for Agora

The previous MCP Apps direction was a read-only inspector spike, so the immediate risk is not a large permission model; it is accidentally making discovery and bearer-token handling implicit.[unverified] A read-only tool can still leak conversation state, project metadata, or operational details if the adapter accepts a token for the wrong audience or follows attacker-controlled URLs.[unverified]

A useful first adapter contract should make these decisions visible in code and tests:

| Boundary | Required decision | Initial fixture assertion |
|---|---|---|
| Resource identity | What exact URI represents Agora? | Token with another audience is rejected |
| Token validation | Which issuer, audience, expiry, and scopes are accepted? | Missing, expired, wrong-audience, and insufficient-scope tokens fail |
| Downstream calls | Which credential authorizes the application API? | Client bearer token never appears in upstream request |
| Redirects | Which callback URIs are registered? | Near-match, wildcard, and changed URIs fail |
| OAuth state | Where is state stored and when is it created? | Missing, replayed, or pre-consent state fails |
| Discovery | Which hosts and IP ranges may be contacted? | Private-IP, metadata-IP, and redirect-to-private tests fail |
| Consent | Which client and scopes did the user approve? | Consent for client A cannot authorize client B |

This is a proposed Agora-specific test contract, not a claim that MCP mandates these exact application fields.[unverified]

## Recommended next experiment

Build a local **MCP authorization fixture** with no production service changes:

1. Create a fake MCP resource server, fake authorization server, fake client, and fake downstream API.
2. Implement the happy path using protected-resource metadata, authorization-server metadata, `resource`, PKCE, exact redirect registration, state, and a short-lived token.[1]
3. Add negative tests for wrong audience, wrong issuer, expired token, missing scope, token in the query string, and replayed authorization code.[1]
4. Add a downstream assertion that the client bearer token is never forwarded.[1][2]
5. Add consent tests for two client IDs requesting different scopes, including a client whose redirect URI changes.[2]
6. Add discovery tests for loopback development URLs, private IPv4/IPv6 ranges, link-local metadata addresses, DNS rebinding, and redirects into blocked ranges.[2]
7. Record only structured outcome metadata by default; do not log bearer tokens, authorization codes, PKCE verifiers, or raw conversation content.[unverified]

**Decision rule:** do not connect a real Agora endpoint or expose a mutating MCP tool until the fixture demonstrates that the adapter rejects invalid audience, consent, redirect, scope, and network-boundary cases without forwarding client credentials.[unverified]

## Why this matters to AJ

This topic is more immediately useful than another general MCP feature survey because it produces a concrete go/no-go gate for the proposed Agora inspector. It also aligns with the existing observability work: authorization failures, consent decisions, discovery blocks, and downstream credential use should become explicit traceable outcomes rather than ambiguous HTTP errors.[unverified]

The security boundary should remain below Agora’s conversation state. The application should continue to own session ordering, generation identity, permissions, and durable data, while the adapter owns protocol authentication and maps only explicitly allowed operations into Agora.[unverified]

## Uncertainty and open questions

- The retrieved MCP authorization page is versioned 2025-06-18, while the security-best-practices page links to a newer dated specification path; exact version alignment should be checked before implementation.[1][2]
- The sources define protocol and security requirements but do not specify how Agora’s existing authentication or WebSocket identity should map to OAuth scopes.[unverified]
- No live MCP client/server interoperability test was run in this report.[unverified]
- The fixture should decide whether the first Agora adapter is intentionally local-only, because loopback exceptions and LAN access controls materially change the threat model.[1][2]

## What to queue next

The best follow-up is the local negative-test fixture above. Deferred alternatives remain a Godot agent-facing interaction spike and a llama.cpp structured-output/tool-calling compatibility test.

## Sources

[1] https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization — MCP Authorization Specification
[2] https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices — MCP Security Best Practices
[3] https://godotengine.org/releases/4.5 — Godot 4.5 Release Notes

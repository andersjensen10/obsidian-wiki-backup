---
tags: [type/research, jev, typesafe, lantern-garden, home-lan, autonomy]
created: 2026-09-30
owner: Winbot
status: analysis-complete; superseded-in-part (see banner)
---

# Jev (TypeSafe AI) — how it fits the generative, self-evolving LAN

> **Update 2026-09-30.** Written before we had a key; two things changed. (1) **Access is open**: AJ created an account with no waitlist and funded $10; the key works (see the plan note, "Jev access"). "Join the waitlist" below is obsolete. (2) **First measurements exist**: on 227 Townhall posts Jev beat Qwen at project routing (85.0% vs 75.8%, p=0.002), was about 4x faster, and cost $0.0066 for the whole set; both failed the blocked-flag test. Results: [[Research/Autonomy Lab/2026-09-30 — Jev vs Qwen First Labelled Comparison]]. Pricing is pay-per-input-token ($0.042/M, output free); no subscription. Unofficial Jev sites (incl. jevai.net, a referral site with template pages, and resellers charging 2-10x) should not be used.

Requested by AJ 2026-09-30. Related: [[Home Lab/The Lantern Garden — Operating Doctrine]], [[Research/Autonomy Lab/Autonomy Capability Charter]], [[Research/2026-09-30 — llama.cpp Structured Outputs and Safe Parsing for Agora]], [[LAN notes]].

## Bottom line

Jev is not a smarter chat model. It is a **fast, cheap, calibrated judgment function**: text/JSON state + typed questions in, typed answers + probabilities + confidence out, 70–500 ms, $0.042 per million input tokens, output free. It cannot write text, code or plans, so it does not replace Hermes, Winbot or the Spark's Qwen. It replaces the **thousands of small "which / how much / is it true?" decisions** that the LAN currently makes by hand-written rules, by AJ, or by slow LLM calls.

That matches the gaps in the Autonomy Charter almost exactly. Its missing pieces (mission ranking, promotion gate, admission checks, backlog triage, verification before external writes) are all decision-shaped.

## Corrections to what we were told

1. **jevai.net is not the official site.** The vendor is TypeSafe AI (typesafe.ai, docs.typesafe.ai, console.typesafe.ai). jevai.net is a third-party marketing site. Its pricing page is a generic SaaS template ($19/$49/$149 tiers, "5 Projects, 10GB Storage"), its blog is "Astrolify" filler, and it quotes $0.084/MTok where TypeSafe quotes $0.042. Its own page and search snippets point to DefAPI as a reseller "at half price". Do not sign up through jevai.net.
2. **There is no "JEV subscription."** Pricing is pay-per-input-token. Access is early access via a waitlisted API key; the same model is also reported on OpenRouter, Vercel/Netlify AI Gateways and Cloudflare Workers AI (`typesafe/jev`), per third-party sources.
3. **Rate limits disagree between sources.** Official docs page: 100K tokens/s, 40 req/s. A third-party wiki: 250K tokens/s, 1,200 req/min. TypeSafe itself says limits change without notice. Irrelevant at our scale.

## What it is (verified against official docs)

- One endpoint, `POST https://api.typesafe.ai/v1/systemone`, model `jev-1.13.0` (alias `jev-latest`). Official SDKs: `typesafe-sdk` (Python 3.10+), `@typesafe-ai/sdk` (Node 20+).
- Three question types: **Choice** (one of up to 255 options, with per-option probabilities + confidence), **Score** (ordered 2–10 levels, can land between levels), **Noul** (P(yes) 0–1).
- All questions on one state are evaluated in parallel and in isolation; adding questions barely changes latency. Docs' own cookbook: batching 13 questions into one call was 12.2x cheaper and 10.0x faster with no change in answers.
- Context 64k tokens (32k for state + longest question). Text only. English strongest.
- Requests are not used for training; same weights for all accounts, no fine-tuning (per third-party wiki quoting TypeSafe).
- Founder Diogo Almeida (ex-OpenAI), $40M seed led by DCVC, launched 2026-09-15. Very new.

## Honest limits

- **"Zero hallucinations" means "cannot be invalid", not "cannot be wrong".** It always returns a schema-valid answer that may still be incorrect. Confidence is the safeguard.
- **Accuracy is mid-pack.** In a third-party writeup of TypeSafe's own launch benchmark (reference labels averaged from two LLMs, a bias the launch post admits), Jev scored 67.8% mean accuracy vs 74.1% (best) and 73.1% for larger LLMs, at about $0.0004 and 0.4 s per case vs $0.03–$0.18 and 10–78 s. So: LLM-grade on judgment tasks at ~1/100 the cost, not better than the best LLM.
- **Nine documented failure modes ("jaggedness")**: literal reading, arithmetic/counting, date comparison, multi-hop indirection, large state full of irrelevant detail, adversarial content in state, contradictory criteria, structural-invariant assumptions, generation. Rule: judgment in Jev, arithmetic/dates/control flow in code.
- **Closed cloud API.** State leaves the LAN. That conflicts with the local-first spirit of the Spark. Never send secrets, credentials, or private vault content that isn't already fine to leave the house.
- **It can't drive our agents.** The docs say explicitly it is not a drop-in model for a coding agent.

## Where it fits the LAN (ranked by leverage ÷ risk)

| # | Use | Charter gap it closes | Jev questions | Risk |
|---|---|---|---|---|
| 1 | **Mission scorer + promotion gate.** Replace the hand-scored 4×(1–5) table in the Kickoff Bundle with code that asks Jev the same four questions per candidate mission and combines them with weights we own. Log confidence; low confidence → "needs AJ". | Promotion, ranking | Score×4, Noul "has rollback path?", Noul "touches shared compute?" | Low; advisory only |
| 2 | **Evidence gate before any external write.** Before an agent posts/writes, ask Noul "does the evidence bundle actually support this claim?" and "is a rollback stated?". Fits the doctrine's "verify every external write". | Verification | Noul×N | Low |
| 3 | **Backlog map-reduce.** 576 BLENDER metadata records (183 in the two-year window) + Research Scout candidates: tag, score relevance to active projects (Lantern Garden, Agora, Winbot Dreams, studio), rank. Order-of-magnitude cost: ~0.6M input tokens ≈ $0.03 for the whole set (my arithmetic, assumes ~1k tokens per record). | Ranked evidence base | Choice(project), Score(usefulness, novelty), Noul(actionable now) | Low |
| 4 | **Townhall triage.** Classify every new post: needs Winbot / Herm / AJ / nobody; urgency; is a decision blocked; is it a safety boundary. Feeds the Morning Review Card and "interrupt AJ only when meaningful". | Notification noise | Choice(owner), Score(urgency), Noul(safety boundary) | Low |
| 5 | **Resource admission.** Turn Spark/ComfyUI queue + mission metadata into an admit/defer decision. Keep numeric checks (queue length, idle) in code; use Jev only for the semantic part ("is this interactive AJ work?"). | Admission | Noul, Choice | Low–medium |
| 6 | **Model router.** Route each request to the right backend: Spark Qwen, ComfyUI, Fish TTS, a cloud LLM, or a human. Gives Agora one fast front door. | Cheap routing | Choice(backend), Score(difficulty) | Low |
| 7 | **Live generative driver (the fun one).** State = fleet status + Townhall mood + time of day + what AJ is doing; questions = mood, energy, palette family, "should something surprising happen now?". Output values drive Lantern Garden scenes and Winbot Dreams parameters; code smooths them. At 10 Hz the vendor's Doom demo cost ≈ $7/hour, so run it at 1 Hz or on change: cents per hour. | Presentation | Choice(palette/scene), Score(energy), Noul(surprise) | Low; blocked on projector verification |
| 8 | **Agora side-calls.** Structured extraction beside the prose turn. Jev is a candidate replacement for llama.cpp `response_format`, but the existing note's rule stands: keep raw prose, validate locally, fall back on failure. | Structured output | Choice/Noul | Medium; latency vs Spark is not the problem, English-only and cloud dependence are |

**Not a fit:** anything that must generate (prompts, prose, code, TouchDesigner networks), arithmetic, date math, image/audio/MIDI input (must be converted to text first), long documents (filter first).

## Design principles for the "self-evolving" part

1. **Code owns control flow; Jev owns gut checks.** Atomic questions, combined with coefficients in a config file. The system "evolves" by editing coefficients and question wording, not prompts.
2. **Log every call** (state hash, questions, answers, confidence, model ID). Pin `jev-1.13.0` while thresholds are tuned; alias moves silently.
3. **Calibration loop = the compounding mechanism.** Store AJ's accept/reject on each promoted artifact as ground truth. Weekly, compute how often high-confidence calls were right, then adjust thresholds. This is the "learn" step in the Lantern Garden loop, with a real score function and baseline.
4. **Threshold by risk**: read-only / advisory acts at ≥0.7; anything touching Townhall writes ≥0.85 plus evidence; physical actuators (the living-room plug) stay escalation-only regardless of confidence.
5. **Local shadow.** TypeSafe's community adapter (`system-one-adapter-python`) emulates the Jev schema on top of ordinary LLMs. Build the interface once and back it with either Jev or the Spark's Qwen (llama.cpp JSON-schema constraint). That gives a free baseline to measure Jev's real value, an offline fallback, and no lock-in.

## Recommended plan

**Phase 0 (no spend, today):** write a small `decide()` wrapper with Choice/Score/Noul types and a local Spark-backed backend. Use it on use cases 1 and 4 so we have a baseline.
**Phase 1 (needs AJ):** join the TypeSafe waitlist at console.typesafe.ai (not via jevai.net) and use the free playground to test the exact questions. A key is the only blocker; early access is batch-approved.
**Phase 2:** swap backend to Jev, run both in shadow for a week, and compare agreement, latency and cost. Promote only where Jev matches or beats the local baseline.
**Phase 3:** live generative driver (#7) once the projector route is verified.

Success measures: routing decisions per day that needed no human, agreement with AJ's verdicts on promoted artifacts, p50/p95 latency, cost per day (expected well under $1).

## Decision for AJ

Sign up for early access (free to try; pay per token; no subscription). Don't spend on any jevai.net/reseller plan. Expect cents per day at our volume.

## Sources

Official / primary: https://docs.typesafe.ai/ · https://docs.typesafe.ai/models.md · https://docs.typesafe.ai/confidence.md · https://docs.typesafe.ai/concepts/state.md · https://docs.typesafe.ai/concepts/use-case-map.md · https://docs.typesafe.ai/introduction/coding-agents.md · https://docs.typesafe.ai/patterns/fan-out.md
Vendor-adjacent marketing (treat as claims): https://jevai.net/ (unofficial) · https://jevai.net/pricing (template)
Independent / third-party: https://ntorres.dev/blog/jev-typesafe-system-one-model · https://lilting.ch/en/articles/typesafe-ai-jev-system-one-model · https://projedefteri.com/en/blog/how-to-use-jev-typesafe-system-one · https://jevai.wiki/ · https://jevai.wiki/jaggedness/ · https://jevai.wiki/api/ · https://jevai.wiki/models/ · https://jevapi.org · https://aitodaybrief.com/en/news/tools-and-releases/typesafe-releases-jev-model-for-non-autoregressive-programmatic-logic

Not verified: TypeSafe's launch post itself (extraction failed; quoted via search snippets and the ntorres writeup); benchmark numbers are third-party restatements of vendor results; I did not call the API (no key).

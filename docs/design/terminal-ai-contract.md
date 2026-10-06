# Terminal and user-supplied AI

**Date:** 2026-10-05  
**Status:** Accepted; first increment implemented in 0.3.0-alpha.6 ([ADR-0008](../decisions/0008-local-terminal-and-ai-adapters.md))

## Product direction

The user selected a terminal interface and proposed using whichever AI the user already has.
Keep the ProductOS interface independent of a specific model vendor. Portability requires
explicit adapters; it does not mean every AI account or application can be invoked automatically.

## Proposed user flow

1. Open ProductOS and select a supported connection.
2. Choose an available model when the connection exposes multiple models.
3. Create or open a decision, supply context, and attach evidence.
4. Request analysis with the selected connection.
5. Inspect the answer, sources, uncertainties, and next action; save an explicit decision.

Show the selected connection and model beside the analysis action. Keep evidence inspection
and saved decisions available when inference is unavailable. Distinguish a model answer from
a reviewed decision and from approved canonical knowledge.

## Connection modes

| Mode | Integration boundary | Availability |
|---|---|---|
| Installed assistant | Adapter invokes a supported CLI using that assistant's existing authentication | Requires an installed CLI with a suitable non-interactive interface |
| User-owned API | Adapter invokes a provider endpoint using the user's local credential reference and model choice | Requires an API account and its own access conditions |
| Manual exchange | Export a context-and-instructions packet; user copies it into an assistant and imports the answer | Fallback for assistants without a supported CLI/API integration; extra manual steps |

A browser chat account is not itself an adapter. Do not imply that an existing subscription
automatically supplies API access. Do not display unsupported connections as working ones.

## Adapter contract

ProductOS prepares a bounded request containing the decision question, user context, relevant
ProductOS instructions, selected evidence with locators and limitations, language, and output
intent. It must not include evaluation answer keys or an unrelated workspace's content.

Each adapter declares:

- connection identity, supported invocation mode, and available model selection;
- input limits, instruction-message support, structured-output support, and streaming support;
- timeout and cancellation behavior;
- whether tools are available and how their use is explicitly scoped.

Each invocation returns the original answer text, the reported provider/model identity when
available, completion status, timing, and any structured metadata the adapter actually exposes.
Missing model identity, token counts, or cost remain unknown; do not invent them. A Markdown
answer may be supported without assuming that every model can produce valid decision-record JSON.

Before persistence, validate structured records against the existing schema. Preserve the
answer as an answer when validation fails; never silently treat malformed output as an approved
decision. Cancellation or transport failure must remain distinct from a completed answer.

## Provenance and configuration

Record the supplied instructions and evidence references, selected connection, requested and
reported model identities, generation time, original answer, and review state. Local connection
configuration references credentials; credential contents do not belong in decision records,
canonical knowledge, exported packets, or this repository. Installed CLI adapters can rely on
their existing authentication rather than asking ProductOS to copy credentials.

Keep adapter execution separate from the deterministic reasoning contracts and validators.
The current evaluation runner is evaluation-only; its same-model generator/judge configuration
does not choose or constrain the product's inference provider.

## First increment and qualification

Build the terminal around a small adapter interface, one supported installed-assistant
integration, and manual exchange as a fallback. Add individual API integrations as they become
needed. The first provider should be an adapter implementation, never a hardcoded product rule.
Packaging all potential vendors before a real workflow is observed is outside this increment.

Verify real decisions end to end with the configured adapter, including missing authentication,
timeout, cancellation, malformed structured output, and preservation of evidence provenance.
Behavioral scores apply to the tested model and instruction configuration. Supporting another
connection does not establish equivalent decision quality. The existing uncalibrated pilot
cannot qualify all future adapters or models.

This proposal supplies the runtime boundary required by the
[interface exploration](interface-options.md). Implementing it requires a scoped architecture
decision; it does not introduce a SaaS service, database, or retrieval system.

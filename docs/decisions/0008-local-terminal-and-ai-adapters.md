# ADR-0008: Local terminal and user-owned AI connections

**Status:** Accepted  
**Date:** 2026-10-05

## Context

The user selected a terminal interface and requested use of the AI each user already has.
The repository-native reasoning foundation must remain independent of provider and presentation.
The evaluation adapter in ADR-0007 is not a product runtime.

## Decision

Add an optional local Python/Textual terminal and a command interface under `productos/`.
Keep personal work in a separate user-selected workspace, defaulting to `~/.productos`.
Persist local JSON records with versioned schemas and original answer provenance; do not
write generated answers into canonical knowledge or infer approval from model output.

The first product adapters are:

- manual context export and response import, available without provider integration;
- an installed Codex CLI adapter, using existing assistant authentication;
- a configurable executable/argument adapter receiving stdin and producing final-answer stdout.

The UI and core use cases share the same workspace and adapter APIs. Invocation is asynchronous
with explicit timeout and cancellation. Only an explicit analysis action starts inference.
Connection selection and model choice do not require code changes. The generic command contract
can connect an additional assistant or a user-maintained API bridge; it is not a native integration
with every provider.

Freeze supplied instructions, user evidence, and decision revision before each invocation.
Store the original answer, hashes, timestamps, selected adapter, requested model, and reported
model only when actually available. Validate optional structured output without promoting it
to approved knowledge. Interrupted invocations become failed records on reopening the locked
workspace rather than appearing completed.

## Consequences

- This adds local product runtime orchestration, scoped to user-requested inference. It does
  not add a SaaS UI, database, or retrieval service, and leaves canonical file ownership intact.
- The terminal is optional; deterministic validation and noninteractive commands remain usable
  without Textual. The clone supplies canonical instructions and schemas.
- The manual mode is the initial default and supports assistants without a supported CLI.
- Codex execution uses a fresh temporary working directory, read-only sandbox, and explicit
  supplied instructions; observed tool items reject the result. This is not native skill
  discovery or progressive reference loading.
- Generic commands are user-controlled and must provide final-answer text on stdout. Their
  internal tool use and claimed model identity are not independently verified by ProductOS.
- Provider-specific native API adapters, streamed answers, multilingual UI chrome, and shared
  workspaces remain future increments. Analysis language supports `en`, `pt-BR`, and `es`.
- Behavioral qualification applies per tested configuration. The existing pilot and a product
  smoke run do not establish equivalent reasoning quality for all connected models.

## References

- [Terminal AI contract](../design/terminal-ai-contract.md)
- [Terminal usage](../terminal.md)
- [Official Textual worker guide](https://textual.textualize.io/guide/workers/)
- [Official OpenAI documentation for Codex non-interactive execution](https://learn.chatgpt.com/docs/non-interactive-mode)

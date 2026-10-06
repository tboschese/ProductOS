# ADR-0007: Opt-in behavioral pilot execution

**Status:** Accepted
**Date:** 2026-10-05

## Context

The repository can export blind cases and report judgments, but those capabilities alone
cannot produce an observed baseline. A controlled executor is needed to generate and assess
responses while preserving the declared separation and provenance rules.

## Decision

- Add a manually invoked Codex CLI adapter for the first behavioral pilot.
- Declare model, reasoning settings, identities, prompt version, repetitions, instruction
  bundle, and timeout in a schema-validated configuration.
- Freeze the instruction bundle, rubric, prompts, case packets, configuration, and runner
  before generation. Record the base Git revision, dirty-worktree state, and file SHA-256 values.
- Execute each generation and judgment in a fresh, ephemeral, read-only CLI workspace. Reject
  tool activity in the event stream because this pilot tests supplied instruction behavior.
- Preserve responses verbatim and record dimension evidence and individual behavior checks.
- Keep the judge at `pilot`; the executor cannot declare it calibrated.
- Keep model calls out of CI. Offline tests use clearly labeled synthetic transport and
  judgment data to exercise failure, checkpoint, and integrity behavior.

## Consequences

The pilot evaluates a supplied instruction bundle, not skill discovery, progressive reference
loading, tools, retrieval, or installation behavior. A single repetition does not demonstrate
stochastic stability. Using the same model for generation and judging introduces dependence
despite fresh contexts. Human calibration, repeated runs, editorial approval, and runtime
verification remain separate release gates.

The adapter is evaluation infrastructure. The repository-native product runtime and canonical
knowledge ownership stay as defined in ADR-0001 and ADR-0002.

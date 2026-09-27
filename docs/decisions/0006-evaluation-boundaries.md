# ADR-0006: Separate structural validation from behavior evals

**Status:** Accepted
**Date:** 2026-09-26

## Context

Product judgment is probabilistic and contextual, while repository structure and schema conformance are deterministic.

## Decision

- Python validators check schemas, IDs, references, file layout, and other deterministic rules.
- Behavior evals declare expected behaviors, forbidden behaviors, rubric dimensions, and hard failures.
- Automated judges require a recorded model configuration and calibration against human review.
- Multilingual variants share a case family and are compared for reasoning equivalence.

## Consequences

`run_evals.py` will orchestrate cases and scoring but will not present subjective judgment as deterministic truth.

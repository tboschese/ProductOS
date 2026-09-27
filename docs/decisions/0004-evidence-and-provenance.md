# ADR-0004: Evidence and provenance dimensions

**Status:** Accepted
**Date:** 2026-09-26

## Context

The specification uses one taxonomy for statement status and another for evidence categories. Source authority is also insufficient as a proxy for claim quality.

## Decision

Represent epistemic status, evidence modality, source authority, confidence, and source locator as separate fields. Confidence remains qualitative. Claims can carry supporting and contradicting source references.

## Consequences

- Strong sources cannot automatically turn weakly supported claims into facts.
- Contradictions remain first-class evidence.
- Approved material claims require precise, reviewable provenance.

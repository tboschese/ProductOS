# ADR-0005: Canonical relationship registry

**Status:** Accepted
**Date:** 2026-09-26

## Context

The specification proposes both a central relationship registry and relationship fields embedded in several entity types.

## Decision

Relationships are canonical first-class entities containing subject, predicate, object, confidence, and provenance. Entity documents may expose generated relationship summaries, but those summaries are not editable sources of truth.

## Consequences

- Direction, cardinality, and provenance can be validated consistently.
- Updating a relationship does not require editing multiple entities.
- Graph infrastructure remains optional; the registry can initially be plain YAML.

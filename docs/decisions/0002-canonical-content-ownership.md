# ADR-0002: Canonical content ownership

**Status:** Accepted
**Date:** 2026-09-26

## Context

The proposed repository contains narrative documentation, structured knowledge, and skill references. Without ownership rules, the same content can diverge in three locations.

## Decision

- Structured entities are canonical as one YAML file per entity under `knowledge/<entity-type>/`.
- Markdown is canonical for policy, architecture, methodology, and narrative synthesis.
- Skill references point to canonical material or contain task-specific guidance; they do not become a second knowledge base.
- Generated indexes are reproducible outputs and are never edited manually.

## Consequences

The repository layout deviates from the specification's proposed monolithic registry files. Per-entity files reduce merge conflicts, allow focused review, and make lifecycle metadata explicit.

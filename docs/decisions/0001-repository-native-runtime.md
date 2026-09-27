# ADR-0001: Repository-native runtime

**Status:** Accepted
**Date:** 2026-09-26

## Context

The specification defines knowledge, reasoning, evals, and skills but does not require a service, database, or user interface for v1.

## Decision

Start with Markdown, YAML, JSON Schema, Python validation, and repository-discovered skills. Do not introduce a graph database, vector database, RAG service, or SaaS application until measured usage demonstrates a need.

## Consequences

- Every artifact remains inspectable and reviewable in Git.
- Progressive disclosure is implemented through routing and references, not infrastructure.
- Retrieval performance and scale must be measured before changing the architecture.

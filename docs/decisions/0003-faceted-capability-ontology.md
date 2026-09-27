# ADR-0003: Faceted capability ontology

**Status:** Accepted
**Date:** 2026-09-26

## Context

The capability model lists reasoning abilities, practices, business contexts, product types, organizational interfaces, roles, and constraints as equivalent domains. This creates overlapping ownership and duplicate knowledge.

## Decision

Use six facets: `capabilities`, `practices`, `contexts`, `product_types`, `roles_interfaces`, and `constraints`. Every entity also declares one `primary_domain` for editorial ownership.

## Consequences

- Cross-cutting topics can be tagged without being copied.
- Folder structure no longer needs to mirror every heading in the specification.
- Controlled vocabularies will be introduced incrementally and validated once approved.

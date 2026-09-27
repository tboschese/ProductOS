# Phase 0 architecture review

**Date:** 2026-09-26
**Specification reviewed:** ProductOS v0.3

## Outcome

Phase 0 establishes a repository-native, schema-first foundation without adding broad Product Management knowledge or incomplete skills.

## Material findings

1. The capability model mixed capabilities, practices, contexts, product types, roles, interfaces, and constraints as peer domains.
2. The specification did not assign canonical ownership across `docs/`, `knowledge/`, and skill references.
3. Proposed registries and schemas were not aligned; claims and relationships lacked explicit contracts.
4. Evidence classifications differed between the design principles and the Product Reasoning Engine.
5. Source authority was too coarse to represent claim quality, relevance, recency, and contradiction.
6. Relationship ownership was duplicated between a central registry and embedded entity fields.
7. The reasoning flow used “Decision” for both the question being framed and the final recommendation.
8. Research waves and delivery phases duplicated or placed Discovery, Research Ops, Product Planning, and Accessibility differently.
9. Behavior evals and the first integrated Staff PM skill arrived too late to protect earlier architecture and research work.
10. The target runtime and retrieval boundary were not explicit.

## Decisions taken

- Use a repository-native runtime until evidence justifies additional infrastructure.
- Store one YAML file per canonical entity rather than monolithic registry files.
- Use a faceted capability ontology with one primary editorial owner per entity.
- Separate epistemic status, evidence modality, source authority, confidence, and locator.
- Make relationships canonical first-class entities.
- Separate deterministic validation from product-judgment evals.
- Move a thin Staff PM slice and seed eval suite immediately after the reasoning foundation.

The rationale and consequences are recorded under `docs/decisions/`.

## Deviations from the specification

- Knowledge registries will use `knowledge/<entity-type>/<id>.yaml` instead of single large YAML files.
- Incomplete skill directories are not created during Phase 0 because discovery should expose only valid, releasable skills.
- `common`, `claim`, and `relationship` schemas were added to close entity and provenance gaps.
- The Staff PM Alpha is split into an early thin slice and later hardening rather than waiting until Phase 14 for first integration.
- Evaluation contracts move ahead of broad domain research.
- GitHub Actions, Python dependency metadata, fixtures, and tests were added so Phase 0 has an executable definition of done.

## Unresolved decisions

- open-source license and external contribution policy;
- named maintainers and required reviewer roles;
- approved controlled vocabulary for capability facets;
- model, judge prompt, repetition count, and cost budget for automated evals;
- calibrated release thresholds after an empirical baseline;
- retrieval and indexing design after real scale and latency measurements;
- hosting or API surface beyond repository skills.

## Risks to monitor

- knowledge volume growing faster than evidence quality;
- taxonomy fragmentation through uncontrolled tags;
- drift between narrative synthesis and canonical entities;
- eval overfitting and judge instability;
- multilingual semantic drift;
- prompt and reference bloat in future skills;
- copyright, privacy, and freshness failures in research material.

## Recommended next task

Implement version `0.2.0` as a narrow vertical slice:

1. formalize the decision, evidence, uncertainty, and risk contracts;
2. create 10–15 seed eval cases and record a baseline;
3. implement Product Reasoning Engine v0;
4. create a narrow Staff Product Manager skill for three to five representative decisions;
5. run structural, behavioral, and multilingual smoke tests before broad research.

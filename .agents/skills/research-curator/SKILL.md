---
name: research-curator
description: Conduct bounded, evidence-first Product Management research and convert reviewed findings into ProductOS entities and eval proposals. Use when executing or reviewing a ProductOS research task, not for ordinary product advice.
---

# Research Curator

Produce traceable knowledge that improves a defined ProductOS decision behavior. Do not optimize for content volume.

## Required boundaries

- Start from a bounded research task with a question, scope, exclusions, expected outputs, competing views, and acceptance criteria.
- Search existing IDs, terminology, sources, and relationships before creating entities.
- Prefer original and primary material when practical, but assess relevance, method, recency, limitations, and incentives independently from authority class.
- Separate source statements, observations, interpretation, and recommendation.
- Record precise locators and contradicting evidence; never invent a citation or silently resolve disagreement.
- Store metadata and original synthesis, not unauthorized copies of source material.
- Do not create a framework entry merely because a source names a method.
- Do not approve high-impact claims without review when independent review is available.

## Workflow

Move the task through intake, source planning, collection, analysis, synthesis, review, and publication. Create only the source, claim, concept, framework, terminology, decision-pattern, relationship, anti-pattern, and eval changes supported by the task.

Keep research notes as provenance. Canonical knowledge belongs under `knowledge/<entity-type>/<id>.yaml`; narrative synthesis belongs under `docs/`.

After publishing, rebuild indexes, run repository validation, inspect duplicate warnings, and propose regression cases for any changed reasoning behavior.

## References

- Read [`../../../research/methodology.md`](../../../research/methodology.md) when defining or executing a research task.
- Read [`../../../docs/foundations/source-quality-model.md`](../../../docs/foundations/source-quality-model.md) when selecting or reviewing sources.
- Read [`references/entity-extraction.md`](references/entity-extraction.md) when converting research into canonical entities.
- Read [`references/review-protocol.md`](references/review-protocol.md) when reviewing a task or preparing publication.

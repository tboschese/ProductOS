# ProductOS Architecture

**Status:** Phase 0 baseline
**Architecture version:** 0.1.0

## Objective

ProductOS is a shared reasoning substrate for Product Management skills. The initial product surface will be a Staff Product Manager skill; the durable product is the combination of reasoning contracts, structured knowledge, provenance, terminology, and behavior evals beneath it.

## Runtime boundary

The first implementation is repository-native:

- Markdown for instructions, policies, and narrative synthesis;
- YAML for canonical structured entities;
- JSON Schema for machine-verifiable contracts;
- Python for deterministic validation and index generation;
- repository skills for task-specific behavior.

Phase 0 deliberately excludes a graph database, vector database, RAG service, SaaS UI, and model-specific orchestration. These can be introduced only after a measured retrieval problem exists.

## System layers

```text
Interaction language
        ↓
Product skills
        ↓
Reasoning and decision contracts
        ↓
Knowledge, evidence, terminology, and relationships
        ↓
Research and editorial workflow
        ↓
Schemas, validators, and evals
```

Dependencies point downward. Skills may select and apply knowledge; they do not own canonical knowledge.

## Sources of truth

| Concern | Canonical representation | Derived or supporting representation |
|---|---|---|
| Architecture and policy | Root and foundation Markdown | ADR summaries and README links |
| Structured entities | One YAML file per entity under `knowledge/<entity-type>/` | Generated indexes |
| Research process | Files under `research/` | Extracted knowledge entities |
| Terminology | Structured terminology entities | Localized presentation in skills |
| Skill behavior | A skill's `SKILL.md` | Its references, scripts, and assets |
| Evaluation cases | Files under `evals/cases/` and `evals/multilingual/` | Reports under `evals/results/` |

Narrative documents must not silently duplicate canonical entity fields. When prose interprets an entity, it links to the canonical ID.

## Capability ontology

The capability model in the specification mixes several kinds of concepts. ProductOS therefore uses facets rather than treating every heading as a peer domain:

- `capabilities`: reasoning abilities such as decision making and systems thinking;
- `practices`: discovery, research, experimentation, planning, and delivery;
- `contexts`: B2B, B2C, enterprise, SaaS, marketplace, and internal products;
- `product_types`: platform, API, data, developer, and AI products;
- `roles_interfaces`: Staff PM, leadership, Product Ops, Sales, Customer Success, and Design;
- `constraints`: privacy, security, accessibility, regulation, ethics, and organizational limits.

Every canonical entity has one `primary_domain` and may have multiple facets. This provides ownership without duplicating knowledge.

## Entity lifecycle

Canonical entities use stable kebab-case IDs and one of these states:

```text
draft → in_review → approved → deprecated
```

Every entity carries a schema version. Approved entities require provenance and review metadata. Breaking schema changes require a migration plan and a schema-version increment.

## Evidence and provenance

ProductOS separates dimensions that the project specification originally combined:

- **epistemic status:** fact, observation, interpretation, assumption, hypothesis, opinion, recommendation, or unknown;
- **evidence modality:** quantitative, qualitative, market, business, technical, organizational, regulatory, mixed, or none;
- **source authority:** A through E, describing provenance class rather than truth;
- **confidence:** very low through very high, expressed qualitatively to avoid false precision;
- **locator:** the exact page, section, timestamp, dataset slice, or other verifiable location supporting a claim.

A source's authority does not automatically determine a claim's confidence. Relevance, method quality, recency, limitations, and contradictory evidence still matter.

## Relationships

Relationships are first-class entities with a subject, predicate, and object. The relationship registry is canonical; duplicated relationship fields in concepts or frameworks are not authoritative.

Initial predicates are:

```text
supports, contradicts, alternative_to, complements, derived_from,
requires, tests, measures, influences, causes, mitigates, used_for
```

## Reasoning contract

Phase 1 will implement a flexible decision record containing:

1. context;
2. decision question or diagnostic intent;
3. problem framing;
4. evidence and unknowns;
5. dominant uncertainty;
6. competing hypotheses;
7. viable options;
8. methods for reducing uncertainty;
9. trade-offs;
10. recommendation and confidence;
11. execution steps;
12. measurement;
13. learning and updates.

This is an internal rigor contract, not a requirement to expose hidden chain-of-thought. User-facing output should communicate conclusions, evidence, uncertainty, trade-offs, and next actions at an appropriate level.

## Multilingual architecture

English is canonical for IDs, schemas, taxonomy, and knowledge. Localized terminology maps `en`, `pt-BR`, and `es` labels and aliases to the same canonical entity. Multilingual eval variants share a `case_family_id` so reasoning equivalence can be assessed independently from writing quality.

## Evaluation architecture

ProductOS separates:

- deterministic structural validation;
- behavior scoring against expected and forbidden behaviors;
- multilingual equivalence checks;
- regression and holdout suites.

Deterministic scripts must not attempt to encode product judgment. Behavior scoring requires a declared judge protocol and periodic human calibration.

## Security and content policy

- Skills are reviewed as privileged instructions before release.
- Research stores source metadata, precise locators, and original synthesis rather than unauthorized copies of source material.
- Secrets and API keys never belong in the repository.
- Network and write-capable skill actions require explicit scope and appropriate approval boundaries.

## Deferred decisions

- final open-source license;
- model and judge configuration for automated evals;
- retrieval/indexing implementation after usage evidence exists;
- hosting or external service architecture;
- specialized ProductOS skills beyond Staff PM and Research Curator.

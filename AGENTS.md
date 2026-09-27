# ProductOS

## Mission

Build an evidence-based, multilingual Product Management knowledge and reasoning system.

## Principles

- Evidence over opinion.
- Prefer primary sources when practical.
- Frameworks are tools, not answers.
- Reasoning precedes artifact generation.
- Distinguish facts, observations, interpretations, assumptions, hypotheses, opinions, recommendations, and unknowns.
- Preserve meaningful contradictions.
- Avoid false precision and invented sources.
- Keep canonical knowledge in English; interaction language must not change reasoning quality.

## Repository map

- `ARCHITECTURE.md`: boundaries, data ownership, and system contracts.
- `ROADMAP.md`: delivery sequence and quality gates.
- `docs/foundations/`: foundational models and policies.
- `knowledge/`: canonical structured knowledge, populated after Phase 0.
- `research/`: bounded research workflow and review states.
- `evals/`: behavior evaluation strategy, rubric, cases, and results.
- `schemas/`: versioned JSON Schemas for structured artifacts.
- `.agents/skills/`: executable skills, added only when their release gates are met.

## Rules

- Read only the documents relevant to the current change.
- Before adding knowledge, search existing IDs, concepts, terminology, and sources.
- Every material claim requires traceable provenance and documented limitations.
- Do not create domain knowledge, frameworks, or skills without their required schemas and eval coverage.
- Keep `AGENTS.md` concise; put detailed guidance in the relevant subsystem documentation.
- Run `python scripts/validate_repository.py` after structural or schema changes.
- Inspect the seed suite with `python -m scripts.run_evals --suite seed` after changes to reasoning, skill instructions, or knowledge selection; run scored regression evals once a judge protocol is configured.

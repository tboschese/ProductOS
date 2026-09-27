# ProductOS

ProductOS is an evidence-based, multilingual Product Management knowledge and reasoning system. Its purpose is to improve product decisions, not to maximize framework recall or artifact generation.

## Status

The repository is in **Phase 0 — Bootstrap**. It contains architecture, research, terminology, source-quality, schema, and evaluation contracts. It intentionally does not yet contain broad Product Management research, framework registries, or released skills.

## Design principles

- Reasoning before frameworks.
- Evidence and provenance before confidence.
- Explicit uncertainty and competing hypotheses.
- Recommendations proportional to available evidence.
- Canonical English knowledge with equivalent interaction quality in English, Brazilian Portuguese, and Spanish.
- Progressive disclosure instead of a monolithic prompt.

## Getting started

Requires Python 3.9 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python scripts/validate_repository.py
pytest
```

## Repository guide

- [Project specification](PROJECT_SPEC.md)
- [Architecture](ARCHITECTURE.md)
- [Roadmap](ROADMAP.md)
- [Phase 0 architecture review](docs/phase-0-review.md)
- [Research methodology](research/methodology.md)
- [Evaluation strategy](evals/strategy.md)
- [Contribution guide](CONTRIBUTING.md)

## Scope boundary

Phase 0 establishes contracts and executable validation only. Knowledge expansion begins after the architecture and evaluation gates pass.

No open-source license has been selected yet. Until one is added, normal copyright restrictions apply.

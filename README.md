# ProductOS

ProductOS is an evidence-based, multilingual Product Management knowledge and reasoning system. Its purpose is to improve product decisions, not to maximize framework recall or artifact generation.

## Status

The repository is at **0.2.0-alpha.1 — Reasoning vertical slice**. It contains the Phase 0 foundation, Product Reasoning Engine v0, decision/evidence/uncertainty/risk contracts, a narrow Staff Product Manager skill, and a 20-case seed eval suite. Broad Product Management research and scored behavioral baselines remain intentionally pending.

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
- [0.2.0 alpha review](docs/releases/0.2.0-alpha.1.md)
- [Research methodology](research/methodology.md)
- [Evaluation strategy](evals/strategy.md)
- [Contribution guide](CONTRIBUTING.md)

## Scope boundary

Phase 0 establishes contracts and executable validation only. Knowledge expansion begins after the architecture and evaluation gates pass.

No open-source license has been selected yet. Until one is added, normal copyright restrictions apply.

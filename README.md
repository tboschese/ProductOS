# ProductOS

ProductOS is an evidence-based, multilingual Product Management knowledge and reasoning system. Its purpose is to improve product decisions, not to maximize framework recall or artifact generation.

## Status

The repository is at **0.3.0-alpha.6 — Research and evaluation infrastructure with a local runtime preview**. It contains the Phase 0 foundation, Product Reasoning Engine v0, Staff Product Manager and Research Curator skills, structured registries, cross-reference validation, deterministic indexes and source-freshness enforcement, a 21-case seed eval suite, blind exports, snapshot-based reporting, an opt-in behavioral pilot executor, and an optional [local terminal](docs/terminal.md) that uses the user's own AI connection. A [first observed pilot](evals/baselines/seed-pilot-2026-10-05/README.md) is recorded; its multilingual gate failed and its judge remains uncalibrated. The first bounded knowledge slice is `in_review`; broad research and a calibrated scored baseline remain intentionally pending.

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
- [0.3.0 alpha review](docs/releases/0.3.0-alpha.1.md)
- [0.3.0 alpha.2 review](docs/releases/0.3.0-alpha.2.md)
- [0.3.0 alpha.3 review](docs/releases/0.3.0-alpha.3.md)
- [0.3.0 alpha.4 review](docs/releases/0.3.0-alpha.4.md)
- [0.3.0 alpha.5 review](docs/releases/0.3.0-alpha.5.md)
- [0.3.0 alpha.6 review](docs/releases/0.3.0-alpha.6.md)
- [Terminal usage](docs/terminal.md)
- [Research methodology](research/methodology.md)
- [Evaluation strategy](evals/strategy.md)
- [Interface options](docs/design/interface-options.md)
- [Contribution guide](CONTRIBUTING.md)

## Scope boundary

Phase 0 establishes contracts and executable validation only. Knowledge expansion begins after the architecture and evaluation gates pass.

No open-source license has been selected yet. Until one is added, normal copyright restrictions apply.

# Changelog

All notable changes to ProductOS will be documented here.

The format follows Keep a Changelog principles and the project uses semantic versioning for milestones.

## [Unreleased]

## [0.3.0-alpha.2] — 2026-09-27

### Added

- Versioned behavioral eval-run schema with complete positive and negative fixtures.
- Reproducible judge protocol covering blind generation, repetitions, calibration, and gate
  interpretation.
- Semantic result validation and deterministic aggregation for behavior coverage, forbidden
  behaviors, hard failures, critical dimensions, citations, and multilingual deltas.
- Suite-owned gate policies and tests proving that hard failures cannot be hidden by averages.

### Known limitations

- The repository contains no claimed behavioral baseline; synthetic test data only verifies the
  machinery.
- Judge calibration and an independently reviewed run remain pending.

## [0.3.0-alpha.1] — 2026-09-27

### Added

- Research Curator skill and review references.
- Per-entity knowledge registries and schemas for anti-patterns, cases, and playbooks.
- Cross-entity reference validation, deterministic indexes, and duplicate-label checks.
- First bounded research slice on decision quality versus outcome quality.
- Three reviewed source records, three claims, two concepts, multilingual terminology, relationships, an anti-pattern, a decision pattern, a playbook, and an eval case in `in_review` state.

### Changed

- Terminology entries now map explicitly to a canonical `concept_id`.
- The seed eval suite now contains 21 cases.

### Known limitations

- The first knowledge slice has not received independent editorial approval.
- No scored behavioral baseline or automated judge is configured.

## [0.2.0-alpha.1] — 2026-09-27

### Added

- Product Reasoning Engine v0 and decision, evidence, uncertainty, and risk models.
- Decision-record, evidence-item, hypothesis, uncertainty, risk, and eval-suite schemas.
- Narrow Staff Product Manager skill with progressive references and five initial decision patterns.
- Twelve canonical English eval families and eight linked Portuguese/Spanish variants.
- Seed regression manifest and deterministic eval packet runner.

### Changed

- Repository validation now checks eval-suite references and multilingual case families.
- Phase status now distinguishes structural readiness from unrun behavioral scoring.

### Known limitations

- No scored baseline or calibrated automated judge is configured.
- Skill behavior has passed structural validation but not independent forward-testing.

## [0.1.0] — 2026-09-26

### Added

- Phase 0 repository bootstrap.
- Architecture, roadmap, governance, and contribution documentation.
- Research methodology, source-quality model, and terminology model.
- Versioned JSON Schemas with positive and negative fixtures.
- Evaluation strategy and rubric skeleton.
- Deterministic repository validator and continuous integration workflow.

### Changed

- Canonicalized the original specification filename as `PROJECT_SPEC.md`.
- Moved the thin Staff PM integration earlier in the roadmap to reduce integration risk.

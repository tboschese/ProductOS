# Changelog

All notable changes to ProductOS will be documented here.

The format follows Keep a Changelog principles and the project uses semantic versioning for milestones.

## [Unreleased]

### Added

- Judge-calibration kit: `scripts.calibrate prepare` freezes a shuffled, blind packet of sampled
  run responses and negative controls with a separate coordinator key and blank score sheet;
  `scripts.calibrate compare` validates returned sheets against the exact packet and run, then
  reports pairwise hard-failure, behavior-check, and dimension-score agreement plus control
  detection. It never marks a judge calibrated.
- Four labeled synthetic negative controls (three English, one Brazilian Portuguese) whose
  intended failures must be declared by their eval case.
- Schemas and fixtures for calibration controls, packets, keys, and score sheets.
- `evals/configs/seed-calibration.yaml`: the pilot executor with three repetitions.
- `docs/status.md`: shared, tool-independent working memory referenced from `AGENTS.md`.

### Fixed

- One tampered or unreadable analysis record no longer blocks opening the local workspace or
  listing other decisions' analyses; opening a specific analysis still verifies its integrity.

## [0.3.0-alpha.6] — 2026-10-06

### Added

- Optional local terminal (Python/Textual) and `productos` command interface for creating
  decisions, recording context and evidence, requesting analysis, and saving the user's choice.
- Separate personal workspace, defaulting to `~/.productos`, with schema-validated decision,
  analysis, and AI-connection records, revision checks, a single-writer lock, and SHA-256
  integrity checks for frozen inputs and original answers.
- User-owned AI connections: manual context export and response import, an installed Codex CLI
  adapter, and a configurable stdin/stdout command adapter, with timeout and cancellation.
- Optional structured output validated against the decision-record schema without promoting
  generated answers to approved decisions or canonical knowledge.
- `productos doctor` for local path and executable checks without model execution.
- Offline tests covering subprocess transport with fake assistants, timeout, cancellation,
  interrupted-invocation recovery, malformed output, and the terminal flow at 120×40 and 80×24.

### Changed

- The package now installs the `productos` entry point; the terminal dependency is the optional
  `terminal` extra.
- Architecture distinguishes the local product runtime (ADR-0008) from the evaluation-only pilot
  adapter (ADR-0007).

## [0.3.0-alpha.5] — 2026-10-05

### Added

- Opt-in Codex pilot execution with explicit configuration, frozen instructions, fresh contexts,
  verbatim responses, separate judging, and dimension-level evidence.
- Integrity-checked checkpoints and resumption without repeating completed generation or judging.
- Optional eval-run snapshot provenance recording the base commit, dirty-worktree state, CLI
  version, input files, and response hashes.
- Schema-validated seed pilot configuration and versioned generator/judge prompts.
- Offline tests for transport failures, interrupted runs, snapshot tampering, and calibration
  boundaries; archived-pilot provenance checks in repository validation.
- First observed 21-case pilot with archived responses, inputs, judgments, metrics, and a human
  calibration handoff; multilingual gate failed and release qualification remains pending.
- Terminal, local-browser, and desktop interface exploration with explicit implementation
  boundaries and a provisional recommendation by first-user profile.

### Changed

- Empty partial eval runs can represent prepared checkpoints; completed runs still require full
  assessment coverage.
- Evaluation architecture now distinguishes the model pilot adapter from deterministic validation
  and the repository-native product runtime.

## [0.3.0-alpha.4] — 2026-10-05

### Added

- Schema-validated generator and reviewer packets with separate export commands.
- Evaluation against exported reviewer cases and gate policy, with the packet SHA-256 recorded
  in the summary.
- Regression coverage for rubric leakage, packet integrity, and evaluation after live cases or
  gate policy change.

### Fixed

- Generator exports no longer expose expected behaviors, forbidden behaviors, hard failures,
  scoring notes, or gate thresholds.
- Generator and reviewer exports cannot share an output path.
- Source schema version is now explicitly `0.3.1`; canonical records and the valid fixture were
  migrated to identify the required freshness contract.
- JSON result summaries remain valid JSON when also written with `--output`.

## [0.3.0-alpha.3] — 2026-10-05

### Added

- Required temporal-stability and review-interval metadata for every registered source.
- Deterministic source freshness audit with optional, non-CI URL probing.
- CI enforcement for overdue and future-dated source verification records.
- Regression coverage for due-date boundaries, future verification, CLI exit codes, JSON
  reports, invalid freshness metadata, and offline URL-probe failure and fallback paths.

### Changed

- Research Curator review guidance now distinguishes freshness, reachability, and content
  verification.

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

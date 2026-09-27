# Evaluation strategy

## Purpose

ProductOS evals determine whether changes improve product judgment while preserving evidence discipline, multilingual fidelity, and communication quality.

## Evaluation layers

### Structural validation

Deterministic checks cover schema conformance, IDs, references, required provenance, locale shapes, and repository integrity. Structural validation is necessary but says nothing about decision quality.

### Behavioral evaluation

Each decision case declares:

- context and user input;
- applicable rubric dimensions;
- expected behaviors;
- forbidden behaviors;
- hard failures;
- evaluation notes and uncertainty.

Cases should permit multiple defensible answers. They evaluate reasoning behavior rather than exact wording.

### Multilingual equivalence

Localized variants share a `case_family_id` and expected reasoning. Language-specific scoring covers naturalness and terminology, while decision-quality scoring should remain materially equivalent across locales.

### Regression and holdouts

Frequently exercised cases form the regression suite. Unseen or restricted holdouts reduce overfitting. New failure modes become new cases rather than ad hoc prompt instructions whenever practical.

## Judge protocol

Automated scoring is introduced only with a recorded model, prompt version, sampling settings, run date, and repetition policy. Human reviewers calibrate the rubric and periodically measure judge agreement. A score is evidence about behavior, not objective truth.

## Initial scenario families

Phase 1 begins with scenarios spanning:

- retention decline after acquisition changes;
- enterprise feature pressure;
- strategy-to-OKR translation;
- regulated legacy modernization;
- AI feature proposals;
- instrumentation and metric conflicts;
- roadmap overload;
- pricing or packaging changes.

## Provisional release gates

Thresholds are calibrated after a baseline to avoid false precision. Initial targets are:

- no hard failure in evidence integrity, safety, or decision quality;
- average score of at least 3 on critical applicable dimensions;
- no critical dimension scored 0;
- traceable citations for at least 95% of material factual claims when citations are expected;
- average multilingual decision-quality difference no greater than 0.5 on the four-point scale.

These values are starting hypotheses, not permanent truths.

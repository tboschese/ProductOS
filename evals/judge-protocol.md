# Behavioral evaluation judge protocol

## Purpose

This protocol makes ProductOS behavioral results reproducible and auditable. It does not
make an automated judge authoritative. A score remains an assessment tied to a named rubric,
judge configuration, repository revision, and response.

## Run lifecycle

1. Freeze the suite, repository revision, skill version, generator configuration, and
   repetition count before generating responses.
2. Give the generator only the case input and context. Do not expose expected behaviors,
   forbidden behaviors, hard failures, scoring notes, or other cases.
3. Preserve each response verbatim in an eval-run record.
4. Judge each response independently against the case and rubric. Record evidence for every
   behavior check and every non-obvious score.
5. Validate the run structurally and semantically with `scripts.evaluate_results`.
6. Inspect both aggregate gates and case-level failures. Never use an average to waive a hard
   failure.
7. Mark the baseline provisional until judge calibration is complete.

## Required separation

The generator must not judge its own output in a single pass. When the same model family is
used for generation and judging, use separate contexts and record that dependence. Human,
model, and hybrid judging are supported, but all named participants and model settings must be
recorded.

## Scoring

Use the scale in [rubric.md](rubric.md). A completed assessment must score every dimension that
the case declares applicable. Use concise response excerpts or precise descriptions as evidence.

- Expected behavior: mark observed only when the response demonstrates it materially.
- Forbidden behavior: mark observed whenever the response exhibits it, even alongside stronger
  reasoning elsewhere.
- Hard failure: mark observed without averaging it away.
- Citation coverage: count only material factual claims for cases that declare citations
  expected. A link or citation counts as support only when it resolves to evidence relevant to
  the claim.

## Repetitions

Use at least three repetitions for stochastic model configurations during calibration. A
single deterministic run may be useful for a smoke test but is weak evidence of stable behavior.
Each response is a separate assessment identified by case ID and one-based repetition number.

## Calibration

Calibration compares at least two independent judges on a shared sample containing strong,
borderline, and failing responses.

1. Score independently before discussion.
2. Compare hard-failure classification, per-dimension scores, and behavior checks.
3. Resolve rubric ambiguities and record changes before rescoring.
4. Report agreement; do not label a judge `calibrated` merely because prompts were tested.
5. Recalibrate after material rubric, judge-model, or judge-prompt changes.

ProductOS does not yet prescribe a universal agreement coefficient or sample size. Those
thresholds must be selected with actual baseline distributions rather than invented in advance.

## Gate interpretation

The suite owns explicit provisional thresholds. `scripts.evaluate_results` calculates:

- hard-failure count;
- expected-behavior coverage;
- forbidden-behavior violations;
- mean and floor across suite-critical dimensions;
- citation coverage when citations are expected;
- maximum `decision_quality` score delta between English and localized variants.

A structurally valid run can pass behavioral gates while remaining ineligible for release. A
run becomes release-eligible only when it is complete, its judge is marked calibrated, the suite
and every selected case are approved, and all gates pass. Independent review is still required
for consequential release decisions.

## Commands

Export the case packet supplied to the response generator:

```bash
python -m scripts.run_evals --suite seed --export evals/results/seed-packet.json
```

Validate and summarize a populated eval-run file:

```bash
python -m scripts.evaluate_results evals/results/seed-run.json --suite seed
python -m scripts.evaluate_results evals/results/seed-run.json --suite seed --json
python -m scripts.evaluate_results evals/results/seed-run.json --suite seed --enforce-gates
```

Exit code `1` means the repository or run is invalid. With `--enforce-gates`, exit code `2`
means the run is valid but one or more behavioral gates failed.

Generated packets, runs, and reports remain under the ignored `evals/results/` directory unless
a maintainer deliberately promotes a sanitized artifact.

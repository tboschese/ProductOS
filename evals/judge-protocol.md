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

Export generator and reviewer packets together before generation. The generator packet is a
host-side collection of independent requests: send only one case's `input` and `context` per
fresh generation context, using its ID and locale for routing and result association. Do not
send the whole packet or the reviewer packet to the generator. An export file alone does not
enforce runtime isolation; the executor must preserve that separation.

Use the reviewer packet for scoring and result evaluation so later edits to cases or gate
policy cannot silently change the run's evaluation context. The summary records the SHA-256 of
the exact reviewer file. This freezes cases and policy only; the repository revision, skill
instructions, rubric, executor configuration, and raw responses must still be preserved as
required above.

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

`scripts.calibrate` prepares a blind, shuffled packet of sampled responses and labeled negative
controls, keeps provenance in a separate coordinator key, validates returned score sheets against
the exact packet, and reports agreement for every pair of judges. It does not mark a judge
calibrated. See [calibration/README.md](calibration/README.md).

`evals/configs/seed-calibration.yaml` declares the same pilot executor with three repetitions for
the stochastic-calibration run.

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

Export the blind generator packet and the separate reviewer snapshot:

```bash
python -m scripts.run_evals --suite seed --export evals/results/seed-generator.json \
  --export-review evals/results/seed-reviewer.json
```

Validate and summarize a populated eval-run file:

```bash
python -m scripts.evaluate_results evals/results/seed-run.json \
  --review-packet evals/results/seed-reviewer.json
python -m scripts.evaluate_results evals/results/seed-run.json \
  --review-packet evals/results/seed-reviewer.json --json
python -m scripts.evaluate_results evals/results/seed-run.json \
  --review-packet evals/results/seed-reviewer.json --enforce-gates
```

For exploratory evaluation against live repository cases, use `--suite seed` instead of
`--review-packet`. The result summary labels which context was used.

Exit code `1` means the repository or run is invalid. With `--enforce-gates`, exit code `2`
means the run is valid but one or more behavioral gates failed.

Generated packets, runs, and reports remain under the ignored `evals/results/` directory unless
a maintainer deliberately promotes a sanitized artifact.

## First pilot adapter

`scripts.execute_evals` freezes the configured instruction bundle, rubric, templates, packets,
and runner, then generates all responses before starting judgments. It runs one fresh CLI
context per call and rejects tool activity in the recorded events. Resume checks snapshot and
response hashes and does not regenerate completed responses or assessments.

The configuration under `evals/configs/seed-pilot.yaml` is a one-repetition smoke pilot with the
judge marked `pilot`. It does not meet the repetition requirement for calibration. When the
generator and judge use the same model, their fresh contexts provide procedural separation but
not statistical independence. Independent human review must test score and hard-failure
classification before the judge can be described as calibrated.

The adapter loads the full declared instruction bundle as text. Assessing installed skill
discovery, progressive references, tool use, and retrieval requires a different runtime test.

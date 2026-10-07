# Seed behavioral pilot — 2026-10-05

**Status:** Observed, completed, uncalibrated; release ineligible

The pilot generated and judged all 21 seed cases once: 13 English, four Brazilian Portuguese,
and four Spanish. Generation and judging used `gpt-6.1-sol` with high reasoning effort in
separate fresh contexts. All generation finished before judging began. These are observed
model responses to synthetic scenarios, not the synthetic output fixtures used in unit tests.

## Observations

The [summary](summary.json), calculated against the [frozen reviewer packet](snapshot/reviewer.json),
records the automated judge's assessments:

| Measure | Observed result | Frozen gate |
|---|---|---|
| Hard failures | 0 | 0 |
| Forbidden behavior violations | 0 | 0 |
| Expected behavior coverage | 88.6% | At least 80% |
| Critical dimension average | 3.68 / 4 | At least 3 |
| Lowest critical dimension score | 3 / 4 | At least 1 |
| Maximum multilingual dimension difference | 1 point across eight comparisons | At most 0.5 |
| Citation coverage | Not applicable: no assessable citation claims recorded | 95% when applicable |

The multilingual gate failed. `gates_passed` and `release_eligible` are both false. Passing
other provisional gates does not establish reliable competence: the judge remains `pilot`,
the run has one repetition, and editorial approval is absent. Not-applicable citation coverage
provides no evidence that citation handling is reliable.

Scores differed in both directions. The Portuguese retention and modernization responses
received lower decision-quality scores than their English variants; Portuguese and Spanish
enterprise-request responses received higher scores in several dimensions. A one-point
difference is an observation of this response-and-judge combination, not proof of a language
deficit or a stable improvement.

## Human calibration handoff

Review the responses blind to automated scores first, using the [frozen rubric](snapshot/rubric.md)
and exact behaviors in the reviewer packet. Then compare independent scores and explanations
with the [recorded assessments](run.json) and per-dimension evidence in the judgment files.

| Sample | Reason for inclusion | Response / judgment |
|---|---|---|
| English retention | Strong critical scores, despite one expected behavior being unobserved | [Response](generation/retention-decline-en-1.response.txt), [judgment](judging/retention-decline-en-1.judgment.json) |
| English pricing | Customer reasoning and trade-off awareness scored 2; test whether the rubric demands unsupported breadth | [Response](generation/pricing-change-en-1.response.txt), [judgment](judging/pricing-change-en-1.judgment.json) |
| English product sunset | Two expected behaviors unobserved; inspect partial coverage of compound behavior statements | [Response](generation/product-sunset-en-1.response.txt), [judgment](judging/product-sunset-en-1.judgment.json) |
| Portuguese retention | Paired decision-quality difference of one point | [Response](generation/retention-decline-pt-br-1.response.txt), [judgment](judging/retention-decline-pt-br-1.judgment.json) |
| English and Portuguese enterprise request | Largest spread across multiple dimensions, in favor of Portuguese | [English](generation/enterprise-feature-request-en-1.response.txt), [Portuguese](generation/enterprise-feature-request-pt-br-1.response.txt) |
| Spanish modernization | Completes a three-language decision family | [Response](generation/legacy-modernization-es-1.response.txt), [judgment](judging/legacy-modernization-es-1.judgment.json) |

There was no observed hard-failure response in this pilot. The calibration protocol still
requires failing examples; use explicitly labeled negative controls or subsequent observed
failures rather than relabeling this run. The [calibration workflow](../../calibration/README.md)
prepares this sample with the labeled controls as a blind packet and compares returned scores. At least three repetitions are required during
stochastic calibration. Do not change skill instructions or relax thresholds merely to match
these scores. Resolve response omissions, compound-behavior interpretation, and judge-anchor
disagreements before using automated scores for release decisions.

## Provenance and limitations

- [Run](run.json): base commit, dirty-worktree state, timestamps, model settings, complete
  responses, behavior checks, dimension scores, and snapshot/response SHA-256 values.
- `snapshot/`: configuration, runner, instruction bundle, prompts, rubric, and separate blind
  generator and full reviewer packets. The recorded base commit does not describe the supplied
  uncommitted content; the snapshots identify that content.
- `generation/`: original response text. Promotion checked byte equality with assessment
  response fields and every snapshot hash.
- `judging/`: JSON judgments, preserving dimension-level explanations. Transport events,
  thread identifiers, and stderr remain in ignored local results and are not published here.
- One judgment call timed out after 240 seconds. Resume reused all 21 saved generations and
  the first 11 judgments, then completed the remaining judgments.
- The same model generated and judged in separate contexts; this does not ensure independent
  judgment. The supplied bundle does not test native skill discovery, progressive reference
  loading, tools, or retrieval. No unskilled-model control was run, so this pilot cannot establish
  improvement attributable to the skill.

## Offline verification

```bash
python scripts/validate_repository.py
python -m scripts.evaluate_results evals/baselines/seed-pilot-2026-10-05/run.json \
  --review-packet evals/baselines/seed-pilot-2026-10-05/snapshot/reviewer.json
```

Adding `--enforce-gates` returns exit code 2 because the completed, structurally valid pilot
fails a behavioral gate. These commands make no model calls.

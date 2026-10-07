# Judge calibration

Calibration tests whether a judge's scores and failure classifications agree with independent
review. This directory holds the reusable inputs; generated packets, keys, and score sheets stay
under the ignored `evals/results/` directory.

## Negative controls

`controls/` contains synthetic failing responses, each labeled `negative_control` and tied to an
existing eval case. Every control declares the hard failures and forbidden behaviors it was
written to exhibit, and repository validation rejects any intended failure the case does not
declare. Controls supply the failing examples the [judge protocol](../judge-protocol.md) requires
without relabeling observed pilot responses.

Controls are written to be unambiguous, so detecting them is necessary but not sufficient: a judge
that catches every control can still disagree with reviewers on borderline responses. Controls are
synthetic; they are never evidence of how the system under test behaves.

## Workflow

1. Prepare a blind packet from a completed run, its frozen reviewer packet, a chosen sample of
   assessments, and the negative controls:

   ```bash
   python -m scripts.calibrate prepare \
     --run evals/baselines/seed-pilot-2026-10-05/run.json \
     --review-packet evals/baselines/seed-pilot-2026-10-05/snapshot/reviewer.json \
     --output evals/results/seed-pilot-calibration \
     --sample retention-decline-en#1 --sample pricing-change-en#1 \
     --sample product-sunset-en#1 --sample retention-decline-pt-br#1 \
     --sample enterprise-feature-request-en#1 --sample enterprise-feature-request-pt-br#1 \
     --sample legacy-modernization-es#1 --seed 20261006
   ```

   Without `--control`, every control whose case is in the reviewer packet is included.

2. Send each reviewer only `packet.json` and a copy of `score-template.json`. Keep `key.json`
   with the coordinator. Items are shuffled and carry opaque IDs; the packet contains the rubric,
   each case's criteria, and the response, but no automated scores, repetition numbers, or control
   labels.

3. Each reviewer fills in every applicable dimension score (0–4) and every behavior check with
   evidence, sets `reviewer.identity`, `scored_at`, and `independent_of_automated_scores`, and
   returns the sheet. Reviewers score before any discussion.

4. Compare all judges:

   ```bash
   python -m scripts.calibrate compare \
     --key evals/results/seed-pilot-calibration/key.json \
     --packet evals/results/seed-pilot-calibration/packet.json \
     --run evals/baselines/seed-pilot-2026-10-05/run.json \
     --scores reviewer-a.json --scores reviewer-b.json --output report.json
   ```

The report covers every pair of judges, including the automated judge on run items: hard-failure
classification agreement, behavior-check agreement, exact and within-one score agreement, mean
absolute and signed score differences overall and by dimension, score differences of two or more
points, and whether each judge detected every intended failure in each control.

## Limits

- The report never marks a judge `calibrated`. Maintainers review disagreements, resolve rubric
  ambiguities, record the decision, and recalibrate after material rubric or judge changes.
- No agreement threshold is prescribed; the protocol requires choosing one from observed
  distributions rather than inventing it in advance.
- The archived pilot judge never saw the controls, so control detection is reported only for
  judges that scored them. Testing the automated judge on controls requires a separate judged run.
- Blinding is procedural. Run files and controls are in the repository, so reviewers must agree
  not to consult them before scoring, and they attest to that in the score sheet.
- Item order and IDs hide provenance, but a case that appears twice signals that one copy may be a
  control or another repetition.

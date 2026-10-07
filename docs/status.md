# Current status

Shared working memory for every agent and contributor (Cursor, Codex, or human). Read it before
starting work; update it in the same commit when a task changes what is in progress, decided, or
next. Keep stable rules in `AGENTS.md` and durable decisions in [ADRs](decisions/README.md).

**Last updated:** 2026-10-06

## Where the project is

- Version `0.3.0-alpha.6`; see the [roadmap](../ROADMAP.md) and [changelog](../CHANGELOG.md).
- 0.2.0 exit item still open: a calibrated, independently reviewed baseline. The
  [first seed pilot](../evals/baselines/seed-pilot-2026-10-05/README.md) passed every gate
  except multilingual (maximum delta 1 against a 0.5 threshold), with a `pilot` judge and one
  repetition.
- 0.3.0: the first knowledge slice (`res-001`, decision quality versus outcome quality) awaits
  independent review.
- Optional local terminal (`productos`) is implemented; see [terminal guide](terminal.md).

## In progress

- Judge calibration. The [calibration kit](../evals/calibration/README.md) is implemented. A
  blind packet for the pilot sample (7 responses and 4 negative controls) can be regenerated
  under `evals/results/seed-pilot-calibration/` with the command in that README.
- Waiting on: at least two independent reviewers to score `packet.json`, then
  `python -m scripts.calibrate compare`.

- Automated judging of the 4 negative controls: `scripts.calibrate judge-controls` is
  implemented and tested with a fake judge, but has not produced results. In Cursor on
  2026-10-06 the bundled Codex CLI (0.158.0-alpha.2.1, ChatGPT login, no API key) refused the
  pilot judge model `gpt-6.1-sol`; the pilot used CLI 0.160.0. Run it from Codex outside Cursor:

  ```bash
  python -m scripts.calibrate judge-controls \
    --archive evals/baselines/seed-pilot-2026-10-05 \
    --output evals/results/control-judging-2026-10-06
  ```

  Then record which controls were detected here. Do not substitute another judge model; that
  would not test the pilot judge.

## Next candidates

- Run `evals/configs/seed-calibration.yaml` (three repetitions; makes model calls).
- Independent review of `res-001`.
- 0.4.0 research. Five bounded tasks are drafted in `research/backlog/` (all `draft`; source
  plans list candidates still to verify). Suggested order, by how many seed cases each affects:
  1. `res-003-customer-evidence-quality` (rubric hard failure on stakeholder requests);
  2. `res-002-reversibility-and-evidence-threshold`;
  3. `res-004-strategy-as-coherent-choices`;
  4. `res-005-second-order-effects-and-metric-gaming`;
  5. `res-006-when-product-intuition-is-trustworthy` (may propose rubric guidance; apply only
     after calibration).
  Executing a task (sources, claims, canonical entities) needs independent review before
  approval, and should not start before calibration unless deliberately reprioritized.

## Recent decisions

- 2026-10-06: Do not change skill instructions or relax gate thresholds to match pilot scores;
  resolve calibration first.
- 2026-10-06: Calibration reports agreement only; maintainers decide whether a judge is
  calibrated, and no agreement threshold is set before observing real distributions.
- 2026-10-06: Workspace listing and recovery tolerate one damaged analysis record; opening or
  finishing a specific analysis still verifies integrity.

## Open questions

- Who are the independent reviewers for calibration and for `res-001`?
- Which agreement statistic and threshold will define `calibrated` once real scores exist?

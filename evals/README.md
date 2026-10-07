# ProductOS evals

Evals test realistic product decisions, not framework trivia.

## Structure

- `cases/`: canonical English decision scenarios.
- `multilingual/`: linked `pt-BR` and `es` variants.
- `expected-behaviors/`: reusable behavior definitions.
- `anti-patterns/`: reusable forbidden-behavior definitions.
- `regression/`: curated suites and holdout manifests.
- `configs/`: schema-validated, explicitly chosen pilot execution settings.
- `calibration/`: labeled synthetic negative controls and the blind judge-calibration workflow.
- `prompts/`: versioned generation and judgment templates.
- `results/`: generated reports; ignored except for the directory placeholder.

See [strategy.md](strategy.md) and [rubric.md](rubric.md).

Behavioral runs conform to `schemas/eval-run.schema.json`. See
[judge-protocol.md](judge-protocol.md) for the blind-generation, scoring, calibration, and gate
workflow. Generated response packets and result reports stay ignored under `results/`; schema
fixtures and unit tests exercise the contract without claiming a real baseline.

Evaluation packets conform to `schemas/eval-packet.schema.json`. Generator packets contain
only routing metadata, input, and context. Reviewer packets preserve full cases and gate policy
for later evaluation with `--review-packet`; they must never enter generator contexts.

Use `scripts.execute_evals` for an opt-in behavioral pilot. It preserves a frozen snapshot and
checkpointed responses and judgments under `results/`. `source_snapshot` in the eval-run record
identifies the supplied inputs, runner, CLI version, and response hashes. The base commit plus
the declared snapshot identifies a dirty-worktree run; it must not be presented as a clean
execution of that commit alone. Empty `partial` runs are valid preparation checkpoints;
`completed` runs still require every declared case and repetition.

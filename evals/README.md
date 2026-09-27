# ProductOS evals

Evals test realistic product decisions, not framework trivia.

## Structure

- `cases/`: canonical English decision scenarios.
- `multilingual/`: linked `pt-BR` and `es` variants.
- `expected-behaviors/`: reusable behavior definitions.
- `anti-patterns/`: reusable forbidden-behavior definitions.
- `regression/`: curated suites and holdout manifests.
- `results/`: generated reports; ignored except for the directory placeholder.

See [strategy.md](strategy.md) and [rubric.md](rubric.md).

Behavioral runs conform to `schemas/eval-run.schema.json`. See
[judge-protocol.md](judge-protocol.md) for the blind-generation, scoring, calibration, and gate
workflow. Generated response packets and result reports stay ignored under `results/`; schema
fixtures and unit tests exercise the contract without claiming a real baseline.

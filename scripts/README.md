# Deterministic scripts

Scripts validate repository structure and data contracts. They must not encode Product Management judgment.

Current entry point:

```bash
python scripts/validate_repository.py
```

Inspect the seed behavior suite or export an unscored packet with:

```bash
python -m scripts.run_evals --suite seed --list
python -m scripts.run_evals --suite seed --export evals/results/seed-packet.json
```

The runner does not assign product-judgment scores. Automated judging is added only after its model configuration and human-calibration protocol are approved.

Build or verify deterministic knowledge indexes with:

```bash
python -m scripts.build_indexes --write
python -m scripts.build_indexes --check
```

Check deterministic concept and terminology collisions with:

```bash
python -m scripts.check_duplicates
```

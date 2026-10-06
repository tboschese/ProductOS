# Repository and evaluation scripts

Validation and reporting scripts check repository structure and data contracts. They must not
encode Product Management judgment. The opt-in pilot executor below makes declared model calls;
its judgments are observations requiring review, not deterministic validation.

Current entry point:

```bash
python scripts/validate_repository.py
```

Inspect the seed behavior suite or export separate generator and reviewer packets with:

```bash
python -m scripts.run_evals --suite seed --list
python -m scripts.run_evals --suite seed --export evals/results/seed-generator.json \
  --export-review evals/results/seed-reviewer.json
```

`--export` uses an allowlist: each generator case contains only its ID, locale, user input, and
context. `--export-review` includes full case criteria and the suite gate policy, and must stay
outside generator contexts. Both exports conform to `schemas/eval-packet.schema.json`.

The packet runner does not assign product-judgment scores. The opt-in executor uses a declared
pilot configuration and judge protocol; calibration remains required for release eligibility.

Validate, summarize, and optionally enforce the gates on a populated result file with:

```bash
python -m scripts.evaluate_results evals/results/seed-run.json --suite seed
python -m scripts.evaluate_results evals/results/seed-run.json --suite seed --enforce-gates
python -m scripts.evaluate_results evals/results/seed-run.json \
  --review-packet evals/results/seed-reviewer.json --enforce-gates
```

The result evaluator computes deterministic aggregates from recorded assessments; it never
generates responses or assigns judgment scores. `--review-packet` uses the exported cases and
thresholds and records the packet SHA-256 in the summary. `--suite` uses current repository data;
the two options are mutually exclusive. Archive the reviewer packet alongside the responses so
later case edits do not change the evaluation context.

Freeze a behavioral pilot without calling a model, then execute or resume it with:

```bash
python -m scripts.execute_evals --config evals/configs/seed-pilot.yaml \
  --output evals/results/seed-pilot --prepare-only
python -m scripts.execute_evals --config evals/configs/seed-pilot.yaml \
  --output evals/results/seed-pilot --resume
```

Requires an authenticated Codex CLI. The adapter follows the
[official non-interactive CLI documentation](https://learn.chatgpt.com/docs/non-interactive-mode).
An execution makes one generation and one judgment call per case and repetition. Each call
gets a fresh workspace, supplied text instructions, and read-only permissions; tool activity
invalidates the call. A new run requires a new directory. Resume verifies frozen file hashes,
executor metadata, response checkpoints, configuration, and runner identity before proceeding.

The seed pilot explicitly sets `gpt-6.1-sol` with high reasoning effort, one repetition, and a
judge marked `pilot`. It evaluates the bundled instructions rather than installed
skill routing or reference-loading behavior. Same-model judging requires independent calibration
before release. Model calls never run in CI.

Build or verify deterministic knowledge indexes with:

```bash
python -m scripts.build_indexes --write
python -m scripts.build_indexes --check
```

Check deterministic concept and terminology collisions with:

```bash
python -m scripts.check_duplicates
```

Audit source review deadlines deterministically, with optional best-effort URL probes:

```bash
python -m scripts.audit_sources --fail-stale
python -m scripts.audit_sources --check-links
```

Only the freshness check runs in CI. External reachability is deliberately excluded because
transient network behavior must not make repository validation nondeterministic.

Use `--as-of YYYY-MM-DD` to reproduce freshness results for a fixed audit date, `--json` for
machine-readable output, and `--output PATH` to save the same report to a file. A source is fresh
through its due date and overdue on the following day. Future verification dates fail the gate.

Exit code `1` means invalid repository data; `2` means a freshness failure with `--fail-stale`;
`3` means a failed URL probe with `--check-links`. Link failure takes precedence if both checks
fail. Without `--fail-stale`, freshness findings are reported without causing a nonzero exit.

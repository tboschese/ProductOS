# Contributing

ProductOS is in early architectural development. Contributions should improve decision quality, evidence quality, or the reliability of the system rather than add undifferentiated content.

## Before contributing

1. Read the relevant architecture or foundation document.
2. Search existing IDs and terminology before creating a new entity.
3. Define the decision or failure mode the change improves.
4. Add or update eval coverage for behavior changes.

## Research contributions

Research must use a bounded task, record competing perspectives and limitations, and include precise source provenance. Do not commit copyrighted source copies, credentials, personal research data, or confidential material.

## Validation

```bash
python scripts/validate_repository.py
pytest
ruff check .
```

## Change discipline

- Use stable kebab-case IDs.
- Keep canonical entity content in YAML and narrative synthesis in Markdown.
- Document meaningful architecture changes with an ADR.
- Treat breaking schema changes as migrations.
- Do not weaken existing evals solely to make a change pass.

The repository does not yet declare an open-source license or a formal external-contribution policy.

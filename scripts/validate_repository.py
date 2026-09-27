#!/usr/bin/env python3
"""Validate ProductOS Phase 0 repository contracts."""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

import yaml
from jsonschema import FormatChecker
from jsonschema.protocols import Validator
from jsonschema.validators import validator_for
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
VALID_FIXTURES = ROOT / "tests" / "fixtures" / "valid"
INVALID_FIXTURES = ROOT / "tests" / "fixtures" / "invalid"

REQUIRED_PATHS = (
    "AGENTS.md",
    "README.md",
    "PROJECT_SPEC.md",
    "ARCHITECTURE.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    ".agents/skills",
    "docs/foundations",
    "docs/decisions",
    "knowledge",
    "research/methodology.md",
    "evals/strategy.md",
    "evals/rubric.md",
    "schemas",
    "scripts",
)

SCHEMA_BY_CONTENT_PARENT = {
    "sources": "source",
    "claims": "claim",
    "concepts": "concept",
    "frameworks": "framework",
    "terminology": "terminology",
    "decision-patterns": "decision-pattern",
    "relationships": "relationship",
    "backlog": "research-task",
    "active": "research-task",
    "cases": "eval-case",
    "multilingual": "eval-case",
    "regression": "eval-suite",
}

MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class ProductOSLoader(yaml.SafeLoader):
    """Safe YAML loader that preserves ISO dates as schema-valid strings."""


ProductOSLoader.yaml_implicit_resolvers = {
    key: list(resolvers) for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
for resolver_key, resolver_values in ProductOSLoader.yaml_implicit_resolvers.items():
    ProductOSLoader.yaml_implicit_resolvers[resolver_key] = [
        (tag, pattern)
        for tag, pattern in resolver_values
        if tag != "tag:yaml.org,2002:timestamp"
    ]


class ValidationFailure(Exception):
    """Raised when repository validation finds one or more failures."""


def load_json(path: Path) -> Mapping[str, object]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_yaml(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return yaml.load(handle, Loader=ProductOSLoader)


def load_schemas() -> tuple[dict[str, Mapping[str, object]], Registry]:
    schemas: dict[str, Mapping[str, object]] = {}
    resources = []

    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        schema = load_json(path)
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            raise ValidationFailure(f"Schema {path.relative_to(ROOT)} has no $id")
        if schema_id in schemas:
            raise ValidationFailure(f"Duplicate schema $id: {schema_id}")
        schemas[schema_id] = schema
        resources.append((schema_id, Resource.from_contents(schema)))

    registry = Registry().with_resources(resources)
    return schemas, registry


def schema_name(schema: Mapping[str, object]) -> str:
    schema_id = str(schema["$id"])
    return schema_id.rsplit("/", 1)[-1].removesuffix(".schema.json")


def build_validators(
    schemas: Mapping[str, Mapping[str, object]], registry: Registry
) -> dict[str, Validator]:
    validators: dict[str, Validator] = {}
    for schema in schemas.values():
        validator_class = validator_for(schema)
        validator_class.check_schema(schema)
        validators[schema_name(schema)] = validator_class(
            schema,
            registry=registry,
            format_checker=FormatChecker(),
        )
    return validators


def fixture_pairs(directory: Path) -> Iterable[tuple[Path, str]]:
    for path in sorted(directory.glob("*.yaml")):
        yield path, path.stem


def format_errors(errors: Sequence[object]) -> str:
    details = []
    for error in errors:
        path = ".".join(str(part) for part in error.absolute_path) or "<root>"
        details.append(f"{path}: {error.message}")
    return "; ".join(details)


def validate_fixtures(validators: Mapping[str, Validator]) -> list[str]:
    failures: list[str] = []

    for path, name in fixture_pairs(VALID_FIXTURES):
        validator = validators.get(name)
        if validator is None:
            failures.append(f"No schema found for valid fixture {path.relative_to(ROOT)}")
            continue
        errors = sorted(validator.iter_errors(load_yaml(path)), key=lambda error: list(error.path))
        if errors:
            failures.append(
                f"Valid fixture {path.relative_to(ROOT)} failed: {format_errors(errors)}"
            )

    for path, name in fixture_pairs(INVALID_FIXTURES):
        validator = validators.get(name)
        if validator is None:
            failures.append(f"No schema found for invalid fixture {path.relative_to(ROOT)}")
            continue
        errors = list(validator.iter_errors(load_yaml(path)))
        if not errors:
            failures.append(f"Invalid fixture {path.relative_to(ROOT)} unexpectedly passed")

    return failures


def validate_required_paths() -> list[str]:
    return [
        f"Missing required path: {path}"
        for path in REQUIRED_PATHS
        if not (ROOT / path).exists()
    ]


def markdown_files() -> Iterable[Path]:
    for path in ROOT.rglob("*.md"):
        if ".git" not in path.parts and ".venv" not in path.parts:
            yield path


def validate_markdown_links() -> list[str]:
    failures: list[str] = []
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            target_path = (path.parent / target).resolve()
            if not target_path.exists():
                failures.append(
                    f"Broken Markdown link in {path.relative_to(ROOT)}: {raw_target}"
                )
    return failures


def content_files() -> Iterable[tuple[Path, str]]:
    roots = (ROOT / "knowledge", ROOT / "research", ROOT / "evals")
    for content_root in roots:
        for path in content_root.rglob("*.yaml"):
            schema_key = SCHEMA_BY_CONTENT_PARENT.get(path.parent.name)
            if schema_key:
                yield path, schema_key


def validate_content(validators: Mapping[str, Validator]) -> list[str]:
    failures: list[str] = []
    seen_ids: dict[str, Path] = {}
    records: list[tuple[Path, str, dict[str, object]]] = []

    for path, schema_key in content_files():
        data = load_yaml(path)
        errors = sorted(
            validators[schema_key].iter_errors(data), key=lambda error: list(error.path)
        )
        if errors:
            failures.append(f"{path.relative_to(ROOT)}: {format_errors(errors)}")
            continue

        if not isinstance(data, dict) or not isinstance(data.get("id"), str):
            failures.append(f"{path.relative_to(ROOT)} has no string id")
            continue

        entity_id = data["id"]
        previous = seen_ids.get(entity_id)
        if previous:
            failures.append(
                f"Duplicate entity id {entity_id}: {previous.relative_to(ROOT)} and "
                f"{path.relative_to(ROOT)}"
            )
        else:
            seen_ids[entity_id] = path

        records.append((path, schema_key, data))

    eval_cases = {
        str(data["id"]): data
        for _, schema_key, data in records
        if schema_key == "eval-case"
    }
    english_families = {
        str(data["case_family_id"])
        for _, schema_key, data in records
        if schema_key == "eval-case" and data.get("locale") == "en"
    }

    for path, schema_key, data in records:
        if schema_key == "eval-suite":
            for case_id in data["case_ids"]:
                if case_id not in eval_cases:
                    failures.append(
                        f"{path.relative_to(ROOT)} references missing eval case {case_id}"
                    )

        if schema_key == "eval-case" and path.parent.name == "multilingual":
            family_id = str(data["case_family_id"])
            if data.get("locale") == "en":
                failures.append(
                    f"{path.relative_to(ROOT)} is multilingual but uses locale en"
                )
            if family_id not in english_families:
                failures.append(
                    f"{path.relative_to(ROOT)} has no canonical English case for {family_id}"
                )

    return failures


def run_validation() -> list[str]:
    schemas, registry = load_schemas()
    validators = build_validators(schemas, registry)

    failures: list[str] = []
    failures.extend(validate_required_paths())
    failures.extend(validate_fixtures(validators))
    failures.extend(validate_content(validators))
    failures.extend(validate_markdown_links())
    return failures


def main() -> int:
    try:
        failures = run_validation()
    except (OSError, ValueError, ValidationFailure, yaml.YAMLError, json.JSONDecodeError) as error:
        print(f"validation error: {error}", file=sys.stderr)
        return 1

    if failures:
        print("ProductOS validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    schema_count = len(list(SCHEMA_DIR.glob("*.schema.json")))
    fixture_count = len(list(VALID_FIXTURES.glob("*.yaml"))) + len(
        list(INVALID_FIXTURES.glob("*.yaml"))
    )
    print(f"ProductOS validation passed ({schema_count} schemas, {fixture_count} fixtures).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

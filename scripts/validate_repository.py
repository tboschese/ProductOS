#!/usr/bin/env python3
"""Validate ProductOS Phase 0 repository contracts."""

from __future__ import annotations

import hashlib
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

KNOWLEDGE_SCHEMA_BY_PARENT = {
    "sources": "source",
    "claims": "claim",
    "concepts": "concept",
    "frameworks": "framework",
    "terminology": "terminology",
    "decision-patterns": "decision-pattern",
    "relationships": "relationship",
    "anti-patterns": "anti-pattern",
    "cases": "case",
    "playbooks": "playbook",
}

RESEARCH_SCHEMA_BY_PARENT = {
    "backlog": "research-task",
    "active": "research-task",
    "completed": "research-task",
}

EVAL_SCHEMA_BY_PARENT = {
    "cases": "eval-case",
    "multilingual": "eval-case",
    "regression": "eval-suite",
    "configs": "eval-config",
    "controls": "calibration-control",
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
    roots = (
        (ROOT / "knowledge", KNOWLEDGE_SCHEMA_BY_PARENT),
        (ROOT / "research", RESEARCH_SCHEMA_BY_PARENT),
        (ROOT / "evals", EVAL_SCHEMA_BY_PARENT),
    )
    for content_root, schema_map in roots:
        for path in content_root.rglob("*.yaml"):
            schema_key = schema_map.get(path.parent.name)
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

        if path.is_relative_to(ROOT / "knowledge") and path.stem != entity_id:
            failures.append(
                f"{path.relative_to(ROOT)} filename must match entity id {entity_id}"
            )

    ids_by_schema: dict[str, set[str]] = {}
    for _, schema_key, data in records:
        ids_by_schema.setdefault(schema_key, set()).add(str(data["id"]))

    knowledge_schema_keys = set(KNOWLEDGE_SCHEMA_BY_PARENT.values())
    knowledge_ids = {
        str(data["id"])
        for _, schema_key, data in records
        if schema_key in knowledge_schema_keys
    }

    def require_ids(
        path: Path, values: object, target_schema: str, field_name: str
    ) -> None:
        target_ids = ids_by_schema.get(target_schema, set())
        for value in values if isinstance(values, list) else []:
            if value not in target_ids:
                failures.append(
                    f"{path.relative_to(ROOT)} {field_name} references missing "
                    f"{target_schema} {value}"
                )

    def require_source_refs(path: Path, values: object, field_name: str) -> None:
        source_ids = ids_by_schema.get("source", set())
        for value in values if isinstance(values, list) else []:
            if isinstance(value, dict) and value.get("source_id") not in source_ids:
                failures.append(
                    f"{path.relative_to(ROOT)} {field_name} references missing source "
                    f"{value.get('source_id')}"
                )

    for path, schema_key, data in records:
        if schema_key == "source":
            require_ids(path, data.get("concept_ids", []), "concept", "concept_ids")
        elif schema_key == "claim":
            require_source_refs(path, data.get("supporting_sources", []), "supporting_sources")
            require_source_refs(
                path, data.get("contradicting_sources", []), "contradicting_sources"
            )
        elif schema_key == "concept":
            require_ids(path, data.get("claim_ids", []), "claim", "claim_ids")
        elif schema_key == "terminology":
            require_ids(path, [data.get("concept_id")], "concept", "concept_id")
        elif schema_key == "framework":
            require_source_refs(path, data.get("source_refs", []), "source_refs")
            require_ids(path, data.get("alternatives", []), "framework", "alternatives")
            require_ids(path, data.get("complements", []), "framework", "complements")
        elif schema_key == "decision-pattern":
            require_ids(path, data.get("claim_ids", []), "claim", "claim_ids")
            require_ids(
                path, data.get("anti_pattern_ids", []), "anti-pattern", "anti_pattern_ids"
            )
        elif schema_key == "relationship":
            for field_name in ("subject_id", "object_id"):
                value = data.get(field_name)
                if value not in knowledge_ids:
                    failures.append(
                        f"{path.relative_to(ROOT)} {field_name} references missing entity {value}"
                    )
            require_source_refs(path, data.get("source_refs", []), "source_refs")
        elif schema_key == "anti-pattern":
            require_ids(path, data.get("claim_ids", []), "claim", "claim_ids")
            require_ids(path, data.get("eval_case_ids", []), "eval-case", "eval_case_ids")
        elif schema_key == "case":
            require_source_refs(path, data.get("source_refs", []), "source_refs")
        elif schema_key == "playbook":
            require_ids(
                path,
                data.get("decision_pattern_ids", []),
                "decision-pattern",
                "decision_pattern_ids",
            )
            require_ids(path, data.get("claim_ids", []), "claim", "claim_ids")

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
            suite_cases = [
                eval_cases[case_id]
                for case_id in data["case_ids"]
                if case_id in eval_cases
            ]
            exercised_dimensions = {
                str(dimension)
                for case in suite_cases
                for dimension in case["applicable_dimensions"]
            }
            for dimension in data["gate_policy"]["critical_dimensions"]:
                if dimension not in exercised_dimensions:
                    failures.append(
                        f"{path.relative_to(ROOT)} gate policy references unexercised "
                        f"critical dimension {dimension}"
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

        if schema_key == "calibration-control":
            relative = path.relative_to(ROOT)
            if path.stem != data["id"]:
                failures.append(f"{relative} filename must match control id {data['id']}")
            case = eval_cases.get(str(data["case_id"]))
            if case is None:
                failures.append(f"{relative} references missing eval case {data['case_id']}")
                continue
            for field_name in ("hard_failures", "forbidden_behaviors"):
                for behavior in data["intended_failures"][field_name]:
                    if behavior not in case[field_name]:
                        failures.append(
                            f"{relative} intended {field_name} entry is not declared by "
                            f"{data['case_id']}: {behavior}"
                        )

    return failures


def validate_eval_archives(
    validators: Mapping[str, Validator], archive_root: Path | None = None
) -> list[str]:
    """Check archived pilot shape, file integrity, and verbatim response provenance."""
    archive_root = archive_root or ROOT / "evals" / "baselines"
    failures: list[str] = []
    for run_path in sorted(archive_root.rglob("run.json")):
        run = load_json(run_path)
        errors = list(validators["eval-run"].iter_errors(run))
        if errors:
            failures.append(f"{run_path}: {format_errors(errors)}")
            continue
        snapshot = run.get("source_snapshot")
        if not isinstance(snapshot, dict):
            failures.append(f"{run_path}: archived pilot requires source_snapshot")
            continue
        if run["run_status"] != "completed":
            failures.append(f"{run_path}: archived pilot must be completed")
        for relative, expected in snapshot["files"].items():
            path = (run_path.parent / relative).resolve()
            if not path.is_relative_to(run_path.parent.resolve()):
                failures.append(f"{run_path}: snapshot path escapes archive: {relative}")
            elif not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                failures.append(f"{run_path}: snapshot integrity failure: {relative}")
        for assessment in run["assessments"]:
            relative = (
                f"generation/{assessment['case_id']}-{assessment['repetition']}.response.txt"
            )
            expected = snapshot["files"].get(relative)
            response_digest = hashlib.sha256(assessment["response"].encode("utf-8")).hexdigest()
            if expected != response_digest:
                failures.append(f"{run_path}: response differs from its checkpoint: {relative}")
    return failures


def run_validation() -> list[str]:
    schemas, registry = load_schemas()
    validators = build_validators(schemas, registry)

    failures: list[str] = []
    failures.extend(validate_required_paths())
    failures.extend(validate_fixtures(validators))
    failures.extend(validate_content(validators))
    failures.extend(validate_eval_archives(validators))
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

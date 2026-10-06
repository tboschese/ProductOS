import hashlib
import json

import pytest

from scripts.validate_repository import (
    INVALID_FIXTURES,
    ROOT,
    VALID_FIXTURES,
    build_validators,
    load_schemas,
    load_yaml,
    validate_eval_archives,
    validate_markdown_links,
    validate_required_paths,
)


def test_required_paths_exist() -> None:
    assert validate_required_paths() == []


def test_json_schemas_are_valid() -> None:
    schemas, registry = load_schemas()
    validators = build_validators(schemas, registry)
    assert "source" in validators
    assert "eval-case" in validators
    assert "eval-run" in validators


def test_valid_fixtures_pass() -> None:
    schemas, registry = load_schemas()
    validators = build_validators(schemas, registry)

    for path in sorted(VALID_FIXTURES.glob("*.yaml")):
        errors = list(validators[path.stem].iter_errors(load_yaml(path)))
        assert errors == [], f"{path.relative_to(ROOT)}: {errors}"


def test_invalid_fixtures_fail() -> None:
    schemas, registry = load_schemas()
    validators = build_validators(schemas, registry)

    for path in sorted(INVALID_FIXTURES.glob("*.yaml")):
        errors = list(validators[path.stem].iter_errors(load_yaml(path)))
        assert errors, f"{path.relative_to(ROOT)} unexpectedly passed"


def test_markdown_links_resolve() -> None:
    assert validate_markdown_links() == []


def test_original_specification_is_canonicalized() -> None:
    assert (ROOT / "PROJECT_SPEC.md").is_file()
    assert not list(ROOT.glob("ProductOS — Complete Project Specification*.md"))


@pytest.mark.parametrize("corruption", [None, "checkpoint", "record", "escape", "missing_snapshot"])
def test_archived_pilots_verify_response_provenance(tmp_path, corruption) -> None:
    schemas, registry = load_schemas()
    validators = build_validators(schemas, registry)
    run = load_yaml(VALID_FIXTURES / "eval-run.yaml")
    run["run_status"] = "completed"
    run["completed_at"] = "2026-09-27T10:10:00Z"
    assessment = run["assessments"][0]
    relative = f"generation/{assessment['case_id']}-{assessment['repetition']}.response.txt"
    checkpoint = tmp_path / relative
    checkpoint.parent.mkdir()
    checkpoint.write_bytes(assessment["response"].encode("utf-8"))
    run["source_snapshot"] = {
        "revision_role": "base_commit", "worktree_dirty": True, "cli_version": "synthetic",
        "files": {relative: hashlib.sha256(checkpoint.read_bytes()).hexdigest()},
    }
    if corruption == "checkpoint":
        checkpoint.write_text("Altered checkpoint", encoding="utf-8")
    elif corruption == "record":
        assessment["response"] = "Altered response in the record"
    elif corruption == "escape":
        run["source_snapshot"]["files"]["../outside.txt"] = "a" * 64
    elif corruption == "missing_snapshot":
        run.pop("source_snapshot")
    (tmp_path / "run.json").write_text(json.dumps(run), encoding="utf-8")
    failures = validate_eval_archives(validators, tmp_path)
    assert bool(failures) == (corruption is not None)

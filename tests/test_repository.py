from scripts.validate_repository import (
    INVALID_FIXTURES,
    ROOT,
    VALID_FIXTURES,
    build_validators,
    load_schemas,
    load_yaml,
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

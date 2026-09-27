from scripts.check_duplicates import normalize, run_duplicate_checks


def test_normalize_is_case_and_whitespace_insensitive() -> None:
    assert normalize("  Product   Sense ") == normalize("product sense")


def test_repository_has_no_deterministic_duplicate_labels() -> None:
    assert run_duplicate_checks() == []

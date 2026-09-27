from scripts.run_evals import load_cases, load_suite, suite_cases


def test_seed_suite_resolves_all_cases() -> None:
    cases = load_cases()
    suite = load_suite("seed")
    selected = suite_cases(suite, cases)

    assert len(selected) == 21
    assert {case["locale"] for case in selected} == {"en", "pt-BR", "es"}


def test_multilingual_cases_have_english_family() -> None:
    cases = load_cases()
    english_families = {
        case["case_family_id"] for case in cases.values() if case["locale"] == "en"
    }

    for case in cases.values():
        if case["locale"] != "en":
            assert case["case_family_id"] in english_families

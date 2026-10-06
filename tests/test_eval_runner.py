import json
from copy import deepcopy

import pytest

from scripts import run_evals
from scripts.run_evals import export_packet, load_cases, load_suite, suite_cases
from scripts.validate_repository import build_validators, load_schemas


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


def test_generator_export_excludes_judging_fields_and_future_metadata(tmp_path) -> None:
    suite = load_suite("seed")
    selected = suite_cases(suite, load_cases())
    original = deepcopy(selected)
    selected[0]["future_review_hint"] = "SECRET_REVIEW_HINT"
    output = tmp_path / "generator.json"

    export_packet(suite, selected, output)
    packet = json.loads(output.read_text(encoding="utf-8"))
    assert packet["audience"] == "generator"
    assert "suite" not in packet
    assert "SECRET_REVIEW_HINT" not in output.read_text(encoding="utf-8")
    assert len(packet["cases"]) == len(suite["case_ids"])
    for exported, case in zip(packet["cases"], original):
        assert set(exported) == {"id", "locale", "input", "context"}
        assert exported["input"] == case["input"]
        assert exported["context"] == case["context"]
        assert exported["locale"] == case["locale"]
    selected[0].pop("future_review_hint")
    assert selected == original


def test_reviewer_export_preserves_full_cases_and_gate_policy(tmp_path) -> None:
    suite = load_suite("seed")
    selected = suite_cases(suite, load_cases())
    output = tmp_path / "reviewer.json"

    export_packet(suite, selected, output, audience="reviewer")
    packet = json.loads(output.read_text(encoding="utf-8"))
    assert packet["audience"] == "reviewer"
    assert packet["cases"] == selected
    assert packet["suite"] == suite


@pytest.mark.parametrize(
    "leak",
    ["expected_behaviors", "forbidden_behaviors", "hard_failures", "scoring_notes", "tags"],
)
def test_packet_schema_rejects_judging_fields_in_generator_cases(tmp_path, leak) -> None:
    suite = load_suite("seed")
    selected = suite_cases(suite, load_cases())
    output = tmp_path / "generator.json"
    export_packet(suite, selected, output)
    packet = json.loads(output.read_text(encoding="utf-8"))
    packet["cases"][0][leak] = selected[0][leak]

    schemas, registry = load_schemas()
    validator = build_validators(schemas, registry)["eval-packet"]
    assert list(validator.iter_errors(packet))


def test_packet_schema_rejects_gate_policy_in_generator_packet(tmp_path) -> None:
    suite = load_suite("seed")
    output = tmp_path / "generator.json"
    export_packet(suite, suite_cases(suite, load_cases()), output)
    packet = json.loads(output.read_text(encoding="utf-8"))
    packet["suite"] = suite

    schemas, registry = load_schemas()
    validator = build_validators(schemas, registry)["eval-packet"]
    assert list(validator.iter_errors(packet))


def test_reviewer_export_rejects_missing_rubric_before_writing(tmp_path) -> None:
    suite = load_suite("seed")
    selected = suite_cases(suite, load_cases())
    selected[0].pop("expected_behaviors")
    output = tmp_path / "reviewer.json"

    with pytest.raises(ValueError, match="Invalid reviewer packet"):
        export_packet(suite, selected, output, audience="reviewer")
    assert not output.exists()


def test_cli_rejects_shared_output_path_without_overwriting(monkeypatch, tmp_path) -> None:
    output = tmp_path / "packet.json"
    output.write_text("existing report", encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv", ["run_evals", "--export", str(output), "--export-review", str(output)]
    )
    with pytest.raises(SystemExit) as error:
        run_evals.main()
    assert error.value.code == 2
    assert output.read_text(encoding="utf-8") == "existing report"


def test_cli_exports_separate_generator_and_reviewer_packets(monkeypatch, capsys, tmp_path) -> None:
    generator = tmp_path / "generator.json"
    reviewer = tmp_path / "reviewer.json"
    monkeypatch.setattr(
        "sys.argv",
        ["run_evals", "--export", str(generator), "--export-review", str(reviewer)],
    )
    assert run_evals.main() == 0
    assert json.loads(generator.read_text(encoding="utf-8"))["audience"] == "generator"
    assert json.loads(reviewer.read_text(encoding="utf-8"))["audience"] == "reviewer"
    assert "scoring not run" in capsys.readouterr().out


def test_cli_reports_missing_suite_without_traceback(monkeypatch, capsys, tmp_path) -> None:
    monkeypatch.setattr("sys.argv", ["run_evals", "--suite", str(tmp_path / "missing.yaml")])
    assert run_evals.main() == 1
    assert "error:" in capsys.readouterr().err

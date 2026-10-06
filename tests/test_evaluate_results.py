import hashlib
import json
from copy import deepcopy

import pytest

from scripts import evaluate_results
from scripts.evaluate_results import (
    load_review_context,
    summarize_run,
    validate_run_semantics,
    validate_run_shape,
)
from scripts.run_evals import export_packet, load_cases, load_suite, suite_cases


def complete_run() -> tuple[dict, dict, dict]:
    cases = load_cases()
    suite = load_suite("seed")
    assessments = []
    for case_id in suite["case_ids"]:
        case = cases[case_id]
        assessments.append(
            {
                "case_id": case_id,
                "repetition": 1,
                "response": f"Synthetic test response for {case_id}.",
                "dimension_scores": {
                    dimension: 3 for dimension in case["applicable_dimensions"]
                },
                "expected_behavior_checks": [
                    {"behavior": behavior, "observed": True, "evidence": "Synthetic evidence."}
                    for behavior in case["expected_behaviors"]
                ],
                "forbidden_behavior_checks": [
                    {"behavior": behavior, "observed": False, "evidence": "Not observed."}
                    for behavior in case["forbidden_behaviors"]
                ],
                "hard_failure_checks": [
                    {"behavior": behavior, "observed": False, "evidence": "Not observed."}
                    for behavior in case["hard_failures"]
                ],
                "citation_check": {
                    "expected": bool(case.get("citations_expected", False)),
                    "material_claims": 0,
                    "supported_claims": 0,
                    "notes": "No citations expected in seed cases.",
                },
                "notes": "Synthetic test assessment, not an eval result.",
            }
        )

    run = {
        "id": "synthetic-seed-run",
        "schema_version": "0.3.0",
        "suite_id": suite["id"],
        "run_status": "completed",
        "started_at": "2026-09-27T10:00:00Z",
        "completed_at": "2026-09-27T10:10:00Z",
        "repository_revision": "7b43f2045789dddf1655f7447c301311f026fe9c",
        "system_under_test": {
            "id": "staff-product-manager",
            "version": "0.2.0-alpha.1",
            "instruction_path": ".agents/skills/staff-product-manager/SKILL.md",
        },
        "generator": {
            "type": "model",
            "identities": ["synthetic-generator"],
            "provider": "example",
            "model": "example-model",
            "prompt_version": "test-v1",
            "settings": {"temperature": 0},
        },
        "judge": {
            "type": "human",
            "identities": ["synthetic-reviewer"],
            "provider": None,
            "model": None,
            "prompt_version": None,
            "settings": {},
            "rubric_version": "0.3.0",
            "calibration_status": "calibrated",
        },
        "repetitions": 1,
        "assessments": assessments,
    }
    return run, suite, cases


def test_complete_run_is_valid_and_passes_provisional_gates() -> None:
    run, suite, cases = complete_run()

    assert validate_run_shape(run) == []
    assert validate_run_semantics(run, suite, cases) == []

    summary = summarize_run(run, suite, cases)
    assert summary["gates_passed"] is True
    assert summary["release_eligible"] is False
    assert summary["content_approved"] is False
    assert summary["metrics"]["maximum_multilingual_delta"] == 0


def test_release_eligibility_requires_approved_suite_and_cases() -> None:
    run, suite, cases = complete_run()
    suite = deepcopy(suite)
    cases = deepcopy(cases)
    suite["status"] = "approved"
    for case_id in suite["case_ids"]:
        cases[case_id]["status"] = "approved"

    summary = summarize_run(run, suite, cases)
    assert summary["content_approved"] is True
    assert summary["release_eligible"] is True


def test_hard_failure_cannot_be_hidden_by_average_scores() -> None:
    run, suite, cases = complete_run()
    run = deepcopy(run)
    assessment = next(
        item for item in run["assessments"] if item["hard_failure_checks"]
    )
    assessment["hard_failure_checks"][0]["observed"] = True

    summary = summarize_run(run, suite, cases)
    assert summary["metrics"]["critical_average"] == 3
    assert summary["metrics"]["hard_failures"] == 1
    assert summary["gates_passed"] is False


def test_semantics_require_every_declared_behavior_check() -> None:
    run, suite, cases = complete_run()
    run = deepcopy(run)
    run["assessments"][0]["expected_behavior_checks"].pop()

    failures = validate_run_semantics(run, suite, cases)
    assert any("must cover each declared expected_behaviors" in failure for failure in failures)


def test_review_context_preserves_exported_cases_policy_and_digest(tmp_path) -> None:
    run, suite, cases = complete_run()
    packet_path = tmp_path / "reviewer.json"
    export_packet(suite, suite_cases(suite, cases), packet_path, audience="reviewer")
    suite["gate_policy"]["minimum_critical_average"] = 4
    cases[suite["case_ids"][0]]["expected_behaviors"].append("New behavior after the run")

    frozen_suite, frozen_cases, digest = load_review_context(packet_path)
    assert frozen_suite["gate_policy"]["minimum_critical_average"] == 3
    assert validate_run_semantics(run, frozen_suite, frozen_cases) == []
    assert summarize_run(run, frozen_suite, frozen_cases)["gates_passed"] is True
    assert summarize_run(run, suite, cases)["gates_passed"] is False
    assert digest == hashlib.sha256(packet_path.read_bytes()).hexdigest()


def test_generator_packet_cannot_be_used_for_scoring(tmp_path) -> None:
    _, suite, cases = complete_run()
    packet_path = tmp_path / "generator.json"
    export_packet(suite, suite_cases(suite, cases), packet_path)
    with pytest.raises(ValueError, match="requires a reviewer packet"):
        load_review_context(packet_path)


@pytest.mark.parametrize(
    "corruption", ["suite_id", "duplicate_case", "missing_case", "unexercised_dimension"]
)
def test_review_context_rejects_inconsistent_snapshot(tmp_path, corruption) -> None:
    _, suite, cases = complete_run()
    packet_path = tmp_path / "reviewer.json"
    export_packet(suite, suite_cases(suite, cases), packet_path, audience="reviewer")
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    if corruption == "suite_id":
        packet["suite_id"] = "different-suite"
    elif corruption == "duplicate_case":
        packet["cases"].append(packet["cases"][0])
    elif corruption == "missing_case":
        packet["cases"].pop()
    else:
        packet["suite"]["gate_policy"]["critical_dimensions"].append("regulatory_reasoning")
        for case in packet["cases"]:
            case["applicable_dimensions"] = [
                dimension for dimension in case["applicable_dimensions"]
                if dimension != "regulatory_reasoning"
            ]
    packet_path.write_text(json.dumps(packet), encoding="utf-8")
    with pytest.raises(ValueError):
        load_review_context(packet_path)


def test_cli_scores_snapshot_without_loading_live_cases(monkeypatch, capsys, tmp_path) -> None:
    run, suite, cases = complete_run()
    packet_path = tmp_path / "reviewer.json"
    run_path = tmp_path / "run.json"
    summary_path = tmp_path / "summary.json"
    export_packet(suite, suite_cases(suite, cases), packet_path, audience="reviewer")
    run_path.write_text(json.dumps(run), encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        [
            "evaluate_results", str(run_path), "--review-packet", str(packet_path),
            "--json", "--output", str(summary_path), "--enforce-gates",
        ],
    )

    def unexpected_live_load(*args):
        pytest.fail("Snapshot scoring must not use live case or suite definitions")

    monkeypatch.setattr(evaluate_results, "load_cases", unexpected_live_load)
    monkeypatch.setattr(evaluate_results, "load_suite", unexpected_live_load)
    assert evaluate_results.main() == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed == json.loads(summary_path.read_text(encoding="utf-8"))
    assert printed["evaluation_context"] == {
        "source": "reviewer_packet",
        "sha256": hashlib.sha256(packet_path.read_bytes()).hexdigest(),
    }
    assert printed["release_eligible"] is False


def test_cli_rejects_live_suite_and_snapshot_together(monkeypatch) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["evaluate_results", "run.json", "--suite", "seed", "--review-packet", "packet.json"],
    )
    with pytest.raises(SystemExit) as error:
        evaluate_results.main()
    assert error.value.code == 2


def test_empty_preparation_checkpoint_is_valid_only_while_partial() -> None:
    run, suite, cases = complete_run()
    run["assessments"] = []
    run["run_status"] = "partial"
    run["completed_at"] = None
    assert validate_run_shape(run) == []
    assert validate_run_semantics(run, suite, cases) == []
    assert summarize_run(run, suite, cases)["release_eligible"] is False

    run["run_status"] = "completed"
    run["completed_at"] = "2026-09-27T10:10:00Z"
    assert validate_run_shape(run)
    assert any(
        "missing assessments" in error for error in validate_run_semantics(run, suite, cases)
    )

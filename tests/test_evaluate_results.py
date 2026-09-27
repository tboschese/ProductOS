from copy import deepcopy

from scripts.evaluate_results import summarize_run, validate_run_semantics, validate_run_shape
from scripts.run_evals import load_cases, load_suite


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

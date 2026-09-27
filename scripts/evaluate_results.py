#!/usr/bin/env python3
"""Validate and summarize a ProductOS behavioral evaluation run."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any

import yaml

from scripts.run_evals import load_cases, load_suite
from scripts.validate_repository import (
    ROOT,
    build_validators,
    format_errors,
    load_json,
    load_schemas,
    load_yaml,
    run_validation,
)


def load_run(path: Path) -> dict[str, Any]:
    data = load_json(path) if path.suffix.lower() == ".json" else load_yaml(path)
    if not isinstance(data, dict):
        raise ValueError("Evaluation run must be an object")
    return data


def validate_run_shape(run: dict[str, Any]) -> list[str]:
    schemas, registry = load_schemas()
    validator = build_validators(schemas, registry)["eval-run"]
    errors = sorted(validator.iter_errors(run), key=lambda error: list(error.path))
    return [format_errors(errors)] if errors else []


def _executor_failures(label: str, executor: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    automated = executor["type"] in {"model", "hybrid"}
    for field in ("provider", "model", "prompt_version"):
        value = executor[field]
        if automated and not value:
            failures.append(f"{label}.{field} is required for {executor['type']} execution")
        if not automated and value is not None:
            failures.append(f"{label}.{field} must be null for human execution")
    return failures


def _check_texts(checks: list[dict[str, Any]]) -> Counter[str]:
    return Counter(str(check["behavior"]) for check in checks)


def validate_run_semantics(
    run: dict[str, Any], suite: dict[str, Any], cases: dict[str, dict[str, Any]]
) -> list[str]:
    failures: list[str] = []
    if run["suite_id"] != suite["id"]:
        failures.append(
            f"Run suite_id {run['suite_id']} does not match selected suite {suite['id']}"
        )

    failures.extend(_executor_failures("generator", run["generator"]))
    failures.extend(_executor_failures("judge", run["judge"]))

    instruction_path = ROOT / run["system_under_test"]["instruction_path"]
    if not instruction_path.is_file():
        failures.append(
            "system_under_test.instruction_path does not resolve to a repository file: "
            f"{run['system_under_test']['instruction_path']}"
        )

    if run["run_status"] == "completed" and run["completed_at"] is None:
        failures.append("A completed run must record completed_at")
    if run["completed_at"] is not None:
        started_at = datetime.fromisoformat(run["started_at"].replace("Z", "+00:00"))
        completed_at = datetime.fromisoformat(run["completed_at"].replace("Z", "+00:00"))
        if completed_at < started_at:
            failures.append("completed_at precedes started_at")

    suite_case_ids = set(suite["case_ids"])
    repetitions = run["repetitions"]
    seen: set[tuple[str, int]] = set()

    for assessment in run["assessments"]:
        case_id = assessment["case_id"]
        repetition = assessment["repetition"]
        key = (case_id, repetition)
        if key in seen:
            failures.append(f"Duplicate assessment for {case_id} repetition {repetition}")
        seen.add(key)

        if case_id not in suite_case_ids:
            failures.append(f"Assessment case {case_id} is not in suite {suite['id']}")
            continue
        if case_id not in cases:
            failures.append(f"Assessment references missing case {case_id}")
            continue
        if repetition > repetitions:
            failures.append(
                f"Assessment {case_id} repetition {repetition} exceeds declared repetitions"
            )

        case = cases[case_id]
        actual_dimensions = set(assessment["dimension_scores"])
        applicable_dimensions = set(case["applicable_dimensions"])
        unexpected_dimensions = actual_dimensions - applicable_dimensions
        if unexpected_dimensions:
            failures.append(
                f"Assessment {case_id} scores non-applicable dimensions: "
                f"{', '.join(sorted(unexpected_dimensions))}"
            )
        if run["run_status"] == "completed":
            missing_dimensions = applicable_dimensions - actual_dimensions
            if missing_dimensions:
                failures.append(
                    f"Assessment {case_id} omits applicable dimensions: "
                    f"{', '.join(sorted(missing_dimensions))}"
                )
            null_dimensions = [
                dimension
                for dimension, score in assessment["dimension_scores"].items()
                if score is None
            ]
            if null_dimensions:
                failures.append(
                    f"Completed assessment {case_id} has N/A applicable dimensions: "
                    f"{', '.join(sorted(null_dimensions))}"
                )

        checks = (
            ("expected_behavior_checks", "expected_behaviors"),
            ("forbidden_behavior_checks", "forbidden_behaviors"),
            ("hard_failure_checks", "hard_failures"),
        )
        for check_field, case_field in checks:
            actual = _check_texts(assessment[check_field])
            expected = Counter(case[case_field])
            if actual != expected:
                failures.append(
                    f"Assessment {case_id} {check_field} must cover each declared "
                    f"{case_field} exactly once"
                )

        citation = assessment["citation_check"]
        expected_citations = bool(case.get("citations_expected", False))
        if citation["expected"] != expected_citations:
            failures.append(
                f"Assessment {case_id} citation expectation does not match the case"
            )
        if citation["supported_claims"] > citation["material_claims"]:
            failures.append(
                f"Assessment {case_id} has more supported than material claims"
            )

    if run["run_status"] == "completed":
        expected_keys = {
            (case_id, repetition)
            for case_id in suite["case_ids"]
            for repetition in range(1, repetitions + 1)
        }
        missing = expected_keys - seen
        if missing:
            preview = ", ".join(
                f"{case_id}#{repetition}" for case_id, repetition in sorted(missing)[:10]
            )
            suffix = " ..." if len(missing) > 10 else ""
            failures.append(f"Completed run is missing assessments: {preview}{suffix}")

    return failures


def summarize_run(
    run: dict[str, Any], suite: dict[str, Any], cases: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    policy = suite["gate_policy"]
    critical_dimensions = set(policy["critical_dimensions"])
    critical_scores: list[int] = []
    expected_observed = 0
    expected_total = 0
    forbidden_violations = 0
    hard_failures = 0
    material_claims = 0
    supported_claims = 0
    citation_assessments = 0
    decision_scores: dict[tuple[str, int, str], list[int]] = defaultdict(list)

    for assessment in run["assessments"]:
        case = cases[assessment["case_id"]]
        for dimension, score in assessment["dimension_scores"].items():
            if dimension in critical_dimensions and score is not None:
                critical_scores.append(score)
        expected_total += len(assessment["expected_behavior_checks"])
        expected_observed += sum(
            check["observed"] for check in assessment["expected_behavior_checks"]
        )
        forbidden_violations += sum(
            check["observed"] for check in assessment["forbidden_behavior_checks"]
        )
        hard_failures += sum(
            check["observed"] for check in assessment["hard_failure_checks"]
        )
        citation = assessment["citation_check"]
        if citation["expected"]:
            citation_assessments += 1
            material_claims += citation["material_claims"]
            supported_claims += citation["supported_claims"]
        decision_score = assessment["dimension_scores"].get("decision_quality")
        if decision_score is not None:
            decision_scores[
                (case["case_family_id"], assessment["repetition"], case["locale"])
            ].append(decision_score)

    multilingual_deltas: list[float] = []
    families = {key[0] for key in decision_scores}
    for family_id in families:
        for repetition in range(1, run["repetitions"] + 1):
            english = decision_scores.get((family_id, repetition, "en"), [])
            if not english:
                continue
            english_average = mean(english)
            localized_keys = [
                key
                for key in decision_scores
                if key[0] == family_id and key[1] == repetition and key[2] != "en"
            ]
            for key in localized_keys:
                multilingual_deltas.append(abs(english_average - mean(decision_scores[key])))

    expected_coverage = expected_observed / expected_total if expected_total else 1.0
    citation_coverage = (
        supported_claims / material_claims
        if material_claims
        else (1.0 if citation_assessments else None)
    )
    critical_average = mean(critical_scores) if critical_scores else None
    critical_minimum = min(critical_scores) if critical_scores else None
    maximum_multilingual_delta = max(multilingual_deltas) if multilingual_deltas else None
    multilingual_required = any(
        cases[case_id]["locale"] != "en" for case_id in suite["case_ids"]
    )

    gate_checks = [
        {
            "name": "hard_failures",
            "passed": hard_failures <= policy["maximum_hard_failures"],
            "actual": hard_failures,
            "threshold": policy["maximum_hard_failures"],
        },
        {
            "name": "expected_behavior_coverage",
            "passed": expected_coverage >= policy["minimum_expected_behavior_coverage"],
            "actual": expected_coverage,
            "threshold": policy["minimum_expected_behavior_coverage"],
        },
        {
            "name": "forbidden_behavior_violations",
            "passed": forbidden_violations
            <= policy["maximum_forbidden_behavior_violations"],
            "actual": forbidden_violations,
            "threshold": policy["maximum_forbidden_behavior_violations"],
        },
        {
            "name": "critical_average",
            "passed": critical_average is not None
            and critical_average >= policy["minimum_critical_average"],
            "actual": critical_average,
            "threshold": policy["minimum_critical_average"],
        },
        {
            "name": "critical_score_floor",
            "passed": critical_minimum is not None
            and critical_minimum >= policy["minimum_critical_score"],
            "actual": critical_minimum,
            "threshold": policy["minimum_critical_score"],
        },
        {
            "name": "citation_coverage",
            "passed": citation_coverage is None
            or citation_coverage >= policy["minimum_citation_coverage"],
            "actual": citation_coverage,
            "threshold": policy["minimum_citation_coverage"],
            "not_applicable": citation_coverage is None,
        },
        {
            "name": "multilingual_delta",
            "passed": not multilingual_required
            or (
                maximum_multilingual_delta is not None
                and maximum_multilingual_delta <= policy["maximum_multilingual_delta"]
            ),
            "actual": maximum_multilingual_delta,
            "threshold": policy["maximum_multilingual_delta"],
            "not_applicable": not multilingual_required,
        },
    ]
    gates_passed = all(check["passed"] for check in gate_checks)
    complete = run["run_status"] == "completed"
    calibrated = run["judge"]["calibration_status"] == "calibrated"
    content_approved = suite["status"] == "approved" and all(
        cases[case_id]["status"] == "approved" for case_id in suite["case_ids"]
    )

    return {
        "run_id": run["id"],
        "suite_id": suite["id"],
        "run_status": run["run_status"],
        "assessment_count": len(run["assessments"]),
        "expected_assessment_count": len(suite["case_ids"]) * run["repetitions"],
        "judge_calibration_status": run["judge"]["calibration_status"],
        "content_approved": content_approved,
        "metrics": {
            "hard_failures": hard_failures,
            "expected_behavior_coverage": expected_coverage,
            "forbidden_behavior_violations": forbidden_violations,
            "critical_average": critical_average,
            "critical_score_floor": critical_minimum,
            "citation_coverage": citation_coverage,
            "multilingual_comparisons": len(multilingual_deltas),
            "maximum_multilingual_delta": maximum_multilingual_delta,
        },
        "gate_checks": gate_checks,
        "gates_passed": gates_passed,
        "release_eligible": complete and calibrated and content_approved and gates_passed,
    }


def print_summary(summary: dict[str, Any]) -> None:
    print(
        f"Run {summary['run_id']}: {summary['assessment_count']}/"
        f"{summary['expected_assessment_count']} assessments; "
        f"status={summary['run_status']}; judge={summary['judge_calibration_status']}; "
        f"content_approved={summary['content_approved']}."
    )
    for check in summary["gate_checks"]:
        status = "N/A" if check.get("not_applicable") else ("PASS" if check["passed"] else "FAIL")
        print(
            f"- {status} {check['name']}: actual={check['actual']!r}, "
            f"threshold={check['threshold']!r}"
        )
    verdict = "PASS" if summary["gates_passed"] else "FAIL"
    eligibility = "eligible" if summary["release_eligible"] else "not release-eligible"
    print(f"Gate verdict: {verdict}; {eligibility}.")


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("run", type=Path, help="JSON or YAML eval-run file")
    command.add_argument("--suite", default="seed", help="Suite ID or repository-relative path")
    command.add_argument("--json", action="store_true", help="Print the summary as JSON")
    command.add_argument("--output", type=Path, help="Write the JSON summary to a file")
    command.add_argument(
        "--enforce-gates",
        action="store_true",
        help="Exit 2 when valid results do not pass every behavioral gate",
    )
    return command


def main() -> int:
    args = parser().parse_args()
    repository_failures = run_validation()
    if repository_failures:
        for failure in repository_failures:
            print(f"error: {failure}", file=sys.stderr)
        return 1

    try:
        run = load_run(args.run)
        shape_failures = validate_run_shape(run)
        if shape_failures:
            for failure in shape_failures:
                print(f"error: {failure}", file=sys.stderr)
            return 1
        suite = load_suite(args.suite)
        cases = load_cases()
        semantic_failures = validate_run_semantics(run, suite, cases)
    except (OSError, ValueError, KeyError, json.JSONDecodeError, yaml.YAMLError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if semantic_failures:
        for failure in semantic_failures:
            print(f"error: {failure}", file=sys.stderr)
        return 1

    summary = summarize_run(run, suite, cases)
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print_summary(summary)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"Wrote summary: {args.output}")
    return 2 if args.enforce_gates and not summary["gates_passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

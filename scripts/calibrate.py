#!/usr/bin/env python3
"""Prepare blind judge-calibration packets and report agreement between judges.

The script never decides whether a judge is calibrated. `prepare` and `compare` make no model
calls. `judge-controls` is opt-in and asks an archived run's automated judge to assess the
labeled negative controls with that run's frozen prompt and rubric.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from statistics import mean
from typing import Any, Callable

from jsonschema import Draft202012Validator, ValidationError

from scripts.evaluate_results import (
    load_review_context,
    load_run,
    validate_run_semantics,
    validate_run_shape,
)
from scripts.validate_repository import (
    ROOT,
    build_validators,
    format_errors,
    load_schemas,
    load_yaml,
)

CONTROL_ROOT = ROOT / "evals" / "calibration" / "controls"
CHECK_FIELDS = (
    ("expected_behavior_checks", "expected_behaviors"),
    ("forbidden_behavior_checks", "forbidden_behaviors"),
    ("hard_failure_checks", "hard_failures"),
)
REVIEW_CASE_FIELDS = (
    "id", "locale", "title", "input", "context", "applicable_dimensions", "expected_behaviors",
    "forbidden_behaviors", "hard_failures", "scoring_notes",
)
AUTOMATED = "automated"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def validator(name: str):
    schemas, registry = load_schemas()
    return build_validators(schemas, registry)[name]


def require_valid(name: str, value: object, label: str) -> None:
    errors = list(validator(name).iter_errors(value))
    if errors:
        raise ValueError(f"Invalid {label}: {format_errors(errors)}")


def load_controls(root: Path = CONTROL_ROOT) -> dict[str, tuple[dict[str, Any], str]]:
    controls = {}
    for path in sorted(root.glob("*.yaml")):
        data = load_yaml(path)
        require_valid("calibration-control", data, f"control {path.name}")
        controls[data["id"]] = (data, sha256(path.read_bytes()))
    return controls


def parse_sample(values: list[str]) -> list[tuple[str, int]]:
    sample = []
    for value in values:
        case_id, separator, repetition = value.partition("#")
        if not separator or not repetition.isdigit() or int(repetition) < 1:
            raise ValueError(f"Sample entries use CASE_ID#REPETITION: {value}")
        sample.append((case_id, int(repetition)))
    if len(set(sample)) != len(sample):
        raise ValueError("Sample entries must be unique")
    return sample


def review_case(case: dict[str, Any]) -> dict[str, Any]:
    return {
        **{field: case[field] for field in REVIEW_CASE_FIELDS},
        "citations_expected": bool(case.get("citations_expected", False)),
    }


def prepare(
    run_path: Path,
    review_packet: Path,
    output: Path,
    sample: list[tuple[str, int]] | None,
    control_ids: list[str] | None,
    seed: int,
    rubric_path: Path | None = None,
    control_root: Path = CONTROL_ROOT,
) -> dict[str, Any]:
    run_bytes = run_path.read_bytes()
    run = load_run(run_path)
    suite, cases, review_digest = load_review_context(review_packet)
    failures = validate_run_shape(run) or validate_run_semantics(run, suite, cases)
    if failures:
        raise ValueError("; ".join(failures))
    if run["run_status"] != "completed":
        raise ValueError("Calibration samples require a completed run")

    assessments = {(item["case_id"], item["repetition"]): item for item in run["assessments"]}
    selected = sample if sample is not None else sorted(assessments)
    missing = [
        f"{case_id}#{repetition}"
        for case_id, repetition in selected
        if (case_id, repetition) not in assessments
    ]
    if missing:
        raise ValueError(f"Sample entries are not assessments in the run: {', '.join(missing)}")

    available = load_controls(control_root)
    if control_ids is None:
        control_ids = [key for key, (data, _) in available.items() if data["case_id"] in cases]
    unknown = [key for key in control_ids if key not in available]
    if unknown:
        raise ValueError(f"Unknown negative controls: {', '.join(unknown)}")
    for key in control_ids:
        if available[key][0]["case_id"] not in cases:
            raise ValueError(f"Control {key} targets a case outside the reviewer packet")

    entries: list[tuple[dict[str, Any], dict[str, Any], str]] = []
    for case_id, repetition in selected:
        entries.append(
            (
                {"kind": "run", "case_id": case_id, "repetition": repetition},
                cases[case_id],
                assessments[(case_id, repetition)]["response"],
            )
        )
    for key in control_ids:
        control, digest = available[key]
        entries.append(
            (
                {
                    "kind": "control",
                    "case_id": control["case_id"],
                    "control_id": key,
                    "control_sha256": digest,
                },
                cases[control["case_id"]],
                control["response"],
            )
        )
    if not entries:
        raise ValueError("Calibration sample is empty")
    if len(entries) > 999:
        raise ValueError("Calibration samples are limited to 999 items")
    random.Random(seed).shuffle(entries)

    if rubric_path is None:
        archived = run_path.parent / "snapshot" / "rubric.md"
        rubric_path = archived if archived.is_file() else ROOT / "evals" / "rubric.md"
    rubric = rubric_path.read_text(encoding="utf-8")

    items, key_items = [], {}
    for position, (provenance, case, response) in enumerate(entries, 1):
        item_id = f"item-{position:03d}"
        items.append({"item_id": item_id, "case": review_case(case), "response": response})
        key_items[item_id] = provenance
    packet = {
        "schema_version": "0.1.0",
        "audience": "calibration_reviewer",
        "rubric": rubric,
        "rubric_sha256": sha256(rubric.encode("utf-8")),
        "items": items,
    }
    require_valid("calibration-packet", packet, "calibration packet")
    packet_bytes = json_bytes(packet)
    key = {
        "schema_version": "0.1.0",
        "packet_sha256": sha256(packet_bytes),
        "run_id": run["id"],
        "run_sha256": sha256(run_bytes),
        "review_packet_sha256": review_digest,
        "seed": seed,
        "items": key_items,
    }
    require_valid("calibration-key", key, "calibration key")
    template = {
        "schema_version": "0.1.0",
        "packet_sha256": key["packet_sha256"],
        "reviewer": {"identity": None, "type": "human"},
        "independent_of_automated_scores": None,
        "scored_at": None,
        "items": [
            {
                "item_id": item["item_id"],
                "dimension_scores": {
                    dimension: None for dimension in item["case"]["applicable_dimensions"]
                },
                **{
                    check_field: [
                        {"behavior": behavior, "observed": None, "evidence": ""}
                        for behavior in item["case"][case_field]
                    ]
                    for check_field, case_field in CHECK_FIELDS
                },
                "notes": "",
            }
            for item in items
        ],
    }

    output.mkdir(parents=True, exist_ok=False)
    (output / "packet.json").write_bytes(packet_bytes)
    (output / "key.json").write_bytes(json_bytes(key))
    (output / "score-template.json").write_bytes(json_bytes(template))
    return key


def load_key(path: Path, packet_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    key = json.loads(path.read_bytes())
    require_valid("calibration-key", key, "calibration key")
    packet_bytes = packet_path.read_bytes()
    if sha256(packet_bytes) != key["packet_sha256"]:
        raise ValueError("Calibration packet does not match the key")
    packet = json.loads(packet_bytes)
    require_valid("calibration-packet", packet, "calibration packet")
    if {item["item_id"] for item in packet["items"]} != set(key["items"]):
        raise ValueError("Calibration key and packet list different items")
    return key, {item["item_id"]: item for item in packet["items"]}


def validate_scores(
    sheet: dict[str, Any], key: dict[str, Any], items: dict[str, dict[str, Any]], label: str
) -> list[str]:
    errors = list(validator("calibration-scores").iter_errors(sheet))
    if errors:
        return [f"{label}: {format_errors(errors)}"]
    failures = []
    if sheet["packet_sha256"] != key["packet_sha256"]:
        failures.append(f"{label}: scored a different calibration packet")
    scored = [item["item_id"] for item in sheet["items"]]
    if len(set(scored)) != len(scored):
        failures.append(f"{label}: scores an item more than once")
    if set(scored) != set(items):
        failures.append(f"{label}: must score exactly the items in the packet")
    for item in sheet["items"]:
        case = items.get(item["item_id"], {}).get("case")
        if case is None:
            continue
        if set(item["dimension_scores"]) != set(case["applicable_dimensions"]):
            failures.append(f"{label}: {item['item_id']} must score each applicable dimension")
        for check_field, case_field in CHECK_FIELDS:
            behaviors = sorted(check["behavior"] for check in item[check_field])
            if behaviors != sorted(case[case_field]):
                failures.append(
                    f"{label}: {item['item_id']} {check_field} must cover each declared "
                    f"{case_field} exactly once"
                )
    return failures


def automated_scores(
    run: dict[str, Any], key: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    assessments = {(item["case_id"], item["repetition"]): item for item in run["assessments"]}
    scores = {}
    for item_id, provenance in key["items"].items():
        if provenance["kind"] != "run":
            continue
        assessment = assessments.get((provenance["case_id"], provenance["repetition"]))
        if assessment is None:
            raise ValueError(f"Run has no assessment for {item_id}")
        scores[item_id] = assessment
    return scores


def observed(checks: list[dict[str, Any]]) -> dict[str, bool]:
    return {check["behavior"]: check["observed"] for check in checks}


def compare_pair(
    left: dict[str, dict[str, Any]], right: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    shared = sorted(set(left) & set(right))
    hard_agreements, hard_disagreements = 0, []
    check_totals: dict[str, list[int]] = {field: [0, 0] for field, _ in CHECK_FIELDS}
    differences: list[int] = []
    per_dimension: dict[str, list[int]] = defaultdict(list)
    score_disagreements = []
    for item_id in shared:
        a, b = left[item_id], right[item_id]
        a_hard = any(check["observed"] for check in a["hard_failure_checks"])
        b_hard = any(check["observed"] for check in b["hard_failure_checks"])
        if a_hard == b_hard:
            hard_agreements += 1
        else:
            hard_disagreements.append(item_id)
        for field, _ in CHECK_FIELDS:
            a_checks, b_checks = observed(a[field]), observed(b[field])
            for behavior, value in a_checks.items():
                check_totals[field][1] += 1
                check_totals[field][0] += value == b_checks.get(behavior)
        for dimension, a_score in a["dimension_scores"].items():
            b_score = b["dimension_scores"].get(dimension)
            if a_score is None or b_score is None:
                continue
            difference = a_score - b_score
            differences.append(difference)
            per_dimension[dimension].append(difference)
            if abs(difference) >= 2:
                score_disagreements.append(
                    {"item_id": item_id, "dimension": dimension, "left": a_score, "right": b_score}
                )

    def rates(values: list[int]) -> dict[str, Any]:
        if not values:
            return {"pairs": 0, "exact": None, "within_one": None, "mean_absolute": None,
                    "mean_signed": None}
        return {
            "pairs": len(values),
            "exact": sum(value == 0 for value in values) / len(values),
            "within_one": sum(abs(value) <= 1 for value in values) / len(values),
            "mean_absolute": mean(abs(value) for value in values),
            "mean_signed": mean(values),
        }

    return {
        "shared_items": len(shared),
        "hard_failure_classification": {
            "agreement": hard_agreements / len(shared) if shared else None,
            "disagreements": hard_disagreements,
        },
        "behavior_check_agreement": {
            field: (agree / total if total else None)
            for field, (agree, total) in check_totals.items()
        },
        "dimension_scores": rates(differences),
        "dimension_scores_by_dimension": {
            dimension: rates(values) for dimension, values in sorted(per_dimension.items())
        },
        "score_differences_of_two_or_more": score_disagreements,
    }


def missed_failures(control: dict[str, Any], scores: dict[str, Any]) -> list[str]:
    intended = control["intended_failures"]
    hard = observed(scores["hard_failure_checks"])
    forbidden = observed(scores["forbidden_behavior_checks"])
    return [b for b in intended["hard_failures"] if not hard.get(b)] + [
        b for b in intended["forbidden_behaviors"] if not forbidden.get(b)
    ]


def control_detection(
    judges: dict[str, dict[str, dict[str, Any]]],
    key: dict[str, Any],
    control_root: Path = CONTROL_ROOT,
) -> list[dict[str, Any]]:
    controls = load_controls(control_root)
    results = []
    for item_id, provenance in sorted(key["items"].items()):
        if provenance["kind"] != "control":
            continue
        control, digest = controls.get(provenance["control_id"], (None, None))
        if control is None or digest != provenance["control_sha256"]:
            raise ValueError(f"Control {provenance['control_id']} changed since preparation")
        detection = {}
        for name, scores in judges.items():
            if item_id not in scores:
                continue
            missed = missed_failures(control, scores[item_id])
            detection[name] = {"detected_all": not missed, "missed": missed}
        results.append(
            {"item_id": item_id, "control_id": provenance["control_id"], "judges": detection}
        )
    return results


def compare(
    key_path: Path,
    packet_path: Path,
    run_path: Path,
    score_paths: list[Path],
    control_root: Path = CONTROL_ROOT,
) -> dict[str, Any]:
    key, items = load_key(key_path, packet_path)
    run_bytes = run_path.read_bytes()
    if sha256(run_bytes) != key["run_sha256"]:
        raise ValueError("Run file differs from the run used to prepare the packet")
    judges = {AUTOMATED: automated_scores(json.loads(run_bytes), key)}
    attestations = {}
    failures = []
    for path in score_paths:
        sheet = load_yaml(path)
        failures.extend(validate_scores(sheet, key, items, path.name))
        if failures:
            continue
        identity = sheet["reviewer"]["identity"]
        if identity in judges:
            failures.append(f"{path.name}: duplicate reviewer identity {identity}")
            continue
        judges[identity] = {item["item_id"]: item for item in sheet["items"]}
        attestations[identity] = sheet["independent_of_automated_scores"]
    if failures:
        raise ValueError("; ".join(failures))

    kinds = defaultdict(int)
    for provenance in key["items"].values():
        kinds[provenance["kind"]] += 1
    return {
        "packet_sha256": key["packet_sha256"],
        "run_id": key["run_id"],
        "items": dict(kinds),
        "judges": sorted(judges),
        "independent_of_automated_scores": attestations,
        "pairs": [
            {"left": left, "right": right, **compare_pair(judges[left], judges[right])}
            for left, right in combinations(sorted(judges), 2)
        ],
        "negative_controls": control_detection(judges, key, control_root),
        "interpretation": (
            "Agreement statistics only. They do not mark any judge calibrated; maintainers must "
            "review disagreements, resolve rubric ambiguities, and record the decision."
        ),
    }


def judge_controls(
    archive: Path,
    output: Path,
    control_ids: list[str] | None = None,
    control_root: Path = CONTROL_ROOT,
    invoke_judge: Callable[..., str] | None = None,
    cli_version: str | None = None,
) -> dict[str, Any]:
    from scripts.execute_evals import invoke, judge_schema, load_config

    snapshot = archive / "snapshot"
    run = load_run(archive / "run.json")
    if run["run_status"] != "completed" or "source_snapshot" not in run:
        raise ValueError("Control judging requires a completed, archived run with a snapshot")
    for relative, expected in run["source_snapshot"]["files"].items():
        if not relative.startswith("snapshot/"):
            continue
        if sha256((archive / relative).read_bytes()) != expected:
            raise ValueError(f"Archived snapshot integrity failure: {relative}")
    _, cases, review_digest = load_review_context(snapshot / "reviewer.json")
    config = load_config(snapshot / "configuration.yaml")
    template = (snapshot / "judge-prompt.md").read_text(encoding="utf-8")
    rubric = (snapshot / "rubric.md").read_text(encoding="utf-8")
    judge = run["judge"]

    available = load_controls(control_root)
    if control_ids is None:
        control_ids = [key for key, (data, _) in available.items() if data["case_id"] in cases]
    unknown = [key for key in control_ids if key not in available]
    if unknown:
        raise ValueError(f"Unknown negative controls: {', '.join(unknown)}")
    if not control_ids:
        raise ValueError("No negative controls target cases in this run")

    invoke_judge = invoke_judge or invoke
    if cli_version is None:
        cli_version = subprocess.check_output(["codex", "--version"], text=True).strip()
    output.mkdir(parents=True, exist_ok=True)
    results = []
    for position, control_id in enumerate(control_ids, 1):
        control, digest = available[control_id]
        case = cases.get(control["case_id"])
        if case is None:
            raise ValueError(f"Control {control_id} targets a case outside the archived run")
        meta = {"control_sha256": digest, "judge": judge, "review_packet_sha256": review_digest}
        prefix = output / control_id
        meta_path = prefix.with_suffix(".meta.json")
        judgment_path = prefix.with_suffix(".judgment.json")
        schema = judge_schema(case)
        if judgment_path.exists():
            if not meta_path.exists() or json.loads(meta_path.read_bytes()) != meta:
                raise ValueError(f"Existing judgment for {control_id} used different inputs")
            judgment = json.loads(judgment_path.read_bytes())
        else:
            meta_path.write_bytes(json_bytes(meta))
            prompt = template.format(
                rubric=rubric,
                case=json.dumps(case, ensure_ascii=False),
                response=control["response"],
            )
            judgment = json.loads(
                invoke_judge(prompt, judge, prefix, config["timeout_seconds"], schema)
            )
            Draft202012Validator(schema).validate(judgment)
            judgment_path.write_bytes(json_bytes(judgment))
        missed = missed_failures(control, judgment)
        results.append(
            {
                "control_id": control_id,
                "case_id": control["case_id"],
                "control_sha256": digest,
                "detected_all": not missed,
                "missed": missed,
                "hard_failures_observed": [
                    check["behavior"] for check in judgment["hard_failure_checks"]
                    if check["observed"]
                ],
                "forbidden_behaviors_observed": [
                    check["behavior"] for check in judgment["forbidden_behavior_checks"]
                    if check["observed"]
                ],
                "dimension_scores": judgment["dimension_scores"],
            }
        )
        print(f"Judged control {position}/{len(control_ids)}: {control_id}", flush=True)

    report = {
        "schema_version": "0.1.0",
        "run_id": run["id"],
        "review_packet_sha256": review_digest,
        "judge": judge,
        "judge_cli_version": cli_version,
        "run_cli_version": run["source_snapshot"]["cli_version"],
        "judged_at": datetime.now(timezone.utc).isoformat(),
        "controls": results,
        "interpretation": (
            "Detection of deliberately unambiguous synthetic failures is necessary but not "
            "sufficient for calibration; it does not mark the judge calibrated."
        ),
    }
    require_valid("calibration-control-judging", report, "control judging report")
    (output / "report.json").write_bytes(json_bytes(report))
    return report


def percent(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.0%}"


def print_report(report: dict[str, Any]) -> None:
    print(
        f"Calibration comparison for {report['run_id']}: "
        f"{report.get('items', {}).get('run', 0)} run items, "
        f"{report.get('items', {}).get('control', 0)} negative controls; "
        f"judges: {', '.join(report['judges'])}."
    )
    for identity, independent in report["independent_of_automated_scores"].items():
        if not independent:
            print(f"warning: {identity} did not attest independence from automated scores")
    for pair in report["pairs"]:
        dimensions = pair["dimension_scores"]
        print(
            f"- {pair['left']} vs {pair['right']} ({pair['shared_items']} shared items): "
            f"hard-failure agreement {percent(pair['hard_failure_classification']['agreement'])}; "
            f"exact scores {percent(dimensions['exact'])}, within one "
            f"{percent(dimensions['within_one'])} over {dimensions['pairs']} pairs"
        )
        if pair["hard_failure_classification"]["disagreements"]:
            print(
                "  hard-failure disagreements: "
                + ", ".join(pair["hard_failure_classification"]["disagreements"])
            )
    for control in report["negative_controls"]:
        for judge, result in control["judges"].items():
            status = (
                "detected" if result["detected_all"] else "missed " + "; ".join(result["missed"])
            )
            print(f"- control {control['item_id']} ({judge}): {status}")
    print(report["interpretation"])


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    actions = command.add_subparsers(dest="action", required=True)

    prepare_command = actions.add_parser("prepare", help="Freeze a blind calibration packet")
    prepare_command.add_argument("--run", type=Path, required=True, help="Completed eval-run file")
    prepare_command.add_argument(
        "--review-packet", type=Path, required=True, help="Frozen reviewer packet for the run"
    )
    prepare_command.add_argument("--output", type=Path, required=True, help="New directory")
    selection = prepare_command.add_mutually_exclusive_group(required=True)
    selection.add_argument(
        "--sample", action="append", metavar="CASE_ID#REPETITION", help="Run assessment to include"
    )
    selection.add_argument(
        "--all-assessments", action="store_true", help="Include every assessment in the run"
    )
    controls = prepare_command.add_mutually_exclusive_group()
    controls.add_argument(
        "--control", action="append", metavar="CONTROL_ID", help="Negative control to include"
    )
    controls.add_argument(
        "--no-controls", action="store_true", help="Exclude negative controls (not recommended)"
    )
    prepare_command.add_argument("--seed", type=int, default=0, help="Shuffle seed")
    prepare_command.add_argument("--rubric", type=Path, help="Rubric file (default: run snapshot)")

    compare_command = actions.add_parser("compare", help="Report agreement between judges")
    compare_command.add_argument("--key", type=Path, required=True)
    compare_command.add_argument("--packet", type=Path, required=True)
    compare_command.add_argument("--run", type=Path, required=True)
    compare_command.add_argument(
        "--scores", type=Path, action="append", required=True, help="Completed score sheet"
    )
    compare_command.add_argument("--json", action="store_true", help="Print the report as JSON")
    compare_command.add_argument("--output", type=Path, help="Write the JSON report to a file")

    judge_command = actions.add_parser(
        "judge-controls", help="Opt-in: ask an archived run's model judge to assess the controls"
    )
    judge_command.add_argument(
        "--archive", type=Path, required=True, help="Archived run directory with snapshot/"
    )
    judge_command.add_argument(
        "--output", type=Path, required=True, help="Directory for judgments; reused on resume"
    )
    judge_command.add_argument(
        "--control", action="append", metavar="CONTROL_ID", help="Control to judge (default: all)"
    )
    return command


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.action == "prepare":
            key = prepare(
                args.run,
                args.review_packet,
                args.output,
                None if args.all_assessments else parse_sample(args.sample),
                [] if args.no_controls else args.control,
                args.seed,
                args.rubric,
            )
            controls = sum(item["kind"] == "control" for item in key["items"].values())
            print(
                f"Prepared {len(key['items'])} blind items ({controls} negative controls) in "
                f"{args.output}. Send only packet.json and score-template.json to reviewers."
            )
            if not controls:
                print("warning: the sample has no negative controls", file=sys.stderr)
            return 0
        if args.action == "judge-controls":
            judged = judge_controls(args.archive, args.output, args.control)
            for result in judged["controls"]:
                status = (
                    "detected" if result["detected_all"]
                    else "missed " + "; ".join(result["missed"])
                )
                print(f"- {result['control_id']}: {status}")
            print(judged["interpretation"])
            return 0
        report = compare(args.key, args.packet, args.run, args.scores)
    except (
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
        ValidationError,
        subprocess.SubprocessError,
    ) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_report(report)
    if args.output:
        args.output.write_bytes(json_bytes(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

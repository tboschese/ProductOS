#!/usr/bin/env python3
"""Inspect or export ProductOS evaluation suites without pretending to score judgment."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from scripts.validate_repository import (
    ROOT,
    build_validators,
    format_errors,
    load_schemas,
    load_yaml,
    run_validation,
)

CASE_ROOTS = (ROOT / "evals" / "cases", ROOT / "evals" / "multilingual")
SUITE_ROOT = ROOT / "evals" / "regression"


def load_cases() -> dict[str, dict[str, object]]:
    cases: dict[str, dict[str, object]] = {}
    for case_root in CASE_ROOTS:
        for path in sorted(case_root.glob("*.yaml")):
            case = load_yaml(path)
            if not isinstance(case, dict) or not isinstance(case.get("id"), str):
                raise ValueError(f"Invalid eval case shape: {path.relative_to(ROOT)}")
            cases[case["id"]] = case
    return cases


def load_suite(suite_name: str) -> dict[str, object]:
    path = Path(suite_name)
    if not path.suffix:
        path = SUITE_ROOT / f"{suite_name}.yaml"
    elif not path.is_absolute():
        path = ROOT / path

    suite = load_yaml(path)
    if not isinstance(suite, dict):
        raise ValueError(f"Invalid eval suite shape: {path}")
    return suite


def suite_cases(
    suite: dict[str, object], cases: dict[str, dict[str, object]]
) -> list[dict[str, object]]:
    selected = []
    for case_id in suite["case_ids"]:
        if case_id not in cases:
            raise ValueError(f"Suite references missing case: {case_id}")
        selected.append(cases[case_id])
    return selected


def export_packet(
    suite: dict[str, object], selected_cases: list[dict[str, object]], output: Path,
    *, audience: str = "generator",
) -> Path:
    if audience not in {"generator", "reviewer"}:
        raise ValueError(f"Unknown packet audience: {audience}")
    packet = {
        "suite_id": suite["id"],
        "schema_version": "0.3.0",
        "audience": audience,
        "scoring_status": "unscored",
        "cases": [
            {field: case[field] for field in ("id", "locale", "input", "context")}
            for case in selected_cases
        ] if audience == "generator" else selected_cases,
    }
    if audience == "reviewer":
        packet["suite"] = suite

    failures = validate_packet_shape(packet)
    if failures:
        raise ValueError(f"Invalid {audience} packet: {'; '.join(failures)}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


def validate_packet_shape(packet: dict[str, object]) -> list[str]:
    schemas, registry = load_schemas()
    validator = build_validators(schemas, registry)["eval-packet"]
    errors = list(validator.iter_errors(packet))
    return [format_errors(errors)] if errors else []


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--suite", default="seed", help="Suite ID or repository-relative path")
    command.add_argument("--list", action="store_true", help="List selected cases")
    command.add_argument("--export", type=Path, help="Export a blind generator JSON packet")
    command.add_argument(
        "--export-review", type=Path, help="Export full cases and gate policy for reviewers only"
    )
    return command


def main() -> int:
    command = parser()
    args = command.parse_args()
    if args.export and args.export_review and args.export.resolve() == args.export_review.resolve():
        command.error("Generator and reviewer packets must use different output paths")
    failures = run_validation()
    if failures:
        for failure in failures:
            print(f"error: {failure}")
        return 1

    try:
        cases = load_cases()
        suite = load_suite(args.suite)
        selected = suite_cases(suite, cases)

        if args.export:
            output = export_packet(suite, selected, args.export)
            print(f"Exported blind generator packet: {output}")
        if args.export_review:
            output = export_packet(suite, selected, args.export_review, audience="reviewer")
            print(f"Exported reviewer packet: {output}")
    except (OSError, ValueError, KeyError, yaml.YAMLError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.list:
        for case in selected:
            print(f"{case['id']}\t{case['locale']}\t{case['title']}")

    locales: dict[str, int] = {}
    for case in selected:
        locale = str(case["locale"])
        locales[locale] = locales.get(locale, 0) + 1
    locale_summary = ", ".join(f"{key}={value}" for key, value in sorted(locales.items()))
    print(f"Suite {suite['id']}: {len(selected)} cases ({locale_summary}); scoring not run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

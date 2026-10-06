#!/usr/bin/env python3
"""Execute an explicitly configured, uncalibrated Codex behavioral pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, ValidationError

from scripts.evaluate_results import (
    load_review_context,
    load_run,
    summarize_run,
    validate_run_semantics,
    validate_run_shape,
)
from scripts.run_evals import export_packet, load_cases, load_suite, suite_cases
from scripts.validate_repository import (
    ROOT,
    build_validators,
    load_schemas,
    load_yaml,
    run_validation,
)

PROMPT_ROOT = ROOT / "evals" / "prompts"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_config(path: Path) -> dict[str, Any]:
    config = load_yaml(path)
    schemas, registry = load_schemas()
    validator = build_validators(schemas, registry)["eval-config"]
    errors = list(validator.iter_errors(config))
    if errors:
        raise ValueError(f"Invalid evaluation configuration: {errors[0].message}")
    if config["system_under_test"]["instruction_path"] not in config["instruction_paths"]:
        raise ValueError("Instruction bundle must include the system_under_test instruction_path")
    return config


def instruction_bundle(paths: list[str]) -> str:
    parts = []
    allowed = (ROOT / ".agents" / "skills" / "staff-product-manager", ROOT / "docs" / "foundations")
    for relative in paths:
        path = (ROOT / relative).resolve()
        if not any(path.is_relative_to(directory.resolve()) for directory in allowed):
            raise ValueError(
                f"Instruction path is outside the allowed instruction directories: {relative}"
            )
        if path.suffix != ".md":
            raise ValueError(f"Instruction path must be Markdown: {relative}")
        parts.append(f"Reference: {relative}\n\n{path.read_text(encoding='utf-8')}")
    return "\n\n".join(parts)


def prepare_run(config_path: Path, output: Path) -> dict[str, Any]:
    config = load_config(config_path)
    instructions = instruction_bundle(config["instruction_paths"])
    cli_version = subprocess.check_output(["codex", "--version"], text=True).strip()
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True))
    output.mkdir(parents=True, exist_ok=False)
    snapshot = output / "snapshot"
    snapshot.mkdir()
    (snapshot / "configuration.yaml").write_bytes(config_path.read_bytes())
    (snapshot / "instructions.txt").write_text(instructions, encoding="utf-8")
    copies = {
        "rubric.md": ROOT / "evals" / "rubric.md",
        "generator-prompt.md": PROMPT_ROOT / "generator-pilot-v1.md",
        "judge-prompt.md": PROMPT_ROOT / "judge-pilot-v1.md",
        "execute_evals.py": Path(__file__),
    }
    for name, path in copies.items():
        (snapshot / name).write_bytes(path.read_bytes())
    suite = load_suite(config["suite"])
    selected = suite_cases(suite, load_cases())
    export_packet(suite, selected, snapshot / "generator.json")
    export_packet(suite, selected, snapshot / "reviewer.json", audience="reviewer")
    run = {
        "id": f"{config['id']}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "schema_version": "0.3.1",
        "suite_id": suite["id"],
        "run_status": "partial",
        "started_at": utc_now(),
        "completed_at": None,
        "repository_revision": revision,
        "source_snapshot": {
            "revision_role": "base_commit",
            "worktree_dirty": dirty,
            "cli_version": cli_version,
            "files": {
                path.relative_to(output).as_posix(): digest(path) for path in snapshot.iterdir()
            },
        },
        "system_under_test": config["system_under_test"],
        "generator": config["generator"],
        "judge": config["judge"],
        "repetitions": config["repetitions"],
        "assessments": [],
    }
    failures = validate_run_shape(run)
    if failures:
        raise ValueError("; ".join(failures))
    write_json(output / "run.json", run)
    return run


def verify_snapshot(output: Path, run: dict[str, Any], config_path: Path) -> None:
    failures = validate_run_shape(run)
    if failures:
        raise ValueError("; ".join(failures))
    for relative, expected in run["source_snapshot"]["files"].items():
        path = (output / relative).resolve()
        if not path.is_relative_to(output.resolve()) or digest(path) != expected:
            raise ValueError(f"Snapshot integrity failure: {relative}")
    if digest(config_path) != digest(output / "snapshot" / "configuration.yaml"):
        raise ValueError("Resume configuration differs from the frozen configuration")
    if digest(Path(__file__)) != digest(output / "snapshot" / "execute_evals.py"):
        raise ValueError("Runner changed since preparation; create a new pilot directory")
    config = load_config(output / "snapshot" / "configuration.yaml")
    for field in ("generator", "judge", "system_under_test", "repetitions"):
        if run[field] != config[field]:
            raise ValueError(f"Run metadata differs from the frozen configuration: {field}")


def generator_prompt(template: str, instructions: str, case: dict[str, Any]) -> str:
    return template.format(
        instructions=instructions,
        input=case["input"],
        context=json.dumps(case["context"], ensure_ascii=False),
    )


def judge_schema(case: dict[str, Any]) -> dict[str, Any]:
    def closed(properties: dict[str, Any]) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": properties,
            "required": list(properties),
            "additionalProperties": False,
        }

    scores = {
        dimension: {"type": "integer", "enum": [0, 1, 2, 3, 4]}
        for dimension in case["applicable_dimensions"]
    }
    evidence = {dimension: {"type": "string", "minLength": 1} for dimension in scores}
    properties = {"dimension_scores": closed(scores), "dimension_evidence": closed(evidence)}
    for output_field, case_field in (
        ("expected_behavior_checks", "expected_behaviors"),
        ("forbidden_behavior_checks", "forbidden_behaviors"),
        ("hard_failure_checks", "hard_failures"),
    ):
        behaviors = case[case_field]
        check = closed(
            {
                "behavior": {"type": "string", "enum": behaviors}
                if behaviors
                else {"type": "string"},
                "observed": {"type": "boolean"},
                "evidence": {"type": "string", "minLength": 1},
            }
        )
        properties[output_field] = {
            "type": "array",
            "items": check,
            "minItems": len(behaviors),
            "maxItems": len(behaviors),
        }
    properties["citation_check"] = closed(
        {
            "expected": {"type": "boolean", "enum": [bool(case.get("citations_expected", False))]},
            "material_claims": {"type": "integer", "minimum": 0},
            "supported_claims": {"type": "integer", "minimum": 0},
            "notes": {"type": "string"},
        }
    )
    properties["notes"] = {"type": "string"}
    return closed(properties)


def invoke(
    prompt: str,
    executor: dict[str, Any],
    prefix: Path,
    timeout: int,
    schema: dict[str, Any] | None = None,
) -> str:
    prefix.parent.mkdir(parents=True, exist_ok=True)
    prefix.with_suffix(".prompt.txt").write_text(prompt, encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="productos-eval-") as workspace:
        final = Path(workspace) / "final.txt"
        command = [
            "codex",
            "exec",
            "--ignore-user-config",
            "--ephemeral",
            "--skip-git-repo-check",
            "--sandbox",
            "read-only",
            "--json",
            "-C",
            workspace,
            "-o",
            str(final),
            "-c",
            f"model={json.dumps(executor['model'])}",
            "-c",
            f"model_reasoning_effort={json.dumps(executor['settings']['reasoning_effort'])}",
            "-c",
            f"service_tier={json.dumps(executor['settings']['service_tier'])}",
        ]
        if schema is not None:
            schema_path = prefix.with_suffix(".schema.json").resolve()
            write_json(schema_path, schema)
            command.extend(["--output-schema", str(schema_path)])
        command.append("-")
        try:
            result = subprocess.run(
                command,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as error:
            for suffix, value in ((".events.jsonl", error.stdout), (".stderr.txt", error.stderr)):
                text = (
                    value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value
                )
                prefix.with_suffix(suffix).write_text(text or "", encoding="utf-8")
            prefix.with_suffix(".error.txt").write_text("Execution timed out", encoding="utf-8")
            raise ValueError(f"Execution timed out after {timeout}s: {prefix.name}") from error
        prefix.with_suffix(".events.jsonl").write_text(result.stdout, encoding="utf-8")
        prefix.with_suffix(".stderr.txt").write_text(result.stderr, encoding="utf-8")
        if result.returncode:
            raise ValueError(
                f"Codex failed with exit {result.returncode}: {prefix.name}; see its stderr"
            )
        events = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        if not any(event["type"] == "turn.completed" for event in events):
            raise ValueError(f"Codex did not complete the turn: {prefix.name}")
        for event in events:
            item = event.get("item", {})
            if item and item.get("type") not in {"agent_message", "reasoning"}:
                raise ValueError(f"Tools are outside this pilot protocol: {item.get('type')}")
        response = final.read_text(encoding="utf-8")
        if not response.strip():
            raise ValueError(f"Empty Codex response: {prefix.name}")
        return response


def execute(output: Path, run: dict[str, Any]) -> dict[str, Any]:
    snapshot = output / "snapshot"
    config = load_config(snapshot / "configuration.yaml")
    suite, cases, _ = load_review_context(snapshot / "reviewer.json")
    failures = validate_run_semantics(run, suite, cases)
    if failures:
        raise ValueError("; ".join(failures))
    if run["run_status"] == "completed":
        return run
    for stage in ("generation", "judging"):
        (output / stage).mkdir(exist_ok=True)
    instructions = (snapshot / "instructions.txt").read_text(encoding="utf-8")
    template = (snapshot / "generator-prompt.md").read_text(encoding="utf-8")
    blind = json.loads((snapshot / "generator.json").read_text(encoding="utf-8"))["cases"]
    jobs = [(case, repetition) for case in blind for repetition in range(1, run["repetitions"] + 1)]
    for position, (case, repetition) in enumerate(jobs, 1):
        prefix = output / "generation" / f"{case['id']}-{repetition}"
        response_path = prefix.with_suffix(".response.txt")
        if not response_path.exists():
            response = invoke(
                generator_prompt(template, instructions, case),
                run["generator"],
                prefix,
                config["timeout_seconds"],
            )
            response_path.write_text(response, encoding="utf-8")
            run["source_snapshot"]["files"][response_path.relative_to(output).as_posix()] = digest(
                response_path
            )
            write_json(output / "run.json", run)
        elif response_path.relative_to(output).as_posix() not in run["source_snapshot"]["files"]:
            raise ValueError(f"Response checkpoint is not tracked: {response_path.name}")
        print(f"Generated {position}/{len(jobs)}: {case['id']}#{repetition}", flush=True)

    judged = {(item["case_id"], item["repetition"]) for item in run["assessments"]}
    template = (snapshot / "judge-prompt.md").read_text(encoding="utf-8")
    rubric = (snapshot / "rubric.md").read_text(encoding="utf-8")
    for position, (blind_case, repetition) in enumerate(jobs, 1):
        case_id = blind_case["id"]
        if (case_id, repetition) in judged:
            continue
        case = cases[case_id]
        response = (output / "generation" / f"{case_id}-{repetition}.response.txt").read_text(
            encoding="utf-8"
        )
        schema = judge_schema(case)
        prompt = template.format(
            rubric=rubric, case=json.dumps(case, ensure_ascii=False), response=response
        )
        prefix = output / "judging" / f"{case_id}-{repetition}"
        judgment = json.loads(
            invoke(prompt, run["judge"], prefix, config["timeout_seconds"], schema)
        )
        Draft202012Validator(schema).validate(judgment)
        write_json(prefix.with_suffix(".judgment.json"), judgment)
        evidence = judgment.pop("dimension_evidence")
        judgment["notes"] += "\nDimension evidence:\n" + "\n".join(
            f"{dimension}: {text}" for dimension, text in evidence.items()
        )
        candidate = deepcopy(run)
        candidate["assessments"].append(
            {"case_id": case_id, "repetition": repetition, "response": response, **judgment}
        )
        failures = validate_run_shape(candidate) + validate_run_semantics(candidate, suite, cases)
        if failures:
            raise ValueError("; ".join(failures))
        run = candidate
        write_json(output / "run.json", run)
        print(f"Judged {position}/{len(jobs)}: {case_id}#{repetition}", flush=True)
    run["run_status"] = "completed"
    run["completed_at"] = utc_now()
    failures = validate_run_shape(run) + validate_run_semantics(run, suite, cases)
    if failures:
        raise ValueError("; ".join(failures))
    write_json(output / "run.json", run)
    return run


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", type=Path, default=ROOT / "evals" / "configs" / "seed-pilot.yaml"
    )
    parser.add_argument("--output", type=Path, required=True, help="New pilot artifact directory")
    parser.add_argument(
        "--resume", action="store_true", help="Resume using intact frozen artifacts"
    )
    parser.add_argument(
        "--prepare-only", action="store_true", help="Freeze inputs without model calls"
    )
    args = parser.parse_args()
    failures = run_validation()
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    try:
        run = (
            load_run(args.output / "run.json")
            if args.resume
            else prepare_run(args.config, args.output)
        )
        verify_snapshot(args.output, run, args.config)
        if args.prepare_only:
            print(f"Prepared pilot: {args.output}; no model calls made")
            return 0
        run = execute(args.output, run)
        suite, cases, packet_digest = load_review_context(
            args.output / "snapshot" / "reviewer.json"
        )
        summary = summarize_run(run, suite, cases)
        summary["evaluation_context"] = {"source": "reviewer_packet", "sha256": packet_digest}
        write_json(args.output / "summary.json", summary)
        print(f"Pilot complete: gates_passed={summary['gates_passed']}; release_eligible=False")
        return 0
    except (OSError, ValueError, ValidationError, subprocess.SubprocessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

import json
import subprocess
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import execute_evals
from scripts.evaluate_results import summarize_run, validate_run_shape
from scripts.execute_evals import (
    execute,
    generator_prompt,
    instruction_bundle,
    invoke,
    load_config,
    prepare_run,
    verify_snapshot,
)
from scripts.run_evals import load_cases, load_suite
from scripts.validate_repository import VALID_FIXTURES, load_yaml


def prepared_pilot(tmp_path, monkeypatch):
    config = load_yaml(VALID_FIXTURES / "eval-config.yaml")
    suite = load_suite("seed")
    suite["case_ids"] = ["retention-decline-en"]
    suite_path = tmp_path / "suite.yaml"
    suite_path.write_text(json.dumps(suite), encoding="utf-8")
    config["suite"] = str(suite_path)
    config_path = tmp_path / "config.yaml"
    config_path.write_text(json.dumps(config), encoding="utf-8")

    def fake_check_output(command, **kwargs):
        if command[0] == "codex":
            return "codex-cli synthetic"
        if "rev-parse" in command:
            return "a" * 40
        return " M synthetic-file"

    monkeypatch.setattr(execute_evals.subprocess, "check_output", fake_check_output)
    output = tmp_path / "pilot"
    run = prepare_run(config_path, output)
    return config_path, output, run


def synthetic_judgment(case):
    return {
        "dimension_scores": {dimension: 3 for dimension in case["applicable_dimensions"]},
        "dimension_evidence": {
            dimension: "Synthetic test evidence." for dimension in case["applicable_dimensions"]
        },
        "expected_behavior_checks": [
            {"behavior": text, "observed": True, "evidence": "Synthetic test evidence."}
            for text in case["expected_behaviors"]
        ],
        "forbidden_behavior_checks": [
            {"behavior": text, "observed": False, "evidence": "Synthetic absence."}
            for text in case["forbidden_behaviors"]
        ],
        "hard_failure_checks": [
            {"behavior": text, "observed": False, "evidence": "Synthetic absence."}
            for text in case["hard_failures"]
        ],
        "citation_check": {
            "expected": False,
            "material_claims": 0,
            "supported_claims": 0,
            "notes": "Synthetic.",
        },
        "notes": "Synthetic unit-test assessment; not a behavioral baseline.",
    }


def test_preparation_freezes_inputs_without_model_execution(tmp_path, monkeypatch) -> None:
    def forbidden_invoke(*args, **kwargs):
        pytest.fail("Preparation must not execute a model")

    monkeypatch.setattr(execute_evals, "invoke", forbidden_invoke)
    config_path, output, run = prepared_pilot(tmp_path, monkeypatch)
    verify_snapshot(output, run, config_path)
    assert run["assessments"] == []
    assert run["run_status"] == "partial"
    assert run["source_snapshot"]["worktree_dirty"] is True
    assert validate_run_shape(run) == []


@pytest.mark.parametrize("target", ["instructions.txt", "configuration.yaml", "reviewer.json"])
def test_resume_rejects_modified_snapshot(tmp_path, monkeypatch, target) -> None:
    config_path, output, run = prepared_pilot(tmp_path, monkeypatch)
    (output / "snapshot" / target).write_text("Modified content", encoding="utf-8")
    with pytest.raises(ValueError, match="Snapshot integrity"):
        verify_snapshot(output, run, config_path)


def test_resume_rejects_changed_executor_metadata(tmp_path, monkeypatch) -> None:
    config_path, output, run = prepared_pilot(tmp_path, monkeypatch)
    run["generator"]["model"] = "different-model"
    with pytest.raises(ValueError, match="Run metadata differs"):
        verify_snapshot(output, run, config_path)


def test_instruction_bundle_rejects_eval_criteria() -> None:
    with pytest.raises(ValueError, match="outside the allowed"):
        instruction_bundle(["evals/judge-protocol.md"])


def test_pilot_configuration_cannot_claim_calibration(tmp_path) -> None:
    config = load_yaml(VALID_FIXTURES / "eval-config.yaml")
    config["judge"]["calibration_status"] = "calibrated"
    config_path = tmp_path / "config.yaml"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid evaluation configuration"):
        load_config(config_path)


def test_generator_prompt_does_not_include_review_fields() -> None:
    case = deepcopy(load_cases()["retention-decline-en"])
    case["scoring_notes"] = "SECRET_SCORING_NOTES"
    template = "{instructions}\n{input}\n{context}"
    prompt = generator_prompt(template, "Synthetic instructions", case)
    assert case["input"] in prompt
    assert "SECRET_SCORING_NOTES" not in prompt
    assert "expected_behaviors" not in prompt


def test_pilot_preserves_response_and_never_self_certifies_calibration(
    tmp_path, monkeypatch
) -> None:
    config_path, output, run = prepared_pilot(tmp_path, monkeypatch)
    case = load_cases()["retention-decline-en"]
    calls = []
    raw_response = " \nSynthetic response, with intentional whitespace.\n "

    def fake_invoke(prompt, executor, prefix, timeout, schema=None):
        calls.append((prefix.parent.name, prompt))
        if schema is None:
            assert "Case and judging criteria" not in prompt
            return raw_response
        assert raw_response in prompt
        return json.dumps(synthetic_judgment(case))

    monkeypatch.setattr(execute_evals, "invoke", fake_invoke)
    completed = execute(output, run)
    verify_snapshot(output, completed, config_path)
    assert [role for role, prompt in calls] == ["generation", "judging"]
    assert completed["assessments"][0]["response"] == raw_response
    assert "Dimension evidence:" in completed["assessments"][0]["notes"]
    assert completed["judge"]["calibration_status"] == "pilot"
    suite, cases, _ = execute_evals.load_review_context(output / "snapshot" / "reviewer.json")
    assert summarize_run(completed, suite, cases)["release_eligible"] is False
    timestamp = completed["completed_at"]
    assert execute(output, completed)["completed_at"] == timestamp
    assert len(calls) == 2


def test_failed_judging_can_resume_without_regenerating_response(tmp_path, monkeypatch) -> None:
    config_path, output, run = prepared_pilot(tmp_path, monkeypatch)
    case = load_cases()["retention-decline-en"]
    calls = []

    def first_attempt(prompt, executor, prefix, timeout, schema=None):
        calls.append(prefix.parent.name)
        if schema is None:
            return "Synthetic raw response"
        raise ValueError("Synthetic transport failure")

    monkeypatch.setattr(execute_evals, "invoke", first_attempt)
    with pytest.raises(ValueError, match="Synthetic transport failure"):
        execute(output, run)
    checkpoint = execute_evals.load_run(output / "run.json")
    assert checkpoint["run_status"] == "partial"
    verify_snapshot(output, checkpoint, config_path)

    def resumed_attempt(prompt, executor, prefix, timeout, schema=None):
        assert schema is not None, "Resume must not regenerate the completed response"
        calls.append(prefix.parent.name)
        return json.dumps(synthetic_judgment(case))

    monkeypatch.setattr(execute_evals, "invoke", resumed_attempt)
    assert execute(output, checkpoint)["run_status"] == "completed"
    assert calls == ["generation", "judging", "judging"]


def test_resume_rejects_altered_response_checkpoint(tmp_path, monkeypatch) -> None:
    config_path, output, run = prepared_pilot(tmp_path, monkeypatch)

    def interrupted(prompt, executor, prefix, timeout, schema=None):
        if schema is None:
            return "Synthetic original response"
        raise ValueError("Interrupted")

    monkeypatch.setattr(execute_evals, "invoke", interrupted)
    with pytest.raises(ValueError):
        execute(output, run)
    response_path = next((output / "generation").glob("*.response.txt"))
    response_path.write_text("Replacement response", encoding="utf-8")
    checkpoint = execute_evals.load_run(output / "run.json")
    with pytest.raises(ValueError, match="Snapshot integrity"):
        verify_snapshot(output, checkpoint, config_path)


@pytest.mark.parametrize("item_type", ["agent_message", "command_execution", "web_search"])
def test_codex_transport_rejects_tool_activity(tmp_path, monkeypatch, item_type) -> None:
    config = load_config(VALID_FIXTURES / "eval-config.yaml")

    def fake_run(command, **kwargs):
        assert "--ignore-user-config" in command
        assert command[command.index("--sandbox") + 1] == "read-only"
        final = Path(command[command.index("-o") + 1])
        final.write_text("Synthetic response", encoding="utf-8")
        events = [
            {"type": "item.completed", "item": {"type": item_type}},
            {"type": "turn.completed"},
        ]
        return SimpleNamespace(returncode=0, stdout="\n".join(map(json.dumps, events)), stderr="")

    monkeypatch.setattr(execute_evals.subprocess, "run", fake_run)
    prefix = tmp_path / "job"
    if item_type == "agent_message":
        assert invoke("Synthetic input", config["generator"], prefix, 30) == "Synthetic response"
    else:
        with pytest.raises(ValueError, match="Tools are outside"):
            invoke("Synthetic input", config["generator"], prefix, 30)
    assert prefix.with_suffix(".events.jsonl").is_file()


def test_timeout_preserves_partial_transport_events(tmp_path, monkeypatch) -> None:
    config = load_config(VALID_FIXTURES / "eval-config.yaml")

    def timed_out(command, **kwargs):
        raise subprocess.TimeoutExpired(command, 30, output=b"{}\n", stderr=b"partial error")

    monkeypatch.setattr(execute_evals.subprocess, "run", timed_out)
    prefix = tmp_path / "job"
    with pytest.raises(ValueError, match="timed out"):
        invoke("Synthetic input", config["generator"], prefix, 30)
    assert prefix.with_suffix(".events.jsonl").read_text() == "{}\n"
    assert prefix.with_suffix(".stderr.txt").read_text() == "partial error"

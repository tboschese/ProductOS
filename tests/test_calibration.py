import json
from copy import deepcopy

import pytest

from scripts import calibrate
from scripts.calibrate import compare, prepare
from scripts.validate_repository import ROOT

ARCHIVE = ROOT / "evals" / "baselines" / "seed-pilot-2026-10-05"
RUN = ARCHIVE / "run.json"
REVIEW = ARCHIVE / "snapshot" / "reviewer.json"
SAMPLE = [("retention-decline-en", 1), ("small-experiment-sample-en", 1)]
CONTROLS = ["retention-decline-en-invented-research"]


@pytest.fixture
def kit(tmp_path):
    output = tmp_path / "kit"
    key = prepare(RUN, REVIEW, output, SAMPLE, CONTROLS, seed=7)
    packet = json.loads((output / "packet.json").read_text(encoding="utf-8"))
    return output, key, packet


def sheet_from(key, packet, identity, *, detect_controls=True):
    run = json.loads(RUN.read_text(encoding="utf-8"))
    assessments = {(item["case_id"], item["repetition"]): item for item in run["assessments"]}
    items = []
    for item in packet["items"]:
        provenance = key["items"][item["item_id"]]
        if provenance["kind"] == "run":
            source = assessments[(provenance["case_id"], provenance["repetition"])]
            scored = {
                field: deepcopy(source[field])
                for field in (
                    "dimension_scores",
                    "expected_behavior_checks",
                    "forbidden_behavior_checks",
                    "hard_failure_checks",
                )
            }
        else:
            case = item["case"]
            scored = {
                "dimension_scores": {dimension: 0 for dimension in case["applicable_dimensions"]},
                **{
                    field: [
                        {"behavior": behavior, "observed": observed, "evidence": "Reviewer note."}
                        for behavior in case[case_field]
                    ]
                    for field, case_field, observed in (
                        ("expected_behavior_checks", "expected_behaviors", False),
                        ("forbidden_behavior_checks", "forbidden_behaviors", detect_controls),
                        ("hard_failure_checks", "hard_failures", detect_controls),
                    )
                },
            }
        items.append({"item_id": item["item_id"], **scored, "notes": "Synthetic test sheet."})
    return {
        "schema_version": "0.1.0",
        "packet_sha256": key["packet_sha256"],
        "reviewer": {"identity": identity, "type": "human"},
        "independent_of_automated_scores": True,
        "scored_at": "2026-10-06T12:00:00Z",
        "items": items,
    }


def write(path, value):
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_packet_is_blind_and_key_records_provenance(kit):
    output, key, packet = kit
    assert len(packet["items"]) == 3
    assert set(packet) == {"schema_version", "audience", "rubric", "rubric_sha256", "items"}
    for item in packet["items"]:
        assert set(item) == {"item_id", "case", "response"}
        assert set(item["case"]) == {*calibrate.REVIEW_CASE_FIELDS, "citations_expected"}
    assert "negative_control" not in json.dumps(packet)
    kinds = sorted(item["kind"] for item in key["items"].values())
    assert kinds == ["control", "run", "run"]
    template = json.loads((output / "score-template.json").read_text(encoding="utf-8"))
    assert template["packet_sha256"] == key["packet_sha256"]
    assert all(
        score is None for item in template["items"] for score in item["dimension_scores"].values()
    )


def test_preparation_is_deterministic_and_never_overwrites(tmp_path, kit):
    _, key, _ = kit
    again = prepare(RUN, REVIEW, tmp_path / "again", SAMPLE, CONTROLS, seed=7)
    assert again == key
    with pytest.raises(FileExistsError):
        prepare(RUN, REVIEW, tmp_path / "again", SAMPLE, CONTROLS, seed=7)


@pytest.mark.parametrize(
    ("sample", "controls", "message"),
    [
        ([("retention-decline-en", 2)], [], "not assessments"),
        (SAMPLE, ["missing-control"], "Unknown negative controls"),
    ],
)
def test_preparation_rejects_unknown_items(tmp_path, sample, controls, message):
    with pytest.raises(ValueError, match=message):
        prepare(RUN, REVIEW, tmp_path / "kit", sample, controls, seed=1)


def test_compare_reports_agreement_and_control_detection(tmp_path, kit):
    output, key, packet = kit
    faithful = write(tmp_path / "a.json", sheet_from(key, packet, "reviewer-a"))
    lenient = sheet_from(key, packet, "reviewer-b", detect_controls=False)
    for item in lenient["items"]:
        if key["items"][item["item_id"]]["kind"] == "run":
            item["dimension_scores"] = {d: 0 for d in item["dimension_scores"]}
    lenient_path = write(tmp_path / "b.json", lenient)

    report = compare(
        output / "key.json", output / "packet.json", RUN, [faithful, lenient_path]
    )
    pairs = {(pair["left"], pair["right"]): pair for pair in report["pairs"]}
    automated_a = pairs[("automated", "reviewer-a")]
    assert automated_a["shared_items"] == 2
    assert automated_a["dimension_scores"]["exact"] == 1.0
    assert automated_a["hard_failure_classification"]["agreement"] == 1.0
    assert pairs[("reviewer-a", "reviewer-b")]["hard_failure_classification"]["disagreements"]
    assert pairs[("automated", "reviewer-b")]["score_differences_of_two_or_more"]

    (control,) = report["negative_controls"]
    assert control["judges"]["reviewer-a"]["detected_all"] is True
    assert control["judges"]["reviewer-b"]["detected_all"] is False
    assert "automated" not in control["judges"]
    assert "calibrated" in report["interpretation"]


def test_compare_rejects_mismatched_or_incomplete_inputs(tmp_path, kit):
    output, key, packet = kit
    sheet = sheet_from(key, packet, "reviewer-a")

    stale = write(tmp_path / "stale.json", {**sheet, "packet_sha256": "0" * 64})
    with pytest.raises(ValueError, match="different calibration packet"):
        compare(output / "key.json", output / "packet.json", RUN, [stale])

    partial = write(tmp_path / "partial.json", {**sheet, "items": sheet["items"][:1]})
    with pytest.raises(ValueError, match="exactly the items"):
        compare(output / "key.json", output / "packet.json", RUN, [partial])

    unscored = deepcopy(sheet)
    first = next(iter(unscored["items"][0]["dimension_scores"]))
    unscored["items"][0]["dimension_scores"][first] = None
    with pytest.raises(ValueError, match="calibration-scores|None is not"):
        compare(
            output / "key.json",
            output / "packet.json",
            RUN,
            [write(tmp_path / "unscored.json", unscored)],
        )

    complete = write(tmp_path / "complete.json", sheet)
    (output / "packet.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="does not match the key"):
        compare(output / "key.json", output / "packet.json", RUN, [complete])


def test_compare_rejects_a_different_run(tmp_path, kit):
    output, key, packet = kit
    other = tmp_path / "run.json"
    other.write_text(RUN.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    sheet = write(tmp_path / "a.json", sheet_from(key, packet, "reviewer-a"))
    with pytest.raises(ValueError, match="differs from the run"):
        compare(output / "key.json", output / "packet.json", other, [sheet])


def test_repository_rejects_controls_with_undeclared_failures():
    from scripts.validate_repository import build_validators, load_schemas, validate_content

    source = calibrate.CONTROL_ROOT / f"{CONTROLS[0]}.yaml"
    probe = calibrate.CONTROL_ROOT / "zz-test-undeclared-failure.yaml"
    text = source.read_text(encoding="utf-8").replace(
        f"id: {CONTROLS[0]}", "id: zz-test-undeclared-failure"
    )
    probe.write_text(
        text.replace("Invent customer research or causal evidence.", "Undeclared failure."),
        encoding="utf-8",
    )
    try:
        failures = validate_content(build_validators(*load_schemas()))
    finally:
        probe.unlink()
    assert any("not declared by retention-decline-en" in failure for failure in failures)


def fake_judge(detect):
    calls = []

    def invoke(prompt, judge, prefix, timeout, schema):
        calls.append(prefix.name)
        properties = schema["properties"]

        def checks(field, observed):
            behaviors = properties[field]["items"]["properties"]["behavior"].get("enum", [])
            return [
                {"behavior": behavior, "observed": observed, "evidence": "Fake judge."}
                for behavior in behaviors
            ]

        dimensions = list(properties["dimension_scores"]["properties"])
        return json.dumps(
            {
                "dimension_scores": {dimension: 0 for dimension in dimensions},
                "dimension_evidence": {dimension: "Fake judge." for dimension in dimensions},
                "expected_behavior_checks": checks("expected_behavior_checks", False),
                "forbidden_behavior_checks": checks("forbidden_behavior_checks", detect),
                "hard_failure_checks": checks("hard_failure_checks", detect),
                "citation_check": {
                    "expected": False,
                    "material_claims": 0,
                    "supported_claims": 0,
                    "notes": "",
                },
                "notes": "Fake judge.",
            }
        )

    return invoke, calls


def test_judge_controls_uses_frozen_judge_and_resumes(tmp_path):
    invoke, calls = fake_judge(detect=True)
    report = calibrate.judge_controls(
        ARCHIVE, tmp_path / "judged", CONTROLS, invoke_judge=invoke, cli_version="fake 1"
    )
    assert calls == CONTROLS
    (result,) = report["controls"]
    assert result["detected_all"] is True
    assert report["judge"]["calibration_status"] == "pilot"
    assert report["run_cli_version"] != report["judge_cli_version"]

    again, repeated = fake_judge(detect=False)
    resumed = calibrate.judge_controls(
        ARCHIVE, tmp_path / "judged", CONTROLS, invoke_judge=again, cli_version="fake 1"
    )
    assert repeated == []
    assert resumed["controls"][0]["detected_all"] is True

    meta = tmp_path / "judged" / f"{CONTROLS[0]}.meta.json"
    meta.write_text(meta.read_text().replace('"pilot"', '"calibrated"'), encoding="utf-8")
    with pytest.raises(ValueError, match="different inputs"):
        calibrate.judge_controls(
            ARCHIVE, tmp_path / "judged", CONTROLS, invoke_judge=again, cli_version="fake 1"
        )


def test_judge_controls_reports_missed_failures(tmp_path):
    invoke, _ = fake_judge(detect=False)
    report = calibrate.judge_controls(
        ARCHIVE, tmp_path / "judged", invoke_judge=invoke, cli_version="fake 1"
    )
    assert len(report["controls"]) == 4
    assert all(not result["detected_all"] and result["missed"] for result in report["controls"])


def test_cli_prepare_and_compare(tmp_path, capsys):
    output = tmp_path / "kit"
    assert (
        calibrate.main(
            [
                "prepare",
                "--run", str(RUN),
                "--review-packet", str(REVIEW),
                "--output", str(output),
                "--sample", "retention-decline-en#1",
                "--control", CONTROLS[0],
            ]
        )
        == 0
    )
    assert "Send only packet.json" in capsys.readouterr().out
    key = json.loads((output / "key.json").read_text(encoding="utf-8"))
    packet = json.loads((output / "packet.json").read_text(encoding="utf-8"))
    sheet = write(tmp_path / "a.json", sheet_from(key, packet, "reviewer-a"))
    arguments = [
        "compare",
        "--key", str(output / "key.json"),
        "--packet", str(output / "packet.json"),
        "--run", str(RUN),
        "--scores", str(sheet),
    ]
    assert calibrate.main(arguments) == 0
    assert "automated vs reviewer-a" in capsys.readouterr().out
    assert calibrate.main([*arguments[:-1], str(tmp_path / "missing.json")]) == 1

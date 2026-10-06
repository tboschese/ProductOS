import json
from datetime import date
from urllib.error import HTTPError, URLError

import pytest

from scripts import audit_sources
from scripts.audit_sources import audit_freshness, probe_url
from scripts.validate_repository import VALID_FIXTURES, build_validators, load_schemas, load_yaml


def source(last_verified: str, interval: int = 30) -> dict:
    return {
        "id": "test-source",
        "last_verified": last_verified,
        "freshness": {
            "temporal_stability": "evolving",
            "review_interval_days": interval,
        },
    }


def test_source_is_fresh_through_due_date() -> None:
    result = audit_freshness([source("2026-01-01")], date(2026, 1, 31))[0]
    assert result["status"] == "fresh"
    assert result["days_until_due"] == 0


def test_source_is_stale_after_due_date() -> None:
    result = audit_freshness([source("2026-01-01")], date(2026, 2, 1))[0]
    assert result["status"] == "stale"
    assert result["days_until_due"] == -1


def test_future_verification_is_invalid_for_audit_date() -> None:
    result = audit_freshness([source("2026-02-01")], date(2026, 1, 31))[0]
    assert result["status"] == "future_verification"


@pytest.mark.parametrize(
    ("verified", "fail_stale", "expected_exit"),
    [
        ("2026-01-01", True, 0),
        ("2025-12-31", True, 2),
        ("2026-02-01", True, 2),
        ("2025-12-31", False, 0),
    ],
)
def test_cli_freshness_gate(monkeypatch, capsys, verified, fail_stale, expected_exit) -> None:
    monkeypatch.setattr(audit_sources, "run_validation", lambda: [])
    monkeypatch.setattr(audit_sources, "load_sources", lambda: [source(verified)])
    args = ["audit_sources", "--as-of", "2026-01-31", "--json"]
    if fail_stale:
        args.append("--fail-stale")
    monkeypatch.setattr("sys.argv", args)

    assert audit_sources.main() == expected_exit
    report = json.loads(capsys.readouterr().out)
    assert report["as_of"] == "2026-01-31"
    assert "links" not in report


def test_cli_writes_same_json_report_to_file(monkeypatch, capsys, tmp_path) -> None:
    monkeypatch.setattr(audit_sources, "run_validation", lambda: [])
    monkeypatch.setattr(audit_sources, "load_sources", lambda: [source("2026-01-01")])
    output = tmp_path / "reports" / "audit.json"
    monkeypatch.setattr(
        "sys.argv",
        ["audit_sources", "--as-of", "2026-01-31", "--json", "--output", str(output)],
    )

    assert audit_sources.main() == 0
    assert output.read_text(encoding="utf-8") == capsys.readouterr().out


def test_cli_stops_before_loading_sources_when_repository_is_invalid(monkeypatch, capsys) -> None:
    monkeypatch.setattr(audit_sources, "run_validation", lambda: ["invalid source metadata"])
    monkeypatch.setattr("sys.argv", ["audit_sources", "--check-links"])

    def unexpected_load():
        pytest.fail("Invalid repository must not load sources or probe URLs")

    monkeypatch.setattr(audit_sources, "load_sources", unexpected_load)
    assert audit_sources.main() == 1
    assert "invalid source metadata" in capsys.readouterr().err


def test_cli_failed_link_probe_returns_nonzero(monkeypatch, capsys) -> None:
    monkeypatch.setattr(audit_sources, "run_validation", lambda: [])
    monkeypatch.setattr(audit_sources, "load_sources", lambda: [source("2026-01-01")])
    monkeypatch.setattr(
        audit_sources, "audit_links", lambda sources, timeout: [{"status": "unreachable"}]
    )
    monkeypatch.setattr(
        "sys.argv", ["audit_sources", "--as-of", "2026-01-31", "--check-links", "--json"]
    )

    assert audit_sources.main() == 3
    assert json.loads(capsys.readouterr().out)["links"][0]["status"] == "unreachable"


def test_probe_uses_get_when_head_is_unsupported(monkeypatch) -> None:
    requests = []

    class Response:
        status = 206

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def geturl(self):
            return "https://example.org/resolved"

    def fake_urlopen(request, timeout):
        requests.append(request)
        assert timeout == 5
        if request.get_method() == "HEAD":
            raise HTTPError(request.full_url, 405, "Method Not Allowed", {}, None)
        return Response()

    monkeypatch.setattr(audit_sources, "urlopen", fake_urlopen)
    result = probe_url("https://example.org/source", timeout=5)

    assert [request.get_method() for request in requests] == ["HEAD", "GET"]
    assert requests[1].get_header("Range") == "bytes=0-0"
    assert result["status"] == "reachable"
    assert result["resolved_url"] == "https://example.org/resolved"


def test_probe_reports_network_failure_without_raising(monkeypatch) -> None:
    def failed_urlopen(request, timeout):
        raise URLError("connection unavailable")

    monkeypatch.setattr(audit_sources, "urlopen", failed_urlopen)
    result = probe_url("https://example.org/source", timeout=5)
    assert result["status"] == "unreachable"
    assert result["http_status"] is None
    assert "connection unavailable" in result["error"]


@pytest.mark.parametrize(
    "freshness",
    [
        None,
        {},
        {"temporal_stability": "unknown", "review_interval_days": 30},
        {"temporal_stability": "stable", "review_interval_days": 0},
        {"temporal_stability": "stable", "review_interval_days": 3651},
        {"temporal_stability": "stable", "review_interval_days": 1.5},
    ],
)
def test_source_schema_rejects_missing_or_invalid_freshness(freshness) -> None:
    schemas, registry = load_schemas()
    validator = build_validators(schemas, registry)["source"]
    record = load_yaml(VALID_FIXTURES / "source.yaml")
    if freshness is None:
        record.pop("freshness")
    else:
        record["freshness"] = freshness
    assert list(validator.iter_errors(record))


def test_source_schema_rejects_unmigrated_version() -> None:
    schemas, registry = load_schemas()
    validator = build_validators(schemas, registry)["source"]
    record = load_yaml(VALID_FIXTURES / "source.yaml")
    record["schema_version"] = "0.3.0"
    errors = list(validator.iter_errors(record))
    assert any(list(error.path) == ["schema_version"] for error in errors)

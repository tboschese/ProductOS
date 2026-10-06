#!/usr/bin/env python3
"""Audit registered source freshness and optionally probe access URLs."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from scripts.validate_repository import ROOT, load_yaml, run_validation

SOURCE_ROOT = ROOT / "knowledge" / "sources"
USER_AGENT = "ProductOS-source-audit/0.1 (+https://github.com/tboschese/ProductOS)"


def load_sources() -> list[dict[str, Any]]:
    sources = []
    for path in sorted(SOURCE_ROOT.glob("*.yaml")):
        source = load_yaml(path)
        if not isinstance(source, dict):
            raise ValueError(f"Invalid source record: {path.relative_to(ROOT)}")
        sources.append(source)
    return sources


def audit_freshness(
    sources: list[dict[str, Any]], as_of: date
) -> list[dict[str, Any]]:
    results = []
    for source in sources:
        verified = date.fromisoformat(source["last_verified"])
        interval = source["freshness"]["review_interval_days"]
        due = verified + timedelta(days=interval)
        if verified > as_of:
            status = "future_verification"
        elif as_of > due:
            status = "stale"
        else:
            status = "fresh"
        results.append(
            {
                "source_id": source["id"],
                "temporal_stability": source["freshness"]["temporal_stability"],
                "last_verified": verified.isoformat(),
                "review_due": due.isoformat(),
                "days_until_due": (due - as_of).days,
                "status": status,
            }
        )
    return results


def probe_url(url: str, timeout: float) -> dict[str, Any]:
    headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    methods = ("HEAD", "GET")
    last_error = ""
    for method in methods:
        request_headers = dict(headers)
        if method == "GET":
            request_headers["Range"] = "bytes=0-0"
        request = Request(url, headers=request_headers, method=method)
        try:
            with urlopen(request, timeout=timeout) as response:
                return {
                    "status": "reachable",
                    "http_status": response.status,
                    "resolved_url": response.geturl(),
                    "method": method,
                    "error": None,
                }
        except HTTPError as error:
            last_error = f"HTTP {error.code}: {error.reason}"
            if method == "HEAD" and error.code in {403, 405, 501}:
                continue
            return {
                "status": "unreachable",
                "http_status": error.code,
                "resolved_url": url,
                "method": method,
                "error": last_error,
            }
        except (URLError, TimeoutError, OSError) as error:
            last_error = str(error)
            if method == "HEAD":
                continue
            return {
                "status": "unreachable",
                "http_status": None,
                "resolved_url": url,
                "method": method,
                "error": last_error,
            }
    return {
        "status": "unreachable",
        "http_status": None,
        "resolved_url": url,
        "method": "GET",
        "error": last_error or "No response",
    }


def audit_links(sources: list[dict[str, Any]], timeout: float) -> list[dict[str, Any]]:
    results = []
    for source in sources:
        result = probe_url(source["url"], timeout)
        results.append({"source_id": source["id"], "url": source["url"], **result})
    return results


def print_report(report: dict[str, Any]) -> None:
    print(f"Source audit as of {report['as_of']}: {report['source_count']} sources")
    for item in report["freshness"]:
        print(
            f"- {item['status'].upper()} {item['source_id']}: "
            f"verified={item['last_verified']}, due={item['review_due']}"
        )
    for item in report.get("links", []):
        detail = item["http_status"] if item["http_status"] is not None else item["error"]
        print(f"- {item['status'].upper()} {item['source_id']}: {detail}")


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument(
        "--as-of",
        type=date.fromisoformat,
        default=date.today(),
        help="Audit date in YYYY-MM-DD form (default: today)",
    )
    command.add_argument(
        "--fail-stale", action="store_true", help="Exit nonzero for stale or future-dated sources"
    )
    command.add_argument(
        "--check-links", action="store_true", help="Probe external source URLs (not deterministic)"
    )
    command.add_argument(
        "--timeout", type=float, default=15.0, help="Per-request timeout for --check-links"
    )
    command.add_argument("--json", action="store_true", help="Print JSON instead of text")
    command.add_argument("--output", type=Path, help="Write the JSON report to a file")
    return command


def main() -> int:
    args = parser().parse_args()
    failures = run_validation()
    if failures:
        for failure in failures:
            print(f"error: {failure}", file=sys.stderr)
        return 1

    try:
        sources = load_sources()
        freshness = audit_freshness(sources, args.as_of)
        links = audit_links(sources, args.timeout) if args.check_links else []
    except (OSError, ValueError, KeyError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    report = {
        "as_of": args.as_of.isoformat(),
        "source_count": len(sources),
        "freshness": freshness,
    }
    if args.check_links:
        report["links"] = links

    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.json:
        print(rendered, end="")
    else:
        print_report(report)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        if not args.json:
            print(f"Wrote report: {args.output}")

    freshness_failed = any(item["status"] != "fresh" for item in freshness)
    link_failed = any(item["status"] != "reachable" for item in links)
    if args.check_links and link_failed:
        return 3
    if args.fail_stale and freshness_failed:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

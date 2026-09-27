#!/usr/bin/env python3
"""Detect deterministic ID, concept-name, and terminology-alias collisions."""

from __future__ import annotations

import re
import unicodedata

from scripts.validate_repository import ROOT, load_yaml, run_validation

KNOWLEDGE_ROOT = ROOT / "knowledge"


def normalize(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold().strip()
    return re.sub(r"\s+", " ", normalized)


def duplicate_concepts() -> list[str]:
    owners: dict[str, str] = {}
    failures: list[str] = []
    for path in sorted((KNOWLEDGE_ROOT / "concepts").glob("*.yaml")):
        entity = load_yaml(path)
        if not isinstance(entity, dict) or entity.get("status") == "deprecated":
            continue
        entity_id = str(entity["id"])
        labels = [str(entity["canonical_name"]), *entity.get("aliases", [])]
        for label in labels:
            key = normalize(label)
            previous = owners.get(key)
            if previous and previous != entity_id:
                failures.append(
                    f"Concept label {label!r} maps to both {previous} and {entity_id}"
                )
            else:
                owners[key] = entity_id
    return failures


def duplicate_terminology() -> list[str]:
    owners: dict[tuple[str, str], str] = {}
    failures: list[str] = []
    for path in sorted((KNOWLEDGE_ROOT / "terminology").glob("*.yaml")):
        entity = load_yaml(path)
        if not isinstance(entity, dict) or entity.get("status") == "deprecated":
            continue
        entity_id = str(entity["id"])
        for locale, localized in entity["localized"].items():
            labels = [localized["preferred"], *localized["aliases"]]
            for label in labels:
                key = (locale, normalize(label))
                previous = owners.get(key)
                if previous and previous != entity_id:
                    failures.append(
                        f"Terminology alias {label!r} in {locale} maps to both "
                        f"{previous} and {entity_id}"
                    )
                else:
                    owners[key] = entity_id
    return failures


def run_duplicate_checks() -> list[str]:
    return [*duplicate_concepts(), *duplicate_terminology()]


def main() -> int:
    repository_failures = run_validation()
    duplicate_failures = run_duplicate_checks()
    failures = [*repository_failures, *duplicate_failures]
    if failures:
        for failure in failures:
            print(f"error: {failure}")
        return 1
    print("No deterministic concept or terminology collisions found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

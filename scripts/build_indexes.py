#!/usr/bin/env python3
"""Build deterministic indexes for canonical ProductOS knowledge."""

from __future__ import annotations

import argparse
import json

from scripts.validate_repository import KNOWLEDGE_SCHEMA_BY_PARENT, ROOT, load_yaml, run_validation

KNOWLEDGE_ROOT = ROOT / "knowledge"
INDEX_PATH = KNOWLEDGE_ROOT / "index.json"


def entity_label(entity: dict[str, object]) -> str:
    for field in ("canonical_name", "name", "title", "statement"):
        value = entity.get(field)
        if isinstance(value, str) and value:
            return value
    return str(entity["id"])


def build_index() -> dict[str, object]:
    groups: dict[str, list[dict[str, object]]] = {}
    for directory_name in sorted(KNOWLEDGE_SCHEMA_BY_PARENT):
        entries = []
        for path in sorted((KNOWLEDGE_ROOT / directory_name).glob("*.yaml")):
            entity = load_yaml(path)
            if not isinstance(entity, dict):
                raise ValueError(f"Invalid entity shape: {path.relative_to(ROOT)}")
            entries.append(
                {
                    "id": entity["id"],
                    "label": entity_label(entity),
                    "status": entity["status"],
                    "path": path.relative_to(ROOT).as_posix(),
                    "primary_domain": entity.get("primary_domain"),
                }
            )
        groups[directory_name] = sorted(entries, key=lambda entry: str(entry["id"]))

    return {"schema_version": "0.3.0", "entities": groups}


def serialized_index() -> str:
    return json.dumps(build_index(), indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    mode = command.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="Write knowledge/index.json")
    mode.add_argument("--check", action="store_true", help="Fail if the committed index is stale")
    return command


def main() -> int:
    args = parser().parse_args()
    failures = run_validation()
    if failures:
        for failure in failures:
            print(f"error: {failure}")
        return 1

    expected = serialized_index()
    if args.write:
        INDEX_PATH.write_text(expected, encoding="utf-8")
        print(f"Wrote {INDEX_PATH.relative_to(ROOT)}")
        return 0

    if args.check:
        actual = INDEX_PATH.read_text(encoding="utf-8") if INDEX_PATH.exists() else ""
        if actual != expected:
            print("knowledge/index.json is stale; run python -m scripts.build_indexes --write")
            return 1
        print("Knowledge index is current.")
        return 0

    print(expected, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import json

from scripts.build_indexes import INDEX_PATH, build_index, serialized_index


def test_index_is_deterministic_and_current() -> None:
    first = serialized_index()
    second = serialized_index()

    assert first == second
    assert INDEX_PATH.read_text(encoding="utf-8") == first


def test_index_has_all_entity_groups() -> None:
    index = build_index()
    groups = index["entities"]

    assert "sources" in groups
    assert "claims" in groups
    assert "relationships" in groups
    assert json.loads(serialized_index()) == index

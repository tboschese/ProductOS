"""Read runtime contracts from an explicitly selected ProductOS repository."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


class RuntimeFailure(ValueError):
    """A recoverable user-facing runtime failure."""


class Contracts:
    def __init__(self, repository: Path):
        self.repository = repository.resolve()
        directory = self.repository / "schemas"
        if not directory.is_dir():
            raise RuntimeFailure("Selecione o repositório ProductOS com --repository.")
        schemas = [json.loads(p.read_bytes()) for p in sorted(directory.glob("*.schema.json"))]
        registry = Registry().with_resources(
            (schema["$id"], Resource.from_contents(schema)) for schema in schemas
        )
        self.validators = {
            schema["$id"].rsplit("/", 1)[-1].removesuffix(".schema.json"): Draft202012Validator(
                schema, registry=registry, format_checker=FormatChecker()
            )
            for schema in schemas
        }
        required = {"workspace-decision", "workspace-analysis", "ai-connection", "decision-record"}
        if not required <= self.validators.keys():
            raise RuntimeFailure("O repositório não contém os contratos desta versão do terminal.")

    def errors(self, name: str, value: object) -> list[str]:
        return [
            f"{'.'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
            for error in self.validators[name].iter_errors(value)
        ]

    def validate(self, name: str, value: object) -> None:
        errors = self.errors(name, value)
        if errors:
            raise RuntimeFailure(f"Registro inválido ({name}): {'; '.join(errors)}")


def find_repository(selected: Path | None = None) -> Path:
    if selected is not None:
        return selected.expanduser().resolve()
    candidates = [Path.cwd(), *Path.cwd().parents, Path(__file__).resolve().parents[1]]
    for candidate in candidates:
        if (candidate / ".agents/skills/staff-product-manager/SKILL.md").is_file():
            return candidate
    raise RuntimeFailure("Repositório ProductOS não encontrado. Use --repository CAMINHO.")

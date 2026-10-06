"""Local user records and immutable analysis snapshots; no canonical knowledge writes."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from productos.contracts import Contracts, RuntimeFailure

MAX_TEXT_BYTES = 2_000_000
ID_PATTERN = re.compile(r"^(?:decision|analysis)-[a-f0-9]{32}$")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read_text(path: Path) -> str:
    with path.open("rb") as handle:
        data = handle.read(MAX_TEXT_BYTES + 1)
    if len(data) > MAX_TEXT_BYTES:
        raise RuntimeFailure("O arquivo excede o limite de 2 MB.")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeFailure("Use um arquivo de texto em UTF-8.") from exc


class Workspace:
    def __init__(self, directory: Path, contracts: Contracts):
        self.root = directory.expanduser().resolve()
        self.contracts = contracts
        for protected in (
            "knowledge",
            "schemas",
            ".agents",
            "research",
            "evals",
            "docs",
            "scripts",
            "productos",
        ):
            try:
                self.root.relative_to(contracts.repository / protected)
            except ValueError:
                continue
            raise RuntimeFailure("Escolha um workspace pessoal fora dos arquivos canônicos.")
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self._lock = None

    def __enter__(self):
        self._lock = self.path("workspace.lock").open("a+b")
        try:
            if os.name == "nt":
                import msvcrt

                self._lock.seek(0)
                self._lock.write(b"0")
                self._lock.flush()
                self._lock.seek(0)
                msvcrt.locking(self._lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(self._lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            self._lock.close()
            self._lock = None
            raise RuntimeFailure("Este workspace já está aberto em outro processo.") from exc
        try:
            self.recover_interrupted()
        except BaseException:
            self.__exit__()
            raise
        return self

    def __exit__(self, *_):
        if self._lock is not None:
            self._lock.close()
            self._lock = None

    def path(self, *parts: str) -> Path:
        path = self.root.joinpath(*parts)
        try:
            path.resolve().relative_to(self.root)
        except ValueError as exc:
            raise RuntimeFailure("Caminho fora do workspace.") from exc
        return path

    def record_path(self, kind: str, record_id: str) -> Path:
        prefix = "decision" if kind == "decisions" else "analysis"
        if not ID_PATTERN.fullmatch(record_id) or not record_id.startswith(prefix + "-"):
            raise RuntimeFailure("Identificador inválido.")
        return (
            self.path(kind, record_id + ".json")
            if kind == "decisions"
            else self.path(kind, record_id, "analysis.json")
        )

    def atomic_write(self, path: Path, data: bytes) -> None:
        self.path(str(path.relative_to(self.root)))
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            try:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
                os.replace(temporary, path)
            finally:
                temporary.unlink(missing_ok=True)

    def save(self, schema: str, path: Path, value: dict) -> dict:
        self.contracts.validate(schema, value)
        self.atomic_write(path, json_bytes(value))
        return value

    def create(self, title: str, question: str, locale: str = "pt-BR", context: str = "") -> dict:
        stamp = now()
        value = {
            "schema_version": "0.1.0",
            "id": "decision-" + uuid4().hex,
            "revision": 1,
            "title": title.strip(),
            "locale": locale,
            "question": question.strip(),
            "context": context,
            "evidence": [],
            "created_at": stamp,
            "updated_at": stamp,
            "chosen_decision": "",
            "next_action": "",
        }
        return self.save("workspace-decision", self.record_path("decisions", value["id"]), value)

    def decision(self, decision_id: str) -> dict:
        path = self.record_path("decisions", decision_id)
        if not path.is_file():
            raise RuntimeFailure("Decisão não encontrada.")
        value = json.loads(path.read_bytes())
        self.contracts.validate("workspace-decision", value)
        if value["id"] != decision_id:
            raise RuntimeFailure("O ID salvo não corresponde ao arquivo da decisão.")
        return value

    def decisions(self) -> list[dict]:
        directory = self.path("decisions")
        return sorted(
            (self.decision(p.stem) for p in directory.glob("decision-*.json")),
            key=lambda item: item["updated_at"],
            reverse=True,
        )

    def update(self, value: dict) -> dict:
        current = self.decision(value["id"])
        if current["revision"] != value["revision"]:
            raise RuntimeFailure("A decisão mudou. Reabra antes de salvar.")
        value = {**value, "revision": value["revision"] + 1, "updated_at": now()}
        return self.save("workspace-decision", self.record_path("decisions", value["id"]), value)

    def add_evidence(
        self,
        value: dict,
        statement: str,
        source: str,
        locator: str,
        status: str = "observation",
        limitations: str = "",
        content: str = "",
    ) -> dict:
        item = {
            "id": "evidence-" + uuid4().hex,
            "statement": statement.strip(),
            "epistemic_status": status,
            "source": source.strip(),
            "locator": locator.strip(),
            "limitations": limitations,
            "content": content,
        }
        return self.update({**value, "evidence": [*value["evidence"], item]})

    def connection(self) -> dict:
        path = self.path("connection.json")
        value = (
            json.loads(path.read_bytes())
            if path.exists()
            else {
                "schema_version": "0.1.0",
                "kind": "manual",
                "model": None,
                "command": [],
                "timeout_seconds": 240,
            }
        )
        self.contracts.validate("ai-connection", value)
        return value

    def set_connection(self, value: dict) -> dict:
        return self.save("ai-connection", self.path("connection.json"), value)

    def prepare_analysis(
        self,
        decision: dict,
        connection: dict,
        prompt: str,
        instructions: str,
        output_format: str = "markdown",
    ) -> dict:
        self.contracts.validate("workspace-decision", decision)
        self.contracts.validate("ai-connection", connection)
        if len(prompt.encode("utf-8")) > 400_000:
            raise RuntimeFailure("O contexto excede 400 KB. Reduza os anexos ou o texto.")
        analysis_id = "analysis-" + uuid4().hex
        directory = self.record_path("analyses", analysis_id).parent
        directory.mkdir(parents=True, mode=0o700)
        files = {
            "prompt.txt": prompt.encode("utf-8"),
            "decision.json": json_bytes(decision),
            "instructions.txt": instructions.encode("utf-8"),
        }
        for name, data in files.items():
            self.atomic_write(directory / name, data)
        value = {
            "schema_version": "0.1.0",
            "id": analysis_id,
            "decision_id": decision["id"],
            "decision_revision": decision["revision"],
            "status": "exported" if connection["kind"] == "manual" else "running",
            "started_at": now(),
            "completed_at": None,
            "connection": {
                "kind": connection["kind"],
                "requested_model": connection["model"],
                "reported_model": None,
                "executable": (connection["command"] or ["codex"])[0]
                if connection["kind"] != "manual"
                else None,
            },
            "input_hashes": {name: sha256(data) for name, data in files.items()},
            "response_sha256": None,
            "error": None,
            "output_format": output_format,
            "structured_status": "pending"
            if output_format == "decision_record"
            else "not_requested",
        }
        return self.save("workspace-analysis", directory / "analysis.json", value)

    def analysis(self, analysis_id: str, verify: bool = True) -> dict:
        path = self.record_path("analyses", analysis_id)
        if not path.is_file():
            raise RuntimeFailure("Análise não encontrada.")
        value = json.loads(path.read_bytes())
        self.contracts.validate("workspace-analysis", value)
        if value["id"] != analysis_id:
            raise RuntimeFailure("O ID salvo não corresponde ao arquivo da análise.")
        if verify:
            for name, expected in value["input_hashes"].items():
                data = self.path("analyses", analysis_id, name).read_bytes()
                if sha256(data) != expected:
                    raise RuntimeFailure("O contexto salvo da análise foi alterado.")
            snapshot = json.loads(self.path("analyses", analysis_id, "decision.json").read_bytes())
            self.contracts.validate("workspace-decision", snapshot)
            if (snapshot["id"], snapshot["revision"]) != (
                value["decision_id"],
                value["decision_revision"],
            ):
                raise RuntimeFailure("A análise não corresponde à revisão do contexto salvo.")
            if value["response_sha256"] is not None:
                response = self.path("analyses", analysis_id, "response.txt").read_bytes()
                if sha256(response) != value["response_sha256"]:
                    raise RuntimeFailure("A resposta salva da análise foi alterada.")
        return value

    def analyses(self, decision_id: str) -> list[dict]:
        self.record_path("decisions", decision_id)
        return sorted(
            (
                value
                for p in self.path("analyses").glob("analysis-*/analysis.json")
                if (value := self.analysis(p.parent.name))["decision_id"] == decision_id
            ),
            key=lambda item: item["started_at"],
            reverse=True,
        )

    def finish(self, analysis_id: str, response: str, reported_model: str | None = None) -> dict:
        value = self.analysis(analysis_id)
        if value["status"] not in {"exported", "running"}:
            raise RuntimeFailure("Esta análise já foi encerrada; crie uma nova análise.")
        data = response.encode("utf-8")
        if not response.strip() or len(data) > MAX_TEXT_BYTES:
            raise RuntimeFailure("A resposta deve ser texto não vazio com até 2 MB.")
        directory = self.record_path("analyses", analysis_id).parent
        structured_status = value["structured_status"]
        if value["output_format"] == "decision_record":
            candidate = response.strip()
            if candidate.startswith("```json\n") and candidate.endswith("```"):
                candidate = candidate[8:-3].strip()
            try:
                record = json.loads(candidate)
                errors = self.contracts.errors("decision-record", record)
            except json.JSONDecodeError:
                record, errors = None, ["A resposta não é JSON válido."]
            structured_status = "invalid" if errors else "valid"
            if not errors:
                self.atomic_write(directory / "decision-record.json", json_bytes(record))
            else:
                self.atomic_write(directory / "validation-errors.json", json_bytes(errors))
        response_path = self.path("analyses", analysis_id, "response.txt")
        if response_path.exists():
            raise RuntimeFailure("Uma resposta já existe; preserve a análise e crie outra.")
        self.atomic_write(response_path, data)
        value.update(
            status="completed",
            completed_at=now(),
            response_sha256=sha256(data),
            structured_status=structured_status,
        )
        value["connection"]["reported_model"] = reported_model
        return self.save("workspace-analysis", directory / "analysis.json", value)

    def fail(self, analysis_id: str, error: str, cancelled: bool = False) -> dict:
        value = self.analysis(analysis_id)
        if value["status"] != "running":
            raise RuntimeFailure("A análise não está em execução.")
        value.update(status="cancelled" if cancelled else "failed", completed_at=now(), error=error)
        return self.save("workspace-analysis", self.record_path("analyses", analysis_id), value)

    def recover_interrupted(self) -> None:
        for path in self.path("analyses").glob("analysis-*/analysis.json"):
            value = self.analysis(path.parent.name)
            if value["status"] == "running":
                self.fail(value["id"], "interrupted: execução anterior não foi encerrada")

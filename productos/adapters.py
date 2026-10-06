"""Async installed-assistant adapters. Credentials stay with the user's assistant."""

from __future__ import annotations

import asyncio
import json
import os
import signal
import tempfile
from pathlib import Path

from productos.contracts import RuntimeFailure
from productos.workspace import MAX_TEXT_BYTES

MAX_TRANSPORT_BYTES = 8_000_000


class AdapterFailure(RuntimeFailure):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


async def stop_process(process: asyncio.subprocess.Process) -> None:
    if process.returncode is None:
        try:
            if os.name == "posix":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
        except ProcessLookupError:
            pass

    async def discard(stream):
        while await stream.read(65536):
            pass

    await asyncio.gather(discard(process.stdout), discard(process.stderr))
    await process.wait()


async def read_limited(stream: asyncio.StreamReader) -> bytes:
    chunks, size = [], 0
    while chunk := await stream.read(65536):
        size += len(chunk)
        if size > MAX_TRANSPORT_BYTES:
            raise AdapterFailure("output_limit", "O assistente excedeu o limite de saída.")
        chunks.append(chunk)
    return b"".join(chunks)


async def execute_process(
    argv: list[str], prompt: str, directory: Path, timeout: int
) -> tuple[bytes, bytes]:
    try:
        process = await asyncio.create_subprocess_exec(
            *argv,
            cwd=directory,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            start_new_session=os.name == "posix",
        )
    except OSError as exc:
        raise AdapterFailure(
            "not_available", "Assistente não encontrado ou não executável."
        ) from exc

    async def communicate():
        async def send():
            try:
                process.stdin.write(prompt.encode("utf-8"))
                await process.stdin.drain()
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                process.stdin.close()

        readers = [
            asyncio.create_task(send()),
            asyncio.create_task(read_limited(process.stdout)),
            asyncio.create_task(read_limited(process.stderr)),
        ]
        try:
            _, stdout, stderr = await asyncio.gather(*readers)
        finally:
            for reader in readers:
                reader.cancel()
            await asyncio.gather(*readers, return_exceptions=True)
        await process.wait()
        return stdout, stderr

    task = asyncio.create_task(communicate())
    try:
        stdout, stderr = await asyncio.wait_for(task, timeout)
    except asyncio.TimeoutError as exc:
        await stop_process(process)
        raise AdapterFailure("timeout", "O assistente excedeu o tempo configurado.") from exc
    except BaseException:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await stop_process(process)
        raise
    if process.returncode:
        raise AdapterFailure(
            f"exit_{process.returncode}",
            f"O assistente encerrou com código {process.returncode}. "
            "Confira a autenticação e o comando na instalação do assistente.",
        )
    return stdout, stderr


def decode_answer(data: bytes) -> str:
    if len(data) > MAX_TEXT_BYTES:
        raise AdapterFailure("answer_limit", "A resposta excedeu 2 MB.")
    try:
        value = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AdapterFailure("encoding", "O assistente não retornou texto UTF-8.") from exc
    if not value.strip():
        raise AdapterFailure("empty", "O assistente retornou uma resposta vazia.")
    return value


async def invoke(connection: dict, prompt: str) -> str:
    kind = connection["kind"]
    if kind == "manual":
        raise AdapterFailure("manual", "Exporte o contexto e importe a resposta no modo manual.")
    with tempfile.TemporaryDirectory(prefix="productos-ai-") as temporary:
        directory = Path(temporary)
        if kind == "command":
            argv = list(connection["command"])
            if "{model}" in argv:
                if not connection["model"]:
                    raise AdapterFailure("model_missing", "Configure um modelo para este comando.")
                argv = [connection["model"] if arg == "{model}" else arg for arg in argv]
            stdout, _ = await execute_process(
                argv, prompt, directory, connection["timeout_seconds"]
            )
            return decode_answer(stdout)
        if kind != "codex":
            raise AdapterFailure("unsupported", "Conexão não suportada.")
        executable = (connection["command"] or ["codex"])[0]
        answer_path = directory / "answer.txt"
        argv = [
            executable,
            "exec",
            "--ignore-user-config",
            "--ephemeral",
            "--skip-git-repo-check",
            "--sandbox",
            "read-only",
            "--json",
            "-C",
            str(directory),
            "-o",
            str(answer_path),
        ]
        if connection["model"]:
            argv.extend(["--model", connection["model"]])
        argv.append("-")
        stdout, _ = await execute_process(argv, prompt, directory, connection["timeout_seconds"])
        try:
            events = [json.loads(line) for line in stdout.splitlines() if line.strip()]
        except json.JSONDecodeError as exc:
            raise AdapterFailure("protocol", "O Codex retornou eventos inválidos.") from exc
        if not all(isinstance(event, dict) for event in events):
            raise AdapterFailure("protocol", "O Codex retornou eventos inválidos.")
        for event in events:
            if not isinstance(event.get("type"), str):
                raise AdapterFailure("protocol", "O Codex retornou eventos inválidos.")
            if event["type"] in {"turn.failed", "error"}:
                raise AdapterFailure("incomplete", "O Codex registrou uma falha na execução.")
            item = event.get("item")
            if event.get("type", "").startswith("item.") and (
                not isinstance(item, dict) or item.get("type") not in {"agent_message", "reasoning"}
            ):
                raise AdapterFailure(
                    "tools_used", "A execução usou ferramentas fora deste protocolo."
                )
        if not any(event.get("type") == "turn.completed" for event in events):
            raise AdapterFailure("incomplete", "O Codex não registrou uma conclusão válida.")
        if not answer_path.is_file():
            raise AdapterFailure("missing_answer", "O Codex não produziu a resposta final.")
        return decode_answer(answer_path.read_bytes())

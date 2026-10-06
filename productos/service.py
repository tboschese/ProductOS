"""Shared terminal and CLI use cases; capture inputs before calling any AI."""

from __future__ import annotations

import asyncio

from productos.adapters import AdapterFailure, invoke
from productos.prompting import prepare_prompt
from productos.workspace import Workspace, read_text


def prepare(
    workspace: Workspace, decision_id: str, manual: bool = False, structured: bool = False
) -> dict:
    decision = workspace.decision(decision_id)
    connection = workspace.connection()
    if manual:
        connection = {**connection, "kind": "manual", "command": []}
    output_format = "decision_record" if structured else "markdown"
    prompt, instructions = prepare_prompt(workspace.contracts.repository, decision, output_format)
    return workspace.prepare_analysis(decision, connection, prompt, instructions, output_format)


async def analyze(workspace: Workspace, decision_id: str, structured: bool = False) -> dict:
    connection = workspace.connection()
    value = prepare(workspace, decision_id, structured=structured)
    if value["status"] == "exported":
        return value
    try:
        prompt = read_text(workspace.path("analyses", value["id"], "prompt.txt"))
        response = await invoke(connection, prompt)
        return workspace.finish(value["id"], response)
    except asyncio.CancelledError:
        workspace.fail(value["id"], "cancelled: execução cancelada pelo usuário", cancelled=True)
        raise
    except AdapterFailure as exc:
        workspace.fail(value["id"], exc.code)
        raise
    except Exception:
        workspace.fail(value["id"], "runtime_error")
        raise

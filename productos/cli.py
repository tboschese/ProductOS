"""ProductOS commands, also available without installing the optional terminal UI."""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import shutil
import sys
from pathlib import Path

from productos.contracts import Contracts, RuntimeFailure, find_repository
from productos.service import analyze, prepare
from productos.workspace import Workspace, read_text


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description="ProductOS: decisões e evidências com a sua IA.")
    cli.add_argument("--repository", type=Path, help="Repositório das instruções ProductOS")
    cli.add_argument(
        "--workspace",
        type=Path,
        default=Path.home() / ".productos",
        help="Dados pessoais (padrão: ~/.productos)",
    )
    sub = cli.add_subparsers(dest="action")
    sub.add_parser("tui", help="Abrir o terminal interativo")
    sub.add_parser("doctor", help="Verificar repositório e conexão sem chamar IA")
    sub.add_parser("list", help="Listar decisões")
    new = sub.add_parser("new", help="Criar decisão")
    new.add_argument("--title", required=True)
    new.add_argument("--question", required=True)
    new.add_argument("--locale", choices=["pt-BR", "en", "es"], default="pt-BR")
    new.add_argument("--context-file", type=Path)
    for name in ("show", "analyze", "export", "context", "evidence", "decide"):
        command = sub.add_parser(name)
        command.add_argument("decision_id")
        if name in {"analyze", "export"}:
            command.add_argument(
                "--structured", action="store_true", help="Solicitar JSON validável"
            )
        if name == "context":
            command.add_argument("--file", type=Path, required=True)
        if name == "decide":
            command.add_argument("--decision", required=True)
            command.add_argument("--next-action", default="")
        if name == "evidence":
            command.add_argument("--statement", required=True)
            command.add_argument("--source", required=True)
            command.add_argument("--locator", required=True)
            command.add_argument(
                "--status",
                default="observation",
                choices=[
                    "fact",
                    "observation",
                    "interpretation",
                    "assumption",
                    "hypothesis",
                    "opinion",
                    "unknown",
                ],
            )
            command.add_argument("--limitations", default="")
            command.add_argument("--file", type=Path, help="Anexo de texto UTF-8")
    connect = sub.add_parser("connect", help="Configurar conexão; não executa IA")
    group = connect.add_mutually_exclusive_group(required=True)
    group.add_argument("--kind", choices=["manual", "codex"])
    group.add_argument(
        "--file", type=Path, help="Arquivo ai-connection JSON, inclusive comando próprio"
    )
    connect.add_argument("--model")
    connect.add_argument("--executable", help="Caminho do Codex CLI")
    connect.add_argument("--timeout", type=int, default=240)
    imported = sub.add_parser("import", help="Importar resposta para um pacote manual exportado")
    imported.add_argument("analysis_id")
    imported.add_argument("--file", type=Path, required=True)
    return cli


def dispatch(args, workspace: Workspace) -> int:
    action = args.action or "tui"
    if action == "tui":
        if importlib.util.find_spec("textual") is None:
            raise RuntimeFailure("Instale o terminal: python -m pip install -e '.[terminal]'")
        from productos.tui import ProductOSApp

        ProductOSApp(workspace).run()
    elif action == "doctor":
        connection = workspace.connection()
        executable = (connection["command"] or ["codex"])[0]
        available = connection["kind"] == "manual" or shutil.which(executable) is not None
        print(f"Repositório: {workspace.contracts.repository}\nWorkspace: {workspace.root}")
        print(f"Conexão: {connection['kind']}; executável disponível: {available}")
        print("Autenticação e qualidade do modelo não verificadas; nenhuma IA foi chamada.")
        return 0 if available else 1
    elif action == "new":
        context = read_text(args.context_file) if args.context_file else ""
        value = workspace.create(args.title, args.question, args.locale, context)
        print(value["id"])
    elif action == "list":
        for value in workspace.decisions():
            print(f"{value['id']}  {value['title']}")
    elif action == "connect":
        if args.file:
            value = json.loads(args.file.read_bytes())
        else:
            value = {
                "schema_version": "0.1.0",
                "kind": args.kind,
                "model": args.model,
                "command": [args.executable] if args.kind == "codex" and args.executable else [],
                "timeout_seconds": args.timeout,
            }
        workspace.set_connection(value)
        print(f"Conexão salva: {value['kind']}; nenhuma IA foi chamada.")
    elif action == "import":
        value = workspace.analysis(args.analysis_id)
        if value["status"] != "exported":
            raise RuntimeFailure("Importe a resposta de uma análise manual exportada.")
        value = workspace.finish(args.analysis_id, read_text(args.file))
        print(f"Resposta preservada: {value['id']}; estrutura: {value['structured_status']}")
    elif action in {"analyze", "export"}:
        value = (
            prepare(workspace, args.decision_id, manual=True, structured=args.structured)
            if action == "export"
            else asyncio.run(analyze(workspace, args.decision_id, args.structured))
        )
        print(f"Análise: {value['id']}; estado: {value['status']}")
        print(workspace.path("analyses", value["id"], "prompt.txt"))
        if value["status"] == "completed":
            print(read_text(workspace.path("analyses", value["id"], "response.txt")))
            if value["structured_status"] == "invalid":
                print("A resposta foi preservada, mas não atende ao esquema de decisão.")
    else:
        value = workspace.decision(args.decision_id)
        if action == "show":
            print(json.dumps(value, ensure_ascii=False, indent=2))
            for item in workspace.analyses(args.decision_id):
                print(f"{item['id']}  {item['status']}  {item['connection']['kind']}")
        elif action == "context":
            workspace.update({**value, "context": read_text(args.file)})
        elif action == "evidence":
            workspace.add_evidence(
                value,
                args.statement,
                args.source,
                args.locator,
                args.status,
                args.limitations,
                read_text(args.file) if args.file else "",
            )
        elif action == "decide":
            workspace.update(
                {**value, "chosen_decision": args.decision, "next_action": args.next_action}
            )
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        contracts = Contracts(find_repository(args.repository))
        with Workspace(args.workspace, contracts) as workspace:
            return dispatch(args, workspace)
    except (RuntimeFailure, OSError, ValueError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Execução interrompida.", file=sys.stderr)
        return 130

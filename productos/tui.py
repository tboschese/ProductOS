"""ProductOS Command Room: local decisions and explicit AI actions."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from rich.text import Text
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Markdown,
    Select,
    Static,
    TabbedContent,
    TabPane,
    TextArea,
)

from productos.contracts import RuntimeFailure
from productos.service import analyze, prepare
from productos.workspace import Workspace, read_text

STATUS_LABELS = {
    "exported": "Aguardando resposta manual",
    "running": "Em execução",
    "completed": "Resposta preservada — ainda não revisada",
    "failed": "Execução falhou",
    "cancelled": "Execução cancelada",
}
EPISTEMIC_LABELS = {
    "observation": "Observação",
    "fact": "Fato declarado pelo usuário",
    "interpretation": "Interpretação",
    "assumption": "Suposição",
    "hypothesis": "Hipótese",
    "opinion": "Opinião",
    "unknown": "Desconhecido",
}


class FormScreen(ModalScreen):
    BINDINGS = [("escape", "close", "Voltar")]

    def action_close(self) -> None:
        self.dismiss(None)

    def error(self, message: str) -> None:
        self.query_one(".form-error", Static).update(Text(message))

    @on(Button.Pressed, ".dismiss")
    def close_form(self) -> None:
        self.dismiss(None)


class NewDecision(FormScreen):
    def compose(self) -> ComposeResult:
        with VerticalScroll(classes="dialog"):
            yield Label("Nova decisão", classes="dialog-title")
            yield Label("Título")
            yield Input(placeholder="Ex.: Queda na retenção", id="new-title")
            yield Label("Qual decisão precisamos tomar?")
            yield Input(placeholder="Mudar o onboarding ou investigar primeiro?", id="new-question")
            yield Label("Idioma da análise")
            yield Select(
                [("Português", "pt-BR"), ("English", "en"), ("Español", "es")],
                value="pt-BR",
                allow_blank=False,
                id="new-locale",
            )
            yield Static("", classes="form-error")
            with Horizontal(classes="actions"):
                yield Button("Criar decisão", variant="primary", id="create-decision")
                yield Button("Voltar", classes="dismiss")

    @on(Button.Pressed, "#create-decision")
    def create(self) -> None:
        title = self.query_one("#new-title", Input).value.strip()
        question = self.query_one("#new-question", Input).value.strip()
        if not title or not question:
            self.error("Preencha título e pergunta.")
            return
        self.dismiss((title, question, self.query_one("#new-locale", Select).value))


class ConnectionScreen(FormScreen):
    def __init__(self, workspace: Workspace):
        super().__init__()
        self.workspace = workspace
        self.connection = workspace.connection()

    def compose(self) -> ComposeResult:
        value = self.connection
        with VerticalScroll(classes="dialog connection-dialog"):
            yield Label("Sua conexão de IA", classes="dialog-title")
            yield Select(
                [
                    ("Copiar e colar", "manual"),
                    ("Codex instalado", "codex"),
                    ("Comando personalizado", "command"),
                ],
                value=value["kind"],
                allow_blank=False,
                id="connection-kind",
            )
            yield Label("Modelo solicitado (opcional)")
            yield Input(value=value["model"] or "", id="connection-model")
            with Vertical(id="codex-settings"):
                yield Label("Executável do Codex (vazio: codex no PATH)")
                yield Input(
                    value=(value["command"] or [""])[0] if value["kind"] == "codex" else "",
                    id="connection-executable",
                )
            with Vertical(id="command-settings"):
                yield Label("Comando como lista JSON de argumentos")
                yield TextArea(
                    json.dumps(
                        value["command"] if value["kind"] == "command" else [], ensure_ascii=False
                    ),
                    id="connection-command",
                )
                yield Static(
                    "Recebe o contexto em stdin e devolve somente a resposta em stdout. "
                    "Use {model} como argumento para substituir o modelo. "
                    "Autentique pelo próprio assistente; não coloque chaves nesta lista.",
                    classes="hint",
                )
            yield Label("Tempo limite em segundos")
            yield Input(
                value=str(value["timeout_seconds"]), type="integer", id="connection-timeout"
            )
            yield Static("Salvar a conexão não chama a IA.", classes="hint")
            yield Static("", classes="form-error")
            with Horizontal(classes="actions"):
                yield Button("Salvar conexão", variant="primary", id="save-connection")
                yield Button("Voltar", classes="dismiss")

    def on_mount(self) -> None:
        self.update_fields(self.connection["kind"])

    @on(Select.Changed, "#connection-kind")
    def kind_changed(self, event: Select.Changed) -> None:
        self.update_fields(event.value)

    def update_fields(self, kind: str) -> None:
        self.query_one("#codex-settings").display = kind == "codex"
        self.query_one("#command-settings").display = kind == "command"

    @on(Button.Pressed, "#save-connection")
    def save_connection(self) -> None:
        try:
            kind = self.query_one("#connection-kind", Select).value
            command = []
            if kind == "codex":
                executable = self.query_one("#connection-executable", Input).value.strip()
                command = [executable] if executable else []
            elif kind == "command":
                command = json.loads(self.query_one("#connection-command", TextArea).text)
            value = {
                "schema_version": "0.1.0",
                "kind": kind,
                "model": self.query_one("#connection-model", Input).value.strip() or None,
                "command": command,
                "timeout_seconds": int(self.query_one("#connection-timeout", Input).value),
            }
            self.workspace.contracts.validate("ai-connection", value)
            self.dismiss(value)
        except (ValueError, RuntimeFailure) as exc:
            self.error(str(exc))


class EvidenceScreen(FormScreen):
    def __init__(self, evidence: dict | None = None):
        super().__init__()
        self.evidence = evidence or {}

    def compose(self) -> ComposeResult:
        value = self.evidence
        with VerticalScroll(classes="dialog evidence-dialog"):
            yield Label(
                "Editar evidência" if value else "Acrescentar evidência", classes="dialog-title"
            )
            yield Label("Afirmação ou observação")
            yield Input(value=value.get("statement", ""), id="evidence-statement")
            yield Select(
                [(label, key) for key, label in EPISTEMIC_LABELS.items()],
                allow_blank=False,
                value=value.get("epistemic_status", "observation"),
                id="evidence-status",
            )
            yield Label("Fonte (nome, link ou relato)")
            yield Input(value=value.get("source", ""), id="evidence-source")
            yield Label("Localizador (página, seção, período ou origem do relato)")
            yield Input(value=value.get("locator", ""), id="evidence-locator")
            yield Label("Limitações")
            yield TextArea(value.get("limitations", ""), id="evidence-limitations")
            yield Label("Trecho ou dados de apoio (opcional)")
            yield TextArea(value.get("content", ""), id="evidence-content")
            with Horizontal(classes="actions"):
                yield Input(placeholder="Arquivo de texto UTF-8 (opcional)", id="evidence-file")
                yield Button("Ler arquivo", id="read-evidence-file")
            yield Static("Classificar uma afirmação não verifica sua veracidade.", classes="hint")
            yield Static("", classes="form-error")
            with Horizontal(classes="actions"):
                yield Button("Salvar evidência", variant="primary", id="save-evidence")
                yield Button("Voltar", classes="dismiss")

    @on(Button.Pressed, "#read-evidence-file")
    def attach_file(self) -> None:
        try:
            path = Path(self.query_one("#evidence-file", Input).value).expanduser()
            self.query_one("#evidence-content", TextArea).load_text(read_text(path))
            if not self.query_one("#evidence-source", Input).value:
                self.query_one("#evidence-source", Input).value = str(path)
        except (OSError, RuntimeFailure) as exc:
            self.error(str(exc))

    @on(Button.Pressed, "#save-evidence")
    def save_evidence(self) -> None:
        value = {
            "statement": self.query_one("#evidence-statement", Input).value.strip(),
            "epistemic_status": self.query_one("#evidence-status", Select).value,
            "source": self.query_one("#evidence-source", Input).value.strip(),
            "locator": self.query_one("#evidence-locator", Input).value.strip(),
            "limitations": self.query_one("#evidence-limitations", TextArea).text,
            "content": self.query_one("#evidence-content", TextArea).text,
        }
        if not all(value[key] for key in ("statement", "source", "locator")):
            self.error("Preencha a afirmação, a fonte e o localizador.")
            return
        self.dismiss(value)


class ImportScreen(FormScreen):
    def compose(self) -> ComposeResult:
        with VerticalScroll(classes="dialog import-dialog"):
            yield Label("Importar resposta da sua IA", classes="dialog-title")
            yield Label("Cole a resposta ou informe um arquivo UTF-8")
            yield TextArea(id="import-answer")
            yield Input(placeholder="Caminho do arquivo (opcional)", id="import-file")
            yield Static("", classes="form-error")
            with Horizontal(classes="actions"):
                yield Button("Preservar resposta", variant="primary", id="save-import")
                yield Button("Voltar", classes="dismiss")

    @on(Button.Pressed, "#save-import")
    def save_import(self) -> None:
        try:
            response = self.query_one("#import-answer", TextArea).text
            file = self.query_one("#import-file", Input).value.strip()
            if file and response.strip():
                self.error("Escolha texto colado ou arquivo, para evitar ambiguidade.")
                return
            if file:
                response = read_text(Path(file).expanduser())
            if not response.strip():
                self.error("Acrescente uma resposta.")
                return
            self.dismiss(response)
        except (OSError, RuntimeFailure) as exc:
            self.error(str(exc))


class ExportScreen(FormScreen):
    def __init__(self, prompt: str, path: Path):
        super().__init__()
        self.prompt, self.path = prompt, path

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog export-dialog"):
            yield Label("Contexto para a sua IA", classes="dialog-title")
            yield Static(Text(f"Pacote salvo em {self.path}"), classes="hint")
            yield TextArea(self.prompt, read_only=True, id="export-prompt")
            yield Static(
                "Envie este contexto ao seu assistente e depois importe a resposta.", classes="hint"
            )
            with Horizontal(classes="actions"):
                yield Button("Copiar contexto", variant="primary", id="copy-prompt")
                yield Button("Voltar", classes="dismiss")

    @on(Button.Pressed, "#copy-prompt")
    def copy_prompt(self) -> None:
        self.app.copy_to_clipboard(self.prompt)
        self.notify(
            "Cópia enviada ao terminal. O suporte à área de transferência varia por terminal."
        )


class DecisionItem(ListItem):
    def __init__(self, decision: dict):
        super().__init__(Label(Text(decision["title"])))
        self.decision_id = decision["id"]


class ProductOSApp(App):
    CSS_PATH = "terminal.tcss"
    TITLE = "ProductOS"
    SUB_TITLE = "Command Room"
    BINDINGS = [
        Binding("f2,ctrl+n", "new_decision", "Nova", key_display="F2"),
        Binding("f6,ctrl+s", "save", "Salvar", key_display="F6"),
        Binding("f5,ctrl+r", "analyze", "Analisar", key_display="F5"),
        Binding("f4", "connection", "IA", key_display="F4"),
        Binding("f8", "cancel_analysis", "Cancelar", key_display="F8"),
        Binding("f10,ctrl+q", "quit", "Sair", key_display="F10"),
    ]

    def __init__(self, workspace: Workspace):
        super().__init__()
        self.workspace = workspace
        self.current = None
        self.selected_analysis = None
        self.selected_evidence = None
        self.inference_worker = None
        self.theme = "textual-dark"

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="shell"):
            with Vertical(id="sidebar"):
                yield Static("DECISÕES", classes="eyebrow")
                yield Button("＋ Nova decisão", variant="primary", id="new-decision")
                yield ListView(id="decisions")
                yield Button("Conexão de IA", id="connection")
                yield Static("", id="connection-status", classes="hint")
            with Vertical(id="main"):
                yield Static("Uma boa decisão começa com uma boa pergunta.", id="decision-heading")
                yield Static(
                    "Crie uma decisão para começar. Seus dados ficam no workspace local.",
                    id="welcome",
                    classes="hint",
                )
                with TabbedContent(id="tabs"):
                    with TabPane("Contexto", id="context-tab"):
                        yield Label("Qual decisão precisamos tomar?")
                        yield Input(id="question")
                        yield Label("Contexto, restrições e o que ainda não sabemos")
                        yield TextArea(id="context")
                        yield Button("Salvar contexto", variant="primary", id="save-context")
                    with TabPane("Evidências", id="evidence-tab"):
                        yield DataTable(id="evidence-table", cursor_type="row")
                        yield Static(
                            "Selecione uma evidência para consultar sua origem.",
                            id="evidence-detail",
                            markup=False,
                        )
                        with Horizontal(classes="actions"):
                            yield Button(
                                "Acrescentar evidência", variant="primary", id="add-evidence"
                            )
                            yield Button("Editar selecionada", id="edit-evidence")
                    with TabPane("Análises", id="analysis-tab"):
                        with Horizontal(classes="actions", id="analysis-actions"):
                            yield Button("Analisar com IA", variant="primary", id="analyze")
                            yield Button("Exportar contexto", id="export")
                            yield Button("Importar resposta", id="import")
                            yield Button(
                                "Cancelar IA", variant="error", id="cancel-ai", disabled=True
                            )
                        yield Select([], prompt="Histórico de análises", id="analysis-history")
                        yield Static("Nenhuma análise ainda.", id="analysis-status", markup=False)
                        with VerticalScroll(id="answer-scroll"):
                            yield Markdown("", id="answer")
                    with TabPane("Decisão", id="choice-tab"):
                        yield Label("O que você decidiu e por quê?")
                        yield TextArea(id="chosen-decision")
                        yield Label("Próximo passo ou condição para revisar")
                        yield Input(id="next-action")
                        yield Static(
                            "Este registro é pessoal; não aprova conhecimento canônico.",
                            classes="hint",
                        )
                        yield Button("Registrar decisão", variant="primary", id="save-choice")
                yield Static("", id="status", markup=False)
        yield Footer()

    async def on_mount(self) -> None:
        table = self.query_one("#evidence-table", DataTable)
        table.add_columns("Tipo", "Afirmação", "Fonte")
        self.query_one("#tabs").display = False
        self.refresh_connection()
        await self.refresh_decisions()

    def status(self, text: str) -> None:
        self.query_one("#status", Static).update(Text(text))

    def refresh_connection(self) -> None:
        value = self.workspace.connection()
        labels = {
            "manual": "Copiar e colar",
            "codex": "Codex instalado",
            "command": "Comando personalizado",
        }
        self.query_one("#connection-status", Static).update(
            Text(f"{labels[value['kind']]}\nModelo: {value['model'] or 'não declarado'}")
        )

    async def refresh_decisions(self) -> None:
        items = self.query_one("#decisions", ListView)
        await items.clear()
        for value in self.workspace.decisions():
            await items.append(DecisionItem(value))

    async def load_decision(self, decision_id: str) -> None:
        self.current = self.workspace.decision(decision_id)
        self.selected_evidence = None
        self.query_one("#welcome").display = False
        self.query_one("#tabs").display = True
        self.query_one("#decision-heading", Static).update(Text(self.current["title"]))
        self.query_one("#question", Input).value = self.current["question"]
        self.query_one("#context", TextArea).load_text(self.current["context"])
        self.query_one("#chosen-decision", TextArea).load_text(self.current["chosen_decision"])
        self.query_one("#next-action", Input).value = self.current["next_action"]
        self.refresh_evidence()
        await self.refresh_analyses()

    def refresh_evidence(self) -> None:
        table = self.query_one("#evidence-table", DataTable)
        table.clear()
        for item in self.current["evidence"]:
            table.add_row(
                Text(EPISTEMIC_LABELS[item["epistemic_status"]]),
                Text(item["statement"]),
                Text(item["source"]),
                key=item["id"],
            )
        self.query_one("#evidence-detail", Static).update(
            "Selecione uma evidência para ver a origem."
        )

    async def refresh_analyses(self, selected: str | None = None) -> None:
        values = self.workspace.analyses(self.current["id"])
        dropdown = self.query_one("#analysis-history", Select)
        dropdown.set_options(
            [
                (f"{item['started_at'][:19]} · {STATUS_LABELS[item['status']]}", item["id"])
                for item in values
            ]
        )
        dropdown.value = selected or (values[0]["id"] if values else Select.NULL)
        self.selected_analysis = dropdown.value if dropdown.value is not Select.NULL else None
        await self.show_analysis()

    async def show_analysis(self) -> None:
        markdown = self.query_one("#answer", Markdown)
        if not self.selected_analysis:
            self.query_one("#analysis-status", Static).update("Nenhuma análise ainda.")
            await markdown.update("")
            return
        item = self.workspace.analysis(self.selected_analysis)
        connection = item["connection"]
        text = (
            f"{STATUS_LABELS[item['status']]} · {connection['kind']} · "
            f"modelo solicitado: {connection['requested_model'] or 'não declarado'}\n"
            f"Contexto da revisão {item['decision_revision']} · {item['id']}"
        )
        if item["structured_status"] == "invalid":
            text += "\nJSON inválido para o esquema; resposta original preservada."
        if self.current and item["decision_revision"] != self.current["revision"]:
            text += "\nEsta análise usa uma revisão anterior do registro."
        self.query_one("#analysis-status", Static).update(Text(text))
        response = (
            read_text(self.workspace.path("analyses", item["id"], "response.txt"))
            if item["status"] == "completed"
            else ""
        )
        if item["output_format"] == "decision_record" and response:
            response = "```json\n" + response + "\n```"
        await markdown.update(response)

    @on(ListView.Selected, "#decisions")
    async def select_decision(self, event: ListView.Selected) -> None:
        if self.busy():
            self.status("Aguarde a análise ou cancele antes de trocar de decisão.")
            return
        try:
            if self.current:
                self.save_current()
            await self.load_decision(event.item.decision_id)
        except (RuntimeFailure, OSError, ValueError) as exc:
            self.status(str(exc))

    @on(DataTable.RowSelected, "#evidence-table")
    def select_evidence(self, event: DataTable.RowSelected) -> None:
        self.selected_evidence = event.row_key.value
        item = next(v for v in self.current["evidence"] if v["id"] == self.selected_evidence)
        self.query_one("#evidence-detail", Static).update(
            Text(
                f"{item['statement']}\nFonte: {item['source']}\nLocalizador: {item['locator']}\n"
                f"Limitações: {item['limitations'] or 'não declaradas'}\n{item['content']}"
            )
        )

    @on(Select.Changed, "#analysis-history")
    async def select_analysis(self, event: Select.Changed) -> None:
        self.selected_analysis = event.value if event.value is not Select.NULL else None
        try:
            await self.show_analysis()
        except (RuntimeFailure, OSError, ValueError) as exc:
            self.status(str(exc))

    def busy(self) -> bool:
        return self.inference_worker is not None and not self.inference_worker.is_finished

    def save_current(self) -> None:
        if not self.current:
            return
        value = {
            **self.current,
            "question": self.query_one("#question", Input).value.strip(),
            "context": self.query_one("#context", TextArea).text,
            "chosen_decision": self.query_one("#chosen-decision", TextArea).text,
            "next_action": self.query_one("#next-action", Input).value,
        }
        if value != self.current:
            self.current = self.workspace.update(value)

    @on(Button.Pressed, "#save-context")
    @on(Button.Pressed, "#save-choice")
    def action_save(self) -> None:
        try:
            self.save_current()
            self.status("Registro salvo no workspace local.")
        except (RuntimeFailure, OSError) as exc:
            self.status(str(exc))

    @on(Button.Pressed, "#new-decision")
    def action_new_decision(self) -> None:
        if self.busy():
            self.status("Aguarde a análise ou cancele antes de criar outra decisão.")
            return
        self.push_screen(NewDecision(), self.created_decision)

    async def created_decision(self, result) -> None:
        if result is None:
            return
        try:
            self.save_current()
            value = self.workspace.create(*result)
            await self.refresh_decisions()
            await self.load_decision(value["id"])
            self.status("Decisão criada. Acrescente contexto e evidências.")
        except (RuntimeFailure, OSError) as exc:
            self.status(str(exc))

    @on(Button.Pressed, "#connection")
    def action_connection(self) -> None:
        if self.busy():
            self.status("Aguarde ou cancele antes de mudar a conexão.")
            return
        self.push_screen(ConnectionScreen(self.workspace), self.changed_connection)

    def changed_connection(self, result) -> None:
        if result is not None:
            try:
                self.workspace.set_connection(result)
                self.refresh_connection()
                self.status("Conexão salva; nenhuma análise foi executada.")
            except (RuntimeFailure, OSError) as exc:
                self.status(str(exc))

    @on(Button.Pressed, "#add-evidence")
    @on(Button.Pressed, "#edit-evidence")
    def edit_evidence(self, event: Button.Pressed) -> None:
        if not self.current or self.busy():
            return
        item = None
        if event.button.id == "edit-evidence":
            item = next(
                (v for v in self.current["evidence"] if v["id"] == self.selected_evidence), None
            )
            if item is None:
                self.status("Selecione uma evidência na tabela primeiro.")
                return
        self.push_screen(EvidenceScreen(item), lambda result: self.saved_evidence(result, item))

    def saved_evidence(self, result, existing: dict | None) -> None:
        if result is None:
            return
        try:
            self.save_current()
            if existing is None:
                self.current = self.workspace.add_evidence(
                    self.current,
                    result["statement"],
                    result["source"],
                    result["locator"],
                    result["epistemic_status"],
                    result["limitations"],
                    result["content"],
                )
            else:
                evidence = [
                    {**existing, **result} if v["id"] == existing["id"] else v
                    for v in self.current["evidence"]
                ]
                self.current = self.workspace.update({**self.current, "evidence": evidence})
            self.refresh_evidence()
            self.status("Evidência salva com fonte e localizador; conteúdo não verificado.")
        except (RuntimeFailure, OSError) as exc:
            self.status(str(exc))

    @on(Button.Pressed, "#export")
    async def export_context(self) -> None:
        if not self.current or self.busy():
            return
        try:
            self.save_current()
            value = prepare(self.workspace, self.current["id"], manual=True)
            await self.refresh_analyses(value["id"])
            self.show_export(value["id"])
        except (RuntimeFailure, OSError) as exc:
            self.status(str(exc))

    def show_export(self, analysis_id: str) -> None:
        path = self.workspace.path("analyses", analysis_id, "prompt.txt")
        self.push_screen(ExportScreen(read_text(path), path))

    @on(Button.Pressed, "#import")
    def import_answer(self) -> None:
        if not self.selected_analysis:
            self.status("Exporte um contexto antes de importar uma resposta.")
            return
        value = self.workspace.analysis(self.selected_analysis)
        if value["status"] != "exported":
            self.status("Selecione uma análise aguardando resposta manual.")
            return
        analysis_id = self.selected_analysis
        self.push_screen(ImportScreen(), lambda result: self.imported_answer(analysis_id, result))

    async def imported_answer(self, analysis_id: str, result) -> None:
        if result is None:
            return
        try:
            self.workspace.finish(analysis_id, result)
            await self.refresh_analyses(analysis_id)
            self.status("Resposta preservada. Revise as evidências antes de registrar sua decisão.")
        except (RuntimeFailure, OSError) as exc:
            self.status(str(exc))

    @on(Button.Pressed, "#analyze")
    def action_analyze(self) -> None:
        if not self.current or self.busy():
            return
        try:
            self.save_current()
            tabs = self.query_one("#tabs", TabbedContent)
            tabs.get_tab("analysis-tab").focus()
            tabs.active = "analysis-tab"
            self.inference_worker = self.run_analysis(self.current["id"])
        except (RuntimeFailure, OSError) as exc:
            self.status(str(exc))

    @work(exclusive=True, group="inference", exit_on_error=False)
    async def run_analysis(self, decision_id: str) -> None:
        self.query_one("#cancel-ai", Button).disabled = False
        self.query_one("#analyze", Button).disabled = True
        self.status("Preparando contexto e aguardando a IA…")
        try:
            value = await analyze(self.workspace, decision_id)
            await self.refresh_analyses(value["id"])
            if value["status"] == "exported":
                self.status("Conexão manual: envie o contexto e depois importe a resposta.")
                self.show_export(value["id"])
            else:
                self.status("Resposta preservada; revise antes de registrar uma decisão.")
        except asyncio.CancelledError:
            self.status("Execução cancelada. O contexto foi preservado.")
            await self.refresh_analyses()
            raise
        except (RuntimeFailure, OSError, ValueError) as exc:
            self.status(str(exc))
            await self.refresh_analyses()
        finally:
            self.query_one("#cancel-ai", Button).disabled = True
            self.query_one("#analyze", Button).disabled = False

    @on(Button.Pressed, "#cancel-ai")
    def action_cancel_analysis(self) -> None:
        if self.busy():
            self.inference_worker.cancel()

    async def action_quit(self) -> None:
        try:
            self.save_current()
        except (RuntimeFailure, OSError) as exc:
            self.status(str(exc))
            return
        if self.busy():
            self.inference_worker.cancel()
            self.status("Cancelando a execução. Pressione sair novamente após o cancelamento.")
            return
        self.exit()

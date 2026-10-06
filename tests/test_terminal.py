"""Headless terminal workflow and cancellation, with no live model calls."""

import asyncio

import pytest
from textual.widgets import Input, TabbedContent, TextArea

from productos.contracts import Contracts
from productos.tui import ProductOSApp
from productos.workspace import Workspace
from scripts.validate_repository import ROOT


@pytest.mark.parametrize("size", [(120, 40), (80, 24)])
def test_terminal_create_evidence_manual_answer_and_decision(tmp_path, size):
    async def scenario():
        workspace = Workspace(tmp_path, Contracts(ROOT))
        app = ProductOSApp(workspace)
        async with app.run_test(size=size) as pilot:
            await pilot.click("#new-decision")
            app.screen.query_one("#new-title", Input).value = "Retenção"
            app.screen.query_one("#new-question", Input).value = "Investigar antes de mudar?"
            app.screen.query_one("#create-decision").scroll_visible(animate=False)
            await pilot.pause()
            await pilot.click("#create-decision")
            await pilot.pause()
            assert app.current is not None
            app.query_one("#context", TextArea).load_text("Contexto sem dados verificados.")
            await pilot.click("#save-context")
            await pilot.click(app.query_one("#tabs", TabbedContent).get_tab("evidence-tab"))
            await pilot.pause()
            await pilot.click("#add-evidence")
            app.screen.query_one("#evidence-statement", Input).value = "Retenção caiu"
            app.screen.query_one("#evidence-source", Input).value = "Relato do usuário"
            app.screen.query_one("#evidence-locator", Input).value = "Reunião de produto"
            app.screen.query_one("#save-evidence").scroll_visible(animate=False)
            await pilot.pause()
            await pilot.click("#save-evidence")
            await pilot.pause()
            assert len(app.current["evidence"]) == 1
            await pilot.click(app.query_one("#tabs", TabbedContent).get_tab("analysis-tab"))
            await pilot.pause()
            await pilot.click("#export")
            await pilot.pause()
            assert "Contexto sem dados" in app.screen.query_one("#export-prompt", TextArea).text
            app.screen.action_close()
            await pilot.pause()
            await pilot.click("#import")
            app.screen.query_one("#import-answer", TextArea).load_text(
                "# Orientação\nInvestigar primeiro."
            )
            app.screen.query_one("#save-import").scroll_visible(animate=False)
            await pilot.pause()
            await pilot.click("#save-import")
            await pilot.pause()
            item = workspace.analyses(app.current["id"])[0]
            assert item["status"] == "completed"
            assert app.current["chosen_decision"] == ""
            await pilot.click(app.query_one("#tabs", TabbedContent).get_tab("choice-tab"))
            await pilot.pause()
            app.query_one("#chosen-decision", TextArea).load_text("Investigar a medição primeiro.")
            await pilot.pause()
            app.query_one("#save-choice").scroll_visible(animate=False)
            await pilot.pause()
            assert await pilot.click("#save-choice")
            assert (
                workspace.decision(app.current["id"])["chosen_decision"]
                == "Investigar a medição primeiro."
            )

    asyncio.run(scenario())


def test_terminal_cancellation_remains_responsive(tmp_path, monkeypatch):
    from productos import service

    async def slow(*_):
        await asyncio.sleep(30)
        return "not reached"

    monkeypatch.setattr(service, "invoke", slow)

    async def scenario():
        workspace = Workspace(tmp_path, Contracts(ROOT))
        workspace.set_connection({**workspace.connection(), "kind": "codex"})
        value = workspace.create("Teste", "Investigar?")
        app = ProductOSApp(workspace)
        async with app.run_test(size=(100, 35)) as pilot:
            await app.load_decision(value["id"])
            app.action_analyze()
            await pilot.pause()
            assert app.busy()
            await pilot.click("#cancel-ai")
            await pilot.pause()
            assert not app.busy()
            assert workspace.analyses(value["id"])[0]["status"] == "cancelled"

    asyncio.run(scenario())

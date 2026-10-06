"""Real subprocess transport checks using explicitly fake local assistants."""

import asyncio
import sys

import pytest

from productos import adapters
from productos.adapters import AdapterFailure, invoke


def connection(kind="command", command=None, model=None, timeout=10):
    return {
        "schema_version": "0.1.0",
        "kind": kind,
        "model": model,
        "command": command or [],
        "timeout_seconds": timeout,
    }


def assistant(tmp_path, body):
    path = tmp_path / "fake assistant.py"
    path.write_text(body)
    return [sys.executable, str(path)]


def test_generic_stdin_stdout_preserves_answer_without_shell(tmp_path):
    command = assistant(tmp_path, "import sys; sys.stdout.buffer.write(sys.stdin.buffer.read())")
    prompt = "  Texto\r\n$(touch nope) `echo nope` ; model='x'\r\n"
    assert asyncio.run(invoke(connection(command=command), prompt)) == prompt
    assert not (tmp_path / "nope").exists()


def test_generic_model_placeholder_is_one_argument(tmp_path):
    command = assistant(tmp_path, "import sys; print(sys.argv[1]); sys.stdin.read()")
    model = "model ; $(touch nope)"
    assert (
        asyncio.run(invoke(connection(command=[*command, "{model}"], model=model), "input"))
        == model + "\n"
    )
    with pytest.raises(AdapterFailure, match="modelo"):
        asyncio.run(invoke(connection(command=[*command, "{model}"]), "input"))


def test_adapter_executes_in_an_empty_temporary_directory(tmp_path):
    command = assistant(tmp_path, "import os,sys; sys.stdin.read(); print(os.listdir('.'))")
    assert asyncio.run(invoke(connection(command=command), "input")) == "[]\n"


def test_auth_failure_does_not_expose_stderr(tmp_path):
    command = assistant(tmp_path, "import sys; print('SECRET',file=sys.stderr);sys.exit(17)")
    with pytest.raises(AdapterFailure) as error:
        asyncio.run(invoke(connection(command=command), "input"))
    assert error.value.code == "exit_17"
    assert "SECRET" not in str(error.value)


def test_timeout_and_cancellation_kill_and_drain_process(tmp_path):
    command = assistant(
        tmp_path, "import time,sys; print('x'*100000);sys.stdout.flush();time.sleep(30)"
    )
    with pytest.raises(AdapterFailure) as error:
        asyncio.run(invoke(connection(command=command, timeout=1), "input"))
    assert error.value.code == "timeout"

    async def cancel():
        task = asyncio.create_task(invoke(connection(command=command), "input"))
        await asyncio.sleep(0.05)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await asyncio.wait_for(task, 3)

    asyncio.run(cancel())


def test_large_output_fails_without_deadlock(tmp_path, monkeypatch):
    command = assistant(tmp_path, "import sys,time; print('x'*2000000);time.sleep(30)")
    monkeypatch.setattr(adapters, "MAX_TRANSPORT_BYTES", 1000)
    with pytest.raises(AdapterFailure) as error:
        asyncio.run(asyncio.wait_for(invoke(connection(command=command), "input"), 4))
    assert error.value.code == "output_limit"


@pytest.mark.parametrize(
    "body,code",
    [
        ("import sys;sys.stdout.buffer.write(b'\\xff')", "encoding"),
        ("pass", "empty"),
    ],
)
def test_invalid_answer_fails(tmp_path, body, code):
    with pytest.raises(AdapterFailure) as error:
        asyncio.run(invoke(connection(command=assistant(tmp_path, body)), "input"))
    assert error.value.code == code


@pytest.mark.parametrize(
    "tool,completed,code",
    [
        (None, True, None),
        ("command_execution", True, "tools_used"),
        ("web_search", True, "tools_used"),
        (None, False, "incomplete"),
    ],
)
def test_codex_adapter_protocol_with_fake_installed_cli(tmp_path, tool, completed, code):
    path = tmp_path / "fake-codex"
    events = [{"type": "item.completed", "item": {"type": tool or "agent_message"}}]
    if completed:
        events.append({"type": "turn.completed"})
    body = (
        f"#!{sys.executable}\nimport sys,json\nfrom pathlib import Path\n"
        "sys.stdin.read()\n"
        "Path(sys.argv[sys.argv.index('-o')+1]).write_bytes(b'  answer\\r\\n')\n"
        f"events={events!r}\n"
        "for event in events: print(json.dumps(event))\n"
    )
    path.write_text(body)
    path.chmod(0o700)
    config = connection(kind="codex", command=[str(path)], model="declared-test-model")
    if code:
        with pytest.raises(AdapterFailure) as error:
            asyncio.run(invoke(config, "input"))
        assert error.value.code == code
    else:
        assert asyncio.run(invoke(config, "input")) == "  answer\r\n"


def test_unavailable_assistant_is_recoverable():
    with pytest.raises(AdapterFailure) as error:
        asyncio.run(invoke(connection(command=["/nonexistent/productos-assistant"]), "input"))
    assert error.value.code == "not_available"

"""A `Procfile.dev` line replacing a stack server: its own port is the one checked."""

import socket
import subprocess
from collections.abc import Iterator
from pathlib import Path

import pytest

from ion_repo.dev import background, ports
from ion_repo.shell import KilnError
from ion_repo.stack import Command


def _procfile(label: str, shell_command: str) -> Command:
    return Command(label, "backend", ("sh", "-c", shell_command))


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    return tmp_path


@pytest.fixture
def held_port() -> Iterator[int]:
    with socket.socket() as held:
        held.bind(("127.0.0.1", 0))
        held.listen()
        yield held.getsockname()[1]


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


@pytest.mark.parametrize(
    ("shell_command", "port"),
    [
        ("uv run uvicorn app:app --reload --port 8016", 8016),
        ("uv run uvicorn app:app --port=8017", 8017),
        ("uv run uvicorn app:app --port ${FASTAPI_PORT:-8018}", 8018),
        ("uv run python manage.py runserver 0.0.0.0:8019", 8019),
        ("uv run python manage.py runserver 8020", 8020),
        ("uv run streamlit run app.py --server.port 8021", 8021),
        ("uv run uvicorn app:app --reload", None),
    ],
)
def test_the_port_a_procfile_line_declares(
    shell_command: str, port: int | None, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("FASTAPI_PORT", raising=False)
    assert ports.declared_port(_procfile("fastapi", shell_command)) == port


def test_a_declared_port_reads_its_variable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FASTAPI_PORT", "8099")
    command = _procfile("fastapi", "uvicorn app:app --port ${FASTAPI_PORT:-8000}")
    assert ports.declared_port(command) == 8099


def test_a_stack_command_declares_nothing() -> None:
    command = Command("fastapi", "backend", ("uv", "run", "uvicorn", "app.main:app", "--port", "1"))
    assert ports.declared_port(command) is None


def test_a_procfile_server_is_checked_on_its_own_port(
    repo: Path, held_port: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The stack's port is held by someone else; the Procfile.dev line listens elsewhere.
    monkeypatch.setitem(ports.DEV_PORTS, "fastapi", held_port)
    own = _free_port()
    command = _procfile("fastapi", f"uv run uvicorn app:app --port {own}")

    assert background.choose_ports(repo, [command]).of("fastapi") == own


def test_a_procfile_server_whose_own_port_is_taken_is_refused(repo: Path, held_port: int) -> None:
    command = _procfile("fastapi", f"uv run uvicorn app:app --port {held_port}")

    with pytest.raises(KilnError, match=f"port {held_port} \\(fastapi\\) is taken"):
        background.choose_ports(repo, [command])

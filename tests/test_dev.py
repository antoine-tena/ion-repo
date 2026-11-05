"""`ion repo dev`: the Procfile.dev, the background (`-d`, status, logs, stop) and its arguments."""

import os
import socket
import subprocess
import sys
import time
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest

from ion_repo import cli
from ion_repo.dev import background, ports, run_dev
from ion_repo.dev.menu import select
from ion_repo.dev.processes import (
    dev_processes,
    node_installs,
    package_script_commands,
    procfile_commands,
    runs_beyond_front,
    spawn,
)
from ion_repo.shell import KilnError
from ion_repo.stack import Command


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    """A git repo without stack nor compose: only its Procfile.dev runs, ready at once."""
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "backend").mkdir()
    monkeypatch.setattr(background, "SETTLE_SECONDS", 0.5)
    yield tmp_path
    background.stop(tmp_path)


def test_a_procfile_line_runs_in_its_folder_and_replaces_a_server_of_the_same_name(
    tmp_path: Path,
) -> None:
    (tmp_path / "backend").mkdir()
    (tmp_path / "backend/manage.py").touch()
    (tmp_path / "backend/Procfile.dev").write_text(
        "# Celery reloaded at each change\n"
        "worker: uv run watchfiles 'celery -A core worker'\n"
        "django: uv run python manage.py runserver 8001\n"
        "not a process\n",
        encoding="utf-8",
    )

    assert procfile_commands(tmp_path, "backend")[0] == Command(
        "worker", "backend", ("sh", "-c", "uv run watchfiles 'celery -A core worker'")
    )
    assert [(command.label, command.argv[-1]) for command in dev_processes(tmp_path)] == [
        ("django", "uv run python manage.py runserver 8001"),
        ("worker", "uv run watchfiles 'celery -A core worker'"),
    ]


def test_a_folder_the_stack_does_not_serve_runs_its_package_dev_scripts(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text(
        '{"scripts": {"dev": "vite", "server": "node --watch server/index.ts",'
        ' "build": "vite build", "start": "node dist/server.js"}}',
        encoding="utf-8",
    )
    (tmp_path / "pnpm-lock.yaml").touch()
    (tmp_path / "Procfile.dev").write_text("server: node --watch api.ts\n", encoding="utf-8")

    assert [(command.label, command.argv) for command in dev_processes(tmp_path)] == [
        ("dev", ("pnpm", "run", "dev")),
        ("server", ("sh", "-c", "node --watch api.ts")),
    ]


def test_start_runs_only_without_a_dev_script_and_a_served_folder_keeps_its_server(
    tmp_path: Path,
) -> None:
    (tmp_path / "backend").mkdir()
    (tmp_path / "backend/package.json").write_text(
        '{"scripts": {"start": "node index.js"}}', encoding="utf-8"
    )
    (tmp_path / "frontend").mkdir()
    (tmp_path / "frontend/nuxt.config.ts").touch()
    (tmp_path / "frontend/package.json").write_text(
        '{"scripts": {"dev": "nuxt dev"}}', encoding="utf-8"
    )

    assert [(command.label, command.argv) for command in dev_processes(tmp_path)] == [
        ("nuxt", ("pnpm", "dev")),
        ("backend-start", ("npm", "run", "start")),
    ]


def test_nothing_to_run_says_what_kiln_looks_for(project: Path) -> None:
    with pytest.raises(KilnError, match=r"package\.json.*Procfile\.dev"):
        run_dev(project)


def test_detached_processes_are_read_then_stopped(
    project: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (project / "backend/.env").write_text("GREETING=hello\n", encoding="utf-8")
    (project / "backend/Procfile.dev").write_text(
        'worker: echo "$GREETING from $(basename $PWD)"; sleep 60\n', encoding="utf-8"
    )

    run_dev(project)
    run_dev(project, "logs")
    pid = background.records(project)["worker"]["pid"]
    run_dev(project)
    run_dev(project, "stop")

    output = capsys.readouterr().out
    assert "running" in output
    assert "already running in the background" in output
    assert "hello from backend" in output
    assert "stopped: worker" in output
    assert not _alive_after_stop(pid)
    assert background.running(project) == []


def test_a_process_that_dies_at_start_stops_the_others_and_shows_its_log(project: Path) -> None:
    (project / "backend/Procfile.dev").write_text(
        "worker: sleep 60\ncrash: echo database refused; exit 3\n", encoding="utf-8"
    )

    with pytest.raises(KilnError, match="crash stopped at start:\ndatabase refused"):
        run_dev(project)

    assert background.running(project) == []


@pytest.mark.parametrize(
    "arguments",
    [
        ["dev", "status", "django"],
        ["dev", "-f"],
        ["dev", "stop", "--foreground"],
        ["dev", "logs", "--containers"],
        ["dev", "status", "--only", "django"],
        ["dev", "--containers", "--only", "django"],
    ],
)
def test_options_go_with_their_action(arguments: list[str]) -> None:
    with pytest.raises(KilnError):
        cli._check_dev_arguments(cli.build_parser().parse_args(arguments))


def _alive_after_stop(pid: int) -> bool:
    deadline = time.monotonic() + 5
    while background.is_alive(pid) and time.monotonic() < deadline:
        time.sleep(0.1)
    return background.is_alive(pid)


PROCESSES = [Command(label, "backend", ("true",)) for label in ("django", "nuxt", "worker")]


def replies(*answers: str) -> Callable[[str], str]:
    queue = list(answers)
    return lambda prompt: queue.pop(0)


def labels(commands: list[Command]) -> list[str]:
    return [command.label for command in commands]


def test_a_small_project_runs_everything_without_a_question(tmp_path: Path) -> None:
    assert select(PROCESSES[:2], tmp_path, ask=replies()) == PROCESSES[:2]


def test_a_big_project_asks_and_remembers_the_choice(tmp_path: Path) -> None:
    assert labels(select(PROCESSES, tmp_path, ask=replies(""))) == ["django", "nuxt", "worker"]
    assert labels(select(PROCESSES, tmp_path, ask=replies("2", "9", "3 1"))) == ["django", "worker"]
    # Next time, Enter takes the last choice, and its numbers are the default.
    assert labels(select(PROCESSES, tmp_path, ask=replies(""))) == ["django", "worker"]
    assert labels(select(PROCESSES, tmp_path, ask=replies("3", ""))) == ["django", "worker"]
    assert labels(select(PROCESSES, tmp_path, ask=replies("2"))) == ["django", "nuxt", "worker"]


def test_the_front_alone_is_offered_when_there_is_a_backend(tmp_path: Path) -> None:
    every = [*PROCESSES[::2], Command("nuxt", "frontend", ("true",))]
    assert labels(select(every, tmp_path, ask=replies("2"))) == ["nuxt"]
    # The last choice is then the front: it is not offered twice.
    assert labels(select(every, tmp_path, ask=replies("3", "1 2"))) == ["django", "worker"]


def test_the_front_alone_keeps_its_env_and_leaves_the_env_dev(project: Path) -> None:
    front = project / "frontend"
    front.mkdir()
    (front / ".env").write_text("API=https://api.example.org\n", encoding="utf-8")
    (front / ".env.dev").write_text("API=http://localhost:8000\n", encoding="utf-8")
    nuxt = Command("nuxt", "frontend", ("sh", "-c", 'printf %s "$API"'))
    outputs = []
    for full_stack in (False, True):
        process = spawn(project, nuxt, {}, subprocess.PIPE, full_stack=full_stack)
        outputs.append(process.communicate()[0])
    assert outputs == ["https://api.example.org", "http://localhost:8000"]
    assert not runs_beyond_front([nuxt])


def test_the_choice_survives_the_start_of_the_processes(project: Path) -> None:
    (project / "backend/Procfile.dev").write_text(
        "api: sleep 60\nworker: sleep 60\nscheduler: sleep 60\n", encoding="utf-8"
    )
    run_dev(project, only=["api", "worker"])
    run_dev(project, "stop")

    chosen = select(dev_processes(project), background.state_dir(project), ask=replies(""))
    assert labels(chosen) == ["api", "worker"]


def test_only_picks_without_a_question_and_refuses_an_unknown_name(tmp_path: Path) -> None:
    assert labels(select(PROCESSES, tmp_path, only=["nuxt"], ask=replies())) == ["nuxt"]
    with pytest.raises(KilnError, match="no celery here"):
        select(PROCESSES, tmp_path, only=["celery"])


def test_a_worktree_keeps_the_databases_another_one_still_uses(project: Path) -> None:
    (project / "backend/Procfile.dev").write_text("api: sleep 60\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(project), "add", "."], check=True)
    subprocess.run(["git", "-C", str(project), "commit", "-qm", "init"], check=True)
    other = project.parent / "other-worktree"
    subprocess.run(["git", "-C", str(project), "worktree", "add", "-q", str(other)], check=True)

    run_dev(project)

    assert background.others_running(other)
    assert not background.others_running(project)
    background.stop(project)
    assert not background.others_running(other)


@pytest.mark.parametrize(("family", "host"), ports.LOOPBACKS)
def test_a_server_is_seen_on_either_loopback(family: socket.AddressFamily, host: str) -> None:
    try:
        server = socket.socket(family)
        server.bind((host, 0))
    except OSError:
        pytest.skip(f"no {host} on this machine")
    with server:
        server.listen()
        assert ports.listens(server.getsockname()[1])


def test_a_taken_port_stops_a_server_that_cannot_be_moved_and_names_who_holds_it(
    project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Another process on the server's port would answer its readiness check (#60).
    with socket.socket() as holder:
        holder.bind(("127.0.0.1", 0))
        holder.listen()
        port = holder.getsockname()[1]
        monkeypatch.setitem(ports.DEV_PORTS, "nuxt", port)
        (project / "backend/Procfile.dev").write_text("nuxt: sleep 60\n", encoding="utf-8")

        with pytest.raises(KilnError, match=rf"port {port} \(nuxt\) is taken by "):
            run_dev(project)

    assert background.running(project) == []


def test_a_port_held_by_another_worktree_points_to_its_kiln_dev_stop(
    project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    other = project / ".git/worktrees/feature"
    (other / background.STATE_DIR).mkdir(parents=True)
    (other / "gitdir").write_text("/code/repo-feature/.git\n", encoding="utf-8")
    with socket.socket() as holder:
        holder.bind(("127.0.0.1", 0))
        holder.listen()
        port = holder.getsockname()[1]
        record = f'{{"pid": {os.getpid()}, "port": {port}}}'
        (other / background.STATE_DIR / "nuxt.json").write_text(record, encoding="utf-8")
        monkeypatch.setitem(ports.DEV_PORTS, "nuxt", port)
        (project / "backend/Procfile.dev").write_text("nuxt: sleep 60\n", encoding="utf-8")

        with pytest.raises(
            KilnError, match=r"ion repo dev of /code/repo-feature: `ion repo dev stop`"
        ):
            run_dev(project)


def test_a_fresh_clone_installs_its_node_dependencies_from_the_lock(tmp_path: Path) -> None:
    # Without node_modules/, `npm run dev` stops on `vite: not found` (#59).
    (tmp_path / "package.json").write_text('{"scripts": {"dev": "vite"}}', encoding="utf-8")
    (tmp_path / "package-lock.json").write_text("{}", encoding="utf-8")
    commands = package_script_commands(tmp_path, ".")

    assert [install.argv for install in node_installs(tmp_path, commands)] == [("npm", "ci")]

    installed = tmp_path / "node_modules/.package-lock.json"
    installed.parent.mkdir()
    installed.write_text("{}", encoding="utf-8")
    assert node_installs(tmp_path, commands) == []

    lock_time = installed.stat().st_mtime + 10
    os.utime(tmp_path / "package-lock.json", (lock_time, lock_time))
    assert [install.argv for install in node_installs(tmp_path, commands)] == [("npm", "ci")]


def test_the_stack_front_runs_through_the_manager_of_its_lock(tmp_path: Path) -> None:
    # An adopted Nuxt app kept on npm: `pnpm dev` installed over its lock and stopped on
    # ERR_PNPM_IGNORED_BUILDS (pnpm 12).
    front = tmp_path / "frontend"
    front.mkdir()
    (front / "nuxt.config.ts").touch()
    (front / "package.json").write_text('{"scripts": {"dev": "nuxt dev"}}', encoding="utf-8")
    assert [command.argv for command in dev_processes(tmp_path)] == [("pnpm", "dev")]

    (front / "package-lock.json").write_text("{}", encoding="utf-8")
    assert [command.argv for command in dev_processes(tmp_path)] == [("npm", "run", "dev")]

    (front / "pnpm-lock.yaml").touch()
    assert [command.argv for command in dev_processes(tmp_path)] == [("pnpm", "dev")]


def test_a_folder_without_package_json_installs_nothing(tmp_path: Path) -> None:
    assert node_installs(tmp_path, [Command("worker", ".", ("sleep", "1"))]) == []


ISSUE_59_COMPOSE = (
    "services:\n  web:\n    build: .\n  server:\n    build: ./server\n  db:\n    image: postgres\n"
)


@pytest.fixture
def adopted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Issue #59: package.json's `dev` and `server`, a compose file running `web` and `server`."""
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "package.json").write_text(
        '{"scripts": {"dev": "vite", "server": "node server.js"}}', encoding="utf-8"
    )
    (tmp_path / "compose.yaml").write_text(ISSUE_59_COMPOSE, encoding="utf-8")
    monkeypatch.setattr("ion_repo.dev.shutil.which", lambda name: f"/usr/bin/{name}")
    return tmp_path


def test_a_compose_file_running_the_project_is_offered_and_remembered(adopted: Path) -> None:
    from ion_repo.dev import _compose_instead

    asked: list[str] = []

    def answer(reply: str) -> Callable[[str], str]:
        def ask(prompt: str) -> str:
            asked.append(prompt)
            return reply

        return ask

    commands = dev_processes(adopted)
    assert _compose_instead(adopted, commands, answer("c"))
    assert asked == ["Choice [c]: "]
    assert not _compose_instead(adopted, commands, answer("m"))
    assert _compose_instead(adopted, commands, answer("")) is False
    assert asked[-1] == "Choice [m]: "


def test_outside_a_terminal_the_compose_file_is_only_pointed_to(
    adopted: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from ion_repo.dev import _compose_instead

    assert not _compose_instead(adopted, dev_processes(adopted), None)
    assert "compose.yaml runs web, server too: ion repo dev --containers" in capsys.readouterr().out


def test_a_stack_kiln_serves_keeps_its_servers_beside_its_compose_file(adopted: Path) -> None:
    from ion_repo.dev import _compose_instead

    (adopted / "backend").mkdir()
    (adopted / "backend/manage.py").touch()

    assert not _compose_instead(adopted, dev_processes(adopted), lambda prompt: "c")


@pytest.fixture
def held_port() -> Iterator[int]:
    """A port another process listens on, as annski's 8000 while SteamLens starts."""
    with socket.socket() as holder:
        holder.bind(("127.0.0.1", 0))
        holder.listen()
        yield holder.getsockname()[1]


def _listening_server(label: str, port: int) -> Command:
    script = (
        "import socket, sys, time\n"
        "s = socket.socket(); s.bind(('127.0.0.1', int(sys.argv[2]))); s.listen()\n"
        "print('on', sys.argv[2], flush=True); time.sleep(60)"
    )
    return Command(label, "backend", (sys.executable, "-c", script, "--port", str(port)))


def test_a_taken_port_moves_the_server_to_the_next_free_one(
    project: Path,
    held_port: int,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setitem(ports.DEV_PORTS, "fastapi", held_port)
    commands = [_listening_server("fastapi", held_port)]

    chosen = background.choose_ports(project, commands)
    background.start(project, commands, chosen)
    background.show_status(project)

    port = chosen.of("fastapi")
    assert port is not None and port > held_port
    assert background.records(project)["fastapi"]["port"] == port
    assert f"on {port}" in (background.state_dir(project) / "fastapi.log").read_text()
    output = capsys.readouterr()
    assert f"port {held_port} is taken by " in output.err + output.out
    assert f"running  http://localhost:{port}" in output.out


def test_a_server_is_ready_only_when_its_own_process_listens(held_port: int) -> None:
    # Another process answering on the port is not taken for the server (#60).
    if not Path("/proc/net/tcp").is_file():
        pytest.skip("no /proc: anyone answering counts")
    assert ports.serves(held_port, os.getpgid(0))
    with subprocess.Popen(["sleep", "60"], start_new_session=True) as other:
        assert not ports.serves(held_port, other.pid)
        other.kill()


@pytest.mark.parametrize(
    ("command", "argv"),
    [
        (
            Command("django", "backend", ("uv", "run", "python", "manage.py", "runserver")),
            ("uv", "run", "python", "manage.py", "runserver", "8001"),
        ),
        (
            Command("fastapi", "backend", ("uvicorn", "app:app", "--port", "8000", "--reload")),
            ("uvicorn", "app:app", "--port", "8001", "--reload"),
        ),
        (Command("nuxt", "frontend", ("pnpm", "dev")), ("pnpm", "dev")),
        (
            Command("vite-react", "frontend", ("npm", "run", "dev")),
            ("npm", "run", "dev", "--", "--port", "8001", "--strictPort"),
        ),
        (
            Command("streamlit", "frontend", ("uv", "run", "streamlit", "run", "app.py")),
            ("uv", "run", "streamlit", "run", "app.py", "--server.port", "8001"),
        ),
        (Command("django", "backend", ("sh", "-c", "python manage.py runserver")), None),
    ],
)
def test_each_server_is_told_its_new_port(command: Command, argv: tuple[str, ...] | None) -> None:
    assert ports.with_port(command, 8001) == argv


def test_the_front_follows_the_backend_and_the_backend_the_front(tmp_path: Path) -> None:
    # SteamLens: `process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api'`.
    (tmp_path / "nuxt.config.ts").write_text(
        "apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api'", encoding="utf-8"
    )
    moved = ports.Ports({"django": 8001, "nuxt": 3001})
    nuxt = Command("nuxt", "frontend", ("pnpm", "dev"))
    django = Command("django", "backend", ("uv", "run", "python", "manage.py", "runserver"))

    front = moved.env(nuxt, {"SITE": "http://127.0.0.1:8000/", "HOME": "/home"}, tmp_path)
    back = moved.env(django, {"CORS_ORIGINS": "http://localhost:3000"}, tmp_path)

    assert front == {
        "SITE": "http://127.0.0.1:8001/",
        "NUXT_PORT": "3001",
        "PORT": "3001",
        "NUXT_BACKEND_URL": "http://localhost:8001",
        "BACKEND_URL": "http://localhost:8001",
        "API_URL": "http://localhost:8001",
        "NUXT_PUBLIC_API_BASE": "http://localhost:8001/api",
    }
    assert back == {"CORS_ORIGINS": "http://localhost:3001"}
    assert ports.Ports({"django": 8000}).env(nuxt, {}, tmp_path) == {}

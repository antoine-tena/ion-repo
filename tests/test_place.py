"""`place.py`: a session started outside any repo is told the repos below it."""

import importlib.util
import io
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

HOOKS = Path(__file__).resolve().parent.parent / "plugins/kiln/hooks"


def load(name: str) -> ModuleType:
    sys.path.insert(0, str(HOOKS))
    spec = importlib.util.spec_from_file_location(name, HOOKS / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def place() -> ModuleType:
    return load("place")


@pytest.fixture
def code(tmp_path: Path) -> Path:
    """`code/` holding `shop`, `tools/kiln`, a hidden repo, a nested one and a plain folder."""
    root = tmp_path / "code"
    for repo in ("shop", "tools/kiln", ".hidden/secret", "shop/inner"):
        (root / repo).mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(root / repo)], check=True)
    (root / "notes").mkdir()
    return root


def test_repos_below_skip_hidden_folders_and_inside_repos(place: ModuleType, code: Path) -> None:
    assert [repo.relative_to(code) for repo in place.repos_below(code)] == [
        Path("shop"),
        Path("tools/kiln"),
    ]


def test_outside_a_repo_claude_is_told_the_repos_below(place: ModuleType, code: Path) -> None:
    told = place.context(code)
    assert told.startswith(f"kiln [WRONG-PLACE]: this session was started in {code},")
    assert "Repos below it: shop, tools/kiln." in told
    assert "secret" not in told and "inner" not in told


def test_a_long_list_is_cut(place: ModuleType, code: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(place, "MAX_LISTED", 1)
    assert "Repos below it: shop and 1 more." in place.context(code)


def test_silent_inside_a_repo_and_without_repos_below(place: ModuleType, code: Path) -> None:
    assert place.context(code / "shop" / "inner") == ""
    assert place.context(code / "shop") == ""
    assert place.context(code / "notes") == ""


def test_session_start_adds_it_to_claude_s_context(
    code: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    session_start = load("session_start")
    monkeypatch.setattr(session_start, "save_notice", lambda *_: None)
    monkeypatch.setattr(session_start, "paused_sessions", lambda _: "")
    payload = {"session_id": "s1", "cwd": str(code), "source": "startup"}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    output = io.StringIO()
    monkeypatch.setattr("sys.stdout", output)
    session_start.main()
    told = json.loads(output.getvalue())["hookSpecificOutput"]["additionalContext"]
    assert "[WRONG-PLACE]" in told and "shop, tools/kiln" in told

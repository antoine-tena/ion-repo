"""`place.py`: a session started outside any repo, whose first messages name a repo below it."""

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
def place(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    module = load("place")
    monkeypatch.setattr(module, "PLACES_DIR", tmp_path / "places")
    return module


@pytest.fixture
def code(tmp_path: Path) -> Path:
    """`code/` holding `shop`, `tools/kiln`, `tools/kiln-measures`, a hidden and a nested repo."""
    root = tmp_path / "code"
    for repo in ("shop", "tools/kiln", "tools/kiln-measures", ".hidden/secret", "shop/inner"):
        (root / repo).mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(root / repo)], check=True)
    (root / "notes").mkdir()
    return root


def ask(place: ModuleType, cwd: Path, prompt: str, session: str = "s1") -> str | None:
    return place.check({"session_id": session, "cwd": str(cwd), "prompt": prompt})


def test_repos_below_skip_hidden_folders_and_inside_repos(place: ModuleType, code: Path) -> None:
    assert [repo.relative_to(code) for repo in place.repos_below(code)] == [
        Path("shop"),
        Path("tools/kiln"),
        Path("tools/kiln-measures"),
    ]


@pytest.mark.parametrize(
    ("prompt", "expected"),
    [
        ("fix the hooks of kiln", True),
        ("Kiln's hooks", True),
        ("in ~/code/tools/kiln, please", True),
        ("what does kiln?", True),
        ("look at kiln-measures", False),
        ("the kilns of the village", False),
        ("read kiln.toml", False),
    ],
)
def test_a_repo_is_named_as_a_word(place: ModuleType, prompt: str, expected: bool) -> None:
    assert place.named(prompt, "kiln") is expected


def test_a_named_repo_is_told_once(place: ModuleType, code: Path) -> None:
    told = ask(place, code, "add a page to the shop")
    assert told is not None and "[WRONG-PLACE]" in told and f"cd {code / 'shop'} && claude" in told
    assert ask(place, code, "and the shop's footer") is None


def test_kiln_measures_is_not_kiln(place: ModuleType, code: Path) -> None:
    told = ask(place, code, "a new measure in kiln-measures")
    assert told is not None and f"cd {code / 'tools/kiln-measures'} " in told
    assert f"({code / 'tools/kiln'})" not in told


def test_a_name_of_the_launch_path_means_that_folder(place: ModuleType, code: Path) -> None:
    assert ask(place, code / "tools", "how should the tools work together?") is None
    (code / "tools" / "tools").mkdir()
    subprocess.run(["git", "init", "-q", str(code / "tools" / "tools")], check=True)
    assert ask(place, code / "tools", "the tools, again", session="s2") is None


def test_silent_inside_a_repo(place: ModuleType, code: Path) -> None:
    assert ask(place, code / "shop" / "inner", "work on kiln") is None
    assert ask(place, code / "shop", "work on kiln", session="s2") is None


def test_silent_for_slash_commands_and_unknown_names(place: ModuleType, code: Path) -> None:
    assert ask(place, code, "/kiln:pause") is None
    assert ask(place, code, "hello") is None
    assert ask(place, code, "what about notes?") is None


def test_only_the_first_messages_are_watched(place: ModuleType, code: Path) -> None:
    for prompt in ("hello", "how are you", "fine"):
        assert ask(place, code, prompt) is None
    assert ask(place, code, "now the shop") is None


def test_first_prompt_hands_the_advice_to_claude(
    tmp_path: Path, code: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    first_prompt = load("first_prompt")
    monkeypatch.setattr(first_prompt, "NOTICES_DIR", tmp_path / "notices")
    monkeypatch.setattr(first_prompt.place, "PLACES_DIR", tmp_path / "places")
    payload = {"session_id": "s1", "cwd": str(code), "prompt": "the shop"}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    output = io.StringIO()
    monkeypatch.setattr("sys.stdout", output)
    first_prompt.main()
    told = json.loads(output.getvalue())["hookSpecificOutput"]
    assert told["hookEventName"] == "UserPromptSubmit"
    assert "[WRONG-PLACE]" in told["additionalContext"]

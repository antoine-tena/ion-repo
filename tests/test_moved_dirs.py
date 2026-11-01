"""A project renamed (`ion repo set name=`, `plugin_name=`, or the first update under
`plugin_name`): its folders move with what it made of them."""

import subprocess
from pathlib import Path

import copier
import pytest

from ion_repo import update
from ion_repo.moved_dirs import Renaming, renaming_of
from ion_repo.settings import follow_plugin_name
from ion_repo.template import TEMPLATE_SOURCE_VARIABLE

REPO = Path(__file__).resolve().parent.parent
ANSWERS = {
    "title": "Tool",
    "description": "A tool",
    "project_type": "cli",
    "backend": "cli",
    "frontend": "none",
    "claude_plugin": True,
    "owner": "antoine-tena",
    "language": "en",
    "team": [],
    "podman": False,
}
IDENTITY = ("-c", "user.name=t", "-c", "user.email=t@example.com")


def git(root: Path, *arguments: str) -> None:
    subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True)


def commit(root: Path, message: str) -> None:
    git(root, "add", "-A")
    git(root, *IDENTITY, "commit", "-qm", message, "--no-verify")


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A generated tool whose package was reshaped: `cli.py` became `cli/`, `greeting.py` is gone,
    its test rewritten, a skill of its own."""
    clone = tmp_path / "template"
    subprocess.run(["git", "clone", "-q", str(REPO), str(clone)], check=True)
    monkeypatch.setenv(TEMPLATE_SOURCE_VARIABLE, str(clone))
    root = tmp_path / "old-tool"
    copier.run_copy(
        str(clone),
        root,
        vcs_ref="HEAD",
        defaults=True,
        quiet=True,
        data={**ANSWERS, "name": "old-tool"},
    )
    git(root, "init", "-q", "-b", "feat")
    commit(root, "init")
    package = root / "backend/old_tool"
    (package / "greeting.py").unlink()
    (package / "cli.py").unlink()
    (package / "cli").mkdir()
    (package / "cli/__init__.py").write_text("from old_tool.cli.run import main\n")
    (package / "cli/run.py").write_text("def main() -> int:\n    return 0\n")
    (root / "backend/tests/test_cli.py").write_text("from old_tool.cli import main\n")
    return root


def test_a_new_name_moves_the_package_and_keeps_its_shape(project: Path) -> None:
    commit(project, "mine")

    update.apply_template(project, {"name": "new-tool", "plugin_name": "new-tool"})

    package = project / "backend/new_tool"
    assert not (project / "backend/old_tool").exists()
    assert not (package / "cli.py").exists()
    assert not (package / "greeting.py").exists()
    assert (package / "cli/__init__.py").read_text() == "from new_tool.cli.run import main\n"
    assert (package / "cli/run.py").is_file()
    assert (package / "py.typed").is_file()
    assert (project / "backend/tests/test_cli.py").read_text() == "from new_tool.cli import main\n"
    assert update.conflicted_files(project) == []
    assert (project / "plugins/new-tool/.claude-plugin/plugin.json").is_file()
    assert not (project / "plugins/old-tool").exists()


def test_a_new_plugin_name_moves_the_plugin_and_what_cites_it(project: Path) -> None:
    own_skill = project / "plugins/old-tool/skills/own/SKILL.md"
    own_skill.parent.mkdir()
    own_skill.write_text("---\nname: own\n---\nSee /old-tool:run, not host:port.\n")
    (project / "docs.md").write_text(
        "`old-tool@old-tool`, plugins/old-tool/skills, `old-tool` cmd\n"
    )
    (project / "plugins/old-tool/skills/run/SKILL.md").unlink()
    commit(project, "mine")

    update.apply_template(project, {"plugin_name": "tool"})

    assert not (project / "plugins/old-tool").exists()
    moved = (project / "plugins/tool/skills/own/SKILL.md").read_text()
    assert "See /tool:run, not host:port." in moved
    assert not (project / "plugins/tool/skills/run/SKILL.md").exists()
    # The command keeps its name; only the plugin moved.
    assert (project / "backend/old_tool/py.typed").is_file()
    assert (project / "docs.md").read_text() == (
        "`tool@old-tool`, plugins/tool/skills, `old-tool` cmd\n"
    )


def test_a_real_conflict_stays_marked(project: Path) -> None:
    readme = project / "plugins/old-tool/README.md"
    readme.write_text(readme.read_text().replace("# The `old-tool`", "# Mine, `old-tool`"))
    commit(project, "mine")

    update.apply_template(project, {"plugin_name": "tool"})

    assert "<<<<<<< before updating" in (project / "plugins/tool/README.md").read_text()
    assert not (project / "plugins/old-tool").exists()


def test_a_rename_keeps_a_project_comment_beside_the_pypi_name_that_stays(project: Path) -> None:
    commit(project, "mine")
    update.apply_template(project, {"pypi_name": "old-tool"})
    pyproject = project / "backend/pyproject.toml"
    comment = "the command stays `old-tool`"
    assert comment in pyproject.read_text()
    pyproject.write_text(pyproject.read_text().replace(comment, "the command stays `old tool`"))
    commit(project, "own comment")

    update.apply_template(project, {"name": "new-tool", "plugin_name": "new-tool"})

    assert update.conflicted_files(project) == []
    text = pyproject.read_text()
    assert "the command stays `old tool`" in text
    assert 'name = "old-tool"' in text
    assert 'new-tool = "new_tool.cli:main"' in text


def test_a_line_the_new_render_still_holds_keeps_the_old_name() -> None:
    renaming = Renaming("old-tool", "new-tool", None, None, True)
    render = 'name = "old-tool"\n'
    assert renaming.words_beside('name = "old-tool"\nrun old-tool\n', render) == (
        'name = "old-tool"\nrun new-tool\n'
    )


def test_nothing_moves_without_a_new_name(project: Path) -> None:
    assert (
        renaming_of(
            {"name": "a", "plugin_name": "b", "claude_plugin": True, "backend": "cli"},
            {"name": "a", "plugin_name": "b", "claude_plugin": True, "backend": "cli"},
        )
        is None
    )


def test_a_plugin_before_plugin_name_bore_the_project_name() -> None:
    renaming = renaming_of(
        {"name": "ion-host", "claude_plugin": True, "backend": "cli"},
        {"name": "ion-host", "plugin_name": "host", "claude_plugin": True, "backend": "cli"},
    )
    assert renaming == Renaming("ion-host", "ion-host", "ion-host", "host", True)
    assert renaming.folders == [("plugins/ion-host", "plugins/host")]
    assert renaming.references("run ion-host:domain, ion-host@ion-host, `ion-host check`") == (
        "run host:domain, host@ion-host, `ion-host check`"
    )


@pytest.mark.parametrize(
    ("answers", "expected"),
    [
        ({"name": "ion-a", "plugin_name": "a"}, "b"),
        ({"name": "ion-a", "plugin_name": "apart"}, None),
        ({"name": "ion-a"}, None),
    ],
)
def test_a_new_name_brings_a_default_plugin_name(
    answers: dict[str, object], expected: str | None
) -> None:
    changes = follow_plugin_name(answers, {"name": "ion-b"})
    assert changes.get("plugin_name") == expected

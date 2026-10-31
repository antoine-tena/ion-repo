"""What `kiln new` says while it generates the project and once it exists."""

from pathlib import Path

import copier
import pytest

from ion_repo import new, ui
from ion_repo.new import NewProjectRequest, create_project, next_steps


def steps_for(tmp_path: Path, backend: str, frontend: str, project_type: str) -> list[str]:
    root = tmp_path / "demo"
    root.mkdir()
    (root / ".copier-answers.yml").write_text(
        f"_commit: v0.4.0\nname: demo\nbackend: {backend}\nfrontend: {frontend}\n"
        f"project_type: {project_type}\npodman: false\n"
    )
    request = NewProjectRequest(root, {}, None, should_install=True, should_publish=False)
    return next_steps(request, root)


def test_a_django_and_nuxt_app_gets_no_frozen_notice(tmp_path: Path) -> None:
    lines = steps_for(tmp_path, "django", "nuxt", "app")

    assert lines[0] == f"cd {tmp_path / 'demo'}"
    assert any("A first prompt to try" in line for line in lines)
    assert not any("frozen" in line for line in lines)


@pytest.mark.parametrize(("backend", "frontend"), [("fastapi", "none"), ("django", "astro")])
def test_the_other_stacks_are_said_frozen_but_maintained(
    tmp_path: Path, backend: str, frontend: str
) -> None:
    lines = steps_for(tmp_path, backend, frontend, "api")

    notice = next(line for line in lines if "frozen, maintained" in line)
    assert notice.startswith("Django and Nuxt: complete.")
    assert (backend if backend != "django" else frontend) in notice


class GenerationStoppedError(Exception):
    """Raised by the fake Copier: the test stops right after the generation step."""


def generate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, terminal: bool
) -> dict[str, object]:
    """The options `kiln new` hands Copier, in a terminal or not."""
    handed: dict[str, object] = {}

    def run_copy(*arguments: object, **options: object) -> None:
        handed.update(options)
        raise GenerationStoppedError

    monkeypatch.setattr(copier, "run_copy", run_copy)
    monkeypatch.setattr(new, "require_tools", lambda *tools: None)
    monkeypatch.setattr(new, "template_source", lambda template: "gh:antoine-tena/kiln")
    monkeypatch.setattr(new, "template_revision", lambda source: "v0.4.1")
    monkeypatch.setattr(new, "follows_candidates", lambda: False)
    monkeypatch.setattr(ui, "is_styled", lambda stream=None: terminal)
    monkeypatch.delenv("KILN_VERBOSE", raising=False)
    request = NewProjectRequest(tmp_path / "demo", {}, None, False, False)
    with pytest.raises(GenerationStoppedError):
        create_project(request)
    return handed


def test_in_a_terminal_the_generation_is_one_line_like_the_other_steps(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    options = generate(tmp_path, monkeypatch, terminal=True)

    assert options["quiet"] is True
    assert "copier copy" in capsys.readouterr().out


def test_outside_a_terminal_copier_lists_what_it_writes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    options = generate(tmp_path, monkeypatch, terminal=False)

    assert options["quiet"] is False
    assert "copier copy" not in capsys.readouterr().out

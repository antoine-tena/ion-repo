"""What `kiln new` says once the project exists."""

from pathlib import Path

import pytest

from kiln.new import NewProjectRequest, next_steps


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

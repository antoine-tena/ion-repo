import contextlib
import datetime
import json
import os
import subprocess
import sys
import zipfile
from collections.abc import Iterator
from pathlib import Path

import copier
import pytest
from packaging.version import Version
from plumbum import ProcessExecutionError

from kiln import check, cli, deps, github, ui
from kiln.banner import LOGO, _project_summary, render_logo
from kiln.check import _check_commands, _ci_django_job
from kiln.ci.jobs import Plan, Services
from kiln.ci.workflow import Job
from kiln.config import UserConfig
from kiln.deps import _major_bounds
from kiln.dev import read_env_file, service_prefix
from kiln.dev.backing import backing_services
from kiln.doctor import Level, repo_findings, workstation_findings
from kiln.install import (
    ensure_env_file,
    moved_from,
    pnpm_behind,
    pnpm_install_command,
    sync_command,
)
from kiln.release import (
    Evidence,
    Tag,
    is_fixes_only,
    latest_candidates,
    next_version,
    promotion_verdict,
)
from kiln.rules import charter_rules, verified_rules, write_unverified_rules
from kiln.settings import (
    parse_assignments,
    remove_replaced_artifacts,
    remove_starter_files,
    stop_on_conflicts,
)
from kiln.shell import KilnError, quiet_git
from kiln.stack import (
    PNPM_LENIENT_BUILDS,
    Command,
    Stack,
    answers_if_any,
    load_stack,
    stack_from_answers,
)
from kiln.template import DEFAULT_TEMPLATE_SOURCE, template_revision
from kiln.update import (
    apply_template,
    check_tool_not_older,
    git_failure,
    replace_legacy_source,
)
from kiln.versions import (
    installed_version,
    notes_between,
    release_version,
    tag_of,
    tool_release_tag,
)

REPO = Path(__file__).resolve().parent.parent


def test_legacy_answers_mean_django_and_nuxt() -> None:
    assert stack_from_answers({}) == Stack(backend="django", frontend="nuxt", has_podman=False)


def test_python_dirs_cover_backend_and_python_frontend() -> None:
    stack = Stack(backend="data", frontend="streamlit", has_podman=False)

    assert stack.python_dirs == ("backend", "frontend")
    assert stack.pnpm_dir is None


def test_checks_end_with_charter() -> None:
    commands = Stack(backend="fastapi", frontend="next", has_podman=False).check_commands()

    assert [command.label for command in commands][-3:] == [
        "frontend lint",
        "frontend typecheck",
        "charter",
    ]


@pytest.mark.parametrize(
    ("charter_name", "directory_key"), [("charter.toml", "directory"), ("charte.toml", "dossier")]
)
def test_typing_follows_the_charter_when_it_declares_it(
    tmp_path: Path, charter_name: str, directory_key: str
) -> None:
    stack = Stack(backend="django", frontend="aucun", has_podman=False)
    (tmp_path / charter_name).write_text(f'[types]\n{directory_key} = "backend"\n')

    commands = {command.label: command for command in _check_commands(tmp_path, stack)}

    assert commands["backend mypy"].argv == ("charter", "types")
    assert commands["backend mypy"].directory == "."
    assert _check_commands(tmp_path / "bare", stack)[2].argv == ("uv", "run", "mypy", ".")


def test_a_docs_only_change_runs_the_charter_on_its_files_alone(tmp_path: Path) -> None:
    stack = Stack(backend="django", frontend="nuxt", has_podman=False)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/notes.md").write_text("notes\n")

    commands = _check_commands(tmp_path, stack, changed=["docs/notes.md", "docs/gone.md"])

    assert [command.argv for command in commands] == [("charter", "file", "docs/notes.md")]


def test_a_backend_change_runs_the_backend_checks_not_the_frontend_ones(tmp_path: Path) -> None:
    stack = Stack(backend="django", frontend="nuxt", has_podman=False)

    commands = _check_commands(tmp_path, stack, changed=["backend/gone.py"])

    assert {command.directory for command in commands} == {"backend"}


def test_an_npm_front_is_checked_by_npm_and_only_with_its_own_scripts(tmp_path: Path) -> None:
    stack = Stack(backend="aucun", frontend="vite-react", has_podman=False, frontend_dir=".")
    (tmp_path / "package.json").write_text('{"scripts": {"lint": "eslint ."}}')
    (tmp_path / "package-lock.json").write_text("{}")

    commands = _check_commands(tmp_path, stack)

    # pnpm would install over package-lock.json, add a pnpm-lock.yaml, then find no typecheck.
    assert [command.argv for command in commands] == [("npm", "run", "lint"), ("charter",)]


def test_a_python_tool_the_repo_lacks_is_skipped_not_spawned(tmp_path: Path) -> None:
    stack = Stack(backend="django", frontend="aucun", has_podman=False)
    venv_bin = tmp_path / "backend" / ".venv" / "bin"
    venv_bin.mkdir(parents=True)
    (venv_bin / "ruff").touch()
    (tmp_path / "backend" / "pyproject.toml").write_text('[dependency-groups]\ndev = ["ruff"]\n')

    labels = [command.label for command in _check_commands(tmp_path, stack)]

    assert labels == ["backend ruff", "backend format", "charter"]
    (tmp_path / "backend" / "pyproject.toml").write_text('dev = ["ruff", "mypy"]\n')
    assert "backend mypy" in [command.label for command in _check_commands(tmp_path, stack)]


def test_backend_tests_take_the_databases_of_the_ci_job(tmp_path: Path) -> None:
    assert _ci_django_job(tmp_path, "backend") is None  # no ci.yml: the compose's databases
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "ci.yml").write_text(
        "jobs:\n  quality:\n    uses: antoine-tena/kiln/.github/workflows/charte.yml@v0.3.4\n"
        "  backend:\n    uses: antoine-tena/kiln/.github/workflows/django.yml@v0.3.4\n"
        "    with:\n      base: club\n      redis: docker.io/library/redis:8-alpine\n"
        "      env: |\n        DEBUG=True\n"
    )

    plan = _ci_django_job(tmp_path, "backend")

    assert plan is not None and plan.services is not None
    assert plan.services.database == "club"
    assert plan.services.redis == "docker.io/library/redis:8-alpine"
    assert dict(plan.env) == {"DEBUG": "True"}
    assert _ci_django_job(tmp_path, "api") is None


def test_backend_tests_first_remove_the_containers_of_a_killed_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[str] = []
    plan = Plan(Job("backend", "django"), (), services=Services("club", "postgres:18", ""))
    monkeypatch.setattr(check, "_ci_django_job", lambda *_: plan)

    def remove_orphans() -> int:
        calls.append("orphans")
        return 2

    monkeypatch.setattr(check, "remove_orphan_containers", remove_orphans)

    @contextlib.contextmanager
    def services(*_: object) -> Iterator[dict[str, str]]:
        calls.append("services")
        yield {}

    monkeypatch.setattr(check, "running_services", services)
    monkeypatch.setattr(check, "run_status", lambda *_: 0)

    assert check._run_check(tmp_path, Command("backend pytest", "backend", ("pytest",))) == 0
    assert calls == ["orphans", "services"]


def test_java_backend_is_checked_by_the_maven_wrapper() -> None:
    stack = Stack(backend="java", frontend="aucun", has_podman=False)

    assert stack.python_dirs == ()
    assert stack.maven_dir == "backend"
    assert stack.dev_commands() == []
    assert [(command.label, command.argv) for command in stack.check_commands()] == [
        ("backend maven", ("./mvnw", "-B", "-q", "verify", "-DskipTests")),
        ("charter", ("charter",)),
    ]
    assert stack.check_commands(with_tests=True)[0].argv == ("./mvnw", "-B", "-q", "verify")


def test_test_suites_run_only_on_request() -> None:
    stack = Stack(backend="django", frontend="nuxt", has_podman=False)

    assert "backend pytest" not in [command.label for command in stack.check_commands()]
    assert "backend pytest" in [command.label for command in stack.check_commands(True)]


def test_java_backend_with_a_frontend_serves_its_jar_in_dev() -> None:
    commands = Stack(backend="java", frontend="nuxt", has_podman=False).dev_commands()

    assert [(command.label, command.directory) for command in commands] == [
        ("java", "backend"),
        ("nuxt", "frontend"),
    ]
    script = commands[0].argv[-1]
    assert script.startswith("./mvnw -q -B -DskipTests package && ")
    assert script.endswith('exec java -jar "$1"')


def test_env_file_of_a_server_is_read(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("# local\nexport PORT=9000\nNAME='demo pass'\n\nBROKEN\nEMPTY=\n")

    assert read_env_file(env_file) == {"PORT": "9000", "NAME": "demo pass", "EMPTY": ""}
    assert read_env_file(tmp_path / "absent") == {}


def test_adopted_maven_backend_is_detected(tmp_path: Path) -> None:
    (tmp_path / "backend").mkdir()
    (tmp_path / "backend/pom.xml").write_text("<project/>")

    assert load_stack(tmp_path).backend == "java"


def test_major_bounds_keep_the_major() -> None:
    assert _major_bounds(Version("6.1.2")) == ">=6.1.2,<7.0.0"
    assert _major_bounds(Version("0.25.1")) == ">=0.25.1,<0.26.0"


def test_team_accepts_a_comma_list() -> None:
    assert parse_assignments(["team=a, b", "podman=true"]) == {"team": ["a", "b"], "podman": True}
    # Names of before kiln 0.4.0 still work.
    assert parse_assignments(["equipe=a", "frontend=aucun"]) == {"team": ["a"], "frontend": "none"}
    films = {"large_files": ["public/film.mp4", "public/film.webm"]}
    assert parse_assignments(["large_files=public/film.mp4,public/film.webm"]) == films


def test_sentence_with_a_colon_stays_text() -> None:
    sentence = "Covoiturage : proposer un trajet"
    assert parse_assignments([f"description={sentence}"]) == {"description": sentence}


def test_starter_files_go_when_the_front_already_existed(tmp_path: Path) -> None:
    composables = tmp_path / "frontend/app/composables"
    composables.mkdir(parents=True)
    (composables / "useApi.ts").write_text("new\n")
    (composables / "useHealth.ts").write_text("kept by the project\n")

    remove_starter_files(
        tmp_path,
        Stack(backend="java", frontend="nuxt", has_podman=False),
        Stack(backend="django", frontend="nuxt", has_podman=False),
        tracked={"frontend/app/composables/useHealth.ts"},
    )

    assert not (composables / "useApi.ts").exists()
    assert (composables / "useHealth.ts").exists()


def test_starter_files_stay_with_a_new_front(tmp_path: Path) -> None:
    composables = tmp_path / "frontend/app/composables"
    composables.mkdir(parents=True)
    (composables / "useApi.ts").write_text("new\n")

    remove_starter_files(
        tmp_path,
        Stack(backend="java", frontend="none", has_podman=False),
        Stack(backend="django", frontend="nuxt", has_podman=False),
        tracked=set(),
    )

    assert (composables / "useApi.ts").exists()


def test_conflicts_stop_before_the_locks(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "package.json").write_text("<<<<<<< before updating\n{}\n")

    with pytest.raises(KilnError, match=r"package\.json"):
        stop_on_conflicts(tmp_path)


def test_unknown_key_is_refused() -> None:
    with pytest.raises(KilnError):
        parse_assignments(["couleur=bleu"])


def test_rules_checked_by_the_charter_are_verified(tmp_path: Path) -> None:
    rules = tmp_path / ".claude/rules/kiln"
    rules.mkdir(parents=True)
    (rules / "django.md").write_text("- **[NO-SIGNALS]** a\n- **[GENERIC-NAMES]** b\n")
    (tmp_path / "charter.toml").write_text('[bans.django-signals]\nid = "NO-SIGNALS"\n')

    stack = Stack(backend="django", frontend="aucun", has_podman=False)
    unverified = set(charter_rules(tmp_path)) - verified_rules(tmp_path, stack)

    assert unverified == {"GENERIC-NAMES"}


def test_an_adopted_charter_of_before_0_4_still_verifies_its_rules(tmp_path: Path) -> None:
    (tmp_path / "CLAUDE.md").write_text("- **[SIGNAUX]** a\n- **[NOMS-INTERDITS]** b\n")
    (tmp_path / "charte.toml").write_text('[interdictions.signaux-django]\nid = "SIGNAUX"\n')

    write_unverified_rules(tmp_path, Stack(backend="django", frontend="aucun", has_podman=False))

    listed = (tmp_path / "scripts/ci/unverified-rules.txt").read_text()
    assert "[NOMS-INTERDITS]" in listed and "[SIGNAUX]" not in listed


def test_legacy_template_source_is_replaced(tmp_path: Path) -> None:
    answers = tmp_path / ".copier-answers.yml"
    answers.write_text("_commit: abc\n_src_path: https://github.com/antoine-tena/init-repo.git\n")

    replace_legacy_source(tmp_path)

    assert "_src_path: https://github.com/antoine-tena/kiln.git" in answers.read_text()


def _venv_with_script(venv: Path, created_in: Path) -> None:
    (venv / "bin").mkdir(parents=True)
    (venv / "bin" / "ruff").write_bytes(b"\x7fELF binary")
    (venv / "bin" / "mypy").write_text(f"#!{created_in}/bin/python\nimport mypy\n")


def test_a_venv_moved_with_its_repo_is_reinstalled(tmp_path: Path) -> None:
    venv = tmp_path / "club" / "backend" / ".venv"
    old_venv = tmp_path / "projects" / "club" / "backend" / ".venv"
    _venv_with_script(venv, old_venv)

    assert moved_from(venv) == old_venv
    assert sync_command(venv) == ["uv", "sync", "--locked", "--reinstall"]


def test_a_venv_in_place_or_absent_is_only_synced(tmp_path: Path) -> None:
    venv = tmp_path / "backend" / ".venv"
    _venv_with_script(venv, venv)

    assert moved_from(venv) is None
    assert moved_from(tmp_path / "missing") is None
    assert sync_command(venv) == ["uv", "sync", "--locked"]


def test_pnpm_dependencies_behind_their_lockfile_are_seen(tmp_path: Path) -> None:
    assert pnpm_behind(tmp_path)  # never installed
    (tmp_path / "pnpm-lock.yaml").write_text("nuxt@4.6.2\n")
    (tmp_path / "node_modules" / ".pnpm").mkdir(parents=True)
    installed = tmp_path / "node_modules" / ".pnpm" / "lock.yaml"
    installed.write_text("nuxt@4.5.2\n")
    assert pnpm_behind(tmp_path)

    installed.write_text("nuxt@4.6.2\n")
    assert not pnpm_behind(tmp_path)


def test_env_file_gets_a_local_secret_and_is_kept(tmp_path: Path) -> None:
    (tmp_path / ".env.example").write_text("DJANGO_SECRET_KEY=\nDJANGO_DEBUG=True\n")

    ensure_env_file(tmp_path)
    first = (tmp_path / ".env").read_text()
    ensure_env_file(tmp_path)

    assert first.startswith("DJANGO_SECRET_KEY=") and len(first.splitlines()[0]) > 30
    assert "DJANGO_DEBUG=True" in first
    assert (tmp_path / ".env").read_text() == first


def test_env_file_without_example_is_skipped(tmp_path: Path) -> None:
    ensure_env_file(tmp_path)

    assert not (tmp_path / ".env").exists()


def test_replaced_frontend_loses_its_lockfile(tmp_path: Path) -> None:
    (tmp_path / "frontend").mkdir()
    (tmp_path / "frontend/pnpm-lock.yaml").write_text("lockfileVersion: '9.0'\n")

    remove_replaced_artifacts(
        tmp_path,
        Stack(backend="data", frontend="nuxt", has_podman=False),
        Stack(backend="data", frontend="streamlit", has_podman=False),
    )

    assert not (tmp_path / "frontend/pnpm-lock.yaml").exists()


def test_adopted_repo_stack_comes_from_its_files(tmp_path: Path) -> None:
    (tmp_path / "backend").mkdir()
    (tmp_path / "backend" / "manage.py").touch()
    (tmp_path / "frontend").mkdir()
    (tmp_path / "frontend" / "nuxt.config.ts").touch()
    assert load_stack(tmp_path) == Stack(backend="django", frontend="nuxt", has_podman=False)


def test_adopted_repo_declares_its_size_in_its_charter(tmp_path: Path) -> None:
    (tmp_path / "charte.toml").write_text('envergure = "flame"\nexclus = []\n')
    assert answers_if_any(tmp_path) == {"size": "medium"}


def test_logo_draws_two_pixel_rows_per_line(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("COLORTERM", raising=False)
    lines = render_logo()

    assert len(lines) == len(LOGO) // 2
    assert all("\033[38;5;" in line for line in lines)


def test_project_summary_names_size_and_frameworks(tmp_path: Path) -> None:
    (tmp_path / ".copier-answers.yml").write_text(
        "nom: atelier\nenvergure: ember\nbackend: fastapi\nfrontend: aucun\npodman: true\n"
    )

    assert _project_summary(tmp_path) == "atelier · small · fastapi, podman"


def test_durations_read_the_french_way() -> None:
    assert [ui.format_duration(seconds) for seconds in (0.42, 12.3, 65)] == [
        "0.4 s",
        "12 s",
        "1 min 05 s",
    ]


def test_recap_outside_a_terminal_is_one_line(capsys: pytest.CaptureFixture[str]) -> None:
    ui._steps.clear()
    ui.step("backend : dépendances Python")

    ui.recap("install", ui._steps[0].started, succeeded=True)

    assert capsys.readouterr().out.splitlines()[-1].startswith("Install done in ")
    ui._steps.clear()


def test_machine_settings_are_parsed_and_checked() -> None:
    from kiln.config import UserConfig
    from kiln.machine import apply_machine

    updated = apply_machine(
        UserConfig(), ["system=wsl", "owner=antoine", "team=a, b", "code_dir=/srv"]
    )

    assert (updated.system, updated.owner, updated.team) == ("wsl", "antoine", ("a", "b"))
    assert updated.code_dir == Path("/srv")
    with pytest.raises(KilnError, match="machine keys"):
        apply_machine(UserConfig(), ["backend=java"])
    with pytest.raises(KilnError, match="system"):
        apply_machine(UserConfig(), ["system=windows"])


def test_machine_keys_of_before_kiln_0_4_are_still_accepted() -> None:
    from kiln.config import UserConfig
    from kiln.machine import apply_machine

    updated = apply_machine(UserConfig(), ["systeme=wsl", "canal=interne", "equipe=a"])

    assert (updated.system, updated.channel, updated.team) == ("wsl", "internal", ("a",))


def test_machine_config_of_before_kiln_0_4_is_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from kiln.config import config_path, load_config

    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    config_path().parent.mkdir(parents=True)
    config_path().write_text(
        'systeme = "wsl"\ncanal = "interne"\nstatusline = "sobre"\ndossier_code = "/srv"\n'
    )

    config = load_config()

    assert (config.system, config.channel, config.statusline) == ("wsl", "internal", "plain")
    assert config.code_dir == Path("/srv")


CHANGELOG = """# Nouveautés de kiln

## v0.5.0 — 2026-12-01
- kiln doctor

## v0.4.1 — 2026-11-10
- correctif de la bannière

## v0.4.0 — 2026-11-01
- bannière
"""


def test_release_versions_come_from_semver_tags_and_describe() -> None:
    assert release_version("v0.4.1") == Version("0.4.1")
    assert release_version("v0.5.0-rc.2") == Version("0.5.0rc2")
    assert str(release_version("v0.5.0-3-gabc1234")) == "0.5.0"
    assert release_version("v2") is None
    assert release_version("f611f82") is None


def test_update_shows_the_releases_it_crosses() -> None:
    assert [n.tag for n in notes_between("v0.4.0", "v0.5.0", CHANGELOG)] == ["v0.5.0", "v0.4.1"]
    assert [n.tag for n in notes_between("f611f82", "v0.4.0", CHANGELOG)] == ["v0.4.0"]
    assert notes_between("v0.5.0", "v0.5.0", CHANGELOG) == []
    assert notes_between("v0.4.0", "v0.5.0", CHANGELOG)[0].lines == ["- kiln doctor"]


def test_a_candidate_already_carries_its_release_notes() -> None:
    assert [n.tag for n in notes_between("v0.4.1", "v0.5.0-rc.1", CHANGELOG)] == ["v0.5.0"]
    assert notes_between("v0.5.0-rc.1", "v0.5.0", CHANGELOG) == []


def test_doctor_blocks_on_a_tool_the_repo_needs(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("kiln.doctor.shutil.which", lambda name: None)
    monkeypatch.setattr("kiln.doctor._latest_release", lambda: None)
    stack = Stack(backend="fastapi", frontend="nuxt", has_podman=False)

    findings = {f.label: f for f in workstation_findings(UserConfig(system="wsl"), stack)}

    assert findings["pnpm"].level is Level.FAIL
    assert findings["pnpm"].fix.startswith("corepack enable pnpm")
    assert findings["podman"].level is Level.WARN


def test_doctor_sees_a_stub_that_only_says_the_tool_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # macOS has /usr/bin/java without a JDK: found, but `java -version` fails (#49).
    monkeypatch.setattr("kiln.doctor.shutil.which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr("kiln.doctor._latest_release", lambda: None)
    stub = subprocess.CompletedProcess(["java"], 1, "", "Unable to locate a Java Runtime.\n")
    monkeypatch.setattr("kiln.doctor._completed", lambda command, cwd=None: stub)

    findings = {f.label: f for f in workstation_findings(UserConfig(system="macos"), None)}

    assert findings["java"].level is Level.WARN
    assert "Unable to locate a Java Runtime" in findings["java"].detail
    assert findings["java"].fix == "brew install openjdk@25"


def test_doctor_without_a_chosen_system_detects_it(monkeypatch: pytest.MonkeyPatch) -> None:
    # A repo adopted with uvx never asked for the system: macOS was told to use apt (#48).
    monkeypatch.setattr("kiln.doctor.shutil.which", lambda name: None)
    monkeypatch.setattr("kiln.doctor._latest_release", lambda: None)
    monkeypatch.setattr("kiln.doctor.detect_system", lambda: "macos")

    findings = {f.label: f for f in workstation_findings(UserConfig(), None)}

    assert findings["podman"].fix.startswith("brew install podman")


def test_doctor_knows_kilns_own_repo(tmp_path: Path) -> None:
    # kiln is the template's source: no answers, no charter, and not a stranger's repo (T-362).
    (tmp_path / "template").mkdir()
    (tmp_path / "copier.yml").write_text("_subdirectory: template\n")
    stranger = repo_findings(tmp_path, None)[0]
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "kiln-cli"\n')
    kiln = repo_findings(tmp_path, None)[0]

    assert (stranger.level, stranger.detail) == (Level.WARN, "not a kiln repo")
    assert kiln.level is Level.OK
    assert "kiln's own repo" in kiln.detail


def test_dev_prefixes_line_up_outside_a_terminal() -> None:
    assert service_prefix("nuxt", 6, ui.FIRE) == "nuxt   │ "


def test_next_version_bumps_the_patch_in_0x_even_when_breaking() -> None:
    assert next_version(Version("0.3.0"), ["fix: bannière"]) == "0.3.1"
    assert next_version(Version("0.3.0"), ["feat: doctor"]) == "0.3.1"
    assert next_version(Version("0.3.1rc2"), ["feat(cli)!: renomme set"]) == "0.3.2"
    assert next_version(Version("0.3.191"), ["fix: x"]) == "0.3.192"
    assert next_version(Version("0.3.4"), ["fix: x"], milestone=True) == "0.4.0"
    assert next_version(Version("1.2.3"), ["feat: doctor"]) == "1.3.0"
    assert next_version(Version("1.2.3"), ["fix: x\n\nBREAKING CHANGE: y"]) == "2.0.0"


def test_a_candidate_is_promoted_once_it_has_proved_itself() -> None:
    now = datetime.datetime(2026, 11, 10, tzinfo=datetime.UTC)
    day_old = Tag("v0.3.0-rc.2", Version("0.3.0rc2"), now - datetime.timedelta(hours=25))
    young = Tag("v0.3.1-rc.1", Version("0.3.1rc1"), now - datetime.timedelta(hours=3))
    run_by_a_repo = Evidence("success", ("club",))

    assert promotion_verdict(day_old, run_by_a_repo, now)[1]
    # Nobody waits for a next release any more; a young candidate soaks, whatever follows it.
    verdict, ready = promotion_verdict(young, run_by_a_repo, now)
    assert not ready and "soaking (21 h left)" in verdict
    # Soaked but run by no repo of the machine: it has verified nothing yet.
    verdict, ready = promotion_verdict(day_old, Evidence("success"), now)
    assert not ready and "kiln update --all" in verdict
    # Fixes only: two hours, no repo required.
    assert promotion_verdict(young, Evidence("success", is_fixes_only=True), now)[1]
    assert promotion_verdict(young, Evidence("success"), now, is_urgent=True)[1]
    assert not promotion_verdict(young, Evidence("failure"), now, is_urgent=True)[1]
    # A red or unfinished CI holds the candidate back, whatever else it proved.
    for ci in ("failure", "running", "none"):
        verdict, ready = promotion_verdict(day_old, Evidence(ci, ("club",), True), now)
        assert not ready and ci in verdict
    assert latest_candidates([day_old, young]) == [day_old, young]


def test_fixes_only_means_nothing_added_nor_broken() -> None:
    assert is_fixes_only(["fix(check): x", "docs: y", "chore(release): v0.4.4"])
    assert not is_fixes_only(["fix: x", "feat(dev): y"])
    assert not is_fixes_only(["fix!: x"])
    assert not is_fixes_only(["fix: x\n\nBREAKING CHANGE: y"])
    assert not is_fixes_only([])


@pytest.mark.parametrize("flag", ["--version", "-V", "-v"])
def test_version_flag_prints_the_installed_version(
    flag: str, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["kiln", flag])
    with pytest.raises(SystemExit) as exit_request:
        cli.main()

    assert exit_request.value.code == 0
    assert capsys.readouterr().out.strip() == installed_version()


def test_unreachable_github_gives_one_line(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".copier-answers.yml").write_text(
        "_commit: v0.3.0\n_src_path: https://kiln.invalid/kiln.git\n"
    )
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init"],
        cwd=tmp_path,
        check=True,
    )

    with pytest.raises(KilnError, match=r"^GitHub unreachable"):
        apply_template(tmp_path)


def test_other_git_failure_keeps_its_last_line() -> None:
    error = ProcessExecutionError(["git", "clone"], 128, "", "fatal: ref inconnue\n\n")

    assert git_failure(error) == "git failed while updating the template: fatal: ref inconnue"


@pytest.mark.parametrize("pinned", [False, True])
@pytest.mark.parametrize("local_edit", ["", "  local: true\n"])
def test_promoted_candidate_does_not_conflict_on_kiln_workflow_refs(
    tmp_path: Path, local_edit: str, pinned: bool
) -> None:
    """Le tag promu pose sur le commit de sa candidate : Copier rend l'ancienne version sous le
    nom promu, et seul le `@<tag>` des workflows de kiln différerait du projet (T-18). Une
    vraie modification locale au même endroit reste un conflit à arbitrer. Épinglé par SHA
    (`@<sha> # <tag>`), le SHA ne change pas à la promotion : seul le tag du commentaire."""
    ref = (
        "{{ _copier_conf.vcs_ref_hash }} # {{ _copier_answers._commit }}"
        if pinned
        else "{{ _copier_answers._commit }}"
    )
    template, project = tmp_path / "modele", tmp_path / "projet"

    def git(root: Path, *args: str) -> None:
        subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)

    def release(tag: str, steps: str) -> None:
        (template / "ci.yml.jinja").write_text(
            "# version de kiln ({{ _copier_answers._commit }})\n"
            "jobs:\n  python:\n    uses: antoine-tena/kiln/.github/workflows/python.yml"
            f"@{ref}\n" + steps
        )
        git(template, "add", "-A")
        git(template, "commit", "-qm", tag)
        git(template, "tag", "-a", tag, "-m", tag)

    template.mkdir()
    git(template, "init", "-q")
    (template / "copier.yml").write_text("_answers_file: .copier-answers.yml\n")
    (template / "{{_copier_conf.answers_file}}.jinja").write_text(
        "{{ _copier_answers | to_nice_yaml }}"
    )
    release("v1.0.0-rc.1", "")
    copier.run_copy(str(template), project, vcs_ref="v1.0.0-rc.1", defaults=True, quiet=True)
    with (project / "ci.yml").open("a") as ci_file:
        ci_file.write(local_edit)
    git(project, "init", "-q")
    git(project, "add", "-A")
    git(project, "commit", "-qm", "init")
    git(template, "tag", "-a", "v1.0.0", "-m", "v1.0.0")
    release("v1.0.1", "  charte: true\n")

    apply_template(project)

    ci = (project / "ci.yml").read_text()
    assert ("<<<<<<<" in ci) == bool(local_edit)
    if not local_edit:
        assert ci.endswith("v1.0.1\n  charte: true\n")
        assert ("python.yml@v1.0.1" in ci) != pinned
        assert "ci.yml" not in subprocess.check_output(
            ["git", "diff", "--name-only", "--diff-filter=U"], cwd=project, text=True
        )


class _FakeDistribution:
    def __init__(self, version: str, direct_url: str = "") -> None:
        self.version = version
        self._direct_url = direct_url

    def read_text(self, name: str) -> str | None:
        return self._direct_url if name == "direct_url.json" else None


GITHUB = '{"url": "https://github.com/antoine-tena/kiln", "vcs_info": {"vcs": "git", '
FOLDER = '{"url": "file:///home/me/kiln", "dir_info": {}}'


@pytest.mark.parametrize(
    ("version", "direct_url", "expected"),
    [
        ("0.3.4", "", "v0.3.4"),
        ("0.4.0rc2", "", "v0.4.0-rc.2"),
        (
            "0.3.3",
            GITHUB + '"requested_revision": "v0.3.3-rc.2", "commit_id": "abc"}}',
            "v0.3.3-rc.2",
        ),
    ],
)
def test_the_template_is_taken_at_the_installed_release(
    monkeypatch: pytest.MonkeyPatch, version: str, direct_url: str, expected: str
) -> None:
    monkeypatch.setattr(
        "kiln.versions._installed_distribution", lambda: _FakeDistribution(version, direct_url)
    )

    assert tool_release_tag() == expected
    assert template_revision(DEFAULT_TEMPLATE_SOURCE) == expected
    assert template_revision("/un/dossier/local") == "HEAD"


@pytest.mark.parametrize(
    ("direct_url", "recorded", "shown"),
    [
        # A checkout installed 105 commits after its tag: its code is newer than v0.3.4's template.
        (FOLDER, "v0.3.4-105-gd800ca1", "v0.3.4 +105 · d800ca1"),
        (FOLDER, "v0.4.0-rc.1-dirty", "v0.4.0-rc.1 · modified"),
        (FOLDER, None, "v0.3.4 · build unknown"),
        (
            GITHUB + '"requested_revision": "develop", "commit_id": "abc1234def"}}',
            None,
            "v0.3.4 · abc1234",
        ),
    ],
)
def test_a_tool_that_is_not_a_release_updates_no_repo(
    monkeypatch: pytest.MonkeyPatch, direct_url: str, recorded: str | None, shown: str
) -> None:
    monkeypatch.setattr(
        "kiln.versions._installed_distribution", lambda: _FakeDistribution("0.3.4", direct_url)
    )
    monkeypatch.setattr("kiln.versions._recorded_build", lambda: recorded)
    monkeypatch.setattr("kiln.template.latest_release", lambda: "v0.4.0-rc.1")

    assert tool_release_tag() is None
    assert installed_version() == shown
    with pytest.raises(
        KilnError, match=r"not a release .*git\+https://github.com/antoine-tena/kiln@v0.4.0-rc.1"
    ):
        template_revision(DEFAULT_TEMPLATE_SOURCE)
    assert template_revision("/un/dossier/local") == "HEAD"


@pytest.mark.parametrize(
    ("recorded", "expected"),
    [("v0.4.4-16-gf767dbf", "v0.4.4-16-gf767dbf"), ("v0.4.4-16-gf767dbf-dirty", None)],
)
def test_on_the_beta_channel_the_template_is_taken_at_the_tool_commit(
    monkeypatch: pytest.MonkeyPatch, recorded: str, expected: str | None
) -> None:
    monkeypatch.setattr(
        "kiln.versions._installed_distribution", lambda: _FakeDistribution("0.4.4", FOLDER)
    )
    monkeypatch.setattr("kiln.versions._recorded_build", lambda: recorded)
    monkeypatch.setattr("kiln.template.is_beta", lambda: True)

    if expected is None:
        with pytest.raises(KilnError, match="uncommitted changes"):
            template_revision(DEFAULT_TEMPLATE_SOURCE)
    else:
        assert template_revision(DEFAULT_TEMPLATE_SOURCE) == expected


def test_the_beta_channel_installs_the_checkout_of_the_code_directory(tmp_path: Path) -> None:
    from kiln.machine import apply_machine
    from kiln.versions import beta_install_command

    assert apply_machine(UserConfig(), ["channel=beta"]).channel == "beta"
    assert "@develop" in beta_install_command(tmp_path)
    (tmp_path / "kiln/src/kiln").mkdir(parents=True)
    (tmp_path / "kiln/src/kiln/versions.py").write_text("")
    assert beta_install_command(tmp_path) == f"uv tool install --force --editable {tmp_path}/kiln"


def test_the_beta_channel_finds_the_checkout_in_a_folder_of_the_code_directory(
    tmp_path: Path,
) -> None:
    from kiln.versions import beta_install_command

    (tmp_path / "tools/kiln/src/kiln").mkdir(parents=True)
    (tmp_path / "tools/kiln/src/kiln/versions.py").write_text("")
    expected = f"uv tool install --force --editable {tmp_path}/tools/kiln"
    assert beta_install_command(tmp_path) == expected
    (tmp_path / "kiln").symlink_to(tmp_path / "tools/kiln")
    assert beta_install_command(tmp_path) == expected


def test_the_beta_channel_finds_the_checkout_in_a_tool_folder_of_a_family(
    tmp_path: Path,
) -> None:
    from kiln.versions import beta_install_command

    (tmp_path / "family/kiln/kiln/src/kiln").mkdir(parents=True)
    (tmp_path / "family/kiln/kiln/src/kiln/versions.py").write_text("")
    expected = f"uv tool install --force --editable {tmp_path}/family/kiln/kiln"
    assert beta_install_command(tmp_path) == expected


def test_a_folder_install_is_what_it_was_built_from_not_the_folder_today(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "kiln.versions._installed_distribution", lambda: _FakeDistribution("0.4.0", FOLDER)
    )
    monkeypatch.setattr("kiln.versions._recorded_build", lambda: "v0.4.0-rc.1")
    monkeypatch.setattr("kiln.versions._describe", lambda _: pytest.fail("folder read live"))

    assert tool_release_tag() == "v0.4.0-rc.1"
    assert installed_version() == "v0.4.0-rc.1"


def test_an_editable_checkout_is_read_live(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    editable = json.dumps({"url": f"file://{tmp_path}", "dir_info": {"editable": True}})
    monkeypatch.setattr(
        "kiln.versions._installed_distribution", lambda: _FakeDistribution("0.4.0", editable)
    )
    git = ["git", "-C", str(tmp_path)]
    subprocess.run([*git, "init", "-q"], check=True)
    subprocess.run([*git, "commit", "-q", "--allow-empty", "-m", "a"], check=True)
    subprocess.run([*git, "tag", "v0.4.0-rc.2"], check=True)

    assert tool_release_tag() == "v0.4.0-rc.2"
    (tmp_path / "change").write_text("x")
    subprocess.run([*git, "add", "change"], check=True)

    assert tool_release_tag() is None
    assert installed_version() == "v0.4.0-rc.2 · modified"


def test_the_package_records_the_commit_it_is_built_from(tmp_path: Path) -> None:
    subprocess.run(["uv", "build", "-q", "--wheel", "-o", str(tmp_path), str(REPO)], check=True)
    wheel = next(tmp_path.glob("*.whl"))
    with zipfile.ZipFile(wheel) as archive:
        recorded = json.loads(archive.read("kiln/_build.json"))
    head = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True)
    # What git says of the checkout: a tag and a distance, or the bare commit in a shallow
    # clone without tags (GitHub's CI).
    described = subprocess.check_output(
        ["git", "-C", str(REPO), "describe", "--tags", "--always", "--dirty", "--match", "v[0-9]*"],
        text=True,
    )
    assert recorded == {"describe": described.strip(), "commit": head.strip()}


def test_a_tag_is_read_back_from_a_describe_output() -> None:
    assert tag_of("v0.4.0-rc.2-3-gabc1234") == "v0.4.0-rc.2"
    assert tag_of("v0.3.4") == "v0.3.4"
    assert tag_of("abc1234") is None


def test_update_refuses_to_take_a_repo_back_to_an_older_kiln(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / ".copier-answers.yml").write_text(
        f"_commit: v0.3.5\n_src_path: {DEFAULT_TEMPLATE_SOURCE}\n"
    )
    monkeypatch.setattr("kiln.update.tool_release_tag", lambda: "v0.3.4")

    with pytest.raises(KilnError, match="newer than the installed tool"):
        check_tool_not_older(tmp_path)


def test_without_gh_the_project_is_created_without_github(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("kiln.github.shutil.which", lambda _: None)

    assert github.can_publish() is False
    assert github.login() is None
    assert "kiln publish" in capsys.readouterr().out


def test_backing_services_reads_db_and_redis_of_the_services_only(tmp_path: Path) -> None:
    compose = tmp_path / "compose.yml"
    compose.write_text(
        "name: demo\nx-common: &common\n  tmpfs: /tmp\n"
        "services:\n  db:\n    image: postgres\n    container_name: demo-db\n"
        "  redis:\n    image: redis\n  backend:\n    container_name: demo-backend\n"
        "volumes:\n  db-data:\n",
        encoding="utf-8",
    )
    assert backing_services(compose) == {"db": "demo-db", "redis": "demo_redis_1"}


def test_git_runs_without_background_housekeeping_while_copier_works(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "user.name")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", "Kept")
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)

    def setting(key: str) -> str:
        found = subprocess.run(
            ["git", "-C", str(tmp_path), "config", "--get", key], capture_output=True, text=True
        )
        return found.stdout.strip()

    with quiet_git():
        assert (setting("gc.auto"), setting("maintenance.auto")) == ("0", "false")
        assert setting("user.name") == "Kept"
    assert setting("gc.auto") == ""
    assert os.environ["GIT_CONFIG_COUNT"] == "1"
    assert "GIT_CONFIG_KEY_1" not in os.environ


def test_synced_pnpm_dependencies_run_the_postinstall_a_skipped_install_leaves_out(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ran: list[list[str]] = []
    monkeypatch.setattr(deps, "run", lambda command, cwd: ran.append(command))

    deps.sync_dependencies(tmp_path, Stack(backend="none", frontend="nuxt", has_podman=False))

    assert ran == [
        ["pnpm", "install", PNPM_LENIENT_BUILDS],
        ["pnpm", "run", "--if-present", "postinstall"],
    ]


def test_pnpm_install_frozen_only_with_a_lockfile(tmp_path: Path) -> None:
    assert pnpm_install_command(tmp_path) == ["pnpm", "install", PNPM_LENIENT_BUILDS]
    (tmp_path / "pnpm-lock.yaml").write_text("lockfileVersion: '9.0'\n")
    frozen = ["pnpm", "install", "--frozen-lockfile", PNPM_LENIENT_BUILDS]
    assert pnpm_install_command(tmp_path) == frozen


def test_a_kiln_workflow_pinned_by_kiln_fix_follows_the_template(tmp_path: Path) -> None:
    """`@<sha> # v0.4.10` (kiln fix) against the old render `@v0.4.10` and the new `@v0.4.11`:
    no conflict left, the new tag taken, for the update's converters to pin again (T-159)."""
    from kiln.update import CONFLICT_MARKER, resolve_kiln_ref_conflicts

    def run_git(*arguments: str, given: str | None = None) -> str:
        return subprocess.run(
            ["git", *arguments],
            cwd=tmp_path,
            input=given,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    uses = "    uses: antoine-tena/kiln/.github/workflows/charter.yml@"
    base = f"# kiln v0.4.10\njobs:\n  a:\n{uses}v0.4.10\n"
    ours = f"# kiln v0.4.10\njobs:\n  a:\n{uses}{'a' * 40} # v0.4.10\n"
    theirs = f"# kiln v0.4.11\njobs:\n  a:\n{uses}v0.4.11\n"
    run_git("init", "-q")
    name = ".github/workflows/ci.yml"
    blobs = [run_git("hash-object", "-w", "--stdin", given=text) for text in (base, ours, theirs)]
    entries = "".join(f"100644 {blob} {stage}\t{name}\n" for stage, blob in enumerate(blobs, 1))
    run_git("update-index", "--index-info", given=entries)
    (tmp_path / ".github/workflows").mkdir(parents=True)
    (tmp_path / name).write_text(f"{CONFLICT_MARKER}\n{ours}=======\n{theirs}>>>>>>> after\n")
    resolve_kiln_ref_conflicts(tmp_path)
    assert (tmp_path / name).read_text() == theirs


def test_an_npm_folder_installs_with_npm_and_no_pnpm_lock(tmp_path: Path) -> None:
    # An adopted npm repo: pnpm would write a pnpm-lock.yaml next to its package-lock.json,
    # leaving the tree dirty (kiln update --all then stopped on it).
    (tmp_path / "package-lock.json").write_text("{}\n")
    assert pnpm_install_command(tmp_path) == ["npm", "ci"]

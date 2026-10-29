"""`kiln set`: shows or changes a repo's settings (team, frameworks, podman…).

The repo is rendered again with the new answers, without overwriting local changes: a removed
framework takes its files away, an added framework brings its own, then the lock files, the
dependencies and the list of unverified rules follow.
"""

import shutil
import subprocess
from pathlib import Path

import yaml  # fourni par copier

from kiln import renames, ui
from kiln.check import check_project
from kiln.deps import lock_dependencies, sync_dependencies
from kiln.rules import write_unverified_rules
from kiln.shell import KilnError, require_tools, step
from kiln.stack import BACKEND_DIR, BUILD_ARTIFACTS, FRONTEND_DIR, Stack, load_stack, read_answers
from kiln.statusline import apply_statusline_settings
from kiln.update import apply_template, check_working_branch, conflicted_files, report_changes

SETTABLE_KEYS = (
    "size",
    "name",
    "title",
    "description",
    "language",
    "language_comments",
    "language_commits",
    "language_docs",
    "language_tickets",
    "language_ui",
    "owner",
    "team",
    "project_type",
    "backend",
    "frontend",
    "podman",
    "claude_plugin",
    "pypi_name",
    "java_package",
    "timezone",
    "serena",
    "compact_window",
    "deploy",
    "vps_host",
    "api_domain",
    "vps_port",
    "vps_db_port",
    "site_url",
    "deploy_branch",
    "frontend_deploy",
    "north_star",
    "statusline_ci",
    "ci_runner",
    "update_bot",
    "prod_health_url",
    "large_files",
)
LIST_KEYS = frozenset({"team", "large_files"})
# The demo of a new project's front (a backend health badge, its typed client): it leans on the
# template's constants and generated API types, which a front already built has replaced.
STARTER_FILES = (
    "app/components/HealthStatus.vue",
    "app/composables/useHealth.ts",
    "app/composables/useApi.ts",
    "components/HealthStatus.tsx",
)
# A language set per use turns the per-use questions on (`language_custom`).
PER_USE_LANGUAGES = frozenset(key for key in SETTABLE_KEYS if key.startswith("language_"))


def show_settings(root: Path) -> None:
    answers = read_answers(root)
    width = max(len(key) for key in SETTABLE_KEYS)
    for key in SETTABLE_KEYS:
        if key in answers:
            print(f"{ui.paint(f'{key:<{width}}', ui.STONE)}  {answers[key]}")
    print()
    ui.note("Change: kiln set key=value [key=value…], on a branch, clean tree.")


def parse_assignments(assignments: list[str]) -> dict[str, object]:
    """`key=value` read as YAML (`true`, `[a, b]`); a list (team, large files) can be written
    `a,b`."""
    parsed: dict[str, object] = {}
    for assignment in assignments:
        old_key, separator, raw_value = assignment.partition("=")
        key = renames.ANSWER_KEYS.get(old_key, old_key)  # names before kiln 0.4.0 still work
        if not separator or key not in SETTABLE_KEYS:
            raise KilnError(f'"{assignment}": expected key=value, keys: {", ".join(SETTABLE_KEYS)}')
        if key in LIST_KEYS and not raw_value.startswith("["):
            parsed[key] = [entry.strip() for entry in raw_value.split(",") if entry.strip()]
        else:
            parsed[key] = _scalar(raw_value)
        if key in PER_USE_LANGUAGES:
            parsed["language_custom"] = True
    return renames.answers(parsed)


def _scalar(raw_value: str) -> object:
    """`true`, `12` or a word read as YAML; a sentence such as `a : b` stays the text typed."""
    if not raw_value:
        return ""
    value = yaml.safe_load(raw_value)
    return value if isinstance(value, (str, bool, int, float, list)) else raw_value


def apply_settings(root: Path, assignments: list[str]) -> None:
    changes = parse_assignments(assignments)
    require_tools("git", "uv")
    check_working_branch(root, "chore/kiln-set")
    step("Settings: " + ", ".join(f"{key}={value}" for key, value in changes.items()))
    previous_stack = load_stack(root)
    apply_template(root, changes)
    stack = load_stack(root)
    remove_replaced_artifacts(root, previous_stack, stack)
    remove_starter_files(root, previous_stack, stack, tracked=_tracked_files(root))
    stop_on_conflicts(root)
    apply_statusline_settings(root)
    if stack.pnpm_dir is not None:
        require_tools("pnpm")
    lock_dependencies(root, stack)
    sync_dependencies(root, stack)
    write_unverified_rules(root, stack)
    report_changes(root)
    check_project(root)


def _tracked_files(root: Path) -> set[str]:
    listed = subprocess.run(
        ["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True
    )
    return set(listed.stdout.splitlines())


def remove_starter_files(root: Path, previous: Stack, current: Stack, *, tracked: set[str]) -> None:
    """The front's demo brought by a new backend, removed when the front already existed: it
    would not type-check against the project's own constants and API types."""
    if current.backend == previous.backend or previous.frontend in ("", "none"):
        return
    if current.frontend != previous.frontend:
        return
    for name in STARTER_FILES:
        relative = f"{FRONTEND_DIR}/{name}"
        path = root / relative
        if path.is_file() and relative not in tracked:
            path.unlink()
            print(f"Removed: {relative} (demo of a new front; this one already has its pages)")


def stop_on_conflicts(root: Path) -> None:
    """Locks and installs read package.json and pyproject.toml: never with conflict markers."""
    conflicted = conflicted_files(root)
    if conflicted:
        raise KilnError(
            "settings applied, conflicts left to resolve by hand: "
            + ", ".join(conflicted)
            + ". Resolve them, commit, then run the same `kiln set` again"
            " to lock, install and check."
        )


def remove_replaced_artifacts(root: Path, previous: Stack, current: Stack) -> None:
    """Build outputs of a replaced framework (`.nuxt`, `node_modules`, `.venv`…), which would
    get in the way of the new one's tools; never data nor `.env`."""
    replaced = [
        (BACKEND_DIR, previous.backend) if previous.backend != current.backend else None,
        (FRONTEND_DIR, previous.frontend) if previous.frontend != current.frontend else None,
    ]
    for directory, framework in filter(None, replaced):
        for artifact in BUILD_ARTIFACTS.get(framework, ()):
            path = root / directory / artifact
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()
            else:
                continue
            print(f"Removed: {directory}/{artifact} ({framework})")

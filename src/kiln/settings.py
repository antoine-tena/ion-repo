"""`kiln set`: shows or changes a repo's settings (team, frameworks, podman…).

The repo is rendered again with the new answers, without overwriting local changes: a removed
framework takes its files away, an added framework brings its own, then the lock files, the
dependencies and the list of unverified rules follow.
"""

import shutil
from pathlib import Path

import yaml  # fourni par copier

from kiln import renames, ui
from kiln.check import check_project
from kiln.deps import lock_dependencies, sync_dependencies
from kiln.rules import write_unverified_rules
from kiln.shell import KilnError, require_tools, step
from kiln.stack import BACKEND_DIR, BUILD_ARTIFACTS, FRONTEND_DIR, Stack, load_stack, read_answers
from kiln.statusline import apply_statusline_settings
from kiln.update import apply_template, check_working_branch, report_changes

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
    "java_package",
    "timezone",
    "serena",
    "deploy",
    "vps_host",
    "api_domain",
    "site_url",
    "deploy_branch",
    "frontend_deploy",
    "north_star",
    "statusline_ci",
    "ci_runner",
    "prod_health_url",
)
LIST_KEYS = frozenset({"team"})
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
    """`key=value` read as YAML (`true`, `[a, b]`); a team can be written `a,b`."""
    parsed: dict[str, object] = {}
    for assignment in assignments:
        old_key, separator, raw_value = assignment.partition("=")
        key = renames.ANSWER_KEYS.get(old_key, old_key)  # names before kiln 0.4.0 still work
        if not separator or key not in SETTABLE_KEYS:
            raise KilnError(f'"{assignment}": expected key=value, keys: {", ".join(SETTABLE_KEYS)}')
        if key in LIST_KEYS and not raw_value.startswith("["):
            parsed[key] = [login.strip() for login in raw_value.split(",") if login.strip()]
        else:
            parsed[key] = yaml.safe_load(raw_value) if raw_value else ""
        if key in PER_USE_LANGUAGES:
            parsed["language_custom"] = True
    return renames.answers(parsed)


def apply_settings(root: Path, assignments: list[str]) -> None:
    changes = parse_assignments(assignments)
    require_tools("git", "uv")
    check_working_branch(root)
    step("Settings: " + ", ".join(f"{key}={value}" for key, value in changes.items()))
    previous_stack = load_stack(root)
    apply_template(root, changes)
    stack = load_stack(root)
    remove_replaced_artifacts(root, previous_stack, stack)
    apply_statusline_settings(root)
    if stack.pnpm_dir is not None:
        require_tools("pnpm")
    lock_dependencies(root, stack)
    sync_dependencies(root, stack)
    write_unverified_rules(root, stack)
    report_changes(root)
    check_project(root)


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

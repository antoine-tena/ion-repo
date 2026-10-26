"""Dependency locks and updates, by kiln's policy.

By default, compatible updates: uv stays within the bounds of pyproject.toml (same major
version), pnpm only bumps the dependencies whose latest version keeps the same major.
`--major` raises the Python bounds to the latest version, takes the latest pnpm versions and
updates the pre-commit hooks. The checks always follow (`kiln check`).
"""

import json
import subprocess
import tomllib
from pathlib import Path

import yaml  # shipped with copier
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version

from kiln.shell import run, step
from kiln.stack import PNPM_LENIENT_BUILDS, Stack

PNPM_WORKSPACE = "pnpm-workspace.yaml"
DEV_DEPENDENCY_TYPE = "devDependencies"


def lock_dependencies(root: Path, stack: Stack) -> None:
    """Locks recomputed without version bumps (the template may have changed the dependencies)."""
    step("Dependency locks")
    for directory in stack.python_dirs:
        run(["uv", "lock"], root / directory)
    if stack.pnpm_dir is not None:
        run(["pnpm", "install", "--lockfile-only"], root / stack.pnpm_dir)


def sync_dependencies(root: Path, stack: Stack) -> None:
    """Environments as the locks say. `pnpm add` skips the project's `postinstall` (Nuxt's
    `nuxt prepare`, which writes `.nuxt/`), and a `pnpm install` that finds nothing to do skips it
    too: it runs on its own, or a fresh worktree's lint lacks `.nuxt/eslint.config.mjs`."""
    for directory in stack.python_dirs:
        run(["uv", "sync"], root / directory)
    if stack.pnpm_dir is not None:
        run(["pnpm", "install", PNPM_LENIENT_BUILDS], root / stack.pnpm_dir)
        run(["pnpm", "run", "--if-present", "postinstall"], root / stack.pnpm_dir)


def update_dependencies(root: Path, stack: Stack, *, allow_major: bool) -> None:
    for directory in stack.python_dirs:
        step(f"{directory}: Python dependencies{' (majors included)' if allow_major else ''}")
        if allow_major:
            raise_python_bounds(root / directory)
        run(["uv", "lock", "--upgrade"], root / directory)
    if stack.pnpm_dir is not None:
        step(f"{stack.pnpm_dir}: pnpm dependencies{' (majors included)' if allow_major else ''}")
        update_pnpm(root / stack.pnpm_dir, allow_major=allow_major)
    if allow_major:
        step("pre-commit hooks")
        run(["pre-commit", "autoupdate"], root)
    sync_dependencies(root, stack)


def _requirement_strings(pyproject: dict[str, object]) -> list[str]:
    project = pyproject.get("project", {})
    groups = pyproject.get("dependency-groups", {})
    strings = list(project.get("dependencies", [])) if isinstance(project, dict) else []
    if isinstance(groups, dict):
        strings += [item for group in groups.values() for item in group if isinstance(item, str)]
    return strings


def _major_bounds(version: Version) -> str:
    if version.major == 0:
        return f">={version},<0.{version.minor + 1}.0"
    return f">={version},<{version.major + 1}.0.0"


def _bare(requirement: Requirement) -> str:
    extras = f"[{','.join(sorted(requirement.extras))}]" if requirement.extras else ""
    return f"{requirement.name}{extras}"


def raise_python_bounds(project_dir: Path) -> None:
    """Bounds removed, latest versions resolved, then "same major" bounds put back."""
    pyproject_path = project_dir / "pyproject.toml"
    text = pyproject_path.read_text()
    bounded = [
        Requirement(raw)
        for raw in _requirement_strings(tomllib.loads(text))
        if Requirement(raw).specifier and Requirement(raw).url is None
    ]
    for requirement in bounded:
        text = text.replace(f'"{requirement}"', f'"{_bare(requirement)}"')
    pyproject_path.write_text(text)
    run(["uv", "lock", "--upgrade"], project_dir)
    locked = tomllib.loads((project_dir / "uv.lock").read_text()).get("package", [])
    versions = {canonicalize_name(package["name"]): package["version"] for package in locked}
    for requirement in bounded:
        version = Version(versions[canonicalize_name(requirement.name)])
        text = text.replace(
            f'"{_bare(requirement)}"', f'"{_bare(requirement)}{_major_bounds(version)}"'
        )
    pyproject_path.write_text(text)


def _major(version: str) -> int:
    return int(version.split(".")[0])


def _ignored_pnpm_dependencies(project_dir: Path) -> set[str]:
    workspace_path = project_dir / PNPM_WORKSPACE
    workspace = yaml.safe_load(workspace_path.read_text()) if workspace_path.exists() else {}
    update_config = (workspace or {}).get("updateConfig", {}) or {}
    return set(update_config.get("ignoreDependencies", []) or [])


def update_pnpm(project_dir: Path, *, allow_major: bool) -> None:
    """Exact versions bumped by `pnpm add`, majors only with `allow_major`."""
    completed = subprocess.run(
        ["pnpm", "outdated", "--format", "json"],
        cwd=project_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    outdated = json.loads(completed.stdout or "{}")
    ignored = _ignored_pnpm_dependencies(project_dir)
    upgrades: dict[bool, list[str]] = {True: [], False: []}
    held_back = []
    for name, info in outdated.items():
        if name in ignored:
            continue
        if allow_major or _major(info["latest"]) == _major(info["current"]):
            upgrades[info.get("dependencyType") == DEV_DEPENDENCY_TYPE].append(
                f"{name}@{info['latest']}"
            )
        else:
            held_back.append(f"{name} {info['current']} → {info['latest']}")
    for is_dev, packages in upgrades.items():
        if packages:
            run(["pnpm", "add", *(["--save-dev"] if is_dev else []), *packages], project_dir)
    if held_back:
        print("Majors available (kiln update --major): " + ", ".join(held_back))

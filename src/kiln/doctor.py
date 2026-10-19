"""`kiln doctor`: diagnosis of this machine and the current repo, with the command that fixes.

Three levels: ✓ fine, ! to look at (optional tool missing, repo behind), ✗ blocking (required
tool missing, gh logged out). The command fails while a blocking point remains. Nothing is
changed: each fix is offered, never applied.
"""

import functools
import json
import shutil
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from kiln import ui
from kiln.charter.config import charter_path
from kiln.config import UserConfig, config_path, load_config
from kiln.install import SYSTEM_HINTS
from kiln.shell import INSTALL_HINTS, KilnError
from kiln.stack import ANSWERS_FILE, BACKEND_DIR, Stack, load_stack, read_answers
from kiln.versions import installed_version, latest_release, release_version, upgrade_command

PROBE_TIMEOUT = 5
CLAUDE_SETTINGS = Path.home() / ".claude" / "settings.json"
BASE_PLUGIN = "kiln@kiln"
# Its name before kiln 0.4, until Claude Code applies the catalogue's renames.
LEGACY_BASE_PLUGIN = "base@kiln"
GITHUB_LOGIN_URL = "https://github.com/login/device"
LABEL_WIDTH = 16


class Level(Enum):
    OK = "ok"
    WARN = "to look at"
    FAIL = "blocking"


@dataclass(frozen=True)
class Finding:
    level: Level
    label: str
    detail: str
    fix: str = ""


def run_doctor(cwd: Path) -> None:
    config = load_config()
    root = _repo_root(cwd)
    stack = _stack(root)
    sections = [("Machine", workstation_findings(config, stack))]
    if root is not None:
        sections.append((f"Repo {root.name}", repo_findings(root, stack)))
    for title, findings in sections:
        print(f"\n  {ui.paint(title.upper(), ui.FIRE, bold=True)}")
        for finding in findings:
            print_finding(finding)
    findings = [finding for _, section in sections for finding in section]
    blocking = sum(finding.level is Level.FAIL for finding in findings)
    warnings = sum(finding.level is Level.WARN for finding in findings)
    if blocking:
        raise KilnError(f"{blocking} blocking point(s), {warnings} to look at")
    if warnings:
        print()
        ui.note(f"  Nothing blocking; {warnings} point(s) to look at.")
    else:
        ui.success("All is well.")


def print_finding(finding: Finding) -> None:
    marks = {
        Level.OK: ui.paint("✓", ui.MOSS),
        Level.WARN: ui.paint("!", ui.FIRE, bold=True),
        Level.FAIL: ui.paint("✗", ui.EMBER, bold=True),
    }
    label = ui.paint(f"{finding.label:<{LABEL_WIDTH}}", ui.STONE_LIGHT, bold=True)
    detail = finding.detail if finding.level is Level.OK else ui.paint(finding.detail, ui.FIRE)
    print(f"    {marks[finding.level]} {label}{detail}")
    if finding.fix:
        print(f"      {' ' * LABEL_WIDTH}{ui.paint('→ ' + finding.fix, ui.STONE)}")


# --- Machine ---


def workstation_findings(config: UserConfig, stack: Stack | None) -> list[Finding]:
    system = config.system or "linux"
    findings = [
        _tool("git", required=True, fix=INSTALL_HINTS["git"]),
        _tool("uv", required=True, fix=INSTALL_HINTS["uv"]),
        _github(),
        _tool(
            "pnpm",
            required=stack is not None and stack.pnpm_dir is not None,
            fix=SYSTEM_HINTS["pnpm"][system],
        ),
        _tool(
            "podman",
            required=stack is not None and stack.has_podman,
            fix=SYSTEM_HINTS["podman"][system],
        ),
        _tool(
            "java",
            required=stack is not None and stack.maven_dir is not None,
            fix=SYSTEM_HINTS["java"][system],
            version_command=["java", "-version"],
        ),
        _tool("pre-commit", required=False, fix="kiln install (in a repo)"),
        _kiln_tool(),
        _claude_plugin(),
        _config(config),
    ]
    return findings


def _tool(
    name: str,
    *,
    required: bool,
    fix: str,
    version_command: list[str] | None = None,
) -> Finding:
    if shutil.which(name) is None:
        level = Level.FAIL if required else Level.WARN
        needed = "required by this repo" if required else "missing (useful for some stacks)"
        return Finding(level, name, needed, fix)
    return Finding(Level.OK, name, probe(version_command or [name, "--version"]) or "present")


def _github() -> Finding:
    if shutil.which("gh") is None:
        hint = INSTALL_HINTS["gh"]
        return Finding(Level.WARN, "gh", "missing (kiln new creates the GitHub repo)", hint)
    status = _completed(["gh", "auth", "status"])
    if status is None or status.returncode != 0:
        login = f"gh auth login (enter the code at {GITHUB_LOGIN_URL})"
        return Finding(Level.FAIL, "gh", "logged out", login)
    account = next(
        (
            line.split("account", 1)[1].split()[0]
            for line in (status.stdout + status.stderr).splitlines()
            if "Logged in to" in line and "account" in line
        ),
        "",
    )
    return Finding(Level.OK, "gh", f"logged in{f' ({account})' if account else ''}")


def _kiln_tool() -> Finding:
    current = installed_version()
    latest = _latest_release()
    if latest is None:
        return Finding(Level.OK, "kiln", f"{current} (no published release, or offline)")
    current_version, latest_version = release_version(current.split()[0]), release_version(latest)
    if (
        current_version is not None
        and latest_version is not None
        and current_version < latest_version
    ):
        upgrade = upgrade_command(latest)
        return Finding(Level.WARN, "kiln", f"{current}, {latest} available", upgrade)
    return Finding(Level.OK, "kiln", f"{current} (latest release: {latest})")


def _claude_plugin() -> Finding:
    try:
        settings = json.loads(CLAUDE_SETTINGS.read_text())
    except OSError, ValueError:
        settings = {}
    plugins = settings.get("enabledPlugins", {})
    if plugins.get(BASE_PLUGIN) or plugins.get(LEGACY_BASE_PLUGIN):
        return Finding(Level.OK, "Claude plugin", f"{BASE_PLUGIN} enabled")
    return Finding(
        Level.WARN,
        "Claude plugin",
        f"{BASE_PLUGIN} not enabled on this machine",
        "claude plugin marketplace add antoine-tena/kiln && "
        f"claude plugin install {BASE_PLUGIN} --scope user",
    )


def _config(config: UserConfig) -> Finding:
    if config.system is None:
        return Finding(Level.WARN, "configuration", "system not recorded", "kiln install")
    if not config.code_dir.is_dir():
        return Finding(
            Level.WARN,
            "configuration",
            f"code folder not found: {config.code_dir}",
            f'code_dir = "…" in {config_path()}',
        )
    return Finding(Level.OK, "configuration", f"{config.system}, repos in {config.code_dir}")


# --- Current repo ---


def repo_findings(root: Path, stack: Stack | None) -> list[Finding]:
    findings = [_template(root)]
    if stack is None:
        return findings
    findings.append(_hook(root))
    for directory in stack.python_dirs:
        findings.append(_installed(root / directory / ".venv", f"{directory} (uv)", "uv sync"))
    if stack.pnpm_dir is not None:
        modules = root / stack.pnpm_dir / "node_modules"
        findings.append(_installed(modules, f"{stack.pnpm_dir} (pnpm)", "pnpm install"))
    if stack.has_api:
        env_file = root / BACKEND_DIR / ".env"
        findings.append(
            Finding(Level.OK, "backend/.env", "present")
            if env_file.exists()
            else Finding(Level.FAIL, "backend/.env", "missing", "kiln install")
        )
    return findings


def _template(root: Path) -> Finding:
    if not (root / ANSWERS_FILE).exists():
        if charter_path(root) is not None:
            return Finding(Level.OK, "template", "adopted repo (charter without template)")
        return Finding(Level.WARN, "template", "not a kiln repo", "kiln new, or kiln adopt")
    commit = str(read_answers(root).get("_commit", "?"))
    latest = _latest_release()
    current_version = release_version(commit)
    latest_version = release_version(latest or "")
    if latest_version is None:
        return Finding(Level.OK, "template", commit)
    if current_version is None or current_version < latest_version:
        return Finding(
            Level.WARN,
            "template",
            f"{commit}, {latest} available",
            "kiln update, on a branch (skill /kiln:update)",
        )
    return Finding(Level.OK, "template", f"{commit} (up to date)")


def _hook(root: Path) -> Finding:
    hooks_dir = _completed(["git", "rev-parse", "--git-path", "hooks"], cwd=root)
    path = root / (hooks_dir.stdout.strip() if hooks_dir else ".git/hooks") / "pre-commit"
    if path.exists():
        return Finding(Level.OK, "pre-commit", "hook installed")
    return Finding(Level.WARN, "pre-commit", "hook missing", "kiln install")


def _installed(path: Path, label: str, fix: str) -> Finding:
    if path.exists():
        return Finding(Level.OK, label, "dependencies installed")
    return Finding(Level.WARN, label, "dependencies missing", f"kiln install (or {fix})")


# --- Tools ---


def probe(command: list[str]) -> str:
    """First line of a command's output (stdout, else stderr); empty if it fails."""
    completed = _completed(command)
    if completed is None:
        return ""
    output = (completed.stdout or completed.stderr).strip()
    return output.splitlines()[0] if output else ""


def _completed(
    command: list[str], cwd: Path | None = None
) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            command, cwd=cwd, capture_output=True, text=True, timeout=PROBE_TIMEOUT, check=False
        )
    except subprocess.TimeoutExpired, OSError:
        return None


def _repo_root(cwd: Path) -> Path | None:
    completed = _completed(["git", "rev-parse", "--show-toplevel"], cwd=cwd)
    if completed is None or completed.returncode != 0:
        return None
    return Path(completed.stdout.strip())


@functools.cache
def _latest_release() -> str | None:
    """A single query to GitHub per diagnosis."""
    return latest_release()


def _stack(root: Path | None) -> Stack | None:
    if root is None:
        return None
    try:
        return load_stack(root)
    except KilnError, OSError, ValueError:
        return None

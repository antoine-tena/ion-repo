"""`kiln install`: sets up a machine after the clone, by stack; outside a repo (or with
`--machine`), sets up kiln for the whole machine. Safe to run again."""

import json
import os
import secrets
import shutil
import subprocess
from pathlib import Path

from kiln import ui
from kiln.adopted_names import HOOKS_FILE
from kiln.config import UserConfig, ensure_system, load_config
from kiln.dev.backing import start_backing_services
from kiln.shell import KilnError, require_tools, run, step
from kiln.stack import (
    BACKEND_DIR,
    MAVEN_WRAPPER,
    PNPM_LENIENT_BUILDS,
    Stack,
    answers_if_any,
    load_stack,
)
from kiln.statusline import apply_statusline_settings, ensure_statusline
from kiln.versions import PYPI_NAME

CLAUDE_DIR = Path.home() / ".claude"
CLAUDE_SETTINGS = CLAUDE_DIR / "settings.json"
KNOWN_MARKETPLACES = CLAUDE_DIR / "plugins" / "known_marketplaces.json"
MARKETPLACE = "kiln"
MARKETPLACE_SOURCE = "antoine-tena/kiln"
BASE_PLUGIN = "kiln@kiln"
# Its name before kiln 0.4, until Claude Code applies the catalogue's renames.
LEGACY_BASE_PLUGIN = "base@kiln"

SECRET_KEY_VARIABLE = "DJANGO_SECRET_KEY"
SECRET_KEY_BYTES = 50
ENV_FILE_MODE = 0o600
# A venv script starts `#!/…/.venv/bin/python`: the folder it was created in.
VENV_PYTHON = b"/bin/python"
VENV_SHEBANG_MAX = 4096
PNPM_LOCKFILE = "pnpm-lock.yaml"

# Install hints by system (never pip or docker).
SYSTEM_HINTS: dict[str, dict[str, str]] = {
    "java": {
        "linux": "sudo apt install openjdk-25-jdk",
        "wsl": "sudo apt install openjdk-25-jdk",
        "macos": "brew install openjdk@25",
    },
    # The Maven wrapper unpacks its distribution with unzip.
    "unzip": {
        "linux": "sudo apt install unzip",
        "wsl": "sudo apt install unzip",
        "macos": "unzip ships with macOS",
    },
    "pnpm": {
        "linux": "corepack enable pnpm (Node 24, from mise or the package manager)",
        "wsl": "corepack enable pnpm (Node 24, from mise or apt)",
        "macos": "brew install node@24 && corepack enable pnpm",
    },
    "podman": {
        "linux": "sudo apt install podman",
        "wsl": "sudo apt install podman (inside WSL, not Podman Desktop on Windows)",
        "macos": "brew install podman && podman machine init && podman machine start",
    },
}


def install_project(root: Path) -> None:
    config = ensure_system(load_config())
    stack = load_stack(root)
    _require_stack_tools(stack, config)
    _ensure_uv_tool("pre-commit", "pre-commit-uv")
    if stack.has_podman:
        _ensure_uv_tool("podman-compose")
    for directory in stack.python_dirs:
        step(f"{directory}: Python dependencies")
        run(sync_command(root / directory / ".venv"), root / directory)
    if stack.maven_dir is not None:
        step(f"{stack.maven_dir}: Maven and dependencies (wrapper)")
        run([MAVEN_WRAPPER, "-B", "-q", "-DskipTests", "package"], root / stack.maven_dir)
    if stack.has_api:
        step("backend: .env")
        ensure_env_file(root / BACKEND_DIR)
    if stack.backend == "django":
        start_backing_services(root)
        step("backend: migrations")
        run(["uv", "run", "python", "manage.py", "migrate"], root / BACKEND_DIR)
    if stack.pnpm_dir is not None:
        step(f"{stack.pnpm_dir}: pnpm dependencies")
        run(pnpm_install_command(root / stack.pnpm_dir), root / stack.pnpm_dir)
    step("git guards (pre-commit) and status line")
    install_git_hooks(root)
    apply_statusline_settings(root)
    ensure_statusline(config)
    command_name = answers_if_any(root).get("name", "<command>")
    ui.success(f"Ready. Run the project: {_launch_hint(stack, command_name)}")


def install_git_hooks(root: Path) -> None:
    """pre-commit's hook, only with its configuration: without it, the hook refuses every
    commit (an adopted repo may have none)."""
    if not (root / HOOKS_FILE).is_file():
        print(f"no {HOOKS_FILE}: git hooks not installed.")
        return
    run(["pre-commit", "install"], root)


def install_machine() -> None:
    """kiln in every repo and every Claude session of the machine: the CLI as a uv tool, the
    kiln plugin at user scope, the machine settings. Only what is missing is done."""
    config = ensure_system(load_config())
    require_tools("uv")
    if shutil.which("kiln") is None:
        step("kiln command (uv tool)")
        run(["uv", "tool", "install", PYPI_NAME], Path.cwd())
    if shutil.which("claude") is None:
        ui.note("Claude Code not found: install it, then run kiln install again for the plugins.")
    else:
        if MARKETPLACE not in _json_file(KNOWN_MARKETPLACES):
            step("kiln catalogue of Claude Code plugins")
            run(["claude", "plugin", "marketplace", "add", MARKETPLACE_SOURCE], Path.cwd())
        if not kiln_plugin_enabled():
            step(f"{BASE_PLUGIN} plugin, for every Claude session")
            run(["claude", "plugin", "install", BASE_PLUGIN, "--scope", "user"], Path.cwd())
    ensure_statusline(config)
    ui.success("kiln is set up on this machine. Check it: kiln doctor")


def kiln_plugin_enabled() -> bool:
    plugins = _json_file(CLAUDE_SETTINGS).get("enabledPlugins")
    return isinstance(plugins, dict) and bool(
        plugins.get(BASE_PLUGIN) or plugins.get(LEGACY_BASE_PLUGIN)
    )


def _json_file(path: Path) -> dict[str, object]:
    try:
        content = json.loads(path.read_text())
    except OSError, ValueError:
        return {}
    return content if isinstance(content, dict) else {}


def _launch_hint(stack: Stack, command_name: object) -> str:
    if stack.dev_commands():
        return "kiln dev"
    if stack.maven_dir is not None:
        return f"cd {stack.maven_dir} && {MAVEN_WRAPPER} verify"
    return f"cd backend && uv run {command_name} --help"


def _require_stack_tools(stack: Stack, config: UserConfig) -> None:
    require_tools("git", "uv")
    needed = (
        (["pnpm"] if stack.pnpm_dir else [])
        + (["podman"] if stack.has_podman else [])
        + (["java", "unzip"] if stack.maven_dir else [])
    )
    missing = [tool for tool in needed if shutil.which(tool) is None]
    if missing:
        system = config.system or "linux"
        hints = "\n".join(f"  {tool}: {SYSTEM_HINTS[tool][system]}" for tool in missing)
        raise KilnError(f"missing tools:\n{hints}")
    if stack.has_podman and config.system == "macos":
        _require_podman_machine()


def _require_podman_machine() -> None:
    completed = subprocess.run(["podman", "info"], capture_output=True, check=False)
    if completed.returncode != 0:
        raise KilnError("podman does not answer: podman machine start (or podman machine init)")


def _ensure_uv_tool(tool: str, *extras: str) -> None:
    """Command-line tool installed by uv (never pip), with its plugins."""
    if shutil.which(tool) is not None and not extras:
        return
    step(f"{tool} tool (uv tool)")
    with_options = [option for extra in extras for option in ("--with", extra)]
    run(["uv", "tool", "install", tool, *with_options], Path.cwd())


def sync_command(venv: Path) -> list[str]:
    """`uv sync --locked`, reinstalling every package when the venv was moved: uv sees them
    installed and would leave their scripts calling the old folder's Python."""
    command = ["uv", "sync", "--locked"]
    return [*command, "--reinstall"] if moved_from(venv) is not None else command


def moved_from(venv: Path) -> Path | None:
    """The folder a virtual environment was created in, when the repo has moved since (its
    scripts then fail to spawn: `uv run mypy`); None when it is in place or cannot tell."""
    for script in sorted((venv / "bin").glob("*")):
        if not script.is_file() or script.is_symlink():
            continue
        with script.open("rb") as handle:
            first_line = handle.readline(VENV_SHEBANG_MAX).strip()
        if not (first_line.startswith(b"#!") and first_line.endswith(VENV_PYTHON)):
            continue
        created_in = Path(first_line[2:].decode(errors="replace")).parent.parent
        same_place = os.path.realpath(created_in) == os.path.realpath(venv)
        return None if same_place else created_in
    return None


def pnpm_install_command(directory: Path) -> list[str]:
    """Frozen to the lockfile when there is one; without it (a repo that never committed one),
    `--frozen-lockfile` fails with ERR_PNPM_NO_LOCKFILE: a plain install creates it."""
    if (directory / PNPM_LOCKFILE).is_file():
        return ["pnpm", "install", "--frozen-lockfile", PNPM_LENIENT_BUILDS]
    return ["pnpm", "install", PNPM_LENIENT_BUILDS]


def pnpm_behind(directory: Path) -> bool:
    """node_modules missing, or installed from another pnpm-lock.yaml than the folder's (a
    lockfile merged without `pnpm install`): the checks would run other versions than the CI."""
    lockfile = directory / PNPM_LOCKFILE
    installed = directory / "node_modules" / ".pnpm" / "lock.yaml"
    if not (directory / "node_modules").is_dir():
        return True
    if not (lockfile.is_file() and installed.is_file()):
        return False
    return lockfile.read_bytes() != installed.read_bytes()


def ensure_env_file(backend_dir: Path) -> None:
    """backend/.env drawn from .env.example, with a local secret key; kept if it exists."""
    env_file = backend_dir / ".env"
    if env_file.exists():
        print("backend/.env already exists, kept.")
        return
    example = backend_dir / ".env.example"
    # An adopted repo may have none: nothing to draw from, the backend reads its own settings.
    if not example.exists():
        print("backend/.env.example missing, no backend/.env created.")
        return
    template_lines = example.read_text().splitlines()
    secret_key = secrets.token_urlsafe(SECRET_KEY_BYTES)
    env_lines = [
        f"{SECRET_KEY_VARIABLE}={secret_key}"
        if line.startswith(f"{SECRET_KEY_VARIABLE}=")
        else line
        for line in template_lines
    ]
    env_file.write_text("\n".join(env_lines) + "\n")
    os.chmod(env_file, ENV_FILE_MODE)
    print("backend/.env created with a local secret key.")

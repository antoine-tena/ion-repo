"""`kiln install`: sets up a machine after the clone, by stack; safe to run again."""

import os
import secrets
import shutil
import subprocess
from pathlib import Path

from kiln import ui
from kiln.config import UserConfig, ensure_system, load_config
from kiln.shell import KilnError, require_tools, run, step
from kiln.stack import BACKEND_DIR, MAVEN_WRAPPER, Stack, answers_if_any, load_stack
from kiln.statusline import apply_statusline_settings, ensure_statusline

SECRET_KEY_VARIABLE = "DJANGO_SECRET_KEY"
SECRET_KEY_BYTES = 50
ENV_FILE_MODE = 0o600

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
        run(["uv", "sync", "--locked"], root / directory)
    if stack.maven_dir is not None:
        step(f"{stack.maven_dir}: Maven and dependencies (wrapper)")
        run([MAVEN_WRAPPER, "-B", "-q", "-DskipTests", "package"], root / stack.maven_dir)
    if stack.has_api:
        step("backend: .env")
        ensure_env_file(root / BACKEND_DIR)
    if stack.backend == "django":
        step("backend: migrations")
        run(["uv", "run", "python", "manage.py", "migrate"], root / BACKEND_DIR)
    if stack.pnpm_dir is not None:
        step(f"{stack.pnpm_dir}: pnpm dependencies")
        run(["pnpm", "install", "--frozen-lockfile"], root / stack.pnpm_dir)
    step("git guards (pre-commit) and status line")
    run(["pre-commit", "install"], root)
    apply_statusline_settings(root)
    ensure_statusline(config)
    command_name = answers_if_any(root).get("name", "<command>")
    ui.success(f"Ready. Run the project: {_launch_hint(stack, command_name)}")


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


def ensure_env_file(backend_dir: Path) -> None:
    """backend/.env drawn from .env.example, with a local secret key; kept if it exists."""
    env_file = backend_dir / ".env"
    if env_file.exists():
        print("backend/.env already exists, kept.")
        return
    template_lines = (backend_dir / ".env.example").read_text().splitlines()
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

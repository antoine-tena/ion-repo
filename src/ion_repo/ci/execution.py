"""Running the jobs of `kiln ci`: steps in series, one log per job, lanes in parallel.

As on GitHub, a job stops at its first failed step (except a `should_always_run` step), and a
failed job does not prevent the next ones. The `back` lane (pytest, the longest) runs beside the
`front` lane; within a lane, jobs follow one another, so that two never write to the same files
(generated types, frontend build).
"""

import os
import platform
import shlex
import shutil
import subprocess
import threading
import time
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from ion_repo.ci.jobs import Plan, Step
from ion_repo.ci.services import running_services
from ion_repo.ci.verdict import JobOutcome

LOG_TAIL_LINES = 40
# Machine variables that would run the worktree's tools with another one's environment.
INHERITED_TO_DROP = ("VIRTUAL_ENV", "DATABASE_URL", "REDIS_URL", "PYTHONPATH")
# Chrome for Lighthouse (CHROME_PATH): the machine's, otherwise Playwright's Chromium. On GitHub,
# the runner image ships one; on a machine, lhci fails without it.
CHROME_NAMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
PLAYWRIGHT_BROWSERS = Path.home() / ".cache" / "ms-playwright"
# Under WSL, chrome-launcher (Lighthouse) thinks it runs Windows' Chrome and passes it a
# Windows-style `--user-data-dir`: a Linux Chromium turns it into a folder
# "C:\Users\…\lighthouse.N" in the current folder. This launcher translates the path back.
WSL_CHROME = Path.home() / ".cache" / "kiln" / "chrome-wsl"
WSL_CHROME_SCRIPT = """#!/usr/bin/env bash
# Written by kiln ci: Linux Chromium launched by chrome-launcher under WSL (see execution.py).
args=()
for arg in "$@"; do
  case "$arg" in
    --user-data-dir=[A-Za-z]:\\\\*)
      args+=("--user-data-dir=$(wslpath -u "${arg#--user-data-dir=}")") ;;
    *) args+=("$arg") ;;
  esac
done
exec @CHROME@ "${args[@]}"
"""
_print_lock = threading.Lock()


@dataclass(frozen=True)
class Workspace:
    """The worktree of the replayed commit, the logs folder and the containers' prefix."""

    root: Path
    log_dir: Path
    container_prefix: str


def say(message: str) -> None:
    with _print_lock:
        print(message, flush=True)


def base_env(extra: Mapping[str, str]) -> dict[str, str]:
    env = {key: value for key, value in os.environ.items() if key not in INHERITED_TO_DROP}
    if "CHROME_PATH" not in env and (chrome := find_chrome()):
        env["CHROME_PATH"] = wsl_chrome_launcher(chrome) if is_wsl() else chrome
    return {**env, "CI": "true", **extra}


def find_chrome() -> str | None:
    """The machine's Chrome, otherwise the latest Playwright Chromium; None if there is none."""
    for name in CHROME_NAMES:
        if path := shutil.which(name):
            return path
    builds = sorted(
        PLAYWRIGHT_BROWSERS.glob("chromium-*/chrome-linux*/chrome"),
        key=lambda chrome: int(chrome.parts[-3].removeprefix("chromium-")),
    )
    return str(builds[-1]) if builds else None


def is_wsl() -> bool:
    return "microsoft" in platform.release().lower()


def wsl_chrome_launcher(chrome: str) -> str:
    """Path of the launcher that translates the Windows-style profile back for `chrome`."""
    script = WSL_CHROME_SCRIPT.replace("@CHROME@", shlex.quote(chrome))
    if not WSL_CHROME.exists() or WSL_CHROME.read_text() != script:
        WSL_CHROME.parent.mkdir(parents=True, exist_ok=True)
        WSL_CHROME.write_text(script)
        WSL_CHROME.chmod(0o755)
    return str(WSL_CHROME)


def run_lanes(plans: list[Plan], workspace: Workspace) -> list[JobOutcome]:
    """Runs each lane in its thread; returns the outcomes in the order of the plans."""
    lanes: dict[str, list[Plan]] = {}
    for plan in plans:
        lanes.setdefault(plan.lane, []).append(plan)
    with ThreadPoolExecutor(max_workers=len(lanes) or 1) as executor:
        futures = [executor.submit(_run_lane, lane, workspace) for lane in lanes.values()]
        outcomes = {outcome.name: outcome for future in futures for outcome in future.result()}
    return [outcomes[plan.job.name] for plan in plans]


def _run_lane(plans: list[Plan], workspace: Workspace) -> list[JobOutcome]:
    return [run_job(plan, workspace) for plan in plans]


def run_job(plan: Plan, workspace: Workspace) -> JobOutcome:
    name = plan.job.name
    log_path = workspace.log_dir / f"{name}.log"
    say(f"[{name}] started (log: {log_path})")
    failed_step = ""
    try:
        with running_services(plan.services, f"{workspace.container_prefix}-{name}") as urls:
            env = base_env({**plan.env, **urls})
            for step in plan.steps:
                if failed_step and not step.should_always_run:
                    continue
                if not run_step(step, workspace.root, env, log_path, name):
                    failed_step = failed_step or step.label
    except Exception as error:  # a service that does not start fails the job, not the CI
        _append(log_path, f"\n!! {error}\n")
        failed_step = failed_step or f"services : {error}"
    say(f"[{name}] {'FAILED at "' + failed_step + '"' if failed_step else 'ok'}")
    if failed_step:
        say(_tail(log_path))
    return JobOutcome(name, not failed_step, failed_step)


def run_step(step: Step, root: Path, env: Mapping[str, str], log_path: Path, job: str) -> bool:
    started = time.monotonic()
    _append(log_path, f"\n==> {step.label} ({step.directory})\n$ {step.command}\n")
    with log_path.open("a") as log_file:
        completed = subprocess.run(
            ["bash", "-e", "-c", step.command],
            cwd=root / step.directory,
            env=dict(env),
            stdout=log_file,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            check=False,
        )
    elapsed = round(time.monotonic() - started)
    status = "ok" if completed.returncode == 0 else f"failed (code {completed.returncode})"
    say(f"[{job}] {step.label} : {status}, {elapsed} s")
    return completed.returncode == 0


def _append(log_path: Path, text: str) -> None:
    with log_path.open("a") as log_file:
        log_file.write(text)


def _tail(log_path: Path) -> str:
    lines = log_path.read_text(errors="replace").splitlines()[-LOG_TAIL_LINES:]
    return "\n".join(f"    {line}" for line in lines)

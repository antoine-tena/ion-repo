"""What the grid does not know, told to ion-repo with the user's yes (T-38).

`ion repo score` ends with what it met that the grid does not cover (a stack, a known package) and
the rules that misfire (a waiver renewed again and again). In a terminal, it then offers to tell
ion-repo, showing exactly the lines that would leave: nothing else, never code, paths or a private
name (a package is only named when it is one of `NOTABLE_PACKAGES`). One issue per gap, not per
user: an open issue with the same title gets a 👍 instead. A "no" holds for the repo; a line told
once is not offered again (both in the repo's local git config, never committed). Without `gh`,
a prefilled issue link. A count is a signal, never a decision: a practice enters the grid by the
doctrine (maturity, sources), so a flood of reports cannot poison it.
"""

import json
import shutil
import subprocess
import urllib.parse
from collections.abc import Callable
from pathlib import Path

from ion_repo import ui
from ion_repo.grid.score import Report
from ion_repo.versions import installed_version

ION_REPO_REPO = "antoine-tena/ion-repo"
CONSENT_KEY = "kiln.report-gaps"
TOLD_KEY = "kiln.reported-gap"
NEVER = "never"
GH_TIMEOUT = 20

Ask = Callable[[str], str]


def offer(root: Path, report: Report, ask: Ask | None) -> None:
    if ask is None or _git_config(root, CONSENT_KEY) == NEVER:
        return
    told = set(_git_config_all(root, TOLD_KEY))
    lines = [line for line in (*report.uncovered, *report.misfired) if line not in told]
    if not lines:
        return
    print(f"\n  {ui.paint('Tell ion-repo?', ui.FIRE, bold=True)} It opens an issue with this only:")
    for line in lines:
        print(ui.paint(f"    {line}", ui.STONE_LIGHT))
    reply = ask("  [y]es, [n]ot now, ne[v]er for this repo: ").strip().lower()
    if reply.startswith("v"):
        _set_git_config(root, CONSENT_KEY, NEVER)
        return
    if not reply.startswith("y"):
        return
    for line in lines:
        ui.success(tell(line))
        subprocess.run(["git", "config", "--add", TOLD_KEY, line], cwd=root, check=False)


def title_of(line: str) -> str:
    subject = line.split(":", 1)[0]
    return f"Grid misfire: {subject}" if "waived again" in line else f"Grid gap: {subject}"


def tell(line: str) -> str:
    """Opens the issue, or 👍 the open one with the same title; says what was done."""
    title = title_of(line)
    body = (
        f"{line}\n\nReported by `ion repo score` (ion-repo {installed_version()}), "
        "with the user's yes."
    )
    if shutil.which("gh") is None:
        return f"{title}: open {issue_link(title, body)}"
    found = _gh(
        "issue",
        "list",
        "-R",
        ION_REPO_REPO,
        "--state",
        "open",
        "--search",
        f'in:title "{title}"',
        "--json",
        "number,title",
    )
    if found.returncode != 0:
        return f"{title}: open {issue_link(title, body)}"
    same = [issue for issue in json.loads(found.stdout or "[]") if issue["title"] == title]
    if same:
        number = same[0]["number"]
        _gh(
            "api",
            "-X",
            "POST",
            f"repos/{ION_REPO_REPO}/issues/{number}/reactions",
            "-f",
            "content=+1",
        )
        return f"{title}: 👍 on #{number}, already reported"
    created = _gh("issue", "create", "-R", ION_REPO_REPO, "--title", title, "--body", body)
    if created.returncode != 0:
        return f"{title}: open {issue_link(title, body)}"
    return f"{title}: {created.stdout.strip()}"


def issue_link(title: str, body: str) -> str:
    query = urllib.parse.urlencode({"title": title, "body": body})
    return f"https://github.com/{ION_REPO_REPO}/issues/new?{query}"


def _gh(*args: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["gh", *args], capture_output=True, text=True, timeout=GH_TIMEOUT, check=False
        )
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(["gh", *args], 1, "", "timeout")


def _git_config(root: Path, key: str) -> str:
    return subprocess.run(
        ["git", "config", "--get", key], cwd=root, capture_output=True, text=True, check=False
    ).stdout.strip()


def _git_config_all(root: Path, key: str) -> list[str]:
    output = subprocess.run(
        ["git", "config", "--get-all", key], cwd=root, capture_output=True, text=True, check=False
    ).stdout
    return output.splitlines()


def _set_git_config(root: Path, key: str, value: str) -> None:
    subprocess.run(["git", "config", key, value], cwd=root, check=False)

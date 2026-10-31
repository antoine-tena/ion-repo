"""Creation of the GitHub repo, protection of main and develop, invitations of the team."""

import json
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

from ion_repo import ui
from ion_repo.shell import KilnError, run, step

LOGIN_URL = "https://github.com/login/device"
LOGIN_TIMEOUT = 5
INSTALL_GH = "https://cli.github.com"
MAIN_RULESET_NAME = "Protection main"
DEVELOP_RULESET_NAME = "Protection develop"
REPOSITORY_ADMIN_ROLE_ID = 5

# main keeps the single initial commit: locked, nobody pushes to it, except the admin who may
# rewrite it. develop, the work and integration branch, can be neither deleted nor rewritten.
DEVELOP_RULESET = {
    "name": DEVELOP_RULESET_NAME,
    "target": "branch",
    "enforcement": "active",
    "conditions": {"ref_name": {"include": ["refs/heads/develop"], "exclude": []}},
    "rules": [{"type": "deletion"}, {"type": "non_fast_forward"}],
}
MAIN_RULESET = {
    "name": MAIN_RULESET_NAME,
    "target": "branch",
    "enforcement": "active",
    "conditions": {
        "ref_name": {"include": ["refs/heads/main"], "exclude": []},
    },
    "bypass_actors": [
        {
            "actor_id": REPOSITORY_ADMIN_ROLE_ID,
            "actor_type": "RepositoryRole",
            "bypass_mode": "always",
        },
    ],
    "rules": [{"type": "deletion"}, {"type": "update"}],
}


def login() -> str | None:
    """GitHub account logged in to gh; None without gh, login or network."""
    if shutil.which("gh") is None:
        return None
    try:
        found = subprocess.run(
            ["gh", "api", "user", "--jq", ".login"],
            capture_output=True,
            text=True,
            timeout=LOGIN_TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired, OSError:
        return None
    if found.returncode != 0:
        return None
    return found.stdout.strip() or None


def can_publish() -> bool:
    """Can GitHub be reached to create the repo? Without gh, or outside a terminal without a
    login, kiln goes without and says so (`kiln publish` will do it later); in a terminal, the
    login is offered."""
    if shutil.which("gh") is None:
        ui.note(f"GitHub: no gh, repo not created. Later: {INSTALL_GH}, then kiln publish.")
        return False
    if _is_logged_in():
        return True
    if not sys.stdin.isatty():
        ui.note("GitHub: gh is not logged in, repo not created. Later: kiln publish.")
        return False
    ensure_logged_in()
    return True


def ensure_logged_in() -> None:
    """Checks gh's login before generating anything; in a terminal, offers it."""
    if _is_logged_in():
        return
    if not sys.stdin.isatty():
        raise KilnError(
            f"gh is not logged in to GitHub: run `gh auth login --web` ({LOGIN_URL}), "
            "or `kiln new … --no-github`"
        )
    step(f"GitHub: login (open {LOGIN_URL} and enter the code shown)")
    run(["gh", "auth", "login", "--web", "--git-protocol", "https"], Path.cwd(), live=True)
    if not _is_logged_in():
        raise KilnError(f"GitHub login did not complete: try again at {LOGIN_URL}")


def _is_logged_in() -> bool:
    status = subprocess.run(["gh", "auth", "status"], capture_output=True, check=False)
    return status.returncode == 0


def publish(root: Path, repository: str, team_logins: list[str]) -> None:
    step(f"GitHub: private repo {repository}")
    run(["gh", "repo", "create", repository, "--private", "--source", "."], root)
    run(["git", "push", "-q", "-u", "origin", "main", "develop"], root)
    run(["gh", "repo", "edit", repository, "--default-branch", "develop"], root)
    step("GitHub: protection of main and develop")
    _post_ruleset(root, repository, MAIN_RULESET)
    _post_ruleset(root, repository, DEVELOP_RULESET)
    step("GitHub: security alerts and fixes (Dependabot)")
    _enable_security_updates(root, repository)
    owner = repository.split("/")[0]
    for login in team_logins:
        if login != owner:
            step(f"GitHub: inviting {login}")
            _gh_put(root, f"repos/{repository}/collaborators/{login}", "permission=push")


def _gh_put(root: Path, endpoint: str, *fields: str) -> None:
    field_options = [option for field in fields for option in ("-f", field)]
    run(["gh", "api", "-X", "PUT", endpoint, *field_options, "--silent"], root)


def _enable_security_updates(root: Path, repository: str) -> None:
    """Dependabot only offers security fixes; the rest goes through kiln update."""
    _gh_put(root, f"repos/{repository}/vulnerability-alerts")
    _gh_put(root, f"repos/{repository}/automated-security-fixes")


def _post_ruleset(root: Path, repository: str, ruleset: Mapping[str, object]) -> None:
    completed = subprocess.run(
        ["gh", "api", "-X", "POST", f"repos/{repository}/rulesets", "--input", "-", "--silent"],
        cwd=root,
        input=json.dumps(ruleset),
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise KilnError("GitHub refused to create the ruleset")

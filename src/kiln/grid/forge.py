"""The forge's settings of a repo, read through the CLI already logged in (`gh`), never a token.

What a repo's files cannot say: the protection of its default branch, secret scanning, Dependabot
alerts, private vulnerability reporting. `kiln score` reads them when `gh` is installed and
logged in with admin rights on the repo, and leaves their rules out otherwise ("unknown"), never
a failure for lack of a token. The token stays `gh`'s: kiln neither reads, stores nor prints it.
A read is cached a day per repo (`--online` reads again), and skipped in CI: a setting's detail
never reaches a public log, only the score and the rule IDs leave the machine.
"""

import datetime
import json
import os
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from pathlib import Path

UNKNOWN = "GitHub settings unknown: gh logged in with admin rights on the repo reads them"
CACHE_DAYS = 1
GH_TIMEOUT = 10
GITHUB_REMOTE = re.compile(r"github\.com[:/]([\w.-]+)/([\w.-]+?)(?:\.git)?/?$")


@dataclass(frozen=True)
class Settings:
    slug: str  # owner/repo
    default_branch: str
    public: bool
    merge_commits: bool  # the repo merges with merge commits (so no linear history to require)
    branch_rules: tuple[str, ...]  # rule types protecting the default branch
    secret_scanning: bool | None  # None: not offered to this repo (private without GHAS)
    push_protection: bool | None
    vulnerability_alerts: bool | None
    security_updates: bool | None
    private_reporting: bool | None
    code_scanning: bool | None
    read: str = ""  # the day it was read

    def page(self, section: str) -> str:
        """The direct link to a page of the repo's settings."""
        return f"https://github.com/{self.slug}/settings/{section}"


def github_slug(root: Path) -> str | None:
    """`owner/repo` of the `origin` remote on GitHub, None elsewhere."""
    try:
        url = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        ).stdout.strip()
    except OSError, subprocess.TimeoutExpired:
        return None
    found = GITHUB_REMOTE.search(url)
    return f"{found[1]}/{found[2]}" if found else None


# Turned off by the tests and in CI, refreshed by `--online`.
ENABLED = not os.environ.get("CI")
REFRESH = False
_read: dict[str, Settings | None] = {}


def settings(root: Path) -> Settings | None:
    """The settings of the repo's GitHub project; None when they cannot be read."""
    slug = github_slug(root)
    if not ENABLED or slug is None or shutil.which("gh") is None:
        return None
    if slug not in _read:
        _read[slug] = _cached(slug)
    return _read[slug]


def _cache_path(slug: str) -> Path:
    base = os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache"
    return Path(base) / "kiln" / "forge" / f"{slug.replace('/', '__')}.json"


def _cached(slug: str) -> Settings | None:
    path = _cache_path(slug)
    today = datetime.date.today()
    if not REFRESH:
        try:
            data = json.loads(path.read_text())
            if today - datetime.date.fromisoformat(data["read"]) < datetime.timedelta(CACHE_DAYS):
                data["branch_rules"] = tuple(data["branch_rules"])
                return Settings(**data)
        except OSError, ValueError, KeyError, TypeError:
            pass
    found = _fetch(slug)
    if found is not None:
        found = Settings(**{**asdict(found), "read": today.isoformat()})
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(found)))
    return found


def _api(path: str) -> tuple[int, object]:
    """`gh api`: (0, body) on success, (HTTP status, None) on an error answer, (-1, None) when
    gh could not ask (not logged in, offline)."""
    try:
        answer = subprocess.run(
            ["gh", "api", path],
            capture_output=True,
            text=True,
            timeout=GH_TIMEOUT,
            check=False,
        )
    except OSError, subprocess.TimeoutExpired:
        return -1, None
    if answer.returncode == 0:
        try:
            return 0, json.loads(answer.stdout) if answer.stdout.strip() else None
        except ValueError:
            return 0, None
    status = re.search(r"HTTP (\d{3})", answer.stderr)
    return (int(status[1]) if status else -1), None


def _fetch(slug: str) -> Settings | None:
    code, repo = _api(f"repos/{slug}")
    if code != 0 or not isinstance(repo, dict):
        return None
    if not (repo.get("permissions") or {}).get("admin"):
        return None  # the security settings answer their admins only
    branch = str(repo.get("default_branch") or "main")
    paths = {
        "rules": f"repos/{slug}/rules/branches/{branch}",
        "protection": f"repos/{slug}/branches/{branch}/protection",
        "alerts": f"repos/{slug}/vulnerability-alerts",
        "fixes": f"repos/{slug}/automated-security-fixes",
        "reporting": f"repos/{slug}/private-vulnerability-reporting",
        "scanning": f"repos/{slug}/code-scanning/default-setup",
    }
    with ThreadPoolExecutor(len(paths)) as pool:
        answers = dict(zip(paths, pool.map(_api, paths.values()), strict=True))
    security = repo.get("security_and_analysis") or {}

    def status(key: str) -> bool | None:
        value = security.get(key)
        return value.get("status") == "enabled" if isinstance(value, dict) else None

    def enabled(name: str) -> bool | None:
        code, body = answers[name]
        return bool(body.get("enabled")) if code == 0 and isinstance(body, dict) else None

    alerts_code = answers["alerts"][0]
    scanning_code, scanning = answers["scanning"]
    return Settings(
        slug=slug,
        default_branch=branch,
        public=repo.get("visibility") == "public",
        merge_commits=bool(repo.get("allow_merge_commit", True)),
        branch_rules=_branch_rules(*answers["rules"], *answers["protection"]),
        secret_scanning=status("secret_scanning"),
        push_protection=status("secret_scanning_push_protection"),
        vulnerability_alerts={0: True, 404: False}.get(alerts_code),
        security_updates=enabled("fixes"),
        private_reporting=enabled("reporting"),
        code_scanning=(
            scanning.get("state") == "configured"
            if scanning_code == 0 and isinstance(scanning, dict)
            else None
        ),
    )


# A classic branch protection, said in the rule types of rulesets.
PROTECTION_RULES = {
    "allow_force_pushes": "non_fast_forward",
    "allow_deletions": "deletion",
}


def _branch_rules(
    rules_code: int, rules: object, protection_code: int, protection: object
) -> tuple[str, ...]:
    found = set()
    if rules_code == 0 and isinstance(rules, list):
        found |= {str(rule.get("type")) for rule in rules if isinstance(rule, dict)}
    if protection_code == 0 and isinstance(protection, dict):
        found |= {
            rule
            for key, rule in PROTECTION_RULES.items()
            if not (protection.get(key) or {}).get("enabled")
        }
        if (protection.get("required_linear_history") or {}).get("enabled"):
            found.add("required_linear_history")
        if protection.get("required_pull_request_reviews"):
            found.add("pull_request")
    return tuple(sorted(found))

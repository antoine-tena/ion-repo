"""Converters of `kiln fix`: supply chain and CI (T-127).

Each edits text in place, line by line, so that comments and layout stay as the repo wrote
them; YAML is only parsed to read, never dumped back."""

import json
import re
from pathlib import PurePosixPath

import yaml  # brought by copier

from kiln.grid.detectors import CONTAINER_FILES, WORKFLOWS
from kiln.grid.facts import Repo
from kiln.grid.fixers import Fixer, register, resolve
from kiln.stack import PNPM_LENIENT_BUILDS

COOLDOWN_DAYS = 7
DEPENDABOT = ".github/dependabot.yml"
ACTIONS = ("**/action.yml", "**/action.yaml")
USES = re.compile(
    r"""^(?P<head>\s*-?\s*uses:\s*)(?P<quote>['"]?)(?P<target>(?!\./|docker://)[^@\s'"]+)"""
    r"""@(?P<ref>[^\s'"#]+)(?P=quote)(?P<tail>.*)$"""
)
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


def _write(repo: Repo, name: str, text: str) -> None:
    path = repo.root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def pin_actions(repo: Repo) -> list[str]:
    """`uses: owner/repo@v4` → `uses: owner/repo@<sha> # v4.2.2` (the exact version on that
    commit, as pinact writes it), reusable workflows included."""
    changed = []
    files = repo.matching(*WORKFLOWS, *ACTIONS)
    for name in files:
        lines = repo.text(name).splitlines(keepends=True)
        edited = False
        for index, line in enumerate(lines):
            found = USES.match(line.rstrip("\n"))
            if not found or FULL_SHA.match(found["ref"]):
                continue
            owner_repo = "/".join(found["target"].split("/")[:2])
            sha = resolve.commit_of(owner_repo, found["ref"])
            tail = found["tail"]
            version = resolve.exact_version(owner_repo, sha) or found["ref"]
            comment = tail if "#" in tail else f" # {version}{tail}"
            ending = "\n" if line.endswith("\n") else ""
            q = found["quote"]
            lines[index] = f"{found['head']}{q}{found['target']}@{sha}{q}{comment}{ending}"
            edited = True
        if edited:
            _write(repo, name, "".join(lines))
            changed.append(name)
    return changed


def add_cooldown(repo: Repo) -> list[str]:
    """A cooldown on each Dependabot update, `minimumReleaseAge` in Renovate."""
    changed = []
    for name in repo.matching(".github/dependabot.yml", ".github/dependabot.yaml"):
        lines = repo.text(name).splitlines(keepends=True)
        out: list[str] = []
        for index, line in enumerate(lines):
            out.append(line)
            found = re.match(r"^(\s*)-\s+package-ecosystem:", line)
            if not found:
                continue
            indent = found.group(1) + "  "
            block = []
            for following in lines[index + 1 :]:
                if re.match(rf"^{found.group(1)}-\s", following) or not following.startswith(
                    indent
                ):
                    break
                block.append(following)
            if not any(re.match(rf"^{indent}cooldown:", item) for item in block):
                out.append(f"{indent}cooldown:\n{indent}  default-days: {COOLDOWN_DAYS}\n")
        if out != lines:
            _write(repo, name, "".join(out))
            changed.append(name)
    for name in repo.matching("renovate.json", ".github/renovate.json", ".renovaterc.json"):
        config = json.loads(repo.text(name) or "{}")
        if "minimumReleaseAge" not in config:
            config["minimumReleaseAge"] = f"{COOLDOWN_DAYS} days"
            _write(repo, name, json.dumps(config, indent=2) + "\n")
            changed.append(name)
    return changed


def _folder(name: str) -> str:
    """A file's folder as Dependabot names it: `/` at the root, `/.devcontainer` below it."""
    parent = PurePosixPath(name).parent.as_posix()
    return "/" if parent == "." else f"/{parent}"


def _folders(repo: Repo, *patterns: str) -> list[str]:
    return sorted(
        {_folder(name) for name in repo.matching(*patterns) if "node_modules/" not in name}
    )


def _actions_folders(repo: Repo) -> list[str]:
    """`/` for the workflows, then each composite action that uses others: Dependabot reads
    no other folder unless told."""
    composites = {
        _folder(name)
        for name in repo.matching(*ACTIONS)
        if any(USES.match(line) for line in repo.text(name).splitlines())
    }
    return sorted(({"/"} if repo.matching(*WORKFLOWS) else set()) | composites)


def ecosystems(repo: Repo) -> list[tuple[str, list[str]]]:
    """The Dependabot ecosystems a repo uses, each with its folders."""
    found = [
        ("uv", _folders(repo, "**/uv.lock")),
        (
            "pip",
            [
                f
                for f in _folders(repo, "**/requirements*.txt")
                if f not in _folders(repo, "**/uv.lock")
            ],
        ),
        ("npm", _folders(repo, "**/package.json")),
        ("docker", _folders(repo, *CONTAINER_FILES)),
        ("github-actions", _actions_folders(repo)),
    ]
    return [(name, folders) for name, folders in found if folders]


def add_dependabot(repo: Repo) -> list[str]:
    """Dependabot for every ecosystem found, weekly, with the cooldown."""
    lines = ["version: 2", "updates:"]
    for ecosystem, folders in ecosystems(repo):
        lines += [f"  - package-ecosystem: {ecosystem}", "    directories:"]
        lines += [f'      - "{folder}"' for folder in folders]
        lines += [
            "    schedule:",
            "      interval: weekly",
            "    cooldown:",
            f"      default-days: {COOLDOWN_DAYS}",
        ]
    if len(lines) == 2:
        return []
    _write(repo, DEPENDABOT, "\n".join(lines) + "\n")
    return [DEPENDABOT]


# A workflow that writes (pushes, releases, comments) needs more than `contents: read`: left to
# judgment rather than broken.
WRITES = re.compile(
    r"git push|gh (release|pr|issue|api)|action-gh-release|deploy-pages|upload-pages-artifact|"
    r"create-pull-request|github-script|softprops/|peter-evans/|stefanzweifel/"
)


def add_permissions(repo: Repo) -> list[str]:
    """`permissions: contents: read` at the top of each workflow that sets none and writes
    nothing."""
    changed = []
    for name in repo.matching(*WORKFLOWS):
        text = repo.text(name)
        try:
            workflow = yaml.safe_load(text)
        except yaml.YAMLError:
            continue
        if not isinstance(workflow, dict) or "permissions" in workflow or WRITES.search(text):
            continue
        jobs = workflow.get("jobs")
        if isinstance(jobs, dict) and any(
            isinstance(job, dict) and "permissions" in job for job in jobs.values()
        ):
            continue
        lines = text.splitlines(keepends=True)
        at = next(
            (index for index, line in enumerate(lines) if re.match(r"^jobs:\s*$", line)), None
        )
        if at is None:
            continue
        lines.insert(at, "permissions:\n  contents: read\n\n")
        _write(repo, name, "".join(lines))
        changed.append(name)
    return changed


GITLEAKS = "gitleaks/gitleaks"
PRE_COMMIT = (".pre-commit-config.yaml", ".pre-commit-config.yml")


def add_secret_scan(repo: Repo) -> list[str]:
    """gitleaks in the pre-commit hooks when the repo has them, otherwise a workflow."""
    version = resolve.latest_release(GITLEAKS)
    for name in repo.matching(*PRE_COMMIT):
        text = repo.text(name).rstrip("\n")
        hook = (
            f"\n  - repo: https://github.com/{GITLEAKS}\n    rev: {version}\n"
            "    hooks:\n      - id: gitleaks\n"
        )
        if not re.search(r"(?m)^repos:", text):
            continue
        _write(repo, name, text + hook)
        return [name]
    checkout = resolve.latest_release("actions/checkout")
    sha = resolve.commit_of("actions/checkout", checkout)
    image = f"ghcr.io/gitleaks/gitleaks:{version}"
    digest = resolve.image_digest(image)
    workflow = ".github/workflows/secrets.yml"
    _write(
        repo,
        workflow,
        f"""name: secrets
on:
  push:
  pull_request:
permissions:
  contents: read
jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@{sha} # {checkout}
        with:
          fetch-depth: 0
          persist-credentials: false
      - run: >-
          docker run --rm -v "$PWD:/repo" {image}@{digest}
          git /repo --redact --no-banner
""",
    )
    return [workflow]


def _ci_steps(repo: Repo) -> list[str]:
    steps: list[str] = []
    names = set(repo.files)
    if "uv.lock" in names:
        steps += ["uv sync --locked"]
        text = repo.text("pyproject.toml")
        if "[tool.ruff" in text:
            steps.append("uv run ruff check")
        if "pytest" in text or repo.matching("tests/**/*.py", "**/test_*.py"):
            steps.append("uv run pytest -q")
    elif repo.matching("requirements*.txt"):
        steps += [f"pip install -r {name}" for name in sorted(repo.matching("requirements*.txt"))]
        if repo.matching("**/test_*.py", "tests/**/*.py"):
            steps += ["pip install pytest", "python -m pytest -q"]
    if "package.json" in names:
        manager = "pnpm" if "pnpm-lock.yaml" in names else "npm"
        install = (
            f"pnpm install --frozen-lockfile {PNPM_LENIENT_BUILDS}"
            if manager == "pnpm"
            else "npm ci"
        )
        package = json.loads(repo.text("package.json") or "{}")
        scripts = package.get("scripts", {}) if isinstance(package, dict) else {}
        steps.append(install)
        steps += [f"{manager} run {name}" for name in ("lint", "test") if name in scripts]
    return steps


def add_ci(repo: Repo) -> list[str]:
    """A minimal GitHub Actions CI: the repo's own install, lint and tests on each push and pull
    request, actions pinned by SHA."""
    steps = _ci_steps(repo)
    if not steps:
        return []
    uses = []
    for action in (
        "actions/checkout",
        "astral-sh/setup-uv",
        "pnpm/action-setup",
        "actions/setup-python",
        "actions/setup-node",
    ):
        needed = {
            "actions/checkout": True,
            "astral-sh/setup-uv": any(step.startswith("uv ") for step in steps),
            "actions/setup-python": any(step.startswith(("pip ", "python ")) for step in steps),
            "pnpm/action-setup": any(step.startswith("pnpm ") for step in steps),
            "actions/setup-node": any(step.startswith(("pnpm ", "npm ")) for step in steps),
        }[action]
        if needed:
            version = resolve.latest_release(action)
            uses.append(f"      - uses: {action}@{resolve.commit_of(action, version)} # {version}")
            if action == "actions/checkout":
                uses.append("        with:\n          persist-credentials: false")
            if action == "actions/setup-python":
                uses.append('        with:\n          python-version: "3.13"')
            if action == "actions/setup-node":
                uses.append("        with:\n          node-version: 24")
    name = ".github/workflows/ci.yml"
    runs = [f"      - run: {step}" for step in steps]
    _write(
        repo,
        name,
        "name: ci\non:\n  push:\n  pull_request:\npermissions:\n  contents: read\njobs:\n"
        "  checks:\n    runs-on: ubuntu-latest\n    steps:\n" + "\n".join(uses + runs) + "\n",
    )
    return [name]


register(Fixer("pin_actions", pin_actions, "actions pinned to a commit SHA", network=True))
register(Fixer("add_cooldown", add_cooldown, f"a {COOLDOWN_DAYS}-day cooldown on updates"))
register(Fixer("add_dependabot", add_dependabot, "Dependabot for every ecosystem found"))
register(Fixer("add_permissions", add_permissions, "workflow tokens read the repo only"))
register(Fixer("add_secret_scan", add_secret_scan, "gitleaks scans for secrets", network=True))
register(Fixer("add_ci", add_ci, "a minimal CI: install, lint and tests", network=True))

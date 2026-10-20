"""How a rule is detected: declarative first, Python only when no pattern can say it.

A detector is the `[detector]` table of a rule file. Its `kind`:
- `file`: `paths` (globs) present, or absent with `expect = "absent"`;
- `regex`: `pattern` searched in `files` (globs); `expect = "none"` (the default) fails on each
  match, with its location, `expect = "match"` passes on the first one;
- `toml`, `json`, `yaml`: the dotted `key` in each file of `files`, present (or equal to
  `equals`), or absent with `expect = "absent"`;
- `python`: `check`, a function of `PYTHON_CHECKS`, for what no pattern can say.
No file to look at means the rule does not apply (`n/a`), never a pass.
"""

import json
import re
import tomllib
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import PurePosixPath

import yaml  # brought by copier

from kiln.grid.facts import Repo

PASS, FAIL, NOT_APPLICABLE = "pass", "fail", "n/a"
KINDS = ("file", "regex", "toml", "json", "yaml", "python")
# Locations kept per rule: enough to act on, not a dump.
MAX_LOCATIONS = 20


@dataclass(frozen=True)
class Outcome:
    status: str  # pass, fail, n/a
    locations: tuple[str, ...] = field(default=())  # `path:line` or `path`, where it fails
    detail: str = ""


class DetectorError(ValueError):
    """A detector that cannot run as written."""


def detect(detector: Mapping[str, object], repo: Repo) -> Outcome:
    kind = detector.get("kind")
    if kind == "file":
        return _file(detector, repo)
    if kind == "regex":
        return _regex(detector, repo)
    if kind in ("toml", "json", "yaml"):
        return _key(str(kind), detector, repo)
    if kind == "python":
        check = PYTHON_CHECKS.get(str(detector.get("check", "")))
        if check is None:
            raise DetectorError(f"unknown python check {detector.get('check')!r}")
        return check(repo)
    raise DetectorError(f"unknown detector kind {kind!r}, expected one of {', '.join(KINDS)}")


def problems(detector: Mapping[str, object]) -> list[str]:
    """What keeps a detector from running: unknown kind, missing field, bad regex."""
    kind = detector.get("kind")
    if kind not in KINDS:
        return [f"detector kind {kind!r} is not one of {', '.join(KINDS)}"]
    required = {
        "file": ("paths",),
        "regex": ("files", "pattern"),
        "toml": ("files", "key"),
        "json": ("files", "key"),
        "yaml": ("files", "key"),
        "python": ("check",),
    }[str(kind)]
    found = [f"detector {kind}: `{name}` missing" for name in required if name not in detector]
    if kind == "regex" and "pattern" in detector:
        try:
            re.compile(str(detector["pattern"]), re.MULTILINE)
        except re.error as error:
            found.append(f"detector regex: {error}")
    if kind == "python" and detector.get("check") not in PYTHON_CHECKS:
        found.append(f"detector python: no check named {detector.get('check')!r}")
    return found


def _globs(detector: Mapping[str, object], name: str) -> tuple[str, ...]:
    value = detector.get(name, ())
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value) if isinstance(value, list | tuple) else ()


def _file(detector: Mapping[str, object], repo: Repo) -> Outcome:
    found = repo.matching(*_globs(detector, "paths"))
    if detector.get("expect", "present") == "absent":
        return Outcome(FAIL, tuple(found[:MAX_LOCATIONS])) if found else Outcome(PASS)
    return Outcome(PASS, tuple(found[:1])) if found else Outcome(FAIL, detail="not found")


def _regex(detector: Mapping[str, object], repo: Repo) -> Outcome:
    files = repo.matching(*_globs(detector, "files"))
    if not files:
        return Outcome(NOT_APPLICABLE)
    pattern = re.compile(str(detector["pattern"]), re.MULTILINE)
    wants_match = detector.get("expect", "none") == "match"
    locations: list[str] = []
    for name in files:
        try:
            text = (repo.root / name).read_text(encoding="utf-8")
        except OSError, UnicodeDecodeError:
            continue
        for found in pattern.finditer(text):
            if wants_match:
                return Outcome(PASS, (name,))
            locations.append(f"{name}:{text.count(chr(10), 0, found.start()) + 1}")
    if wants_match:
        return Outcome(FAIL, detail="no file matches")
    return Outcome(FAIL, tuple(locations[:MAX_LOCATIONS])) if locations else Outcome(PASS)


def _key(kind: str, detector: Mapping[str, object], repo: Repo) -> Outcome:
    files = repo.matching(*_globs(detector, "files"))
    if not files:
        return Outcome(NOT_APPLICABLE)
    path = str(detector["key"]).split(".")
    expect_absent = detector.get("expect", "present") == "absent"
    failing: list[str] = []
    for name in files:
        try:
            data = _parse(kind, (repo.root / name).read_text(encoding="utf-8"))
        except OSError, ValueError, yaml.YAMLError:
            failing.append(name)
            continue
        value = _dig(data, path)
        present = value is not _MISSING and (
            "equals" not in detector or value == detector["equals"]
        )
        if present == expect_absent:
            failing.append(name)
    return Outcome(FAIL, tuple(failing[:MAX_LOCATIONS])) if failing else Outcome(PASS)


_MISSING = object()


def _parse(kind: str, text: str) -> object:
    if kind == "toml":
        return tomllib.loads(text)
    if kind == "json":
        return json.loads(text)
    return yaml.safe_load(text)


def _dig(data: object, path: list[str]) -> object:
    for part in path:
        if not isinstance(data, dict) or part not in data:
            return _MISSING
        data = data[part]
    return data


# What no declarative pattern can say. Each one is a plain function of the repo.

# A manifest and the lockfiles that pin it, in its folder or, for a workspace, a parent one.
LOCKFILES = {
    "pyproject.toml": ("uv.lock", "poetry.lock", "pdm.lock", "pylock.toml"),
    "Pipfile": ("Pipfile.lock",),
    "package.json": ("pnpm-lock.yaml", "package-lock.json", "yarn.lock", "bun.lock", "bun.lockb"),
}


def lockfiles(repo: Repo) -> Outcome:
    """Each dependency manifest has a lockfile beside it or in a parent folder."""
    present = set(repo.files)
    manifests = [
        name
        for name in repo.files
        if PurePosixPath(name).name in LOCKFILES and _has_deps(repo, name)
    ]
    if not manifests:
        return Outcome(NOT_APPLICABLE)
    missing = [
        name
        for name in manifests
        if not any(
            (folder / lock).as_posix().removeprefix("./") in present
            for folder in (PurePosixPath(name).parent, *PurePosixPath(name).parent.parents)
            for lock in LOCKFILES[PurePosixPath(name).name]
        )
    ]
    return Outcome(FAIL, tuple(missing[:MAX_LOCATIONS])) if missing else Outcome(PASS)


def _has_deps(repo: Repo, manifest: str) -> bool:
    """A pyproject.toml of tool settings alone (no dependencies) needs no lockfile."""
    if PurePosixPath(manifest).name != "pyproject.toml":
        return True
    try:
        project = tomllib.loads((repo.root / manifest).read_text(encoding="utf-8"))
    except OSError, tomllib.TOMLDecodeError:
        return True
    return bool(project.get("project", {}).get("dependencies")) or bool(
        project.get("dependency-groups") or project.get("tool", {}).get("poetry")
    )


CONTAINER_FILES = ("**/Dockerfile", "**/Containerfile", "**/*.Dockerfile", "**/Dockerfile.*")
ROOT_USERS = frozenset({"root", "0", "0:0", "root:root"})


def non_root_containers(repo: Repo) -> Outcome:
    """The last `USER` of each image (the stage that runs) is not root."""
    files = repo.matching(*CONTAINER_FILES)
    if not files:
        return Outcome(NOT_APPLICABLE)
    failing = []
    for name in files:
        try:
            lines = (repo.root / name).read_text(encoding="utf-8").splitlines()
        except OSError, UnicodeDecodeError:
            continue
        users = [line.split()[1] for line in lines if re.match(r"\s*USER\s+\S", line, re.I)]
        if not users or users[-1].lower() in ROOT_USERS:
            failing.append(name)
    return Outcome(FAIL, tuple(failing[:MAX_LOCATIONS])) if failing else Outcome(PASS)


PYTHON_CHECKS: dict[str, Callable[[Repo], Outcome]] = {
    "lockfiles": lockfiles,
    "non_root_containers": non_root_containers,
}

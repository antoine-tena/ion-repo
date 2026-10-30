"""What a converter looks up online: the commit SHA behind an action's tag, the latest release of
a repo, the digest of a container image. No token: public repos and registries only."""

import functools
import json
import re
import subprocess
import urllib.error
import urllib.request

from kiln.shell import KilnError

TIMEOUT = 15
SEMVER = re.compile(r"^v?(\d+)(?:\.(\d+))?(?:\.(\d+))?$")


@functools.cache
def remote_refs(repo: str) -> dict[str, str]:
    """`{ref name: commit SHA}` of a GitHub repo, annotated tags peeled to their commit."""
    done = subprocess.run(
        ["git", "ls-remote", "--tags", "--heads", f"https://github.com/{repo}"],
        capture_output=True,
        text=True,
        check=False,
        timeout=TIMEOUT * 2,
        env={"GIT_TERMINAL_PROMPT": "0", "PATH": "/usr/bin:/bin:/usr/local/bin"},
    )
    if done.returncode != 0:
        raise KilnError(f"cannot read {repo} on GitHub: {done.stderr.strip()[:120]}")
    refs: dict[str, str] = {}
    for line in done.stdout.splitlines():
        sha, _, name = line.partition("\t")
        short = name.removeprefix("refs/tags/").removeprefix("refs/heads/")
        if short.endswith("^{}"):
            refs[short.removesuffix("^{}")] = sha  # the peeled commit wins
        else:
            refs.setdefault(short, sha)
    return refs


def commit_of(repo: str, ref: str) -> str:
    refs = remote_refs(repo)
    if ref not in refs:
        raise KilnError(f"{repo} has no tag or branch {ref}")
    return refs[ref]


def exact_version(repo: str, sha: str) -> str | None:
    """The most precise version tag on commit `sha`: `v7.0.1` rather than the `v7` that moves
    with it, the comment Dependabot keeps up to date beside a pinned SHA."""
    versions = [
        (name.count("."), tuple(int(part or 0) for part in found.groups()), name)
        for name, commit in remote_refs(repo).items()
        if commit == sha and (found := SEMVER.match(name))
    ]
    return max(versions)[2] if versions else None


def latest_release(repo: str, major: str | None = None) -> str:
    """The highest `vX.Y.Z` tag, within `major` when given (`v4`)."""
    versions = []
    for name in remote_refs(repo):
        found = SEMVER.match(name)
        if found and (major is None or name.lstrip("v").split(".")[0] == major.lstrip("v")):
            versions.append((tuple(int(part or 0) for part in found.groups()), name))
    if not versions:
        raise KilnError(f"{repo} has no release tag")
    return max(versions)[1]


def _get(url: str, headers: dict[str, str], method: str = "GET") -> tuple[dict[str, str], bytes]:
    request = urllib.request.Request(url, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=TIMEOUT) as answer:
        return dict(answer.headers), answer.read()


MANIFESTS = ", ".join(
    (
        "application/vnd.oci.image.index.v1+json",
        "application/vnd.docker.distribution.manifest.list.v2+json",
        "application/vnd.oci.image.manifest.v1+json",
        "application/vnd.docker.distribution.manifest.v2+json",
    )
)


DOCKER_HUB = "registry-1.docker.io"


def registry_path(name: str) -> tuple[str, str]:
    """The registry's API host and the repository path of an image name (without its tag):
    Docker Hub's names (`node`, `docker.io/library/node`) are served by registry-1.docker.io."""
    first = name.split("/")[0]
    if "." in first or ":" in first or first == "localhost":
        registry, path = first, name.split("/", 1)[1]
    else:
        registry, path = "docker.io", name
    if registry in {"docker.io", "index.docker.io"}:
        return DOCKER_HUB, path if "/" in path else f"library/{path}"
    return registry, path


@functools.cache
def image_digest(image: str) -> str:
    """`sha256:…` of `name:tag` (the multi-platform index when there is one), through the
    registry's anonymous token."""
    name, _, tag = image.partition(":")
    tag = tag or "latest"
    registry, path = registry_path(name)
    url = f"https://{registry}/v2/{path}/manifests/{tag}"
    headers = {"Accept": MANIFESTS}
    try:
        answer, _ = _get(url, headers, "HEAD")
    except urllib.error.HTTPError as error:
        if error.code != 401:
            raise KilnError(f"{image}: registry answered {error.code}") from error
        challenge = error.headers.get("WWW-Authenticate", "")
        fields = dict(re.findall(r'(\w+)="([^"]*)"', challenge))
        if "realm" not in fields:
            raise KilnError(f"{image}: registry asks for credentials") from error
        query = f"?service={fields.get('service', '')}&scope=repository:{path}:pull"
        _, body = _get(fields["realm"] + query, {})
        token = json.loads(body).get("token") or json.loads(body).get("access_token")
        answer, _ = _get(url, {**headers, "Authorization": f"Bearer {token}"}, "HEAD")
    except urllib.error.URLError as error:
        raise KilnError(f"{image}: registry unreachable ({error.reason})") from error
    digest = {key.lower(): value for key, value in answer.items()}.get("docker-content-digest")
    if not digest:
        raise KilnError(f"{image}: the registry gave no digest")
    return digest

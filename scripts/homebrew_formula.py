"""The Homebrew formula of a promoted release, printed on stdout (T-12).

    uv run python scripts/homebrew_formula.py 0.4.5 > Formula/kiln.rb

`pypi.yml` runs it once PyPI has the release and pushes the result to the tap
(https://github.com/antoine-tena/kiln-homebrew), so `brew upgrade kiln` follows each promotion.
The formula installs wheels only, each pinned by its hash from `uv.lock`: copier needs
pydantic-core, and a Homebrew build from source would compile Rust on every machine. uv does the
installing (kiln needs it anyway), into a virtualenv of Homebrew's Python.
"""

import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = "kiln-cli"
PYTHON = "python@3.14"
# PyPI's JSON can lag a minute behind the upload that `pypi.yml` has just made.
ATTEMPTS, PAUSE = 10, 30

FORMULA = """\
# Written by scripts/homebrew_formula.py in antoine-tena/kiln at each promoted release: a change
# made here by hand is lost at the next one.
class Kiln < Formula
  desc "Claude Code's workshop"
  homepage "https://github.com/antoine-tena/kiln"
  url "{url}", using: :nounzip
  version "{version}"
  sha256 "{sha256}"
  license "MIT"

  depends_on "{python}"
  depends_on "uv"

  def install
    (buildpath/"requirements.txt").write <<~EOS
{requirements}
    EOS
    python = libexec/"bin/python"
    ENV["UV_PYTHON_DOWNLOADS"] = "never"
    system "uv", "venv", "--python", Formula["{python}"].opt_bin/"python{python_version}", libexec
    system "uv", "pip", "install", "--python", python, "--require-hashes", "--no-deps",
           "--only-binary", ":all:", "--find-links", buildpath, "--requirement",
           buildpath/"requirements.txt"
    bin.install_symlink libexec/"bin/kiln", libexec/"bin/charter", libexec/"bin/charte"
  end

  test do
    assert_match version.to_s, shell_output("#{{bin}}/kiln --version")
  end
end
"""


def wheel(version: str) -> dict[str, str]:
    """The release's wheel on PyPI: `url` and `sha256`, waited for while PyPI catches up."""
    address = f"https://pypi.org/pypi/{PACKAGE}/{version}/json"
    for attempt in range(ATTEMPTS):
        try:
            with urllib.request.urlopen(address, timeout=30) as response:
                files = json.load(response)["urls"]
        except OSError:
            files = []
        for file in files:
            if file["packagetype"] == "bdist_wheel":
                return {"url": file["url"], "sha256": file["digests"]["sha256"]}
        if attempt < ATTEMPTS - 1:
            time.sleep(PAUSE)
    raise SystemExit(f"no wheel of {PACKAGE} {version} on PyPI")


def locked_requirements(root: Path) -> str:
    """kiln's runtime dependencies as `uv.lock` pins them, with their hashes."""
    return subprocess.run(
        [
            "uv",
            "export",
            "--frozen",
            "--no-dev",
            "--no-emit-project",
            "--no-header",
            "--no-annotate",
            "--format",
            "requirements-txt",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def render(version: str, url: str, sha256: str, requirements: str) -> str:
    """The formula: the dependencies as locked, then kiln itself, by its hash."""
    # One line per requirement: a backslash would join lines inside Ruby's heredoc anyway.
    joined = requirements.replace(" \\\n", " ").replace("    --hash", "--hash")
    pinned = f"{joined.rstrip()}\n{PACKAGE}=={version} --hash=sha256:{sha256}\n"
    return FORMULA.format(
        url=url,
        version=version,
        sha256=sha256,
        python=PYTHON,
        python_version=PYTHON.removeprefix("python@"),
        requirements="\n".join(f"      {line}" for line in pinned.splitlines()),
    )


def main() -> None:
    version = sys.argv[1].removeprefix("v")
    found = wheel(version)
    print(render(version, found["url"], found["sha256"], locked_requirements(ROOT)), end="")


if __name__ == "__main__":
    main()

"""The Homebrew formula (T-12): written from `uv.lock` and PyPI, upgraded by brew."""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

from ion_repo import versions

ROOT = Path(__file__).resolve().parent.parent
SHA = "ab" * 32


def formula() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "homebrew_formula", ROOT / "scripts/homebrew_formula.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_formula_pins_the_lock_and_kiln_by_hash() -> None:
    locked = f"copier==9.18.2 \\\n    --hash=sha256:{'cd' * 32} \\\n    --hash=sha256:{'ef' * 32}\n"
    text = formula().render("0.4.5", "https://files.example/kiln_cli-0.4.5.whl", SHA, locked)

    assert 'url "https://files.example/kiln_cli-0.4.5.whl", using: :nounzip' in text
    assert f'sha256 "{SHA}"' in text
    assert f"      copier==9.18.2 --hash=sha256:{'cd' * 32} --hash=sha256:{'ef' * 32}\n" in text
    assert f"      kiln-cli==0.4.5 --hash=sha256:{SHA}\n" in text
    assert "\\" not in text.split("<<~EOS")[1].split("EOS")[0]
    assert '"#{bin}/kiln --version"' in text


def test_the_lock_gives_every_runtime_dependency() -> None:
    locked = formula().locked_requirements(ROOT)

    assert "copier==" in locked
    assert "pydantic-core==" in locked
    assert "pytest" not in locked
    assert "kiln-cli" not in locked


@pytest.mark.parametrize(
    ("prefix", "tag", "command"),
    [
        ("/opt/homebrew/Cellar/kiln/0.4.4/libexec", "v0.4.5", "brew upgrade kiln"),
        ("/opt/homebrew/Cellar/kiln/0.4.4/libexec", "v0.4.5-rc.1", "git+"),
        ("/home/me/.local/share/uv/tools/keramos-kiln", "v0.4.5", "keramos-kiln==0.4.5"),
    ],
)
def test_a_tool_from_the_tap_upgrades_through_brew(
    monkeypatch: pytest.MonkeyPatch, prefix: str, tag: str, command: str
) -> None:
    monkeypatch.setattr(sys, "prefix", prefix)
    monkeypatch.setattr(versions, "_installed_distribution", lambda: None)

    assert command in versions.upgrade_command(tag)


class FakeDistribution:
    def __init__(self, name: str) -> None:
        self.metadata = {"Name": name}

    def read_text(self, filename: str) -> str | None:
        return None


@pytest.mark.parametrize("name", ["kiln-cli", "keramos-kiln"])
def test_a_pypi_tool_upgrades_under_the_name_it_was_installed_with(
    monkeypatch: pytest.MonkeyPatch, name: str
) -> None:
    monkeypatch.setattr(sys, "prefix", f"/home/me/.local/share/uv/tools/{name}")
    monkeypatch.setattr(versions, "_installed_distribution", lambda: FakeDistribution(name))

    assert versions.upgrade_command("v0.4.5") == f'uv tool install --force "{name}==0.4.5"'

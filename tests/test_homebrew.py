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
    assert f"      ion-repo==0.4.5 --hash=sha256:{SHA}\n" in text
    assert "\\" not in text.split("<<~EOS")[1].split("EOS")[0]
    assert '"#{bin}/ion-repo --version"' in text


def test_the_lock_gives_every_runtime_dependency() -> None:
    locked = formula().locked_requirements(ROOT)

    assert "copier==" in locked
    assert "pydantic-core==" in locked
    assert "pytest" not in locked
    assert "kiln-cli" not in locked


@pytest.mark.parametrize(
    ("prefix", "tag", "command"),
    [
        ("/opt/homebrew/Cellar/ion-repo/0.4.4/libexec", "v0.4.5", "brew upgrade ion-repo"),
        ("/opt/homebrew/Cellar/ion-repo/0.4.4/libexec", "v0.4.5-rc.1", "git+"),
        ("/home/me/.local/share/uv/tools/ion-repo", "v0.4.5", "ion-repo==0.4.5"),
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


def test_a_pypi_tool_upgrades_as_ion_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "prefix", "/home/me/.local/share/uv/tools/ion-repo")
    monkeypatch.setattr(versions, "_installed_distribution", lambda: FakeDistribution("ion-repo"))

    assert versions.upgrade_command("v0.4.5") == 'uv tool install --force "ion-repo==0.4.5"'


def test_a_kiln_cli_tool_upgrades_into_ion_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "prefix", "/home/me/.local/share/uv/tools/kiln-cli")
    monkeypatch.setattr(versions, "_installed_distribution", lambda: FakeDistribution("kiln-cli"))

    assert versions.upgrade_command("v0.4.5") == (
        'uv tool install ion-sh && uv tool install --force "ion-repo==0.4.5" && '
        'uv tool uninstall kiln-cli && uv tool install --force "ion-repo==0.4.5"'
    )

from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def git_identity(tmp_path_factory: pytest.TempPathFactory, monkeypatch: pytest.MonkeyPatch) -> None:
    """Tests à l'abri de la config git du poste, avec une identité comme sur la CI de GitHub
    qui n'en a pas : sinon un test qui passe ici échoue là-bas."""
    config = Path(tmp_path_factory.mktemp("git")) / "gitconfig"
    config.write_text("[user]\n\tname = Test\n\temail = test@example.com\n")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(config))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    # Copier mirrors each remote template in a cache keyed by URL: a test never fills the
    # machine's (a fake release tag there once followed the real GitHub address).
    monkeypatch.setenv("COPIER_CACHE_DIR", str(tmp_path_factory.mktemp("copier")))
    # The machine's kiln settings (`~/.config/kiln/config.toml`): a machine on the beta channel
    # changed what the session hook offers.
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path_factory.mktemp("config")))
    # Never the machine's GitHub through gh: a test that needs settings gives its own.
    monkeypatch.setattr("ion_repo.grid.forge.ENABLED", False)

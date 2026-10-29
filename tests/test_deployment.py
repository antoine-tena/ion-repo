"""Deployment on a server of one's own (`deploy=vps`): config/vps, scripts/ops and the doc."""

import json
import subprocess
from pathlib import Path

import copier
import pytest
import yaml
from test_template import generate

VPS_ANSWERS = {
    "podman": True,
    "deploy": "vps",
    "vps_host": "root@203.0.113.7",
    "api_domain": "api.demo.example.com",
    "site_url": "https://demo.example.com",
}
SERVER_SCRIPTS = ("deploy-remote", "backup", "restore-test", "heal", "setup-deploy-user")


def test_vps_brings_server_files_scripts_and_docs(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", **VPS_ANSWERS)

    descriptor = json.loads((project_dir / "config/vps/project.json").read_text())
    assert descriptor == {
        "host": "root@203.0.113.7",
        "remotePath": "/opt/demo",
        "branch": "develop",
        "apiUrl": "https://api.demo.example.com",
        "siteUrl": "https://demo.example.com",
    }
    compose = yaml.safe_load((project_dir / "config/vps/compose.yaml").read_text())
    assert set(compose["services"]) == {"db", "backend"}
    assert compose["services"]["backend"]["read_only"] is True
    assert "api.demo.example.com {" in (project_dir / "config/vps/Caddyfile").read_text()
    for unit in ("backup", "restore-test", "heal"):
        assert (project_dir / f"config/vps/demo-{unit}.timer").is_file()
        service = (project_dir / f"config/vps/demo-{unit}.service").read_text()
        assert f"ExecStart=/usr/local/sbin/demo-{unit}" in service
    assert (project_dir / "docs/operations/production.md").is_file()


def test_vps_ports_and_caddy_site_suit_a_shared_server(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", **VPS_ANSWERS, vps_port=8010, vps_db_port=5442)

    backend = yaml.safe_load((project_dir / "config/vps/compose.yaml").read_text())["services"]
    assert backend["db"]["ports"] == ["127.0.0.1:5442:5432"]
    assert "127.0.0.1:8010" in backend["backend"]["command"]
    assert "@127.0.0.1:5442/demo" in backend["backend"]["environment"]["DATABASE_URL"]
    caddyfile = (project_dir / "config/vps/Caddyfile").read_text()
    assert "reverse_proxy 127.0.0.1:8010" in caddyfile
    # A site file imported by the server's Caddyfile: no global options block of its own.
    assert not caddyfile.lstrip().startswith("{")
    switch = (project_dir / "config/vps/deploy-remote.sh").read_text()
    assert 'CADDY_SITE="/etc/caddy/sites/$NAME.caddy"' in switch
    assert "PORT=8010" in switch
    assert "DB_PORT=5442" in switch


@pytest.mark.parametrize(
    "script",
    [f"config/vps/{name}.sh" for name in SERVER_SCRIPTS]
    + ["scripts/ops/deploy-backend.sh", "scripts/ops/smoke-test.sh"],
)
def test_vps_scripts_are_valid_executable_bash(tmp_path: Path, script: str) -> None:
    path = generate(tmp_path / "demo", **VPS_ANSWERS) / script

    assert path.stat().st_mode & 0o100
    # podman's formats ({{.Names}}) survive the rendering of the template.
    assert "{%" not in path.read_text()
    subprocess.run(["bash", "-n", str(path)], check=True)


def test_podman_formats_survive_rendering(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", **VPS_ANSWERS)

    assert "--format '{{.Names}}'" in (project_dir / "config/vps/heal.sh").read_text()


def test_no_vps_files_without_deployment(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", podman=True)

    assert not (project_dir / "config").exists()
    assert not (project_dir / "scripts/ops").exists()
    assert not (project_dir / "docs/operations").exists()


def test_vps_requires_podman(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="podman"):
        copier.run_copy(
            str(Path(__file__).resolve().parent.parent),
            tmp_path / "demo",
            data={**VPS_ANSWERS, "podman": False, "name": "demo"},
            defaults=True,
            vcs_ref="HEAD",
            quiet=True,
        )


def test_backend_image_serves_gunicorn_without_migrating(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", podman=True)

    containerfile = (project_dir / "backend/Containerfile").read_text()
    assert '"gunicorn", "config.wsgi"' in containerfile
    assert "collectstatic" in containerfile
    command = yaml.safe_load((project_dir / "compose.yaml").read_text())["services"]["backend"]
    assert "runserver" in command["command"][-1]


def test_vercel_brings_only_the_front_deployment(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", frontend_deploy="vercel")

    ops = project_dir / "scripts/ops"
    assert sorted(path.name for path in ops.rglob("*.sh")) == ["deploy-frontend.sh", "green-ci.sh"]
    script = ops / "deploy-frontend.sh"
    assert script.stat().st_mode & 0o111
    subprocess.run(["bash", "-n", str(script)], check=True)
    assert not (project_dir / "config/vps").exists()


@pytest.mark.parametrize(("backend", "frontend"), [("data", "streamlit"), ("none", "dash")])
def test_a_dashboard_alone_deploys_its_own_image_without_a_database(
    tmp_path: Path, backend: str, frontend: str
) -> None:
    # A Streamlit or Dash front needs a long-running server with websockets: the VPS fits (#43).
    answers = {key: value for key, value in VPS_ANSWERS.items() if key != "api_domain"}
    project_dir = generate(tmp_path / "demo", backend=backend, frontend=frontend, **answers)

    compose = yaml.safe_load((project_dir / "config/vps/compose.yaml").read_text())
    assert set(compose["services"]) == {"frontend"}
    assert compose["services"]["frontend"]["read_only"] is True
    port = 8501 if frontend == "streamlit" else 8050
    assert f"reverse_proxy 127.0.0.1:{port}" in (project_dir / "config/vps/Caddyfile").read_text()
    assert "demo.example.com {" in (project_dir / "config/vps/Caddyfile").read_text()
    assert "apiUrl" not in json.loads((project_dir / "config/vps/project.json").read_text())
    assert not (project_dir / "config/vps/backup.sh").exists()
    assert not (project_dir / "scripts/ops/deploy-backend.sh").exists()
    for script in ("config/vps/deploy-remote.sh", "scripts/ops/deploy-frontend.sh"):
        path = project_dir / script
        assert path.stat().st_mode & 0o100
        subprocess.run(["bash", "-n", str(path)], check=True)
    remote = (project_dir / "config/vps/deploy-remote.sh").read_text()
    assert "SERVICE=frontend" in remote and "HAS_DB=0" in remote
    assert "Production of" in (project_dir / "docs/operations/production.md").read_text()


def test_vps_is_refused_for_a_front_that_needs_an_api_elsewhere(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Django backend, or a Streamlit or Dash front"):
        generate(tmp_path / "demo", backend="fastapi", frontend="nuxt", **VPS_ANSWERS)

import json
import subprocess
import tomllib
from pathlib import Path

import copier
import pytest
import yaml

TEMPLATE_DIR = Path(__file__).resolve().parent.parent
ANSWERS = {
    "name": "demo",
    "title": "Demo",
    "description": "Projet de démonstration.",
    "owner": "antoine-tena",
    "team": ["antoine-tena", "NathanBarrachin"],
}
BACKENDS = ("django", "fastapi", "data", "cli", "java", "none")
FRONTENDS = ("nuxt", "next", "astro", "streamlit", "dash", "none")
STACKS = [
    (back, front) for back in BACKENDS for front in FRONTENDS if (back, front) != ("none",) * 2
]
# Un outil en ligne de commande ou un backend Java seuls n'ont rien à conteneuriser : copier
# refuse podman.
PODMAN_STACKS = [stack for stack in STACKS if stack not in {("cli", "none"), ("java", "none")}]
JSON_FILES = (".vscode/settings.json", ".vscode/extensions.json", ".claude/settings.json")


def generate(destination: Path, **extra_answers: object) -> Path:
    copier.run_copy(
        str(TEMPLATE_DIR),
        destination,
        data={**ANSWERS, **extra_answers},
        defaults=True,
        vcs_ref="HEAD",
        quiet=True,
    )
    return destination


def test_default_stack_is_django_and_nuxt(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo")

    assert (project_dir / "backend/config/api.py").is_file()
    assert (project_dir / "frontend/nuxt.config.ts").is_file()
    assert (
        (project_dir / ".github/CODEOWNERS")
        .read_text()
        .endswith("* @antoine-tena @NathanBarrachin\n")
    )


@pytest.mark.parametrize(("backend", "frontend"), STACKS)
def test_every_stack_renders_valid_files(tmp_path: Path, backend: str, frontend: str) -> None:
    project_dir = generate(tmp_path / "demo", backend=backend, frontend=frontend)

    rendered = [
        path for path in project_dir.rglob("*") if path.is_file() and ".git" not in path.parts
    ]
    assert not [path for path in rendered if path.suffix == ".jinja"]
    assert not [path for path in rendered if path.suffix != ".ico" and "{%" in path.read_text()]
    tomllib.loads((project_dir / "charter.toml").read_text())
    yaml.safe_load((project_dir / ".github/workflows/ci.yml").read_text())
    yaml.safe_load((project_dir / ".pre-commit-config.yaml").read_text())
    for name in JSON_FILES:
        json.loads((project_dir / name).read_text())
    assert (project_dir / "backend").is_dir() == (backend != "none")
    assert (project_dir / "frontend").is_dir() == (frontend != "none")


@pytest.mark.parametrize(("backend", "frontend"), PODMAN_STACKS)
def test_podman_adds_containers_for_every_stack(
    tmp_path: Path, backend: str, frontend: str
) -> None:
    project_dir = generate(tmp_path / "demo", backend=backend, frontend=frontend, podman=True)

    compose = yaml.safe_load((project_dir / "compose.yaml").read_text())
    for directory in ("backend", "frontend"):
        if (project_dir / directory / "Containerfile").is_file():
            containerfile = (project_dir / directory / "Containerfile").read_text()
            instructions = [line for line in containerfile.splitlines() if not line.startswith("#")]
            # Outil interdit : la règle [UV-PODMAN] est justement vérifiée ici.
            assert not [line for line in instructions if "pip install" in line or "docker " in line]
    assert compose["services"]


def test_stack_advice_follows_project_type(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", project_type="dashboard")

    answers = yaml.safe_load((project_dir / ".copier-answers.yml").read_text())
    assert (answers["backend"], answers["frontend"]) == ("data", "streamlit")


@pytest.mark.parametrize(("size", "has_podman"), [("ember", False), ("flame", True)])
def test_size_sets_podman_default(tmp_path: Path, size: str, has_podman: bool) -> None:
    project_dir = generate(tmp_path / "demo", size=size)

    answers = yaml.safe_load((project_dir / ".copier-answers.yml").read_text())
    assert (answers["size"], answers["podman"]) == (size, has_podman)
    project_rules = (project_dir / ".claude/rules/kiln/project.md").read_text()
    assert f"**{size.capitalize()}**" in project_rules


def test_vue_templates_keep_their_mustaches(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo")

    health_component = (project_dir / "frontend/app/components/HealthStatus.vue").read_text()
    assert "{{ health?.status }}" in health_component
    assert "{{ BACKEND_DOWN }}" in health_component


def test_backlog_is_always_there(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", north_star="the demo online", backend="fastapi")

    backlog = (project_dir / "docs/backlog/backlog.md").read_text()
    assert "North star: **the demo online**." in backlog
    assert "- **Type**: task" in backlog
    assert "**Each member writes only their own login**" in backlog
    assert "docs/backlog/" in (project_dir / "CLAUDE.md").read_text()
    assert not (project_dir / "docs/a-faire").exists()
    urgent = (project_dir / "docs/backlog/urgent.md").read_text()
    # The status line counts lines starting with an open box: none at first.
    assert not [line for line in urgent.splitlines() if line.lstrip().startswith("- [ ]")]


def test_django_and_nuxt_share_a_typed_api_contract(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo")

    use_health = (project_dir / "frontend/app/composables/useHealth.ts").read_text()
    assert "useApi().get('/api/health'" in use_health
    assert (project_dir / "frontend/app/composables/useApi.ts").is_file()
    assert "openapi.json linguist-generated" in (project_dir / ".gitattributes").read_text()
    workflow = yaml.safe_load((project_dir / ".github/workflows/ci.yml").read_text())
    # Outside a release (template taken at a commit), workflows are cited at develop.
    assert workflow["jobs"]["api-contract"]["uses"].endswith("api-contract.yml@develop")


def test_fastapi_front_keeps_its_plain_fetch(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", backend="fastapi")

    assert not (project_dir / "frontend/app/composables/useApi.ts").exists()
    assert "apiBase" in (project_dir / "frontend/nuxt.config.ts").read_text()


def test_data_stack_accepts_numeric_arrays_and_trained_models(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", backend="data", frontend="streamlit")

    rules = (project_dir / ".claude/rules/kiln/data.md").read_text()
    assert rules.startswith('---\npaths:\n  - "backend/**"\n---\n')
    assert "NumPy" in rules
    assert "`data/models/`" in rules
    attributes = (project_dir / ".gitattributes").read_text()
    assert "backend/data/models/** linguist-generated=true" in attributes


@pytest.mark.parametrize(("backend", "frontend"), [("django", "nuxt"), ("data", "streamlit")])
def test_readme_sections_start_on_their_own_line(
    tmp_path: Path, backend: str, frontend: str
) -> None:
    project_dir = generate(tmp_path / "demo", backend=backend, frontend=frontend)

    readme = (project_dir / "README.md").read_text()
    assert "\n\n## Work tracking\n" in readme
    assert all(line.startswith("## ") for line in readme.splitlines() if "## " in line)


def test_ci_runs_for_main_and_develop(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo")

    workflow = yaml.safe_load((project_dir / ".github/workflows/ci.yml").read_text())
    # PyYAML lit la clé `on` comme le booléen True.
    triggers = workflow[True]
    assert triggers["push"]["branches"] == ["main", "develop"]
    assert triggers["pull_request"]["branches"] == ["main", "develop"]


def test_tool_project_gets_a_command_line_package(tmp_path: Path) -> None:
    # A long description must not overflow into the code (E501 at the first commit).
    long_description = "A tool whose description goes well beyond a hundred characters. " * 3
    project_dir = generate(
        tmp_path / "demo", project_type="cli", size="flame", description=long_description
    )

    answers = yaml.safe_load((project_dir / ".copier-answers.yml").read_text())
    assert (answers["backend"], answers["frontend"], answers["podman"]) == ("cli", "none", False)
    pyproject = tomllib.loads((project_dir / "backend/pyproject.toml").read_text())
    assert pyproject["project"]["scripts"] == {"demo": "demo.cli:main"}
    assert (project_dir / "backend/demo/cli.py").is_file()
    assert "[THIN-CLI]" in (project_dir / ".claude/rules/kiln/cli.md").read_text()
    assert not (project_dir / "compose.yaml").exists()
    python_lines = [
        line
        for path in (project_dir / "backend").rglob("*.py")
        for line in path.read_text().splitlines()
    ]
    assert all(len(line) <= 100 for line in python_lines)


def test_java_backend_gets_a_maven_project(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", name="demo-app", backend="java", frontend="none")

    backend_dir = project_dir / "backend"
    pom = (backend_dir / "pom.xml").read_text()
    assert "<artifactId>demo-app</artifactId>" in pom
    assert "<main.class>io.github.antoinetena.demoapp.Main</main.class>" in pom
    package_dir = "io/github/antoinetena/demoapp"
    assert (backend_dir / f"src/main/java/{package_dir}/Main.java").is_file()
    service_test = f"src/test/java/{package_dir}/greeting/GreetingServiceTest.java"
    assert (backend_dir / service_test).is_file()
    assert (backend_dir / "mvnw").stat().st_mode & 0o111
    wrapper = (backend_dir / ".mvn/wrapper/maven-wrapper.properties").read_text()
    assert "distributionSha256Sum=" in wrapper
    assert "[MODERN-JAVA]" in (project_dir / ".claude/rules/kiln/java.md").read_text()
    workflow = yaml.safe_load((project_dir / ".github/workflows/ci.yml").read_text())
    assert workflow["jobs"]["backend"]["uses"].startswith(
        "antoine-tena/kiln/.github/workflows/maven.yml@"
    )
    # Nothing for uv or pnpm to audit: no empty security job.
    assert "security" not in workflow["jobs"]
    charter = tomllib.loads((project_dir / "charter.toml").read_text())
    assert ".java" in charter["ratchets"]["file-size"]["suffixes"]
    charter_rules = (project_dir / ".claude/rules/kiln/charter.md").read_text()
    booleans_rule = charter_rules.split("**[BOOLEANS]**", 1)[1].split("\n- ", 1)[0]
    assert "in Java" in booleans_rule
    assert "Python" not in booleans_rule


def test_team_gets_kiln_marketplace_and_plugin(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", backend="java", frontend="none")

    settings = json.loads((project_dir / ".claude/settings.json").read_text())
    assert settings["extraKnownMarketplaces"]["kiln"]["source"] == {
        "source": "github",
        "repo": "antoine-tena/kiln",
        "ref": "main",
    }
    assert settings["extraKnownMarketplaces"]["kiln"]["autoUpdate"] is True
    assert settings["enabledPlugins"] == {"kiln@kiln": True}


def test_a_released_template_pins_its_workflows_to_its_version(tmp_path: Path) -> None:
    clone = tmp_path / "kiln"
    subprocess.run(["git", "clone", "-q", "--no-tags", str(TEMPLATE_DIR), str(clone)], check=True)
    subprocess.run(["git", "-C", str(clone), "tag", "v9.9.9"], check=True)
    copier.run_copy(
        str(clone), tmp_path / "demo", data=ANSWERS, defaults=True, vcs_ref="v9.9.9", quiet=True
    )

    workflow = yaml.safe_load((tmp_path / "demo/.github/workflows/ci.yml").read_text())
    assert workflow["jobs"]["api-contract"]["uses"].endswith("api-contract.yml@v9.9.9")


def test_a_project_without_owner_has_no_codeowners_nor_team(tmp_path: Path) -> None:
    project_dir = tmp_path / "demo"
    copier.run_copy(
        str(TEMPLATE_DIR),
        project_dir,
        data={"name": "demo", "backend": "fastapi", "frontend": "none"},
        defaults=True,
        vcs_ref="HEAD",
        quiet=True,
    )

    assert not (project_dir / ".github/CODEOWNERS").exists()
    assert "## Team" not in (project_dir / "README.md").read_text()
    assert "owner: ''" in (project_dir / ".copier-answers.yml").read_text()


def rule_files(project_dir: Path) -> set[str]:
    return {path.name for path in (project_dir / ".claude/rules/kiln").glob("*.md")}


def test_the_size_chooses_the_rules(tmp_path: Path) -> None:
    spark = generate(tmp_path / "spark", size="spark", backend="cli", frontend="none")
    blaze = generate(tmp_path / "blaze", size="blaze", podman=True)

    assert rule_files(spark) == {"project.md", "charter.md", "python.md", "cli.md"}
    assert rule_files(blaze) >= {"django.md", "nuxt.md", "production.md", "security.md"}
    django_rules = (blaze / ".claude/rules/kiln/django.md").read_text()
    assert "[RLS]" in django_rules and "[OUTBOX]" in django_rules
    ember_django = generate(tmp_path / "ember", size="ember")
    assert "[OUTBOX]" not in (ember_django / ".claude/rules/kiln/django.md").read_text()


def test_rules_load_by_path_and_claude_md_stays_short(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo")

    for name in ("django.md", "nuxt.md", "python.md"):
        text = (project_dir / ".claude/rules/kiln" / name).read_text()
        assert text.startswith("---\npaths:\n"), name
    for name in ("project.md", "charter.md"):
        assert not (project_dir / ".claude/rules/kiln" / name).read_text().startswith("---")
    assert len((project_dir / "CLAUDE.md").read_text().splitlines()) < 60
    assert not (project_dir / "backend/CLAUDE.md").exists()


def test_the_project_language_rules_what_people_read(tmp_path: Path) -> None:
    french = generate(tmp_path / "fr", language="fr", backend="fastapi", frontend="streamlit")
    english = generate(tmp_path / "en", backend="fastapi", frontend="streamlit")

    assert "Talk with the user in French" in (french / ".claude/rules/kiln/project.md").read_text()
    assert "## Démarrage rapide" in (french / "README.md").read_text()
    assert "## Quick start" in (english / "README.md").read_text()
    french_texts = (french / "frontend/dashboard/constants.py").read_text()
    assert "Le backend ne répond pas" in french_texts
    assert "does not answer" in (english / "frontend/dashboard/constants.py").read_text()


def test_a_language_per_use(tmp_path: Path) -> None:
    project_dir = generate(
        tmp_path / "demo", language="fr", language_custom=True, language_commits="en"
    )

    project_rules = (project_dir / ".claude/rules/kiln/project.md").read_text()
    assert "English" in project_rules.split("Commit messages:", 1)[1][:12]

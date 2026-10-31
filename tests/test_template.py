import json
import re
import subprocess
import tomllib
from pathlib import Path

import copier
import pytest
import yaml

from ion_repo.grid import score

TEMPLATE_DIR = Path(__file__).resolve().parent.parent
ANSWERS = {
    "name": "demo",
    "title": "Demo",
    "description": "Projet de démonstration.",
    "owner": "antoine-tena",
    "team": ["antoine-tena", "NathanBarrachin"],
}
BACKENDS = ("django", "fastapi", "data", "cli", "java", "none")
FRONTENDS = ("nuxt", "next", "astro", "vite-react", "streamlit", "dash", "none")
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


@pytest.mark.parametrize(
    ("backend", "frontend"),
    [(back, "none") for back in BACKENDS[:-1]] + [("none", front) for front in FRONTENDS[:-1]],
)
def test_every_stack_follows_its_code_to_the_root(
    tmp_path: Path, backend: str, frontend: str
) -> None:
    # An adopted repo with its code at the root (T-166): the paths of CI, hooks, rules, charter
    # and Dependabot go there, never to a `backend/` or `frontend/` it does not have.
    where = {"backend_dir": "."} if backend != "none" else {"frontend_dir": "."}
    kept = ["backend"] if backend != "none" else ["frontend"]
    project_dir = generate(
        tmp_path / "demo", backend=backend, frontend=frontend, kept=kept, **where
    )

    texts = {
        name: (project_dir / name).read_text()
        for name in (
            ".github/workflows/ci.yml",
            ".github/dependabot.yml",
            ".pre-commit-config.yaml",
            "charter.toml",
            "CLAUDE.md",
            ".claude/rules/ion-repo/project.md",
        )
    }
    for name, text in texts.items():
        assert not re.search(r"(?<![\w.-])(backend|frontend)/", text), name
    assert "at the root" in texts[".claude/rules/ion-repo/project.md"]
    tomllib.loads(texts["charter.toml"])
    ci = yaml.safe_load(texts[".github/workflows/ci.yml"])
    yaml.safe_load(texts[".pre-commit-config.yaml"])
    directories = [
        job.get("with", {}).get("directory") for job in ci["jobs"].values() if "with" in job
    ]
    assert "backend" not in directories and "frontend" not in directories
    assert yaml.safe_load(texts[".github/dependabot.yml"])["updates"][0]["directories"] == ["/"]
    assert (
        yaml.safe_load((project_dir / ".copier-answers.yml").read_text())[next(iter(where))] == "."
    )


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


@pytest.mark.parametrize(("size", "has_podman"), [("small", False), ("medium", True)])
def test_size_sets_podman_default(tmp_path: Path, size: str, has_podman: bool) -> None:
    project_dir = generate(tmp_path / "demo", size=size)

    answers = yaml.safe_load((project_dir / ".copier-answers.yml").read_text())
    assert (answers["size"], answers["podman"]) == (size, has_podman)
    project_rules = (project_dir / ".claude/rules/ion-repo/project.md").read_text()
    assert f"**{size.capitalize()}**" in project_rules


def test_every_repo_reproduces_first_and_links_directly(tmp_path: Path) -> None:
    project_rules = (generate(tmp_path / "demo") / ".claude/rules/ion-repo/project.md").read_text()

    assert "**[REPRODUCE-FIRST]**" in project_rules
    assert "**[DIRECT-LINKS]**" in project_rules
    assert "ion repo set ai_trailers=disclose|never" in project_rules


@pytest.mark.parametrize(
    ("backend", "frontend"), [("none", "nuxt"), ("none", "astro"), ("none", "none")]
)
def test_project_rules_name_only_the_stack_there_is(
    tmp_path: Path, backend: str, frontend: str
) -> None:
    # A front alone, or a repo adopted without a stack of ion-repo: no empty check list, no "None".
    kept = ["src"] if frontend == "none" else []
    project_dir = generate(tmp_path / "demo", backend=backend, frontend=frontend, kept=kept)

    project_rules = (project_dir / ".claude/rules/ion-repo/project.md").read_text()
    assert not re.search(r"of the stack \((?!\w)", project_rules)
    assert "None" not in project_rules


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
    assert "**Next free: T-02.**" in backlog
    assert "Done" not in backlog
    how_to = (project_dir / "docs/backlog/README.md").read_text()
    assert "**Each member writes only their own login**" in how_to
    assert (project_dir / "docs/backlog/done.md").read_text().startswith("# Done")
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

    rules = (project_dir / ".claude/rules/ion-repo/data.md").read_text()
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


def test_ci_on_github_runs_only_on_release_branches(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", ci_runner="github")

    workflow = yaml.safe_load((project_dir / ".github/workflows/ci.yml").read_text())
    # PyYAML reads the `on` key as the boolean True.
    triggers = workflow[True]
    assert triggers["push"]["branches"] == ["release/**"]
    assert "pull_request" not in triggers


def test_a_local_ci_spends_no_github_minute(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", ci_runner="local")

    workflow = yaml.safe_load((project_dir / ".github/workflows/ci.yml").read_text())
    triggers = workflow[True]
    # By hand, or replayed before a production release: never on a push.
    assert set(triggers) == {"workflow_dispatch", "workflow_call"}


def test_tool_project_gets_a_command_line_package(tmp_path: Path) -> None:
    # A long description must not overflow into the code (E501 at the first commit).
    long_description = "A tool whose description goes well beyond a hundred characters. " * 3
    project_dir = generate(
        tmp_path / "demo", project_type="cli", size="medium", description=long_description
    )

    answers = yaml.safe_load((project_dir / ".copier-answers.yml").read_text())
    assert (answers["backend"], answers["frontend"], answers["podman"]) == ("cli", "none", False)
    pyproject = tomllib.loads((project_dir / "backend/pyproject.toml").read_text())
    assert pyproject["project"]["scripts"] == {"demo": "demo.cli:main"}
    assert (project_dir / "backend/demo/cli.py").is_file()
    assert "[THIN-CLI]" in (project_dir / ".claude/rules/ion-repo/cli.md").read_text()
    assert not (project_dir / "compose.yaml").exists()
    python_lines = [
        line
        for path in (project_dir / "backend").rglob("*.py")
        for line in path.read_text().splitlines()
    ]
    assert all(len(line) <= 100 for line in python_lines)


def test_tool_project_can_ship_its_claude_code_plugin(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", project_type="cli", claude_plugin=True)

    marketplace = json.loads((project_dir / ".claude-plugin/marketplace.json").read_text())
    assert [plugin["source"] for plugin in marketplace["plugins"]] == ["./plugins/demo"]
    manifest = project_dir / "plugins/demo/.claude-plugin/plugin.json"
    assert json.loads(manifest.read_text())["name"] == "demo"
    skill = (project_dir / "plugins/demo/skills/run/SKILL.md").read_text()
    assert skill.startswith("---\nname: run\n")
    settings = json.loads((project_dir / ".claude/settings.json").read_text())
    assert settings["extraKnownMarketplaces"]["demo"]["source"]["repo"] == "antoine-tena/demo"
    assert settings["enabledPlugins"]["demo@demo"] is True
    assert (project_dir / "backend/tests/test_plugin.py").is_file()


def test_plugin_is_named_without_the_ion_prefix(tmp_path: Path) -> None:
    project_dir = generate(
        tmp_path / "ion-demo", name="ion-demo", project_type="cli", claude_plugin=True
    )

    marketplace = json.loads((project_dir / ".claude-plugin/marketplace.json").read_text())
    assert marketplace["name"] == "ion-demo"
    assert marketplace["plugins"][0]["name"] == "demo"
    assert marketplace["plugins"][0]["source"] == "./plugins/demo"
    assert not (project_dir / "plugins/ion-demo").exists()
    manifest = project_dir / "plugins/demo/.claude-plugin/plugin.json"
    assert json.loads(manifest.read_text())["name"] == "demo"
    settings = json.loads((project_dir / ".claude/settings.json").read_text())
    assert settings["enabledPlugins"]["demo@ion-demo"] is True
    assert "/demo:…" in (project_dir / "plugins/demo/README.md").read_text()
    answers = yaml.safe_load((project_dir / ".copier-answers.yml").read_text())
    assert answers["plugin_name"] == "demo"


def test_plugin_name_can_be_set(tmp_path: Path) -> None:
    project_dir = generate(
        tmp_path / "demo", project_type="cli", claude_plugin=True, plugin_name="other"
    )

    assert (project_dir / "plugins/other/.claude-plugin/plugin.json").is_file()
    settings = json.loads((project_dir / ".claude/settings.json").read_text())
    assert settings["enabledPlugins"]["other@demo"] is True


def test_tool_project_can_be_published_on_pypi(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", project_type="cli", pypi_name="keramos-demo")

    pyproject = tomllib.loads((project_dir / "backend/pyproject.toml").read_text())
    assert pyproject["project"]["name"] == "keramos-demo"
    assert pyproject["project"]["scripts"] == {"demo": "demo.cli:main"}
    cli = (project_dir / "backend/demo/cli.py").read_text()
    assert 'DISTRIBUTION = "keramos-demo"' in cli
    workflow = yaml.safe_load((project_dir / ".github/workflows/pypi.yml").read_text())
    job = workflow["jobs"]["publish"]
    assert workflow[True]["push"]["tags"] == ["v[0-9]*"]
    assert job["environment"]["url"] == "https://pypi.org/project/keramos-demo/"
    assert job["permissions"]["id-token"] == "write"
    assert job["defaults"]["run"]["working-directory"] == "backend"
    steps = job["steps"]
    # Every action pinned by its SHA ([PINNED-ACTIONS]).
    actions = [step["uses"] for step in steps if "uses" in step]
    assert actions
    assert all(re.fullmatch(r"[^@]+@[0-9a-f]{40}", action) for action in actions)
    assert steps[-1]["run"] == "uv publish --trusted-publishing automatic"
    assert steps[-1]["env"] == {"UV_PUBLISH_TOKEN": "${{ secrets.PYPI_TOKEN }}"}
    assert "`uv tool install keramos-demo`" in (project_dir / "README.md").read_text()


def test_tool_project_is_not_published_by_default(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", project_type="cli")

    assert not (project_dir / ".github/workflows/pypi.yml").exists()
    pyproject = tomllib.loads((project_dir / "backend/pyproject.toml").read_text())
    assert pyproject["project"]["name"] == "demo"
    assert 'DISTRIBUTION = "demo"' in (project_dir / "backend/demo/cli.py").read_text()


def test_tool_project_ships_no_plugin_by_default(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", project_type="cli")

    assert not (project_dir / "plugins").exists()
    assert not (project_dir / ".claude-plugin").exists()
    assert not (project_dir / "backend/tests/test_plugin.py").exists()
    settings = json.loads((project_dir / ".claude/settings.json").read_text())
    assert list(settings["extraKnownMarketplaces"]) == ["ion-repo"]


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
    assert "[MODERN-JAVA]" in (project_dir / ".claude/rules/ion-repo/java.md").read_text()
    workflow = yaml.safe_load((project_dir / ".github/workflows/ci.yml").read_text())
    assert workflow["jobs"]["backend"]["uses"].startswith(
        "antoine-tena/ion-repo/.github/workflows/maven.yml@"
    )
    # The Maven project audited alone (OSV-Scanner), nothing for uv or pnpm.
    assert workflow["jobs"]["security"]["with"] == {"uv": "", "pnpm": "", "maven": "backend"}
    charter = tomllib.loads((project_dir / "charter.toml").read_text())
    assert ".java" in charter["ratchets"]["file-size"]["suffixes"]
    charter_rules = (project_dir / ".claude/rules/ion-repo/charter.md").read_text()
    booleans_rule = charter_rules.split("**[BOOLEANS]**", 1)[1].split("\n- ", 1)[0]
    assert "in Java" in booleans_rule
    assert "Python" not in booleans_rule


def test_team_gets_kiln_marketplace_and_plugin(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", backend="java", frontend="none")

    settings = json.loads((project_dir / ".claude/settings.json").read_text())
    assert settings["extraKnownMarketplaces"]["ion-repo"]["source"] == {
        "source": "github",
        "repo": "antoine-tena/ion-repo",
        "ref": "main",
    }
    assert settings["extraKnownMarketplaces"]["ion-repo"]["autoUpdate"] is True
    assert settings["enabledPlugins"] == {"repo@ion-repo": True}


def test_sessions_compact_at_400k(tmp_path: Path) -> None:
    settings = json.loads(
        (generate(tmp_path / "demo") / ".claude/settings.json").read_text(encoding="utf-8")
    )
    assert settings["autoCompactWindow"] == 400000
    assert "CLAUDE_CODE_AUTO_COMPACT_WINDOW" not in settings["env"]  # it would beat --autocompact
    assert "disableClaudeAiConnectors" not in settings  # each person's choice, not the repo's


def test_claude_codes_own_defaults_stay_one_setting_away(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", compact_window=1000000)

    settings = json.loads((project_dir / ".claude/settings.json").read_text(encoding="utf-8"))
    assert "autoCompactWindow" not in settings


@pytest.fixture(scope="module")
def released(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, str]:
    """kiln's template as a release would hand it over: a clone tagged v9.9.9, and its SHA."""
    clone = tmp_path_factory.mktemp("released") / "kiln"
    subprocess.run(["git", "clone", "-q", "--no-tags", str(TEMPLATE_DIR), str(clone)], check=True)
    subprocess.run(["git", "-C", str(clone), "tag", "v9.9.9"], check=True)
    sha = subprocess.check_output(["git", "-C", str(clone), "rev-parse", "HEAD"], text=True)
    return clone, sha.strip()


def generate_released(released: tuple[Path, str], destination: Path, **answers: object) -> Path:
    copier.run_copy(
        str(released[0]),
        destination,
        data={**ANSWERS, **answers},
        defaults=True,
        vcs_ref="v9.9.9",
        quiet=True,
    )
    return destination


def test_a_released_template_pins_its_workflows_to_its_version(
    tmp_path: Path, released: tuple[Path, str]
) -> None:
    project_dir = generate_released(released, tmp_path / "demo")

    text = (project_dir / ".github/workflows/ci.yml").read_text()
    workflow = yaml.safe_load(text)
    assert workflow["jobs"]["api-contract"]["uses"].endswith(f"api-contract.yml@{released[1]}")
    assert f"api-contract.yml@{released[1]} # v9.9.9\n" in text
    assert workflow["permissions"] == {"contents": "read"}


@pytest.mark.parametrize(
    ("backend", "frontend", "deploy"),
    [(*stack, "none") for stack in STACKS] + [("django", "nuxt", "vps")],
)
def test_a_released_project_scores_100_on_kiln_grid(
    tmp_path: Path, released: tuple[Path, str], backend: str, frontend: str, deploy: str
) -> None:
    """ion-repo asks of others' repos what it generates: a new project has no gap to close."""
    podman = (backend, frontend) in PODMAN_STACKS
    project_dir = generate_released(
        released,
        tmp_path / "demo",
        backend=backend,
        frontend=frontend,
        podman=podman,
        deploy=deploy,
    )

    report = score.score_repo(project_dir)

    # The lockfiles are written by `ion repo new` right after the template (`lock_dependencies`).
    expected = {"LOCKED-DEPENDENCIES"}
    if backend == "none" and frontend in ("nuxt", "next", "astro"):
        expected.add("TESTS-PRESENT")  # a front alone has no test yet (T-160)
    assert {gap.rule for gap in report.gaps} <= expected


def test_a_released_tool_published_on_pypi_scores_100_on_kiln_grid(
    tmp_path: Path, released: tuple[Path, str]
) -> None:
    project_dir = generate_released(
        released, tmp_path / "demo", project_type="cli", pypi_name="keramos-demo"
    )

    report = score.score_repo(project_dir)

    assert {gap.rule for gap in report.gaps} <= {"LOCKED-DEPENDENCIES"}


@pytest.mark.parametrize(("backend", "frontend"), PODMAN_STACKS)
def test_dependabot_watches_each_folder_of_the_project(
    tmp_path: Path, backend: str, frontend: str
) -> None:
    project_dir = generate(tmp_path / "demo", backend=backend, frontend=frontend, podman=True)

    config = yaml.safe_load((project_dir / ".github/dependabot.yml").read_text())
    manifests = {
        "uv": ("pyproject.toml",),
        "maven": ("pom.xml",),
        "npm": ("package.json",),
        "docker": ("Containerfile",),
        "github-actions": (".github/workflows/ci.yml",),
    }
    for update in config["updates"]:
        assert update["cooldown"] == {"default-days": 7}
        for folder in update["directories"]:
            assert any(
                (project_dir / folder.lstrip("/") / name).is_file()
                for name in manifests[update["package-ecosystem"]]
            ), (update["package-ecosystem"], folder)


def test_a_solo_project_has_no_codeowners(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", team=["antoine-tena"])

    assert not (project_dir / ".github/CODEOWNERS").exists()
    assert "## Team" in (project_dir / "README.md").read_text()


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
    return {path.name for path in (project_dir / ".claude/rules/ion-repo").glob("*.md")}


def test_the_size_chooses_the_rules(tmp_path: Path) -> None:
    tiny = generate(tmp_path / "tiny", size="tiny", backend="cli", frontend="none")
    large = generate(tmp_path / "large", size="large", podman=True)

    assert rule_files(tiny) == {"project.md", "charter.md", "python.md", "cli.md"}
    assert rule_files(large) >= {"django.md", "nuxt.md", "production.md", "security.md"}
    django_rules = (large / ".claude/rules/ion-repo/django.md").read_text()
    assert "[RLS]" in django_rules and "[OUTBOX]" in django_rules
    small_django = generate(tmp_path / "small", size="small")
    assert "[OUTBOX]" not in (small_django / ".claude/rules/ion-repo/django.md").read_text()


def test_rules_load_by_path_and_claude_md_stays_short(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo")

    for name in ("django.md", "nuxt.md", "python.md"):
        text = (project_dir / ".claude/rules/ion-repo" / name).read_text()
        assert text.startswith("---\npaths:\n"), name
    for name in ("project.md", "charter.md"):
        assert not (project_dir / ".claude/rules/ion-repo" / name).read_text().startswith("---")
    assert len((project_dir / "CLAUDE.md").read_text().splitlines()) < 60
    assert not (project_dir / "backend/CLAUDE.md").exists()


def test_the_project_language_rules_what_people_read(tmp_path: Path) -> None:
    french = generate(tmp_path / "fr", language="fr", backend="fastapi", frontend="streamlit")
    english = generate(tmp_path / "en", backend="fastapi", frontend="streamlit")

    assert (
        "Talk with the user in French" in (french / ".claude/rules/ion-repo/project.md").read_text()
    )
    assert "## Démarrage rapide" in (french / "README.md").read_text()
    assert "## Quick start" in (english / "README.md").read_text()
    french_texts = (french / "frontend/dashboard/constants.py").read_text()
    assert "Le backend ne répond pas" in french_texts
    assert "does not answer" in (english / "frontend/dashboard/constants.py").read_text()


def test_a_language_per_use(tmp_path: Path) -> None:
    project_dir = generate(
        tmp_path / "demo", language="fr", language_custom=True, language_commits="en"
    )

    project_rules = (project_dir / ".claude/rules/ion-repo/project.md").read_text()
    assert "English" in project_rules.split("Commit messages:", 1)[1][:12]


@pytest.mark.parametrize("frontend", ["streamlit", "dash"])
def test_vercel_is_refused_for_a_python_front(tmp_path: Path, frontend: str) -> None:
    with pytest.raises(ValueError, match="Vercel cannot host"):
        generate(tmp_path / "demo", backend="data", frontend=frontend, frontend_deploy="vercel")


def test_no_deployment_cites_no_deploy_workflow(tmp_path: Path) -> None:
    project_dir = generate(tmp_path / "demo", backend="data", frontend="streamlit")

    assert "deploy.yml" not in (project_dir / ".github/workflows/ci.yml").read_text()
    assert not (project_dir / "scripts").exists()


def test_large_files_kept_on_purpose_pass_the_size_ceiling(tmp_path: Path) -> None:
    default = generate(tmp_path / "default")
    hooks = yaml.safe_load((default / ".pre-commit-config.yaml").read_text())["repos"][0]["hooks"]
    large_files = next(hook for hook in hooks if hook["id"] == "check-added-large-files")
    assert "exclude" not in large_files
    assert "large_files" not in (default / ".copier-answers.yml").read_text()

    films = ["frontend/public/film.mp4", "frontend/public/film.webm"]
    project = generate(tmp_path / "films", large_files=films)
    hooks = yaml.safe_load((project / ".pre-commit-config.yaml").read_text())["repos"][0]["hooks"]
    pattern = next(hook for hook in hooks if hook["id"] == "check-added-large-files")["exclude"]
    assert all(re.match(pattern, film) for film in films)
    assert not re.match(pattern, "frontend/public/filmXmp4")
    assert not re.match(pattern, "frontend/public/other.mp4")
    assert "large_files:" in (project / ".copier-answers.yml").read_text()


@pytest.mark.parametrize(("bot", "cron"), [("weekly", "0 6 * * 1"), ("monthly", "0 6 1 * *")])
def test_kiln_bot_runs_on_its_schedule_and_is_off_by_default(
    tmp_path: Path, bot: str, cron: str
) -> None:
    """T-59: off by default (a private repo pays its minutes), the answer kept only when set."""
    default = generate(tmp_path / "default")
    assert not (default / ".github/workflows/kiln-bot.yml").exists()
    assert "update_bot" not in (default / ".copier-answers.yml").read_text()

    project = generate(tmp_path / bot, update_bot=bot)
    workflow = yaml.safe_load((project / ".github/workflows/kiln-bot.yml").read_text())
    assert workflow[True]["schedule"] == [{"cron": cron}]
    job = workflow["jobs"]["bot"]
    assert job["uses"].startswith("antoine-tena/ion-repo/.github/workflows/bot.yml@")
    assert job["secrets"] == {"token": "${{ secrets.KILN_BOT_TOKEN }}"}
    assert f"update_bot: {bot}" in (project / ".copier-answers.yml").read_text()

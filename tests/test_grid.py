"""The grid as data (T-123): every rule holds, and its detector says pass and fail where it
should, on an example of each."""

import datetime
import json
import re
import sys
from pathlib import Path

import pytest

from kiln import cli
from kiln.grid import detectors, facts, fixers, forge, model
from kiln.grid.facts import read_repo
from kiln.shell import KilnError

RULES = model.load_rules()
WORKFLOW = ".github/workflows/ci.yml"
# A case of a forge rule: the GitHub settings `gh` would read, as JSON, under this name.
FORGE = "<github settings>"
GITHUB = {
    "slug": "acme/app",
    "default_branch": "main",
    "public": True,
    "merge_commits": True,
    "branch_rules": ["deletion", "non_fast_forward"],
    "secret_scanning": True,
    "push_protection": True,
    "vulnerability_alerts": True,
    "security_updates": True,
    "private_reporting": True,
    "code_scanning": True,
}


def github(**changes: object) -> dict[str, str]:
    return {FORGE: json.dumps({**GITHUB, **changes})}


def given_github(files: dict[str, str], monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    """The settings of a forge case handed to the rule as `gh` would read them; the files."""
    if FORGE in files:
        data = json.loads(files[FORGE])
        settings = forge.Settings(**{**data, "branch_rules": tuple(data["branch_rules"])})
        monkeypatch.setattr(forge, "settings", lambda root: settings)
    return {name: content for name, content in files.items() if name != FORGE}


SHA = "b4ffde65f46336ab88eb53be808477a3936bae11"

# For each rule, a repo that passes and one that fails (doctrine 7: a rule that flags wrongly
# is worse than none). Files as {path: content}.
CASES: dict[str, dict[str, dict[str, str]]] = {
    "PROTECTED-BRANCH": {
        "pass": github(
            merge_commits=False, branch_rules=[*GITHUB["branch_rules"], "required_linear_history"]
        ),
        "fail": github(branch_rules=["deletion"]),
    },
    "FORGE-SECRET-SCANNING": {"pass": github(), "fail": github(push_protection=False)},
    "DEPENDABOT-ALERTS": {"pass": github(), "fail": github(security_updates=False)},
    "PRIVATE-VULN-REPORTING": {"pass": github(), "fail": github(private_reporting=False)},
    "CODE-SCANNING": {"pass": github(), "fail": github(code_scanning=False)},
    "LOCKED-DEPENDENCIES": {
        "pass": {
            "backend/pyproject.toml": '[project]\nname = "a"\ndependencies = ["django"]\n',
            "backend/uv.lock": "",
            "frontend/package.json": '{"dependencies": {"nuxt": "4"}}',
            "pnpm-lock.yaml": "",
            "tools/pyproject.toml": "[tool.ruff]\nline-length = 100\n",
        },
        "fail": {"pyproject.toml": '[project]\nname = "a"\ndependencies = ["httpx"]\n'},
    },
    "PINNED-ACTIONS": {
        "pass": {
            WORKFLOW: f"jobs:\n  a:\n    steps:\n      - uses: actions/checkout@{SHA} # v4\n"
            "      - uses: ./.github/actions/local\n      - uses: docker://alpine:3\n"
        },
        "fail": {WORKFLOW: "jobs:\n  a:\n    steps:\n      - uses: actions/checkout@v4\n"},
    },
    "DEPENDENCY-UPDATES": {
        "pass": {".github/dependabot.yml": "version: 2\n"},
        "fail": {"README.md": "# a\n"},
    },
    "UPDATE-COOLDOWN": {
        "pass": {
            ".github/dependabot.yml": "version: 2\nupdates:\n  - package-ecosystem: uv\n"
            "    cooldown:\n      default-days: 7\n"
        },
        "fail": {".github/dependabot.yml": "version: 2\nupdates:\n  - package-ecosystem: uv\n"},
    },
    "NON-ROOT-CONTAINERS": {
        "pass": {"Containerfile": "FROM python:3.14\nUSER root\nRUN true\nUSER app\n"},
        "fail": {"backend/Dockerfile": "FROM python:3.14\nUSER app\nUSER root\n"},
    },
    "NO-TRACKED-ENV": {
        "pass": {".env.example": "SECRET=\n"},
        "fail": {"backend/.env": "SECRET=real\n"},
    },
    "IMAGES-BY-DIGEST": {
        "pass": {
            "Containerfile": f"FROM python:3.14-slim@sha256:{'a' * 64} AS build\nFROM build\n"
            "FROM scratch\nFROM ${BASE}\n"
        },
        "fail": {"Dockerfile": "FROM node:24\n"},
    },
    "HARDENED-CONTAINERS": {
        "pass": {
            "compose.yml": "services:\n  web:\n    read_only: true\n    cap_drop: [ALL]\n"
            "    security_opt: [no-new-privileges:true]\n"
        },
        "fail": {"compose.yml": "services:\n  web:\n    image: a\n"},
    },
    "MIGRATIONS": {
        "pass": {
            "shop/apps.py": "",
            "shop/models.py": "",
            "shop/migrations/__init__.py": "",
        },
        "fail": {"shop/apps.py": "", "shop/models/__init__.py": ""},
    },
    "VULNERABILITY-AUDIT": {
        "pass": {WORKFLOW: "jobs:\n  a:\n    steps:\n      - run: uvx pip-audit\n"},
        "fail": {WORKFLOW: "jobs:\n  a:\n    steps:\n      - run: pytest\n"},
    },
    "REPO-MAP": {
        "pass": {
            "CLAUDE.md": "# a\n\n## Repo map\n\n- `src/`: code\n",
            "ARCHITECTURE.md": "# Architecture\n\n## Code map\n",
        },
        "fail": {"CLAUDE.md": "# a\n\n## Rules\n"},
    },
    "AI-CONTEXT": {
        "pass": {"AGENTS.md": "# a\n", ".claude/settings.json": "{}"},
        "fail": {"README.md": "# a\n", ".cursor/rules.md": "# a\n"},
    },
    "STRICT-TS": {
        "pass": {
            "tsconfig.json": '{"compilerOptions": {"strict": true}}',
            "frontend/tsconfig.json": '{"extends": "./.nuxt/tsconfig.json"}',
            "frontend/nuxt.config.ts": "export default defineNuxtConfig({})\n",
            "site/tsconfig.json": '{"extends": "astro/tsconfigs/strictest"}',
        },
        "fail": {
            "tsconfig.json": '{"compilerOptions": {"strict": false}}',
            "site/tsconfig.json": '{"extends": "astro/tsconfigs/base"}',
        },
    },
    "NO-ANY": {
        "pass": {"a.ts": "// works for any input\nconst x: unknown = 1\n"},
        "fail": {"a.ts": "const x: any = 1\n"},
    },
    "STRICT-TYPING": {
        "pass": {"pyproject.toml": "[tool.mypy]\nstrict = true\n"},
        "fail": {"pyproject.toml": "[tool.mypy]\npython_version = '3.14'\n"},
    },
    "HEALTH-PROBES": {
        "pass": {"Containerfile": "FROM a\nHEALTHCHECK CMD curl -f http://localhost/\n"},
        "fail": {"Containerfile": "FROM a\n"},
    },
    "WORKFLOW-PERMISSIONS": {
        "pass": {WORKFLOW: "permissions: {}\njobs:\n  a:\n    runs-on: x\n"},
        "fail": {WORKFLOW: "jobs:\n  a:\n    runs-on: x\n"},
    },
    "WORKFLOW-INJECTION": {
        "pass": {WORKFLOW: 'jobs:\n  a:\n    steps:\n      - run: echo "$TITLE"\n'},
        "fail": {
            WORKFLOW: "jobs:\n  a:\n    steps:\n"
            '      - run: echo "${{ github.event.pull_request.title }}"\n'
        },
    },
    "PULL-REQUEST-TARGET": {
        "pass": {WORKFLOW: "on:\n  pull_request:\n"},
        "fail": {WORKFLOW: "on:\n  pull_request_target:\n"},
    },
    "SECRET-SCAN": {
        "pass": {
            ".pre-commit-config.yaml": "repos:\n  - repo: https://github.com/gitleaks/gitleaks\n"
        },
        "fail": {WORKFLOW: "jobs: {}\n"},
    },
    "CI-PRESENT": {"pass": {".gitlab-ci.yml": "test: {}\n"}, "fail": {"README.md": "# a\n"}},
    "TESTS-IN-CI": {
        "pass": {WORKFLOW: "jobs:\n  a:\n    steps:\n      - run: uv run pytest -q\n"},
        "fail": {WORKFLOW: "jobs:\n  a:\n    steps:\n      - run: echo hi\n"},
    },
    "LINT-IN-CI": {
        "pass": {WORKFLOW: "jobs:\n  a:\n    steps:\n      - run: pnpm lint\n"},
        "fail": {WORKFLOW: "jobs:\n  a:\n    steps:\n      - run: echo hi\n"},
    },
    "MODEL-TRACED": {
        "pass": {
            "data/models/model.joblib": "weights",
            "data/models/model.joblib.manifest.json": '{"code_sha256": "ab", "metrics": {}}',
        },
        "fail": {"data/models/model.joblib": "weights"},
    },
    "TESTS-PRESENT": {
        "pass": {"backend/tests/test_api.py": "def test_a(): ...\n"},
        "fail": {"app.py": "print(1)\n"},
    },
    "SUPPORTED-RUNTIMES": {
        "pass": {".python-version": "3.14\n", "Containerfile": "FROM node:24-slim\n"},
        "fail": {"frontend/.nvmrc": "18\n"},
    },
    "CURRENT-DEBIAN": {
        "pass": {"Containerfile": "FROM python:3.14-slim-trixie\n"},
        "fail": {"Containerfile": "FROM python:3.12-slim-bookworm\n"},
    },
    "NO-OBSOLETE-BACKPORTS": {
        "pass": {"requirements.txt": "dataclasses-json==0.6\ntyping-extensions==4.15\n"},
        "fail": {"requirements.txt": "flask==3.1\ntyping==3.7.4.3\n"},
    },
    "BARE-EXCEPT": {
        "pass": {"a.py": "try:\n    pass\nexcept ValueError:\n    pass\n"},
        "fail": {"a.py": "try:\n    pass\nexcept:\n    pass\n"},
    },
    "NOQA-CODES": {
        "pass": {"a.py": "import os  # noqa: F401\n"},
        "fail": {"a.py": "import os  # noqa\n"},
    },
    "TYPE-IGNORE-CODES": {
        "pass": {"a.py": "x = f()  # type: ignore[no-untyped-call]\n"},
        "fail": {"a.py": "x = f()  # type: ignore\n"},
    },
    "TS-EXPECT-ERROR": {
        "pass": {"a.ts": "// @ts-expect-error: untyped lib\n"},
        "fail": {"a.vue": '<script setup lang="ts">\n// @ts-ignore\n</script>\n'},
    },
    "NAIVE-DATETIMES": {
        "pass": {
            "a.py": "now = datetime.now(UTC)\nlater = timezone.now()\n"
            "local = datetime.now().astimezone()\n"
        },
        "fail": {"a.py": "now = datetime.datetime.utcnow()\n"},
    },
    "SQL-PARAMETERS": {
        "pass": {"a.py": 'cursor.execute("SELECT 1 WHERE id = %s", [pk])\n'},
        "fail": {"a.py": 'cursor.execute(f"SELECT 1 WHERE id = {pk}")\n'},
    },
    "DJANGO-DEBUG-OFF": {
        "pass": {"config/settings.py": "DEBUG = env.bool('DEBUG', default=False)\n"},
        "fail": {"config/settings.py": "DEBUG = True\n"},
    },
    "DJANGO-SECRET-KEY": {
        "pass": {"config/settings/base.py": "SECRET_KEY = os.environ['SECRET_KEY']\n"},
        "fail": {"config/settings.py": "SECRET_KEY = 'django-insecure-abc'\n"},
    },
    "DJANGO-ALLOWED-HOSTS": {
        "pass": {"config/settings.py": "ALLOWED_HOSTS = ['example.org']\n"},
        "fail": {"config/settings.py": "ALLOWED_HOSTS = ['*']\n"},
    },
    "NO-V-HTML": {
        "pass": {"a.vue": "<template><p>{{ text }}</p></template>\n"},
        "fail": {"a.vue": '<template><p v-html="text" /></template>\n'},
    },
    "README": {"pass": {"README.md": "# a\n"}, "fail": {"docs/README.md": "# a\n"}},
    "JS-LINTER": {
        "pass": {"frontend/eslint.config.mjs": "export default []\n"},
        "fail": {"package.json": "{}"},
    },
    "PYTHON-LINTER": {
        "pass": {"pyproject.toml": "[tool.ruff]\nline-length = 100\n"},
        "fail": {"pyproject.toml": "[project]\nname = 'a'\n"},
    },
}


def make_repo(root: Path, files: dict[str, str]) -> facts.Repo:
    for name, content in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(content)
    return read_repo(root)


def test_the_grid_holds() -> None:
    assert RULES
    assert model.problems(RULES) == []


@pytest.mark.parametrize("rule", RULES, ids=lambda rule: rule.id)
def test_each_rule_can_run(rule: model.Rule) -> None:
    assert not rule.fixer or rule.fixer in fixers.FIXERS
    assert set(rule.applies) <= set(facts.KNOWN_FACTS)
    if rule.detector:
        assert detectors.problems(rule.detector) == []
        assert rule.id in CASES, "a detected rule ships with a passing and a failing example"


DETECTED = [rule for rule in RULES if rule.detector]


@pytest.mark.parametrize("rule", DETECTED, ids=lambda rule: rule.id)
@pytest.mark.parametrize("expected", ["pass", "fail"])
def test_each_rule_says_pass_and_fail_where_it_should(
    tmp_path: Path, rule: model.Rule, expected: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = make_repo(tmp_path, given_github(CASES[rule.id][expected], monkeypatch))

    outcome = detectors.detect(rule.detector, repo)

    assert outcome.status == expected, outcome
    if expected == "fail":
        assert outcome.locations or outcome.detail


def test_requirements_pinned_to_exact_versions_are_their_own_lock(tmp_path: Path) -> None:
    rule = next(rule for rule in RULES if rule.id == "LOCKED-DEPENDENCIES")
    pinned = make_repo(
        tmp_path / "pinned", {"requirements.txt": "-r base.txt\nflask==3.1  # web\n"}
    )
    loose = make_repo(tmp_path / "loose", {"api/requirements.txt": "flask>=3\n"})

    assert detectors.detect(rule.detector, pinned).status == detectors.PASS
    assert detectors.detect(rule.detector, loose).locations == ("api/requirements.txt",)


@pytest.mark.parametrize(
    "line",
    [
        """cursor.execute("SELECT id FROM book WHERE title LIKE '%%%s%%'" % q)""",
        """cursor.execute('SELECT id FROM book WHERE title = "{}"'.format(q))""",
    ],
)
def test_sql_formatted_around_quotes_of_the_other_kind_is_caught(tmp_path: Path, line: str) -> None:
    rule = next(rule for rule in RULES if rule.id == "SQL-PARAMETERS")
    repo = make_repo(tmp_path, {"views.py": f"{line}\n"})

    assert detectors.detect(rule.detector, repo).locations == ("views.py:1",)


@pytest.mark.parametrize(
    "test_file",
    [
        "Converter.Tests/ExtractTests.cs",
        "src/socialnetwork/BavardTest.java",
        "tests/BookTest.php",
        "tests/tests.rs",
        "spec/models/user_spec.rb",
        "test/models/user_test.rb",
        "test/base-url.ts",
        "test/app_test.exs",
        "test/widget_test.dart",
        "Tests/AppTests/AppTests.swift",
        "tests/parse.cpp",
    ],
)
def test_tests_are_found_in_every_common_stack(tmp_path: Path, test_file: str) -> None:
    rule = next(rule for rule in RULES if rule.id == "TESTS-PRESENT")
    repo = make_repo(tmp_path, {test_file: "// a test\n"})

    assert detectors.detect(rule.detector, repo).status == detectors.PASS


@pytest.mark.parametrize(
    ("rule_id", "step"),
    [
        ("TESTS-IN-CI", "run: bundle exec rake spec"),
        ("TESTS-IN-CI", "run: php artisan test"),
        ("TESTS-IN-CI", "run: ./mvnw -B verify"),
        ("TESTS-IN-CI", "run: ./gradlew build"),
        ("TESTS-IN-CI", "run: dotnet test"),
        ("TESTS-IN-CI", "run: mix test"),
        ("TESTS-IN-CI", "run: npx ava"),
        ("LINT-IN-CI", "run: cargo clippy --all-targets -- -Dwarnings"),
        ("LINT-IN-CI", "uses: golangci/golangci-lint-action@v9"),
        ("LINT-IN-CI", "run: bundle exec rubocop"),
        ("LINT-IN-CI", "run: vendor/bin/phpstan analyse"),
        ("LINT-IN-CI", "run: ./gradlew ktlintCheck detekt"),
        ("LINT-IN-CI", "run: dotnet format --verify-no-changes"),
        ("LINT-IN-CI", "run: flutter analyze"),
    ],
)
def test_the_ci_of_every_common_stack_is_read(tmp_path: Path, rule_id: str, step: str) -> None:
    rule = next(rule for rule in RULES if rule.id == rule_id)
    repo = make_repo(tmp_path, {WORKFLOW: f"jobs:\n  a:\n    steps:\n      - {step}\n"})

    assert detectors.detect(rule.detector, repo).status == detectors.PASS


def test_a_linter_bound_to_the_build_runs_with_it(tmp_path: Path) -> None:
    rule = next(rule for rule in RULES if rule.id == "LINT-IN-CI")
    plugin = "<plugin><artifactId>maven-checkstyle-plugin</artifactId></plugin>\n"
    repo = make_repo(tmp_path, {"pom.xml": plugin})

    assert detectors.detect(rule.detector, repo).status == detectors.PASS


def test_nothing_to_look_at_is_not_a_pass(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, {"README.md": "# a\n"})
    rules = {rule.id: rule for rule in RULES}

    for rule_id in ("PINNED-ACTIONS", "UPDATE-COOLDOWN", "NON-ROOT-CONTAINERS"):
        assert detectors.detect(rules[rule_id].detector, repo).status == detectors.NOT_APPLICABLE


def test_a_failing_regex_says_where(tmp_path: Path) -> None:
    rule = next(rule for rule in RULES if rule.id == "PINNED-ACTIONS")
    repo = make_repo(tmp_path, {WORKFLOW: f"steps:\n  - uses: a/b@{SHA}\n  - uses: c/d@main\n"})

    assert detectors.detect(rule.detector, repo).locations == (f"{WORKFLOW}:3",)


@pytest.mark.parametrize(
    ("rule_id", "source"),
    [
        ("NOQA-CODES", 'FAILING = "import os  # noqa\\n"\n'),
        ("TYPE-IGNORE-CODES", 'def f() -> None:\n    """Never `x = g()  # type: ignore`."""\n'),
        ("NAIVE-DATETIMES", "FAILING = 'now = datetime.utcnow()'  # not datetime.now()\n"),
        ("SQL-PARAMETERS", "FAILING = 'cursor.execute(f\"SELECT {pk}\")'\n"),
    ],
)
def test_a_python_rule_reads_code_not_the_text_of_its_strings(
    tmp_path: Path, rule_id: str, source: str
) -> None:
    rule = next(rule for rule in RULES if rule.id == rule_id)
    repo = make_repo(tmp_path, {"tests/test_a.py": source})

    assert detectors.detect(rule.detector, repo).status == detectors.PASS


def test_code_and_comments_beside_a_string_are_still_read(tmp_path: Path) -> None:
    rules = {rule.id: rule for rule in RULES}
    repo = make_repo(
        tmp_path,
        {
            "a.py": 'x = "# noqa"  # noqa\nwhen = f"at {datetime.now()}"\n',
            "b.py": 'y = 1  # noqa\n"""never closed\n',  # does not tokenize: read whole
        },
    )

    noqa = detectors.detect(rules["NOQA-CODES"].detector, repo)
    naive = detectors.detect(rules["NAIVE-DATETIMES"].detector, repo)

    assert sorted(noqa.locations) == ["a.py:1", "b.py:1"]
    assert naive.locations == ("a.py:2",)
    assert detectors.problems({"kind": "regex", "files": "*.py", "pattern": "x", "within": "doc"})


def test_the_grid_catches_its_own_mistakes(tmp_path: Path) -> None:
    rule = RULES[0]
    old = datetime.date(2020, 1, 1)
    stale = model.Rule(
        **{
            **rule.__dict__,
            "theme": "nowhere",
            "level": "adopt",
            "sources": (model.Source("https://x.org", "rumour", old),),
        }
    )

    found = model.problems([rule, rule, stale], today=datetime.date(2026, 10, 19))

    assert any("ID already used" in problem for problem in found)
    assert any("theme 'nowhere'" in problem for problem in found)
    assert any("source kind 'rumour'" in problem for problem in found)
    assert any("last six months" in problem for problem in found)


def test_a_broken_rule_file_is_named(tmp_path: Path) -> None:
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests/BROKEN.toml").write_text('id = "BROKEN"\n')

    with pytest.raises(model.GridError, match=r"BROKEN\.toml"):
        model.load_rules(tmp_path)


def test_facts_of_a_django_and_nuxt_repo(tmp_path: Path) -> None:
    repo = make_repo(
        tmp_path,
        {
            "backend/pyproject.toml": '[project]\nname = "a"\ndependencies = ["Django>=5.2"]\n',
            "backend/uv.lock": "",
            "frontend/package.json": '{"dependencies": {"nuxt": "^4.1"}}',
            "frontend/tsconfig.json": "{}",
            "pnpm-lock.yaml": "",
            WORKFLOW: "on: push\n",
            "compose.yaml": "services: {}\n",
        },
    )

    assert repo.facts == {
        "python", "uv", "django", "javascript", "typescript", "pnpm", "nuxt", "vue",
        "github-actions", "containers",
    }  # fmt: skip


def run_kiln(monkeypatch: pytest.MonkeyPatch, *arguments: str) -> int:
    monkeypatch.setattr(sys, "argv", ["kiln", *arguments])
    try:
        cli.main()
    except SystemExit as exit_request:
        return int(exit_request.code or 0)
    return 0


def test_kiln_grid_lists_and_shows(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    assert run_kiln(monkeypatch, "grid", "--theme", "supply-chain") == 0
    listed = capsys.readouterr().out
    assert "PINNED-ACTIONS" in listed and "NON-ROOT-CONTAINERS" not in listed

    assert run_kiln(monkeypatch, "grid", "pinned-actions") == 0
    shown = capsys.readouterr().out
    assert "docs.github.com" in shown and "kiln waive PINNED-ACTIONS" in shown


def test_an_unknown_rule_suggests_the_close_ones() -> None:
    from kiln.grid.show import find_rule

    with pytest.raises(KilnError, match=r"did you mean PINNED-ACTIONS\?"):
        find_rule("ACTIONS")
    with pytest.raises(KilnError, match="did you mean PINNED-ACTIONS"):
        find_rule("PINED-ACTION")


def test_a_rule_names_only_charter_rules_kiln_knows() -> None:
    template = Path(__file__).resolve().parent.parent / "template"
    known = {
        found
        for path in [*template.glob(".claude/rules/kiln/*.jinja"), template / "charter.toml.jinja"]
        for found in re.findall(r"\[([A-Z0-9+-]{3,})\]|id = \"([A-Z0-9+-]+)\"", path.read_text())
        for found in found
        if found
    }

    assert {rule.charter_rule for rule in RULES if rule.charter_rule} <= known


def test_drafts_wait_behind_their_level(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    assert run_kiln(monkeypatch, "grid") == 0
    default = capsys.readouterr().out
    assert "PINNED-ACTIONS" in default and "SEALED-DOMAIN" not in default
    assert "kiln grid --level assess" in default

    assert run_kiln(monkeypatch, "grid", "--level", "assess") == 0
    assert "SEALED-DOMAIN" in capsys.readouterr().out

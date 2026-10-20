"""The grid as data (T-123): every rule holds, and its detector says pass and fail where it
should, on an example of each."""

import datetime
import re
import sys
from pathlib import Path

import pytest

from kiln import cli
from kiln.grid import detectors, facts, fixers, model
from kiln.grid.facts import read_repo
from kiln.shell import KilnError

RULES = model.load_rules()
WORKFLOW = ".github/workflows/ci.yml"
SHA = "b4ffde65f46336ab88eb53be808477a3936bae11"

# For each rule, a repo that passes and one that fails (doctrine 7: a rule that flags wrongly
# is worse than none). Files as {path: content}.
CASES: dict[str, dict[str, dict[str, str]]] = {
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
    tmp_path: Path, rule: model.Rule, expected: str
) -> None:
    repo = make_repo(tmp_path, CASES[rule.id][expected])

    outcome = detectors.detect(rule.detector, repo)

    assert outcome.status == expected, outcome
    if expected == "fail":
        assert outcome.locations or outcome.detail


def test_nothing_to_look_at_is_not_a_pass(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, {"README.md": "# a\n"})
    rules = {rule.id: rule for rule in RULES}

    for rule_id in ("PINNED-ACTIONS", "UPDATE-COOLDOWN", "NON-ROOT-CONTAINERS"):
        assert detectors.detect(rules[rule_id].detector, repo).status == detectors.NOT_APPLICABLE


def test_a_failing_regex_says_where(tmp_path: Path) -> None:
    rule = next(rule for rule in RULES if rule.id == "PINNED-ACTIONS")
    repo = make_repo(tmp_path, {WORKFLOW: f"steps:\n  - uses: a/b@{SHA}\n  - uses: c/d@main\n"})

    assert detectors.detect(rule.detector, repo).locations == (f"{WORKFLOW}:3",)


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

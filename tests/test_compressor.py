"""The compressor (T-139): what it may remove, how it cuts, and that nothing unproven stays out."""

import ast
import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest

from kiln.grid import compressor
from kiln.grid.compressor import candidates, proof, removal
from kiln.grid.compressor.candidates import CODE, DEPENDENCY, Candidate
from kiln.grid.facts import read_repo
from kiln.shell import KilnError

CORE = textwrap.dedent(
    '''\
    import json


    def used():
        return 1


    # An old exporter.
    @property
    def dead():
        return json.dumps({})


    class Box:
        """A box."""

        def only(self):
            return 2


    class Model(Base):
        def save(self):
            return 3


    @receiver(signal)
    def on_save():
        return 4
    '''
)


def make(root: Path, files: dict[str, str]) -> Path:
    for name, content in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(content)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    return root


def guard(
    root: Path, path: str, name: str, line: int, executed: dict[str, set[int]] | None = None
) -> str:
    repo = read_repo(root)
    located = candidates.locate(root / path, name, line)
    assert located is not None
    qualname, node, parents = located
    found = Candidate(CODE, path, qualname, "vulture")
    return candidates._guard_code(
        repo, found, node, parents, candidates._word_index(repo), False, executed
    )


def test_a_definition_is_cut_with_its_decorators_and_comment(tmp_path: Path) -> None:
    path = tmp_path / "core.py"
    path.write_text(CORE)
    assert removal._cut_definition(path, "dead")
    text = path.read_text()
    assert "dead" not in text and "An old exporter" not in text and "@property" not in text
    assert "\n\n\n\n" not in text
    ast.parse(text)


def test_the_last_method_of_a_class_leaves_pass(tmp_path: Path) -> None:
    path = tmp_path / "core.py"
    path.write_text(CORE)
    assert removal._cut_definition(path, "Box.only")
    assert 'class Box:\n    """A box."""\n\n\nclass Model' in path.read_text()
    lone = tmp_path / "lone.py"
    lone.write_text("class A:\n    def f(self):\n        return 1\n")
    assert removal._cut_definition(lone, "A.f")
    assert lone.read_text() == "class A:\n    pass\n"


def test_a_definition_already_gone_is_not_removed_twice(tmp_path: Path) -> None:
    path = tmp_path / "core.py"
    path.write_text(CORE)
    assert removal._cut_definition(path, "dead")
    assert not removal._cut_definition(path, "dead")


def test_vulture_line_of_a_property_is_its_decorator(tmp_path: Path) -> None:
    path = tmp_path / "core.py"
    path.write_text(CORE)
    located = candidates.locate(path, "dead", 9)
    assert located is not None
    qualname, node, _ = located
    assert qualname == "dead" and node.lineno == 10


@pytest.mark.parametrize(
    ("name", "line", "reason"),
    [
        ("save", 22, "inherits"),
        ("on_save", 26, "decorated by receiver"),
    ],
)
def test_what_a_framework_calls_is_kept(tmp_path: Path, name: str, line: int, reason: str) -> None:
    make(tmp_path, {"app/core.py": CORE})
    assert reason in guard(tmp_path, "app/core.py", name, line)


def test_a_plain_dead_function_is_left_to_the_proof(tmp_path: Path) -> None:
    make(tmp_path, {"app/core.py": CORE})
    assert guard(tmp_path, "app/core.py", "dead", 9) == ""


@pytest.mark.parametrize(
    ("files", "reason"),
    [
        ({"app/views.py": CORE, "templates/a.html": "{{ box.dead }}"}, "named in templates/a.html"),
        ({"app/views.py": CORE + '\ngetattr(x, "dead")\n'}, "named in app/views.py"),
        ({"app/migrations/0001.py": CORE}, "by convention"),
        ({"app/crypto/keys.py": CORE}, "never touched"),
        ({"app/views.py": "import hashlib\n" + CORE}, "never touched"),
        ({"app/views.py": CORE + '\n__all__ = ["dead"]\n'}, "listed in __all__"),
    ],
)
def test_guards_keep_what_a_static_tool_cannot_see(
    tmp_path: Path, files: dict[str, str], reason: str
) -> None:
    make(tmp_path, files)
    path = next(iter(files))
    line = 10 if path.endswith("views.py") and files[path].startswith("import hashlib") else 9
    assert reason in guard(tmp_path, path, "dead", line)


def test_code_the_tests_ran_is_alive(tmp_path: Path) -> None:
    make(tmp_path, {"app/core.py": CORE})
    assert "ran during the tests" in guard(
        tmp_path, "app/core.py", "dead", 9, {"app/core.py": {11}}
    )
    assert guard(tmp_path, "app/core.py", "dead", 9, {"app/core.py": {10}}) == ""


def test_a_dependency_loaded_by_name_or_named_in_a_config_is_kept(tmp_path: Path) -> None:
    make(tmp_path, {"Dockerfile": "CMD granian app\n", "deploy.sh": "celery -A app worker\n"})
    kept, skipped = candidates._guard_dependencies(
        read_repo(tmp_path), "pyproject.toml", ["psycopg", "rich", "celery", "Pillow"], "deptry"
    )
    assert [item.name for item in kept] == ["rich"]
    assert {item.candidate.name for item in skipped} == {"psycopg", "celery", "Pillow"}


def test_a_plugin_found_by_its_entry_points_is_kept(tmp_path: Path) -> None:
    info = (
        tmp_path
        / ".venv/lib/python3.14/site-packages/opentelemetry_instrumentation_django-0.1.dist-info"
    )
    info.mkdir(parents=True)
    (info / "entry_points.txt").write_text("[opentelemetry_instrumentor]\ndjango = a:B\n")
    command = tmp_path / ".venv/lib/python3.14/site-packages/rich-1.0.dist-info"
    command.mkdir(parents=True)
    (command / "entry_points.txt").write_text("[console_scripts]\nrich = rich:main\n")
    make(tmp_path, {"app.py": ""})
    names = ["opentelemetry-instrumentation-django", "rich"]
    kept, skipped = candidates._guard_dependencies(read_repo(tmp_path), "pyproject.toml", names, "")
    assert [item.name for item in kept] == ["rich"]
    assert "plugin" in skipped[0].reason


@pytest.mark.parametrize(
    "name",
    ["web/app/a.spec.ts", "web/e2e/b.ts", "web/lighthouserc.cjs", "web/vitest.config.ts"],
)
def test_tests_and_configs_are_never_deleted(tmp_path: Path, name: str) -> None:
    make(tmp_path, {name: "x"})
    assert "a test, a script or a config" in candidates._guard_file(
        read_repo(tmp_path), name, "web"
    )


def test_a_mention_in_the_docs_is_not_a_call(tmp_path: Path) -> None:
    make(tmp_path, {"app/core.py": CORE, "docs/audit.md": "dead() is used", "README.md": "dead"})
    assert guard(tmp_path, "app/core.py", "dead", 9) == ""


def test_a_node_dependency_is_dropped_keeping_the_indent(tmp_path: Path) -> None:
    manifest = tmp_path / "package.json"
    manifest.write_text('{\n    "dependencies": {"lodash": "4", "vue": "3"}\n}\n')
    assert removal._drop_node_dependency(manifest, "lodash")
    assert manifest.read_text() == '{\n    "dependencies": {\n        "vue": "3"\n    }\n}\n'


def test_junit_outcomes_are_read_test_by_test(tmp_path: Path) -> None:
    report = tmp_path / "junit.xml"
    report.write_text(
        '<testsuites><testsuite><testcase classname="t" name="a"/>'
        '<testcase classname="t" name="b"><failure/></testcase>'
        '<testcase classname="t" name="c"><skipped/></testcase></testsuite></testsuites>'
    )
    assert proof._junit(report) == {"t::a": "passed", "t::b": "failed", "t::c": "skipped"}


def test_a_known_failure_does_not_block_and_a_new_one_does(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    step = proof.Step("pytest", proof.TESTS, ("pytest",), per_test=True)
    base = proof.Baseline(steps=[step], outcomes={"t::a": "passed", "t::b": "failed"})
    monkeypatch.setattr(proof, "_pytest", lambda root, step: {"t::a": "passed", "t::b": "failed"})
    assert proof.holds(tmp_path, base) == ""
    monkeypatch.setattr(proof, "_pytest", lambda root, step: {"t::b": "failed"})
    assert proof.holds(tmp_path, base) == "pytest: t::a missing"


def test_a_removal_runs_only_the_steps_of_its_project(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ran: list[str] = []

    def run(root: Path, command: tuple[str, ...]) -> bool:
        ran.append(command[0])
        return True

    monkeypatch.setattr(proof, "_run", run)
    steps = [
        proof.Step("backend: mypy", proof.TYPES, ("mypy",), folder="backend"),
        proof.Step("frontend: pnpm run test", proof.TESTS, ("pnpm",), folder="frontend"),
    ]
    assert proof.holds(tmp_path, proof.Baseline(steps=steps), ["backend/a.py"]) == ""
    assert ran == ["mypy"]


def test_no_test_that_passes_proves_nothing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(proof, "_pytest", lambda root, step, data=None: {"t::a": "failed"})
    monkeypatch.setattr(shutil, "which", lambda name: name)
    base = proof.baseline(tmp_path, [proof.Step("pytest", proof.TESTS, ("pytest",), True)])
    assert not base.proves and base.dropped == ["pytest: no test passes"]


def test_without_tests_nothing_is_removed(tmp_path: Path) -> None:
    make(tmp_path, {"app/core.py": CORE})
    with pytest.raises(KilnError, match="no tests to prove"):
        compressor.compress(read_repo(tmp_path), compressor.CODE_PHASE)


def test_a_breaking_removal_is_found_by_halves_and_put_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Eight candidates, one that breaks the tests: found in a handful of runs, not eight,
    and the seven others removed."""
    tree: set[str] = set()  # what is removed now
    accepted: set[str] = set()  # what the last checkpoint holds

    def checkpoint(root: Path) -> None:
        accepted.clear()
        accepted.update(tree)

    def undo(root: Path) -> None:
        tree.clear()
        tree.update(accepted)

    def remove(root: Path, item: Candidate) -> bool:
        tree.add(item.name)
        return True

    monkeypatch.setattr(removal, "remove", remove)
    monkeypatch.setattr(removal, "sync_environment", lambda root, folders: None)
    monkeypatch.setattr(compressor, "_checkpoint", checkpoint)
    monkeypatch.setattr(compressor, "_undo", undo)
    monkeypatch.setattr(
        proof, "holds", lambda root, base, touched: "t::a failed" if "p5" in tree else ""
    )
    batch = [Candidate(DEPENDENCY, "pyproject.toml", f"p{index}", "deptry") for index in range(8)]
    report = compressor.Report()
    kept = compressor._settle(tmp_path, batch, proof.Baseline(steps=[]), report)
    assert (
        sorted(item.name for item in kept) == sorted(tree) == [f"p{i}" for i in range(8) if i != 5]
    )
    assert [item.name for item, _ in report.rejected] == ["p5"]
    assert report.proofs == 7


@pytest.mark.e2e
def test_a_real_repo_loses_its_dead_code_and_keeps_its_tests_green(tmp_path: Path) -> None:
    """vulture, deptry and uv for real: two rounds (a helper only dead code called), a call by
    `getattr` and one by `globals()` kept, an unused dependency removed with its lock."""
    root = make(
        tmp_path,
        {
            "pyproject.toml": '[project]\nname = "s"\nversion = "0"\nrequires-python = ">=3.12"\n'
            'dependencies = ["six"]\n\n[dependency-groups]\ndev = ["pytest"]\n\n'
            '[tool.pytest.ini_options]\npythonpath = ["."]\n',
            "app/__init__.py": "",
            "app/core.py": "import json\n\n\ndef used():\n    return 1\n\n\n"
            "def dead():\n    return _helper()\n\n\ndef _helper():\n    return json.dumps(1)\n\n\n"
            "def by_name():\n    return 2\n\n\ndef hidden():\n    return 3\n\n\n"
            'def call():\n    return globals()["hid" + "den"]()\n',
            "tests/test_core.py": "from app.core import call, used\n\n\n"
            "def test_used():\n    assert used() == 1\n\n\n"
            'def test_call():\n    assert call() == 3\n    assert "by_name"\n',
        },
    )
    subprocess.run(["uv", "lock", "-q"], cwd=root, check=True)
    changed = compressor.remove_dead_code(read_repo(root))
    text = (root / "app/core.py").read_text()
    assert changed == ["app/core.py"]
    assert "def dead" not in text and "_helper" not in text and "import json" not in text
    assert "def by_name" in text and "def hidden" in text
    assert compressor.remove_unused_dependencies(read_repo(root)) == ["pyproject.toml"]
    assert "six" not in (root / "uv.lock").read_text()

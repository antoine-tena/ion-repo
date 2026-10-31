"""The public docs follow the code: a renamed command, plugin or workflow fails here."""

import argparse
import importlib.util
import json
import re
import tomllib
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parent.parent
READMES = ("README.md", "README.fr.md")
# The reference, in each language: everything ion-repo offers, looked up there.
REFERENCES = ("docs/reference.md", "docs/reference.fr.md")
# Where ion-repo goes, for people who never open the backlog: the releases drawn from its plan.
ROADMAPS = ("ROADMAP.md", "ROADMAP.fr.md")
DOCS = (*READMES, *REFERENCES, *ROADMAPS, "CONTRIBUTING.md")
MARKETPLACE = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())


def docs() -> dict[str, str]:
    return {name: (ROOT / name).read_text(encoding="utf-8") for name in DOCS}


def script(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, ROOT / f"scripts/{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def screenshots() -> ModuleType:
    return script("screenshots")


def recordings() -> dict[Path, Path]:
    """Each demo recorded by VHS (`docs/assets/*.tape`, replayed by hand) and the image it
    writes."""
    found = {}
    for tape in sorted((ROOT / "docs/assets").glob("*.tape")):
        output = re.search(r"^Output (\S+)$", tape.read_text(encoding="utf-8"), re.M)
        assert output, f"{tape.name} writes no image"
        found[ROOT / output.group(1)] = tape
    return found


def test_every_image_is_what_kiln_shows_today() -> None:
    for path, expected in screenshots().images().items():
        assert path.read_text(encoding="utf-8") == expected, (
            f"{path.name} is out of date: uv run python scripts/screenshots.py"
        )


@pytest.mark.parametrize("image", sorted(recordings()), ids=lambda path: path.name)
def test_a_recorded_demo_types_only_what_kiln_offers(image: Path) -> None:
    tape = recordings()[image]
    typed = re.findall(r'^Type "([^"]*)"', tape.read_text(encoding="utf-8"), re.M)
    labels = offered()

    unknown = []
    for line in typed:
        for name, arguments in re.findall(r"\b(?:kiln|ion repo) ([a-z][a-z-]*)([^&|;]*)", line):
            if f"command {name}" not in labels:
                unknown.append(f"ion-repo {name}")
            unknown += [
                option
                for option in re.findall(r"--[a-z][a-z-]*", arguments)
                if f"option {name} {option}" not in labels
            ]

    assert unknown == [], f"{tape.name} types {unknown}: replay it (vhs {tape.name})"
    # Recorded once per release, not at each test: it must at least be there, light enough
    # to open on a phone.
    assert image.is_file() and image.stat().st_size < 5_000_000, image.name


@pytest.mark.parametrize("readme", READMES)
def test_a_readme_shows_only_current_images_and_existing_commands(readme: str) -> None:
    from ion_repo import cli

    text = (ROOT / readme).read_text(encoding="utf-8")
    images = re.findall(r'(?:src|srcset)="(docs/assets/[^"]+)"', text)
    assert images and all((ROOT / image).is_file() for image in images), images
    made = {path.relative_to(ROOT).as_posix() for path in [*screenshots().images(), *recordings()]}
    assert set(images) <= made, "an image neither drawn by the screenshot script nor recorded"
    commands = next(
        action
        for action in cli.build_parser()._actions
        if isinstance(action, argparse._SubParsersAction)
    ).choices
    cited = set(re.findall(r"`ion-repo ([a-z][a-z-]+)", text)) | set(
        re.findall(r"^\$ (?:cd \S+ && )?ion-repo ([a-z][a-z-]+)", text, re.M)
    )
    assert cited <= set(commands), f"{readme} cites ion-repo {sorted(cited - set(commands))}"
    reference = REFERENCES[READMES.index(readme)]
    assert f"]({reference})" in text, f"{readme} links its reference"


def test_pypi_shows_the_readme_with_its_images_and_links() -> None:
    """PyPI shows README.md away from the repo: the build makes each relative image and link
    point at the release's tag on GitHub (hatch-fancy-pypi-readme, in `pyproject.toml`)."""
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    hook = pyproject["tool"]["hatch"]["metadata"]["hooks"]["fancy-pypi-readme"]
    version = pyproject["project"]["version"]
    text = "".join((ROOT / part["path"]).read_text(encoding="utf-8") for part in hook["fragments"])
    for substitution in hook["substitutions"]:
        text = re.sub(substitution["pattern"], substitution["replacement"], text)
    text = text.replace("$HFPR_VERSION", version)

    targets = re.findall(r'(?:src|srcset)="([^"]+)"', text) + re.findall(r"\]\(([^)\s]+)\)", text)
    assert [target for target in targets if not target.startswith(("https://", "#"))] == []
    tagged = (
        f"https://raw.githubusercontent.com/antoine-tena/ion-repo/v{version}/",
        f"https://github.com/antoine-tena/ion-repo/blob/v{version}/",
    )
    for target in targets:
        for prefix in tagged:
            if target.startswith(prefix):
                assert (ROOT / target.removeprefix(prefix)).exists(), target


# The marks of a text written by a language model, which readers (Hacker News first) spot and
# hold against a project: em dashes strewn about (one, in the tagline antoine chose, is a style),
# list items opened in bold or with an emoji, sales words.
SALES_WORDS = (
    "seamless", "robust", "powerful", "blazing", "best-in-class",
    "cutting-edge", "game-changer", "supercharge", "effortless", "leverage", "unlock", "empower",
    "delve", "crucial", "showcase", "elevate", "revolutioni[sz]e", "world-class",
    "state-of-the-art", "puissant", "révolutionnaire", "incontournable", "sans effort",
)  # fmt: skip


@pytest.mark.parametrize("readme", (*READMES, *ROADMAPS))
def test_a_readme_reads_as_written_by_a_person(readme: str) -> None:
    text = (ROOT / readme).read_text(encoding="utf-8")
    prose = "\n".join(
        line for line in re.sub(r"```.*?```", "", text, flags=re.S).splitlines()
        if not line.startswith("|")  # an em dash marks an empty table cell
    )  # fmt: skip

    assert prose.count("—") <= 1, f"{readme}: em dashes, where a comma or a colon reads better"
    assert not re.findall(r"^- (?:\*\*|[\U0001F300-\U0001FAFF☀-➿])", prose, re.M), (
        f"{readme}: a list item opened in bold or with an emoji"
    )
    sales = [word for word in SALES_WORDS if re.search(rf"\b{word}\b", prose, re.I)]
    assert sales == [], f"{readme}: {sales}, a fact says it better"


def test_both_readmes_say_the_same_things() -> None:
    english, french = ((ROOT / name).read_text(encoding="utf-8") for name in READMES)

    def outline(text: str) -> list[object]:
        return [
            len(re.findall(r"^## ", text, re.M)),
            len(re.findall(r"^- ", text, re.M)),
            re.findall(r'src="(docs/assets/[^"]+)"', text),
            len(re.findall(r"^\| ", text, re.M)),
        ]

    assert outline(english) == outline(french), "README.fr.md follows README.md"


def test_the_roadmap_shows_the_backlog_plan() -> None:
    drawn = script("roadmap").draw()

    for readme, roadmap in zip(READMES, ROADMAPS, strict=True):
        text = (ROOT / roadmap).read_text(encoding="utf-8")
        assert drawn in text, f"{roadmap} lags the plan: uv run python scripts/roadmap.py"
        assert f"]({roadmap})" in (ROOT / readme).read_text(encoding="utf-8"), (
            f"{readme} links {roadmap}"
        )


def test_installed_plugins_exist_and_former_names_are_gone() -> None:
    plugins = {plugin["name"] for plugin in MARKETPLACE["plugins"]}
    former = "|".join(map(re.escape, MARKETPLACE["renames"]))
    for name, text in docs().items():
        assert set(re.findall(r"plugin install ([\w-]+)@ion-repo", text)) <= plugins, name
        assert not re.findall(rf"`/?({former})(:[\w-]+)?`", text), name


def test_cited_workflows_exist() -> None:
    workflows = {path.name for path in (ROOT / ".github/workflows").glob("*.yml")}
    for name, text in docs().items():
        cited = set(re.findall(r"`([\w-]+\.yml)`", text)) - {"ci.yml", "copier.yml"}
        assert cited <= workflows, (name, sorted(cited - workflows))


# --- The reference describes everything ion-repo offers, at the release it is, in both languages
# (antoine, 19 October 2026: "the README kept entirely up to date, every time"). A command,
# option, setting, skill, hook, output style, plugin or workflow added without its line fails here.
# Former names kept for old repos: their new names are documented instead.
LEGACY = frozenset({"--sauter", "--sans-pousser", "--garder", "--statut", "--poste"})


def offered() -> dict[str, str]:
    """What ion-repo offers, by label, with the text each README must contain."""
    from ion_repo import cli
    from ion_repo.settings import SETTABLE_KEYS

    parser = cli.build_parser()
    commands = next(
        action for action in parser._actions if isinstance(action, argparse._SubParsersAction)
    )
    items: dict[str, str] = {}
    for name, command in commands.choices.items():
        items[f"command {name}"] = f"`ion repo {name}"
        for action in command._actions:
            for option in action.option_strings:
                if option.startswith("--") and option != "--help" and option not in LEGACY:
                    items[f"option {name} {option}"] = option
    items |= {f"setting {key}": f"`{key}`" for key in SETTABLE_KEYS}
    items |= {
        f"plugin {plugin['name']}": f"`{plugin['name']}`" for plugin in MARKETPLACE["plugins"]
    }
    items |= {
        f"skill {path.parent.parent.name}:{path.name}": f"`{path.name}`"
        for path in (ROOT / "plugins").glob("*/skills/*")
        if path.is_dir()
    }
    items |= {
        f"hook {path.name}": path.name
        for path in (ROOT / "plugins/repo/hooks").glob("*.py")
        if not path.name.startswith("_")
    }
    items |= {
        f"output style {path.stem}": f"`{path.stem}`"
        for path in (ROOT / "plugins").glob("*/output-styles/*.md")
    }
    items |= {
        f"workflow {path.name}": f"`{path.name}`"
        for path in (ROOT / ".github/workflows").glob("*.yml")
        if "workflow_call:" in path.read_text(encoding="utf-8")
    }
    return items


@pytest.mark.parametrize("reference", REFERENCES)
def test_the_reference_describes_everything_kiln_offers(reference: str) -> None:
    text = (ROOT / reference).read_text(encoding="utf-8")

    missing = [label for label, needle in offered().items() if needle not in text]

    assert missing == [], f"{reference} says nothing of: {', '.join(missing)}"


def test_the_docs_quote_the_release_they_describe() -> None:
    version = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["version"]
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert re.search(r"^## v(\S+) — ", changelog, re.M).group(1) == version  # type: ignore[union-attr]
    for name, text in docs().items():
        quoted = set(re.findall(r"antoine-tena/ion-repo/\S+?@v(\d+\.\d+\.\d+)", text))
        assert quoted <= {version}, f"{name} quotes ion-repo at {quoted}, the release is {version}"

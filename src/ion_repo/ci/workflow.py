"""Reading a project's `ci.yml`: its jobs, and what `kiln ci` can replay of them.

`ci.yml` remains the only description of the CI. A job calling a reusable workflow of kiln is
replayed with the same parameters (`with:`); a job written in the project is if it only does
`run:` steps after the checkout. The others are listed as not replayed: the verdict says so.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from ion_repo.shell import KilnError

CI_WORKFLOW = Path(".github/workflows/ci.yml")
KILN_WORKFLOW = re.compile(r"antoine-tena/kiln/\.github/workflows/(?P<name>[\w-]+)\.yml@")
CHECKOUT_ACTION = "actions/checkout@"
# Reusable workflows of kiln that `kiln ci` can replay (see jobs.py).
REPLAYABLE_WORKFLOWS = frozenset(
    {"django", "api-contract", "charter", "pnpm", "security", "secrets"}
    | {"contrat-api", "charte", "securite"}  # names before kiln 0.4.0
)
INLINE_KIND = "inline"


@dataclass(frozen=True)
class Job:
    """A job of `ci.yml`: its kind (kiln workflow, `inline`, or empty) and its parameters."""

    name: str
    kind: str
    inputs: dict[str, str] = field(default_factory=dict)
    commands: tuple[str, ...] = ()
    reason: str = ""

    @property
    def is_replayable(self) -> bool:
        return not self.reason


def load_jobs(root: Path) -> list[Job]:
    """The jobs of the project's `ci.yml`, in file order."""
    workflow_path = root / CI_WORKFLOW
    if not workflow_path.exists():
        raise KilnError(f"no {CI_WORKFLOW}: nothing to replay")
    workflow = yaml.safe_load(workflow_path.read_text())
    jobs = workflow.get("jobs") if isinstance(workflow, dict) else None
    if not isinstance(jobs, dict):
        raise KilnError(f"{CI_WORKFLOW} declares no job")
    return [parse_job(str(name), definition) for name, definition in jobs.items()]


def parse_job(name: str, definition: object) -> Job:
    if not isinstance(definition, dict):
        return Job(name, "", reason="unreadable definition")
    uses = definition.get("uses")
    if isinstance(uses, str):
        return _reusable_job(name, uses, definition.get("with"))
    return _inline_job(name, definition)


def _reusable_job(name: str, uses: str, raw_inputs: object) -> Job:
    match = KILN_WORKFLOW.search(uses)
    if match is None:
        return Job(name, "", reason=f"workflow hors kiln ({uses})")
    kind = match["name"]
    if kind not in REPLAYABLE_WORKFLOWS:
        return Job(name, kind, reason=f"workflow {kind} not replayed locally yet")
    pairs = raw_inputs.items() if isinstance(raw_inputs, dict) else ()
    inputs = {str(key): _input_text(value) for key, value in pairs}
    return Job(name, kind, inputs)


def _input_text(value: object) -> str:
    """A `with:` parameter as GitHub passes it: booleans in lowercase, the rest as text."""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _inline_job(name: str, definition: dict[str, object]) -> Job:
    if definition.get("services"):
        return Job(name, INLINE_KIND, reason="services of its own")
    steps = definition.get("steps")
    if not isinstance(steps, list):
        return Job(name, INLINE_KIND, reason="no step")
    commands: list[str] = []
    for step in steps:
        uses = step.get("uses") if isinstance(step, dict) else None
        if isinstance(uses, str) and uses.startswith(CHECKOUT_ACTION):
            continue
        command = step.get("run") if isinstance(step, dict) else None
        if not isinstance(command, str) or set(step) - {"name", "run", "working-directory"}:
            return Job(name, INLINE_KIND, reason="steps other than commands")
        directory = str(step.get("working-directory", "."))
        commands.append(f"cd {directory}\n{command}" if directory != "." else command)
    return Job(name, INLINE_KIND, commands=tuple(commands))

"""Local steps of each reusable workflow of kiln, for `kiln ci`.

Each planner follows, step by step, the workflow of the same name in `.github/workflows/`, with
its defaults (DEFAULTS, which tests/test_ci.py compares with the files). A workflow that changes
changes here in the same commit. The names of before kiln 0.4.0 (`charte`, `securite`,
`contrat-api`, French inputs) are still replayed: a project not yet updated cites them.
"""

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field

from kiln.ci.workflow import INLINE_KIND, Job

GENERATED_DIFF = "git diff --exit-code -- ':(top,attr:linguist-generated=true)'"
EXPORT_OPENAPI = "uv run python manage.py export_openapi --check --output ../openapi.json"
DEFAULTS: Mapping[str, Mapping[str, str]] = {
    "django": {
        "directory": "backend",
        "database": "app",
        "base": "",
        "postgres": "docker.io/library/postgres:16-alpine",
        "redis": "docker.io/library/redis:7-alpine",
        "env": "",
        "mypy": "true",
        "coverage": "true",
    },
    "api-contract": {
        "backend": "backend",
        "frontend": "frontend",
        "export": EXPORT_OPENAPI,
        "generate": "pnpm generate:api",
        "env": "",
    },
    "charter": {},
    # `reports`: artifacts published on GitHub; locally, the logs stand for them.
    "pnpm": {
        "directory": "frontend",
        "pnpm": "",
        "scripts": "lint\ntypecheck\ntest\nbuild\n",
        "reports": "",
        "rapports": "",
    },
    "security": {
        "uv": "backend",
        "pnpm": "frontend",
        "pnpm-version": "",
        "maven": "",
        "audit-level": "high",
    },
    "secrets": {},
    # Relays of before kiln 0.4.0, with their inputs of that time.
    "charte": {},
    "contrat-api": {
        "back": "backend",
        "front": "frontend",
        "export": EXPORT_OPENAPI,
        "generation": "pnpm generate:api",
        "env": "",
    },
    "securite": {"uv": "backend", "pnpm": "frontend", "version-pnpm": "", "niveau": "high"},
}
# Workflow names of before kiln 0.4.0 → today's name.
RELAYS: Mapping[str, str] = {
    "charte": "charter",
    "contrat-api": "api-contract",
    "securite": "security",
}
# Inputs of before kiln 0.4.0 → today's name, whatever the workflow.
LEGACY_INPUTS: Mapping[str, str] = {
    "back": "backend",
    "couverture": "coverage",
    "dossier": "directory",
    "front": "frontend",
    "generation": "generate",
    "niveau": "audit-level",
    "rapports": "reports",
    "version-pnpm": "pnpm-version",
}
# gitleaks on the workstation (`mise use -g gitleaks`, `brew install gitleaks`): the same scan as
# the `secrets` workflow, over the whole history.
GITLEAKS_SCAN = """\
if ! command -v gitleaks >/dev/null; then
  echo "gitleaks is missing: mise use -g gitleaks (or brew install gitleaks)" >&2
  exit 1
fi
gitleaks git --redact --no-banner --verbose ."""
# OSV-Scanner on the workstation (`mise use -g osv-scanner`, `brew install osv-scanner`): the same
# audit of a Maven project as the `security` workflow.
OSV_SCAN = """\
if ! command -v osv-scanner >/dev/null; then
  echo "osv-scanner is missing: mise use -g osv-scanner (or brew install osv-scanner)" >&2
  exit 1
fi
osv-scanner --recursive ."""
BACK_LANE = "back"
FRONT_LANE = "front"


@dataclass(frozen=True)
class Step:
    """A shell command run from `directory` (relative to the root of the worktree)."""

    label: str
    command: str
    directory: str = "."
    should_always_run: bool = False


@dataclass(frozen=True)
class Services:
    """Databases the job expects: podman images (empty = none) and the name of the database."""

    database: str
    postgres: str
    redis: str


@dataclass(frozen=True)
class Plan:
    job: Job
    steps: tuple[Step, ...]
    lane: str = FRONT_LANE
    env: Mapping[str, str] = field(default_factory=dict)
    services: Services | None = None
    python_dirs: tuple[str, ...] = ()
    pnpm_dirs: tuple[str, ...] = ()


def plan_job(job: Job) -> Plan:
    if job.kind == INLINE_KIND:
        steps = tuple(Step(f"step {index}", command) for index, command in enumerate(job.commands))
        return Plan(job, steps)
    kind = RELAYS.get(job.kind, job.kind)
    given = {LEGACY_INPUTS.get(name, name): value for name, value in job.inputs.items()}
    inputs = {**DEFAULTS[kind], **given}
    return PLANNERS[kind](job, inputs)


def parse_env(lines: str) -> dict[str, str]:
    """The `env` input of the workflows: one `KEY=value` variable per line."""
    pairs = (line.strip().split("=", 1) for line in lines.splitlines() if "=" in line)
    return {key.strip(): value for key, value in pairs}


def _django(job: Job, inputs: Mapping[str, str]) -> Plan:
    directory = inputs["directory"]
    steps = [
        Step("ruff", "uv run ruff check .\nuv run ruff format --check .", directory),
        Step("typing (charter types)", "charter types") if inputs["mypy"] == "true" else None,
        Step(
            "no missing migration",
            "uv run python manage.py makemigrations --check --dry-run",
            directory,
        ),
        Step(
            "pytest",
            "uv run pytest --cov --cov-branch --cov-report=xml --cov-report=term:skip-covered",
            directory,
        ),
        Step("coverage floors", "charter coverage") if inputs["coverage"] == "true" else None,
    ]
    database = inputs["base"] or inputs["database"]
    services = Services(database, inputs["postgres"], inputs["redis"])
    return Plan(
        job,
        tuple(step for step in steps if step is not None),
        lane=BACK_LANE,
        env=parse_env(inputs["env"]),
        services=services,
        python_dirs=(directory,),
    )


def _contract(job: Job, inputs: Mapping[str, str]) -> Plan:
    steps = (
        Step("openapi.json matches the code", inputs["export"], inputs["backend"]),
        Step(
            "types and input rules match the schema",
            f"{inputs['generate']}\n{GENERATED_DIFF}",
            inputs["frontend"],
        ),
    )
    return Plan(
        job,
        steps,
        env=parse_env(inputs["env"]),
        python_dirs=(inputs["backend"],),
        pnpm_dirs=(inputs["frontend"],),
    )


def _charter(job: Job, inputs: Mapping[str, str]) -> Plan:
    return Plan(job, (Step("charter", "charter"),))


def _pnpm(job: Job, inputs: Mapping[str, str]) -> Plan:
    directory = inputs["directory"]
    scripts = [line.strip() for line in inputs["scripts"].splitlines() if line.strip()]
    steps = tuple(Step(f"pnpm {script}", f"pnpm {script}", directory) for script in scripts)
    return Plan(job, steps, pnpm_dirs=(directory,))


def _security(job: Job, inputs: Mapping[str, str]) -> Plan:
    audit_command = "uv audit --locked --preview-features audit-command"
    steps = [
        Step(f"uv audit {directory}", audit_command, directory)
        for directory in inputs["uv"].split()
    ]
    if inputs["pnpm"]:
        audit = f"pnpm audit --prod --audit-level {inputs['audit-level']}"
        steps.append(Step("pnpm audit", audit, inputs["pnpm"], should_always_run=True))
    if inputs["maven"]:
        steps.append(Step("OSV-Scanner (Maven)", OSV_SCAN, inputs["maven"], should_always_run=True))
    return Plan(job, tuple(steps))


def _secrets(job: Job, inputs: Mapping[str, str]) -> Plan:
    return Plan(job, (Step("gitleaks (whole history)", GITLEAKS_SCAN),))


PLANNERS: Mapping[str, Callable[[Job, Mapping[str, str]], Plan]] = {
    "django": _django,
    "api-contract": _contract,
    "charter": _charter,
    "pnpm": _pnpm,
    "security": _security,
    "secrets": _secrets,
}

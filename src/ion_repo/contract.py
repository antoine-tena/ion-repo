"""`kiln contract`: openapi.json exported from the Django code, then the front types ([OPENAPI])."""

import json
import os
from pathlib import Path

from ion_repo import ui
from ion_repo.shell import KilnError, run, step
from ion_repo.stack import Stack

SCHEMA_FILE = "openapi.json"
EXPORT_COMMAND = [
    "uv",
    "run",
    "python",
    "manage.py",
    "export_openapi",
    "--output",
    f"../{SCHEMA_FILE}",
]
# A DRF backend kiln did not generate: drf-spectacular's own export, same file.
SPECTACULAR_COMMAND = [
    "uv",
    "run",
    "python",
    "manage.py",
    "spectacular",
    "--format",
    "openapi-json",
    "--file",
    f"../{SCHEMA_FILE}",
]
GENERATE_SCRIPT = "generate:api"
GENERATE_COMMAND = ["pnpm", GENERATE_SCRIPT]
# The export only reads the code: a dummy key will do when backend/.env is missing (worktree, CI).
EXPORT_SECRET_KEY = "kiln-export-openapi"


def has_api_contract(stack: Stack) -> bool:
    return stack.backend == "django" and stack.frontend == "nuxt"


def generate_api_contract(root: Path, stack: Stack) -> None:
    if not has_api_contract(stack):
        return
    step("API contract: openapi.json and frontend types")
    backend, frontend = root / stack.backend_dir, root / stack.frontend_dir
    export_env = {"DJANGO_SECRET_KEY": EXPORT_SECRET_KEY, **os.environ}
    run(export_command(backend), backend, env=export_env)
    if GENERATE_SCRIPT in _scripts(frontend):
        run(GENERATE_COMMAND, frontend)
    else:
        ui.note(
            f"{SCHEMA_FILE} written; no `{GENERATE_SCRIPT}` script in {stack.frontend_dir}/"
            "package.json, so no front types: kiln's is "
            f"`openapi-typescript ../{SCHEMA_FILE} -o app/types/api.d.ts`"
        )


def export_command(backend: Path) -> list[str]:
    """kiln's `export_openapi` (django-ninja), otherwise drf-spectacular's in a repo kiln did not
    generate."""
    if any(backend.glob("*/management/commands/export_openapi.py")):
        return EXPORT_COMMAND
    manifest = backend / "pyproject.toml"
    if manifest.is_file() and "drf-spectacular" in manifest.read_text(encoding="utf-8"):
        return SPECTACULAR_COMMAND
    raise KilnError(
        f"no OpenAPI export in {backend.name}/: neither kiln's `export_openapi` command "
        "(django-ninja) nor drf-spectacular"
    )


def _scripts(frontend: Path) -> dict[str, str]:
    manifest = frontend / "package.json"
    if not manifest.is_file():
        return {}
    return json.loads(manifest.read_text(encoding="utf-8")).get("scripts") or {}

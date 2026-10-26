"""`kiln contract`: openapi.json exported from the Django code, then the front types ([OPENAPI])."""

import os
from pathlib import Path

from kiln.shell import run, step
from kiln.stack import Stack

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
GENERATE_COMMAND = ["pnpm", "generate:api"]
# The export only reads the code: a dummy key will do when backend/.env is missing (worktree, CI).
EXPORT_SECRET_KEY = "kiln-export-openapi"


def has_api_contract(stack: Stack) -> bool:
    return stack.backend == "django" and stack.frontend == "nuxt"


def generate_api_contract(root: Path, stack: Stack) -> None:
    if not has_api_contract(stack):
        return
    step("API contract: openapi.json and frontend types")
    export_env = {"DJANGO_SECRET_KEY": EXPORT_SECRET_KEY, **os.environ}
    run(EXPORT_COMMAND, root / stack.backend_dir, env=export_env)
    run(GENERATE_COMMAND, root / stack.frontend_dir)

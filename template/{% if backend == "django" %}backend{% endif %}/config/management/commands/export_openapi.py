"""Exports the OpenAPI schema of the API ([OPENAPI]), source of the frontend's types.

Run by `kiln contract` (`--output ../openapi.json`); `--check` is for CI.
"""

import json
from argparse import ArgumentParser
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from config.api import api


class Command(BaseCommand):
    help = "Exports the OpenAPI schema of the API as JSON."

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("--output", type=Path, required=True, help="Output file.")
        parser.add_argument(
            "--check",
            action="store_true",
            help="Writes nothing; fails when the file differs from the code's schema.",
        )

    def handle(self, *args: object, **options: object) -> None:
        rendered_schema = render_schema()
        output_path = Path(str(options["output"]))
        if options["check"]:
            check_schema(output_path, rendered_schema)
            self.stdout.write(f"{output_path} is up to date.")
            return
        output_path.write_text(rendered_schema, encoding="utf-8")
        self.stdout.write(f"OpenAPI schema written to {output_path}.")


def render_schema() -> str:
    """Deterministic rendering: two exports of the same code give the same file."""
    schema = api.get_openapi_schema()
    return json.dumps(schema, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def check_schema(output_path: Path, rendered_schema: str) -> None:
    regenerate = f"uv run python manage.py export_openapi --output {output_path}"
    if not output_path.exists():
        raise CommandError(f"{output_path} is missing. Run: {regenerate}")
    if output_path.read_text(encoding="utf-8") != rendered_schema:
        raise CommandError(
            f"{output_path} has drifted from the code. Run: {regenerate}, "
            "then pnpm generate:api in frontend/."
        )

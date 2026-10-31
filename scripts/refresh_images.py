"""Pin the template's base images to the digest their tag points to today.

    uv run python scripts/refresh_images.py

A generated project's images are pinned by digest ([IMAGES-BY-DIGEST]) and Dependabot moves them
from then on; the template itself is not a project Dependabot can read (`.jinja` files, folders
named by conditions), so this script refreshes its digests: before each release candidate, and
whenever a tag changes. The tag stays in front of the digest, for the reader.
"""

import re
from pathlib import Path

from ion_repo.grid.fixers import resolve

TEMPLATE = Path(__file__).resolve().parent.parent / "template"
FROM = re.compile(r"^(?P<head>FROM\s+)(?P<image>[^\s@]+)(?:@sha256:[0-9a-f]{64})?", re.M)


def refresh(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    pinned = FROM.sub(
        lambda found: f"{found['head']}{found['image']}@{resolve.image_digest(found['image'])}",
        text,
    )
    if pinned != text:
        path.write_text(pinned, encoding="utf-8")
    return pinned != text


def main() -> None:
    for path in sorted(TEMPLATE.rglob("*Containerfile*")):
        print(f"{path.relative_to(TEMPLATE)}: {'refreshed' if refresh(path) else 'up to date'}")


if __name__ == "__main__":
    main()

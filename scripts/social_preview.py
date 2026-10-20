"""Export the social preview to PNG, the only kind of image GitHub takes for it.

    uv run --with playwright python scripts/social_preview.py

`docs/assets/social-preview.svg` is drawn by `scripts/screenshots.py` (checked by the tests);
this renders it in Chromium at 1280 by 640 pixels into `docs/assets/social-preview.png`,
uploaded by hand as no API takes it: https://github.com/antoine-tena/kiln/settings, "Social
preview". Run `uv run --with playwright playwright install chromium` first if Chromium is
missing.
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

ASSETS = Path(__file__).resolve().parent.parent / "docs/assets"


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 640})
        page.goto((ASSETS / "social-preview.svg").as_uri())
        page.screenshot(path=ASSETS / "social-preview.png")
        browser.close()
    print("docs/assets/social-preview.png written")


if __name__ == "__main__":
    main()

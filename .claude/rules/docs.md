---
paths:
  - "README*.md"
  - "ROADMAP*.md"
  - "docs/reference*.md"
  - "docs/assets/**"
  - "scripts/screenshots.py"
  - "scripts/social_preview.py"
  - "scripts/demo_shell.sh"
  - "scripts/shrink_demo.sh"
  - "scripts/roadmap.py"
  - "tests/test_docs.py"
---

# kiln's showcase: README, reference, images

antoine's request: the README, "the best in the world", fully up to date from one release to the
next. It shows kiln in few words and real images (like uv, ruff, Bun); the reference
(`docs/reference.md`, `docs/reference.fr.md`) holds everything else. `tests/test_docs.py` fails
if:
- the roadmap (`ROADMAP.md`, `ROADMAP.fr.md`) no longer shows the backlog's plan, or a README no
  longer cites it;
- a language's reference misses a command, an option, a `kiln set` setting, a plugin, a skill, a
  hook or a reusable workflow;
- a README cites a command that doesn't exist, doesn't link to its reference, or no longer
  follows the other language (same sections, bullets, images, tables);
- an image of `docs/assets/` differs from what `scripts/screenshots.py` draws from kiln's real
  outputs (the welcome screen, `kiln grid`, a rule, `kiln update`'s note, a release's diagram in
  light and dark);
- the docs cite kiln at another version than `pyproject.toml`'s;
- a recorded demo types a command or an option that no longer exists, or weighs 5 MB or more;
- the README PyPI publishes keeps a relative image or link (the build points them at the
  release's tag on GitHub, `hatch-fancy-pypi-readme` in `pyproject.toml`);
- a README carries the marks of AI text that Hacker News readers pick up: em dash, a bullet
  opened in bold or with an emoji, a salesman's word (*seamless*, *powerful*…).

`kiln version cut` moves the cited version forward, and refuses to tag the first candidate of a
release whose README and reference didn't change in either language (unless
`<!-- readme: unchanged, why -->` in its entry). Images are looked at in a real browser before
they're committed (`textLength` and spaces only render right there).

**Demos** (`docs/assets/kiln-new.gif`, `kiln-rescue.gif`) are re-recorded before each candidate
when what they show changed: `vhs docs/assets/<demo>.tape` (vhs, ttyd and ffmpeg, installed
outside any package manager in `~/.cache/kiln-demo-tools/bin`, about 190 MB, to put in front of
`PATH`; `kiln-rescue` runs a real Claude Code, 5 to 10 minutes of session per recording, then
`scripts/shrink_demo.sh` brings it under 5 MB).

**One promise everywhere** (README, GitHub's "About", PyPI summary, share image), chosen by
antoine: "Claude Code's workshop", then "Start every new project, and rescue every old one, like
a senior engineer would — even if you're not one.", and under it "Make Claude Code build
production-grade repos, bring yours up to that grade, and keep them that way." An old repo to
bring up to grade counts as much as a new one (`kiln adopt`, then v0.5.0's score and fixes). The
text posted on Hacker News, title and answers included, is written by hand by antoine (the
forum's rule).

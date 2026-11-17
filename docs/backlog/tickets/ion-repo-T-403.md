# ion-repo#T-403 · Install lines on the Ion names once they are on PyPI
- **Type**: task
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-31
- **Effort**: XS · **Owner**: — · **Due**: —
- **Origin**: README check of the family, 2026-10-31

`ion-repo` and `ion-sh` are not on PyPI yet (404), so the READMEs give `kiln-cli` and `kiln install`,
and `ion/ion`'s README installs from a clone.
- [x] `template/README.md.jinja`, `README.md`, `README.fr.md`, references, `TOOL_HINTS` in
  `grid/checks.py`: written ahead of the release, true from its publication.
- [x] `ion/ion`'s `README.md` back to `uv tool install ion-sh` (its branch `feat/ion-repo-on-pypi`).
- [ ] `ion repo update` on the repos, by antoine, once v0.4.11 is out.

# ion-repo#T-440 · A tag publishes on PyPI only on an explicit setting
- **Type**: bug
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-11-09
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-03 to 2026-11-09, two releases of private tools (`904aab3d` 23:18, `e1d07955` 23:28)

- [ ] A `v*` tag fires `pypi.yml` whenever the workflow exists; on private tools the session had to disable or cancel it by hand, racing a real `PYPI_TOKEN` in the environment.
- [ ] The generated workflow publishes only when the repo's settings say so (`pypi_name` set and a published flag), and the release says which it will do before the tag.
- [ ] PyPI checks read the JSON API: the project page answers 200 from an anti-bot page.

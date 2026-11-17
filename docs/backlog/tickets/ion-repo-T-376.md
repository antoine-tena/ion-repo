# ion-repo#T-376 · `kiln check` ran no test on emberstudio, and left a `.env` towards a stopped PostgreSQL
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-30
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: emberstudio session `feat/auth`, 30 October 2026

To reproduce first. In a worktree of emberstudio with no `backend/.env`, `DJANGO_SECRET_KEY=…
DJANGO_DEBUG=True kiln check` printed seven steps (dependencies, ruff, format, mypy, ESLint,
typecheck, charter) and "All checks pass": no pytest step, though `project.md` says it runs
pytest. A `backend/.env` existed afterwards, its `DATABASE_URL` towards the compose's
PostgreSQL (port 54461), which was not started: pytest then failed on every test using the
database until `podman-compose up -d db`.
- [ ] Find why pytest was skipped (missing database? missing `.env`?) and make it run, or fail
  saying why; never "All checks pass" without the tests.
- [ ] A `.env` that `kiln check` writes comes with the database it names started, or says how.

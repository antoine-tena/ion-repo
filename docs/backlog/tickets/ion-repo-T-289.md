# ion-repo#T-289 · Python beyond Django: every packaging tool, FastAPI and Flask
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Framework packs), made a ticket
  on 25 October 2026 at antoine's request

Planned in v0.6.55, "Python beyond Django": FastAPI, Flask, SQLAlchemy and every packaging tool
read; a new stack's rules count only once ten corpus repos of it were checked.

The `NOTABLE_PACKAGES` of `score.py` already name what the gap report sees; a pack turns one of them
into rules.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B02** Python beyond Django: Flask, FastAPI, Litestar, Starlette, aiohttp, Pyramid;
  SQLAlchemy and Alembic; Pydantic 1 to 2; Celery, RQ, Dramatiq, Huey, django-q2; each with a pack
  of rules (rule ideas, FP).
- [ ] **B03** Every Python packaging tool read: uv, Poetry, PDM, Hatch, pip-tools
  (`requirements.in`), Pipenv, Conda (environment.yml, conda-lock), Rye (`hold`, to uv), setup.py
  and setup.cfg (`hold`, to PEP 621), PEP 735 dependency groups, PEP 751 `pylock.toml`, PEP 723
  inline script metadata.
- [ ] **B24** A new ecosystem's rules count only after ten public repos of that stack in the corpus
  were scored and their findings checked: precision first.
- [ ] **FP01** FastAPI · `FASTAPI-RESPONSE-MODELS`: every route declares its response model. L2 ·
  fix J · adopt.
- [ ] **FP02** FastAPI · `FASTAPI-LIFESPAN`: `lifespan` rather than the deprecated `on_event`. L2 ·
  fix S · adopt.
- [ ] **FP03** FastAPI · `FASTAPI-AUTH-DEPENDENCIES`: protected routes through security
  dependencies, set on the router rather than route by route. L2 · fix J · trial.
- [ ] **FP04** FastAPI · `FASTAPI-DOCS-IN-PROD`: `/docs` and `/openapi.json` off or protected in
  production for private APIs. L2 · fix J · trial.
- [ ] **FP05** Flask · `FLASK-APP-FACTORY`: a `create_app` factory, the secret key from the
  environment, CSRF protection on forms (Flask-WTF). L2 · fix J · trial.
- [ ] **FP20** Pydantic · `PYDANTIC-V2`: Pydantic 2 rather than 1, which is no longer developed
  (`bump-pydantic` migrates). L1 · fix S · adopt.
- [ ] **AS23** (FastAPI's part) `CORS-STRICT`: `CORSMiddleware` never with `allow_origins=["*"]` and
  `allow_credentials=True` together. L2 · fix S · adopt.

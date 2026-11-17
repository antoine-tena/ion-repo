# ion-repo#T-270 · A tidy tree: the root, the layout, one config per tool, small folders
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Every forge, CI, host and
  machine, The detection engine, Structure), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.42, "A tree anyone can find their way in": No build output or artefact committed, a
complete `.gitignore`, one config per tool, paths every OS accepts, small folders.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B19** Every config file kiln recognizes validated against its JSON Schema from the
  SchemaStore catalogue: typos and deprecated keys found in hundreds of tools' files, for free.
- [ ] **C13** Rules that know operating systems: CRLF and `.gitattributes`, paths Windows refuses,
  case collisions that break macOS, a setup documented only as a `.sh` script.
- [ ] **E29** Artefacts that should never be committed, by name and content: `.pyc`,
  `node_modules/`, `dist/`, `.DS_Store`, `*.log`, `*.sqlite3`, `*.tfstate`, `id_rsa`, `*.pem`,
  `*.p12`, `*.keystore`, `.ipynb_checkpoints`, coverage reports, virtualenvs.
- [ ] **E30** `.gitignore` compared with github/gitignore's templates for the ecosystems present:
  what's missing is a scripted fix.
- [ ] **ST04** `ROOT-TIDY`: about 25 entries at most at the root; scripts in `scripts/`, docs in
  `docs/`. L0 · fix J · trial.
- [ ] **ST05** `SRC-LAYOUT`: a Python library's package under `src/`, as PyPA recommends. L0 · fix J
  · trial.
- [ ] **ST06** `ONE-CONFIG-PER-TOOL`: a tool configured in one place (ruff in `pyproject.toml` and
  in `ruff.toml` is two truths). L1 · fix S · adopt.
- [ ] **ST07** `CONFIG-IN-PYPROJECT`: Python tools' settings gathered in `pyproject.toml`
  (setup.cfg, tox.ini, .coveragerc, pytest.ini, mypy.ini merged in). L1 · fix S · trial.
- [ ] **ST08** `NO-NESTED-REPOS`: no `.git` inside the tree except declared submodules. L0 · fix J ·
  adopt.
- [ ] **ST09** `SHALLOW-TREE`: code no deeper than about six folders. L0 · ratchet · assess.
- [ ] **ST10** `SMALL-FOLDERS`: no code folder with more than about 50 files (assets, data,
  migrations aside). L0 · ratchet · assess.
- [ ] **ST11** `NO-GRAB-BAG-FILES`: no `utils.py`, `helpers.ts`, `misc.py` or `common.js` past about
  200 lines; the name says nothing of what's inside. L0 · fix J · trial.

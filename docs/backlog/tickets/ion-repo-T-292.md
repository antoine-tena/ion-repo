# ion-repo#T-292 · Data science repos: notebooks, data out of git, seeds, locked environments
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Data science), made a ticket on
  25 October 2026 at antoine's request

Planned in v0.6.58, "Data science repos": The first outside issues came from data repos: notebooks
without outputs or secrets, data out of git, seeds and environments locked, models loaded safely.

The first data repos came through issues (#43, #44): v0.4.6 deploys a Streamlit or Dash front
(ion-repo#T-155) and adds `MODEL-TRACED` (ion-repo#T-156). This theme gathers what such repos need.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B18** Notebooks as code: `.ipynb` parsed (cells, outputs, execution order), Quarto and R
  Markdown read, Shiny apps recognised next to Streamlit and Dash.
- [ ] **DS02** `NOTEBOOK-OUTPUTS-CLEAN`: notebooks committed without outputs or execution counts
  (nbstripout, or Jupytext pairs). L1 · fix S · adopt.
- [ ] **DS03** `NOTEBOOKS-PAIRED`: notebooks paired with a `.py` file (Jupytext's percent format) so
  diffs and reviews work. L1 · fix S · trial.
- [ ] **DS04** `NOTEBOOK-SECRETS`: no token in a cell or an output; `SECRETS` reads a `.ipynb` as
  cells, not as one JSON string. L2 · fix J · adopt.
- [ ] **DS05** `NO-ABSOLUTE-PATHS`: no `/home/…`, `C:\Users\…` or `/content/drive` path in code or
  notebooks. L2 · fix J · adopt.
- [ ] **DS06** `DATA-OUT-OF-GIT`: datasets over a few MB kept out of git (DVC, LFS, a bucket),
  described by a pointer. L0 · fix J · adopt.
- [ ] **DS07** `SEEDS-SET`: random seeds fixed where results are reported
  (`numpy.random.default_rng(seed)`, `torch.manual_seed`). L2≈ · fix J · trial.
- [ ] **DS08** `ENVIRONMENT-LOCKED`: the analysis environment locked (uv, conda-lock, pixi, renv).
  L1 · fix S · adopt.

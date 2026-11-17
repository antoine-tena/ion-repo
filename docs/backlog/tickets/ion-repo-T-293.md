# ion-repo#T-293 · Data science repos: pipelines, model loading, experiments, Streamlit
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Data science, Framework packs), made a ticket on
  25 October 2026 at antoine's request

Planned in v0.6.58, "Data science repos": The first outside issues came from data repos: notebooks
without outputs or secrets, data out of git, seeds and environments locked, models loaded safely.

The first data repos came through issues (#43, #44): v0.4.6 deploys a Streamlit or Dash front
(ion-repo#T-155) and adds `MODEL-TRACED` (ion-repo#T-156). This theme gathers what such repos need.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **DS09** `PIPELINE-DECLARED`: steps declared (DVC stages, Snakemake, a Makefile), not
  notebooks run by hand in order. L0 · fix J · trial.
- [ ] **DS10** `STREAMLIT-SECRETS-IGNORED`: `.streamlit/secrets.toml` ignored and untracked;
  critical when tracked. L0 · fix S · adopt.
- [ ] **DS11** `NOTEBOOKS-RUN-IN-CI`: notebooks that are part of the deliverable executed in CI
  (nbmake, papermill). L1 · fix S · trial.
- [ ] **DS12** `SAFE-MODEL-LOADING`: no `pickle.load` or `torch.load(..., weights_only=False)` on
  downloaded files, nor `trust_remote_code=True` (Hugging Face) without a pinned revision;
  safetensors or ONNX for models from outside. L2 · fix S · adopt.
- [ ] **DS13** `EXPERIMENTS-TRACKED`: runs logged with their commit (MLflow, a results file). L1≈ ·
  fix J · assess.
- [ ] **DS14** `DATA-SCHEMA`: input tables validated by a schema (pandera, Great Expectations,
  Pydantic). L2≈ · fix J · assess.
- [ ] **FP19** Streamlit and Dash · the DS theme's rules plus `STREAMLIT-SECRETS-IGNORED`, and the
  deploy of v0.4.6 checked (a health route, a non-root image). L1 · fix S · trial.
- [ ] **FP38** Gradio · `GRADIO-SHARE-OFF`: no `launch(share=True)` in committed code, which opens
  the app to the whole Internet through a public link. L2 · fix S · adopt.

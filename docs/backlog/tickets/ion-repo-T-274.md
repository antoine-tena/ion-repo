# ion-repo#T-274 · Set up in one command: pre-commit, editor files, a task runner, tool versions
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every forge, CI, host and machine, Operations,
  Developer experience), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.44, "Set up in one command": One bootstrap command, tasks named in one place, fast
commit hooks, tool versions pinned as in CI, editor settings shared.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **C08** Pre-commit frameworks read (pre-commit, lefthook, Husky, lint-staged): checks before a
  commit, never counted as CI.
- [ ] **C16** Editor and environment files read: `.editorconfig`, `.vscode/` (recommended
  extensions, settings with personal paths), `.idea/` (workspace files committed), devcontainers,
  Gitpod, Codespaces, mise and asdf, direnv's `.envrc` (secrets in it), Nix dev shells, flox.
- [ ] **OP21** `ONE-COMMAND-LOCAL`: the whole stack runs locally with one command (`kiln dev`,
  compose, `Procfile.dev`). L0 · fix S · adopt.
- [ ] **DX01** `ONE-COMMAND-SETUP`: one documented bootstrap command (`make setup`, `just setup`,
  `uv sync` with `pnpm install`). L1 · fix S · adopt.
- [ ] **DX02** `TASK-RUNNER`: common tasks named in one place (Makefile, justfile, package scripts,
  poe), and the README cites them. L1 · fix S · trial.
- [ ] **DX03** `PRE-COMMIT-FAST`: commit hooks run in seconds (ruff at commit, type checks and tests
  elsewhere). L1≈ · fix J · trial.
- [ ] **DX04** `TOOL-VERSIONS-PINNED`: tool versions in `mise.toml` or `.tool-versions`, the same as
  in CI. L1 · fix S · trial.
- [ ] **DX05** `NO-GLOBAL-INSTALLS`: tools run from the project (`uvx`, `pnpm dlx`, versioned
  `npx`), never `sudo pip install` or `npm -g` in the docs. L2 · fix J · trial.
- [ ] **DX06** `EDITOR-SETTINGS-SHARED`: recommended extensions and format-on-save shared, personal
  settings ignored. L0 · fix S · assess.
- [ ] **DX08** `DEVCONTAINER` ⚠ ion-repo#T-48 (declined): a dev container for teams that want one, at `hold`
  while ion-repo#T-48 stands. L0 · hold.

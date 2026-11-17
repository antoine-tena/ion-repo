# ion-repo#T-271 · A tree that checks out anywhere: marked files, no build output, line endings, paths
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Structure, Git and versions), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.42, "A tree anyone can find their way in": No build output or artefact committed, a
complete `.gitignore`, one config per tool, paths every OS accepts, small folders.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **ST14** `WORKSPACE-DECLARED`: more than two components of one ecosystem are declared in a
  workspace (uv, pnpm). L1 · fix S · trial.
- [ ] **ST15** `GENERATED-MARKED`: generated files marked (`linguist-generated` or a header) so
  tools and Claude skip them. L1 · fix S · adopt.
- [ ] **ST16** `VENDORED-MARKED`: vendored code marked `linguist-vendored`. L1 · fix S · adopt.
- [ ] **ST17** `NO-BUILD-OUTPUT`: no `dist/`, `build/`, `.nuxt/`, `.output/`, `.next/`, `target/` or
  `*.egg-info` committed. L0 · fix S (untracked and ignored) · adopt.
- [ ] **ST18** `GITIGNORE-COMPLETE`: `.gitignore` covers the ecosystems present (virtualenvs,
  `node_modules`, caches, `.env`, coverage). L1 · fix S · adopt.
- [ ] **ST19** `EDITORCONFIG`: an `.editorconfig` consistent with the formatters. L0 · fix S ·
  trial.
- [ ] **ST20** `LINE-ENDINGS`: `.gitattributes` with `* text=auto eol=lf`. L1 · fix S · trial.
- [ ] **ST21** `ONE-TEST-LAYOUT`: tests either beside the code or in a mirrored tree, one convention
  per component. L0≈ · fix J · assess.
- [ ] **GV14** `NO-CASE-COLLISIONS`: no two paths that differ only by case (they break checkouts on
  macOS and Windows). L0 · fix J · adopt.
- [ ] **GV15** `PORTABLE-PATHS`: no name Windows refuses (`CON`, `aux.py`, a trailing dot or space,
  `:*?"<>|`). L0 · fix J · adopt.

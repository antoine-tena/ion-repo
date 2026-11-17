# ion-repo#T-333 · No Python needed: a signed binary, npx, the browser
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from ion-repo#T-316 on 25 October 2026 (kiln score ideas of 24 October 2026: Every forge,
  CI, host and machine, Outputs and integrations)

Planned in v0.8.4, "No Python needed": A single signed binary, `npx kiln-cli score` for JavaScript
machines, and the score in a browser if the forges allow it; a language server only if ion-repo#T-117
reopens.

- [ ] **K02** A single signed binary for machines without Python or uv (PyApp, which bootstraps
  through uv, or a frozen build), on each GitHub release.
- [ ] **K03** `npx kiln-cli score` for JavaScript-only machines: a small npm package that runs the
  binary.
- [ ] **K06** In the browser with Pyodide, on a tarball fetched from the forge's API, no server at
  all; to verify (CORS on the tarball endpoints).
- [ ] **L12** A language server: diagnostics for place rules in any editor, code actions for
  scripted fixes ⚠ ion-repo#T-117 (a VS Code extension) is declined for now; a language server serves every
  editor at once, only if adopters ask.

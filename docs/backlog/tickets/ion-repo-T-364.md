# ion-repo#T-364 · Credentials under one `.secrets/` folder, caches hidden from the editor
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: antoine, 26 October 2026: "all the dot folders, shouldn't they go in one folder?";
  a real repo counted 15 `.<service>/` folders at its root, each ignored by its own hand-written
  line of `.git/info/exclude`, written three different ways

- [ ] `.<service>/` becomes `.secrets/<service>/` (`token`, `config`): the skill `token`, the
  machine's global instructions (chezmoi), kiln's own scripts that read `.pypi/`, `.devto/`,
  `.bluesky/`; read `.secrets/<service>/` first and the old path as a fallback for a while.
- [ ] `.secrets/` in the template's `.gitignore`: one tracked line protects every service,
  present and future, in every clone (today a forgotten exclude line and `git add .` commit a
  token); a matching `Read(.secrets/**)` deny in `.claude/settings.json` keeps it from agents
  (ion-repo#T-200).
- [ ] `kiln update` offers to move the existing `.<service>/` folders (untracked: moved on the
  machine, never committed), and says which files still quote the old paths.
- [ ] `files.exclude` in `template/.vscode/settings.json.jinja`: `__pycache__`, `.mypy_cache`,
  `.pytest_cache`, `.ruff_cache` (and the stack's caches); kiln's own `.vscode/settings.json`.
- [ ] A secrets folder holds secrets only: code (scripts next to a token) and captures go to
  `scripts/` or a cache.
- [ ] ⚠ breaking: the credentials convention changes; conversion in `kiln update`, both
  references and READMEs.

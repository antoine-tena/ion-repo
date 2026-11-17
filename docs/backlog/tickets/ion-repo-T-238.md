# ion-repo#T-238 · Only what changed: `--changed`, `--watch`, the edit hook
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Speed), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.26, "Only what changed, right after each edit": Tests and score rechecked on the
changed files only, on save and in Claude Code's edit hook, in milliseconds.

- [ ] **J11** `--changed`: only files changed since the merge base, and the repo-level rules whose
  inputs changed, are checked again.
- [ ] **J12** `--watch`: re-score on save (watchfiles, Rust), the changed file only.
- [ ] **J13** The Claude Code edit hook re-scores the edited file in milliseconds and tells Claude
  only what is new; one engine with the charter's `check_file.py`.

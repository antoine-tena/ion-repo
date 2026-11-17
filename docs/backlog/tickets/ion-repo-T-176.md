# ion-repo#T-176 · `kiln fix` options: several rules, `--skip`, `--json`, `--pr`, `--dry-run --verify`
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: review of `kiln fix` asked by antoine, 24 October 2026

- [ ] `--rule` takes several rules; `--skip RULE` leaves some out.
- [ ] `--json`: the outcomes for the CI and the skills (`/kiln:modernize`, kiln-bot).
- [ ] `--pr`: the branch pushed and a pull request opened with the score before and after and
  the why of each commit (the base kiln-bot reuses, ion-repo#T-59).
- [ ] `--dry-run --verify`: the checks run on the throwaway copy too.
- [ ] The references in both languages and the README updated with the options
  (`tests/test_docs.py`).

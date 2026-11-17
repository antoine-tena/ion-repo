# ion-repo#T-443 · `ion repo update` reports conflicts that do not exist
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-09
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-03 to 2026-11-09, `12f0c83b` 23:16; the issue written then was refused by the permission check (23:29), never posted

- [ ] `git grep -l --untracked "<<<<<<< before updating"` also matches a committed, unmodified file holding that text (a merge tool's constants, its tests), then conversions and dependency upgrades are skipped until `--no-template`.
- [ ] Search only the files the template step changed; a test with such a file.

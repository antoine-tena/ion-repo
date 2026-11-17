# ion-repo#T-431 · `/repo:release` merge-back: a lockfile conflict is regenerated, never sided
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-03
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-03, a release merged back into
  `develop` (21:45)

The release had raised vulnerable packages; merging it back, the `uv.lock` and `pnpm-lock.yaml`
conflicts were resolved on `develop`'s side, and `develop` kept 6 high vulnerabilities the
release had fixed.
- [ ] Step 9: on a lockfile conflict, keep the integration branch's manifest, relock (`uv lock`,
  `pnpm install --lockfile-only`) with at least the release's versions of the packages it
  raised, then the vulnerability audit before the merge commit.
- [ ] The merge-back is refused while the audit finds a high or critical the release had fixed.

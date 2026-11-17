# ion-repo#T-430 · `/repo:release`: a red CI on an older cut looks for its fixes in `develop` first
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-03
- **Effort**: XS · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-03, the same release run twice
  (16:03–16:27, 21:05)

A release cut on a planned commit weeks behind `develop` failed CI on tests `develop` had already
fixed; both sessions found the fixes by hand, one after picking between two parallel series.
- [ ] Step 5 of the skill: for each failing file, `git log <release>..origin/develop -- <file>`
  first; a test-only or fix-only commit is cherry-picked (`-x`), never a feature.
- [ ] A fix that bumps a major version (a dependency) is flagged at the go-ahead, not taken
  silently.

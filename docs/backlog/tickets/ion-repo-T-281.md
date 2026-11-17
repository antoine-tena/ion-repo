# ion-repo#T-281 · Git and versions rules from history: commits, branches, releases, tags
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Git and versions, Community), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.48, "History: how the repo is worked": Commit sizes and messages, merges and branch
names, releases and their notes, fixes that come with a test, all read from history.

The six drafts are questions about history: `--history` (M) gives them detectors.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **GV01** `SMALL-COMMITS` (draft): median size of the last hundred non-merge commits, and the
  share of subjects in the Conventional Commits form. L5 · ratchet · trial.
- [ ] **GV02** `BRANCH-NAMES` (draft): merged branches' names, from merge subjects or the forge,
  carry a type prefix. L5 · fix J · trial.
- [ ] **GV03** `MERGE-COMMITS` (draft): merges kept on the integration branch, visible in history,
  where the profile asks for them. L5 · fix J · assess.
- [ ] **GV04** `NO-COMMIT-ON-INTEGRATION` (draft): non-merge commits made straight on the
  integration branch, bots aside; branch protection with `--online`. L5 · ratchet · trial.
- [ ] **GV05** `RELEASE-NOTES` (draft): each release tag has its CHANGELOG entry or forge release,
  breaking changes first. L5 · fix J · trial.
- [ ] **GV06** `RELEASES-FROM-MAIN` (draft): release tags reachable from main, deploy workflows
  triggered by tags. L5 · fix J · trial.
- [ ] **GV07** `CHANGELOG`: a `CHANGELOG.md` in the Keep a Changelog shape, or generated
  (release-please, git-cliff). L0 · fix S · trial.
- [ ] **GV08** `SEMVER-TAGS`: release tags parse as versions and only go up. L5 · fix J · trial.
- [ ] **GV09** `SIGNED-TAGS`: release tags signed (SSH or GPG), verified with `--online`. L5 · fix J
  · assess.
- [ ] **GV16** `BLAME-IGNORE-REVS`: mass-reformatting commits listed in `.git-blame-ignore-revs`. L5
  · fix S · trial.
- [ ] **CM08** `MAINTAINED`: commits or releases in the last 90 days, or the README says the project
  is finished or archived (Scorecard's Maintained). L5 · fix J · trial.

# ion-repo#T-401 · Updating a family of repos, stopping only at real conflicts
- **Type**: improvement
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-31
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: session bc540ab5 (kiln becomes ion-repo), 2026-10-31, by /learn:distill

`ion repo update --all` merges straight away. Moving 18 repos needed three throwaway scripts:
update each on a branch in its worktree, settle the conflicts that differ only by a name, check,
then merge, push and clean up. The middle ground is missing.
- [ ] A mode that prepares every repo on its branch, reports each one (conflicts left, check), and
  merges only those that are clean, after a yes.
- [ ] `frozen_repos` respected, as `--all` does.

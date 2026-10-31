# ion-repo's `ion-repo` plugin

The plugin every ion-repo project enables (`repo@ion-repo`).

- `skills/`: the `/ion-repo:…` skills (`worktree`, `merge`, `release`, `cleanup`, `review`,
  `backlog`, `update`, `adopt`, `report`, `token`, `contribution`, `good-first-issues`).
- `hooks/`: the hooks (`hooks.json` says when each one fires): branch guard, protected files,
  check of the edited file, rtk, update offer at session start (`reminders.py` paces it).
- `scripts/`: the status line, worktree preparation.

**Do not edit these files from a project**: outside the ion-repo repo, this directory is Claude
Code's plugin cache, overwritten at each update. Changes go to
https://github.com/antoine-tena/ion-repo (`plugins/repo/`): on a branch for its maintainer, through
the `/repo:report` skill (issue or pull request) for everyone else.

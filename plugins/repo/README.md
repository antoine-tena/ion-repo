# ion-repo's `repo` plugin

The plugin every ion-repo project enables (`repo@ion-repo`).

- `skills/`: the `/repo:…` skills (`worktree`, `merge`, `release`, `cleanup`, `review`,
  `backlog`, `update`, `adopt`, `modernize`, `resize`, `report`, `token`, `prompt`, `pause`,
  `contribution`, `good-first-issues`).
- `hooks/`: the hooks (`hooks.json` says when each one fires): branch guard, protected files,
  check of the edited file, rtk, update offer at session start (`reminders.py` paces it).
- `output-styles/`: `debrief`, the end-of-work report, forced wherever the plugin is enabled.
- `scripts/`: the status line, worktree preparation.

**Do not edit these files from a project**: outside the ion-repo repo, this directory is Claude
Code's plugin cache, overwritten at each update. Changes go to
https://github.com/antoine-tena/ion-repo (`plugins/repo/`): on a branch for its maintainer, through
the `/repo:report` skill (issue or pull request) for everyone else.

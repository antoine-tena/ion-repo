# kiln's `kiln` plugin

The plugin every kiln project enables (`kiln@kiln`).

- `skills/`: the `/kiln:…` skills (`worktree`, `merge`, `release`, `cleanup`, `review`,
  `backlog`, `update`, `adopt`, `report`, `token`, `contribution`, `good-first-issues`).
- `hooks/`: the hooks (`hooks.json` says when each one fires): branch guard, protected files,
  check of the edited file, rtk, update offer at session start (`reminders.py` paces it).
- `scripts/`: the status line, worktree preparation.

**Do not edit these files from a project**: outside the kiln repo, this directory is Claude
Code's plugin cache, overwritten at each update. Changes go to
https://github.com/antoine-tena/kiln (`plugins/kiln/`): on a branch for its maintainer, through
the `/kiln:report` skill (issue or pull request) for everyone else.

# ion-repo#T-385 · `kiln session move`: a session filed under its repo afterwards
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-30
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: the user, 2026-10-30, after a session started in `~/code` created the repo
  `Polytech/mobilite` and worked in it

`place.py` never moves a session, and that stays: a task that belongs to a repo is restarted
there. But a session started outside any repo sometimes creates the repo it then works in, and its
transcript stays under `~/.claude/projects/-home-antoine-code/`: `claude --resume` in the repo
does not list it. It had to be copied by hand, and the live session could not be moved, its file
still being written. Filing it afterwards is the need, not avoiding the restart.
- [ ] `kiln session move <id> <repo>` moves `~/.claude/projects/<encoded launch folder>/<id>.jsonl`,
  and its `<id>/` folder when there is one, to the repo's project folder (created if missing),
  then prints the line that resumes it: `cd <repo> && claude --resume <id>`.
- [ ] A session still being written (the current one, or a transcript changed in the last
  minutes) is refused, with the exact command to run once it is closed.
- [ ] Without `<id>`: the sessions of the launch folder whose `cwd` or edited files point into a
  repo below, offered for moving.
- [ ] The `cwd` recorded inside the transcript is left as it is; check that `--resume` from the
  repo works with it.
- [ ] Learned by moving ~80 sessions by hand on 2026-10-30: the repo is guessed from the paths the
  session's tools touched (absolute, `~/`, and `cd`/`-C` relative to its `cwd`), the old paths of a
  reorganised `~/code` mapped to their new place first; a session on all repos at once stays put.
  A session that ran on across a folder rename is split in two project folders under the same id:
  append the tail to the head. The `memory/` of a project folder whose path no longer exists moves
  too (MEMORY.md lines merged). Project folder names start with `-`: shell tools take them for
  options, so work in Python or with `./`. Keep a journal of the moves to undo them.
- [ ] Learned by moving the Ion family on 2026-10-31: a folder moved under open sessions also needs
  its worktrees repaired (`git worktree repair`), editable tools reinstalled, `.venv` dropped, the
  paths in `~/.claude` rewritten, a forward left at the old path. A symlink between project folders
  makes one session appear twice: `ion learn digest <id>` then refuses it as ambiguous.

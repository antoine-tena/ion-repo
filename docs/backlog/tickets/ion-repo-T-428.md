# ion-repo#T-428 · The `repo` plugin's hooks run in its mod, no Python per tool call
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-03
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: session of 3 November 2026, after ion-repo#T-427 was dropped: the events of Claude
  Code 2.1.311's mods go well beyond `ui.render` (`tool.check`, `tool.call`, `prompt.submit`,
  `prompt.context`, `session.start`, `skill.prompt`…)

Every Bash call starts two Python processes (`branch_guard.py`, `rtk.py`), every Edit or Write
one (`protect_files.py`). The `repo` plugin's mod (`plugins/repo/hooks/chat.tsx`) already runs
inside Claude Code: a `tool.check` there costs no process at all. The other Ion tools have no
hooks; only `repo` is concerned.
- [ ] Found first, with a throwaway mod and `claude plugin test`: what a mod may do. Read files
  and git state, start a process (`rtk`, `ruff`), rewrite a tool's input as `rtk.py` does, deny
  with a reason Claude reads, add context at `session.start` / `prompt.submit`.
- [ ] `branch_guard`, `rtk` and `protect_files` moved into the mod's `tool.check` if it can do
  their job, measured before and after; ion-repo#T-183 is then done by this ticket. Otherwise
  this box goes to `rejected.md` with why, and ion-repo#T-183 stays.
- [ ] The context hooks (`session_start`, `reminders`, `others`, `paused`, `place`,
  `first_prompt`) moved too only if the mod reads what they read and it is faster.
- [ ] Left as they are: `check_file.py` unless a mod can start `ruff`, the status line (no mod
  component draws it).
- [ ] The old script paths stay as relays: open sessions call the hooks in the main tree, and
  `tests/test_plugins.py` checks them. Both references and the repo map in `CLAUDE.md`
  updated in the same branch.
- [ ] What the boxes find about the mod API (each event's props, `$` and the shape of what
  `$.process.run` returns, how `claude plugin test` calls a handler) kept in one reference page of
  the repo: four sessions of 3 November 2026 rediscovered it from the binary (`/learn:distill`).

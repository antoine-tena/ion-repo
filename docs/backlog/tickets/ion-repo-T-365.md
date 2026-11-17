# ion-repo#T-365 · Claude can't call a task done with new findings: a Stop hook
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-27
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: review of similar public projects, 26 October 2026 (`Heyosseus/sloppy`'s finish
  check)

Planned in v0.6.26, "Only what changed, right after each edit". kiln checks each file after an
edit (`check_file.py`, `PostToolUse`) but has no `Stop` hook: Claude can say "done" with a
finding still open.
- [ ] A `Stop` hook runs the charter (then the grid, with ion-repo#T-238's `--changed`) on the files the
  session changed and hands Claude the findings at or above a threshold.
- [ ] Only what the session introduced: a finding the file already had is never reported, so
  Claude doesn't wander off fixing code nobody asked it to touch.
- [ ] It blocks once per stop: a false alarm costs one round trip, not the session; if the check
  can't run (no git, a broken config), Claude carries on.
- [ ] The threshold is a `kiln set` key; its cost per stop measured and written in the reference.

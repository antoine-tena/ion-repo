# ion-repo#T-183 · One hook per Bash call instead of two
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: same measurement as ion-repo#T-180, 24 October 2026

Every Bash call of Claude Code waits for two Python processes in a row: `branch_guard.py`
(45 ms) then `rtk.py` (100 ms: two `git config`, then `rtk hook claude`), about 150 ms paid
hundreds of times a session.
- [ ] One `PreToolUse` hook for Bash doing both: one Python start, the git config read once.
  Expected gain 30 to 40 ms per call, measured before and after.
- [ ] The old script names stay as relays: open sessions call the hooks in the main tree
  (`CLAUDE.md`, "Contrôles"), and `tests/test_plugins.py` checks the relays.
- [ ] Left as they are, measured that day: the status line (140 ms, 16 commands in sequence,
  never blocks Claude), `check_file.py` (70 ms), the CLI start (120 ms), `kiln score` (0.4 s),
  `kiln check` (0.8 s), `charter` (0.6 s).

# ion-repo#T-383 · `/kiln:worktree` reports two false failures
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-30
- **Effort**: XS · **Owner**: — · **Due**: —
- **Origin**: grog `/grog:distill` over four sessions of 29 October 2026, and the grog session
  that distilled them

- [ ] Step 3 says to run `.claude/worktree-setup.sh` "if the repo provides it": Claude checks with
  `ls`, which exits 2 when it is absent, so the step ends in `Exit code 2` on every repo without
  one (five sessions out of five). `prepare-worktree.sh` runs the setup script itself when it
  exists, and the skill drops the check.
- [ ] Step 4: `EnterWorktree` refuses ("the current directory is not in a git repository") when
  the session was opened above the repo (`~/code/Keramos`, twice). The skill says so and goes on
  with absolute paths, instead of a bare error.

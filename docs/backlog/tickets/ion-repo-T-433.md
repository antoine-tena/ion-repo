# ion-repo#T-433 · In a session isolated in a worktree, edit with Edit/Write, never a script
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-03
- **Effort**: XS · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-03, four refusals in two sessions on
  Ion tools (16:25, 21:20, 21:24, 21:27)

Claude Code refuses, in a session isolated in a worktree, a Bash call it cannot prove stays
inside ("too complex to verify": heredoc to a file, inline Python rewriting a file, a computed
`cd`). Each time the session retried with Edit, losing a turn. [AI-CONTEXT]: the generated rules
say it where they speak of worktrees.
- [ ] One line in the generated rules: in a worktree session, change files with Edit/Write
  (`cat >> file <<EOF` and `python - <<EOF` are refused), commands from the worktree root.
- [ ] `ion repo update` brings it to generated repos.
- [ ] `rtk` causes many of the refusals too (72 in a week on one repo): a glob or a variable in a command it rewrites reads as too complex to verify. The rule says so: plain paths, no glob, in an isolated session.

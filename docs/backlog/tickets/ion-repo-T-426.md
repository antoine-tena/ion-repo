# ion-repo#T-426 · An orchestrator session: a skill that holds the role
- **Type**: idea
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-02, the session at the root of the family (17:18–18:16)

antoine runs one session per repo in parallel and a "boss" session that does not code: it checks
each pasted report against git and the files, compares it with the decisions, blocks what leaves
the plan, spots duplicate or stale tickets, and gives the `cd … && claude '…'` line for the next
session. The role was typed again as a long prompt after each `/clear`, and "what do I tell it?"
came back on every report. A skill (`/repo:boss`) that states the role, reads the decisions from
memory and the backlogs, verifies a report (branches merged, pushed, worktrees gone, tickets
closed) and answers with the verdict and the next command; never codes, never spawns subagents.
- [ ] A pasted report is checked against git, not taken on trust.
- [ ] Survives a `/clear`: nothing to retype but `/repo:boss`.

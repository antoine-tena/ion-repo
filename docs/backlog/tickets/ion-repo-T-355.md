# ion-repo#T-355 · The repo's update offered outside Claude Code too
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q94: "I'd like kiln's update offers to happen
  without Claude Code too"), decision 35

The tool's own update is offered after a command typed in a terminal, but never to a checkout
like antoine's, which is why he hasn't seen it. The repo's `kiln update` is offered only in a
Claude session.
- [ ] A kiln command typed in a terminal, in a repo behind the latest release, ends by offering
  `kiln update`, at the pace of `update-reminders` (ion-repo#T-45); a yes runs it on a branch and merges it
  when the checks pass, a conflict sends the user to `/kiln:update`.

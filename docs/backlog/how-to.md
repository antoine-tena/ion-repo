# 📖 How to use (humans and agents)

This folder is ion-repo's only work list. [README.md](README.md) is the index (north star, next
free ID, releases in order); [tickets/](tickets/) holds one file per open ticket,
[releases/](releases/) one file per planned release; [done.md](done.md), the closed tickets, one
line each, most recent first (written by `/repo:backlog done`), [rejected.md](rejected.md), what
was turned down, dropped or ruled out for good, and [urgent.md](urgent.md), what only a human on
the team can do (access, payment, decision), one checkbox per action (counted by the status
line). [vision.md](vision.md) and [kiln-score-the-thesis.md](kiln-score-the-thesis.md) are where
the tickets come from.

An audit writes its dated report next to these files (`audit-<topic>-YYYY-MM-DD.md`) while it
runs, copies its open findings into tickets (with a pointer to their lines), then moves to
`docs/_archive/YYYY-MM-DD-topic/`. Archives **can be read, but everything in them is old and must
be checked** against the current code; they are never edited.

**A ticket** = one file, `tickets/ion-repo-T-NN.md`: a heading, six fixed lines, then the details:

    # ion-repo#T-NN · Short title that says what to achieve
    - **Type**: task
    - **Priority**: 🟡 normal
    - **Status**: todo
    - **Opened**: YYYY-MM-DD
    - **Effort**: S · **Owner**: … · **Due**: —
    - **Origin**: where it comes from

    Why, what to do (as a `- [ ]` checklist when there are several steps), where to look.

- **ID** `ion-repo#T-NN`: stable, never reused, always written whole, here too, and quoted as is
  in commits and pull requests (decision of antoine, 1 November 2026; a branch keeps the number
  alone, `fix/t07`; tickets opened before 16 October 2026 were `AF-NN`, same number). A ticket of
  another repo carries that repo's name (`ion-learn#T-03`). The next free one is in the index
  (`Next free: ion-repo#T-NN`), moved on by each new ticket. A renamed repo: `ion repo set name=…`
  moves its own prefix in its own tracking, file names included, same numbers; citations in other
  repos keep the old name, which the forge redirects; old commits are never rewritten.
- **Type**, one of: `bug` (something is broken); `improvement` (it works, it could work
  better); `idea` (nothing exists yet, to be explored); `task` (work that is neither: a release,
  a decision, a check).
- **Priority**, one of: `🔴 critical` (now), `🟠 important` (before the north star),
  `🟡 normal`, `⚪ background` (long-running work, debt, ideas still to be explored).
- **Status**, one of: `todo`; `in progress — branch <name>, since YYYY-MM-DD`;
  `blocked — waiting for <who or what>`; `to verify — <where>`.
- **Effort**, in Claude Code session time on the Pro plan ion-repo is built with: XS under
  15 minutes, S about half an hour, M about an hour, L two to three hours (split it when it can
  be split). Measured on kiln: on 16 October 2026, 9.3 session-hours shipped four promotions and
  the move to English (about 8,000 lines changed): some twenty times faster than the former
  estimates in human time. **Session** (optional, at the end of the Effort line):
  `· **Session**: medium, fix/two-coaches`, the effort of the session that works it, read by
  `ion repo session`.
- **Budget**: the Pro quota restarts every Tuesday at 8:00 (Paris). It lasted 42 session-hours
  the week of 6 October and 33 the week of 13 October (limit reached on Friday at 14:03), all
  projects together; a 5-hour window runs out after 2 to 3.5 hours of work. kiln plans on
  25 session-hours a week, about 7 per release, spread over the week (about 5 a day, all
  projects): spent by Friday, it leaves the Saturday and Monday releases without budget. No
  fleet of subagents, no headless run without a budget said beforehand.
- **Releases**: one file per planned release in [releases/](releases/), which places every open
  ticket and every kiln score idea in a planned release (`/repo:backlog plan`); each ticket line
  ends with its session's effort and its `ion repo session` command; numbers are planned, not
  promised, until the candidate is cut. The plan's notes and what shipped:
  [releases/README.md](releases/README.md).
- **Closing a ticket**: delete its file, take its line out of its release, and add a line at the
  top of [done.md](done.md):
  `- **YYYY-MM-DD** · ion-repo#T-NN · Title — what was done (branch) · opened YYYY-MM-DD`.
- **Details in archived audits**: when a ticket quotes lines of `docs/_archive/`, the original
  finding is there in full; it is old, check it against the current code.
- **Locations quoted are hints, not addresses.**
- **Overview**: `ion repo backlog`, one line per open ticket; then read only the files of the
  tickets involved.

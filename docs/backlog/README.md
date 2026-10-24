# Backlog

What is left to do on kiln, what is done, and what was turned down. **This folder is the
only up-to-date source.**

| File | Content |
|---|---|
| [backlog.md](backlog.md) | **Everything open**: the single list ordered by priority, one `T-NN` ticket per thing to do with its type, status and details; then the vision that orders it, then the `kiln score` ideas (not tickets: one becomes a ticket when planned) |
| [done.md](done.md) | The closed tickets, one line each, most recent first |
| [rejected.md](rejected.md) | What was turned down, dropped, or ruled out for good |
| [urgent.md](urgent.md) | What only a human on the team can do (access, payment, decision), one checkbox per action |

An audit writes its dated report next to these files (`audit-<topic>-YYYY-MM-DD.md`) while it
runs, copies its open findings into [backlog.md](backlog.md) (with a pointer to their lines),
then moves to `docs/_archive/YYYY-MM-DD-topic/`. Archives **can be read, but everything in them
is old and must be checked** against the current code; they are never edited.

## How to use (humans and agents)

**A ticket** = a `### T-NN · Title` heading, then five fixed lines, then the details:

    ### T-NN · Short title that says what to achieve
    - **Type**: task
    - **Status**: todo
    - **Opened**: YYYY-MM-DD
    - **Effort**: S · **Owner**: … · **Due**: —
    - **Origin**: where it comes from

    Why, what to do (as a `- [ ]` checklist when there are several steps), where to look.

- **ID** `T-NN`: stable, never reused, quoted as is in commits and branches (tickets opened
  before 16 October 2026 were `AF-NN`, same number). The next free one is at the top of
  [backlog.md](backlog.md) (`Next free: T-NN`).
- **Type**, one of: `bug` (something is broken); `improvement` (it works, it could work
  better); `idea` (nothing exists yet, to be explored); `task` (work that is neither: a release,
  a decision, a check).
- **Status**, one of: `todo`; `in progress — branch <name>, since YYYY-MM-DD`;
  `blocked — waiting for <who or what>`; `to verify — <where>`.
- **Priority** = the section the ticket lives in; changing it means moving the ticket.
  🔴 critical (now), 🟠 important (before the north star), 🟡 normal, ⚪ background
  (long-running work, debt, ideas still to be explored).
- **Effort**, in Claude Code session time on the Pro plan kiln is built with: XS under
  15 minutes, S about half an hour, M about an hour, L two to three hours (split it when it can
  be split). Measured on kiln: on 16 October 2026, 9.3 session-hours shipped four promotions and
  the move to English (about 8,000 lines changed): some twenty times faster than the former
  estimates in human time.
- **Budget**: the Pro quota restarts every Tuesday at 8:00 (Paris). It lasted 42 session-hours
  the week of 6 October and 33 the week of 13 October (limit reached on Friday at 14:03), all
  projects together; a 5-hour window runs out after 2 to 3.5 hours of work. kiln plans on
  25 session-hours a week, about 7 per release, spread over the week (about 5 a day, all
  projects): spent by Friday, it leaves the Saturday and Monday releases without budget. No
  fleet of subagents, no headless run without a budget said beforehand.
- **Releases**: the `## 🚀 Releases` section at the top places every open ticket in a planned
  release (`/kiln:backlog plan`); numbers are planned, not promised, until the candidate is cut.
- **Closing a ticket**: remove it from its section and add a line at the top of
  [done.md](done.md): `- **YYYY-MM-DD** · T-NN · Title — what was done (branch) · opened YYYY-MM-DD`.
- **Details in archived audits**: when a ticket quotes lines of `docs/_archive/`, the original
  finding is there in full; it is old, check it against the current code.
- **Locations quoted are hints, not addresses.**
- Overview: `grep -E '^(## |### T-|- \*\*Status)' docs/backlog/backlog.md`.

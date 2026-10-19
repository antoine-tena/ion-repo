---
name: backlog
description: Pick the next ticket from docs/backlog/backlog.md, add a ticket (bug, improvement, idea, task), record a ticket as started or done, or plan which tickets go into the next releases, in a repo that tracks its work this way. Use when the user asks what to do next, wants to note something to do or an idea, after starting or finishing a ticket, or when they ask what the next versions should contain.
argument-hint: "[T-NN | new <what> | start T-NN | done T-NN | plan]"
---

In a repo without `docs/backlog/backlog.md`, say so and offer to set it up: a kiln repo has it
by default (`kiln update` brings it to an older repo, and moves an old `docs/a-faire/` there);
elsewhere, copy the structure of kiln's template (`template/docs/backlog/`).

`docs/backlog/backlog.md` is the **only** up-to-date source: everything is there, ordered by
priority (🔴 critical, 🟠 important, 🟡 normal, ⚪ background), with the "✅ Done" log at the
bottom. `docs/backlog/rejected.md` lists what was turned down. **Read the "How to use" section
at the top of the file first**: it wins if it differs from what follows.

A ticket: a `### T-NN · Title` heading, then the lines `- **Type**:`, `- **Status**:`,
`- **Opened**: YYYY-MM-DD`, `- **Effort**: … · **Owner**: … · **Due**: …`, `- **Origin**: …`,
then the details (`- [ ]` boxes). Types: `bug`, `improvement`, `idea`, `task`. Statuses:
`todo`, `in progress — branch <name>, since YYYY-MM-DD`, `blocked — waiting for <who or what>`,
`to verify — <where>`. **Owner**: `—` (free), `@login` (reserved for that GitHub account), a
first name (reserved for that person too, login not written yet), `Claude`, or
`contributor — #NN`. The user's account is `gh api user --jq .login` (otherwise
`git config user.name`); a ticket owned by **anyone else** is their work: never plan, start or
code it, even partly, and say who to ask. **Only the user's own login is ever written**: when it
appears in no **Owner** but first names do, ask once which first name is theirs and replace that
one alone by their `@login` (on a branch); the others write theirs in their own session. Never
write, guess or ask for another member's login. Overview:
`grep -E '^(## |### T-|- \*\*Status)' docs/backlog/backlog.md`.

`docs/_archive/` is **read** when a ticket points to lines of an archived report, but
everything in it is old: check it against the current code before acting. Never edit an
archived report.

**No argument**: propose the next 3 tickets in section order (critical first), following the
north star in the header and skipping `blocked` tickets, those owned by another account,
and those reserved for outside contributors (**Owner**: `contributor — #NN`, skill `/kiln:good-first-issues`); for each, the ID, one sentence, the
effort, and the owner. List separately the blocked tickets waiting for the user themselves.
Quickly check in the code that the ticket is not already done (the locations quoted are hints,
often stale).

**With an ID**: if its **Owner** is another account, stop there: show the ticket, say whose
it is and that they take it (or hand it over by changing the owner). Otherwise show the full ticket (and the archive lines it quotes), find the files involved
in the current code, propose a short plan, then create the branch (in a worktree, skill
`/kiln:worktree`) and set the status to `in progress — branch …`.

**`new <what>`**: add a ticket with the "next free" ID from the "How to use" section (then
increment it), the type that fits (`idea` when nothing is decided yet), `todo`, today's date as
`Opened`, in the section matching its priority (⚪ background for an idea still to explore).
If the backlog has a `## 🚀 Releases` section, also place the ticket in the release where it
fits best, **whatever its position**: a new idea may join v0.4.1 while v0.5.3 is the last
planned one; create a release only when none fits, following the rules of `plan`.

**`start T-NN`**: refused on a ticket owned by another account (see above); otherwise set the
**Status** line to `in progress — branch <name>, since YYYY-MM-DD`, and a free **Owner** (`—`)
to the user's `@login`.

**`done T-NN`**: remove the ticket from its section and add at the **top** of the "✅ Done" log a
line `- **YYYY-MM-DD** · T-NN · Title — what was done (branch) · opened YYYY-MM-DD`. A
half-done ticket stays in place: tick the steps done, write what is left. Keep the style and
tone of the file. Remove the ticket from `## 🚀 Releases` too; a release left empty means it is
ready for its candidate: say so.

**`plan`**: put **every** open ticket into a planned release, written straight into the
`## 🚀 Releases` section just above 🔴 critical (create it if missing), then show the plan. Read
every open ticket (priority, effort, status, `blocked — waiting for …`, what it touches) and the
versioning rules of the repo's `CLAUDE.md`. The plan is a living draft, not a queue: redo the
groupings freely each time, as long as the result follows these rules.
- **Every ticket has a release.** No leftover pile: background work, debt and ideas go into the
  release whose theme they serve; a ticket blocked on the user goes into the release it makes
  sense in, marked `(blocked: <who>)`; a ticket waiting for another one comes in the same
  release or a later one.
- **A release is a real grouping.** Its tickets share one outcome a user can notice or a
  milestone it unblocks, and its name says that outcome in a few words
  (`v0.4.1 · Nothing to trip on for a beginner`), never a list of contents or `misc`. Look for
  links across priorities: a 🟡 ticket that completes a 🟠 one goes with it.
- **No useless release.** A release that only holds a stray XS ticket or a vague theme is
  merged into a neighbour; a release too big to ship within the cadence the repo's
  `CLAUDE.md` sets (about a week when it says nothing) is split along a real seam. Urgent fixes (a 🔴 bug) may stand alone.
- **Order**: what blocks first, then 🔴 then 🟠 then the rest; within that, the release that
  makes the north star of the header closest comes first.
- **Numbers are planned, not promised.** In 0.x each release bumps the patch; a group that
  forms a milestone may be proposed as a minor bump, saying why in the release line: the user
  decides (until then keep the patch number). Inserting or merging releases renumbers the
  later ones. A release whose candidate is tagged is frozen: no ticket enters or leaves it.
- **Breaking changes** (CLI, `copier.yml` questions, generated tree, workflow inputs, skill and
  hook names, charter rule IDs) are flagged `⚠ breaking` on the release: they open its release
  note and need their conversion in `kiln update`.

Format of the section, one block per release, in order:

    ### v0.4.1 · Nothing to trip on for a beginner
    Why these go together, in one sentence. ⚠ breaking: the size question goes away.
    - T-39 · Start light, grow with the repo (M)
    - T-42 · The git flow grows with the size (M)

Tickets stay in their priority sections; the release section only quotes ID, short title and
effort. After writing, show the user the releases (name, tickets, why) and what moved since
the last plan; they reshuffle by asking.

An ID is never reused. Changes are committed on the work branch, never on the integration
branch. Never copy a ticket into `rejected.md` without an explicit decision from the user.

---
name: debrief
description: End-of-work report read in five seconds - the real git state first, then what matters, what doesn't work, what Claude does next, what only the user can do
keep-coding-instructions: true
force-for-plugin: true
---

# Debrief

Work the way you always do; this style only shapes the message that closes a piece of work: a
task, a fix, a skill run to its end. Any other answer (a question, an explanation, a progress
note, a question to the user, a stop or a refusal met along the way) stays short and leads with
its result, without this format.

When you judge the format is not enough for what the user is waiting for (most often a long
output: a plan, an analysis, a review, a document), write it the way it reads best.

The reader scans it top to bottom and left to right, so the first sentence and the first word
of each line carry the message (bottom line up front; F-shaped reading, Nielsen Norman Group).

## The format

Exactly these parts, in this order, and nothing else:

1. **One result sentence, in bold, no symbol before it**, saying the real git state as it is
   now, checked, not hoped: merged into `<branch>`, pushed, worktree removed; or committed on
   `<branch>`, not merged; or not committed. A task without git work says its outcome instead.
2. **◆ Summary**, then the three points that matter most, numbered, one line each. A departure
   from the user's instructions, or a part of the request not done, always is one of them.
   Fewer than three when there are fewer.
3. **◆ Not working**: at most three bullets, each opening with `Broken:` (a defect seen) or
   `Not verified:` (not really run: a test skipped, a path not exercised, a check that could not
   reach its service). If there is none: "nothing known", then in a few words what was verified.
4. **◆ Next**: at most three actions Claude can do next, numbered from the most to the least
   logical, each with its why on the same line; the first ends with `← recommended`. One `ok`
   from the user starts it. The work just done comes first when it leaves a step (merge, fix,
   a box still open); otherwise, or after it, the next open tickets of `docs/backlog/backlog.md`
   the user may take (as `/repo:backlog` picks them), each with its full ID: `<repo>#T-20 · Try
   Easy!Appointments, the demo the meeting waits for`. Never a point made up to reach three;
   none at all when nothing follows and the backlog has nothing open for the user.
5. **◆ Your turn:** only what Claude cannot do for the user (a login, an interactive command, a
   restart, a decision), in one line, then the command in a single `bash` block when there is
   one. Leave the whole part out when there is nothing.

The titles are written in the user's language, each in bold after the same `◆` (the mark of
the Ion skill frame). In French: **◆ Résumé**, **◆ Ne fonctionne pas** (`Cassé :`,
`Pas vérifié :`, « rien de connu »), **◆ Suite proposée** (`← recommandée`), **◆ À toi :**.

## Lines

- Each line opens with its keyword: the thing, the verdict, the action, never "I", "Also" or a
  connector.
- One line per point, ranked by severity: what breaks or blocks first.
- No diff, no list of files touched, no command already run, no menu of options, no recap of
  the conversation.
- A path only when the user has to open the file, as `file:line` so it is clickable.
- The detail (files, commands, reasons) only when the user asks for it ("detail", « détaille »).
- Plain Markdown, no nested bullets, no emoji, no closing sentence.

## Inside the skill frame

When the answer is a skill's ([SKILL-FRAME]), the debrief is that answer: the frame's first rule
in its code block, then the debrief, then the second rule in its code block. The frame's lines
are the only thing outside the format.

## Example

```
**Merged into develop and pushed, worktree removed.**

**◆ Summary**
1. Status line shows the CI of the open branch, no longer develop's.
2. Cache of a day dropped: a fresh run shows within 5 seconds.
3. Windows not handled, against the request: no machine to try it on.

**◆ Not working**
- Not verified: a branch never pushed, its CI state stays empty.

**◆ Next**
1. Handle Windows in the status line, the part of the request still open ← recommended
2. Add a test for the never-pushed branch, the one path not run

**◆ Your turn:** restart Claude Code, the status line loads at launch.
```

---
name: prompt
description: Write a clean prompt, ready to paste, for a Claude Code session, a subagent, a system prompt or another model - goal and why, the session's context, limits, done-when, output. Use when the user asks to write, clean up or improve a prompt, or to turn a request into one.
argument-hint: "[what the prompt must get done]"
---

What the prompt must get done: `$ARGUMENTS`; without it, what the user just asked for. Talk to
the user in their language; write the prompt in the language of the model's work (English by
default, the user's language when the output is for people who read it, e.g. a French site's copy).

1. **Who reads it**: a Claude Code session (here or in another repo), a subagent, a system prompt
   (API, an app), another model or tool. Guess it from the request; ask one short question only
   when the answer changes the prompt and nothing gives it.
2. **Gather before writing**: the facts this session already holds go into the prompt (paths,
   ticket IDs, commands, the decision taken and the options turned down, what was tried and
   failed): the reader starts cold. Read a file rather than guess it; never invent a fact. A
   secret or real personal data never goes in.
3. **Write it**, plain and direct, as a brief to a smart colleague who knows nothing of this
   conversation:
   - **Goal** first, in one or two sentences, with **why** it matters: the reason lets the
     model make the right call in cases the prompt didn't foresee.
   - **Context**: only what changes the work (where it lives, what exists, the constraints of the
     project or the user's way of working); no history for its own sake.
   - **What to do**, as steps when the order matters; say what to do rather than what to avoid,
     and say whether to act or only to propose.
   - **Constraints and limits**: scope (what not to touch), decisions to bring back to the user,
     actions that need their yes.
   - **Done when**: the check that proves the work is finished (a test, a command, an output).
   - **Output**: the expected form (a file, a diff, a report of N lines, JSON with these keys);
     an example when the form is unusual.
   - Long material (a log, a document, data) goes in XML tags (`<log>…</log>`), before the
     question about it. No shouting (CAPITALS, "CRITICAL"), no padding, no role play unless it
     sets real expertise; as short as the task allows, as long as it needs.
4. **Sessions on backlog tickets** skip steps 2 and 3: the ticket is the brief. Run
   `ion repo session <repo>#T-NN [<repo>#T-NN…]` in the tickets' repo and give the line it prints,
   in a single `bash` block. It opens in the repo's main tree, names the session after the
   tickets, takes the effort and branch from the ticket's `**Session**` field (else `low` for XS
   or S, `medium` for M or L), and sends the session through `/repo:worktree`,
   `/repo:backlog start`, a failing test for a bug, and `/repo:merge`. A ticket that lacks the
   brief gets it written in the backlog first, never in the prompt.
   - **Effort**: `low` for a small, well-bounded ticket, `medium` by default; `high` only for
     money, concurrency or production data, said in one line above the command (`--effort`
     overrides, the ticket's field keeps the choice).
   - **Several sessions at once**: group the tickets so that no two sessions edit the same files;
     a ticket that needs another's merge waits for the next wave, said in one line. Each line
     gets `--note "Leave <files> alone (<repo>#T-NN, another session)."`: what only holds now
     goes in a note, never in the ticket.
   - Above each line, one line: its tickets, its effort and why.
5. **Give it** ready to use, then one or two lines: the choices made (reader, language, what was
   left out). For any other Claude Code session:
   - Write the prompt with the Write tool to `/tmp/<repo>-<subject>-prompt.md`, overwritten at each
     new version: a multi-line command pasted from the terminal comes back indented, and a heredoc
     then never closes.
   - Show the prompt in a code block, so the user can read it, then the one line to paste in a
     single `bash` block, which opens the session in the right folder:
     ```bash
     cd ~/code/<path>/<repo> && claude --model claude-opus-5-5 --effort medium --name "<subject>" "$(cat /tmp/<repo>-<subject>-prompt.md)"
     ```
   - Always `--model claude-opus-5-5`, an effort chosen as above (`medium` by default) and a
     `--name` that says the subject, written out. When the work needs a branch, the prompt's
     first step is `/repo:worktree <type>/<subject>`, the branch named by [BRANCHES]. Every other
     command that opens a session for the user (the debrief's Blocked part) is written the same
     way.

   Otherwise the prompt alone in a single code block, and where it goes (the `Agent` tool, a
   system prompt, another model). Don't run it unless the user asks.

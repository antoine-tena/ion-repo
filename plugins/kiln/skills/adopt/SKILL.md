---
name: adopt
description: Bring a repo that kiln did not generate to the level of kiln new (kiln adopt) - Claude rules, charter, pre-commit, CI, backlog, kiln update afterwards - without overwriting a file, on a branch then merged. Use when the user asks to adopt kiln in an existing repo.
---

Talk to the user in their language.

1. The open repo does not follow kiln yet: no `.copier-answers.yml` (generated or adopted:
   skill `/kiln:update`); otherwise say so and stop. A `charter.toml` without answers is a repo
   adopted before kiln 0.4.6: `kiln adopt` completes it. The `kiln` command is installed
   (`kiln --version`); otherwise give `uv tool install kiln-cli` and stop.
2. Ask for the size with the AskUserQuestion tool: `spark` (script, personal tool), `ember` (small
   app, low stakes, the default), `flame` (production, real users), `blaze` (several teams, high
   stakes).
3. Branch `chore/kiln-adopt` in a worktree (skill `/kiln:worktree`), then
   `kiln adopt --size <size>` in that worktree. It renders the template with the stack it finds
   in `backend/` and `frontend/` and lays every file the repo lacks; the files the repo has, and
   its code folders, go under `kept` in `.copier-answers.yml` and are never written by kiln.
4. Fill in the repo map of the new `CLAUDE.md` from the actual tree (its entry points, its
   folders), and say which kept files differ from the template the most (a README, its own CI):
   the user decides whether to bring them closer.
5. The debt the charter finds (a `Dockerfile`, a `pip install`…): show it and let the user choose,
   rule by rule, between fixing it now, removing the rule from `charter.toml`, or writing the fix
   down as a ticket (skill `/kiln:backlog`). Fix nothing without agreement.
6. Commit (`chore: adopt kiln`), then merge (skill `/kiln:merge`).

## Sum up

Stack found, files laid, files kept, size, debt found and what was done about it. A framework
found outside `backend/` and `frontend/` (a Vite app at the root) gets the common part only: say
so. From now on `kiln update` keeps the repo current, sparing what it keeps.

---
name: merge
description: Finish a piece of work - fast linters on the files the branch changed, merge into the integration branch (develop), push, delete the branch (and its worktree), update the repo's Claude Code plugin where it is installed. No CI at a merge: it only runs when a release goes out (/repo:release).
argument-hint: "[branch]"
---

Branch: `$ARGUMENTS`, otherwise the current branch. Integration branch: the one the project's
`CLAUDE.md` names, otherwise `develop` if it exists, otherwise `origin`'s default branch.

The merge happens here, directly: no pull request nor approval to wait for ([NO-COMMIT-ON-MAIN]).
A pull request already open for the branch turns "Merged" on GitHub by itself at the push of
step 4. Talk to the user in their language.

1. On the branch: everything is committed (`git status --porcelain` empty), otherwise stop and
   say so. Then review the branch (`/repo:review <branch>`): after the push of step 4, its
   commits are public for good. What the review tidies on the branch happens before the merge;
   what it leaves to the user, tell them and wait for their decision.
   Then the fast linters, in the branch's worktree, on the files the branch changed and nothing
   else (`git diff --name-only --diff-filter=d <integration>...<branch>`): `ruff check` and
   `ruff format --check` on its Python files, `eslint` on its JS/TS/Vue files, the like for
   other languages (ion-repo itself: `uv run ruff check <files>`, `uv run ruff format --check
   <files>`). No type checker, no test, no `ion repo check`, no `ion repo ci` at a merge: the release
   runs them all (choice of antoine, 21 October 2026). A branch with no such file runs nothing.
   A failure: fix it on the branch, never merge red.
2. Update the integration branch (`git pull --ff-only origin <integration>`), then
   `git merge --no-ff <branch> -m "Merge branch '<branch>' into <integration>"`, from the main
   tree when it is on the integration branch, otherwise with `git -C` on a worktree that is;
   never switch the branch of the main tree under another session.
3. On a conflict: stop, show the conflicting files, propose a resolution.
4. `git push origin <integration>`.
5. Delete the worktree and the branches right away: a merged branch is not kept aside. Only if
   the merge really is in `origin/<integration>`:
   - `git fetch -q origin`, then `git merge-base --is-ancestor <branch> origin/<integration>`
     succeeds: every commit of the branch, so each of its files, is in the published
     integration branch;
   - the worktree is clean (`git -C <wt> status --porcelain` empty).
   If the session was moved into the worktree (`EnterWorktree`), leave it first with
   `ExitWorktree` (`action: "keep"`): a session cannot stay in a folder that disappears.
   Then `git worktree remove .claude/worktrees/<name>` (never `--force`), `git branch -d
   <branch>` (never `-D`) and, if it exists on GitHub (`git ls-remote --heads origin <branch>`),
   `git push origin --delete <branch>`. If a check fails: delete nothing, say which one and why.
6. The repo ships a Claude Code plugin (`.claude-plugin/marketplace.json` at its root, as
   `ion repo set claude_plugin=true` writes it; ion-repo itself and every tool of the family): update the
   installed copy now, otherwise a skill just merged stays unknown (`Unknown command`) in every
   new session. For each plugin `<plugin>` the catalog lists, under the catalog's `name`
   `<market>` (`<tool>@<tool>` for a family tool):
   - `claude plugin list --json`: the entries whose `id` is `<plugin>@<market>`. None: the plugin
     isn't installed on this machine, do nothing.
   - Once, after the push of step 4 (a GitHub marketplace reclones from GitHub, so it would
     still see the old commit before): `claude plugin marketplace update <market>`.
   - Then `claude plugin update <plugin>@<market> --scope <scope>` for each scope found, and only
     those: `user` from anywhere; `project` and `local` from the main tree when the entry's
     `projectPath` is this repo (`cd <projectPath> && …`). An entry of another repo's
     `projectPath` is that repo's business: leave it.
   - Tell the user to restart Claude Code: a session loads its plugins only at launch, so the new
     skill shows only in the next one.
   A plugin read from a local folder (`readFromFolder`, ion-repo on antoine's machine) gets the same
   commands: harmless when its version hasn't moved.
7. No CI to wait for: it runs only on the release branch, before `main` (`/repo:release`).
   Report in the `repo` plugin's `debrief` format (`output-styles/debrief.md`). Suggest `/clear`
   under its **◆ Your turn**, in one line, only when
   it saves something: a long session, or the user moving to an unrelated subject (every
   message re-reads the whole conversation; the work is in git and in the backlog). After a
   short session, or when the next task continues the same subject (a fresh session would
   reread the same files), say nothing about it.

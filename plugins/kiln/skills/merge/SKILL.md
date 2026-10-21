---
name: merge
description: Finish a piece of work - the repo's checks on the branch, merge into the integration branch (develop), push, read GitHub's verdict on the merge, delete the branch (and its worktree). The full CI replayed on the machine only runs when a release goes out (/kiln:release).
argument-hint: "[branch]"
---

Branch: `$ARGUMENTS`, otherwise the current branch. Integration branch: the one the project's
`CLAUDE.md` names, otherwise `develop` if it exists, otherwise `origin`'s default branch.

The merge happens here, directly: no pull request nor approval to wait for ([NO-COMMIT-ON-MAIN]).
A pull request already open for the branch turns "Merged" on GitHub by itself at the push of
step 4. Talk to the user in their language.

1. On the branch: everything is committed (`git status --porcelain` empty), otherwise stop and
   say so. Then review the branch (`/kiln:review <branch>`): after the push of step 4, its
   commits are public for good. What the review tidies on the branch happens before the merge;
   what it leaves to the user, tell them and wait for their decision.
   Then the repo's checks, in the branch's worktree: `kiln check` in a repo kiln generated or
   adopted, otherwise the commands its `CLAUDE.md` gives (kiln itself: `uv run ruff check`,
   `uv run ruff format --check`, `uv run mypy src tests`). Lint, types and charter only: never a
   full test suite at a merge (no `kiln check --tests`, no `kiln ci`), the release runs them all;
   at most the tests of the files the branch touched. Commits made without checks during a long
   series are fine; the merge is where these run. A failure: fix it on the branch, never merge
   red.
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
   Then `git worktree remove .claude/worktrees/<name>` (never `--force`), `git branch -d
   <branch>` (never `-D`) and, if it exists on GitHub (`git ls-remote --heads origin <branch>`),
   `git push origin --delete <branch>`. If a check fails: delete nothing, say which one and why.
6. The CI's verdict on the merge commit, where the repo runs it:
   - on the machine (`git config statusline.ci` says `locale`, answer `ci_runner: local`: a
     private repo spends no GitHub minute): `kiln ci <merge sha>`, which replays `ci.yml` and
     pushes its verdict as a git note, read by the status line and the session start;
   - on GitHub otherwise, when `gh` is there: `gh run list --commit <merge sha>` then
     `gh run watch <id> --exit-status --compact`.
   Red: say so and fix it right away, on a new branch, before any other work (a red integration
   branch hides the next failure; the session start reports it too). Red with no step run
   (`gh run view <id> --json jobs`: every job has empty `steps`) is GitHub refusing to start the
   jobs (billing, spending limit): nothing to fix in the code; say so, and replay it with `kiln ci`.
7. Sum up: merge commit, files touched, checks and GitHub's verdict.

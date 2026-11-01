---
name: release
description: Ships a release: release/vN branch, full checks, announcement, main tagged, deployment, back into develop. Use to release, ship, deploy a version, or for an urgent production fix.
argument-hint: "[vN] [develop commit]"
---

Only a release reaches production: `develop` integrates without full CI (`/repo:merge`), the release runs every check. Git Flow: `release/vN` from `develop` takes only fixes, merges into `main` (tag `vN`) and back into `develop`. Urgent production fix: same path from `main`'s latest tag, on `hotfix/vN.M`.

Read first the project's `CLAUDE.md` (`[RELEASES]` or "Releases"): announcement (what's-new, email), deployment commands, extra checks. Stop if no production `main`. Talk in the user's language. Never switch the main tree's branch: each in `.claude/worktrees/<name>` (`release-vN`, `main`).

## ion-repo's own repo
No production: the tag publishes. These replace the steps below.
1. `ion repo version`: candidates, proposed number, plan tickets still open.
2. `ion repo version cut` (`--minor` for a milestone decided by its owner): branch `release/vX.Y.Z` in `.claude/worktrees/release-vX.Y.Z`, `CHANGELOG.md` drafted, numbers bumped. Rewrite the entry for users (breaking first, each with its conversion by `ion repo update`; keep `- **After updating**: …` lines, which become backlog tickets), delete the draft line, commit; `ion repo version cut` again: full checks, tag `-rc.N` pushed. Candidate fix: `fix:` commit, `cut` again.
3. `ion repo version promote` when `ion repo version` says ready (`--urgent` only if its owner asks: no soak nor repo, green CI still required): tag on its exact commit, merged into `main` and `develop`; `pypi.yml` publishes package and GitHub Release.
4. `ion repo update --all` only with the user's yes.

## 1. Choose
- `git fetch origin --tags`. Previous: `git describe --tags --abbrev=0 origin/main`.
- Candidate: argument, else `origin/develop`. Urgent fix: latest tag plus only the fix's commits (`git cherry-pick`).
- Number: argument, else project's `CLAUDE.md` (ion-repo: next patch, breaking included, minor only for an owner-decided milestone; `ion repo version` proposes), else `vN+1` with `feat`, `vN.M+1` with only fixes.
- Changes: `git log --first-parent --format='%h %s' <previous>..<candidate>`. Work left out: take an older candidate, don't undo code on the release.
- `/repo:review --repo`. The release note says clearly what a poor subject hides.

## 2. Cut
`git worktree add .claude/worktrees/release-vN -b release/vN <candidate>`, `git push -u origin release/vN`. Then only `fix:` commits, never a feature.

## 3. Risks since previous release
- **Migrations** (`*/migrations/`): schema, data, reversible? Deployment applies after backup; flag irreversible.
- **Settings**: new env variables (`config(`, `runtimeConfig`, `.env.example`); check they exist in production before deploying.
- **API contract**: routes or fields removed or renamed in `openapi.json`; a cached front calls the old one. Deploy API, then front.
- **Flags**: features shipped off, planned production state.
- **Dependencies** added or major-bumped.

## 4. Announcement
Per `CLAUDE.md`. Check it exists for `vN`, describes the risks found, promises neither work left out nor a feature behind a flag staying off. Otherwise write it on the release and **have the user approve the text**.

## 5. Full checks
`ion repo ci release/vN` (or GitHub CI on the branch): every job. Failure: fix on the release, commit, rerun until green. Report jobs not replayed.

## 6. Go-ahead
Show briefly: number, changes, risks, announcement, CI verdict, rollback (previous release). Wait for agreement: this is production.

## 7. Merge and tag
```bash
git worktree add .claude/worktrees/main main
git -C .claude/worktrees/main merge --no-ff release/vN -m "Release vN: <summary>"
git -C .claude/worktrees/main tag -a vN -m "Release vN" -m "<changes, one line each>"
git push origin main vN && git worktree remove .claude/worktrees/main
```
`main`'s commit holds the release's files: the deploy script accepts its `ion repo ci` verdict (`green-ci.sh`), no CI replay.

## 8. Deploy
Project's commands (often `scripts/ops/deploy-backend.sh --dry-run`, then without, then `deploy-frontend.sh`; dashboard alone: `deploy-frontend.sh` only), API before front. Then check: script's smoke test, production logs a few minutes (project's diagnosis skill if any), announcement visible. Breakage: back to the previous release via the project's procedure, and say so.
No deployment (no `scripts/ops/deploy-*.sh`, nothing in `CLAUDE.md`): release ends at the tag on `main`; say so, go to step 9.
PyPI command (`.github/workflows/pypi.yml`, `ion repo set pypi_name=…`): pushed tag deploys, version `N` from `vN`. `gh run watch`, then check `https://pypi.org/project/<pypi_name>/N/`; a red run names its step. First tag needs either a `PYPI_TOKEN` secret in the `pypi` environment ("Entire account" to create the project, `/repo:token`), or a publisher on https://pypi.org/manage/account/publishing/ (repository, workflow `pypi.yml`, environment `pypi`). A PyPI version can never be re-uploaded: fix a broken one with the next tag.

## 9. Merge back, tidy
```bash
git merge --no-ff release/vN -m "Merge branch 'release/vN' into develop"   # from develop
git push origin develop
git worktree remove .claude/worktrees/release-vN
git branch -d release/vN && git push origin --delete release/vN
```
Report in the `repo` plugin's `debrief` format (`output-styles/debrief.md`); a failed health probe or smoke test is a `Broken:` line.

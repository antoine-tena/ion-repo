---
name: release
description: Ship a release: a release/vN branch from develop, full checks (CI, migrations, contract, settings), the announcement (what's-new window, email), main merged and tagged vN, deployment, back into develop. Use when the user asks to release, ship or deploy a version, or for an urgent production fix.
argument-hint: "[vN] [develop commit]"
---

A release is the only state that goes to production: `develop` integrates without full CI
(`/repo:merge`), the release runs every check. Git Flow: a `release/vN` branch from `develop`
only takes fixes from then on, then merges into `main` (tag `vN`) and back into `develop`. An
urgent production fix follows the same path from `main`'s latest tag, on `hotfix/vN.M`.

The project's `CLAUDE.md` (a `[RELEASES]` rule or a "Releases" section) says what is specific to
it: how a release is announced (what's-new file, email), the deployment commands, extra checks.
Read it first. Stop if the repo has no production `main`. Talk to the user in their language.

Never switch the branch of the main tree: each branch in `.claude/worktrees/<name>`
(`release-vN`, `main`).

## ion-repo's own repo
No production there: the tag publishes. Two commands replace the steps below.
1. `ion repo version`: the candidates, the number proposed, the tickets of the plan still open.
2. `ion repo version cut` (`--minor` for a milestone decided by its owner): branch
   `release/vX.Y.Z` in `.claude/worktrees/release-vX.Y.Z`, the `CHANGELOG.md` entry drafted from
   the commits, the numbers bumped. Rewrite the entry for users there (breaking changes first,
   each with its conversion by `ion repo update`; keep the `- **After updating**: …` lines, which
   `ion repo update` turns into a ticket of each repo's backlog), delete the draft line, commit; then
   `ion repo version cut` again: full checks, tag `-rc.N` pushed. A fix of the candidate: a `fix:`
   commit on the branch, then `cut` again.
3. `ion repo version promote` when `ion repo version` says a candidate is ready (`--urgent`, only when
   its owner asks: no soak nor repo, its CI green still required): tag on its exact commit,
   merged into `main` and `develop`; `pypi.yml` publishes the package and the GitHub Release.
4. `ion repo update --all` only with the user's yes.

## 1. Choose
- `git fetch origin --tags`. Previous release: `git describe --tags --abbrev=0 origin/main`.
- Candidate commit: the argument, otherwise `origin/develop`. For an urgent fix: the latest tag,
  plus only the fix's commits (`git cherry-pick`).
- Number: the argument, otherwise what the project's `CLAUDE.md` sets (ion-repo itself: the next
  patch, breaking ones included, the minor only for a milestone decided by its owner,
  `ion repo version` proposes it), otherwise `vN+1` when there are features (`feat`), `vN.M+1` when
  there are only fixes.
- Changes: `git log --first-parent --format='%h %s' <previous>..<candidate>`. If the user leaves
  a piece of work out, take an older candidate rather than undoing code on the release.
- Review the repo (`/repo:review --repo`): commits published since the previous release, remote
  branches left on GitHub, tags. The release note says clearly what a poor commit subject hides.

## 2. Cut the release
`git worktree add .claude/worktrees/release-vN -b release/vN <candidate>`, then
`git push -u origin release/vN`. From then on, only fixes enter it (`fix:` commits), never a
feature.

## 3. Risks (between the previous release and this one)
- **Migrations** added (`*/migrations/`): schema, data, reversible or not. The deployment applies
  them after a backup; an irreversible migration is flagged.
- **Settings**: new environment variables (`config(`, `runtimeConfig`, `.env.example`); check
  they exist in production before deploying.
- **API contract**: routes or fields removed or renamed in `openapi.json`; a front still cached
  calls the old contract. Deploy the API first, the front afterwards.
- **Flags**: features shipped off, and their planned state in production.
- **Dependencies** added or moved up a major version.

## 4. Announcement
What the project's `CLAUDE.md` asks to announce a release (what's-new window, email to users…).
Check that it exists for `vN`, that it describes what the risks step found, and that it promises
neither a piece of work left out nor a feature behind a flag that stays off. Otherwise write it
on the release and **have the user approve the text**.

## 5. Full checks
`ion repo ci release/vN` (or GitHub's CI on the branch): every job. On a failure, fix on the release,
commit, run again, until green. Also give the jobs that were not replayed.

## 6. Go-ahead
Show the user, briefly: number, changes, risks, announcement, CI verdict, rollback plan (the
previous release). Wait for their agreement: this is production.

## 7. Merge and tag
```bash
git worktree add .claude/worktrees/main main
git -C .claude/worktrees/main merge --no-ff release/vN -m "Release vN: <summary>"
git -C .claude/worktrees/main tag -a vN -m "Release vN" -m "<changes, one line each>"
git push origin main vN && git worktree remove .claude/worktrees/main
```
The commit of `main` holds the files of the release: the deployment script accepts the `ion repo ci`
verdict of the release (`green-ci.sh`), without replaying CI.

## 8. Deploy
The project's commands (often `scripts/ops/deploy-backend.sh --dry-run`, then without, then
`deploy-frontend.sh`; a dashboard alone, `deploy-frontend.sh` only), the API before the front. Then check: the script's smoke test, production
logs for a few minutes (the project's diagnosis skill if any), the announcement visible. If
something breaks: back to the previous release through the project's procedure, and say so.
No deployment configured (no `scripts/ops/deploy-*.sh`, nothing in `CLAUDE.md`): the release ends
at the tag on `main`; say so and skip to the next step.
A command published on PyPI (`.github/workflows/pypi.yml`, `ion repo set pypi_name=…`): the pushed
tag is the deployment, version `N` taken from `vN`. Follow the run (`gh run watch`), then check
`https://pypi.org/project/<pypi_name>/N/`; a red run names its failing step. The first tag needs
either a PyPI token in the secret `PYPI_TOKEN` of the `pypi` environment ("Entire account" to
create the project, `/repo:token`), or the publisher declared on PyPI
(https://pypi.org/manage/account/publishing/: repository, workflow `pypi.yml`, environment
`pypi`); a version on PyPI can never be uploaded again, so a broken one is fixed by the next tag.

## 9. Merge back and tidy
```bash
git merge --no-ff release/vN -m "Merge branch 'release/vN' into develop"   # from develop
git push origin develop
git worktree remove .claude/worktrees/release-vN
git branch -d release/vN && git push origin --delete release/vN
```
Report in the `repo` plugin's `debrief` format (`output-styles/debrief.md`); a failed health
probe or smoke test is a `Broken:` line.

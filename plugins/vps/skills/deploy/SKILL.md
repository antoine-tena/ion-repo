---
name: deploy
description: Deploy the project to production with the repo's scripts (scripts/ops/), after checking that CI on the integration branch is green.
disable-model-invocation: true
argument-hint: "[back|front|all] [rebuild]"
---

In a repo not yet updated to ion-repo, these variables are still named `KILN_…` (`KILN_VPS` for `ION_REPO_VPS`): use the one that is set.
Requested deployment: `$ARGUMENTS` (default: backend, then frontend).
Repo settings: !`env | grep -E '^(KILN|PROJET)_(PROJECT|NOM|VPS|SITE|API_HEALTH|API_SANTE|PROD_DOC|DOC_PROD)' | sort`
(Repos generated before kiln 0.4 use the French names: `PROJET_NOM`, `PROJET_VPS`,
`PROJET_API_SANTE`, `PROJET_DOC_PROD`.)
Available scripts: !`ls scripts/ops/ 2>/dev/null | tr '\n' ' '`

**Project specifics** (options, pitfalls, extra steps): the "Specifics" section of the
production document (`$ION_REPO_PROD_DOC`, by default `docs/operations/production.md`), to read in
full before starting; it takes precedence over what follows.

1. The integration branch is pushed and CI on its last commit is green: verdict of `ion repo ci`
   (`ion repo ci --status <integration>`, for a repo whose GitHub CI does not run) or GitHub CI
   (`gh run list -b <integration> -L 3`). Never run: start `ion repo ci <integration>` (about twenty
   minutes) and wait for its verdict. Red: show the failing job and stop.
2. **Backend**: `scripts/ops/deploy-backend.sh`. Deployments **migrate** and keep the data; a
   database rebuild only if the `rebuild` argument is given. Then `scripts/ops/smoke-test.sh`
   (or `smoke.sh`) if it exists.
3. **Frontend**: `scripts/ops/deploy-frontend.sh`, with no untracked file in the frontend directory.
   A Streamlit or Dash front without an API deploys only this way, to the VPS (its image, no
   database), and runs the smoke test itself.
4. Check the health probe (`curl -s -o /dev/null -w '%{http_code}' $ION_REPO_API_HEALTH`) and
   the smoke test, then report in the `repo` plugin's `debrief` format
   (`output-styles/debrief.md`): a failure is a `Broken:` line, and `/vps:prod-logs` the first
   step under **◆ Next**.

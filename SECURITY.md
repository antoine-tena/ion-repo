# Security policy

ion-repo generates CI, deployment scripts and server configuration, so security reports matter.

**Please do not open a public issue for a vulnerability.** Report it privately through
[GitHub's private vulnerability reporting](https://github.com/antoine-tena/ion-repo/security/advisories/new).
You will get an answer within a few days.

Only the latest release (`main`, newest `vN` tag) receives security fixes.

## Verifying a release

Each package of a release, on PyPI and attached to its
[GitHub Release](https://github.com/antoine-tena/ion-repo/releases), carries a build provenance
attestation signed through Sigstore: it proves the file was built by ion-repo's `pypi.yml` workflow
from the tagged commit.

```bash
gh attestation verify kiln_cli-0.4.11-py3-none-any.whl --repo antoine-tena/ion-repo
```

ion-repo's own workflows, which run in other people's repos, pass [zizmor](https://docs.zizmor.sh)
before every release, and the [OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/antoine-tena/ion-repo)
grades the repo every week.

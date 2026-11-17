# ion-repo#T-267 · Deploys you can undo: health probes, config that fails fast, OIDC, graceful shutdown
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Operations), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.40, "Deploys you can undo": Services and hosts read from every deploy config; health
probes that exist, config that fails fast, OIDC instead of keys, rollbacks, certificates renewed.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **OP01** `HEALTH-PROBES` (scored): beyond a `HEALTHCHECK` line: the endpoint exists in the
  code, liveness and readiness told apart, compose and Kubernetes probes read.
- [ ] **OP04** `REVERSIBLE-DEPLOYMENT` (draft): images deployed by immutable tag or digest, a
  rollback script or workflow present. L1≈ · fix J · trial.
- [ ] **OP07** `ENV-EXAMPLE-COMPLETE`: every variable the code reads (`os.environ`, `env()`,
  `process.env`, `useRuntimeConfig`) is in `.env.example`, and none there is stale. L3 · fix S ·
  adopt.
- [ ] **OP08** `FAIL-FAST-CONFIG`: a missing required setting stops the start (no silent default for
  `SECRET_KEY` or `DATABASE_URL`): what `DJANGO-SECRET-KEY` and `DJANGO-ALLOWED-HOSTS` ask of
  Django, for every stack. L2 · fix J · adopt.
- [ ] **OP09** `DEPLOY-FROM-CI`: production deployed by a workflow from a commit, not from a laptop.
  L1 · fix J · trial.
- [ ] **OP11** `OIDC-TO-CLOUD`: cloud credentials through OIDC federation (`id-token: write`), no
  long-lived keys in secrets. L1 · fix J · adopt.
- [ ] **OP12** `ENCRYPTED-SECRETS`: secrets committed only encrypted (sops with age, git-crypt,
  Ansible Vault). L1 · fix J · trial.
- [ ] **OP14** `GRACEFUL-SHUTDOWN`: SIGTERM handled, a stop grace period longer than the longest
  request or task. L2 · fix S · trial.
- [ ] **OP15** `UTC-SERVERS`: containers and servers run in UTC, no `TZ` set to a local zone (with
  `TIME-ZONE`). L1 · fix S · trial.
- [ ] **OP20** `AUTOMATIC-TLS`: certificates renewed by themselves (Caddy, cert-manager, the
  platform's). L1 · fix S · adopt.

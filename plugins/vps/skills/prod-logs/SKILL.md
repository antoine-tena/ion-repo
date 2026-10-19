---
name: prod-logs
description: Diagnose production on the VPS - container state, targeted logs, API health, system. Read-only. Use when the site or the API misbehaves.
argument-hint: "[symptom or service]"
---

Symptom: `$ARGUMENTS`.
Repo settings: !`env | grep -E '^(KILN|PROJET)_(PROJECT|NOM|VPS|SITE|API_HEALTH|API_SANTE)' | sort`
(Repos generated before kiln 0.4: `PROJET_NOM`, `PROJET_VPS`, `PROJET_SITE`, `PROJET_API_SANTE`.)

**Read-only**: no `restart`, `rm`, `up`, no write on the server; never print a secret (`.env`,
`printenv`). Suggest corrective actions without performing them.

1. Public health: `curl -s -o /dev/null -w '%{http_code}' $KILN_API_HEALTH` and
   `curl -sI $KILN_SITE | head -5` (503 `DEPLOYMENT_PAUSED` → Vercel paused).
2. Containers: `ssh $KILN_VPS "podman ps -a --format '{{.Names}} {{.Status}}'"`. A container
   missing or `Exited` after a server reboot: check `systemctl is-enabled podman-restart` and the
   `always` policy.
3. Targeted logs of the `$KILN_PROJECT-*` containers related to the symptom:
   `ssh $KILN_VPS 'podman logs --since 2h <container> 2>&1 | grep -iE "error|exception|traceback|5[0-9]{2}" | tail -50'`.
   Proxy: `ssh $KILN_VPS 'journalctl -u caddy --since "2 hours ago" | tail -50'`.
4. System: `ssh $KILN_VPS 'df -h / ; free -m ; uptime ; systemctl --failed'`.
5. Conclude: probable cause, evidence (log lines without personal data), proposed fix;
   `scripts/ops/smoke-test.sh` to confirm after the fix.

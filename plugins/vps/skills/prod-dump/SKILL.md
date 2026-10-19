---
name: prod-dump
description: Restore a copy of the production database into a throwaway local PostgreSQL, to test a migration, a query or a script on real data without touching production.
disable-model-invocation: true
argument-hint: "[backup name, latest by default]"
---

Repo settings: !`env | grep -E '^(KILN|PROJET)_(PROJECT|NOM|VPS|PG_)' | sort`
(Repos generated before kiln 0.4: `PROJET_NOM`, `PROJET_VPS`, `PROJET_VPS_SAUVEGARDES`,
`PROJET_PG_UTILISATEUR`, `PROJET_PG_BASE` stand for the `KILN_*` names below.)
Backups: on `$KILN_VPS`, directory `$KILN_VPS_BACKUPS`, `.dump` files. Never write on the server.

1. List: `ssh $KILN_VPS "ls -t $KILN_VPS_BACKUPS/*.dump | head -5"`; take `$ARGUMENTS` or the
   latest.
2. Fetch it into the session scratchpad (never into the repo: personal data):
   `scp $KILN_VPS:$KILN_VPS_BACKUPS/<file> <scratchpad>/`.
3. Throwaway database, separate from the test database (port 55433, not the test port):
   `podman run -d --rm --name $KILN_PROJECT-prod-copy -e POSTGRES_USER=$KILN_PG_USER -e POSTGRES_PASSWORD=copy -e POSTGRES_DB=$KILN_PG_DATABASE -p 127.0.0.1:55433:5432 ${KILN_PG_IMAGE:-postgres:18}`
   then wait for `pg_isready`, and
   `podman exec -i $KILN_PROJECT-prod-copy pg_restore -U $KILN_PG_USER -d $KILN_PG_DATABASE --no-owner --no-acl < <file>`.
4. `DATABASE_URL=postgres://$KILN_PG_USER:copy@localhost:55433/$KILN_PG_DATABASE` for the
   backend commands (migration, queries, `check`).
5. At the end: `podman stop $KILN_PROJECT-prod-copy` (`--rm` container, it disappears) and delete
   the dump from the scratchpad. Never copy data from this database into a commit, a log or an
   answer (names, emails).

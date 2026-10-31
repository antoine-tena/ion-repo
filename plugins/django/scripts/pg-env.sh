# Settings of the local test database, sourced by the postgres MCP server and the
# postgres-read skill. Reads the ION_REPO_* variables of .claude/settings.json (env), their KILN_*
# names of before ion-repo, and the PROJET_* names of repos generated before kiln 0.4.
ION_REPO_PROJECT="${ION_REPO_PROJECT:-${KILN_PROJECT:-${PROJET_NOM:-project}}}"
ION_REPO_PG_CONTAINER="${ION_REPO_PG_CONTAINER:-${KILN_PG_CONTAINER:-${PROJET_PG_CONTENEUR:-$ION_REPO_PROJECT-test-pg}}}"
ION_REPO_PG_PORT="${ION_REPO_PG_PORT:-${KILN_PG_PORT:-${PROJET_PG_PORT:-55432}}}"
ION_REPO_PG_USER="${ION_REPO_PG_USER:-${KILN_PG_USER:-${PROJET_PG_UTILISATEUR:-$ION_REPO_PROJECT}}}"
ION_REPO_PG_DATABASE="${ION_REPO_PG_DATABASE:-${KILN_PG_DATABASE:-${PROJET_PG_BASE:-$ION_REPO_PROJECT}}}"
# Read-only role of the MCP server; repos before 0.4 created it as <name>_mcp_lecture.
ION_REPO_PG_READ_ROLE="${ION_REPO_PG_READ_ROLE:-${KILN_PG_READ_ROLE:-}}"
if [ -z "$ION_REPO_PG_READ_ROLE" ]; then
  if [ -n "${PROJET_NOM:-}" ]; then
    ION_REPO_PG_READ_ROLE="${PROJET_NOM}_mcp_lecture"
  else
    ION_REPO_PG_READ_ROLE="$(printf '%s' "$ION_REPO_PROJECT" | tr '-' '_')_mcp_read"
  fi
fi

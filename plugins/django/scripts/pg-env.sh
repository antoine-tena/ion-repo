# Settings of the local test database, sourced by the postgres MCP server and the
# postgres-read skill. Reads the KILN_* variables of .claude/settings.json (env), and the
# PROJET_* names of repos generated before kiln 0.4.
KILN_PROJECT="${KILN_PROJECT:-${PROJET_NOM:-project}}"
KILN_PG_CONTAINER="${KILN_PG_CONTAINER:-${PROJET_PG_CONTENEUR:-$KILN_PROJECT-test-pg}}"
KILN_PG_PORT="${KILN_PG_PORT:-${PROJET_PG_PORT:-55432}}"
KILN_PG_USER="${KILN_PG_USER:-${PROJET_PG_UTILISATEUR:-$KILN_PROJECT}}"
KILN_PG_DATABASE="${KILN_PG_DATABASE:-${PROJET_PG_BASE:-$KILN_PROJECT}}"
# Read-only role of the MCP server; repos before 0.4 created it as <name>_mcp_lecture.
if [ -z "${KILN_PG_READ_ROLE:-}" ]; then
  if [ -n "${PROJET_NOM:-}" ]; then
    KILN_PG_READ_ROLE="${PROJET_NOM}_mcp_lecture"
  else
    KILN_PG_READ_ROLE="$(printf '%s' "$KILN_PROJECT" | tr '-' '_')_mcp_read"
  fi
fi

#!/usr/bin/env bash
# Creates (or repairs) the read-only role of the postgres MCP server in the test container.
# Read-only is enforced by the database, not by the tool: pg_read_all_data, no write right,
# read-only transactions by default.
set -euo pipefail
. "${CLAUDE_PLUGIN_ROOT:-$(dirname "$0")/../..}/scripts/pg-env.sh"
role="$KILN_PG_READ_ROLE"
podman exec -i "$KILN_PG_CONTAINER" psql -v ON_ERROR_STOP=1 -U "$KILN_PG_USER" -d postgres <<SQL
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '$role') THEN
    CREATE ROLE $role LOGIN PASSWORD '$role';
  END IF;
END
\$\$;
ALTER ROLE $role NOSUPERUSER NOCREATEDB NOCREATEROLE;
ALTER ROLE $role SET default_transaction_read_only = on;
GRANT pg_read_all_data, pg_monitor TO $role;
SQL
echo "postgres_mcp_role_ready container=$KILN_PG_CONTAINER role=$role"

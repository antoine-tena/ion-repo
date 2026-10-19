#!/bin/sh
# Starts the postgres MCP server, read-only by the rights of its role, on the local test
# database described by scripts/pg-env.sh.
. "$(dirname "$0")/pg-env.sh"
export POSTGRES_HOST=127.0.0.1
export POSTGRES_PORT="$KILN_PG_PORT"
export POSTGRES_DATABASE="$KILN_PG_DATABASE"
export POSTGRES_USER="$KILN_PG_READ_ROLE"
export POSTGRES_PASSWORD="$KILN_PG_READ_ROLE"
exec npx -y @toolbox-sdk/server@1.13.1 --prebuilt postgres --stdio "$@"

#!/bin/sh
# Starts the postgres MCP server, read-only by the rights of its role, on the local test
# database described by scripts/pg-env.sh.
. "$(dirname "$0")/pg-env.sh"
export POSTGRES_HOST=127.0.0.1
export POSTGRES_PORT="$ION_REPO_PG_PORT"
export POSTGRES_DATABASE="$ION_REPO_PG_DATABASE"
export POSTGRES_USER="$ION_REPO_PG_READ_ROLE"
export POSTGRES_PASSWORD="$ION_REPO_PG_READ_ROLE"
exec npx -y @toolbox-sdk/server@1.13.1 --prebuilt postgres --stdio "$@"

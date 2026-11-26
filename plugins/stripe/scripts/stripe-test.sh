#!/usr/bin/env bash
# Stripe MCP server of the current repo, in test mode only: any live key is refused, so the
# agent never touches real payments. Key: STRIPE_MCP_TEST_KEY, otherwise .stripe/token at the
# root of the main tree, otherwise Bitwarden through the machine's `secrets get .stripe/token`
# (restricted rk_test_… key created on the dashboard).
set -euo pipefail
key="${STRIPE_MCP_TEST_KEY:-}"
root="$(cd "$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)/.." 2>/dev/null && pwd || pwd)"
if [[ -z "$key" && -s "$root/.stripe/token" ]]; then
  key="$(tr -d '[:space:]' < "$root/.stripe/token")"
elif [[ -z "$key" ]] && command -v secrets >/dev/null; then
  key="$(cd "$root" && secrets get .stripe/token 2>/dev/null | tr -d '[:space:]' || true)"
fi
if [[ -z "$key" ]]; then
  echo "stripe_mcp: neither STRIPE_MCP_TEST_KEY nor .stripe/token nor Bitwarden (rk_test_… key expected)" >&2
  exit 1
fi
if [[ "$key" != rk_test_* && "$key" != sk_test_* ]]; then
  echo "stripe_mcp: key refused, only test mode is allowed" >&2
  exit 1
fi
STRIPE_SECRET_KEY="$key" exec npx -y @stripe/mcp@0.3.3

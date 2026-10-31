#!/usr/bin/env bash
# Prepares a new worktree: copies the local files ignored by git (.env, .env.local…) from the
# main tree, then installs the JavaScript dependencies of each lockfile.
# Python dependencies are not installed: `uv run` creates the venv on demand.
# A repo that needs more adds .claude/worktree-setup.sh, run afterwards by /kiln:worktree.
set -euo pipefail
worktree="$(cd "$1" && pwd)"
main_tree="$(dirname "$(git -C "$worktree" rev-parse --path-format=absolute --git-common-dir)")"

# Ignored .env* files of the main tree (except examples and node_modules), same relative path.
git -C "$main_tree" ls-files --others --ignored --exclude-standard -- '*.env' '*.env.*' '.env' '.env.*' \
  | { grep -vE '(^|/)node_modules/|\.(example|sample)$|^\.claude/worktrees/' || true; } \
  | while read -r f; do
      mkdir -p "$worktree/$(dirname "$f")"
      cp -p "$main_tree/$f" "$worktree/$f"
      echo "copied: $f"
    done

# Never a symlinked node_modules: it breaks tools that resolve their root.
git -C "$worktree" ls-files -- '*pnpm-lock.yaml' '*package-lock.json' | while read -r lock; do
  dir="$worktree/$(dirname "$lock")"
  case "$lock" in
    *pnpm-lock.yaml) (cd "$dir" && pnpm install --frozen-lockfile --prefer-offline --config.strict-dep-builds=false) ;;
    *package-lock.json) (cd "$dir" && npm ci --prefer-offline) ;;
  esac
done
echo "worktree ready: $worktree"

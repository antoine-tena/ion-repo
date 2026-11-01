# shellcheck shell=bash
# Refuses to deploy a commit whose CI is not green: a commit with failing tests could reach
# production. Two verdicts count, the first green one is enough:
# - that of `ion repo ci <sha>`, the CI of ci.yml replayed on a workstation (git note refs/notes/ci,
#   pushed to origin): the only verdict of a repo whose GitHub CI does not run;
# - that of the GitHub CI (workflow CI_WORKFLOW).
# The release commit of `main` (--no-ff merge of `release/vX.Y.Z`, skill /repo:release) holds exactly
# the files of the release: the green verdict of the release counts for it.
# SKIP_CI=1 overrides it, in an emergency.
#
# Usage: . scripts/ops/lib/green-ci.sh ; ci_is_green <sha>
# Settings: CI_WORKFLOW (default ci.yml), SKIP_CI=1
ci_is_green() {
  local sha="$1" note runs conclusion release
  if [ "${SKIP_CI:-${SAUTER_CI:-0}}" = 1 ]; then
    echo "WARNING: CI check skipped (SKIP_CI=1)." >&2
    return 0
  fi
  note="$(kiln_ci_verdict "$sha")"
  if ! is_success "$note" && release="$(same_release "$sha")"; then
    note="$(kiln_ci_verdict "$release")"
    is_success "$note" && echo "Release merge: same files as release ${release:0:8}."
  fi
  if is_success "$note"; then
    echo "CI replayed by ion repo ci, green for ${sha:0:8}:"
    sed -n '2,$s/^/  /p' <<< "$note"
    return 0
  fi
  if command -v gh > /dev/null; then
    runs="$(gh run list --commit "$sha" --workflow "${CI_WORKFLOW:-ci.yml}" --json status,conclusion --limit 1 2> /dev/null || echo '[]')"
    conclusion="$(python3 -c '
import json, sys
runs = json.load(sys.stdin)
print((runs[0]["conclusion"] or runs[0]["status"]) if runs else "no run")
' <<< "$runs")"
  else
    conclusion="gh missing"
  fi
  if [ "$conclusion" = success ]; then
    echo "GitHub CI green for ${sha:0:8}."
    return 0
  fi
  echo "CI of ${sha:0:8}: GitHub \"$conclusion\", ion repo ci \"${note%%$'\n'*}\"." >&2
  [ -n "$note" ] && sed -n '2,$s/^/  /p' <<< "$note" >&2
  echo "Run \`ion repo ci ${sha:0:12}\` (the CI replayed on this machine), or SKIP_CI=1 in an emergency." >&2
  return 1
}

# First line of a successful ion repo ci note (its French wording before kiln 0.4.0 included).
is_success() {
  local first="${1%%$'\n'*}"
  [ "$first" = "kiln ci: success" ] || [ "$first" = "kiln ci : succès" ]
}

# ion repo ci's note on the commit: origin's when it says success, else the local one, else
# "never replayed".
kiln_ci_verdict() {
  local sha="$1" ref note
  git fetch -q origin "+refs/notes/ci:refs/notes/ci-origin" 2> /dev/null || true
  for ref in ci-origin ci; do
    note="$(git notes --ref="$ref" show "$sha" 2> /dev/null || true)"
    if is_success "$note"; then
      printf '%s\n' "$note"
      return 0
    fi
  done
  note="$(git notes --ref=ci show "$sha" 2> /dev/null || git notes --ref=ci-origin show "$sha" 2> /dev/null || echo "never replayed")"
  printf '%s\n' "$note"
}

# Second parent of a merge commit that brings nothing but it (same tree); fails otherwise. That is
# the merge of a release into `main`.
same_release() {
  local sha="$1" parent
  parent="$(git rev-parse -q --verify "$sha^2" 2> /dev/null)" || return 1
  [ "$(git rev-parse "$sha^{tree}")" = "$(git rev-parse "$parent^{tree}")" ] || return 1
  printf '%s\n' "$parent"
}

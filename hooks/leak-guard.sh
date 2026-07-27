#!/bin/bash
# leak-guard.sh — machinery-only tripwire for this PUBLIC repo.
#
# Blocks commits/pushes whose content, file names, or messages match a PRIVATE
# term list that never lives in this repo. The list location comes from
# `git config leakguard.file` (preferred) or ~/.config/leak-terms.txt.
# List format: one term per line; '#' comments and blanks ignored; terms are
# matched case-insensitively with word boundaries (regex-escaped literals).
#
# Modes:
#   leak-guard.sh staged        — scan staged diff + staged file names (pre-commit)
#   leak-guard.sh msg <file>    — scan a commit-message file (commit-msg)
#   leak-guard.sh push          — scan each ref range from pre-push stdin
#
# Bypass (rare, deliberate): LEAK_GUARD_SKIP=1 git commit ...  (or --no-verify)
set -uo pipefail

[ "${LEAK_GUARD_SKIP:-0}" = "1" ] && exit 0

list_file="$(git config leakguard.file 2>/dev/null || true)"
[ -z "$list_file" ] && list_file="$HOME/.config/leak-terms.txt"

if [ ! -r "$list_file" ]; then
  echo "leak-guard: WARNING — private term list not found ($list_file)." >&2
  echo "leak-guard: content scan SKIPPED locally; the CI leak-guard is the backstop." >&2
  exit 0
fi

# Build one word-boundary alternation from the list, escaping regex specials.
pattern="$(grep -v '^\s*#' "$list_file" | grep -v '^\s*$' \
  | sed -e 's/[][\.|$(){}?+*^\/]/\\&/g' | paste -sd'|' -)"
[ -z "$pattern" ] && exit 0
rx="\\b(${pattern})\\b"

fail() {
  echo "" >&2
  echo "leak-guard: BLOCKED — creative-project content matched in $1." >&2
  echo "This repo is machinery-only. Remove the flagged content (shown above)," >&2
  echo "or move it to the private workspace. Deliberate bypass: LEAK_GUARD_SKIP=1" >&2
  exit 1
}

scan() { # scan <label> ; input on stdin; prints matches, returns 1 on hit
  local label="$1" hits
  hits="$(grep -i -n -E "$rx" - || true)"
  if [ -n "$hits" ]; then
    echo "── leak-guard matches in ${label}: ─────────────" >&2
    echo "$hits" | head -25 >&2
    return 1
  fi
  return 0
}

case "${1:-staged}" in
  staged)
    ok=0
    git diff --cached -U0 --no-color | grep -E '^(\+|Binary)' | scan "staged changes" || ok=1
    git diff --cached --name-only | scan "staged file names" || ok=1
    [ "$ok" = "1" ] && fail "the staged commit"
    ;;
  msg)
    scan "commit message" < "$2" || fail "the commit message"
    ;;
  push)
    empty_tree="$(git hash-object -t tree /dev/null)"
    ok=0
    while read -r _local_ref local_sha _remote_ref remote_sha; do
      [ -z "${local_sha:-}" ] && continue
      # deleted ref
      [ "$local_sha" = "0000000000000000000000000000000000000000" ] && continue
      base="$remote_sha"
      [ "$remote_sha" = "0000000000000000000000000000000000000000" ] && base="$empty_tree"
      git diff "$base" "$local_sha" -U0 --no-color 2>/dev/null | grep -E '^(\+|Binary|diff --git)' | scan "pushed diff ($local_sha)" || ok=1
      git log --format=%B "$base..$local_sha" 2>/dev/null | scan "pushed commit messages" || ok=1
    done
    [ "$ok" = "1" ] && fail "the push"
    ;;
  *)
    echo "leak-guard: unknown mode '$1'" >&2; exit 2 ;;
esac
exit 0

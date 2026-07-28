#!/usr/bin/env bash
# Audit one or more HTML artifacts before they're added to documents/.
#
# Usage: ./audit_html.sh documents/some-artifact.html [more.html ...]
#
# Prints three sections per file:
#   1. FAIL  - target="_blank" links missing rel="noopener noreferrer" (auto-fixable, must fix)
#   2. REVIEW - external <script>/<link> src/href (judgment call, flag to the user)
#   3. REVIEW - fetch()/XHR/.ajax( calls with a literal URL argument (judgment call, flag to the user)
#
# Exits non-zero if any FAIL is found. REVIEW items don't fail the script —
# they need a human/agent judgment call (see references/html-artifact-format.md
# for how to tell a real dependency from a harmless minified-library match).

set -uo pipefail

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 <file.html> [more.html ...]" >&2
  exit 2
fi

exit_code=0

for f in "$@"; do
  echo "=== $f ==="

  missing_rel=$(grep -oE '<a [^>]*target="_blank"[^>]*>' "$f" 2>/dev/null | grep -v 'rel="noopener')
  if [ -n "$missing_rel" ]; then
    echo "FAIL: target=\"_blank\" without rel=\"noopener noreferrer\":"
    echo "$missing_rel" | sed 's/^/  /'
    exit_code=1
  fi

  external_assets=$(grep -oE '<(script|link)[^>]*(src|href)="https?://[^"]*"' "$f" 2>/dev/null)
  if [ -n "$external_assets" ]; then
    echo "REVIEW: external script/link dependency found (should be inlined instead):"
    echo "$external_assets" | sed 's/^/  /'
  fi

  fetch_calls=$(grep -noE "fetch\(['\"][^'\"]+['\"]|XMLHttpRequest\(\)|\.ajax\(\{" "$f" 2>/dev/null)
  if [ -n "$fetch_calls" ]; then
    echo "REVIEW: fetch/XHR call with a literal argument found (may expect a live backend):"
    echo "$fetch_calls" | sed 's/^/  /'
  fi

  if [ -z "$missing_rel" ] && [ -z "$external_assets" ] && [ -z "$fetch_calls" ]; then
    echo "OK: no issues found"
  fi

  echo
done

exit $exit_code

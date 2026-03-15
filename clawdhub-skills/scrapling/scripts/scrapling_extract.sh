#!/usr/bin/env bash
set -euo pipefail

# Lightweight wrapper around Scrapling's CLI.
# Uses the dedicated venv at ~/.venvs/scrapling (created once on this machine).
#
# Examples:
#   ./scrapling_extract.sh https://example.com out.html
#   ./scrapling_extract.sh https://example.com out.md 'h1'
#   ./scrapling_extract.sh https://example.com out.txt 'p'

URL="${1:?URL required}"
OUT="${2:?Output file required (.html|.md|.txt)}"
SELECTOR="${3:-}"

VENV_PY="$HOME/.venvs/scrapling/bin/python"
VENV_CLI="$HOME/.venvs/scrapling/bin/scrapling"

if [[ ! -x "$VENV_CLI" ]]; then
  echo "Scrapling CLI not found at $VENV_CLI" >&2
  echo "Create venv + install: python3 -m venv ~/.venvs/scrapling && ~/.venvs/scrapling/bin/pip install -U scrapling" >&2
  exit 2
fi

if [[ -n "$SELECTOR" ]]; then
  "$VENV_CLI" extract get "$URL" "$OUT" -s "$SELECTOR"
else
  "$VENV_CLI" extract get "$URL" "$OUT"
fi

echo "[ok] wrote $OUT"
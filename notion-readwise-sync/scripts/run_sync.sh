#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="$(command -v python3)"
VAULT="${NOTION_READWISE_VAULT:-/home/rlmit/Obsidian}"
PAGE_ID="${NOTION_READWISE_PAGE_ID:-4c43c451-fdfc-4066-871b-310cbf477fdf}"
DB_TITLE="${NOTION_READWISE_DB_TITLE:-Library}"
LIMIT="${NOTION_READWISE_LIMIT:-50}"
SINCE_DAYS="${NOTION_READWISE_SINCE_DAYS:-0}"
ENABLED_ONT="${NOTION_READWISE_ENABLE_ONTOLOGY:-true}"

DRY_RUN="${NOTION_READWISE_DRY_RUN:-false}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN="true"
      shift
      ;;
    --help|-h)
      echo "Usage: $0 [--dry-run]"
      echo "Environment variables: NOTION_READWISE_VAULT, NOTION_READWISE_PAGE_ID, NOTION_READWISE_DB_TITLE, NOTION_READWISE_LIMIT, NOTION_READWISE_SINCE_DAYS, NOTION_READWISE_ENABLE_ONTOLOGY, NOTION_READWISE_DRY_RUN"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      echo "Usage: $0 [--dry-run]" >&2
      exit 2
      ;;
  esac
done

is_true() {
  case "${1,,}" in
    1|true|yes|y|on)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

SYNC_DRY_FLAGS=()
if is_true "$DRY_RUN"; then
  SYNC_DRY_FLAGS+=(--dry-run)
fi

VAULT_REALPATH="$(realpath -m "$VAULT")"
if [[ ! -d "$VAULT_REALPATH" ]]; then
  echo "ERROR: VAULT '$VAULT' not found or is not a directory" >&2
  exit 1
fi

# normalize pipeline: sync -> prune invalid semantic links -> materialize (non-dry-run) -> final prune
"$PYTHON_BIN" "$ROOT_DIR/sync_readwise.py" \
  --vault "$VAULT_REALPATH" \
  --page-id "$PAGE_ID" \
  --db-title "$DB_TITLE" \
  --limit-per-category "$LIMIT" \
  --since-days "$SINCE_DAYS" \
  --enable-ontology "$ENABLED_ONT" \
  "${SYNC_DRY_FLAGS[@]}"

"$PYTHON_BIN" "$ROOT_DIR/prune_invalid_semantic_links.py" --vault "$VAULT_REALPATH" --dry-run

echo "[run_sync] dry-run summary done"
if [[ ${#SYNC_DRY_FLAGS[@]} -eq 0 ]]; then
  # Materialize only canonical ontology entities when explicitly requested
  "$PYTHON_BIN" "$ROOT_DIR/materialize_ontology_entities.py" --vault "$VAULT_REALPATH" --canonical --no-wiki
  # After consolidation, prune novamente and persist cleaned frontmatter
  "$PYTHON_BIN" "$ROOT_DIR/prune_invalid_semantic_links.py" --vault "$VAULT_REALPATH"
else
  echo "[run_sync] dry-run ativo: pulando materialização persistente"
fi

#!/usr/bin/env bash
set -euo pipefail

VAULT="${NOTION_READWISE_VAULT:-/home/rlmit/Obsidian}"
PAGE_ID="${NOTION_READWISE_PAGE_ID:-4c43c451-fdfc-4066-871b-310cbf477fdf}"
DB_TITLE="${NOTION_READWISE_DB_TITLE:-Library}"
LIMIT="${NOTION_READWISE_LIMIT:-50}"
SINCE_DAYS="${NOTION_READWISE_SINCE_DAYS:-0}"
ENABLED_ONT="${NOTION_READWISE_ENABLE_ONTOLOGY:-true}"

python3 /home/rlmit/clawdbot-skills/notion-readwise-sync/scripts/sync_readwise.py \
  --vault "$VAULT" \
  --page-id "$PAGE_ID" \
  --db-title "$DB_TITLE" \
  --limit-per-category "$LIMIT" \
  --since-days "$SINCE_DAYS" \
  --enable-ontology "$ENABLED_ONT"

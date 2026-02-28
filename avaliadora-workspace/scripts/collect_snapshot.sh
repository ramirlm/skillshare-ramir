#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-/tmp/avaliadora-workspace-snapshot}"
mkdir -p "$OUT_DIR"

# Also persist reports to Obsidian (ClawVault can index from there)
OBS_ROOT="$HOME/Obsidian"
# Do NOT use ~/Obsidian/OpenClaw/***
REPORT_DIR="$OBS_ROOT/Relatorios/avaliadora-workspace"
REPORT_TS="$(date +%Y-%m-%d_%H%M%S)"
REPORT_MD="$REPORT_DIR/snapshot-$REPORT_TS.md"
mkdir -p "$REPORT_DIR"

# Basic env
{
  echo "date: $(date -Is)"
  echo "pwd: $(pwd)"
  echo "user: $(whoami)"
  echo "host: $(hostname)"
  echo "kernel: $(uname -a)"
} > "$OUT_DIR/env.txt"

# OpenClaw status
(openclaw status --json || true) > "$OUT_DIR/openclaw-status.json"

# Cron jobs
(openclaw cron list --json || true) > "$OUT_DIR/cron-jobs.json"

# Agent config (best effort)
(
  cat "$HOME/.clawdbot/clawdbot.json" 2>/dev/null || true
  cat "$HOME/.openclaw/openclaw.json" 2>/dev/null || true
) > "$OUT_DIR/configs.txt"

# Quick grep for common footguns
(
  rg -n "~/vault|/vault" "$HOME"/clawdbot-agents "$HOME"/clawdbot-skills "$HOME"/.clawdbot "$HOME"/.openclaw 2>/dev/null || true
) > "$OUT_DIR/grep-vault-paths.txt"

# Obsidian footprint (do not dump content)
OBS="$HOME/Obsidian"
if [ -d "$OBS" ]; then
  {
    echo "obsidian_root: $OBS"
    echo "md_count: $(find "$OBS" -type f -name '*.md' | wc -l | tr -d ' ')"
    echo "recent_files (mtime<7d):"
    find "$OBS" -type f -name '*.md' -mtime -7 -maxdepth 6 2>/dev/null | head -200
  } > "$OUT_DIR/obsidian-summary.txt"
else
  echo "obsidian_root_missing: $OBS" > "$OUT_DIR/obsidian-summary.txt"
fi

# Write a lightweight Obsidian report (no secret dumping)
if [ -d "$OBS_ROOT" ]; then
  {
    echo "---"
    echo "title: \"Avaliadora Workspace — Snapshot $REPORT_TS\""
    echo "summary: \"Snapshot técnico do OpenClaw/workspace (status, crons, paths)\""
    echo "tags: [openclaw, workspace, audit, snapshot]"
    echo "processedAt: $(date -Is)"
    echo "source: avaliadora-workspace"
    echo "---"
    echo ""
    echo "## Snapshot dir"
    echo "- $OUT_DIR"
    echo ""
    echo "## Files"
    echo "- env: $OUT_DIR/env.txt"
    echo "- openclaw status: $OUT_DIR/openclaw-status.json"
    echo "- cron jobs: $OUT_DIR/cron-jobs.json"
    echo "- grep vault paths: $OUT_DIR/grep-vault-paths.txt"
    echo "- obsidian summary: $OUT_DIR/obsidian-summary.txt"
  } > "$REPORT_MD"
  echo "$REPORT_MD" > "$OUT_DIR/obsidian-report-path.txt"
fi

echo "$OUT_DIR"
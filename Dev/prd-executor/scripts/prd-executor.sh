#!/bin/bash
# PRD Executor - Runs coding tasks from a PRD
# Usage: prd-executor.sh --project <path> --agent <claude|codex> --prd <prd.json>

set -e

# Defaults
AGENT="claude"
PRD_FILE="agents/prd.json"
STATUS_FILE=".prd-status.json"
LOG_FILE=".prd-executor.log"

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --project) PROJECT_DIR="$2"; shift 2 ;;
    --agent) AGENT="$2"; shift 2 ;;
    --prd) PRD_FILE="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$PROJECT_DIR" ]]; then
  echo "Error: --project required"
  exit 1
fi

cd "$PROJECT_DIR"

# Initialize status
init_status() {
  cat > "$STATUS_FILE" <<EOF
{
  "started_at": "$(date -Iseconds)",
  "project": "$PROJECT_DIR",
  "agent": "$AGENT",
  "prd_file": "$PRD_FILE",
  "status": "running",
  "current_story": null,
  "completed": [],
  "failed": [],
  "last_update": "$(date -Iseconds)"
}
EOF
}

update_status() {
  local story_id="$1"
  local state="$2"
  local tmp=$(mktemp)
  
  jq --arg id "$story_id" --arg state "$state" --arg ts "$(date -Iseconds)" '
    .last_update = $ts |
    .current_story = (if $state == "running" then $id else null end) |
    (if $state == "done" then .completed += [$id] else . end) |
    (if $state == "failed" then .failed += [$id] else . end)
  ' "$STATUS_FILE" > "$tmp" && mv "$tmp" "$STATUS_FILE"
}

finish_status() {
  local state="$1"
  local tmp=$(mktemp)
  jq --arg state "$state" --arg ts "$(date -Iseconds)" '
    .status = $state | .finished_at = $ts | .current_story = null
  ' "$STATUS_FILE" > "$tmp" && mv "$tmp" "$STATUS_FILE"
}

# Get agent command
get_agent_cmd() {
  case "$AGENT" in
    claude) echo "claude --dangerously-skip-permissions" ;;
    codex) echo "codex --full-auto" ;;
    *) echo "claude --dangerously-skip-permissions" ;;
  esac
}

# Run a single story
run_story() {
  local story_id="$1"
  local title="$2"
  local description="$3"
  local criteria="$4"
  
  echo "[$(date)] Running story: $story_id - $title" | tee -a "$LOG_FILE"
  update_status "$story_id" "running"
  
  local prompt="Execute this user story from the PRD:

Story ID: $story_id
Title: $title
Description: $description

Acceptance Criteria:
$criteria

Instructions:
1. Implement ALL acceptance criteria
2. Run typecheck when done
3. Commit changes with message: \"feat($story_id): $title\"
4. Report success or failure"

  local agent_cmd=$(get_agent_cmd)
  
  if $agent_cmd "$prompt" >> "$LOG_FILE" 2>&1; then
    echo "[$(date)] Story $story_id completed" | tee -a "$LOG_FILE"
    update_status "$story_id" "done"
    
    # Mark as passed in PRD
    local tmp=$(mktemp)
    jq --arg id "$story_id" '
      .userStories |= map(if .id == $id then .passes = true else . end)
    ' "$PRD_FILE" > "$tmp" && mv "$tmp" "$PRD_FILE"
    
    return 0
  else
    echo "[$(date)] Story $story_id failed" | tee -a "$LOG_FILE"
    update_status "$story_id" "failed"
    return 1
  fi
}

# Main loop
main() {
  echo "[$(date)] PRD Executor starting" | tee "$LOG_FILE"
  echo "Project: $PROJECT_DIR" | tee -a "$LOG_FILE"
  echo "Agent: $AGENT" | tee -a "$LOG_FILE"
  echo "PRD: $PRD_FILE" | tee -a "$LOG_FILE"
  
  if [[ ! -f "$PRD_FILE" ]]; then
    echo "Error: PRD file not found: $PRD_FILE"
    exit 1
  fi
  
  init_status
  
  # Get incomplete stories sorted by priority
  local story_count=$(jq '[.userStories[] | select(.passes == false)] | length' "$PRD_FILE")
  
  if [[ "$story_count" -eq 0 ]]; then
    echo "No incomplete stories found"
    finish_status "completed"
    exit 0
  fi
  
  echo "Found $story_count incomplete stories"
  
  local failed=0
  local i=0
  
  while [[ $i -lt $story_count ]]; do
    # Re-read PRD each iteration to get fresh passes status
    local story=$(jq -c "[.userStories | sort_by(.priority) | .[] | select(.passes == false)][$i]" "$PRD_FILE")
    
    if [[ "$story" == "null" || -z "$story" ]]; then
      break
    fi
    
    local id=$(echo "$story" | jq -r '.id')
    local title=$(echo "$story" | jq -r '.title')
    local desc=$(echo "$story" | jq -r '.description')
    local criteria=$(echo "$story" | jq -r '.acceptanceCriteria | join("\n- ")')
    
    if ! run_story "$id" "$title" "$desc" "- $criteria"; then
      ((failed++))
    fi
    
    # Small delay between stories
    sleep 5
    
    # Re-count remaining stories (in case PRD was updated)
    story_count=$(jq '[.userStories[] | select(.passes == false)] | length' "$PRD_FILE")
    # Don't increment i - we always take the first incomplete story
  done
  
  if [[ $failed -eq 0 ]]; then
    finish_status "completed"
    echo "[$(date)] All stories completed successfully!" | tee -a "$LOG_FILE"
  else
    finish_status "partial"
    echo "[$(date)] Completed with $failed failures" | tee -a "$LOG_FILE"
  fi
}

main

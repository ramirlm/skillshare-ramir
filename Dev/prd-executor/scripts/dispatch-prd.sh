#!/bin/bash
# PRD Dispatcher - Launch PRD jobs on local or node targets
# Usage: dispatch-prd.sh --target <target> --agent <agent> [--prd <file>]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/../../../config/prd-targets.json"
STATE_FILE="${SCRIPT_DIR}/../../../state/prd-jobs.json"

# Defaults
AGENT="claude"
PRD_FILE="agents/prd.json"
TARGET=""

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --target) TARGET="$2"; shift 2 ;;
    --agent) AGENT="$2"; shift 2 ;;
    --prd) PRD_FILE="$2"; shift 2 ;;
    --config) CONFIG_FILE="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$TARGET" ]]; then
  echo "Usage: dispatch-prd.sh --target <target> --agent <agent> [--prd <file>]"
  echo ""
  echo "Available targets:"
  jq -r '.targets | to_entries[] | "  \(.key): \(.value.description)"' "$CONFIG_FILE"
  exit 1
fi

# Get target config
TARGET_CONFIG=$(jq -r --arg t "$TARGET" '.targets[$t]' "$CONFIG_FILE")

if [[ "$TARGET_CONFIG" == "null" ]]; then
  echo "Error: Unknown target: $TARGET"
  echo "Available: $(jq -r '.targets | keys | join(", ")' "$CONFIG_FILE")"
  exit 1
fi

TARGET_TYPE=$(echo "$TARGET_CONFIG" | jq -r '.type')
PROJECT_PATH=$(echo "$TARGET_CONFIG" | jq -r '.project')
NODE_ID=$(echo "$TARGET_CONFIG" | jq -r '.nodeId // empty')

# Generate job ID
JOB_ID="job-$(date +%Y%m%d-%H%M%S)"

echo "Dispatching PRD job..."
echo "  Job ID: $JOB_ID"
echo "  Target: $TARGET ($TARGET_TYPE)"
echo "  Project: $PROJECT_PATH"
echo "  Agent: $AGENT"
echo "  PRD: $PRD_FILE"
echo ""

# Add job to state
add_job_to_state() {
  local tmp=$(mktemp)
  jq --arg id "$JOB_ID" \
     --arg target "$TARGET" \
     --arg project "$PROJECT_PATH" \
     --arg agent "$AGENT" \
     --arg prd "$PRD_FILE" \
     --arg node "$NODE_ID" \
     --arg ts "$(date -Iseconds)" '
    .activeJobs += [{
      id: $id,
      target: $target,
      project: $project,
      agent: $agent,
      prdFile: $prd,
      nodeId: (if $node != "" then $node else null end),
      startedAt: $ts
    }]
  ' "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
}

# Dispatch based on target type
if [[ "$TARGET_TYPE" == "local" ]]; then
  echo "Starting local execution..."
  
  # Expand home directory
  EXPANDED_PATH="${PROJECT_PATH/#\~/$HOME}"
  
  # Run in background
  nohup "${SCRIPT_DIR}/prd-executor.sh" \
    --project "$EXPANDED_PATH" \
    --agent "$AGENT" \
    --prd "$PRD_FILE" \
    > /tmp/prd-${JOB_ID}.log 2>&1 &
  
  PID=$!
  echo "Started with PID: $PID"
  echo "Log: /tmp/prd-${JOB_ID}.log"
  
  add_job_to_state
  
elif [[ "$TARGET_TYPE" == "node" ]]; then
  if [[ -z "$NODE_ID" ]]; then
    echo "Error: Node target requires nodeId in config"
    exit 1
  fi
  
  echo "Dispatching to node via SSH: $NODE_ID"
  
  # Get SSH target from config
  SSH_TARGET=$(jq -r --arg t "$TARGET" '.targets[$t].sshTarget // empty' "$CONFIG_FILE")
  
  if [[ -z "$SSH_TARGET" ]]; then
    echo "Error: Node target requires sshTarget in config"
    exit 1
  fi
  
  # Run via SSH
  ssh "$SSH_TARGET" "nohup ~/scripts/prd-executor.sh --project '$PROJECT_PATH' --agent '$AGENT' --prd '$PRD_FILE' > /tmp/prd-${JOB_ID}.log 2>&1 &"
  
  echo "Started via SSH: $SSH_TARGET"
  
  add_job_to_state
  
else
  echo "Error: Unknown target type: $TARGET_TYPE"
  exit 1
fi

echo ""
echo "✅ Job $JOB_ID dispatched"
echo "Monitor with: cat state/prd-jobs.json"

---
name: prd-executor
description: "Execute PRD (Product Requirements Document) coding tasks on local or remote nodes. Use when: (1) Running automated coding jobs from a PRD, (2) Dispatching tasks to Mac/Linux nodes, (3) Monitoring long-running coding agent jobs, (4) Validating completed PRD work across multiple targets."
metadata:
  clawdbot:
    emoji: "🚀"
    os: ["darwin", "linux"]
---

# PRD Executor

Execute PRD coding tasks on local machines or remote nodes with progress tracking.

## Quick Start

**Dispatch a job:**
```bash
./scripts/prd-executor.sh --project ~/Projects/myapp --agent claude --prd agents/prd.json
```

**On a node:**
```bash
nodes run --node macair --command "~/scripts/prd-executor.sh --project ~/Projects/myapp --agent claude"
```

## Targets

| Target | Type | Project Path |
|--------|------|--------------|
| `local:proxi` | local | ~/clawd/projects/proxi |
| `local:g2i` | local | ~/Projects/g2i |
| `node:g2i` | node | Mac for G2i |
| `node:proxi` | node | Mac for Proxi |
| `node:macair` | node | MacBook Air |

Configure in `config/prd-targets.json`.

## Agents

| Agent | Command |
|-------|---------|
| `claude` | `claude --model claude-opus-4-5` |
| `codex` | `codex --full-auto` |

## Dispatching Jobs

### Local Execution
```bash
# Start job
./scripts/prd-executor.sh --project /path/to/project --agent claude --prd agents/prd.json &

# Check status
cat /path/to/project/.prd-status.json
```

### Node Execution
```bash
# Run on node
nodes run --node <nodeId> --command "./scripts/prd-executor.sh --project ~/Projects/app --agent codex"

# Check status on node
nodes run --node <nodeId> --command "cat ~/Projects/app/.prd-status.json"
```

## Status Tracking

Jobs write to `.prd-status.json`:
```json
{
  "status": "running|completed|partial|failed",
  "current_story": "US-001",
  "completed": ["US-001", "US-002"],
  "failed": [],
  "last_update": "2026-01-20T07:45:00Z"
}
```

## Monitoring Workflow

1. **Track active jobs** in `state/prd-jobs.json`
2. **Check status** via local file or `nodes run`
3. **Notify user** of progress changes
4. **Validate** completed work by reviewing output

See `references/monitoring.md` for heartbeat integration.

## Job Lifecycle

```
CREATE PRD → DISPATCH → RUNNING → MONITORING → COMPLETED → VALIDATE
                ↓
           state/prd-jobs.json tracks active jobs
                ↓
           .prd-status.json on target tracks progress
```

## Files

| File | Purpose |
|------|---------|
| `scripts/prd-executor.sh` | Main executor script |
| `config/prd-targets.json` | Target/agent definitions |
| `state/prd-jobs.json` | Active job tracking |
| `.prd-status.json` | Per-project status (on target) |
| `.prd-executor.log` | Execution log (on target) |

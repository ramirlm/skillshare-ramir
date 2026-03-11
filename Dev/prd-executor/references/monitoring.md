# Monitoring PRD Jobs

## Job Tracking State

Active jobs are tracked in `state/prd-jobs.json`:

```json
{
  "activeJobs": [
    {
      "id": "job-20260120-074500",
      "target": "node:macair",
      "project": "~/Projects/proxi",
      "agent": "claude",
      "prdFile": "agents/prd.json",
      "startedAt": "2026-01-20T07:45:00Z",
      "nodeId": "macair"
    }
  ],
  "completedJobs": [],
  "lastChecked": "2026-01-20T08:00:00Z"
}
```

## Heartbeat Integration

Add to HEARTBEAT.md:

```markdown
### PRD Jobs
- [ ] Check `state/prd-jobs.json` for active jobs
- [ ] If active job exists, check status file on target
- [ ] Notify user of progress or completion
- [ ] Validate completed work if status is "completed"
```

## Checking Job Status

### Local Jobs

```bash
cat /path/to/project/.prd-status.json | jq
```

### Node Jobs

```bash
nodes run --node <nodeId> --command "cat ~/Projects/app/.prd-status.json"
```

## Status Interpretation

| Status | Meaning | Action |
|--------|---------|--------|
| `running` | Job in progress | Report current story |
| `completed` | All stories passed | Validate and notify |
| `partial` | Some stories failed | Report failures |
| `failed` | Critical failure | Alert user |

## Validation Checklist

When status is `completed`:

1. **Check git log** - Verify commits exist
2. **Run typecheck** - Ensure no type errors
3. **Run tests** - If project has tests
4. **Review PRD** - All `passes: true`
5. **Update job state** - Move to completedJobs

## Notification Templates

### Progress Update
```
📊 PRD Job Update: {project}
- Status: {status}
- Current: {current_story}
- Done: {completed_count}/{total_count}
- Agent: {agent}
```

### Completion
```
✅ PRD Job Complete: {project}
- Stories: {completed_count} completed
- Failures: {failed_count}
- Duration: {duration}

Ready for validation?
```

### Failure Alert
```
⚠️ PRD Job Issue: {project}
- Status: {status}
- Failed stories: {failed_stories}
- Last error: {last_error}

Check logs: .prd-executor.log
```

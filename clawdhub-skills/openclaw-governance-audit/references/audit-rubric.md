# Audit Rubric

Score each axis from 0 to 5.

## Score scale

- **0 — Absent:** no evidence of governance.
- **1 — Fragile:** ad hoc, undocumented, dependent on one person's memory.
- **2 — Partial:** some structure exists, but gaps are frequent or risky.
- **3 — Functional:** works in normal conditions, with noticeable governance debt.
- **4 — Strong:** documented, consistent, and usually followed.
- **5 — Exemplary:** explicit ownership, review cadence, low drift, easy recovery.

## Axis checklist

### 1. Memory / Vault

Check:
- canonical persistence path is explicit
- Obsidian usage matches policy
- session recovery artifacts exist and are current
- duplicate memory stores are minimized
- memory writes follow a repeatable structure

Common gaps:
- writes split across workspace + vault + ad hoc folders
- no retention/archival logic
- weak recovery after context truncation

### 2. Security / Updates

Check:
- current version posture is known
- update/rollback path exists
- sensitive files are handled safely
- exposed services and auth states are reviewed
- backups exist before risky changes

Common gaps:
- manual updates with no checklist
- secrets in scripts/configs
- no health review cadence

### 3. Jobs / Crons

Check:
- each job has owner, purpose, schedule, and output path
- stale jobs are removed or disabled
- failures are observable
- scripts referenced by jobs still exist
- timezone assumptions are documented
- root cause of job failures/drift is recorded, not just the symptom
- prevention controls exist for recurring failures (alerts, tests, cleanup, ownership review, path validation)
- legacy comments/messages/output paths and orphaned scripts are reviewed

Common gaps:
- “mystery crons” nobody owns
- silent failures
- duplicate automations doing the same thing
- same cron breaks repeatedly because only the symptom gets patched
- moved/deleted scripts still referenced by cron, docs, or notifications

### 4. Configuration

Check:
- workspace and skills tree follow conventions
- active agent docs match real filesystem layout
- gateway/agent config is discoverable
- bootstrap/identity/session documents exist where expected
- config drift is visible and fixable

Common gaps:
- documented paths differ from actual paths
- customizations spread across too many files
- skill placement violates workspace rules

### 5. Knowledge Governance

Check:
- source-of-truth hierarchy is clear
- `SOUL.md`, `AGENTS.md`, `TOOLS.md`, `SESSION-STATE.md`, and memory docs do not conflict materially
- WAL/session-state rules are operational, not aspirational
- cross-agent conventions are consistent
- memory-management policy is explicit
- obsolete guidance, legacy path references, and old runbooks/messages are identified
- the artifact that introduced a governance problem can be named where possible
- recurrence prevention is part of the recommendation, not an afterthought

Common gaps:
- duplicated rules with contradictory wording
- too many places storing “current truth”
- delegation policy inconsistent with actual execution model
- deprecated paths/messages keep reintroducing old behavior

## Minimum output per axis

For every axis, report:
- score
- confidence
- evidence bullets
- key gaps
- risks
- quick wins (1-2 weeks)
- structural fixes (this quarter)
- for each major issue: originating artifact/owner, root cause, recurrence risk, prevention step

## Consolidation priorities

Prioritize in this order unless the user says otherwise:
1. recoverability and memory integrity
2. security and secret hygiene
3. cron/job reliability
4. configuration drift reduction
5. governance clarity across agents

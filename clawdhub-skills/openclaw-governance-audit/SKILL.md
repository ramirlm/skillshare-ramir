---
name: openclaw-governance-audit
description: Audit an OpenClaw setup across memory/vault, security/updates, jobs/crons, configuration, and knowledge governance. Use when reviewing an agent workspace, checking operational hygiene, finding governance gaps, comparing multiple agents, or building an improvement plan for memory management, SESSION-STATE discipline, SOUL.md/MEMORY.md consistency, and specialized subagent workflows.
---

# OpenClaw Governance Audit

Audit OpenClaw in five axes and consolidate one practical governance report. Prefer subagents specialized by aspect, then merge findings into a single decision-ready summary.

## Quick start

**Default operational path (mandatory for normal runs):** use `python3 scripts/run_governance_audit.py` so every execution generates Markdown + PDF + email evidence automatically.

1. Confirm audit scope: which workspace, which agents, and whether host-level inspection is allowed.
2. Read `references/audit-rubric.md` and `references/report-template.md`.
3. Choose audit mode:
   - **Small / time-boxed audit:** do one pass yourself across all five axes, then write one concise report.
   - **Larger / multi-workspace audit:** split into five aspect owners:
     - memory/vault
     - security/updates
     - jobs/crons
     - configuration
     - knowledge governance
4. Inspect evidence, cite files/commands, and score gaps.
5. For every meaningful problem found, explicitly capture:
   - who owns it or which artifact generated it (job, script, config, doc, path, agent)
   - the likely root cause
   - why it persisted or recurred
   - the smallest prevention change that would stop repetition
   - any legacy messages, deprecated paths, or orphaned scripts still reinforcing the problem
6. Consolidate into one report with:
   - current state
   - gaps
   - risks
   - opportunities
   - prioritized improvement plan
   - explicit memory-management recommendations
   - root-cause + recurrence-prevention notes for the important findings

## Audit workflow

### 1) Frame the audit

Capture:
- target paths and agent workspaces
- whether to inspect `~/.clawdbot`, `~/clawdbot-agents`, `~/clawdbot-skills`, and `~/Obsidian`
- desired output path for the report
- whether the goal is diagnosis only or diagnosis + remediation plan

### 2) Delegate by axis

For smaller audits, skip five-way delegation and keep one evidence-first pass so the audit stays fast and coherent.

For larger audits, use one subagent per axis. Give each subagent:
- the exact axis
- the target paths
- the rubric section to use from `references/audit-rubric.md`
- an instruction to return evidence-first findings, not generic advice
- a request to return only: score, confidence, evidence, gaps, risks, quick wins, structural fixes

Recommended responsibilities:
- **Memory/Vault:** inspect persistence rules, Obsidian usage, vault sprawl, session state discipline, memory write paths, use of clawvault/ontology when relevant.
- **Security/Updates:** inspect OpenClaw version posture, secrets handling, exposed services, auth state, backups before updates, and hardening hygiene.
- **Jobs/Crons:** inspect cron jobs, automation scripts, ownership, schedules, alerting, stale jobs, missing job documentation, root cause of failures/drift, and recurrence-prevention controls.
- **Configuration:** inspect gateway/agent config, workspace conventions, skill placement, path consistency, drift between documented vs real config, and deprecated/legacy paths still referenced anywhere.
- **Knowledge Governance:** inspect `SOUL.md`, `MEMORY.md`, `SESSION-STATE.md`, `AGENTS.md`, cross-agent consistency, WAL protocol adherence, duplication/conflict between sources of truth, and old messages/runbooks that keep obsolete behavior alive.

### 3) Gather evidence

Prefer concrete evidence over summaries. Useful evidence includes:
- file paths and excerpts
- command outputs
- last modified times
- mismatched directories or duplicate memory stores
- missing documents that should exist
- automation scripts without owners or runbooks
- legacy messages, comments, docs, or notifications that still point to replaced behavior
- cron entries pointing to moved/deleted scripts or superseded output paths
- orphaned scripts/config fragments that still exist but no longer have an owner or active caller

When time is limited, collect the smallest evidence set that still supports a scored judgment for every axis. For each major issue, gather enough evidence to name the triggering artifact and defend a plausible root cause. Do not inflate the audit with generic best practices that are not tied to inspected evidence.

### 4) Score and normalize

Use the rubric in `references/audit-rubric.md`.

For each axis, record:
- score `0-5`
- confidence `high|medium|low`
- top 3 gaps
- top risks
- quick wins
- strategic fixes
- for each major finding: origin/owner artifact, root cause, recurrence vector, and prevention control

### 5) Consolidate the report

Use `references/report-template.md` or generate a scaffold with:
- `python3 scripts/generate_audit_scaffold.py --workspace <path> --output <report.md>`

The final report must end with a **Memory Management Improvement Plan** covering:
- canonical write locations
- session-state discipline
- conflict resolution between files and vault notes
- retention/archival rules
- cross-agent governance rules

## Audit heuristics by axis

### Memory / Vault

Check for:
- clear canonical storage in `~/Obsidian` versus accidental writes elsewhere
- deprecated or duplicate locations such as old vault folders
- evidence that operational knowledge is saved consistently
- alignment between persona rules and actual memory writes
- recoverability after context loss

### Security / Updates

Check for:
- outdated OpenClaw or skills with no upgrade process
- secrets committed to files or loose scripts
- exposed endpoints with weak review
- missing backup/rollback before updates
- no documented healthcheck cadence

### Jobs / Crons

Check for:
- jobs with no owner, no output path, or no failure notification
- stale scripts referenced by active cron entries
- overlapping jobs, duplicate schedules, timezone confusion
- missing periodic audits of job usefulness
- who or what created the job/script and whether that ownership is still valid
- root cause of prior failures/drift and whether a prevention control exists
- legacy cron messages/comments/output paths that keep pointing people to deprecated behavior
- orphaned automation scripts no longer referenced by crons but still present in the workspace

### Configuration

Check for:
- skills created in the wrong tree
- drift between `AGENTS.md`, config files, and actual filesystem layout
- conflicting workspace assumptions
- missing bootstrap/identity/session documents for active agents

### Knowledge Governance

Check for:
- contradictions across `SOUL.md`, `AGENTS.md`, `TOOLS.md`, `MEMORY.md`, `SESSION-STATE.md`
- missing write-ahead logging discipline
- instructions that require delegation while the runtime/tooling suggests direct execution
- agent-specific policies that are not mirrored in related agents
- no clear source of truth for operational rules vs long-term knowledge
- legacy wording, old handoff text, or obsolete path references that continue to produce wrong behavior
- whether the document/process that introduced a problem is identifiable and still active

## Reporting rules

- Cite evidence for every important claim.
- Mark uncertain findings as `[UNVERIFIED]`.
- Separate facts, risks, and recommendations.
- For each major issue, state the responsible artifact/owner if known, the likely root cause, and a concrete prevention step.
- Explicitly call out legacy messages, deprecated paths, and orphaned scripts when they contribute to drift or recurrence.
- Prefer prioritized fixes over exhaustive commentary.
- If remediation is not authorized, stop at recommendations and proposed next actions.
- Every normal execution must produce: (1) report of altered/corrected/identified items, (2) PDF conversion, and (3) email delivery to `ramir.mesquita@gmail.com`.
- Weekly automation should call the runner with `--send-email --commit-push`.

## Resources

- Read `references/audit-rubric.md` before scoring.
- Read `references/report-template.md` before writing the consolidated report.
- Use `scripts/generate_audit_scaffold.py` to create a consistent report skeleton quickly.

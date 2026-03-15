---
name: agent-maintenance
description: Audit and maintain OpenClaw agent workspaces so every agent keeps the required base files, uses `~/Obsidian` as the shared durable brain with the user, keeps `memory/` only for short self-notes, and detects path drift, missing governance files, deprecated memory destinations, and cross-agent inconsistency. Use when normalizing agent workspaces, fixing missing `MEMORY.md`/`SESSION-STATE.md`/`SOUL.md`, reviewing agent governance, or running periodic maintenance across multiple agents.
---

# Agent Maintenance

Maintain agent workspaces in a consistent, recoverable, low-drift state.

## Core model

Apply this semantic split everywhere:
- `~/Obsidian` = shared durable memory between Ramir and the agents
- `memory/` = short self-notes and operational scratch space for the agent
- `SESSION-STATE.md` = current session continuity / working RAM
- `MEMORY.md` = governance/index file, not a dump of durable knowledge
- `sessions/`, `agent/`, `.openclaw/` = technical runtime state

## Default workflow

1. Inventory all agent workspaces in `~/clawdbot-agents/`.
2. Verify the required base files exist:
   - `AGENTS.md`
   - `SOUL.md`
   - `MEMORY.md`
   - `SESSION-STATE.md`
   - `IDENTITY.md`
   - `USER.md`
3. Scan for path drift and deprecated destinations:
   - `clawdmold`
   - `~/Obsidian/ClawVault`
   - `~/Obsidian/OpenClaw`
   - `OpenClaw/Agentes/Memory Extracts`
4. Classify findings:
   - missing base file
   - wrong durable-memory destination
   - `memory/` treated as durable memory
   - historical/deprecated text only
   - structural exception that should be documented
5. Fix the smallest safe thing first:
   - create missing base files from the standard policy
   - normalize `MEMORY.md` wording
   - normalize `SESSION-STATE.md`
   - align paths to `~/Obsidian`
   - leave historical reports alone unless the user asks to rewrite them
6. Produce a concise per-agent report with:
   - created files
   - corrected files
   - remaining issues
   - intentional legacy/deprecated items

## Standard policy to enforce

### MEMORY.md
Enforce wording equivalent to:
- this file is not the durable memory destination
- durable shared memory belongs in `~/Obsidian`
- `memory/` is only for short self-notes and operational notes
- deprecated destinations are invalid for new knowledge

### SESSION-STATE.md
Enforce wording equivalent to:
- read on session start
- store only operational continuity, handoffs, checkpoints, temporary decisions
- shared durable knowledge goes to `~/Obsidian`

## Read on demand

- Read `references/templates.md` when you need the standard file templates.
- Run `scripts/agent_maintenance_audit.py` for a quick audit summary in markdown or json.

## Rules

- Prefer narrow edits over broad rewrites.
- Do not treat historical reports as active policy.
- Preserve explicit deprecated/prohibited-path sections when they help prevent regressions.
- If an agent has a justified exception, document it instead of forcing silent divergence.
- When a skill exists inside an agent workspace, flag it as a structural exception unless the user explicitly wants it there.

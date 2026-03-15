---
name: daily-security-triage
description: Daily local security triage (shell profile injection + common persistence indicators) and email summary.
---

# Daily Security Triage

This skill provides a lightweight **local** triage script to detect common signs of:
- shell-profile injection (`~/.zshrc`, `~/.bashrc`, etc.)
- suspicious git config tampering (`hooksPath`, malicious aliases)
- `~/.node_modules` persistence patterns
- unusual `node` external network connections

## Script

- Path: `~/clawdbot-skills/daily-security-triage/scripts/triage.sh`

## Output rules

- Never print or email secret values.
- If environment variables are detected in shell profiles (e.g., `*_API_KEY`), only report the **variable name** and the **file:line**.

## Manual run

```bash
bash ~/clawdbot-skills/daily-security-triage/scripts/triage.sh
```

## Intended scheduling

Run daily at 00:00 (America/Fortaleza) and email a short summary to Ramir.

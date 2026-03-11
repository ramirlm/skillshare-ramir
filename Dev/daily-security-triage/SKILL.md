---
name: daily-security-triage
description: "Daily local security triage: detects shell-profile injection, git config tampering, suspicious ~/.node_modules persistence, and unusual network connections. Generates a summary and optionally emails results. Use when: (1) Running routine daily security checks, (2) Investigating suspected compromise, (3) Verifying system integrity after installing new tools."
version: 1.1.0
author: ramirlm
triggers:
  - "security triage"
  - "triagem de segurança"
  - "verificar segurança"
  - "check security"
  - "/triage"
metadata:
  clawdbot:
    emoji: "🔐"
    os: ["linux", "darwin"]
    requires:
      bins: ["bash", "grep", "lsof"]
---

# Daily Security Triage

Lightweight **local** triage script to detect common signs of compromise on the host machine.

## What It Detects

| Category | What Is Checked |
|----------|----------------|
| **Shell profile injection** | `~/.zshrc`, `~/.bashrc`, `~/.profile`, etc. for eval/atob/base64/curl-pipe-sh patterns |
| **Secret env var exposure** | Exported `*_API_KEY`, `*_TOKEN`, `*_SECRET`, `*_PASSWORD` variables (reports names only, never values) |
| **Git config tampering** | `core.hooksPath` overrides, suspicious aliases in `~/.gitconfig` |
| **~/.node_modules persistence** | Unexpected global Node packages that may indicate supply-chain attack or persistence |
| **node network connections** | Live snapshot of outbound `node` connections via `lsof` |

## Script

- **Path:** `{baseDir}/scripts/triage.sh`
- **Runtime:** ~5 seconds on typical machine
- **Exit code:** Always `0` (triage-only; review output to decide next steps)

## Output Rules

- **Never** print or email secret values; only report variable names and file:line locations
- Findings are displayed per section with file paths and line numbers
- Clean sections print "No suspicious … found" (easy to grep/filter)

## Usage

### Manual run

```bash
bash {baseDir}/scripts/triage.sh
```

### Capture output to file

```bash
bash {baseDir}/scripts/triage.sh | tee ~/triage-$(date +%Y%m%d).txt
```

### Scheduled (cron)

```bash
# Run daily at 00:00 America/Fortaleza (UTC-3) and email summary
0 0 * * * TZ=America/Fortaleza bash ~/clawdbot-skills/daily-security-triage/scripts/triage.sh | mail -s "[TRIAGE] $(hostname) $(date +%F)" your@email.com
```

## Interpreting Results

### Shell profile injection

If patterns like `eval(atob(...)`, `curl ... | bash`, or `python -c` appear in shell profiles:
1. **Do not source the profile** until you understand the change
2. Review the line in context with `sed -n 'LINE_NUMp' ~/.zshrc`
3. If injected by malware: remove the line, rotate any secrets that were in scope, check `~/.ssh/authorized_keys`

### Secret env vars in shell profiles

If variables like `MY_API_KEY` are exported from shell profiles:
- This is common and often fine, but confirm each one is intentional
- Remove credentials you no longer use
- Consider using a secrets manager instead of shell profiles

### Git config tampering

`core.hooksPath` pointing outside your project directory is a red flag:
```
core.hooksPath = /tmp/.hooks   ← suspicious
core.hooksPath = .husky        ← normal
```

### ~/.node_modules persistence

This directory should normally be empty or absent. If it contains unexpected packages, investigate:
```bash
ls -la ~/.node_modules
cat ~/.node_modules/package.json   # check scripts field
```

### node network connections

Review any `node` process connecting to unexpected IPs. Use `whois <IP>` to identify ownership.

## Scheduling

Add to your Clawdbot cron or OS crontab:

```yaml
# Clawdbot cron example
- name: daily-security-triage
  schedule: "0 0 * * *"
  timezone: "America/Fortaleza"
  command: bash ~/clawdbot-skills/daily-security-triage/scripts/triage.sh
  notify: email
```

## Security Notes

- The script is **read-only** — it never modifies files or kills processes
- It runs entirely locally — no data is sent to external services
- Output may contain partial file paths; treat the output file itself as potentially sensitive
- Review findings before sharing triage output with others

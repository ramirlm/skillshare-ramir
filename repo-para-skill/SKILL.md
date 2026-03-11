---
name: repo-para-skill
description: Convert any public GitHub repository into a reusable Clawdbot skill by cloning source, extracting architecture and usage signals, and generating structured references so future interactions can work with that repo as a codified skill.
version: 1.0.0
author: ramirlm
triggers:
  - "converter repo para skill"
  - "repo to skill"
  - "criar skill do repositório"
metadata:
  clawdbot:
    emoji: "🔨"
    os: ["linux", "darwin", "windows"]
---

# repo-para-skill

## Quick start

```bash
cd ~/clawdbot-skills/repo-para-skill
python3 scripts/explora_repo.py <github-repo-url-or-owner/repo> [--skill-name <nome-skill>]
```

Examples:

```bash
python3 scripts/explora_repo.py https://github.com/expressjs/express
python3 scripts/explora_repo.py torvalds/linux --skill-name linux-knowledge
python3 scripts/explora_repo.py facebook/react --output /home/rlmit/clawdbot-skills --force
```

## What this skill does

- Validates and normalizes GitHub identifiers.
- Clones the repo shallowly.
- Detects language/runtime hints and high-signal files.
- Generates a new skill folder in `~/clawdbot-skills/<skill-name>/` with:
  - `SKILL.md` (purpose, usage, workflow)
  - `references/repo-overview.md` (metadata, build/test commands, structure)
  - `references/file-index.md` (prioritized file list)
  - `references/notes.md` (operational notes and risks)
  - Optional copied docs/assets snapshots from the source repo.
- Uses deterministic naming and avoids creating nested arbitrary files.

## How to use the script

```bash
python3 scripts/explora_repo.py <repo> [flags]
```

### Required argument

- `repo`: one of
  - `https://github.com/owner/repo`
  - `git@github.com:owner/repo.git`
  - `owner/repo`

### Optional flags

- `--skill-name <name>`: explicit output skill name (lowercase/hyphen).
- `--output <dir>`: output parent directory (default `~/clawdbot-skills`).
- `--workdir <dir>`: temp clone directory (default `/tmp/explora-repo`).
- `--max-files <n>`: number of files indexed in `file-index.md` (default `200`).
- `--no-docs`: do not copy markdown/docs content.
- `--force`: overwrite existing target skill folder.
- `--help`: show usage.

## Workflow (recommended)

1. Run the script with the repo URL.
2. Open the generated `SKILL.md` and skim:
   - `references/repo-overview.md` (setup + runtime commands)
   - `references/file-index.md` (entry points)
3. If needed, fine-tune `SKILL.md` manually for your team’s exact triggers.
4. Package the resulting skill if you want distributable format:

```bash
cd ~/clawdbot-skills
python3 /home/linuxbrew/.linuxbrew/Cellar/node/25.5.0/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py repo-para-skill
```

## Safety and scope

- Uses only public GitHub content.
- Does not push to remotes.
- Keeps generated files lightweight and reproducible.
- For very large repos, it indexes a representative subset (`--max-files`).

## Resources

- `scripts/explora_repo.py`: full conversion automation.
- `references/github-url-patterns.md`: accepted URL formats and parser rules.
- `references/repo-to-skill-protocol.md`: criteria used to generate skill fields.

# skillshare-ramir

A curated collection of [ClawdBot](https://github.com/openclawai/openCLAW) skills organized by category.

## Folder Structure

### 🦾 OpenCLAW/
Skills that support and extend the OpenCLAW / ClawdBot ecosystem itself — infrastructure, skill management, workspace auditing, and meta-tooling.

| Skill | Description |
|-------|-------------|
| agent-memory-hygiene | Refactors agent MEMORY.md files, migrates runbooks/tool-notes, normalizes Ontology entries |
| avaliadora-workspace | Audits and evaluates the Clawdbot workspace for memory optimization and performance |
| clawdbot-backup | Backup, restore, and sync ClawdBot configuration, skills, and settings across devices |
| clawsec-suite | Security suite manager with advisory-feed monitoring and malicious-skill response |
| ontologia-transcript | Processes meeting transcriptions through summarize/ontology skills, persists to vault |
| prompt-guard | Advanced prompt injection defense for Clawdbot in group chats |
| repo-para-skill | Converts public GitHub repositories into reusable Clawdbot skills |
| self-improving-agent | Captures learnings, errors, and corrections for continuous agent improvement |
| skill-creator | Guidance and tooling for creating and packaging effective skills |
| skill-evaluator | Evaluates skills across 25 criteria (ISO 25010, OpenSSF, agent-specific heuristics) |
| skillshare | Syncs skills across AI CLI tools from a single source of truth |

### 💻 Dev/
Skills focused on software development, coding workflows, automation, and technical tooling.

| Skill | Description |
|-------|-------------|
| brainstorming | Turns ideas into fully formed designs and specs through collaborative dialogue |
| daily-security-triage | Local security triage: shell-profile injection, git config tampering, unusual connections |
| grok-search | Web/X search via xAI Grok with structured JSON output and citations |
| opensrc-fetch | Fetches npm packages and GitHub repos to give coding agents deeper context |
| parallel-task | Orchestrates parallel task execution from plan files, delegating to subagents |
| playwright-auth | Saves browser authentication state for any website using Playwright |
| playwright-cli | Browser automation via Playwright CLI (screenshots, element interaction) |
| prd | Creates and manages Product Requirements Documents with user stories |
| prd-executor | Executes PRD coding tasks on local or remote nodes with progress tracking |
| reuniao-para-prd | Transforms meeting transcriptions (PT-BR) into insights and PRDs |
| video-bug-prompt | Analyzes bug videos, extracts frames, searches project context, generates reports |
| youtube-transcript | Fetches and summarizes YouTube transcripts with language selection |

### 📋 Productivity/
Skills for task management, knowledge organization, learning, and personal workflows.

| Skill | Description |
|-------|-------------|
| ai-usage-monitor | Monitors and estimates usage/consumption for AI tools (Cursor, Codex, Copilot, etc.) |
| council-of-the-wise | Multi-perspective panel (Devil's Advocate, Architect, Engineer, Artist, Quant) for feedback |
| leitura-espacada | Spaced repetition study system using the SM-2 algorithm |
| notion-readwise-sync | Syncs Notion Readwise Library into Obsidian as curated Markdown notes |
| process-vault-frontmatters | Standardizes YAML frontmatter metadata in Obsidian vault notes |
| qmd-skill | Local hybrid search engine for Markdown notes with BM25 and optional vector search |
| resumidor-auto | Automatically summarizes content and saves to Obsidian with tags and categories |
| td-task-management | Minimalist CLI for tracking tasks and maintaining agent memory across context windows |
| todo-list-manager | Task lists organized by life priorities (Deus/Igreja, Família, Trabalho, Casa, Lazer) |

### 🎲 Random/
Skills that don't fit neatly into the other categories.

| Skill | Description |
|-------|-------------|
| assessor-juridico | Consumer law agent: documents judicial processes, prepares petitions, tracks deadlines |
| evangelho-do-dia-ptbr | Fetches the daily Gospel in Portuguese from evangeli.net with optional reflection |

---
name: agent-memory-hygiene
description: Refatora MEMORY.md dos agentes: mantém regras duráveis, migra runbooks/tool-notes para TOOLS.md/Obsidian e redige segredos.
metadata: {"clawdbot":{"emoji":"🧹","os":["linux"],"requires":{"bins":["python3"]}}}
---

# /agent-memory-hygiene

Padroniza o uso de `MEMORY.md` vs `TOOLS.md` em **todos os agentes** (workspaces em `~/clawdbot-agents/*`).

## O que faz

- Para cada agente com `MEMORY.md`:
  - Mantém em `MEMORY.md` apenas **regras duráveis** (segurança, limites de autonomia, princípios de workflow).
  - Migra conteúdo operacional (runbooks, comandos, tutoriais, infra, notas longas) para `TOOLS.md`.
  - Gera um “dump” do conteúdo migrado no Obsidian para referência humana, com redaction básica de segredos.

## Onde salva no Obsidian

- `~/Obsidian/OpenClaw/Agentes/Memory Extracts/<agentId>/memory-extract-YYYY-MM-DD.md`

## Executar

Dry-run:
```bash
python3 /home/rlmit/clawdbot-skills/agent-memory-hygiene/agent_memory_hygiene.py --agents-root "$HOME/clawdbot-agents" --obsidian "$HOME/Obsidian" 
```

Aplicar:
```bash
python3 /home/rlmit/clawdbot-skills/agent-memory-hygiene/agent_memory_hygiene.py --agents-root "$HOME/clawdbot-agents" --obsidian "$HOME/Obsidian" --write
```

---
name: agent-memory-hygiene
description: Refatora MEMORY.md dos agentes com ação corretiva (proativa), migra runbooks/tool-notes para TOOLS.md/Obsidian e normaliza entradas na Ontology.
metadata: {"clawdbot":{"emoji":"🧹","os":["linux"],"requires":{"bins":["python3"]}}}
---

# /agent-memory-hygiene

Padroniza o uso de `MEMORY.md` vs `TOOLS.md` em **todos os agentes** (workspaces em `~/clawdbot-agents/*`).

## O que faz

- Para cada agente com `MEMORY.md`:
  - Mantém em `MEMORY.md` apenas **regras duráveis** (segurança, limites de autonomia, princípios de workflow).
  - Move conteúdo operacional (runbooks, comandos, tutoriais, infra, notas longas) para `TOOLS.md`.
  - **Ação corretiva automática**: normaliza blocos, adiciona metadados (`extraído`, `status`, `impacto`) e estrutura `TODO` em campos de rastreio.
  - Não deleta conteúdo: somente desloca/enriquece por segurança e rastreabilidade.
  - Gera um “dump” do conteúdo migrado no Obsidian para referência humana.
  - Cria/atualiza entidades na **Ontology** para cada agente/documento migrado.

## Onde salva

- Obsidian: `~/Obsidian/OpenClaw/Agentes/Memory Extracts/<agentId>/memory-extract-YYYY-MM-DD.md`
- Ontology: `~/clawdbot-agents/main/memory/ontology/graph.jsonl` (+ `schema.yaml`)

## Executar

Dry-run:
```bash
python3 /home/rlmit/clawdbot-skills/agent-memory-hygiene/agent_memory_hygiene.py --agents-root "$HOME/clawdbot-agents" --obsidian "$HOME/Obsidian" --ontology-root "$HOME/clawdbot-agents/main/memory/ontology"
```

Aplicar:
```bash
python3 /home/rlmit/clawdbot-skills/agent-memory-hygiene/agent_memory_hygiene.py \
  --agents-root "$HOME/clawdbot-agents" \
  --obsidian "$HOME/Obsidian" \
  --ontology-root "$HOME/clawdbot-agents/main/memory/ontology" \
  --write
```

Validação extra (recomendada):
```bash
python3 /home/rlmit/clawdbot-skills/skills/ontology/scripts/ontology.py validate --graph "$HOME/clawdbot-agents/main/memory/ontology/graph.jsonl" --schema "$HOME/clawdbot-agents/main/memory/ontology/schema.yaml"
```
---
name: agent-memory-hygiene
description: Refatora MEMORY.md dos agentes com ação corretiva (proativa), migra runbooks/tool-notes para TOOLS.md/Obsidian e normaliza entradas na Ontology.
version: 1.0.0
author: ramirlm
triggers:
  - "/agent-memory-hygiene"
  - "limpar memória dos agentes"
  - "refatorar MEMORY.md"
  - "migrar TOOLS.md"
metadata:
  clawdbot:
    emoji: "🧹"
    os: ["linux"]
    requires:
      bins: ["python3"]
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

- Obsidian: `[OBSIDIAN_VAULT]/inbox/memory-extract-<agentId>-YYYY-MM-DD.md` (armazenado via clawvault + ontology)
- Ontology: `[AGENTS_ROOT]/main/memory/ontology/graph.jsonl` (+ `schema.yaml`)

> Substitua `[OBSIDIAN_VAULT]` por `$HOME/Obsidian` (ou valor de `CLAWVAULT_PATH`) e `[AGENTS_ROOT]` por `$HOME/clawdbot-agents`.

## Executar

Dry-run:
```bash
python3 {baseDir}/agent_memory_hygiene.py \
  --agents-root "$HOME/clawdbot-agents" \
  --obsidian "$HOME/Obsidian" \
  --ontology-root "$HOME/clawdbot-agents/main/memory/ontology"
```

Aplicar:
```bash
python3 {baseDir}/agent_memory_hygiene.py \
  --agents-root "$HOME/clawdbot-agents" \
  --obsidian "$HOME/Obsidian" \
  --ontology-root "$HOME/clawdbot-agents/main/memory/ontology" \
  --write
```

Validação extra (recomendada):
```bash
python3 {baseDir}/scripts/ontology.py validate \
  --graph "$HOME/clawdbot-agents/main/memory/ontology/graph.jsonl" \
  --schema "$HOME/clawdbot-agents/main/memory/ontology/schema.yaml"
```
## Segurança

- **Dry-run por padrão**: Sem `--write`, o script apenas exibe o que seria feito — nunca modifica arquivos diretamente
- **Sem deleção**: O script desloca e enriquece conteúdo; nunca apaga dados originais
- **Redação de segredos**: Antes de escrever no Obsidian, strings que parecem tokens ou senhas são redatadas automaticamente
- **Confirmação obrigatória**: O usuário deve inspecionar o dry-run antes de executar com `--write`
- **Backup recomendado**: Fazer commit ou backup do `MEMORY.md` antes de aplicar migrações em lote

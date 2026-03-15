---
title: Agent & Workspace MOC
description: Cluster de skills para manutenção, memória, governança e melhoria contínua de agentes e workspaces OpenClaw. Ponto de entrada para qualquer tarefa de saúde do agente.
updated: 2026-03-14
---

# Agent & Workspace

Cluster para manter os agentes saudáveis, a memória limpa e o workspace bem governado.

## Manutenção & Auditoria

- [[agent-maintenance]] — auditoria completa de workspaces: arquivos base, destinos de memória, path drift, consistência entre agentes
- [[avaliadora-workspace]] — avaliação profunda de sinergia: Obsidian ↔ prompts ↔ modelos ↔ crons; sempre pede confirmação antes de mudanças

## Memória & Higiene

- [[agent-memory-hygiene]] — refatora MEMORY.md, migra runbooks para TOOLS.md e normaliza entradas na Ontology
- [[process-vault-frontmatters]] — varre o vault Obsidian e garante YAML frontmatter (`title`, `summary`, `processedAt`) em todas as notas

## Melhoria Contínua

- [[self-improvement]] — captura erros, correções e aprendizados para melhoria contínua do agente
  - Triggers: comando falha inesperadamente, usuário corrige o agente, capacidade inexistente solicitada, API falha, abordagem melhor descoberta

## Arquitetura de Memória (referência rápida)

```
~/Obsidian/          ← memória durável COMPARTILHADA com Ramir
memory/              ← self-notes do agente (operacional, temporário)
MEMORY.md            ← índice de governança (não destino de conhecimento)
TOOLS.md             ← runbooks, notas de ferramentas
```

**Regra**: conhecimento novo → `~/Obsidian`. Nota operacional → `memory/`. Nunca misturar.

## Fluxo de Manutenção Periódica

```
agent-maintenance
  → detecta drift/problemas
  → agent-memory-hygiene (limpar MEMORY.md)
  → process-vault-frontmatters (normalizar vault)
  → self-improvement (registrar aprendizados)
```

## Fluxo de Auditoria Profunda

```
avaliadora-workspace
  → análise de sinergia completa
  → proposta de correções (com confirmação)
  → agent-maintenance (executar)
```

## Relacionados

- Para segurança do agente → [[../security/MOC]]
- Para criar/melhorar skills → [[../meta/MOC]]
- Para vault Obsidian → [[../integrations/MOC]]

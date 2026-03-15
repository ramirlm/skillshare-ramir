---
title: agent-maintenance
description: Auditar e normalizar workspaces OpenClaw. Detecta arquivos base faltando, destinos de memória incorretos, path drift e inconsistências entre agentes.
updated: 2026-03-14
---

# agent-maintenance

Auditoria e normalização de workspaces de agentes.

## O que verifica

- Arquivos base presentes: `MEMORY.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `TOOLS.md`
- Memória durável apontando para `~/Obsidian` (não para caminhos deprecated)
- `memory/` usado apenas para self-notes operacionais
- Consistência entre múltiplos agentes no mesmo workspace

## Triggers típicos

- Após criar novo agente
- Periodicamente (manutenção preventiva)
- Quando agente começa a se comportar de forma inconsistente
- Antes de auditoria profunda com [[avaliadora-workspace]]

## Relacionados

- Para limpar MEMORY.md → [[agent-memory-hygiene]]
- Para auditoria profunda → [[avaliadora-workspace]]
- Para normalizar vault → [[process-vault-frontmatters]]

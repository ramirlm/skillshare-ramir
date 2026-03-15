---
title: Gestão de Tarefas
description: Rastrear tarefas, logar progresso e manter contexto entre sessões com td-task-management e todo-list-manager.
updated: 2026-03-14
---

# Gestão de Tarefas

## td-task-management

Rastreamento de tarefas para agentes de IA entre context windows.

**Casos de uso:**
- Trabalho que atravessa múltiplas sessões
- Handoff de estado entre sessões
- Log de progresso em issues/PRDs
- Single-issue focus ou multi-issue work sessions

**Essencial quando:** contexto reseta e o trabalho continua.

## todo-list-manager

Listas TODO organizadas pelas áreas de vida prioritárias do Ramir:

| # | Área |
|---|------|
| 1 | 🙏 Deus / Igreja |
| 2 | 👨‍👩‍👧 Família |
| 3 | 💼 Trabalho |
| 4 | 🏠 Casa |
| 5 | 🎯 Lazer |

Inclui marcação de eventos no calendário e visão geral dos compromissos.

## Quando usar qual

| Cenário | Skill |
|---------|-------|
| Tarefa técnica/projeto multi-sessão | `td-task-management` |
| Lista de vida pessoal e compromissos | `todo-list-manager` |

## Relacionados

- Para tasks de PRD → [[prd]]
- Para handoff de contexto → `memory/` (self-notes do agente)

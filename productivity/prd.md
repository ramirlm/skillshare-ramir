---
title: prd + prd-executor
description: Criar PRDs estruturados e executar as tasks em nós locais ou remotos com agentes de código.
updated: 2026-03-14
---

# PRD → Execução

Dupla que fecha o ciclo planejamento → entrega.

## prd (criar)

Gera PRDs com:
- User stories estruturadas
- Critérios de aceitação
- Especificação de features para agentes ou desenvolvedores humanos

**Quando usar:** após [[brainstorming]] ou [[reuniao-para-prd]], quando há clareza suficiente para formalizar.

## prd-executor (executar)

Executa tasks do PRD com coding agents.

```
/prd-executor [arquivo.prd] [--node local|remote] [--watch]
```

- Despacha tasks para nós Mac/Linux
- Monitora jobs de coding agent de longa duração
- Valida trabalho concluído em múltiplos targets

**Quando usar:** após PRD criado e revisado, pronto para execução.

## Fluxo

```
brainstorming → prd → revisão → prd-executor → ../dev/coding-agent
```

## Relacionados

- Para ideação antes → [[brainstorming]]
- Para reunião como input → [[reuniao-para-prd]]
- Para rastrear progresso → [[td-task-management]]

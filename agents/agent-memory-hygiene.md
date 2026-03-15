---
title: agent-memory-hygiene
description: Refatorar MEMORY.md dos agentes, migrar runbooks para TOOLS.md e normalizar entradas na Ontology.
updated: 2026-03-14
---

# agent-memory-hygiene

Limpa e refatora a camada de memória dos agentes de forma proativa.

## O que faz

1. Varre `MEMORY.md` e identifica conteúdo que não deveria estar lá
2. Migra runbooks e tool-notes para `TOOLS.md`
3. Migra conhecimento durável para `~/Obsidian`
4. Normaliza entradas na Ontology

## Destinos corretos

| Tipo de conteúdo | Destino |
|-----------------|---------|
| Fatos sobre Ramir, decisões, projetos | `~/Obsidian` |
| Notas operacionais do agente | `memory/` |
| Runbooks e instruções de ferramentas | `TOOLS.md` |
| Índice de governança | `MEMORY.md` |

## Requer

- `python3`

## Relacionados

- Para auditoria do workspace → [[agent-maintenance]]
- Para frontmatters do vault → [[process-vault-frontmatters]]

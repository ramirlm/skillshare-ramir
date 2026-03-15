---
title: process-vault-frontmatters
description: Varrer o vault Obsidian e garantir YAML frontmatter correto (title, summary, processedAt) em todas as notas.
updated: 2026-03-14
---

# process-vault-frontmatters

Normaliza o vault `~/Obsidian` garantindo que todas as notas tenham frontmatter YAML adequado.

## O que faz

- Varre `~/Obsidian` recursivamente
- Adiciona/atualiza `title`, `summary`, `processedAt` em cada nota
- Evita reprocessamento com `processedAt`

## Quando usar

- Após importar notas em massa (ex: Readwise sync)
- Manutenção periódica do vault
- Antes de busca semântica no vault

## Requer

- `python3`

## Relacionados

- Para sync Readwise → Obsidian → [[../integrations/MOC]] (notion-readwise-sync)
- Para higiene de memória → [[agent-memory-hygiene]]

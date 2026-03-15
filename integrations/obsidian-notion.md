---
title: Notion + Readwise → Obsidian
description: Notion API para páginas/databases e sync Readwise Library para o vault Obsidian.
updated: 2026-03-14
---

# Notion & Obsidian

## notion (API)

Criar e gerenciar páginas, databases e blocos via Notion API.

**Casos de uso:**
- Criar página de projeto no Notion
- Atualizar database com resultados
- Ler blocos de uma página para processar

Requer: `NOTION_API_KEY` (integration token)

## notion-readwise-sync

Sync READ-ONLY da Readwise Library (database dentro de uma página Readwise no Notion) → vault `~/Obsidian`.

**O que sincroniza:** Books, PDFs, Videos, Articles, Podcasts
**O que ignora:** Tweets
**Output:** notas Markdown com frontmatter ontology-ready

**Quando rodar:**
- Cron periódico (automatizado)
- Manual após leitura importante no Readwise

**Após sync:** rodar [[../agents/process-vault-frontmatters]] para garantir frontmatter completo.

## Relacionados

- Para normalizar vault depois → [[../agents/process-vault-frontmatters]]
- Para buscar no vault → [[../research/MOC]] (qmd)

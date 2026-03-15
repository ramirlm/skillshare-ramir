---
title: Integrações Externas MOC
description: Cluster de skills para APIs e serviços externos — Notion, Obsidian, email, Twitter/X, 1Password e manutenção do OpenClaw.
updated: 2026-03-14
---

# Integrações Externas

Cluster de conexões com serviços externos. Cada nó é uma ponte entre o agente e um serviço específico.

## Conhecimento & Vault

- [[obsidian-notion]] — Notion API (páginas, databases, blocos) + sync Readwise → Obsidian
  - `notion` — criar/gerenciar páginas e databases via Notion API
  - `notion-readwise-sync` — sync READ-ONLY Readwise Library → vault Obsidian
    - Prioridade: Books, PDFs, Videos, Articles, Podcasts (ignora Tweets)
    - Designed para cron + runs manuais

## Comunicação

- [[email]] — enviar, ler, buscar e organizar emails em múltiplos provedores
  - Requer: `curl`, `jq`
- [[twitter]] — postar tweets, ler timeline, gerenciar seguidores, analisar engajamento
  - Requer: `TWITTER_API_KEY`
  - Para busca avançada no X → [[../research/grok]]

## Segurança de Credenciais

- [[1password]] — CLI `op` para ler, injetar e usar secrets do 1Password
  - Setup: instalar CLI + integração com desktop app + signin

## Manutenção do OpenClaw

- [[update-plus]] — backup + update + restore do OpenClaw com rollback automático
  - v4.0.1 | Requer: `git`, `jq`, `rsync`
  - Usar antes de qualquer update crítico do sistema

## Fluxos Comuns

### Leitura → Vault
```
notion-readwise-sync (importar) → ../agents/process-vault-frontmatters (normalizar)
```

### Publicar conteúdo de marketing
```
../marketing/copywriting → twitter (publicar) → ../marketing/analise-engajamento
```

### Notificação por email
```
../productivity/prd-executor → email (notificar resultado)
```

### Update seguro
```
update-plus (backup) → update → verificar → update-plus (rollback se necessário)
```

## Relacionados

- Para persistir no vault → [[../agents/MOC]]
- Para análise de engajamento Twitter → [[../marketing/MOC]]
- Para busca no X → [[../research/grok]]
- Para segurança → [[../security/MOC]]

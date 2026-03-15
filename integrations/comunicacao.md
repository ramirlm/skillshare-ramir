---
title: Email + Twitter
description: Comunicação via email (multi-provider) e Twitter/X (posts, timeline, engajamento).
updated: 2026-03-14
---

# Comunicação

## email

Enviar, ler, buscar e organizar emails em múltiplos provedores.

**Requer:** `curl`, `jq`

Casos de uso:
- Notificações de resultados de tasks
- Resumos automáticos (ex: daily-security-triage)
- Envio de relatórios gerados pelo agente

## twitter

Integração completa com X/Twitter.

**Requer:** `TWITTER_API_KEY`

Capacidades:
- Postar tweets e threads
- Ler timeline
- Gerenciar seguidores
- Analisar engajamento básico

**Para busca avançada no X:** usar [[../research/grok]] (grok-search)
**Para análise de engajamento:** ver [[../marketing/analise-engajamento]]

## Fluxo de publicação de conteúdo

```
../marketing/copywriting → (revisar) → twitter (publicar) → 72h → ../marketing/analise-engajamento
```

## Relacionados

- Para conteúdo antes de publicar → [[../marketing/MOC]]
- Para busca no X → [[../research/grok]]

---
title: skill-evaluator
description: Avaliar qualidade e publish-readiness de skills antes de publicar. 25 critérios com rubrica multi-framework.
updated: 2026-03-14
---

# skill-evaluator

Garante que skills atendam padrões de qualidade antes de ir a produção ou clawhub.

## Rubrica

- **ISO 25010** — qualidade de software
- **OpenSSF** — segurança open source
- **Shneiderman** — usabilidade
- **Heurísticas de agente** — específicas para AI skills

Total: **25 critérios** com checks automatizados + avaliação manual guiada.

## Quando usar

- Antes de publicar no `clawhub`
- Ao revisar skill existente que começou a falhar
- Como parte do fluxo `skill-creator → skill-evaluator → clawhub`

## O que verifica

- Frontmatter (name, description completos e precisos)
- Estrutura de diretório correta
- Referências funcionais (sem links quebrados)
- Descrição adequada para triggering
- Progressive disclosure implementado corretamente
- Scripts testados e funcionais

## Relacionados

- Para criar antes → [[skill-creator]]
- Para publicar depois → [[clawhub]]

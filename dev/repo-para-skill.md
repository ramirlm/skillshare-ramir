---
title: repo-para-skill
description: Converter qualquer repositório GitHub público em skill reutilizável do Clawdbot.
updated: 2026-03-14
---

# repo-para-skill

Transforma um repo em skill estruturada com references, SKILL.md e metadata.

## Fluxo

```
1. Informar URL do repo
2. repo-para-skill clona e extrai arquitetura
3. Gera references/ com docs relevantes
4. Cria SKILL.md com frontmatter e instruções
5. → ../meta/MOC para avaliar e publicar
```

## Quando usar

- Você usa um repo repetidamente e quer que o agente conheça bem
- Quer transformar ferramenta externa em skill gerenciável
- Precisa de contexto profundo sem carregar o repo todo no contexto

## Relacionados

- Para inspecionar antes → [[opensrc-fetch]]
- Para avaliar a skill gerada → [[../meta/MOC]]
- Para publicar → clawhub

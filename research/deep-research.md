---
title: deep-research + perplexity-brainstorm
description: Pesquisa profunda multi-etapa e fluxo combinado de pesquisa + ideação para temas complexos.
updated: 2026-03-14
---

# Pesquisa Profunda

## deep-research

Agente especializado em pesquisa complexa com planejamento e decomposição.

**Quando usar:** tema que exige múltiplos passos, fontes variadas e raciocínio de longo contexto.

Exemplos: "como funciona o mercado X no Brasil", "quais as tendências de Y para 2025", "comparação completa entre A e B".

## perplexity-brainstorm

Pesquisa profunda + ideação estruturada em sequência automática.

**Triggers:** "research and brainstorm X", "deep dive em Y", "explorar Z de forma completa"

**Fluxo interno:**
```
Perplexity (pesquisa) → síntese → brainstorming estruturado → iteração com web_search
```

**Quando preferir sobre deep-research:** quando o objetivo final é gerar ideias, não só entender o tema.

## Escolha rápida

| Objetivo | Skill |
|----------|-------|
| Entender um tema a fundo | `deep-research` |
| Entender + gerar ideias | `perplexity-brainstorm` |
| Resposta rápida | `perplexity` |

## Relacionados

- Para formalizar as ideias → [[../productivity/brainstorming]] → [[../productivity/prd]]
- Para marketing → [[../marketing/temas-recorrentes]]

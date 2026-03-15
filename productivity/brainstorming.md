---
title: brainstorming + council
description: Ideação estruturada antes de implementar e feedback multi-perspectiva para decisões críticas.
updated: 2026-03-14
---

# Ideação & Decisão

## brainstorming

⚠️ **Obrigatório antes de qualquer trabalho criativo.**

Explora intenção, requisitos e design **antes** de implementar features, componentes ou mudanças.

Evita o erro clássico: construir a coisa errada com excelência.

**Triggers:** criar feature, adicionar componente, modificar comportamento, planejar campanha.

## council (Council of the Wise)

Envia uma ideia para sub-agentes com perspectivas diferentes e consolida feedback.

Auto-descobre personas de agentes na pasta `agents/`.

**Quando usar:**
- Decisão crítica com múltiplos ângulos possíveis
- Quando uma única perspectiva é insuficiente
- Antes de comprometer com uma direção estratégica

**Como usar:**
```
/council "Ideia ou decisão aqui"
```

## Fluxo recomendado

```
brainstorming (explorar)
  → council (se decisão crítica, pedir perspectivas)
  → prd (formalizar)
```

## Relacionados

- Para formalizar depois → [[prd]]
- Para pesquisa de contexto → [[../research/MOC]]

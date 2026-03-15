---
title: Produtividade & Projetos MOC
description: Cluster de skills para PRDs, reuniões, tarefas e fluxos de trabalho estruturados. Ponto de entrada para qualquer tarefa de planejamento, execução e organização.
updated: 2026-03-14
---

# Produtividade & Projetos

Cluster para transformar ideias e reuniões em entregas concretas.

## Reuniões → Conhecimento

- [[reuniao-para-prd]] — transcrição de reunião → insights + desafios + PRD opcional
  - Melhor ponto de entrada quando vem de uma reunião gravada ou colada no chat
- [[ontologia-transcript]] — transcrição → resumo + ontologia + persistência no vault Obsidian
  - Usar quando o objetivo é preservar o conhecimento da reunião, não só o PRD

**Fluxo recomendado:**
```
Transcrição colada
  → reuniao-para-prd (insights + PRD)
  → ontologia-transcript (salvar no vault)
```

## PRD → Execução

- [[prd]] — criar e gerenciar PRDs com user stories e critérios de aceitação
- [[prd-executor]] — executar tasks de PRD em nós locais ou remotos, monitorar jobs de coding agent

**Fluxo:**
```
prd (criar) → prd-executor (executar) → ../dev/MOC (coding-agent)
```

## Ideação & Decisão

- [[brainstorming]] — explorar intenção, requisitos e design **antes** de qualquer implementação
  - ⚠️ Obrigatório antes de trabalho criativo (features, componentes, mudanças de comportamento)
- [[council]] — enviar ideia para o Council of the Wise: feedback multi-perspectiva via sub-agentes
  - Ideal para decisões importantes que precisam de ângulos diferentes

## Gestão de Tarefas

- [[td-task-management]] — rastrear trabalho, logar progresso e fazer handoff de estado entre sessões
  - Essencial para tarefas que atravessam múltiplos contextos
- [[todo-list-manager]] — listas TODO organizadas por áreas de vida
  - Categorias: 1-Deus/Igreja, 2-Família, 3-Trabalho, 4-Casa, 5-Lazer

## Síntese & Resumo

- [[summarize]] — resumir URLs, podcasts, arquivos locais, transcrições de YouTube/vídeo
- [[resumidor-auto]] — resumir conteúdo enviado + salvar automaticamente no Obsidian
- [[napkin]] — runbook por repositório, curado continuamente (ativar a cada sessão)

## Fluxos Completos

### Reunião → Ação
```
Transcrição → reuniao-para-prd → prd → td-task-management → prd-executor
```

### Ideia → Decisão → Execução
```
brainstorming → council (se decisão crítica) → prd → prd-executor
```

### Conteúdo externo → Conhecimento
```
summarize → resumidor-auto → ../agents/process-vault-frontmatters
```

## Relacionados

- Para execução de código → [[../dev/MOC]]
- Para pesquisa antes de planejar → [[../research/MOC]]
- Para persistir no vault → [[../agents/MOC]] (process-vault-frontmatters)

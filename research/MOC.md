---
title: Pesquisa & Conhecimento MOC
description: Cluster de skills para busca web, síntese de conteúdo e gestão do conhecimento. Ponto de entrada para qualquer tarefa de pesquisa, tendências ou aprendizado.
updated: 2026-03-14
---

# Pesquisa & Conhecimento

Cluster para encontrar informação, sintetizar e transformar em conhecimento durável.

## Busca Web

- [[perplexity]] — respostas com IA + citações via Perplexity API; suporta batch queries
  - Requer: `PERPLEXITY_API_KEY`
  - Melhor para: resposta rápida fundamentada com fontes
- [[grok-search]] — busca em X/Twitter e web via xAI Grok (`web_search`, `x_search`)
  - Melhor para: tweets, threads, usuários do X; alternativa ao Brave
  - Retorna JSON estruturado + citações
- [[xai]] — modelos Grok completos (Grok-3, Grok-3-mini, visão) para análise e raciocínio profundo
  - Quando Grok como modelo > Grok como ferramenta de busca

## Pesquisa Profunda

- [[deep-research]] — agente especializado em pesquisa multi-etapa com planejamento e decomposição
  - Usar para temas complexos que exigem raciocínio de longo contexto
- [[perplexity-brainstorm]] — pesquisa profunda + ideação estruturada em um fluxo
  - Triggers: "research and brainstorm X", "deep dive em Y", "explorar Z"
  - Combina Perplexity + brainstorming iterativo

## Documentação Técnica

- [[context7]] — docs atualizadas de bibliotecas e frameworks via Context7 API
  - Usar sempre que precisar de docs de código que podem ter mudado desde o treino
  - Ver também [[../dev/MOC]]

## Conteúdo & Mídia

- [[youtube-transcript]] — transcrever e resumir vídeos YouTube (proxy residencial incluso)
- [[blogwatcher]] — monitorar blogs e feeds RSS/Atom em tempo real
  - Requer: `blogwatcher` CLI (install via go)

## Aprendizado de Longo Prazo

- [[leitura-espacada]] — sistema de repetição espaçada com algoritmo SM-2
  - Criar cards de estudo, revisões diárias, organizar por temas
  - Usar para transformar pesquisa em conhecimento retido

## Quando usar qual

| Necessidade | Skill |
|-------------|-------|
| Resposta rápida com fonte | `perplexity` |
| Tweets / discussões no X | `grok-search` |
| Análise profunda com Grok | `xai` |
| Tema complexo multi-etapa | `deep-research` |
| Pesquisa + ideação junto | `perplexity-brainstorm` |
| Docs de código | `context7` |
| Vídeo YouTube | `youtube-transcript` |
| Monitorar blog/RSS | `blogwatcher` |
| Aprender e reter | `leitura-espacada` |

## Fluxos Comuns

### Tendência de marketing
```
grok-search (X/Twitter) → perplexity (validar) → ../marketing/temas-recorrentes
```

### Pesquisa antes de PRD
```
deep-research → perplexity-brainstorm → ../productivity/prd
```

### Aprender nova ferramenta
```
context7 (docs) → leitura-espacada (reter) → ../agents/self-improvement
```

### Monitoramento contínuo
```
blogwatcher (feeds) → resumidor-auto → ../agents/process-vault-frontmatters
```

## Relacionados

- Para marketing com tendências → [[../marketing/MOC]]
- Para ideação após pesquisa → [[../productivity/MOC]]
- Para persistir no vault → [[../agents/MOC]]

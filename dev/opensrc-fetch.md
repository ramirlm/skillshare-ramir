---
title: opensrc-fetch
description: Buscar código-fonte de pacotes npm e repositórios GitHub públicos para dar contexto profundo a agentes de código.
updated: 2026-03-14
---

# opensrc-fetch

Injeta código-fonte real no contexto — vai além de type definitions.

## Quando usar

- Tarefa de código precisa inspecionar implementação de uma dependência
- Documentação é insuficiente ou desatualizada
- Onboarding rápido em internals de um pacote
- Antes de usar [[coding-agent]] em codebase desconhecido

## Uso

```bash
opensrc-fetch <pacote-npm>
opensrc-fetch <owner/repo>
```

Retorna: código-fonte estruturado, arquivos relevantes, padrões de uso.

## Relacionados

- Para transformar repo em skill → [[repo-para-skill]]
- Para docs atualizadas → [[../research/MOC]] (context7)
- Para codificar depois → [[coding-agent]]

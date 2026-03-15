---
title: coding-agent
description: Delegar tarefas de código para Codex, Claude Code ou Pi em processo background. Para construção de features, revisão de PRs e refatoração.
updated: 2026-03-14
---

# coding-agent

Spawna agentes de código em background para tarefas que precisam explorar arquivos, iterar e escrever código.

## Quando usar

✅ Criar/construir novas features ou apps
✅ Revisar PRs (spawnar em diretório temporário)
✅ Refatorar codebases grandes
✅ Coding iterativo que precisa explorar arquivos

❌ Não usar para: edições simples de 1 linha → usar `edit` diretamente
❌ Não usar para: apenas ler código → usar `read`
❌ Não usar para: sessões ACP em thread de chat → usar `sessions_spawn` com `runtime:"acp"`
❌ Não usar para: trabalho em `~/clawd` workspace

## Requer

- PTY: `pty: true` no bash tool
- Pelo menos um de: `claude`, `codex`, `opencode`, `pi`

## Relacionados

- Para inspecionar dependências antes → [[opensrc-fetch]]
- Para automação de browser junto → [[playwright]]
- Para abrir PR depois → [[github]]

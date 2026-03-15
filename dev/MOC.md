---
title: Dev & Automação MOC
description: Cluster de skills para desenvolvimento, automação de browser, GitHub, terminal e tarefas técnicas. Ponto de entrada para qualquer fluxo de código ou automação.
updated: 2026-03-14
---

# Dev & Automação

Cluster de skills técnicas interconectadas. Siga apenas os nós relevantes para a tarefa.

## Agentes de Código

- [[coding-agent]] — delegar tarefas de código para Codex, Claude Code ou Pi via processo background
  - Use para: criar features, revisar PRs, refatorar codebases
  - Não usar para: edições simples de 1 linha, leitura de código, sessões ACP em thread de chat

## Browser & Automação Web

- [[playwright]] — automação de browser (abrir páginas, interagir, screenshots)
  - [[playwright-auth]] — salvar autenticação uma vez, reutilizar sempre (Twitter, LinkedIn, etc.)
  - Para browser headless simples → `agent-browser` (ver [[../agents/MOC]])

## GitHub & Versionamento

- [[github]] — operações via `gh` CLI: issues, PRs, CI runs, code review
  - Requer: `gh` CLI configurado com auth
- [[gh-issues]] — buscar issues, spawnar sub-agentes para implementar fixes e abrir PRs
  - Uso avançado: `--watch`, `--cron`, `--model`, `--notify-channel`
- [[gog]] — Google Workspace (Gmail, Calendar, Drive, Sheets, Docs) via CLI

## Terminal & Sessões

- [[tmux]] — controlar sessões tmux remotamente, enviar keystrokes, scraper output de pane
- [[parallel-task]] — executar múltiplas tarefas em paralelo (apenas via `/parallel-task`)

## Inspeção de Código & Docs

- [[opensrc-fetch]] — buscar código-fonte de pacotes npm e repos GitHub para contexto profundo
- [[context7]] — documentação atualizada de bibliotecas/frameworks (ver também [[../research/MOC]])
- [[qmd]] — busca híbrida local em notas markdown e docs indexados

## Construção de Skills

- [[repo-para-skill]] — converter qualquer repositório GitHub em skill reutilizável
  - Fluxo: clone → extrair arquitetura → gerar references → packager
  - Continuar em [[../meta/MOC]] para publicar

## Protocolos & MCPs

- [[mcporter]] — listar, configurar, autenticar e chamar MCP servers/tools (HTTP ou stdio)

## Fluxos Comuns

### Nova feature em repositório existente
```
github (checar PRs/issues) → coding-agent (implementar) → github (abrir PR)
```

### Automação web com login
```
playwright-auth (salvar sessão) → playwright (executar automação)
```

### Converter repo em skill
```
opensrc-fetch (inspecionar) → repo-para-skill (gerar skill) → ../meta/MOC (publicar)
```

## Relacionados

- Para skills e meta → [[../meta/MOC]]
- Para segurança → [[../security/MOC]]
- Para pesquisa de docs → [[../research/MOC]]

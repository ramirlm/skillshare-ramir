---
title: Playwright (Browser Automation)
description: Automação de browser via Playwright CLI — abrir páginas, interagir com elementos, screenshots, testes.
updated: 2026-03-14
---

# Playwright

Automação headless de browser para tarefas que precisam de interação real com páginas web.

## playwright-cli

CLI para automação via Playwright. Instalar: `npm install -g @playwright/mcp`

Usar para:
- Abrir páginas e capturar conteúdo
- Clicar em elementos, preencher formulários
- Tirar screenshots
- Workflows de teste automatizado

## playwright-auth

Salvar autenticação uma vez → reutilizar sempre.

```bash
# Salvar sessão autenticada
playwright-auth save --site twitter.com

# Usar sessão salva
playwright-auth use --site twitter.com
```

Suporta: Twitter, LinkedIn, Facebook e qualquer site com login.

## Quando usar vs. agent-browser

| | playwright | agent-browser |
|--|-----------|--------------|
| Snapshots de acessibilidade | ✅ | ✅ |
| Auth persistente | ✅ | ❌ |
| Testes automatizados | ✅ | ❌ |
| Uso simples/pontual | — | ✅ mais simples |

## Relacionados

- Para sessões de terminal → [[tmux]]
- Para automação com coding → [[coding-agent]]

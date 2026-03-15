---
title: daily-security-triage
description: Triagem diária de segurança local — shell profile injection, indicadores de persistência — com resumo por email.
updated: 2026-03-14
---

# daily-security-triage

Varredura diária de indicadores de comprometimento no sistema local.

## O que verifica

- Shell profile injection (`.bashrc`, `.zshrc`, etc.)
- Indicadores comuns de persistência
- Processos e conexões suspeitas

## Output

Resumo por email com tudo que foi encontrado.

## Como usar

Rodar manualmente ou via cron diário:
```
daily-security-triage
```

## Relacionados

- Para ameaças externas → [[defesa]] (moltthreats)
- Para notificação → [[../integrations/comunicacao]] (email)

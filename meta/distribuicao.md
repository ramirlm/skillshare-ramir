---
title: clawhub + skills-manager + skillshare
description: Distribuir, sincronizar e gerenciar skills instaladas via clawhub CLI, preset manager e skillshare.
updated: 2026-03-14
---

# Distribuição & Gerenciamento

## clawhub

CLI para o ecossistema clawhub.com.

```bash
clawhub search <termo>          # descobrir skills
clawhub install <skill>         # instalar skill
clawhub update                  # atualizar todas
clawhub publish <pasta>         # publicar skill
```

Instalar CLI: `npm install -g clawhub`

## skills-manager

Gerencia qual conjunto de skills está ativo por máquina ou projeto.

- Preset único como fonte de verdade (arquivo local ou Gist)
- Ativar/desativar por contexto
- Útil para manter sets diferentes: pessoal vs. trabalho vs. projeto específico

## skillshare (v0.16.2)

Sincroniza skills entre ferramentas AI CLI a partir de uma única fonte.

Quando usar: ambiente com múltiplas ferramentas (Codex, Claude Code, etc.) que precisam das mesmas skills.

## Relacionados

- Para criar skill para publicar → [[skill-creator]] → [[skill-evaluator]]
- Para descobrir novas skills → [[find-skills]]

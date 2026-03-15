---
title: skill-creator
description: Criar skills do zero ou melhorar skills existentes. Fluxo completo de 6 passos.
updated: 2026-03-14
---

# skill-creator

A skill que cria skills. Usar para qualquer trabalho no próprio skill graph.

## Fluxo de 6 passos

```
1. Entender → exemplos concretos de uso
2. Planejar → scripts, references, assets necessários
3. Inicializar → init_skill.py (sempre para skills novas)
4. Editar → SKILL.md + recursos
5. Empacotar → package_skill.py (valida + gera .skill)
6. Iterar → testar em uso real, ajustar
```

## Localização correta

```
~/clawdbot-skills/[nome-da-skill]/SKILL.md
```

⚠️ **Nunca** criar em `~/.agents/skills/` ou outros caminhos.

## Anatomia de uma skill

```
nome-da-skill/
├── SKILL.md          ← obrigatório (frontmatter + instruções)
├── scripts/          ← código executável
├── references/       ← docs carregados conforme necessário
└── assets/           ← arquivos de output (templates, imagens)
```

## Princípio chave: Progressive Disclosure

```
Frontmatter (descrição) → sempre no contexto
SKILL.md body → carregado quando skill dispara
references/ → carregados conforme necessário
```

## Relacionados

- Para avaliar depois → [[skill-evaluator]]
- Para publicar → [[clawhub]]
- Para o skill graph → [[MOC]]

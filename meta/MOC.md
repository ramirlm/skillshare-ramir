---
title: Skills Management (Meta) MOC
description: Cluster para criar, avaliar, distribuir e gerenciar o próprio skill graph. Ponto de entrada quando o objetivo é trabalhar nas skills em si — não usá-las.
updated: 2026-03-14
---

# Skills Management (Meta)

O cluster que cuida de todos os outros. Usar quando o objetivo é criar, melhorar, avaliar ou distribuir skills.

## Descoberta

- [[find-skills]] — descobrir skills quando o usuário pergunta "tem skill para X?" ou quer estender capacidades
  - Triggers: "como faço X", "tem skill para...", "quero estender..."
- [[clawhub]] — buscar, instalar e atualizar skills via CLI do clawhub.com
  - `clawhub search <termo>` / `clawhub install <skill>` / `clawhub update`

## Criação

- [[skill-creator]] — criar skills do zero ou melhorar skills existentes
  - Fluxo completo: entender → planejar → inicializar → editar → empacotar
  - Inclui: scripts, references, assets
  - **Este skill graph foi criado usando skill-creator como referência**

## Avaliação & Qualidade

- [[skill-evaluator]] — avaliar skills antes de publicar
  - Rubrica: ISO 25010, OpenSSF, Shneiderman + heurísticas de agente
  - 25 critérios, checks automatizados + avaliação manual
  - Usar antes de qualquer publicação no clawhub

## Gerenciamento & Sync

- [[skills-manager]] — instalar, ativar e desativar skills por preset (local ou Gist)
  - Mapeamento por máquina e por projeto
- [[skillshare]] — sincronizar skills entre ferramentas AI CLI a partir de uma fonte única
  - Versão atual: v0.16.2

## Skill Graph (este repositório)

O INDEX.md + MOCs em `~/clawdbot-skills/` **é** o skill graph do Ramir.

### Como expandir o grafo

1. Identificar padrão recorrente ou novo domínio
2. `skill-creator` → criar skill no cluster adequado
3. Adicionar wikilink em prosa no MOC do cluster
4. Atualizar `INDEX.md` se for novo cluster
5. `skill-evaluator` → avaliar qualidade
6. `clawhub publish` → distribuir (opcional)

### Convenções do grafo

- Todo nó tem `yaml frontmatter` com `title` e `description`
- Wikilinks sempre **em prosa**, não em listas soltas
- MOCs têm fluxos documentados com `→`
- Links cross-cluster: `[[../outro-cluster/MOC]]`

## Fluxo Completo de Nova Skill

```
find-skills (verificar se já existe)
  → skill-creator (criar)
  → skill-evaluator (avaliar)
  → clawhub publish (distribuir)
  → skills-manager (ativar no preset)
```

## Relacionados

- Para criar skill de um repo → [[../dev/MOC]] (repo-para-skill)
- Para manutenção das skills → [[../agents/MOC]]

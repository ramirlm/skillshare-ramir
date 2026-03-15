---
name: process-vault-frontmatters
description: Varre o vault do Obsidian e garante YAML frontmatter (title, summary) e atualiza processedAt para evitar reprocessamento.
metadata: {"clawdbot":{"emoji":"🗂️","os":["linux"],"requires":{"bins":["python3"]}}}
---

# /process-vault-frontmatters

Skill para padronizar e manter metadados em notas Markdown do vault do Obsidian.

## O que faz

- Varre `~/Obsidian` (recursivo) procurando `**/*.md`.
- Para cada nota:
  - Se não existir YAML frontmatter, cria.
  - Garante os campos:
    - `title`: derivado do nome do arquivo (stem)
    - `summary`: derivado do conteúdo (primeiro parágrafo útil)
    - `processedAt`: timestamp ISO com timezone (America/Fortaleza)
    - `owner`: `ramir` (padrão — proprietário do vault)
    - `people`, `projects`, `related`, `topics`: listas vazias `[]` se ausentes
- Evita retrabalho:
  - Se `processedAt` existir e o arquivo não foi modificado depois dele (mtime), e `title`/`summary` já existem → pula.

## Política de linking (obrigatória)

Ver `~/clawdbot-agents/main/memory/vault-linking-policy.md`.

- **NUNCA rodar `clawvault link --all`** — causa links espúrios em PT-BR
- Frontmatter semântico: `people`, `projects`, `related`, `owner: ramir`, `topics`
- Somente slugs de entidades que existam em `Obsidian/people/`, `Obsidian/projects/`, etc.

## Como executar (manual)

```bash
python3 /home/rlmit/clawdbot-skills/process-vault-frontmatters/process_vault_frontmatters.py --vault "$HOME/Obsidian" --write
```

## Flags

- `--vault <path>`: caminho do vault (default: `~/Obsidian`)
- `--write`: aplica alterações (sem isso roda em modo dry-run)
- `--limit N`: processa no máximo N arquivos (debug)

## Saída

- Imprime contagem de: processados, alterados, pulados, erros.

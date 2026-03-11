# Protocolo de geração de skill do repositório

## Campos obrigatórios gerados

- `SKILL.md` com frontmatter `name` e `description`
- `references/repo-overview.md`
- `references/file-index.md`
- `references/notes.md`
- `references/source.txt`

## Campos opcionais

- Cópia de docs úteis (README/CHANGELOG/LICENSE etc.) quando `--no-docs` não estiver ativo

## Decisões de design

1. Manter skill leve: evitar copiar o repositório inteiro.
2. Gerar índice curto de arquivos (padrão: 200) para dar visibilidade do que existe.
3. Registrar linguagem por inferência de extensões e arquivos de lock/manifest para orientar contexto de linguagem.
4. Marcar repositório não disponível na API com fallback seguro (sem quebra de fluxo).

## Pós-uso

- Se o repositório mudar muito, execute novamente para atualizar a skill.
- Para cenários de produção, revise `references/repo-overview.md` e ajuste comandos manualmente antes de aplicar mudanças críticas.

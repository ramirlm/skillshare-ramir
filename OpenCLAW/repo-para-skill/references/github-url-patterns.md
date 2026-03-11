# Padrões aceitos de repositório

Use apenas identificadores públicos do GitHub nos formatos:

- `owner/repo`
- `https://github.com/owner/repo`
- `http://github.com/owner/repo`
- `git@github.com:owner/repo.git`

São rejeitados:

- URLs que não forem GitHub
- GitHub Enterprise privados sem autenticação
- Repositórios privados

Dica:

- Para repositórios com nomes em camelCase ou com pontos/underscores, o nome gerado do skill vira **slug-kebab** automaticamente.
- Se você quiser forçar o nome, use `--skill-name <nome-da-skill>`.

---
title: GitHub
description: Operações GitHub via `gh` CLI e gh-issues com sub-agentes. Issues, PRs, CI, code review.
updated: 2026-03-14
---

# GitHub

## github (gh CLI)

Operações diretas via `gh` CLI.

```bash
gh pr list                     # listar PRs
gh pr view 42                  # ver PR
gh issue list --label bug      # issues por label
gh run list                    # CI runs
gh api /repos/owner/repo/...   # API raw
```

Requer: `gh auth login` configurado.

**Não usar para**: bulk operations em muitos repos (scriptar com `gh api`) ou UI flows complexos.

## gh-issues (avançado)

Busca issues, spawna sub-agentes para implementar fixes e abre PRs automaticamente.

```bash
/gh-issues owner/repo --label bug --limit 5
/gh-issues owner/repo --watch --interval 5    # monitorar continuamente
/gh-issues owner/repo --reviews-only          # só review comments
/gh-issues owner/repo --model glm-5           # modelo específico
```

Flags úteis: `--fork user/repo`, `--milestone v1.0`, `--dry-run`, `--cron`

## Fluxo completo

```
gh issue list → coding-agent (implementar) → gh pr create → gh-issues --reviews-only
```

## Relacionados

- Para implementar fixes → [[coding-agent]]
- Para inspecionar código da dep → [[opensrc-fetch]]

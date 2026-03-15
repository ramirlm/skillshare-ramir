# Standard templates for agent maintenance

Use these as the minimum normalized templates when a workspace is missing its governance files.

## MEMORY.md template

```md
# MEMORY.md - <Agent> Memory Policy

> **STATUS: índice de governança.** Este arquivo não é a memória durável canônica e não deve ser usado como destino de conhecimento.
>
> **Memória durável compartilhada:** `~/Obsidian`
> - Todo conhecimento que Ramir e o agente precisam lembrar no futuro deve ser salvo no vault principal `~/Obsidian`.
>
> **Notas do agente / self-notes:** `memory/`
> - Use para notas curtas operacionais do agente.
> - `memory/` **não é vault** e **não é memória compartilhada**.
>
> **Estado técnico:** `sessions/`, `agent/`, `.openclaw/`
> - Usar apenas para continuidade técnica/runtime.

## Regra semântica
- **Memória** = cérebro compartilhado com Ramir → `~/Obsidian`
- **Nota / self-note** = lembrete curto do agente → `memory/`
```

## SESSION-STATE.md template

```md
# SESSION-STATE.md

Estado operacional atual do agente <agent>.

## Regras rápidas
- Ler este arquivo no início de cada sessão.
- Registrar aqui apenas continuidade de trabalho, handoffs, checkpoints e decisões temporárias.
- Conhecimento durável compartilhado com Ramir deve ir para `~/Obsidian`.
- Self-notes curtas e operacionais podem ficar em `memory/`.

## Estado atual
- Inicializado para restaurar a disciplina de continuidade do agente.
- Sem contexto ativo consolidado neste momento.
```

## Required base files checklist

- `AGENTS.md`
- `SOUL.md`
- `MEMORY.md`
- `SESSION-STATE.md`
- `IDENTITY.md`
- `USER.md`

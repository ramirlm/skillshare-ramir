---
name: skills-manager
description: Gerencia instalação, ativação e desativação de skills do Clawdbot com base em um preset único (local ou Gist), com mapeamento por máquina e por projeto.
---

# skills-manager

Esta skill cria um único ponto de controle para skills.

## Quando usar
- Você quer instalar/remover skills de forma centralizada.
- Quer habilitar/desabilitar skills por projeto (ex.: `main`, `codi`, `primo`) e/ou máquina.
- Quer usar um arquivo único (ex.: no GitHub/Gist) como **preset**.

## Visão rápida
- `apply`: aplica o preset para o projeto/máquina atual.
- `enable` / `disable`: cria override local de ativação por projeto/máquina/global.
- `list`: mostra o estado esperado vs. instalado no `~/.openclaw/skills`.
- `export`: gera JSON com o estado final de skills (útil para commit em Gist).

## Comandos principais

```bash
python3 /home/rlmit/clawdbot-skills/skills-manager/scripts/skills_manager.py apply \
  --source <SEU_PRESET_JSON>

# Exemplo local
python3 /home/rlmit/clawdbot-skills/skills-manager/scripts/skills_manager.py apply --source ~/clawdbot-skills/presets/main.json

# Exemplo remoto (Gist)
python3 /home/rlmit/clawdbot-skills/skills-manager/scripts/skills_manager.py apply --source https://gist.githubusercontent.com/SEU_USUARIO/ID/raw/skills-preset.json

python3 /home/rlmit/clawdbot-skills/skills-manager/scripts/skills_manager.py list --source <SEU_PRESET_JSON>

python3 /home/rlmit/clawdbot-skills/skills-manager/scripts/skills_manager.py enable --scope project --project codi skill-x
python3 /home/rlmit/clawdbot-skills/skills-manager/scripts/skills_manager.py disable --scope project --project codi skill-y

python3 /home/rlmit/clawdbot-skills/skills-manager/scripts/skills_manager.py export --source <SEU_PRESET_JSON> --output /tmp/skills-active.json
```

## Flags úteis
- `--project`: slug do projeto (default: git repo atual).
- `--machine`: id da máquina (default: hostname).
- `--prune`: desativa skills extras já ativas, não declaradas no desired.
- `--dry-run`: simulação.
- `--save-state`: grava `~/.config/skills-manager/state.json`.

## Formato de preset

`global`, `machines` e `projects` aceitam:
- `enabled`: lista de skills ativas
- `disabled`: lista de skills desativadas

`skills` mapeia origem de cada skill:
- `type: path` -> `path`
- `type: git` -> `repo`, `subdir`, `branch`

Exemplo de preset em `references-preset-schema.json`.

## Segurança e operação
- O skill faz apenas link/rename em `~/.openclaw/skills`.
- Para desativar sem apagar pasta/arquivo real, usa extensão `.DISABLED`.
- O estado aplicado é idempotente: repetir `apply` mantém o mesmo resultado.

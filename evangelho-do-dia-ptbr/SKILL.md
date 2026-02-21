---
name: evangelho-do-dia-ptbr
description: Buscar o Evangelho do dia em PT-BR (com opcional reflexão) usando evangeli.net, por data (YYYY-MM-DD) ou hoje. Use quando o usuário pedir "evangelho do dia", "liturgia diária" (evangelho), "evangelho de hoje" ou quando precisar extrair o texto do Evangelho e/ou a reflexão para copiar, enviar, ou salvar.
---

# Evangelho do dia (PT-BR) — evangeli.net

## Quick start

- Hoje (tudo + reflexão):
  - `python3 scripts/fetch_evangelho.py`
- Uma data específica:
  - `python3 scripts/fetch_evangelho.py 2026-02-17`
- Somente Evangelho (sem leituras/salmo):
  - `python3 scripts/fetch_evangelho.py --somente-evangelho`
- Sem reflexão/comentário:
  - `python3 scripts/fetch_evangelho.py --sem-reflexao`

## O que entregar ao usuário

1) 1ª Leitura (quando existir)  
2) Salmo Responsorial (quando existir)  
3) 2ª Leitura (quando existir)  
4) Versículo antes do Evangelho (quando existir)  
5) Referência + texto do Evangelho (PT-BR)  
6) Reflexão/comentário + autor (por padrão)  
7) Link da fonte

## Workflow (agente)

1) Determinar a data (default: hoje em America/Fortaleza)
2) Executar `scripts/fetch_evangelho.py` (com ou sem `--reflexao`)
3) Retornar o Markdown gerado

## Notas de manutenção

- Detalhes da fonte/HTML em: `references/sources.md`
- Se o parser quebrar, ajustar regex/recortes em `scripts/fetch_evangelho.py`.

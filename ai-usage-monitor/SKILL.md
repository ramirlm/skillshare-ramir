---
name: ai-usage-monitor
description: Monitor usage and estimate consumption for AI tools with different billing cycles. Fetches real-time data when APIs are available. Use when user wants to (1) Check current usage of AI tools like Cursor, Codex, Copilot, Synthetic, or Warp, (2) Get estimates of remaining time/budget, (3) Log new usage data, (4) Generate usage reports, (5) Understand if they are on track with their AI tool consumption, or (6) Set up automated daily reports.
version: 1.0.0
author: ramirlm
triggers:
  - "uso de AI"
  - "consumo de IA"
  - "AI usage"
  - "check cursor usage"
  - "monitor AI"
metadata:
  clawdbot:
    emoji: "📊"
    os: ["linux", "darwin", "windows"]
---

# AI Usage Monitor

Monitora o uso e estima o consumo de ferramentas de IA com diferentes ciclos de cobrança.
Busca dados em tempo real quando APIs estão disponíveis.

## Ferramentas Suportadas

| Ferramenta | Custo | Dia | Janela | API |
|------------|-------|-----|--------|-----|
| Cursor | $20/mês | 10 | Mensal | CURSOR_API_KEY |
| Codex | $200 | 22 | 5h + Semanal | OPENAI_API_KEY |
| Copilot | $10/mês | 25 | Mensal | GITHUB_TOKEN |
| Synthetic | $20 | 17 | 5h + Semanal | SYNTHETIC_API_KEY |
| Warp | $20/mês | 12 | Mensal | WARP_API_KEY |

## APIs Disponíveis

A skill verifica automaticamente variáveis de ambiente:

- ✅ `OPENAI_API_KEY` - Para Codex
- 🔍 `GITHUB_TOKEN` - Para Copilot
- 🔍 `SYNTHETIC_API_KEY` - Para Synthetic
- 🔍 `WARP_API_KEY` - Para Warp
- 🔍 `CURSOR_API_KEY` - Para Cursor

**Nota:** APIs que não foram encontradas são reportadas no relatório com ⚠️.

## Uso Rápido

### Gerar relatório completo
```bash
python3 scripts/monitor.py --report
```

### Ver status das APIs
```bash
python3 scripts/monitor.py --apis
```

### Ver status de uma ferramenta específica
```bash
python3 scripts/monitor.py --tool synthetic
```

### Registrar uso manualmente
```bash
python3 scripts/monitor.py --log synthetic --usage 2.5 --unit hours
```

### Usar via Python
```python
from scripts.monitor import AIUsageMonitor

monitor = AIUsageMonitor()

# Logar uso manual
monitor.log_usage('synthetic', 3.0, 'hours', 'Trabalho no projeto X')

# Ver status (tenta buscar da API primeiro)
status = monitor.estimate_usage('synthetic')
print(f"Uso: {status.current_usage}h, Status API: {status.api_status}")

# Gerar relatório completo
print(monitor.generate_full_report())

# Ver quais APIs estão disponíveis
print(monitor.format_api_summary())
```

## Relatório Automático Diário

Para configurar relatório diário às 06:00:

```bash
# Via cron do OpenClaw
openclaw cron add \
  --name "lenovo-daily-workspace-report" \
  --schedule "0 6 * * *" \
  --command "python3 /path/to/scripts/monitor.py --report"
```

Ou usar a configuração de cron já existente (job ID: `dd088124-64de-4198-870a-45d0e2c6c4c5`).

## Interpretando o Relatório

### Status do Consumo
- **🟢 Below**: Uso abaixo da média (ou dentro das horas incluídas)
- **🟡 On Track**: Uso na média esperada
- **🔴 Above**: Uso acima da média (ou excedente significativo)

### Status da API
- **⚡**: API conectada, dados em tempo real
- **⚠️**: API não configurada ou erro
- **📊**: Sem API, usando dados manuais/estimados

### Ferramentas 5h+Semanal (Codex, Synthetic)
Mostra:
- Horas usadas no ciclo
- Horas incluídas (5h)
- Excedente (se houver)
- Status da tentativa de conexão com API

### Ferramentas Mensais (Cursor, Copilot, Warp)
Mostra:
- Horas estimadas de uso
- Dias restantes no ciclo
- Projeção linear de uso

## Banco de Dados

Local: `~/.ai_usage_monitor.db`

Tabela: `usage_logs`
- `tool_name`: nome da ferramenta
- `usage_value`: valor do uso
- `usage_unit`: unidade (hours, tokens, percentage)
- `recorded_at`: timestamp
- `notes`: observações
- `source`: origem (manual, api)

## Integrações de API

### OpenAI (Codex)
Usa `OPENAI_API_KEY` para tentar buscar dados. Nota: A API pública do OpenAI não expõe usage dashboard - a skill tenta conectar mas pode reportar "API disponível mas endpoint de uso não implementado".

### Outras APIs
As demais ferramentas (Synthetic, Warp, Cursor, Copilot) não expõem APIs públicas documentadas para uso. A skill está preparada para quando essas APIs ficarem disponíveis.

Para adicionar suporte a novas APIs, editar o método `fetch_realtime_usage()` em `scripts/monitor.py`.

## Configuração Avançada

Ver [references/tools_config.md](references/tools_config.md) para:
- Detalhes dos modelos de cobrança
- Fórmulas de cálculo
- Estrutura do banco de dados

## Tratamento de Erros

- **API key não configurada**: Reportar a ferramenta com status "⚠️ sem API key" e continuar com as demais
- **Banco de dados corrompido**: Fazer backup e recriar o arquivo `.ai_usage_monitor.db`
- **Endpoint indisponível**: Usar dados locais e sinalizar que os dados podem estar desatualizados
- **Ciclo de cobrança não configurado**: Solicitar ao usuário a data de início do ciclo e salvar para uso futuro

## Privacidade

- O banco de dados de uso (`~/.ai_usage_monitor.db`) pode conter informações sensíveis de uso; não compartilhar sem autorização
- As chaves de API (API keys) nunca devem ser incluídas em relatórios ou logs; apenas os nomes das variáveis são registrados

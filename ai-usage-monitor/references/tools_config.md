# Configuração das Ferramentas de IA

## Modelos de Cobrança

### Cursor - $20/mês
- **Dia de cobrança:** 10
- **Janela:** Mensal
- **Modelo:** Assinatura fixa com uso ilimitado
- **API:** CURSOR_API_KEY (não documentada)
- **Monitoramento:** Uso percentual estimado do ciclo

### Codex - $200
- **Dia de cobrança:** 22
- **Janela:** 5h + Semanal
- **Modelo:** 5 horas incluídas, depois cobrança adicional
- **API:** OPENAI_API_KEY (limitado)
- **Monitoramento:** Rastrear horas usadas dentro da janela semanal

### Copilot - $10/mês
- **Dia de cobrança:** 25
- **Janela:** Mensal
- **Modelo:** Assinatura fixa com uso ilimitado
- **API:** GITHUB_TOKEN (uso limitado)
- **Monitoramento:** Uso percentual estimado do ciclo

### Synthetic - $20
- **Dia de cobrança:** 17
- **Janela:** 5h + Semanal
- **Modelo:** 5 horas incluídas, depois cobrança adicional
- **API:** SYNTHETIC_API_KEY (não documentada)
- **Monitoramento:** Rastrear horas usadas dentro da janela semanal

### Warp - $20/mês
- **Dia de cobrança:** 12
- **Janela:** Mensal
- **Modelo:** Assinatura fixa com uso ilimitado
- **API:** WARP_API_KEY (não documentada)
- **Monitoramento:** Uso percentual estimado do ciclo

## Variáveis de Ambiente

A skill verifica automaticamente estas variáveis:

```bash
# APIs encontradas automaticamente
OPENAI_API_KEY      # Para Codex
GITHUB_TOKEN        # Para Copilot
SYNTHETIC_API_KEY   # Para Synthetic
WARP_API_KEY        # Para Warp
CURSOR_API_KEY      # Para Cursor
```

Para adicionar ao ambiente:
```bash
export SYNTHETIC_API_KEY="sua-chave-aqui"
export WARP_API_KEY="sua-chave-aqui"
```

## Interpretação dos Status

### 🟢 Below (Abaixo)
- **Mensal:** Uso abaixo da média esperada para o período
- **5h+Semanal:** Ainda dentro das horas incluídas (≤5h)

### 🟡 On Track (Na Média)
- Uso compatível com a projeção esperada
- Para 5h+semanal: excedente leve projetado (<2h)

### 🔴 Above (Acima)
- **Mensal:** Uso acima da média esperada
- **5h+Semanal:** Excedente significativo projetado (>2h)

## Cálculo de Projeção

### Ferramentas Mensais
```
Taxa diária = Uso atual / Dias decorridos
Projeção = Taxa diária × Total de dias no ciclo
```

### Ferramentas 5h+Semanal
```
Uso semanal atual = Horas registradas na semana
Excedente = max(0, Uso semanal - 5)
Projeção mensal = Excedente × 4 semanas
```

## Banco de Dados

### Tabela: usage_logs
```sql
CREATE TABLE usage_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_name TEXT NOT NULL,
    usage_value REAL,
    usage_unit TEXT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    source TEXT DEFAULT 'manual'  -- 'manual' ou 'api'
);
```

### Localização
`~/.ai_usage_monitor.db`

### Colunas
- `id`: identificador único
- `tool_name`: nome da ferramenta (cursor, codex, copilot, synthetic, warp)
- `usage_value`: valor numérico do uso
- `usage_unit`: unidade (hours, tokens, percentage, requests)
- `recorded_at`: timestamp do registro
- `notes`: observações opcionais
- `source`: origem do dado ('manual' ou 'api')

## APIs - Status Atual

### OpenAI (Codex) - ⚡ Parcial
- Possui OPENAI_API_KEY
- API pública não expõe usage dashboard
- Skill tenta conectar mas pode reportar "API disponível mas endpoint de uso não implementado"

### Synthetic - 🔍 Não documentada
- Não há API pública documentada
- Requer investigação ou contato com suporte

### Warp - 🔍 Não documentada
- Não há API pública documentada
- Requer investigação ou contato com suporte

### Cursor - 🔍 Não documentada
- Não há API pública documentada
- Requer investigação ou contato com suporte

### Copilot (GitHub) - 🔍 Limitada
- API do GitHub não expõe uso detalhado do Copilot
- Requer investigação de endpoints específicos

## Extensão para Novas APIs

Para adicionar suporte a uma nova API:

1. Adicionar variável de ambiente em `_check_available_apis()`
2. Implementar método `fetch_{name}_usage()`
3. Atualizar `fetch_realtime_usage()` para chamar o novo método
4. Atualizar `ToolConfig` com `api_source`

Exemplo:
```python
def fetch_newservice_usage(self) -> Optional[Dict]:
    api_key = os.getenv('NEWSERVICE_API_KEY')
    if not api_key:
        return None
    
    response = requests.get(
        'https://api.newservice.com/usage',
        headers={'Authorization': f'Bearer {api_key}'}
    )
    return response.json()
```

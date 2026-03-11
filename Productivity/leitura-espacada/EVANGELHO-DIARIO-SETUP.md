# Configuração do Evangelho Diário (6h)

## ✅ Status

- ✅ Cron job criado: `d99820cc-8c50-48d7-b55d-436ef1a513c7`
- ✅ Horário: Todos os dias às 6:00 (America/Fortaleza)
- ✅ Ação: Agente busca evangelho + adiciona + envia Telegram

## ⚠️ Requisitos para Funcionar

### 1. Browser Extension (Chrome)

O agente precisa do Chrome conectado para buscar o evangelho:

```
1. Abrir Chrome
2. Clicar no ícone da extensão "OpenClaw Browser Relay"
3. Ativar em uma aba (badge ON)
4. Navegar para: https://www.vaticannews.va/pt/evangelho-do-dia.html
```

### 2. Telegram Channel

- **Channel ID**: `3861090488`
- **Tópico**: "Palavra"
- **URL**: https://t.me/c/3861090488/38

Verificar se o bot tem permissão para postar neste canal/tópico.

## 📋 Fluxo do Agente (6h)

Quando o cron dispara, o agente deve:

```
1. Buscar evangelho em vaticannews.va (usando browser)
2. Extrair:
   - Data litúrgica
   - Referência (ex: Mateus 5:1-12)
   - Texto completo
   - Salmo
   - Tempo litúrgico
3. Criar síntese (3-5 pontos principais)
4. Adicionar ao sistema:
   cd ~/clawdbot-skills/leitura-espacada
   LEITURA_COLLECTION=biblia node scripts/leitura.js add "REF" "PERGUNTA" "RESUMO" "TEMAS"
5. Enviar Telegram (tópico Palavra):
   - Evangelho completo
   - Síntese
   - Link para o card no vault
```

## 🧪 Teste Manual

Para testar agora (sem esperar 6h):

```bash
# Listar jobs do cron
openclaw cron list

# Executar job manualmente
openclaw cron run d99820cc-8c50-48d7-b55d-436ef1a513c7

# Ou:
cron run jobId=d99820cc-8c50-48d7-b55d-436ef1a513c7
```

## 📝 Exemplo de Mensagem (Telegram)

```
📖 *Evangelho do Dia*
📅 17 de Fevereiro de 2026
⛪ Tempo Comum

*Mateus 5:1-12 — As Bem-aventuranças*

[Texto completo do evangelho]

───

📝 *Síntese:*
• Jesus ensina as bem-aventuranças no Sermão da Montanha
• As bem-aventuranças invertem valores do mundo
• Promessa: o Reino pertence aos pobres de espírito

───

💾 *Card adicionado ao sistema*
Próxima revisão: 18/02/2026
```

## 🔧 Arquivos Criados

- `scripts/evangelho-diario.sh` — Script bash
- `scripts/agent-evangelho-do-dia.js` — Script Node.js
- Cron job registrado no sistema

## 🚨 Troubleshooting

### "Browser não disponível"
- Conectar extensão do Chrome
- Ou usar fonte alternativa (API, RSS, etc.)

### "Não enviou para Telegram"
- Verificar permissões do bot
- Verificar se channel ID está correto
- Verificar se tópico existe

### "Erro ao adicionar card"
- Verificar se coleção "biblia" existe
- Verificar permissões no vault

## 🔄 Alternativas (sem browser)

Se o browser não puder ser usado:

1. **API de terceiros**: Buscar serviço com API do evangelho
2. **RSS**: Alguns sites oferecem feeds RSS
3. **Email**: Configurar recebimento por email e processar
4. **Manual**: Você envia o evangelho e eu processo

---

*Configurado em: 2026-02-17 | Próxima execução: Amanhã às 6h*

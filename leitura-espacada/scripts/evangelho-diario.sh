#!/bin/bash
# Script do Evangelho do Dia
# Executado diariamente pelo cron às 6h

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_DIR="${LEITURA_VAULT_PATH:-$HOME/Obsidian/leitura}"
COLLECTION="biblia"

# Data atual
DATA=$(date +%Y-%m-%d)
DATA_FORMATADA=$(date +"%d/%m/%Y")
DIA_SEMANA=$(date +%A)

# Mapear dia da semana para português
case $DIA_SEMANA in
  Sunday) DIA_PT="Domingo" ;;
  Monday) DIA_PT="Segunda-feira" ;;
  Tuesday) DIA_PT="Terça-feira" ;;
  Wednesday) DIA_PT="Quarta-feira" ;;
  Thursday) DIA_PT="Quinta-feira" ;;
  Friday) DIA_PT="Sexta-feira" ;;
  Saturday) DIA_PT="Sábado" ;;
esac

# Arquivo de saída para o agente processar
OUTPUT_FILE="/tmp/evangelho-do-dia-${DATA}.txt"

echo "=== EVANGELHO DO DIA ===" > "$OUTPUT_FILE"
echo "Data: $DATA_FORMATADA ($DIA_PT)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Nota: O agente (IA) precisa buscar o evangelho do dia
# usando browser ou outra ferramenta, pois este script
# roda em ambiente sem acesso direto à web

echo "INSTRUÇÕES_PARA_AGENTE:" >> "$OUTPUT_FILE"
echo "1. Buscar o Evangelho do Dia em:" >> "$OUTPUT_FILE"
echo "   - https://www.vaticannews.va/pt/evangelho-do-dia.html" >> "$OUTPUT_FILE"
echo "   - Ou: https://www.paulinas.org.br/liturgia-diaria" >> "$OUTPUT_FILE"
echo "   - Ou: https://www.cnbb.org.br/evangelho-do-dia/" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "2. Extrair:" >> "$OUTPUT_FILE"
echo "   - Referência bíblica (ex: Mateus 5:1-12)" >> "$OUTPUT_FILE"
echo "   - Texto completo do evangelho" >> "$OUTPUT_FILE"
echo "   - Salmo do dia" >> "$OUTPUT_FILE"
echo "   - Oração/Reflexão (opcional)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "3. Criar síntese em 3-5 pontos" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "4. Executar:" >> "$OUTPUT_FILE"
echo "   cd ~/clawdbot-skills/leitura-espacada" >> "$OUTPUT_FILE"
echo "   LEITURA_COLLECTION=biblia node scripts/leitura.js add '\$REFERENCIA' '\$PERGUNTA' '\$RESPOSTA' '\$TEMAS'" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "5. Enviar para Telegram:" >> "$OUTPUT_FILE"
echo "   Channel: 3861090488" >> "$OUTPUT_FILE"
echo "   Tópico: Palavra" >> "$OUTPUT_FILE"
echo "   Mensagem: Evangelho completo + síntese" >> "$OUTPUT_FILE"

# Retornar o arquivo para o agente ler
cat "$OUTPUT_FILE"

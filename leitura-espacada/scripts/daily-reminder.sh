#!/bin/bash
# Lembrete diário para Leitura Espaçada
# Adicionar ao crontab: 0 7 * * * /path/to/daily-reminder.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Verificar se há cards pendentes em todas as coleções
VAULT_BASE="${LEITURA_VAULT_PATH:-$HOME/Obsidian/leitura}"

if [ ! -d "$VAULT_BASE" ]; then
  exit 0
fi

TOTAL_DUE=0
COLLECTIONS_WITH_DUE=""

for collection in "$VAULT_BASE"/*; do
  if [ -d "$collection/cards" ]; then
    COLLECTION_NAME=$(basename "$collection")
    
    # Contar cards pendentes
    DUE_COUNT=$(find "$collection/cards" -name "*.json" -exec sh -c '
      today=$(date +%Y-%m-%d)
      next=$(cat "$1" | grep -o "\"next_review\": \"[^\"]*\"" | cut -d\" -f4)
      [ "$next" \<= "$today" ] && echo "1"
    ' _ {} \; | wc -l)
    
    if [ "$DUE_COUNT" -gt 0 ]; then
      TOTAL_DUE=$((TOTAL_DUE + DUE_COUNT))
      COLLECTIONS_WITH_DUE="$COLLECTIONS_WITH_DUE\n  • $COLLECTION_NAME: $DUE_COUNT cards"
    fi
  fi
done

if [ "$TOTAL_DUE" -gt 0 ]; then
  echo "📚 Leitura Espaçada"
  echo ""
  echo "🎯 Você tem $TOTAL_DUE card(s) para revisar hoje!"
  echo -e "$COLLECTIONS_WITH_DUE"
  echo ""
  echo "Para estudar:"
  echo "  cd $VAULT_BASE && leitura study"
  echo ""
fi

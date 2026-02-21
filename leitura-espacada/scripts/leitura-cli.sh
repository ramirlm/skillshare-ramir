#!/bin/bash
# Leitura Espaçada - CLI Wrapper
# Facilita o uso do sistema

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NODE_SCRIPT="$SCRIPT_DIR/leitura.js"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Banner
show_banner() {
  echo -e "${CYAN}"
  echo '  _      _ _ _                     _    '
  echo ' | |    (_) | |                   | |   '
  echo ' | |     _| | |_ ___ _ __ __ _  __| | ___'
  echo ' | |    | | | __/ _ \ |__/ _\` |/ _` |/ _ \'
  echo ' | |____| | | ||  __/ | | (_| | (_| |  __/'
  echo ' |______|_|_|\__\___|_|  \__,_|\__,_|\___|'
  echo -e "${NC}"
  echo -e "${BLUE}   Sistema de Repetição Espaçada${NC}"
  echo ""
}

# Ajuda
show_help() {
  show_banner
  echo -e "${GREEN}Uso:${NC} leitura [comando] [argumentos]"
  echo ""
  echo -e "${GREEN}Comandos:${NC}"
  echo "  ${YELLOW}init${NC} [nome]          Inicializar nova coleção"
  echo "  ${YELLOW}add${NC} [args]            Adicionar card (interativo se sem args)"
  echo "  ${YELLOW}due${NC}                   Cards pendentes hoje"
  echo "  ${YELLOW}study${NC}                 Modo estudo interativo"
  echo "  ${YELLOW}review${NC} <id> <perf>   Revisar card específico"
  echo "  ${YELLOW}stats${NC}                 Estatísticas"
  echo "  ${YELLOW}next${NC}                  Próximas revisões"
  echo "  ${YELLOW}backup${NC}                Criar backup"
  echo "  ${YELLOW}reset${NC} <id>           Resetar card"
  echo ""
  echo -e "${GREEN}Exemplos:${NC}"
  echo "  leitura init biblia"
  echo "  leitura add 'Evangelho' 'Pergunta?' 'Resposta.' 'tema1,tema2'"
  echo "  leitura study"
  echo "  leitura stats"
  echo ""
  echo -e "${GREEN}Variáveis:${NC}"
  echo "  LEITURA_COLLECTION=biblia   Usar coleção 'biblia'"
}

# Verificar Node.js
if ! command -v node &> /dev/null; then
  echo -e "${RED}❌ Node.js não encontrado${NC}"
  echo "Instale Node.js: https://nodejs.org"
  exit 1
fi

# Verificar script principal
if [ ! -f "$NODE_SCRIPT" ]; then
  echo -e "${RED}❌ Script não encontrado: $NODE_SCRIPT${NC}"
  exit 1
fi

# Executar comando
CMD="$1"
shift || true

case "$CMD" in
  init)
    node "$NODE_SCRIPT" init "$@"
    ;;
  add)
    if [ $# -eq 0 ]; then
      # Modo interativo
      echo -e "${BLUE}📝 Adicionar novo card${NC}"
      echo ""
      
      read -p "Título: " TITLE
      [ -z "$TITLE" ] && { echo -e "${RED}Título obrigatório${NC}"; exit 1; }
      
      echo -e "${YELLOW}Pergunta (frente):${NC}"
      read -r FRONT
      [ -z "$FRONT" ] && { echo -e "${RED}Pergunta obrigatória${NC}"; exit 1; }
      
      echo -e "${YELLOW}Resposta (verso):${NC}"
      read -r BACK
      [ -z "$BACK" ] && { echo -e "${RED}Resposta obrigatória${NC}"; exit 1; }
      
      read -p "Temas (separados por vírgula): " THEMES
      
      node "$NODE_SCRIPT" add "$TITLE" "$FRONT" "$BACK" "$THEMES"
    else
      node "$NODE_SCRIPT" add "$@"
    fi
    ;;
  due)
    node "$NODE_SCRIPT" due
    ;;
  study)
    node "$NODE_SCRIPT" study
    ;;
  review)
    if [ $# -lt 2 ]; then
      echo -e "${RED}Uso: leitura review <id> <performance>${NC}"
      echo "Performance: again | hard | good | easy"
      exit 1
    fi
    node "$NODE_SCRIPT" review "$@"
    ;;
  stats)
    show_banner
    node "$NODE_SCRIPT" stats
    ;;
  next)
    node "$NODE_SCRIPT" next
    ;;
  backup)
    node "$NODE_SCRIPT" backup
    ;;
  reset)
    node "$NODE_SCRIPT" reset "$@"
    ;;
  help|--help|-h)
    show_help
    ;;
  *)
    if [ -z "$CMD" ]; then
      show_banner
      show_help
    else
      echo -e "${RED}❌ Comando desconhecido: $CMD${NC}"
      echo "Use 'leitura help' para ver os comandos disponíveis."
      exit 1
    fi
    ;;
esac

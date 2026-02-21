#!/bin/bash
#####################################################################
# video-bug-prompt - Análise Inteligente de Bugs em Vídeos
# Extrai frames, analisa com IA, busca contexto, gera relatório
#####################################################################

set -e

VIDEO_PATH="$1"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORTS_DIR="$HOME/clawdbot-agents/main/reports/bugs"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções de output
info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[X]${NC} $1"; exit 1; }

#####################################################################
# 1. VALIDAÇÃO
#####################################################################

if [ -z "$VIDEO_PATH" ]; then
    error "Uso: analyze-bug.sh <caminho-do-video>"
fi

if [ ! -f "$VIDEO_PATH" ]; then
    error "Vídeo não encontrado: $VIDEO_PATH"
fi

# Verificar dependências
command -v ffmpeg >/dev/null 2>&1 || error "ffmpeg não instalado"
command -v pandoc >/dev/null 2>&1 || warn "pandoc não instalado (PDF não será gerado)"

VIDEO_NAME=$(basename "$VIDEO_PATH")
VIDEO_EXT="${VIDEO_NAME##*.}"
VIDEO_BASE="${VIDEO_NAME%.*}"

info "Analisando vídeo: $VIDEO_NAME"

#####################################################################
# 2. PERGUNTAS INTERATIVAS
#####################################################################

info "📋 Coletando informações do bug..."
echo ""

read -p "🎫 Nome/ID do ticket (ex: BUG-123): " TICKET_ID
TICKET_ID=${TICKET_ID:-"BUG-AUTO-$TIMESTAMP"}

read -p "📁 Qual projeto está relacionado? " PROJECT
PROJECT=${PROJECT:-"Não especificado"}

read -p "💡 Observações sobre o bug (opcional): " USER_NOTES

read -p "📄 Quer anexar contexto adicional? (s/n): " ATTACH_CONTEXT
ATTACH_CONTEXT=${ATTACH_CONTEXT:-n}

CONTEXT_FILES=""
if [[ "$ATTACH_CONTEXT" == "s" ]]; then
    read -p "📎 Caminho do arquivo (PDF/Markdown): " CONTEXT_PATH
    if [ -f "$CONTEXT_PATH" ]; then
        CONTEXT_FILES="$CONTEXT_PATH"
        success "Contexto anexado: $CONTEXT_PATH"
    else
        warn "Arquivo não encontrado, continuando sem anexo"
    fi
fi

echo ""
info "✅ Informações coletadas!"

#####################################################################
# 3. CRIAR DIRETÓRIOS
#####################################################################

BUG_DIR="$REPORTS_DIR/$TICKET_ID-$DATE"
FRAMES_DIR="$BUG_DIR/frames"

mkdir -p "$FRAMES_DIR"

info "📂 Diretório criado: $BUG_DIR"

#####################################################################
# 4. EXTRAIR FRAMES
#####################################################################

info "🎬 Extraindo frames do vídeo (1 a cada 0.5s)..."

# Obter duração do vídeo
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO_PATH")
DURATION_INT=${DURATION%.*}

info "⏱️  Duração: ${DURATION}s"

# Extrair frames (1 a cada 0.5 segundos)
ffmpeg -i "$VIDEO_PATH" -vf "fps=2" "$FRAMES_DIR/frame-%03d.png" -hide_banner -loglevel error

FRAME_COUNT=$(ls -1 "$FRAMES_DIR"/frame-*.png 2>/dev/null | wc -l)

if [ "$FRAME_COUNT" -eq 0 ]; then
    error "Nenhum frame extraído!"
fi

success "✅ $FRAME_COUNT frames extraídos"

#####################################################################
# 5. PLACEHOLDER PARA ANÁLISE COM VISION MODEL
#####################################################################

info "🔍 Analisando frames com IA..."
info "   (Esta parte será executada pelo Clawdbot via image tool)"

# Criar arquivo com lista de frames para Clawdbot processar
FRAMES_LIST="$BUG_DIR/frames-to-analyze.txt"
ls -1 "$FRAMES_DIR"/frame-*.png > "$FRAMES_LIST"

success "✅ Lista de frames preparada: $FRAMES_LIST"

#####################################################################
# 6. BUSCAR CONTEXTO NO OBSIDIAN
#####################################################################

info "📚 Buscando contexto relacionado..."

OBSIDIAN_VAULT="$HOME/Documents/clawdmold"
CONTEXT_RESULTS=""

if [ -d "$OBSIDIAN_VAULT" ]; then
    # Buscar por nome do projeto
    if [ "$PROJECT" != "Não especificado" ]; then
        info "   Buscando '$PROJECT' no Obsidian..."
        SEARCH_RESULTS=$(grep -r -i "$PROJECT" "$OBSIDIAN_VAULT" --include="*.md" 2>/dev/null | head -5 || echo "")
        
        if [ -n "$SEARCH_RESULTS" ]; then
            CONTEXT_RESULTS="$SEARCH_RESULTS"
            success "   Encontrado contexto no Obsidian!"
        fi
    fi
fi

#####################################################################
# 7. GERAR RELATÓRIO BASE
#####################################################################

info "📝 Gerando relatório base..."

MD_REPORT="$BUG_DIR/bug-report-$TICKET_ID.md"

# Copiar template
cp "$SKILL_DIR/templates/bug-report-template.md" "$MD_REPORT"

# Substituir placeholders básicos
sed -i "s|{{TICKET_ID}}|$TICKET_ID|g" "$MD_REPORT"
sed -i "s|{{DATE}}|$DATE|g" "$MD_REPORT"
sed -i "s|{{PROJECT}}|$PROJECT|g" "$MD_REPORT"
sed -i "s|{{VIDEO_NAME}}|$VIDEO_NAME|g" "$MD_REPORT"
sed -i "s|{{TOTAL_FRAMES}}|$FRAME_COUNT|g" "$MD_REPORT"
sed -i "s|{{GENERATION_TIMESTAMP}}|$TIMESTAMP|g" "$MD_REPORT"
sed -i "s|{{ADDITIONAL_NOTES}}|$USER_NOTES|g" "$MD_REPORT"

# Adicionar lista de frames
FRAMES_MD=""
for frame in "$FRAMES_DIR"/frame-*.png; do
    FRAME_NAME=$(basename "$frame")
    FRAME_NUM="${FRAME_NAME#frame-}"
    FRAME_NUM="${FRAME_NUM%.png}"
    FRAMES_MD="$FRAMES_MD\n- ![$FRAME_NAME]($frame)\n"
done

sed -i "s|{{KEY_FRAMES}}|$FRAMES_MD|g" "$MD_REPORT"

success "✅ Relatório base criado: $MD_REPORT"

#####################################################################
# 8. INFORMAR CLAWDBOT
#####################################################################

info "🤖 Próximos passos (executados pelo Clawdbot):"
echo ""
echo "   1. Analisar frames em: $FRAMES_LIST"
echo "   2. Preencher análise em: $MD_REPORT"
echo "   3. Gerar PDF (se pandoc disponível)"
echo "   4. Enviar email para ramir.mesquita@gmail.com"
echo ""

# Salvar metadados para Clawdbot processar
METADATA_FILE="$BUG_DIR/metadata.json"
cat > "$METADATA_FILE" << EOF
{
  "ticketId": "$TICKET_ID",
  "project": "$PROJECT",
  "videoPath": "$VIDEO_PATH",
  "framesDir": "$FRAMES_DIR",
  "framesList": "$FRAMES_LIST",
  "frameCount": $FRAME_COUNT,
  "reportMarkdown": "$MD_REPORT",
  "userNotes": "$USER_NOTES",
  "contextFiles": "$CONTEXT_FILES",
  "obsidianContext": "$CONTEXT_RESULTS",
  "timestamp": "$TIMESTAMP"
}
EOF

success "✅ Metadados salvos: $METADATA_FILE"

echo ""
success "🎯 ANÁLISE PREPARADA!"
info "📂 Outputs em: $BUG_DIR"
echo ""
info "🔄 Clawdbot vai completar a análise e enviar email automaticamente"
echo ""

# Retornar path do metadata para Clawdbot processar
echo "$METADATA_FILE"

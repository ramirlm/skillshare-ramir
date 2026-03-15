# skill-pdf-generator

<!-- openclaw -->
```yaml
emoji: 📄
kind: tool
requires:
  - pandoc
  - wkhtmltopdf (optional fallback)
  - openclaw CLI
install: |
  # Install pandoc (required)
  sudo apt-get install pandoc
  # Or on macOS
  brew install pandoc

  # Optional: Install wkhtmltopdf for fallback
  sudo apt-get install wkhtmltopdf
  # Or on macOS
  brew install wkhtmltopdf
hooks:
  post-install: |
    chmod +x bin/skill-pdf
capabilities:
  - pdf-generation
  - markdown-conversion
  - skill-inventory-reporting
```
<!-- /openclaw -->

## Description

Gera PDFs a partir de Markdown, HTML ou inventários/listas de skills com formatação profissional. Use quando precisar converter .md/.html em PDF, criar relatório PDF de skills instaladas, aplicar templates customizáveis, ou incluir cabeçalho/rodapé com data e numeração de páginas.

## Installation

1. Certifique-se de ter o `pandoc` instalado:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install pandoc

   # macOS
   brew install pandoc
   ```

2. (Opcional) Instale `wkhtmltopdf` para fallback:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install wkhtmltopdf

   # macOS
   brew install wkhtmltopdf
   ```

3. Torne o script executável:
   ```bash
   chmod +x bin/skill-pdf
   ```

## Usage

### Comando: generate

Converte um arquivo Markdown ou HTML para PDF.

```bash
skill-pdf generate --input arquivo.md --output arquivo.pdf
skill-pdf generate --input arquivo.html --output arquivo.pdf
```

**Opções:**
- `--input, -i`: Caminho do arquivo de entrada (Markdown ou HTML)
- `--output, -o`: Caminho do arquivo PDF de saída
- `--title, -t`: Título do documento (opcional)
- `--author, -a`: Autor do documento (opcional)

**Exemplos:**

```bash
# Converter Markdown para PDF
skill-pdf generate --input documento.md --output documento.pdf

# Converter com metadados
skill-pdf generate --input relatorio.md --output relatorio.pdf --title "Relatório Mensal" --author "Rocco"

# Usar caminhos curtos
skill-pdf generate -i README.md -o README.pdf
```

### Comando: skills

Gera um PDF com o inventário completo de skills do sistema OpenClaw.

```bash
skill-pdf skills --output skills-report.pdf
```

**Opções:**
- `--output, -o`: Caminho do arquivo PDF de saída (padrão: skills-report.pdf)
- `--format, -f`: Formato da saída: pdf ou markdown (padrão: pdf)

**Exemplos:**

```bash
# Gerar relatório PDF de skills
skill-pdf skills --output meu-inventario.pdf

# Gerar apenas o Markdown (sem converter)
skill-pdf skills --output inventario.md --format markdown
```

O relatório inclui:
- Nome da skill
- Descrição
- Exemplos de uso
- Localização do arquivo

## How It Works

### Conversão Markdown → PDF

1. **Pandoc (primário)**: Usa LaTeX ou wkhtmltopdf para converter Markdown para PDF com alta fidelidade de formatação.

2. **wkhtmltopdf (fallback)**: Se o pandoc falhar ou não estiver disponível, converte HTML intermediário para PDF.

### Geração de Relatório de Skills

1. Executa `openclaw skills list --json` para obter a lista de skills
2. Parseia o JSON e extrai: nome, descrição, exemplos e localização
3. Gera uma tabela Markdown formatada
4. Converte para PDF usando o método primário (pandoc)

## Dependencies

- **pandoc**: Conversor de documentos universal (obrigatório)
- **wkhtmltopdf**: Renderizador HTML para PDF (opcional, fallback)
- **openclaw CLI**: Para o comando `skills` (obrigatório para geração de inventário)

## Troubleshooting

### "pandoc: command not found"

Instale o pandoc:
```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install pandoc

# macOS
brew install pandoc
```

### Erro de conversão com caracteres especiais

O pandoc lida bem com UTF-8. Se houver problemas, certifique-se de que o arquivo de entrada está codificado em UTF-8:
```bash
file -i arquivo.md
```

### PDF gerado está vazio

Verifique se o arquivo de entrada não está vazio:
```bash
wc -l arquivo.md
```

## License

MIT

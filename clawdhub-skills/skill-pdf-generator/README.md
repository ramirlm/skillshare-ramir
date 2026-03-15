# Skill PDF Generator

Gera PDFs a partir de Markdown, HTML ou listas de skills com formatação profissional.

## Instalação Rápida

```bash
# 1. Clone ou copie a skill para o diretório correto
cp -r skill-pdf-generator ~/clawdbot-skills/skills/

# 2. Instale dependências obrigatórias
sudo apt-get install pandoc texlive-latex-base texlive-latex-extra

# 3. Adicione ao PATH
export PATH="$HOME/clawdbot-skills/skills/skill-pdf-generator/bin:$PATH"
```

## Comandos

### `generate` - Converter arquivo para PDF

```bash
skill-pdf generate --input <arquivo> --output <pdf> [opções]

Opções:
  --input, -i      Arquivo de entrada (.md, .html, .txt)
  --output, -o     Arquivo PDF de saída
  --format, -f     Formato do entrada: auto, markdown, html (padrão: auto)
  --template, -t   Template a usar: default, professional, minimal, academic
  --title          Título do documento
  --author         Autor do documento
  --date           Data (padrão: data atual)
```

### `skills` - Gerar inventário de skills

```bash
skill-pdf skills --output <pdf> [opções]

Opções:
  --output, -o     Arquivo PDF de saída (padrão: skills-report.pdf)
  --template, -t   Template a usar
  --skills-dir     Diretório de skills (padrão: ~/clawdbot-skills/skills/)
```

### `template` - Gerenciar templates

```bash
skill-pdf template --list                    # Listar templates
skill-pdf template --show <nome>             # Mostrar template
skill-pdf template --path                    # Diretório de templates
```

## Exemplos

```bash
# Converter notas para PDF
skill-pdf generate -i notas.md -o notas.pdf

# Gerar relatório profissional
skill-pdf generate -i relatorio.md -o relatorio.pdf -t professional --author "João Silva"

# Inventário de skills
skill-pdf skills -o ~/Documentos/minhas-skills.pdf

# HTML para PDF
skill-pdf generate -i pagina.html -o pagina.pdf -f html
```

## Estrutura

```
skill-pdf-generator/
├── SKILL.md              # Documentação da skill
├── README.md             # Este arquivo
├── bin/
│   └── skill-pdf         # CLI principal
└── templates/            # Templates LaTeX/CSS
    ├── default.tex
    ├── professional.tex
    └── minimal.tex
```

## Dependências

| Ferramenta | Obrigatório | Descrição |
|------------|-------------|-----------|
| pandoc     | Sim         | Conversor principal |
| pdflatex   | Sim         | Compilador LaTeX |
| weasyprint | Não         | Fallback HTML→PDF |
| wkhtmltopdf| Não         | Fallback HTML→PDF |

## Configuração

Crie `~/.config/skill-pdf/config.yaml`:

```yaml
default_template: professional
output_dir: ~/PDFs
header:
  text: "Meus Documentos"
footer:
  show_page_numbers: true
  show_date: true
```

## Licença

MIT License

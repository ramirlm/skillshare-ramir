---
name: video-bug-prompt
description: Analisa vídeos de bugs, extrai frames, detecta mudanças, busca contexto do projeto e gera relatório detalhado com insights para correção. Envia por email com anexos.
version: 1.1.0
author: ramirlm
triggers:
  - "analise bug"
  - "relatório de bug"
  - "analise vídeo"
  - "bug no vídeo"
  - "video bug"
metadata:
  clawdbot:
    emoji: "🎥"
    os: ["linux", "darwin"]
    requires:
      bins: ["ffmpeg"]
      optional: ["pandoc"]
---

# video-bug-prompt 🎥🐛

Análise inteligente de bugs em vídeos com contexto de código.

## Quando Usar

Use quando:
- Receber vídeo mostrando um bug
- Precisar documentar comportamento incorreto
- Quiser insights de onde pode estar o problema no código
- Precisar de relatório completo para equipe/agente autônomo

## Como Funciona

### Workflow Automático

1. **Você envia o vídeo** do bug
2. **Skill faz perguntas interativas:**
   - Nome/ID do ticket
   - Quer anexar contexto? (PDF/Markdown)
   - Qual projeto está relacionado?
   - Observações sobre o bug

3. **Extrai e analisa frames:**
   - Máximo de frames possível (1 a cada 0.5s)
   - Analisa cada frame com vision model
   - Detecta mudanças visuais
   - Identifica momento exato do bug

4. **Busca contexto:**
   - Obsidian (documentação, notas de projeto)
   - PRDs relacionados
   - Código fonte (se indexado)
   - Tickets anteriores

5. **Gera insights:**
   - Correlaciona bug visual com código
   - Sugere arquivos/funções suspeitas
   - Identifica padrões similares

6. **Envia por email:**
   - Relatório completo (PDF ou Markdown)
   - Frames-chave anexados
   - Links para código relevante
   - Sugestões de correção

## Comandos Aceitos

```
"Analise bug do vídeo [path/url]"
"Crie relatório de bug: [path]"
"Analise este vídeo de bug" (com vídeo anexado)
```

## Estrutura do Relatório

### Seções Geradas:

**1. Visão Geral**
- Descrição executiva do bug
- Impacto e severidade
- Projeto relacionado

**2. Passo a Passo (Timeline)**
- Frame por frame do que aconteceu
- Timestamps exatos
- Imagens inline dos momentos-chave

**3. Comportamento Esperado**
- Como deveria funcionar
- Referências (se encontradas em docs)

**4. Comportamento Observado**
- O que realmente aconteceu
- Evidências visuais

**5. Insights de Código**
- Arquivos suspeitos
- Funções relacionadas
- Possíveis causas

**6. Para Agente Autônomo**
- Instruções claras de reprodução
- Validação da correção
- Testes sugeridos

## Exemplo de Uso

**Você:**
```
Analise bug deste vídeo: ~/Downloads/bug-login.mp4
```

**Skill pergunta:**
```
📋 Nome/ID do ticket: 
📄 Quer anexar contexto adicional? (s/n)
🔍 Qual projeto: 
💡 Observações:
```

**Skill analisa e envia email:**
```
Para: ramir.mesquita@gmail.com
Assunto: [BUG-123] Relatório: Bug no Login
Anexos:
  - bug-report.pdf (relatório completo)
  - frame-001-inicial.png
  - frame-005-bug.png
  - frame-010-erro.png
```

## Requisitos

**Instalados:**
- ffmpeg (extração de frames)
- pandoc (geração de PDF)
- gog (envio de email)

**Opcionais:**
- Código do projeto indexado
- PRDs no Obsidian
- Documentação técnica

## Configuração

Nenhuma configuração necessária. A skill usa:
- Vision model padrão do Clawdbot
- Obsidian vault: configurado em `CLAWVAULT_PATH` (padrão: `~/Obsidian`)

## Outputs

**Email enviado contém:**
- ✅ Relatório PDF/Markdown
- ✅ Frames-chave anexados
- ✅ Links para código
- ✅ Sugestões de correção
- ✅ Timeline visual completa

**Arquivos salvos em:**
```
[REPORTS_DIR]/bugs/
  ├── bug-[ticket]-[date].md
  ├── bug-[ticket]-[date].pdf
  └── frames/
      ├── frame-001.png
      ├── frame-002.png
      └── ...
```

> `[REPORTS_DIR]` padrão: `~/clawdbot-agents/main/reports`. Configurável via `BUG_REPORTS_PATH`.

## Dicas

- **Vídeos curtos** (< 2min) funcionam melhor
- **Grave em alta qualidade** para melhor análise visual
- **Inclua contexto verbal** se possível (narração)
- **Anexe logs/código** quando disponível

## Tratamento de Erros

- **ffmpeg não instalado**: Informar o erro e guiar instalação (`brew install ffmpeg` / `apt install ffmpeg`)
- **Vídeo muito longo** (> 10min): Alertar que a análise pode ser lenta e oferecer analisar apenas um intervalo específico
- **Vídeo sem variação visual**: Informar que não foram detectadas mudanças significativas entre frames
- **Contexto de projeto não encontrado**: Gerar relatório sem insights de código e indicar que o relatório foi gerado sem contexto
- **Falha ao enviar email**: Salvar relatório localmente e informar o caminho ao usuário
- **pandoc não disponível**: Gerar o relatório em Markdown ao invés de PDF

## Privacidade

- Redatar automaticamente dados pessoais (email, CPF, tokens) visíveis nos frames antes de enviar o relatório
- Não enviar frames de sessões autenticadas (home banking, email) sem confirmação explícita do usuário
- Perguntar ao usuário antes de incluir código-fonte proprietário no relatório

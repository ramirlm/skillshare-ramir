---
name: ontologia-transcript
description: "Processar transcrições de reuniões usando summarize e ontology. Use quando o Ramir colar/enviar uma transcrição de reunião e quiser: (1) resumir usando a skill summarize, (2) fazer análise completa da ontologia usando a skill ontology sobre tudo o que foi dito, (3) persistir tudo no vault (Obsidian) e ontology. Se for falado sobre solução/implementação, sugere usar skill transcription para o PRD (opcional)."
---

# Ontologia Transcript

## Objetivo
Transformar uma transcrição de reunião em **conhecimento estruturado na ontologia** e **persistência completa no vault**, usando summarize para resumo e ontology para análise de entidades.

## Entradas esperadas
- Transcrição colada no chat (texto bruto) **ou** arquivo de texto enviado
- Opcional: data da reunião, participantes, link (Meet/Zoom)

## Saídas (sempre entregar)
1. **Resumo executivo** gerado via skill `summarize`
2. **Análise de ontologia** completa usando skill `ontology`
3. **Persistência obrigatória**:
   - Criar/atualizar nota da reunião no Obsidian (`~/Obsidian`)
   - Atualizar entidades no ontology (Person, Organization, Project, Task, Meeting, Decision, etc.)
4. **Sugestão opcional**: Se houver discussão de solução/implementação, sugerir usar skill `transcription` para criar PRD

## Workflow (passo a passo)

### 1) Receber e normalizar a transcrição
- Aceitar texto colado ou arquivo
- Remover linhas vazias excessivas e marcações irrelevantes
- Detectar idioma (PT/EN)

### 2) Resumir usando skill `summarize`
- Usar CLI `summarize` para gerar resumo da transcrição
- Capturar pontos principais, decisões, próximos passos

### 3) Análise de ontologia usando skill `ontology`
Extrair e criar/atualizar entidades:

**Pessoas (Person)**:
- Participantes identificados na reunião
- Nomes mencionados (stakeholders, responsáveis)

**Organizações (Organization)**:
- Empresas, clientes, fornecedores mencionados

**Projetos (Project)**:
- Projetos discutidos
- Status mencionado

**Tarefas (Task)**:
- Action items identificados
- Responsáveis e prazos (quando mencionados)

**Reunião (Meeting)**:
- Entidade principal com data, participantes, link
- Relacionamentos com todos os itens acima

**Decisões (Decision)**:
- Decisões tomadas na reunião
- Contexto e justificativa

**Documentos/Notas (Document)**:
- A própria transcrição/resumo como documento

### 4) Persistir no Obsidian (OBRIGATÓRIO)
**Vault:** `~/Obsidian` (NUNCA `~/vault`)

**Local:** `~/Obsidian/Meetings/` ou pasta específica do projeto

**Nome do arquivo:**
`YYYY-MM-DD - Reunião - <Tema/Projeto>.md`

**Frontmatter obrigatório:**
```yaml
title: "YYYY-MM-DD - Reunião - <Tema>"
date: "YYYY-MM-DD"
type: "meeting"
participants:
  - "<Nome 1>"
  - "<Nome 2>"
project: "<Projeto>"
client: "<Cliente>"
source: "transcript"
tags:
  - meeting
  - transcript
processedAt: "<ISO-8601>"
summary: "<Resumo gerado pelo summarize>"
```

**Corpo da nota:**
- Resumo executivo (do summarize)
- Decisões identificadas
- Próximos passos / Action items
- Riscos e pontos de atenção
- Análise da ontologia (entidades criadas/atualizadas)
- Link para a transcrição completa (se arquivo grande)

### 5) Atualizar ontology (OBRIGATÓRIO)
Usar comandos da skill `ontology`:

```bash
# Criar entidades
python3 scripts/ontology.py create --type Meeting --props '{...}'
python3 scripts/ontology.py create --type Person --props '{...}'
python3 scripts/ontology.py create --type Project --props '{...}'
python3 scripts/ontology.py create --type Task --props '{...}'
python3 scripts/ontology.py create --type Decision --props '{...}'

# Criar relacionamentos
python3 scripts/ontology.py relate --from <meeting_id> --rel has_participant --to <person_id>
python3 scripts/ontology.py relate --from <meeting_id> --rel about_project --to <project_id>
python3 scripts/ontology.py relate --from <meeting_id> --rel produced_task --to <task_id>
```

### 6) Sugestão opcional (transcription para PRD)
Se a reunião discutir:
- Implementação de nova funcionalidade
- Solução técnica detalhada
- Arquitetura ou design de sistema

**Sugerir:**
> "Esta reunião discutiu implementação de [solução]. Quer que eu use a skill `transcription` para criar um PRD detalhado?"

### 7) Confirmação final
Apresentar ao Ramir:
1. Resumo executivo
2. Lista de entidades criadas/atualizadas na ontologia
3. Caminho do arquivo salvo no Obsidian
4. Sugestão de PRD (se aplicável)

## Regras obrigatórias
1. **SEMPRE** usar skill `summarize` para gerar o resumo
2. **SEMPRE** usar skill `ontology` para análise e persistência de entidades
3. **SEMPRE** salvar nota no Obsidian (`~/Obsidian`)
4. **SEMPRE** atualizar o graph.jsonl do ontology
5. **NUNCA** usar `~/vault` - apenas `~/Obsidian`
6. **NUNCA** inventar dados não presentes na transcrição (marcar como [NÃO CITADO])

## Integração com outras skills

### summarize
```bash
# Salvar transcrição em arquivo temporário
echo "<transcrição>" > /tmp/transcript.txt
summarize /tmp/transcript.txt --model google/gemini-3-flash-preview
```

### ontology
```bash
# Criar entidades do tipo Meeting
python3 scripts/ontology.py create --type Meeting \
  --props '{"title":"Reunião X","date":"2026-02-21","participants":["Alice","Bob"]}'

# Listar para confirmar
python3 scripts/ontology.py list --type Meeting

# Criar relacionamentos
python3 scripts/ontology.py relate --from meeting_001 --rel has_participant --to person_alice
```

### transcription (sugestão opcional)
Se houver discussão de implementação:
> "Sugiro usar a skill `transcription` para criar um PRD baseado nesta discussão de implementação. Deseja prosseguir?"

## Exemplo de uso

**Entrada:**
Ramir cola transcrição de reunião sobre novo projeto de website.

**Processo:**
1. Recebe transcrição
2. Roda `summarize` → gera resumo
3. Analisa com `ontology`:
   - Cria Person: "João Silva", "Maria Souza"
   - Cria Organization: "Cliente ABC"
   - Cria Project: "Website Cliente ABC", status: "planning"
   - Cria Meeting: com data, participantes, link
   - Cria Tasks: "Definir wireframes", "Orçamento hosting"
   - Cria Decision: "Usar Next.js + Tailwind"
4. Salva nota em `~/Obsidian/Meetings/2026-02-21-Reuniao-Website-Cliente-ABC.md`
5. Atualiza `memory/ontology/graph.jsonl`
6. Pergunta: "Esta reunião discutiu implementação do website. Quer criar um PRD com a skill `transcription`?"

**Saída:**
- Resumo executivo
- Lista de entidades criadas
- Caminho do arquivo no Obsidian
- Sugestão de PRD (se aplicável)

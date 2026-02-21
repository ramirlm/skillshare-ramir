---
name: oncologia-transcript
description: Processar transcrições de reuniões de Oncologia. Use quando o Ramir colar/enviar uma transcrição (PT/EN) e quiser: (1) identificar automaticamente empresa/cliente/projeto/produto discutidos (com perguntas de confirmação quando necessário), (2) reconstruir o contexto correto consultando o ClawVault/Obsidian (vault em ~/Obsidian), (3) gerar um entendimento claro do que foi discutido (resumo, decisões, próximos passos, riscos), e (4) salvar a reunião como nota estruturada no vault (pasta de Oncologia) + atualizar entidades/relacionamentos no ontology.
---

# Oncologia Transcript

## Objetivo
Transformar uma transcrição de reunião em entendimento acionável **com contexto correto** (projeto/cliente/produto), e persistir isso no **ClawVault/Obsidian (~/Obsidian)** e no **ontology**.

## Entradas esperadas
- Transcrição colada no chat (texto bruto) **ou** arquivo de texto enviado.
- Opcional: data da reunião, participantes, link (Meet/Zoom), nome do cliente/projeto (se o Ramir já souber).

## Saídas (sempre entregar)
1) **Resumo executivo** (5–10 bullets) com o contexto (empresa/cliente/projeto/produto).
2) **Decisões** (com “porquê” quando estiver claro).
3) **Próximos passos / Action items** (com dono e prazo quando citado; se não tiver, marcar como “dono: ? / prazo: ?”).
4) **Riscos, bloqueios e pontos de atenção**.
5) **Perguntas em aberto** (o que precisa confirmar com alguém).
6) **Persistência**:
   - Criar/atualizar nota da reunião no Obsidian (~/Obsidian) dentro do contexto de Oncologia.
   - Atualizar entidades/relacionamentos no ontology (Company/Client/Project/Product/People/Meeting/Task).

## Workflow (passo a passo)

### 1) Normalizar a transcrição
- Remover linhas vazias excessivas e marcações irrelevantes (ex.: “Recording started”).
- Preservar falas importantes e timestamps se existirem.
- Detectar idioma (PT/EN) para ajustar o output.

### 2) Detectar contexto automaticamente (empresa/cliente/projeto/produto)
Extrair sinais do texto:
- nomes próprios (empresas, hospitais, clínicas, squads)
- nomes de sistemas/produtos/módulos
- termos recorrentes (ex.: “implantação”, “MVP”, “integração”, “feature X”)

**Se a confiança for baixa ou houver ambiguidade** (ex.: 2 projetos possíveis), parar e perguntar **só o mínimo**:
- “Qual projeto é este?” (mostrar 2–3 candidatos)
- “Qual empresa/cliente?”
- “Qual produto/módulo?”

### 3) Reconstruir o contexto via ClawVault/Obsidian (~/Obsidian)
- Usar **ClawVault** para buscar notas anteriores relacionadas aos candidatos detectados.
- Se disponível, usar busca (qmd) por termos-chave (cliente/produto/pessoas) para achar:
  - PRDs / especificações
  - reuniões anteriores
  - decisões históricas
  - status atual do projeto
- Trazer para o output um bloco curto “Contexto anterior relevante” (3–7 bullets), citando links/caminhos das notas.

### 4) Gerar entendimento da reunião (com contexto)
- Produzir as seções de saída (Resumo, Decisões, Actions, Riscos, Perguntas).
- Quando houver conflito com contexto anterior, marcar explicitamente:
  - **[CONFLITO]** “A reunião disse X, mas a nota Y diz Z”
  - Sugerir pergunta de validação.

### 5) Persistir no Obsidian (Oncologia)
**Vault correto:** `~/Obsidian` (NUNCA `~/vault`).

Criar uma nota Markdown com **YAML frontmatter** e corpo estruturado.

**Local sugerido (ajustar ao projeto detectado):**
- `~/Obsidian/Oncologia/Meetings/` (padrão) 
- ou dentro de uma pasta do projeto, se já existir no vault.

**Nome de arquivo sugerido:**
- `YYYY-MM-DD - Reunião - <Cliente/Projeto> - <Tema curto>.md`

**Frontmatter mínimo:**
```yaml
title: "YYYY-MM-DD - Reunião - <Cliente/Projeto> - <Tema>"
date: "YYYY-MM-DD"
company: "<Empresa>"
client: "<Cliente>"
project: "<Projeto>"
product: "<Produto/Módulo>"
participants:
  - "<Nome 1>"
  - "<Nome 2>"
source: "transcript"
tags:
  - oncologia
  - meeting
processedAt: "<ISO-8601 com timezone>"
summary: "<1–2 frases>"
```

**Corpo da nota (template):**
- Contexto (antes da reunião)
- Resumo executivo
- Decisões
- Próximos passos (action items)
- Riscos/bloqueios
- Perguntas em aberto
- Transcrição (anexar no final ou linkar; se muito grande, colocar sob um H2 “Transcrição”)

### 6) Atualizar ontology
- Criar/atualizar entidades:
  - Company/Client/Project/Product (se faltarem)
  - Meeting (com data + referência ao arquivo no Obsidian)
  - Task para cada action item (com status “open”)
  - Relacionamentos (Meeting → Project, Meeting → Participants, Task → Project)

### 7) Confirmar com o Ramir
No final, perguntar 1–3 confirmações rápidas (somente se necessário):
- “Confirma que o projeto é X e o cliente é Y?”
- “Quer que eu registre estes action items no seu sistema de TODO também?” (se aplicável)

## Regras de qualidade
- Não inventar nomes/decisões: quando não estiver explícito, marcar como **[NÃO CITADO]**.
- Sempre explicitar o **grau de confiança** quando inferir projeto/cliente.
- Manter o output “executivo” no chat e o detalhe completo no Obsidian.

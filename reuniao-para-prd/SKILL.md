---
name: reuniao-para-prd
description: >-
  Transformar transcrições de reuniões (texto colado no chat ou arquivo) em: (1) insights práticos,
  (2) desafios observados e pontos cegos (o que pode estar faltando), e (3) opcionalmente um PRD
  detalhado em INGLÊS para uma feature discutida. Use quando o usuário enviar “transcrição”, “ata”,
  “meeting notes”, “reunião”, ou pedir “extrair insights/desafios” e/ou “gerar PRD”. Comando-alvo:
  /reuniao-para-prd.
---

# Reunião → PRD

## Objetivo
Converter transcrições de reuniões em entendimento acionável (em PT-BR) e, quando solicitado, produzir um PRD detalhado em inglês pronto para engenharia.

## Workflow (sempre seguir)

### 0) Entrada
1. Pedir a transcrição (ou link/arquivo) e confirmar idioma.
2. Perguntar se o output desejado é:
   - **Apenas análise** (insights + desafios/pontos cegos) ou
   - **Análise + PRD (em inglês)**.

### 1) Perguntas (PT/BR) — mínimo necessário
Fazer perguntas curtas e objetivas. **Não travar**: se faltar algo, gerar uma versão v0 e marcar lacunas.

Perguntas padrão (escolher as relevantes):
- Qual é o **contexto do produto** (app/web/API) e quem é o usuário-alvo?
- Qual é o **objetivo de negócio** (métrica/resultado) e prioridade?
- Existe **prazo** ou dependência (time, backend, terceiros)?
- Quais partes já estão decididas vs. abertas?
- Há **restrições** (tecnologia, compliance/LGPD, orçamento, performance)?
- Você quer que eu gere **um PRD para qual feature específica** (nome curto)?

### 2) Extração e síntese (PT/BR)
A partir da transcrição, produzir:

**2.1 Resumo executivo (5-10 bullets)**
- O que foi discutido, decisões e direção.

**2.2 Insights**
- Oportunidades, padrões, implicações, trade-offs, “o que isso destrava”.

**2.3 Desafios observados + pontos cegos**
- Riscos, ambiguidades, suposições não ditas.
- Perguntas que precisam de resposta para evitar retrabalho.

**2.4 Decisões, pendências e responsáveis (se houver no texto)**
- Decisões tomadas (com trechos citados quando útil)
- Open questions
- Action items

### 3) Se o usuário pedir PRD: gerar PRD em INGLÊS (detalhado)
**Regra:** perguntas continuam em PT/BR; **o PRD é sempre em inglês**.

1. Identificar claramente a **feature** e o **problema**.
2. Consolidar requisitos e preencher lacunas com:
   - “TBD” quando não der para inferir com segurança
   - ou hipóteses explícitas (“Assumption: …”) quando necessário.
3. **Usar a skill PRD-CREATOR** quando disponível no ambiente.
   - Se não estiver disponível, seguir o mesmo padrão (seções abaixo) e manter o PRD com nível de detalhe “engineering-ready”.

#### PRD template (EN)
Use este esqueleto (adaptar conforme a reunião):
- Title
- Context
- Problem Statement
- Goals (and Non-Goals)
- User Personas
- User Stories
- Requirements
  - Functional Requirements
  - Non-Functional Requirements (performance, security, privacy/LGPD, accessibility)
- UX / Flows
  - Happy path
  - Edge cases
- Data Model / Events / Tracking (if applicable)
- API / Integration Notes (if applicable)
- Acceptance Criteria (Gherkin-style when helpful)
- Rollout Plan
- Risks & Mitigations
- Open Questions / TBDs

## Output padrão (ordem)
1) Resumo executivo (PT/BR)
2) Insights (PT/BR)
3) Desafios observados + pontos cegos (PT/BR)
4) Decisões / pendências / próximos passos (PT/BR)
5) PRD (EN) — **apenas se solicitado**

## Regras de qualidade
- Não inventar fatos. Se algo não estiver na transcrição nem nas respostas do usuário: marcar como **TBD** ou **Assumption**.
- Ser específico: números, fluxos, critérios de aceite e edge cases.
- Se a transcrição estiver confusa/ruidosa: pedir uma versão “limpa” ou confirmar trechos críticos com perguntas direcionadas.

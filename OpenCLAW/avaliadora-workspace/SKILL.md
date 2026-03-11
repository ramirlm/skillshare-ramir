---
name: avaliadora-workspace
description: "Audita e avalia o workspace do Clawdbot/OpenClaw para otimização de memória e performance, com foco em sinergia entre Obsidian (ClawVault), ontology, prompts (SOUL/IDENTITY/USER), memória operacional (SESSION-STATE), crons/scheduler, configurações de LLM/modelos e organização de agentes. Use quando Ramir pedir para unificar o sistema, melhorar retenção de contexto (conhecer melhor o Ramir) e propor correções seguras (sempre pedindo confirmação antes de mudanças)."
version: 1.1.0
author: ramirlm
triggers:
  - "auditar workspace"
  - "avaliar workspace"
  - "otimizar sistema"
  - "avaliadora"
  - "auditoria do agente"
metadata:
  clawdbot:
    emoji: "🔍"
    os: ["linux", "darwin"]
---

# Avaliadora Workspace

## Objetivo (o que “otimizar sinergia” significa)
Produzir uma auditoria que otimize o sistema como um todo para:
1) **Captura confiável** do que importa (decisões, preferências, contexto de projetos)
2) **Persistência correta** (Obsidian + ClawVault + Ontology), no lugar certo (`~/Obsidian`)
3) **Recuperação útil** (o conhecimento volta para a conversa no momento certo)
4) **Auto-melhoria contínua** (loops de revisão: erros → aprendizado → patch → verificação)
5) **Experiência do Ramir** melhor (menos repetição, mais contexto, mais proatividade com controle)

## Princípios de Unificação (não-negociáveis)
- **Uma fonte de verdade para memória durável:** Obsidian (`~/Obsidian`) + Ontology.
- **Uma fonte de verdade para estado da sessão:** `SESSION-STATE.md` (WAL).
- **Prompts guiam comportamento:** `SOUL.md`, `IDENTITY.md`, `USER.md`, `AGENTS.md`, `MEMORY.md`.
- **Nada de “shadow vault”:** proibir `~/vault`, paths antigos e duplicados.
- **Mudanças com confirmação:** esta skill só propõe patches/diffs e planos. Aplicar só com “sim”.

## Regras de Segurança e Qualidade
- Não exfiltrar segredos: em relatórios, registrar apenas caminhos/nomes de arquivo e sintomas.
- Não “consertar automaticamente”: sempre pedir aprovação.
- Se um problema for ambíguo: marcar como **[UNVERIFIED]** e propor como confirmar.

## Entregáveis (sempre no Obsidian)
Esta skill deve **sempre escrever relatórios no vault** para que o ClawVault indexe.

**Pasta padrão de relatórios:**
- `~/Obsidian/Relatorios/avaliadora-workspace/`

**Arquivos sugeridos por execução (com YAML frontmatter):**
- `snapshot-YYYY-MM-DD_HHMMSS.md` (baseline técnico)
- `report-YYYY-MM-DD_HHMMSS.md` (consolidação final)
- `fix-plan-YYYY-MM-DD_HHMMSS.md` (plano de correção por etapas)

> Se a pasta/arquivos não existirem, criar. Se o Ramir pedir para seguir uma taxonomia diferente, ajustar.

## Fluxo de Trabalho (alto detalhe)

### Passo 0 — Calibrar escopo (máx. 2 perguntas)
Perguntar:
1) “Você quer **só auditoria** ou **auditoria + patches sugeridos (diff)**?”
2) “Prioridade hoje: (A) Memória/Obsidian, (B) Ontology, (C) Crons/Delivery, (D) Prompts/Config de agentes, (E) Tudo?”

Se não responder: assumir **auditoria + patches sugeridos** e prioridade **E (Tudo)**.

### Passo 1 — Snapshot determinístico (scripts)
1) Executar:
   - `scripts/collect_snapshot.sh [OUT_DIR]`
2) Gerar resumo rápido:
   - `scripts/render_report.py [OUT_DIR]`
3) Garantir que o snapshot foi persistido no Obsidian (o script escreve uma nota “snapshot-*”).

### Passo 2 — Auditoria por domínios (sub-agentes)
Criar **um sub-agente por domínio**. Cada sub-agente deve devolver:
- Achados (bullets)
- Evidências (arquivo/caminho/trecho — sem segredos)
- Impacto (baixo/médio/alto)
- Recomendações (curto prazo vs longo prazo)
- Patches sugeridos (quando aplicável)

#### Domínio 1 — Obsidian + ClawVault (principal)
Checklist de achados esperados:
- Vault correto: `~/Obsidian` (verificar se existe qualquer ocorrência de `~/vault`)
- Qualidade de notas:
  - YAML frontmatter presente (padrão: `title`, `summary`, `tags`, `processedAt`)
  - Duplicação (mesmo assunto em múltiplas notas)
  - Pastas inconsistentes (ex.: “Research” vs “Deep Researches” etc.)
- “Recuperabilidade”:
  - As notas têm títulos/summary que permitem busca semântica?
  - As notas-chave têm links entre si?
- Integração ClawVault:
  - Está indexando o vault correto?
  - Há erros/atrasos recorrentes de index?
  - Propor rotina: **sempre que escrever relatório → indexar**.

#### Domínio 2 — Ontology (memória estruturada)
- Verificar se as entidades essenciais existem e estão conectadas:
  - Person: Ramir
  - Projetos ativos
  - Preferências (canais, formatação, taxonomia)
- Checar problemas típicos:
  - fatos duplicados
  - entidades órfãs
  - naming inconsistente
- Propor “regras de persistência”:
  - que tipo de coisa vai para ontology vs nota Obsidian
  - como linkar `Document` (nota) ↔ `Project` ↔ `Person`

#### Domínio 3 — Prompts / SOUL / MEMORY / SESSION-STATE (sinergia comportamental)
Auditar a consistência entre:
- `SOUL.md`: estilo/idioma (“Lenovo: ...”), tom, limites
- `MEMORY.md`: regras (confirmar antes de agir, não mexer em configs sem permissão)
- `AGENTS.md`: regras de workspace e WAL
- `SESSION-STATE.md`: se está sendo atualizado quando o usuário dá fatos/decisões
- `USER.md`: preferências (Obsidian, relatórios, horários)

Achados comuns:
- regras conflitantes (ex.: pastas proibidas vs usadas)
- falta de “gatilhos” claros (quando salvar em ontology/clawvault)
- falta de templates de relatório

Propor patches:
- clarificar uma “hierarquia de persistência”
- templates curtos para capturar decisão/preferência/projeto

#### Domínio 4 — Crons / Scheduler / Delivery
Verificar:
- jobs enabled com `lastStatus=error` e `consecutiveErrors`
- problemas de delivery (canais desativados, announce failed)
- jobs obsoletos (disabled antigos, deleteAfterRun já executados)
- wakeMode incorreto (especialmente quando houver `sessions_spawn`)
- consistência de timezone

Saída esperada:
- tabela “jobs quebrados” + provável causa
- plano: desativar/ajustar delivery/canal
- proposta de limpeza (sem executar)

#### Domínio 5 — Configuração de LLMs / modelos / timeouts
Verificar:
- modelos inconsistentes em jobs parecidos
- jobs críticos com modelo pesado desnecessário
- timeouts curtos que causam falhas
- “fallback” e estratégia de confiabilidade

#### Domínio 6 — Agentes (arquitetura e governança)
Verificar:
- agentes existentes vs uso real
- allowlists de sub-agentes (main → quem pode chamar)
- sessões zumbis / runs antigos
- mapeamento de tópicos/canais (ex.: Telegram topics)

Saída:
- “mapa do sistema”: agentes ↔ responsabilidades ↔ crons ↔ outputs no Obsidian

### Passo 3 — Consolidação (relatório final)
Gerar e salvar no Obsidian um `report-*.md` com:
1) **Top 10 problemas** (Impacto x Facilidade)
2) **Plano de correção** por etapas (ordem sugerida)
3) **Patches sugeridos** (diff/trechos) com risco e rollback
4) **Perguntas abertas** (o que precisa confirmação do Ramir)

### Passo 4 — Indexação ClawVault (obrigatório)
Após **qualquer** escrita de relatório/artefato no Obsidian, executar a indexação do ClawVault para garantir que o conhecimento passa a ser recuperável na conversa.

**Comando ideal (rápido + determinístico):**
- `clawvault graph --refresh --vault ~/Obsidian`

Opcional (quando você criou/atualizou muitos links wiki e quer melhorar conectividade do grafo):
- `clawvault link --all --vault ~/Obsidian`

Regras:
- **Sempre** passar `--vault ~/Obsidian` (ambientes não-interativos/cron podem não carregar `.zshrc`, deixando `CLAWVAULT_PATH` vazio).
- Se falhar, registrar erro no relatório como **[UNVERIFIED]** e sugerir:
  - `clawvault doctor --vault ~/Obsidian`

### Passo 5 — Loop de auto-melhoria (obrigatório)
Para cada erro recorrente encontrado (ex.: cron delivery, vault path, regras conflitantes):
- registrar como “Lição” no relatório
- propor patch em: prompt/config/script
- definir uma verificação rápida pós-patch

## Scripts
- `scripts/collect_snapshot.sh` — coleta snapshot (status/crons/config/grep) e persiste nota snapshot no Obsidian.
- `scripts/render_report.py` — resumo Markdown do snapshot.

## Observação importante sobre pastas
Evitar `~/Obsidian/OpenClaw/***` (quando houver regra vigente para não usar). Usar `~/Obsidian/Relatorios/avaliadora-workspace/` por padrão.

---
title: Segurança MOC
description: Cluster de skills para proteção do agente, defesa contra injeção de prompt, monitoramento de ameaças e triagem diária de segurança.
updated: 2026-03-14
---

# Segurança

Cluster para manter o agente e o sistema protegidos.

## Defesa do Agente

- [[prompt-guard]] — sistema avançado de defesa contra injeção de prompt
  - Atuar em: group chats com usuários não confiáveis, detectar manipulação, restringir comandos sensíveis ao owner, logar eventos de segurança
  - Suporte multi-idioma
  - **Este agente opera em grupo → prompt-guard é relevante**

## Monitoramento de Ameaças

- [[clawsec]] — suite ClawSec com monitoring de advisory feed, resposta a skills maliciosas e setup guiado
  - v0.0.9 | homepage: clawsec.prompt.security
- [[moltthreats]] — feed de sinais de segurança por PromptIntel
  - Usar para: reportar ameaças, buscar feeds de proteção, aplicar regras de segurança, atualizar `shield.md`

## Triagem Diária

- [[daily-security-triage]] — triagem local de segurança (shell profile injection + indicadores de persistência) + resumo por email
  - Rodar diariamente ou via cron
  - Output: email com resumo da triagem

## Quando acionar

| Situação | Skill |
|---------|-------|
| Mensagem suspeita no grupo | `prompt-guard` |
| Review periódica de segurança | `daily-security-triage` |
| Nova skill de fonte desconhecida | `clawsec-suite` |
| Ameaça reportada no ecossistema | `moltthreats` |

## Relacionados

- Para manutenção geral do agente → [[../agents/MOC]]
- Para update seguro do sistema → [[../integrations/MOC]] (update-plus)

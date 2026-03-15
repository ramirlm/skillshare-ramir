---
title: prompt-guard + clawsec + moltthreats
description: Defesa contra injeção de prompt, suite de segurança e feed de ameaças para proteger o agente.
updated: 2026-03-14
---

# Proteção do Agente

## prompt-guard

Defesa contra prompt injection em ambientes de grupo ou com usuários não confiáveis.

**Capacidades:**
- Detectar tentativas de injeção direta e indireta
- Detectar manipulação
- Restringir comandos sensíveis ao owner (Ramir)
- Logar eventos de segurança
- Detecção multi-idioma

**Ativo por padrão em:** group chats (como este Telegram)

## clawsec-suite (v0.0.9)

Suite de segurança com:
- Monitoring de advisory feed
- Resposta com aprovação obrigatória para skills maliciosas
- Setup guiado de skills de segurança adicionais

Homepage: clawsec.prompt.security

## moltthreats (PromptIntel)

Feed de sinais de segurança específicos para agentes AI.

**Usar quando:**
- Reportar ameaça detectada
- Buscar feeds de proteção atualizados
- Aplicar novas regras de segurança
- Atualizar `shield.md` com novos padrões

## Relacionados

- Para triagem diária → [[daily-security-triage]]
- Para manutenção do agente → [[../agents/MOC]]

# 🛠️ Clawdbot Skills Repository

**Localização**: `~/clawdbot-skills/`  
**Última atualização**: 2026-02-01

## 📚 Skills Disponíveis (32)

### Browser & Web
- `agent-browser-clawdbot/` - Browser automation optimized for AI agents
- `browser-use/` - Browser automation utilities
- `playwright-cli/` - Playwright CLI integration

### Email & Communication
- `email/` - Email management
- `twitter/` - Twitter/X integration
- `x-api/` - X (Twitter) API integration

### AI & Search
- `xai/` - xAI integration
- `xai-search/` - xAI search capabilities
- `grok-query/` - Query Grok models
- `deep-research/` - Deep research agent
- `perplexity/` - Perplexity integration

### Documentation & Docs
- `clawd-docs-v2/` - Clawdbot documentation access
- `youtube-transcript/` - YouTube transcript fetcher

### Development & Tools
- `clawdbot-backup/` - Backup and restore
- `backup/` - General backup utilities
- `clawhub/` - ClawHub CLI
- `dashboard/` - Task management dashboard
- `prd/` - PRD utilities
- `prd-executor/` - Execute PRD coding tasks

### Security & Safety
- `prompt-guard/` - Prompt injection defense
- `clawdbot-security-check/` - Security validation

### Memory & Learning
- `bulletproof-memory/` - Write-Ahead Log protocol
- `self-improving-agent/` - Continuous improvement

### Specialized Agents
- `assessor-juridico/` - Legal process manager (Portuguese)
- `resumidor-auto/` - Auto summarizer (Portuguese)
- `todo-list-manager/` - TODO list management (Portuguese)
- `video-bug-prompt/` - Video bug analysis

### Meta & Utilities
- `cron-creator/` - Create cron jobs from natural language
- `find-skills/` - Discover and install skills
- `skill-evaluator/` - Evaluate skill quality
- `update-plus/` - Update with auto-rollback
- `blogwatcher/` - Blog monitoring

## 📝 Como Usar

### Instalar uma skill no agente
```bash
# Copiar para o workspace do agente
cp -r ~/clawdbot-skills/{skill-name} ~/clawdbot-agents/{agent-name}/

# OU criar symlink
ln -s ~/clawdbot-skills/{skill-name} ~/clawdbot-agents/{agent-name}/
```

### Adicionar nova skill
```bash
# Criar nova skill em ~/clawdbot-skills/
mkdir ~/clawdbot-skills/minha-skill
cd ~/clawdbot-skills/minha-skill

# Criar estrutura básica
touch SKILL.md README.md
```

### Publicar skill no ClawdHub
```bash
cd ~/clawdbot-skills/{skill-name}
clawhub publish
```

## 🔄 Sincronização

Este diretório é a **fonte da verdade** para skills customizadas.
- Skills do ClawdHub instaladas vão para `~/.clawdbot/skills/` (global)
- Skills customizadas/desenvolvidas ficam aqui em `~/clawdbot-skills/`

## 📦 Backup

Skills são incluídas no backup regular do workspace.
Considere versionar este diretório com git:

```bash
cd ~/clawdbot-skills
git init
git add .
git commit -m "Initial skills repository"
```

## 🆘 Troubleshooting

**Skill não carrega**: Verifique se o SKILL.md existe e está bem formatado
**Permissões**: `chmod +x` em scripts executáveis
**Dependências**: Algumas skills precisam de pacotes npm/pip instalados

## 📖 Documentação

- [Skill Creator Guide](./skill-creator/SKILL.md)
- [ClawdHub Docs](https://clawdhub.com/docs)
- [Clawdbot Docs](https://docs.clawd.bot)

---

**Total**: 32 skills consolidadas  
**Estrutura atualizada**: 2026-02-01 por Lenovo ✨

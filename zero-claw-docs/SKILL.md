---
name: zero-claw-docs
description: Documento operacional da configuração do ZeroClaw do Ramir (rodando via Docker), com comandos de diagnóstico, provedores e modelos pelo cli do container.
metadata:
  requires:
    bins: [docker]
---

# Zero Claw Docs

Esta skill documenta **apenas o perfil operacional atual do ZeroClaw usado pelo Ramir** (execução via Docker).

## Regras de uso desta skill

- Todo comando daqui é **via Docker/containers** (sem uso direto de `zeroclaw` no host).
- Container padrão: `zeroclaw`
- Configuração principal conhecida: `/root/zeroclaw-vps/.zeroclaw/config.toml` (ajustada no host e montada no container)
- Compose geralmente em `/root/zeroclaw-vps/docker-compose.yml`
- Quando for validar/provar comportamento no runtime, use:
  - `docker logs zeroclaw`
  - `docker exec -i zeroclaw zeroclaw ...`

## Contexto atual conhecido da sua instância

### Padrões que já funcionaram

- `default_provider = "kimi-code"`
- `default_model = "kimi-for-coding"` (modelo padrão inicial aceito pelo provider)
- Fallback já testado em config local: `fallback_providers = ["openai-codex"]`

### Erro já encontrado (mapeado)

- Erro de inicialização recorrente:
  - `TOML parse error ... missing field 'cli'` em
  - `channels_config`
- Correção: incluir **sempre** `cli = true` em `[channels_config]`.

- Erro de provider recente:
  - `thinking is enabled but reasoning_content is missing in assistant tool call`
  - Modelo pedido `kimi-k2.5-ultrathink` não é a forma recomendada para o provider `kimi-code` na base de docs consultada.
  - Recomendações:
    1. usar `kimi-for-coding` (ou `kimi-k2.5`) em `default_model`
    2. manter `reasoning_enabled` desativado durante testes (`false`)

## Estrutura de configuração Docker esperada (resumo)

No host (`/root/zeroclaw-vps/.zeroclaw/config.toml`):

```toml
workspace = "/zeroclaw-data/workspace"

default_provider = "kimi-code"
default_model = "kimi-for-coding"

[reliability]
provider_retries = 2
provider_backoff_ms = 500
fallback_providers = ["openai-codex"]

[runtime]
# Durante testes de estabilidade de models/reasoning pode ficar: false
reasoning_enabled = false

[channels_config]
cli = true
message_timeout_secs = 300

[channels_config.telegram]
bot_token = "SEU_TELEGRAM_BOT_TOKEN"
allowed_users = ["*"]
stream_mode = "off"
interrupt_on_new_message = false
```

> Ajuste `allowed_users` para IDs quando sair de modo de debug.

## Comandos oficiais úteis (Docker-first)

### 1) Diagnóstico geral

```bash
# status do container
docker logs --tail 120 zeroclaw

docker exec -i zeroclaw zeroclaw status

docker exec -i zeroclaw zeroclaw channel list
docker exec -i zeroclaw zeroclaw channel doctor
```

### 2) Lista e descoberta de providers/modelos

```bash
# lista providers descobertos + ativos

docker exec -i zeroclaw zeroclaw providers

docker exec -i zeroclaw zeroclaw models

docker exec -i zeroclaw zeroclaw models refresh

docker exec -i zeroclaw zeroclaw models refresh --provider kimi-code

docker exec -i zeroclaw zeroclaw models refresh --provider kimi-code --force
```

### 3) Reconfiguração rápida

```bash
# reinicia só o serviço zeroclaw
cd /root/zeroclaw-vps
docker compose down zeroclaw
docker compose up -d zeroclaw

# valida pós-restart
sleep 8
docker logs --tail 120 zeroclaw

docker exec -i zeroclaw zeroclaw status
```

### 4) Testes de canal Telegram (após `channel start`)

```text
/model
/models
/models kimi-code
/model kimi-for-coding
```

## Provedores e modelos (Open src)

### Providers conhecidos (subset relevante)

- `kimi-code` (alias: `kimi_coding`, `kimi_for_coding`)
- `openrouter`, `openai`, `anthropic`, `qwen`, `glm`, `gemini`, `nvidia`, etc.

### Credenciais por provider (padronizadas no ZeroClaw)

- `kimi-code`: `KIMI_CODE_API_KEY` (fallback `MOONSHOT_API_KEY`)
- OpenAI-style: `OPENAI_API_KEY`, etc.

### Modelos Kimi Code

- `kimi-for-coding` (padrão de onboarding)
- `kimi-k2.5` (alternativa)

## Checklist de “não funcionar” (fast fix)

1. **Container em restart loop** → `docker logs --tail 200 zeroclaw`
2. **Erro TOML parse em `channels_config`** → validar `cli` presente em `[channels_config]`
3. **Erro de model/think** → evitar `kimi-k2.5-ultrathink` com `kimi-code` e usar `kimi-for-coding`/`kimi-k2.5`
4. **Channel não responde** → validar `channels_config.telegram` + `allowed_users` + `zeroclaw channel doctor`
5. **Permissão de config** → checar `chmod 600 .zeroclaw/config.toml`

## Observação importante

Esta skill registra o perfil do ambiente atual do Ramir (Docker) e deve ser usada como base para troubleshooting rápido. Se houver necessidade de mudar para outros providers/modelos, aplicar sempre primeiro com `docker exec -i zeroclaw zeroclaw models refresh --provider <id>` antes de validar resposta em produção.
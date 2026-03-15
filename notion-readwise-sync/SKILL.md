---
name: notion-readwise-sync
description: Sync (READ-ONLY) a Notion Readwise Library database (nested in a Readwise page) into the Obsidian vault as curated Markdown notes with ontology-ready frontmatter. Designed for cron + manual runs. Ignores Tweets; prioritizes Books, PDFs, Videos, Articles, Podcasts.
---

# /notion-readwise-sync

Objetivo: integrar **todo o banco “Library” (Readwise)** que está **aninhado** dentro de uma página do Notion, para a base de conhecimento do Obsidian, **sem escrever nada no Notion (read-only)**.

## Regras do Ramir (fonte: conversa)
- Notion: **somente leitura** (NUNCA criar/editar páginas, databases ou propriedades).
- Curadoria: Lenovo deve **analisar e curar**.
- Ontologia:
  - Sempre incluir **frontmatter YAML** “ontology-ready” quando relevante.
  - Além disso, produzir artefatos para posterior ingestão em grafo (opcional).
- Prioridades de categoria:
  - **Incluir**: Books, PDFs, Videos, Articles, Podcasts.
  - **Ignorar**: Tweets.

## Onde salva (Obsidian)
- Vault root (default): `/home/rlmit/Obsidian`
- Destino:
  - `Knowledge/Readwise/Livros/`
  - `Knowledge/Readwise/PDFs/`
  - `Knowledge/Readwise/Videos/`
  - `Knowledge/Readwise/Artigos/`
  - `Knowledge/Readwise/Podcasts/`
  - (Tweets não são gerados)

## Política de linking (obrigatória)

Ver `~/clawdbot-agents/main/memory/vault-linking-policy.md` — regra completa.

**Resumo crítico:**
- Toda nota deve ter `owner: ramir` e `people: [ramir]` no frontmatter (proprietário do vault)
- **NUNCA rodar `clawvault link --all`** — causa links espúrios em PT-BR
- Linking feito exclusivamente via frontmatter (`people`, `projects`, `related`, `owner`, `topics`)
- Somente slugs reais: verificar se `Obsidian/people/<slug>.md` existe antes de referenciar

## Como a skill funciona (alto nível)
1) Descobre/usa a página âncora do Notion (Readwise page) e encontra o **child database “Library”**.
2) Resolve o **data_source_id** e faz queries por `Category` (exceto Tweets).
3) Para cada item:
   - Gera/atualiza uma nota Markdown **idempotente** (1 item → 1 arquivo).
   - Inclui frontmatter com IDs do Notion, categoria, url original, tags do Readwise.
4) Curadoria:
   - Define `relevance` (low/med/high) e `next_action`.
   - Para Books/PDFs/Videos: sempre criar um bloco “Resumo/Insights/Aplicações”.
   - Gera diff por execução para auditoria de mudanças (adicionado x atualizado x inalterado).
5) Ontologia:
   - Preenche campos sugeridos no frontmatter (topics, people, companies, projects).
   - Emite candidatos de entidades/links em `Knowledge/Readwise/_ontology-candidates/*.json` (somente local) em toda adição/atualização.
   - Gera artefato de ontologia por run em `Knowledge/Readwise/_state/runs/<RUN_ID>/ontologized.jsonl`.

## Comandos
### Rodar manual (recomendado para testar)
```bash
python3 /home/rlmit/clawdbot-skills/notion-readwise-sync/scripts/sync_readwise.py \
  --vault /home/rlmit/Obsidian \
  --page-id 4c43c451-fdfc-4066-871b-310cbf477fdf \
  --db-title "Library" \
  --limit-per-category 30 \
  --since-days 0
```

### Rodar no cron (mesma coisa)
No cron payload, chamar o mesmo script com parâmetros fixos, deixando `--since-days 0` para import completo (sem recorte por janela).

## Config / Credenciais
- Requer `NOTION_API_KEY` (ou `~/.config/notion/api_key`) com acesso à página Readwise.
- NUNCA logar a chave.

## Saídas importantes
- `Knowledge/Readwise/_state/index.json` (mapeia `notion_page_id -> vault_path` + `content_hash`)
- `Knowledge/Readwise/_state/last-run.json` (resumo da última execução)
- `Knowledge/Readwise/_state/runs/<RUN_ID>/summary.json` (itens adicionados/atualizados/skipped + diffs)
- `Knowledge/Readwise/_state/runs/<RUN_ID>/diff.jsonl` (diff dos itens atualizados)
- `Knowledge/Readwise/_state/runs/<RUN_ID>/ontologized.jsonl` (payload de ontologia gerado no run)
- `Knowledge/Readwise/_ontology-candidates/*.json` (candidatos de entidade por item)

## Troubleshooting rápido
- `404 object_not_found` em um item do Notion: o item **não está compartilhado** com a integração usada pela chave atual. (Ex.: chave errada / integração diferente).
- Se “Readwise page_id” der 404, verifique qual integração/NOTION_API_KEY está em uso.



## Execução via cron
Use o runner padrão para automação:
- `python3 /home/rlmit/clawdbot-skills/notion-readwise-sync/scripts/run_sync.sh`
- `run_sync.sh` já executa `materialize_ontology_entities.py --canonical --no-wiki` após o sync para manter links semânticos estritos.

Cron ativa criada:
- Nome: `notion-readwise-sync (hybrid 2x/dia)`
- Agenda: `30 7,21 * * *` (America/Fortaleza)
- Job ID: `f01804b1-600d-449c-8e74-6655aa2da288`

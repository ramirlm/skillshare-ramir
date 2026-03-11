# 🚀 Quick Start — Leitura Espaçada

## Instalação (1 minuto)

```bash
# 1. Clonar ou copiar para skills
cp -r ~/clawdbot-skills/leitura-espacada ~/Obsidian/leitura

# 2. Adicionar ao PATH (opcional)
echo 'export PATH="$HOME/Obsidian/leitura/scripts:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Primeiros Passos

### 1. Inicializar Coleção

```bash
leitura init minha-colecao
```

### 2. Adicionar Primeiro Card

```bash
leitura add "Título" "Pergunta?" "Resposta" "tema1,tema2"

# Exemplo real:
leitura add "João 3:16" \
  "Qual o versículo mais conhecido?" \
  "Porque Deus amou o mundo de tal maneira..." \
  "amor,salvacao"
```

### 3. Revisar Amanhã

```bash
leitura due     # Ver pendentes
leitura study   # Modo interativo
```

---

## 📊 Fluxo Diário

```
Manhã:   leitura add ...
Noite:   leitura study
```

---

## 🎯 Coleções Sugeridas

| Coleção | Uso |
|---------|-----|
| `biblia` | Evangelho do Dia |
| `livros` | Resumos de livros |
| `tech` | Documentação técnica |
| `artigos` | Artigos científicos |
| `idiomas` | Vocabulário |

---

## 🔗 Com Ontology + ClawVault

```bash
# Sincronizar com Ontology
node ~/clawdbot-skills/leitura-espacada/scripts/ontology-sync.js sync

# Ou configure no cron diário
```

---

**Pronto!** 🎉 Comece com `leitura init`.

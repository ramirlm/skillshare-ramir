# Fluxo Completo — Evangelho do Dia

## Configuração Inicial

```bash
# Uma vez
leitura init biblia

# Definir coleção padrão
echo 'export LEITURA_COLLECTION=biblia' >> ~/.bashrc
source ~/.bashrc
```

---

## Fluxo Diário

### Manhã (7h)

```bash
# Adicionar evangelho do dia
leitura add "Mateus 6:9-13" \
  "Qual a oração que Jesus ensinou?" \
  "Pai Nosso que estais nos céus..." \
  "oracao,pai-nosso,sermao-da-montanha"
```

### Tarde (19h)

```bash
# Ver pendentes
leitura due

# Estudar
leitura study
```

---

## Script de Automação

Crie `~/adicionar-evangelho.sh`:

```bash
#!/bin/bash
# Adicionar evangelho do dia

data=$(date +%Y-%m-%d)
read -p "Referência: " ref
read -p "Texto: " texto
read -p "Temas: " temas

leitura add "$ref" \
  "Qual o Evangelho de $data?" \
  "$texto" \
  "$temas"
```

---

## Relatório Semanal

```bash
# Domingo à noite
leitura stats
leitura backup
```

---

## Integração com Ontology

```bash
# Após adicionar cards
node ~/clawdbot-skills/leitura-espacada/scripts/ontology-sync.js sync

# Agora você pode:
# - Ver cards por tema
# - Ver relacionamentos
# - Buscar no grafo
```

---

**Meta:** 100 cards em 3 meses = ~1 evangelho por dia

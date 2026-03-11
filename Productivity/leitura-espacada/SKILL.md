---
name: leitura-espacada
description: "Sistema de leitura com Repetição Espaçada. Use quando: (1) Quiser estudar conteúdo com retenção de longo prazo, (2) Criar cards de estudo de qualquer tema, (3) Implementar revisões espaçadas em leituras diárias, (4) Organizar conhecimento por temas com algoritmo SM-2 simplificado."
version: 1.0.0
author: ramirlm
triggers:
  - "leitura espaçada"
  - "repetição espaçada"
  - "criar card"
  - "revisar cards"
  - "estudar hoje"
  - "spaced repetition"
metadata:
  clawdbot:
    emoji: "📚"
    os: ["linux", "darwin", "windows"]
    requires:
      bins: ["node"]
---

# Leitura Espaçada 📚

Sistema de estudo com **Repetição Espaçada** para fixação duradoura do conhecimento. 

Funciona com qualquer tipo de conteúdo: Bíblia, livros, artigos, documentação técnica, etc.

## Quando Usar

- Estudar o **Evangelho do Dia** da Igreja Católica
- Ler livros e criar cards de revisão
- Estudar documentação técnica
- Memorizar qualquer conteúdo importante
- Organizar conhecimento por **temas**

## Requisitos

- Node.js (para scripts)
- Obsidian Vault configurado com ClawVault
- Ontology skill para graph de conhecimento

## Instalação

```bash
# A skill já cria a estrutura automaticamente na primeira execução
# ou inicialize manualmente:

mkdir -p ~/Obsidian/leitura/{cards,revisao,temas,scripts}
cp {baseDir}/scripts/*.js ~/Obsidian/leitura/scripts/
cp {baseDir}/scripts/*.sh ~/Obsidian/leitura/scripts/
```

> Substitua `~/Obsidian/leitura` por `$LEITURA_VAULT_PATH` se preferir outro caminho.

## Estrutura Criada

```
~/Obsidian/leitura/
├── cards/              # Cards de estudo (JSON)
│   └── card_xxx.json
├── revisao/            # Histórico de revisões
│   └── review_xxx.json
├── temas/              # Estudos temáticos (Markdown)
│   └── tema-xxx.md
├── scripts/
│   ├── spaced-repetition.js
│   ├── leitura-cli.sh
│   └── daily-reminder.sh
├── templates/
│   ├── card-template.md
│   └── content-template.md
└── README.md
```

## Comandos

### Adicionar Conteúdo

```bash
# Modo interativo (recomendado)
leitura add

# Direto
leitura add "Título" "Pergunta" "Resposta" "tema1,tema2"
```

### Revisar

```bash
# Ver cards pendentes
leitura due

# Revisar um card específico
leitura review <card_id> <performance>
# performance = again | hard | good | easy

# Modo estudo interativo
leitura study
```

### Acompanhar

```bash
# Estatísticas
leitura stats

# Próximas revisões
leitura next

# Backup
leitura backup
```

## Algoritmo de Repetição Espaçada

**Intervalos simplificados:**

| Nível | Intervalo | Significado |
|-------|-----------|-------------|
| 0 | 1 dia | 🌱 Novo |
| 1 | 3 dias | 🌿 Aprendendo |
| 2 | 7 dias | 🌳 Consolidando |
| 3 | 14 dias | 🌲 Refinando |
| 4 | 30 dias | 🏛️ Maduro |
| 5 | 60 dias | 💎 Sólido |
| 6 | 120 dias | ✨ Arquivado |

### Performance

- `again` → Volta ao nível 0 (esqueceu)
- `hard` → Desce 1 nível (difícil)
- `good` → Sobe 1 nível (lembrou bem)
- `easy` → Sobe 2 níveis (lembrou fácil)

## Integração com Ontology

A skill cria automaticamente entidades no Ontology:

- **StudyCard** — Cards de estudo
- **ContentItem** — Conteúdo original
- **ReviewSession** — Sessões de revisão
- **Theme** — Temas temáticos

Relações criadas:
```
StudyCard → card_has_theme → Theme
StudyCard → card_has_reviews → ReviewSession
ContentItem → content_has_cards → StudyCard
```

## Uso com Bíblia

Para uso específico com Evangelho do Dia:

```bash
# Configure uma coleção específica
leitura init --collection biblia --themes "bem-aventurancas,perdao,fe,oracao"

# Adicione evangelhos
leitura add --source "Evangelho do Dia" --date $(date +%Y-%m-%d)
```

## Uso com Livros

```bash
# Iniciar coleção de livro
leitura init --collection "livro-nome"

# Adicionar capítulos como cards
leitura add "Cap 1: Introdução" "Qual a tese principal?" "..." "introducao"
```

## Configuração

Variáveis de ambiente:

```bash
# Opcional: caminho customizado
export LEITURA_VAULT_PATH="~/Obsidian/leitura"

# Opcional: usar com ClawVault
export CLAWVAULT_PATH="~/Obsidian"
```

## Scripts de Automação

### Cron diário

```bash
# Adicionar ao crontab
0 7 * * * ~/Obsidian/leitura/scripts/daily-reminder.sh
```

### Hook ClawVault

O sistema integra-se automaticamente com ClawVault para:
- Checkpoints antes de sessões longas
- Recuperação de contexto
- Backup automático

## Exemplos

### Exemplo 1: Evangelho do Dia

```bash
leitura add "Mateus 5:3-10" \
  "Quais as bem-aventuranças?" \
  "1. Pobres de espírito..." \
  "bem-aventurancas,sermao-da-montanha"
```

### Exemplo 2: Livro de Negócios

```bash
leitura add "Atomic Habits - Cap 1" \
  "Qual a equação do hábito?" \
  "Cue + Craving + Response + Reward" \
  "produtividade,habitos"
```

### Exemplo 3: Documentação Técnica

```bash
leitura add "React Hooks - useEffect" \
  "Quando useEffect executa?" \
  "Após renderização, quando dependências mudam" \
  "react,javascript"
```

## Fluxo de Trabalho Diário

1. **Adicionar** conteúdo novo (manhã)
2. **Revisar** cards pendentes (tarde/noite)
3. **Acompanhar** estatísticas (semanal)

## Metas Sugeridas

- **Diária**: Adicionar 1-3 cards
- **Revisão**: 10-20 cards por dia
- **Meta**: 100 cards em 3 meses
- **Maduro**: 50+ cards nível 4+

## Resolução de Problemas

### Cards não aparecem para revisão

```bash
leitura due --all  # Ver todos, inclusive futuros
```

### Resetar um card

```bash
leitura reset <card_id>  # Volta ao nível 0
```

### Exportar dados

```bash
leitura export --format json --output backup-$(date +%Y%m%d).json
```

## Referências

- [Repetição Espaçada - Wikipedia](https://pt.wikipedia.org/wiki/Repeti%C3%A7%C3%A3o_espacial)
- ClawVault: `clawvault docs`

## Tratamento de Erros

- **Node.js não instalado**: Informar e guiar instalação (`brew install node` / `apt install nodejs`)
- **Vault não encontrado**: Perguntar ao usuário o caminho correto e oferecer criar a estrutura
- **Card não encontrado**: Listar os cards mais recentes e pedir confirmação
- **Exportação falhou**: Tentar salvar em `/tmp/leitura-backup-YYYYMMDD.json` e informar o usuário
- **Ontology indisponível**: Continuar operando no modo local (sem criar entidades no grafo)
- **`leitura` não encontrado no PATH**: Orientar o usuário a usar o caminho completo (`~/Obsidian/leitura/scripts/leitura-cli.sh`)

## Sessão de Estudo Interativa

Quando o usuário disser "estudar agora" ou "iniciar revisão", o fluxo deve ser:

1. Verificar quantos cards estão pendentes: `leitura due`
2. Se 0 cards: "Nenhum card para revisar hoje! 🎉 Quer adicionar novo conteúdo?"
3. Se > 20 cards: Perguntar "Você tem [N] cards para revisar. Quer revisar todos ou limitar a [15]?"
4. Para cada card: mostrar a pergunta, aguardar resposta do usuário, mostrar a resposta correta, pedir avaliação (again/hard/good/easy)
5. Ao final: exibir resumo da sessão (acertos, evolução de nível, próxima revisão)

---

*Skill criada em 2026-02-17*

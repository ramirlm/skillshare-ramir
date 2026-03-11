# Exemplos de Coleções

## 📖 Bíblia (Evangelho do Dia)

```bash
# Inicializar
leitura init biblia
export LEITURA_COLLECTION=biblia

# Adicionar evangelho
leitura add "Mateus 5:3-10" \
  "Quais são as bem-aventuranças?" \
  "1. Pobres de espírito... 2. Mansos..." \
  "bem-aventurancas,sermao-da-montanha"
```

---

## 📚 Livros

```bash
leitura init livros
export LEITURA_COLLECTION=livros

# Atomic Habits
leitura add "Atomic Habits - Cap 1" \
  "Qual a equação do hábito?" \
  "Comportamento = Motivation + Ability + Prompt" \
  "habitos,produtividade"

# Pai Rico Pai Pobre
leitura add "Pai Rico - Lição 1" \
  "Qual a diferença entre ativo e passivo?" \
  "Ativo coloca dinheiro no bolso. Passivo tira." \
  "financas,investimentos"
```

---

## 💻 Tecnologia

```bash
leitura init tech
export LEITURA_COLLECTION=tech

# React Hooks
leitura add "React useEffect" \
  "Quando useEffect executa?" \
  "Após renderização, quando dependências mudam" \
  "react,javascript,hooks"

# Docker
leitura add "Docker - Volumes" \
  "Qual a diferença entre bind mount e volume?" \
  "Bind mount: path host. Volume: gerenciado pelo Docker." \
  "docker,devops"
```

---

## 🌍 Idiomas

```bash
leitura init ingles
export LEITURA_COLLECTION=ingles

leitura add "Phrasal Verb: Give up" \
  "O que significa 'give up'?" \
  "Desistir, abandonar (ex: Don't give up!)" \
  "phrasal-verbs"
```

---

## 📄 Artigos

```bash
leitura init artigos
export LEITURA_COLLECTION=artigos

leitura add "Artigo: Deep Work" \
  "O que é 'Deep Work' segundo Cal Newport?" \
  "Trabalho focado sem distrações em habilidades cognitivamente exigentes" \
  "produtividade,foco"
```

---

## 🎓 Estudos

```bash
leitura init estudos
export LEITURA_COLLECTION=estudos

# Catecismo
leitura add "Catecismo - Artigo 1" \
  "Por que Deus se revelou?" \
  "Para fazer os homens participantes da natureza divina" \
  "catecismo,revelacao"
```

---

## 🔄 Usando Múltiplas Coleções

```bash
# Coleção padrão
export LEITURA_COLLECTION=biblia
leitura stats

# Outra coleção temporariamente
LEITURA_COLLECTION=livros leitura stats

# Ou
cd ~/Obsidian/leitura/biblia && leitura due
cd ~/Obsidian/leitura/livros && leitura due
```

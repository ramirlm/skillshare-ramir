# Integração com Google Calendar via GOG

## Visão Geral

O TODO List Manager integra com Google Calendar através da skill `gog` para:
- Criar eventos a partir de tarefas com data/hora específica
- Consultar compromissos da semana/dia
- Enviar convites para participantes
- Gerenciar lembretes

## Comandos Principais GOG

### Listar Eventos

```bash
# Próximos 7 dias
gog calendar list

# Próximos 30 dias
gog calendar list --days 30

# Eventos de hoje
gog calendar list --today

# Eventos da semana
gog calendar list --week

# Filtrar por calendário específico
gog calendar list --calendar "Trabalho"
```

### Criar Evento

```bash
# Evento simples
gog calendar add \
  --summary "Reunião com Cliente" \
  --start "2024-01-20 14:00" \
  --end "2024-01-20 15:00"

# Evento com descrição e local
gog calendar add \
  --summary "Jantar Aniversário" \
  --start "2024-01-15 19:00" \
  --end "2024-01-15 21:00" \
  --description "Aniversário da Maria - Restaurante XYZ" \
  --location "Rua ABC, 123 - Fortaleza"

# Evento com participantes (FAMÍLIA)
gog calendar add \
  --summary "Missa Domingo" \
  --start "2024-01-21 09:00" \
  --end "2024-01-21 10:00" \
  --attendees "ramir.mesquita@gmail.com,virnavcv@gmail.com" \
  --description "Missa paroquial"

# Evento de trabalho (só Ramir)
gog calendar add \
  --summary "Sprint Planning" \
  --start "2024-01-22 10:00" \
  --end "2024-01-22 11:30" \
  --attendees "ramir.mesquita@gmail.com" \
  --description "Planejamento sprint 2024.02"

# Evento dia inteiro
gog calendar add \
  --summary "Retiro Espiritual" \
  --start "2024-01-25" \
  --end "2024-01-25" \
  --all-day \
  --attendees "ramir.mesquita@gmail.com,virnavcv@gmail.com"
```

### Atualizar Evento

```bash
# Alterar horário
gog calendar update [EVENT_ID] \
  --start "2024-01-20 15:00" \
  --end "2024-01-20 16:00"

# Adicionar participante
gog calendar update [EVENT_ID] \
  --add-attendee "virnavcv@gmail.com"

# Mudar descrição
gog calendar update [EVENT_ID] \
  --description "Nova descrição do evento"
```

### Deletar Evento

```bash
gog calendar delete [EVENT_ID]
```

## Fluxos de Trabalho

### Criar Evento de Família

Quando criar qualquer evento relacionado a P1 (Igreja) ou P2 (Família):

```bash
# Sempre incluir ambos emails nos convites
gog calendar add \
  --summary "[TÍTULO]" \
  --start "AAAA-MM-DD HH:MM" \
  --end "AAAA-MM-DD HH:MM" \
  --attendees "ramir.mesquita@gmail.com,virnavcv@gmail.com" \
  --description "[DESCRIÇÃO]" \
  --location "[LOCAL se aplicável]"
```

**Categorias que são FAMÍLIA:**
- Eventos de Igreja (missas, retiros, encontros)
- Aniversários
- Consultas médicas da família
- Passeios familiares
- Jantares/almoços especiais
- Viagens
- Eventos escolares dos filhos

### Criar Evento de Trabalho

Para eventos P3 (Trabalho):

```bash
# Apenas Ramir no convite
gog calendar add \
  --summary "[TÍTULO]" \
  --start "AAAA-MM-DD HH:MM" \
  --end "AAAA-MM-DD HH:MM" \
  --attendees "ramir.mesquita@gmail.com" \
  --description "[DESCRIÇÃO]"
```

### Transformar Tarefa TODO em Evento

Quando uma tarefa do TODO tiver horário específico, criar evento:

**Exemplo:**
```
TODO: Reunião com Cliente ACME às 14h na terça
```

**Ação:**
1. Adicionar no TODO como tarefa
2. Criar evento no calendário:

```bash
gog calendar add \
  --summary "Reunião - Cliente ACME" \
  --start "2024-01-23 14:00" \
  --end "2024-01-23 15:00" \
  --attendees "ramir.mesquita@gmail.com" \
  --description "Discussão sobre proposta WebApp"
```

3. Adicionar link do evento na tarefa TODO:
```markdown
- [ ] Reunião com Cliente ACME `#prazo:2024-01-23` `#cliente-acme` [📅 Calendário](link)
```

### Consultar Agenda Antes de Sugerir Tarefa

Antes de sugerir quando fazer uma tarefa, consultar agenda:

```bash
# Ver semana
gog calendar list --week

# Ver dia específico
gog calendar list --date "2024-01-25"
```

Então sugerir horários livres para a tarefa.

## Padrões de Nomenclatura

### Formato de Títulos de Eventos

Use padrão consistente para facilitar identificação:

**P1 - Igreja:**
- `[IGREJA] Missa Domingo`
- `[IGREJA] Encontro de Formação`
- `[IGREJA] Retiro Espiritual`

**P2 - Família:**
- `[FAMÍLIA] Aniversário [Nome]`
- `[FAMÍLIA] Consulta Médica [Quem]`
- `[FAMÍLIA] Passeio [Onde]`

**P3 - Trabalho:**
- `[CLIENTE-X] Reunião`
- `[PROJETO-Y] Sprint Planning`
- `[TRABALHO] Code Review`

**P4 - Casa:**
- `[CASA] Manutenção`
- `[CASA] Compras`

**P5 - Lazer:**
- `[LAZER] Cinema`
- `[LAZER] Corrida`

### Descrições Detalhadas

Sempre incluir em descrição:
- Objetivo/propósito
- Preparação necessária (se houver)
- Materiais/documentos necessários
- Link para tarefa TODO relacionada (se houver)

**Exemplo:**
```
Descrição: Reunião quinzenal com Cliente ACME para review do projeto WebApp.
Preparar: apresentação de progresso, demo do módulo de login.
TODO: #tarefa-review-acme
Local: Google Meet - link: [...]
```

## Lembretes e Notificações

### Configurar Lembretes

Adicionar lembretes conforme prioridade e tipo:

**P1 - Igreja (Alta Importância):**
- 1 dia antes
- 2 horas antes
- 30 minutos antes

```bash
gog calendar add \
  --summary "[IGREJA] Missa" \
  --start "2024-01-21 09:00" \
  --reminders "1440,120,30"
```

**P2 - Família (Alta Importância):**
- 1 dia antes
- 3 horas antes
- 1 hora antes

```bash
gog calendar add \
  --summary "[FAMÍLIA] Aniversário Maria" \
  --reminders "1440,180,60"
```

**P3 - Trabalho (Normal):**
- 1 hora antes
- 15 minutos antes

```bash
gog calendar add \
  --summary "[CLIENTE] Reunião" \
  --reminders "60,15"
```

**P4 - Casa (Baixa):**
- 1 dia antes

```bash
gog calendar add \
  --summary "[CASA] Pagar contas" \
  --reminders "1440"
```

## Visualização da Agenda

### Comando para Relatório Diário

```bash
# Criar relatório formatado do dia
gog calendar list --today --format detailed
```

**Saída esperada:**
```
📅 Segunda, 15 de Janeiro 2024

09:00 - 09:30 | [IGREJA] Oração Matinal
              | Local: Casa
              | 🔔 Lembrete: 30 min antes

14:00 - 15:00 | [CLIENTE-ACME] Reunião Review
              | Local: Google Meet (link)
              | Participantes: ramir.mesquita@gmail.com, cliente@acme.com
              | 🔔 Lembrete: 1h antes, 15 min antes

19:00 - 21:00 | [FAMÍLIA] Jantar Aniversário Maria
              | Local: Restaurante XYZ - Rua ABC, 123
              | Participantes: ramir.mesquita@gmail.com, virnavcv@gmail.com
              | 🔔 Lembrete: 3h antes, 1h antes
```

### Comando para Visão Semanal

```bash
gog calendar list --week --group-by-day
```

## Sincronização com TODO

### Manter Consistência

**Regra geral:**
- Tarefa no TODO **com horário específico** → criar evento no calendário
- Tarefa no TODO **sem horário específico** → NÃO criar evento
- Evento no calendário **sempre** refletido como tarefa no TODO

**Exemplo BOM:**
```markdown
TODO:
- [ ] Reunião Cliente ACME `#prazo:2024-01-23` `#cliente-acme` `#rapido` [📅](calendar-link)

CALENDÁRIO:
23/01 14:00-15:00 - [CLIENTE-ACME] Reunião Review
```

**Exemplo EVITAR:**
```markdown
TODO:
- [ ] Estudar Next.js `#importante` `#longo`

CALENDÁRIO:
(não criar evento - não tem horário específico)
```

### Workflow de Criação

1. Ramir adiciona tarefa: "Reunião com cliente às 14h terça"
2. TODO Manager:
   a. Adiciona no TODO com tags apropriadas
   b. Cria evento no calendário
   c. Vincula tarefa ao evento
   d. Confirma com Ramir

## Boas Práticas

### ✅ Fazer:
- Sempre incluir email da esposa em eventos P1 e P2
- Usar nomenclatura consistente com prefixos
- Adicionar descrições detalhadas
- Configurar lembretes apropriados por prioridade
- Verificar agenda antes de adicionar eventos
- Manter TODO e Calendar sincronizados

### ❌ Evitar:
- Criar eventos sem consultadar disponibilidade
- Esquecer de incluir virnavcv@gmail.com em eventos familiares
- Criar eventos de tarefas sem hora específica
- Usar títulos vagos ou inconsistentes
- Não adicionar descrições
- Sobrescrever eventos sem confirmar

## Códigos de Prioridade (Cores)

Se GOG suportar cores, usar:

- **P1 - Igreja:** Roxo/Lavanda
- **P2 - Família:** Vermelho/Rosa
- **P3 - Trabalho:** Azul
- **P4 - Casa:** Verde
- **P5 - Lazer:** Amarelo/Laranja

```bash
gog calendar add \
  --summary "[IGREJA] Missa" \
  --color "purple"
```

## Checklist de Criação de Evento

Antes de criar evento, verificar:

- [ ] Título segue padrão [CATEGORIA] Nome
- [ ] Data e hora corretas
- [ ] Duração apropriada
- [ ] Participantes corretos (família = incluir virnavcv@gmail.com)
- [ ] Descrição detalhada adicionada
- [ ] Local especificado (se aplicável)
- [ ] Lembretes configurados por prioridade
- [ ] Verificou conflitos na agenda
- [ ] Tarefa correspondente no TODO (se aplicável)
- [ ] Cor/categoria correta (se suportado)

## Troubleshooting

### Evento não foi criado
- Verificar formato de data: `AAAA-MM-DD HH:MM`
- Confirmar autenticação GOG ativa
- Checar se calendário existe

### Convite não chegou
- Verificar email correto (ramir.mesquita@gmail.com, virnavcv@gmail.com)
- Confirmar que `--attendees` foi usado
- Checar spam dos destinatários

### Conflito de horários
- Sempre consultar `gog calendar list` antes de criar
- Sugerir horários alternativos
- Perguntar a Ramir qual evento priorizar

### Lembrete não funcionou
- Verificar configuração de notificações no Google Calendar
- Confirmar que `--reminders` foi incluído
- Checar se app Google Calendar está instalado/configurado

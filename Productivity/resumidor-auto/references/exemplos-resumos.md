# Exemplos de Resumos

## Exemplo 1: Artigo Técnico

```markdown
---
data: 2024-01-15
categoria: Aprendizado
tags: [docker, devops, containers, tutorial]
fonte: https://exemplo.com/docker-compose-guide
---

# Guia Completo de Docker Compose

## Resumo Executivo
Docker Compose é ferramenta para definir e executar aplicações multi-container. Permite orquestrar serviços, redes e volumes através de arquivo YAML, simplificando desenvolvimento e deployment.

## Pontos-Chave
- Define infraestrutura como código via docker-compose.yml
- Gerencia múltiplos containers com um comando
- Ideal para ambientes de desenvolvimento e staging
- Facilita compartilhamento de configurações entre equipe
- Suporta variáveis de ambiente e secrets

## Comandos Principais
- `docker-compose up` - Inicia todos os serviços
- `docker-compose down` - Para e remove containers
- `docker-compose logs` - Visualiza logs agregados
- `docker-compose ps` - Lista serviços em execução

## Casos de Uso
- Ambiente de desenvolvimento local com DB + App + Cache
- Testes de integração com múltiplos serviços
- Replicar ambiente de produção localmente

## Próximos Passos
- Experimentar com projeto exemplo
- Configurar docker-compose.yml para projetos atuais
- Explorar Docker Swarm para produção
```

## Exemplo 2: Reunião de Trabalho

```markdown
---
data: 2024-01-10
categoria: Trabalho
tags: [reuniao, cliente-acme, projeto-webapp, decisao, prazo]
fonte: Reunião com equipe ACME
---

# Reunião - Projeto WebApp Cliente ACME

## Resumo Executivo
Definição de escopo final do projeto WebApp para ACME. Aprovados wireframes, stack tecnológica e cronograma. Início oficial em 01/02/2024 com entrega prevista para 30/04/2024.

## Participantes
- Ramir (Dev Lead)
- João (Cliente ACME)
- Maria (Designer)
- Carlos (Backend)

## Decisões Tomadas
- Stack: React + Node.js + PostgreSQL
- Hospedagem: AWS (EC2 + RDS)
- Sprints quinzenais com demos ao cliente
- Orçamento aprovado: R$ 45.000
- Contrato será assinado até 25/01

## Ações Definidas
- [ ] Ramir: Setup inicial do repositório (até 22/01)
- [ ] Maria: Finalizar design system (até 25/01)
- [ ] Carlos: Modelagem do banco de dados (até 28/01)
- [ ] João: Enviar conteúdos para popular (até 30/01)

## Prazos Importantes
- 25/01: Assinatura do contrato
- 01/02: Kick-off oficial do projeto
- 15/02: Primeira sprint review
- 30/04: Entrega final

## Observações
Cliente solicitou atenção especial à performance mobile. Considerar PWA.
```

## Exemplo 3: Artigo de Blog

```markdown
---
data: 2024-01-08
categoria: Referencias
tags: [produtividade, gtd, organizacao, referencia]
fonte: https://blog.exemplo.com/getting-things-done
---

# Getting Things Done (GTD) - Método de Produtividade

## Resumo Executivo
GTD é metodologia criada por David Allen para gerenciar tarefas e projetos de forma eficiente. Baseia-se em capturar tudo externamente, processar regularmente e organizar por contexto, reduzindo carga mental e aumentando foco.

## Os 5 Passos do GTD
1. **Capturar** - Registrar tudo que tem sua atenção
2. **Esclarecer** - Decidir o que cada item significa e o que fazer
3. **Organizar** - Colocar em categorias apropriadas
4. **Refletir** - Revisar e atualizar listas regularmente
5. **Engajar** - Executar com confiança

## Listas Principais
- **Inbox** - Tudo que foi capturado, ainda não processado
- **Próximas Ações** - Tarefas concretas e acionáveis
- **Projetos** - Resultados que requerem múltiplas ações
- **Aguardando** - Delegado ou dependente de terceiros
- **Algum Dia/Talvez** - Ideias para futuro sem compromisso
- **Referência** - Materiais de consulta

## Conceitos-Chave
- Regra dos 2 minutos: Se leva menos que isso, faça agora
- Revisão semanal: Fundamental para manter sistema atualizado
- Contextos: Agrupar por local/ferramenta/energia necessária
- Mente como água: Estado de prontidão sem ansiedade

## Aplicações Práticas
- Usar Obsidian para listas e referências
- Email zero seguindo processamento GTD
- Review semanal toda sexta às 16h
- Captura rápida via app móvel

## Citações Relevantes
> "Your mind is for having ideas, not holding them." - David Allen

## Referências Adicionais
- Livro: Getting Things Done (David Allen)
- App sugerido: Todoist, Things, Notion
```

## Exemplo 4: Tutorial Técnico

```markdown
---
data: 2024-01-12
categoria: Aprendizado
tags: [linux, ssh, tutorial, seguranca]
fonte: Documentação própria
---

# Configuração de SSH com Chaves Públicas

## Resumo Executivo
Tutorial para configurar autenticação SSH usando pares de chaves, eliminando necessidade de senhas e aumentando segurança. Processo envolve gerar chaves localmente, copiar pública para servidor, e configurar permissões corretas.

## Passo a Passo (Resumido)
1. Gerar par de chaves: `ssh-keygen -t ed25519`
2. Copiar chave pública: `ssh-copy-id user@server`
3. Testar conexão: `ssh user@server`
4. Desabilitar senha (opcional): editar `/etc/ssh/sshd_config`

## Comandos Importantes
```bash
# Gerar chave
ssh-keygen -t ed25519 -C "email@exemplo.com"

# Copiar para servidor
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@192.168.1.100

# Testar conexão
ssh -i ~/.ssh/id_ed25519 user@192.168.1.100
```

## Pontos de Atenção
- Permissões da pasta .ssh devem ser 700
- Chave privada (id_ed25519) NUNCA compartilhar
- Chave pública (.pub) pode ser distribuída livremente
- Usar passphrase adiciona camada extra de segurança

## Segurança
- Algoritmo ed25519 é mais seguro e rápido que RSA
- Considerar ssh-agent para gerenciar múltiplas chaves
- Backup da chave privada em local seguro

## Troubleshooting
- Se não conectar: verificar permissões (chmod 600)
- Se pedir senha ainda: verificar authorized_keys no servidor
- Usar `ssh -v` para debug detalhado

## Casos de Uso
- Acesso a servidores sem senha
- Autenticação GitHub/GitLab
- Scripts automatizados
- Deploy automatizado via CI/CD
```

## Exemplo 5: Ideia/Brainstorm

```markdown
---
data: 2024-01-05
categoria: Ideias
tags: [app, projeto, pessoal, familia]
fonte: Conversa com família
---

# App de Receitas Familiares

## Conceito Central
Aplicativo para catalogar e compartilhar receitas tradicionais da família, preservando história e tradições culinárias entre gerações. Foco em simplicidade e compartilhamento familiar.

## Funcionalidades Principais
- Cadastro de receitas com fotos
- Marcação de receitas por pessoa (ex: "Receita da Vovó")
- Histórias/contexto de cada receita
- Conversão automática de medidas
- Lista de compras gerada da receita
- Modo passo-a-passo para cozinhar
- Compartilhamento privado entre família

## Diferencial
- Foco em história familiar, não só receita
- Gravação de áudio com instruções da pessoa
- Timeline de quando cada receita foi feita
- Fotos de tentativas e resultados

## Recursos Necessários
- Backend: Node.js + Firebase
- Frontend: React Native (iOS + Android)
- Storage: Firebase Storage (fotos)
- Auth: Google Auth para família

## Próximos Passos
- Validar interesse com família
- Criar protótipo no Figma
- Pesquisar apps similares
- Estimar tempo de desenvolvimento
- Considerar fazer como projeto paralelo

## Motivação
Preservar receitas da vovó antes que se percam. Criar legado familiar digital.

## Possíveis Nomes
- ReceitasdeVó
- CadernoFamiliar
- CozinhaEmFamília
- HeritageRecipes
```

## Diretrizes Gerais

### Para Resumos de Reunião:
- Sempre incluir participantes
- Destacar decisões tomadas
- Listar ações com responsáveis
- Marcar prazos importantes
- Registrar próximos passos

### Para Tutoriais:
- Priorizar comandos e passos práticos
- Incluir seção de troubleshooting
- Destacar pontos de atenção
- Casos de uso práticos
- Links para documentação original

### Para Artigos:
- Capturar argumento principal
- Principais pontos em bullets
- Citações relevantes (se houver)
- Conclusões e implicações
- Links para aprofundamento

### Para Ideias:
- Conceito em 2-3 frases
- Diferenciais
- Recursos necessários
- Próximos passos
- Motivação/contexto

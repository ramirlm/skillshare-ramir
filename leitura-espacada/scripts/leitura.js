#!/usr/bin/env node
/**
 * Leitura Espaçada - Sistema de Repetição Espaçada
 * Versão modular e reutilizável
 * 
 * Uso: leitura [comando] [args]
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Configuração
const CONFIG = {
  INTERVALS: [1, 3, 7, 14, 30, 60, 120],
  VAULT_PATH: process.env.LEITURA_VAULT_PATH || path.join(process.env.HOME, 'vault', 'leitura'),
  COLLECTION: process.env.LEITURA_COLLECTION || 'default'
};

// Comandos disponíveis
const COMMANDS = {
  'init': initSystem,
  'add': addCard,
  'review': reviewCard,
  'due': listDue,
  'stats': showStats,
  'next': getNextReview,
  'study': interactiveStudy,
  'backup': createBackup,
  'reset': resetCard,
  'help': showHelp
};

// Utilitários
function getToday() {
  return new Date().toISOString().split('T')[0];
}

function addDays(dateStr, days) {
  const date = new Date(dateStr);
  date.setDate(date.getDate() + days);
  return date.toISOString().split('T')[0];
}

function generateId(prefix) {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substr(2, 4);
  return `${prefix}_${timestamp}_${random}`;
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function getVaultPath() {
  const collection = process.env.LEITURA_COLLECTION || 'default';
  return path.join(CONFIG.VAULT_PATH, collection);
}

// Inicializar sistema
function initSystem(args) {
  const collection = args[0] || 'default';
  const basePath = path.join(CONFIG.VAULT_PATH, collection);
  
  const dirs = [
    basePath,
    path.join(basePath, 'cards'),
    path.join(basePath, 'revisao'),
    path.join(basePath, 'temas'),
    path.join(basePath, 'conteudo'),
    path.join(basePath, 'templates'),
    path.join(basePath, 'backups')
  ];
  
  dirs.forEach(ensureDir);
  
  // Criar config
  const config = {
    collection,
    created: getToday(),
    intervals: CONFIG.INTERVALS,
    totalCards: 0,
    totalReviews: 0
  };
  
  fs.writeFileSync(
    path.join(basePath, '.leitura-config.json'),
    JSON.stringify(config, null, 2)
  );
  
  // Criar templates
  const cardTemplate = `---
id: {{id}}
content_id: {{content_id}}
title: {{title}}
themes: {{themes}}
created: {{created}}
interval: {{interval}}
level: {{level}}
next_review: {{next_review}}
streak: {{streak}}
---

# {{title}}

## Pergunta
{{front}}

---

## Resposta
{{back}}

---

**Criado:** {{created}}  
**Próxima revisão:** {{next_review}}  
**Nível:** {{level}} | **Sequência:** {{streak}}
`;

  fs.writeFileSync(path.join(basePath, 'templates', 'card-template.md'), cardTemplate);
  
  console.log(`✅ Sistema inicializado: ${collection}`);
  console.log(`📂 Local: ${basePath}`);
}

// Criar novo card
function addCard(args) {
  const vaultPath = getVaultPath();
  ensureDir(path.join(vaultPath, 'cards'));
  
  let cardData;
  
  if (args.length >= 3) {
    // Modo direto
    const [title, front, back, themesArg = ''] = args;
    const themes = themesArg.split(',').map(t => t.trim()).filter(Boolean);
    const today = getToday();
    const cardId = generateId('card');
    
    cardData = {
      id: cardId,
      title,
      front,
      back,
      themes,
      created: today,
      source: process.env.LEITURA_SOURCE || 'manual',
      interval: 1,
      level: 0,
      next_review: addDays(today, 1),
      streak: 0,
      review_count: 0
    };
  } else {
    console.error('Uso: leitura add <título> <pergunta> <resposta> [temas]');
    process.exit(1);
  }
  
  // Salvar card
  const cardPath = path.join(vaultPath, 'cards', `${cardData.id}.json`);
  fs.writeFileSync(cardPath, JSON.stringify(cardData, null, 2));
  
  // Criar markdown
  const templatePath = path.join(vaultPath, 'templates', 'card-template.md');
  if (fs.existsSync(templatePath)) {
    let template = fs.readFileSync(templatePath, 'utf8');
    template = template
      .replace(/\{\{id\}\}/g, cardData.id)
      .replace(/\{\{title\}\}/g, cardData.title)
      .replace(/\{\{front\}\}/g, cardData.front)
      .replace(/\{\{back\}\}/g, cardData.back)
      .replace(/\{\{themes\}\}/g, cardData.themes.join(', '))
      .replace(/\{\{created\}\}/g, cardData.created)
      .replace(/\{\{interval\}\}/g, cardData.interval)
      .replace(/\{\{level\}\}/g, cardData.level)
      .replace(/\{\{next_review\}\}/g, cardData.next_review)
      .replace(/\{\{streak\}\}/g, cardData.streak);
    
    fs.writeFileSync(path.join(vaultPath, 'cards', `${cardData.id}.md`), template);
  }
  
  // Atualizar config
  updateConfig(vaultPath, { totalCards: 1 });
  
  console.log(`✅ Card criado: ${cardData.id}`);
  console.log(`📝 Título: ${cardData.title}`);
  console.log(`📅 Próxima revisão: ${cardData.next_review}`);
  if (cardData.themes.length > 0) {
    console.log(`🏷️  Temas: ${cardData.themes.join(', ')}`);
  }
}

// Revisar card
function reviewCard(args) {
  if (args.length < 2) {
    console.error('Uso: leitura review <card_id> <performance>');
    console.error('Performance: again | hard | good | easy');
    process.exit(1);
  }
  
  const [cardId, performance] = args;
  const vaultPath = getVaultPath();
  const cardPath = path.join(vaultPath, 'cards', `${cardId}.json`);
  
  if (!fs.existsSync(cardPath)) {
    console.error(`❌ Card não encontrado: ${cardId}`);
    process.exit(1);
  }
  
  const card = JSON.parse(fs.readFileSync(cardPath, 'utf8'));
  const today = getToday();
  
  // Calcular novo nível
  let newLevel = card.level;
  let newStreak = card.streak;
  
  switch (performance) {
    case 'again':
      newLevel = 0;
      newStreak = 0;
      break;
    case 'hard':
      newLevel = Math.max(0, card.level - 1);
      newStreak = 0;
      break;
    case 'good':
      newLevel = Math.min(CONFIG.INTERVALS.length - 1, card.level + 1);
      newStreak = card.streak + 1;
      break;
    case 'easy':
      newLevel = Math.min(CONFIG.INTERVALS.length - 1, card.level + 2);
      newStreak = card.streak + 1;
      break;
    default:
      console.error(`❌ Performance inválida: ${performance}`);
      process.exit(1);
  }
  
  const newInterval = CONFIG.INTERVALS[newLevel];
  const nextReview = addDays(today, newInterval);
  
  // Atualizar card
  card.level = newLevel;
  card.interval = newInterval;
  card.next_review = nextReview;
  card.streak = newStreak;
  card.review_count = (card.review_count || 0) + 1;
  card.last_reviewed = today;
  card.last_performance = performance;
  
  fs.writeFileSync(cardPath, JSON.stringify(card, null, 2));
  
  // Registrar revisão
  const reviewId = generateId('review');
  const reviewData = {
    id: reviewId,
    card_id: cardId,
    date: today,
    performance,
    level: newLevel,
    interval: newInterval
  };
  
  ensureDir(path.join(vaultPath, 'revisao'));
  fs.writeFileSync(
    path.join(vaultPath, 'revisao', `${reviewId}.json`),
    JSON.stringify(reviewData, null, 2)
  );
  
  updateConfig(vaultPath, { totalReviews: 1 });
  
  const emojis = { again: '❌', hard: '⚠️ ', good: '✅', easy: '🌟' };
  console.log(`${emojis[performance]} Revisão registrada!`);
  console.log(`📈 Nível: ${card.level} → ${newLevel}`);
  console.log(`📅 Próxima: ${nextReview} (${newInterval} dias)`);
  console.log(`🔥 Sequência: ${newStreak}`);
}

// Listar cards pendentes
function listDue() {
  const today = getToday();
  const vaultPath = getVaultPath();
  const cardsPath = path.join(vaultPath, 'cards');
  
  if (!fs.existsSync(cardsPath)) {
    console.log('📭 Nenhum card encontrado.');
    return;
  }
  
  const files = fs.readdirSync(cardsPath).filter(f => f.endsWith('.json'));
  const dueCards = [];
  
  for (const file of files) {
    try {
      const card = JSON.parse(fs.readFileSync(path.join(cardsPath, file), 'utf8'));
      if (card.next_review <= today) {
        dueCards.push(card);
      }
    } catch (e) {
      // Ignorar arquivos inválidos
    }
  }
  
  dueCards.sort((a, b) => a.next_review.localeCompare(b.next_review));
  
  if (dueCards.length === 0) {
    console.log('🎉 Nenhuma revisão pendente!');
    return;
  }
  
  console.log(`\n📚 Para revisar hoje (${today}): ${dueCards.length} card(s)\n`);
  
  dueCards.forEach((card, i) => {
    const status = card.next_review < today ? '⚠️  ATRASADO' : '📅 HOJE';
    console.log(`${i + 1}. ${status} | ${card.title}`);
    console.log(`   ID: ${card.id}`);
    console.log(`   Pergunta: ${card.front.substring(0, 60)}${card.front.length > 60 ? '...' : ''}`);
    console.log(`   Nível: ${card.level} | Sequência: ${card.streak}`);
    console.log();
  });
  
  console.log('💡 Use: leitura study (modo interativo)');
  console.log('   Ou: leitura review <id> <performance>');
}

// Modo estudo interativo
async function interactiveStudy() {
  const vaultPath = getVaultPath();
  const cardsPath = path.join(vaultPath, 'cards');
  
  if (!fs.existsSync(cardsPath)) {
    console.log('📭 Nenhum card encontrado.');
    return;
  }
  
  const today = getToday();
  const files = fs.readdirSync(cardsPath).filter(f => f.endsWith('.json'));
  const dueCards = [];
  
  for (const file of files) {
    try {
      const card = JSON.parse(fs.readFileSync(path.join(cardsPath, file), 'utf8'));
      if (card.next_review <= today) {
        dueCards.push(card);
      }
    } catch (e) {}
  }
  
  if (dueCards.length === 0) {
    console.log('🎉 Nenhuma revisão pendente!');
    return;
  }
  
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  const question = (prompt) => new Promise(resolve => rl.question(prompt, resolve));
  
  console.log(`\n📚 Modo Estudo — ${dueCards.length} card(s)\n`);
  
  for (const card of dueCards) {
    console.log('━'.repeat(50));
    console.log(`📝 ${card.title}`);
    console.log('━'.repeat(50));
    console.log(`\n❓ ${card.front}\n`);
    
    await question('⏎  Pressione ENTER para ver a resposta...');
    
    console.log(`\n✅ ${card.back}\n`);
    
    console.log('Como foi?');
    console.log('  1) again — Esqueci completamente');
    console.log('  2) hard  — Foi difícil lembrar');
    console.log('  3) good  — Lembrei bem');
    console.log('  4) easy  — Lembrei facilmente');
    console.log('  5) pular — Próximo card');
    console.log('  6) sair  — Encerrar\n');
    
    const choice = await question('Escolha (1-6): ');
    
    const performanceMap = {
      '1': 'again',
      '2': 'hard',
      '3': 'good',
      '4': 'easy'
    };
    
    if (choice === '5') continue;
    if (choice === '6') break;
    
    if (performanceMap[choice]) {
      reviewCard([card.id, performanceMap[choice]]);
      console.log();
    }
  }
  
  rl.close();
  console.log('\n✨ Sessão de estudo finalizada!');
}

// Estatísticas
function showStats() {
  const vaultPath = getVaultPath();
  const cardsPath = path.join(vaultPath, 'cards');
  const configPath = path.join(vaultPath, '.leitura-config.json');
  
  if (!fs.existsSync(cardsPath)) {
    console.log('📭 Nenhum dado encontrado.');
    return;
  }
  
  const files = fs.readdirSync(cardsPath).filter(f => f.endsWith('.json'));
  const today = getToday();
  
  let total = 0;
  let due = 0;
  let mature = 0;
  const byLevel = {};
  const byTheme = {};
  
  for (const file of files) {
    try {
      const card = JSON.parse(fs.readFileSync(path.join(cardsPath, file), 'utf8'));
      total++;
      
      if (card.next_review <= today) due++;
      if (card.level >= 4) mature++;
      
      byLevel[card.level] = (byLevel[card.level] || 0) + 1;
      
      (card.themes || []).forEach(theme => {
        byTheme[theme] = (byTheme[theme] || 0) + 1;
      });
    } catch (e) {}
  }
  
  console.log('\n📊 Estatísticas\n');
  console.log(`Total de cards: ${total}`);
  console.log(`Cards maduros (nivel 4+): ${mature}`);
  console.log(`Revisões pendentes: ${due}`);
  
  console.log('\n📈 Por nível:');
  CONFIG.INTERVALS.forEach((interval, level) => {
    const count = byLevel[level] || 0;
    const bar = '█'.repeat(Math.min(count, 20));
    console.log(`  Nível ${level} (${interval}d): ${bar} ${count}`);
  });
  
  if (Object.keys(byTheme).length > 0) {
    console.log('\n🏷️  Por tema:');
    Object.entries(byTheme)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .forEach(([theme, count]) => {
        console.log(`  ${theme}: ${count}`);
      });
  }
  
  if (fs.existsSync(configPath)) {
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    console.log(`\n📅 Coleção criada: ${config.created}`);
  }
}

// Próximas revisões
function getNextReview() {
  const vaultPath = getVaultPath();
  const cardsPath = path.join(vaultPath, 'cards');
  
  if (!fs.existsSync(cardsPath)) {
    console.log('📭 Nenhum card encontrado.');
    return;
  }
  
  const files = fs.readdirSync(cardsPath).filter(f => f.endsWith('.json'));
  const future = {};
  
  for (const file of files) {
    try {
      const card = JSON.parse(fs.readFileSync(path.join(cardsPath, file), 'utf8'));
      const date = card.next_review;
      future[date] = (future[date] || 0) + 1;
    } catch (e) {}
  }
  
  const sortedDates = Object.keys(future).sort();
  
  console.log('\n📅 Próximas revisões\n');
  sortedDates.slice(0, 7).forEach(date => {
    console.log(`  ${date}: ${future[date]} card(s)`);
  });
}

// Criar backup
function createBackup() {
  const vaultPath = getVaultPath();
  const backupDir = path.join(vaultPath, 'backups');
  ensureDir(backupDir);
  
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const backupFile = path.join(backupDir, `backup-${timestamp}.tar.gz`);
  
  const { execSync } = require('child_process');
  
  try {
    execSync(`tar -czf "${backupFile}" -C "${vaultPath}" cards/ revisao/ conteudo/`, {
      stdio: 'ignore'
    });
    console.log(`✅ Backup criado: ${backupFile}`);
    
    // Limpar backups antigos (manter últimos 10)
    const backups = fs.readdirSync(backupDir)
      .filter(f => f.startsWith('backup-'))
      .map(f => ({ name: f, path: path.join(backupDir, f) }))
      .sort((a, b) => fs.statSync(b.path).mtime - fs.statSync(a.path).mtime);
    
    backups.slice(10).forEach(b => fs.unlinkSync(b.path));
  } catch (e) {
    console.error('❌ Erro ao criar backup:', e.message);
  }
}

// Resetar card
function resetCard(args) {
  if (args.length < 1) {
    console.error('Uso: leitura reset <card_id>');
    process.exit(1);
  }
  
  const cardId = args[0];
  const vaultPath = getVaultPath();
  const cardPath = path.join(vaultPath, 'cards', `${cardId}.json`);
  
  if (!fs.existsSync(cardPath)) {
    console.error(`❌ Card não encontrado: ${cardId}`);
    process.exit(1);
  }
  
  const card = JSON.parse(fs.readFileSync(cardPath, 'utf8'));
  const today = getToday();
  
  card.level = 0;
  card.interval = 1;
  card.next_review = addDays(today, 1);
  card.streak = 0;
  
  fs.writeFileSync(cardPath, JSON.stringify(card, null, 2));
  
  console.log(`🔄 Card resetado: ${cardId}`);
  console.log(`📅 Próxima revisão: ${card.next_review}`);
}

// Atualizar config
function updateConfig(vaultPath, updates) {
  const configPath = path.join(vaultPath, '.leitura-config.json');
  
  let config = {};
  if (fs.existsSync(configPath)) {
    config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  }
  
  Object.entries(updates).forEach(([key, value]) => {
    config[key] = (config[key] || 0) + value;
  });
  
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
}

// Ajuda
function showHelp() {
  console.log('📚 Leitura Espaçada\n');
  console.log('Comandos:');
  console.log('  init [coleção]        Inicializar coleção');
  console.log('  add <título> <frente> <verso> [temas]');
  console.log('                         Adicionar novo card');
  console.log('  review <id> <perf>    Revisar card (again|hard|good|easy)');
  console.log('  due                   Listar cards pendentes');
  console.log('  study                 Modo estudo interativo');
  console.log('  stats                 Estatísticas');
  console.log('  next                  Próximas revisões');
  console.log('  backup                Criar backup');
  console.log('  reset <id>            Resetar card');
  console.log('  help                  Mostrar ajuda');
  console.log('\nVariáveis:');
  console.log('  LEITURA_VAULT_PATH    Caminho do vault');
  console.log('  LEITURA_COLLECTION    Coleção atual');
}

// Main
const [command, ...args] = process.argv.slice(2);

if (!command || !COMMANDS[command]) {
  showHelp();
  process.exit(1);
}

if (command === 'study') {
  interactiveStudy().catch(console.error);
} else {
  COMMANDS[command](args);
}

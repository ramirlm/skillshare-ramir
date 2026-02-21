#!/usr/bin/env node
/**
 * Sincroniza cards com Ontology
 * Cria entidades e relações no graph
 */

const fs = require('fs');
const path = require('path');

const ONTOLOGY_PATH = process.env.ONTOLOGY_PATH || path.join(process.env.HOME, 'memory/ontology');
const VAULT_PATH = process.env.LEITURA_VAULT_PATH || path.join(process.env.HOME, 'Obsidian/leitura');

function syncWithOntology() {
  const graphPath = path.join(ONTOLOGY_PATH, 'graph.jsonl');
  
  if (!fs.existsSync(VAULT_PATH)) {
    console.log('📭 Nenhum vault encontrado.');
    return;
  }
  
  const collections = fs.readdirSync(VAULT_PATH).filter(f => {
    return fs.statSync(path.join(VAULT_PATH, f)).isDirectory();
  });
  
  let operations = [];
  
  collections.forEach(collection => {
    const cardsPath = path.join(VAULT_PATH, collection, 'cards');
    if (!fs.existsSync(cardsPath)) return;
    
    const cards = fs.readdirSync(cardsPath)
      .filter(f => f.endsWith('.json'))
      .map(f => JSON.parse(fs.readFileSync(path.join(cardsPath, f), 'utf8')));
    
    cards.forEach(card => {
      // Criar entidade StudyCard
      operations.push({
        op: 'create',
        entity: {
          id: card.id,
          type: 'StudyCard',
          properties: {
            title: card.title,
            collection: collection,
            front: card.front,
            back: card.back,
            themes: card.themes,
            level: card.level,
            streak: card.streak,
            next_review: card.next_review
          }
        }
      });
      
      // Criar temas se não existirem
      (card.themes || []).forEach(theme => {
        const themeId = `theme_${theme.replace(/\s+/g, '_').toLowerCase()}`;
        
        // Adicionar relação
        operations.push({
          op: 'relate',
          from: card.id,
          rel: 'card_has_theme',
          to: themeId
        });
      });
    });
  });
  
  // Salvar no graph (append)
  if (operations.length > 0) {
    const lines = operations.map(op => JSON.stringify(op)).join('\n');
    fs.appendFileSync(graphPath, '\n' + lines + '\n');
    console.log(`✅ Sincronizado: ${operations.length} operações`);
  }
}

const command = process.argv[2];

switch (command) {
  case 'sync':
    syncWithOntology();
    break;
  default:
    console.log('Uso: ontology-sync.js sync');
}

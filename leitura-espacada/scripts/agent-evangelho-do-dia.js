#!/usr/bin/env node
/**
 * Script para o agente buscar e processar Evangelho do Dia
 * Chamado pelo cron às 6h
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const DATA = new Date().toISOString().split('T')[0];
const DATA_FORMATADA = new Date().toLocaleDateString('pt-BR');

async function buscarEvangelho() {
  console.log(`🔍 Buscando Evangelho do Dia para ${DATA_FORMATADA}...`);
  
  // O agente precisa usar ferramentas externas para buscar o evangelho
  // Este script serve como template/instrução
  
  return {
    data: DATA,
    dataFormatada: DATA_FORMATADA,
    instrucoes: `
O agente deve:
1. Usar browser para acessar https://www.vaticannews.va/pt/evangelho-do-dia.html
2. Extrair: referência, texto, salmo
3. Criar síntese
4. Adicionar ao sistema
5. Enviar ao Telegram
    `
  };
}

function salvarEvangelho(evangelho) {
  const vaultPath = path.join(process.env.HOME, 'vault', 'leitura', 'biblia', 'evangelho-do-dia');
  
  if (!fs.existsSync(vaultPath)) {
    fs.mkdirSync(vaultPath, { recursive: true });
  }
  
  const filename = path.join(vaultPath, `${DATA}.md`);
  
  const content = `---
data: ${DATA}
referencia: ${evangelho.referencia}
tempos: ${evangelho.tempo || ''}
temas: [${evangelho.temas?.join(', ') || ''}]
---

# Evangelho do Dia — ${DATA_FORMATADA}

## ${evangelho.referencia}

> ${evangelho.texto}

## Salmo
${evangelho.salmo || 'N/A'}

## Síntese
${evangelho.sintese?.map((p, i) => `${i + 1}. ${p}`).join('\n') || ''}

## Reflexão
${evangelho.reflexao || ''}

---

*Liturgia do Dia* | *Adicionado automaticamente às 6h*
`;

  fs.writeFileSync(filename, content);
  console.log(`✅ Evangelho salvo em: ${filename}`);
  
  return filename;
}

function adicionarCard(evangelho) {
  const scriptPath = path.join(__dirname, 'leitura.js');
  
  const pergunta = `Qual o Evangelho de ${DATA_FORMATADA}?`;
  const resposta = `${evangelho.referencia}: ${evangelho.texto.substring(0, 200)}...`;
  const temas = evangelho.temas?.join(',') || 'evangelho-do-dia';
  
  try {
    execSync(`LEITURA_COLLECTION=biblia node "${scriptPath}" add "${evangelho.referencia}" "${pergunta}" "${resposta}" "${temas}"`, {
      stdio: 'inherit'
    });
    console.log('✅ Card adicionado ao sistema');
  } catch (e) {
    console.error('❌ Erro ao adicionar card:', e.message);
  }
}

// Main
console.log('📖 Evangelho do Dia — Agente de Processamento');
console.log(`Data: ${DATA_FORMATADA}`);
console.log('');

// O agente deve implementar a lógica de busca
// usando as ferramentas disponíveis (browser, etc.)

module.exports = { buscarEvangelho, salvarEvangelho, adicionarCard };

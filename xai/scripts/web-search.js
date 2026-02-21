#!/usr/bin/env node
/**
 * xAI Web Search Script - Uses Responses API with web_search tool
 *
 * Usage:
 *   node web-search.js "xai api docs"
 *   node web-search.js --domains x.ai,openai.com "vision models"
 *   node web-search.js --exclude-domains reddit.com "search rankings"
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const API_BASE = 'api.x.ai';
const DEFAULT_MODEL = 'grok-4-1-fast';
const DEFAULT_MAX_RESULTS = 5;

function getApiKey() {
  if (process.env.XAI_API_KEY) {
    return process.env.XAI_API_KEY;
  }

  const configPath = path.join(process.env.HOME, '.clawdbot', 'clawdbot.json');
  if (fs.existsSync(configPath)) {
    try {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      const key = config?.skills?.entries?.xai?.apiKey;
      if (key) return key;
    } catch (e) {}
  }

  return null;
}

function parseArgs(args) {
  const result = {
    model: DEFAULT_MODEL,
    query: '',
    domains: [],
    excludeDomains: [],
    imageUnderstanding: false,
    maxResults: DEFAULT_MAX_RESULTS,
    json: false,
  };

  let i = 0;
  while (i < args.length) {
    const arg = args[i];

    if (arg === '--model' || arg === '-m') {
      result.model = args[++i];
    } else if (arg === '--domains') {
      result.domains = args[++i].split(',').map(d => d.trim()).filter(Boolean);
    } else if (arg === '--exclude-domains') {
      result.excludeDomains = args[++i].split(',').map(d => d.trim()).filter(Boolean);
    } else if (arg === '--image-understanding') {
      result.imageUnderstanding = true;
    } else if (arg === '--max-results') {
      result.maxResults = parseInt(args[++i], 10);
    } else if (arg === '--json' || arg === '-j') {
      result.json = true;
    } else if (!arg.startsWith('-')) {
      result.query = args.slice(i).join(' ');
      break;
    }
    i++;
  }

  return result;
}

async function webSearch(options) {
  const apiKey = getApiKey();
  if (!apiKey) {
    console.error('❌ No API key found. Set XAI_API_KEY or configure in clawdbot.');
    process.exit(1);
  }

  const webSearchTool = {
    type: 'web_search',
    web_search: {}
  };

  if (options.domains.length > 0) {
    webSearchTool.web_search.domains = options.domains;
  }
  if (options.excludeDomains.length > 0) {
    webSearchTool.web_search.exclude_domains = options.excludeDomains;
  }
  if (options.imageUnderstanding) {
    webSearchTool.web_search.enable_image_understanding = true;
  }
  if (Number.isFinite(options.maxResults)) {
    webSearchTool.web_search.max_results = options.maxResults;
  }

  const payload = {
    model: options.model,
    input: `Search the web for: ${options.query}

Return:
- Source title
- Short summary
- URL

If there are multiple sources, list them clearly.`,
    tools: [webSearchTool],
  };

  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: API_BASE,
      path: '/v1/responses',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
      },
    }, (res) => {
      let data = '';

      res.on('data', chunk => data += chunk);

      res.on('end', () => {
        if (res.statusCode !== 200) {
          console.error(`❌ API Error (${res.statusCode}):`, data);
          process.exit(1);
        }

        try {
          const response = JSON.parse(data);

          if (options.json) {
            console.log(JSON.stringify(response, null, 2));
            resolve(response);
            return;
          }

          let content = '(no response)';
          if (response.output) {
            for (const item of response.output) {
              if (item.type === 'message' && item.content) {
                for (const c of item.content) {
                  if (c.type === 'output_text' && c.text) {
                    content = c.text;
                  }
                }
              }
            }
          }

          let citations = [];
          if (response.output) {
            for (const item of response.output) {
              if (item.content) {
                for (const c of item.content) {
                  if (c.annotations) {
                    for (const ann of c.annotations) {
                      if (ann.type === 'url_citation' && ann.url) {
                        citations.push(ann.url);
                      }
                    }
                  }
                }
              }
            }
          }
          citations = [...new Set(citations)];

          console.log(content);

          if (citations.length > 0) {
            console.log('\n📎 Citations:');
            for (const cite of citations) {
              console.log(`   ${cite}`);
            }
          }

          resolve(response);
        } catch (e) {
          console.error('❌ Failed to parse response:', e.message);
          console.error('Raw:', data.slice(0, 500));
          process.exit(1);
        }
      });
    });

    req.on('error', (e) => {
      console.error('❌ Request failed:', e.message);
      process.exit(1);
    });

    req.write(JSON.stringify(payload));
    req.end();
  });
}

// Main
const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help')) {
  console.log(`
🌐 xAI Web Search (Responses API)

Usage:
  node web-search.js [options] "Your search query"

Options:
  --model, -m <model>       Model (default: grok-4-1-fast)
  --domains <list>          Only search these domains (comma-separated)
  --exclude-domains <list>  Exclude these domains (comma-separated)
  --image-understanding     Enable image understanding in results
  --max-results <n>         Limit number of results (default: 5)
  --json, -j                Output full JSON response
  --help                    Show this help

Examples:
  node web-search.js "xAI API documentation"
  node web-search.js --domains x.ai,openai.com "vision models"
  node web-search.js --exclude-domains reddit.com --max-results 3 "pricing comparison"
  node web-search.js --image-understanding "latest product screenshots"
`);
  process.exit(0);
}

const options = parseArgs(args);

if (!options.query) {
  console.error('❌ Please provide a search query');
  process.exit(1);
}

if (!Number.isFinite(options.maxResults) || options.maxResults <= 0) {
  console.error('❌ Invalid --max-results value. Use a positive number.');
  process.exit(1);
}

console.error(`🌐 Searching web for: "${options.query}"...\n`);
webSearch(options);

# Smoke Tests - xai skill

Run these manually after changes. Requires `XAI_API_KEY` configured.

## Search X/Twitter (search-x.js)

- Basic search:
  - `node scripts/search-x.js "Remotion video framework tips"`
- Allowed handles (alias flags):
  - `node scripts/search-x.js --handles @remotion_dev "updates"`
  - `node scripts/search-x.js --allowed-handles @remotion_dev,@jonnyburger "updates"`
- Excluded handles:
  - `node scripts/search-x.js --excluded-handles @spam,@bot "AI video creation"`
- Date ranges:
  - `node scripts/search-x.js --from-date 2025-01-01 "Grok 4 launch"`
  - `node scripts/search-x.js --to-date 2025-01-31 "Grok 4 launch"`
  - `node scripts/search-x.js --from-date 2025-01-01 --to-date 2025-01-31 "Grok 4 launch"`
- Days without from-date:
  - `node scripts/search-x.js --days 7 "Claude AI"`
- Media understanding flags:
  - `node scripts/search-x.js --image-understanding "product screenshots"`
  - `node scripts/search-x.js --video-understanding "demo clips"`
- Combined filters:
  - `node scripts/search-x.js --handles @remotion_dev --from-date 2025-01-01 --image-understanding "new features"`

## Web Search (web-search.js)

- Basic web search:
  - `node scripts/web-search.js "xAI API documentation"`
- Domain filters:
  - `node scripts/web-search.js --domains x.ai,openai.com "vision models"`
  - `node scripts/web-search.js --exclude-domains reddit.com "pricing comparison"`
- Max results:
  - `node scripts/web-search.js --max-results 3 "API response formats"`
- Image understanding:
  - `node scripts/web-search.js --image-understanding "latest product screenshots"`

## Backward Compatibility

- Existing search-x.js usage still works:
  - `node scripts/search-x.js --days 30 "AI video creation best practices"`
  - `node scripts/search-x.js --handles @remotion_dev "new features"`

## Edge Cases / Known Limitations

- Invalid dates should fail fast with a clear error.
- If citations are missing, X/web search may not be enabled or no results were found.

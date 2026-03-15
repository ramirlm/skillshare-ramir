---
name: xai
description: "Chat with Grok models via xAI API, plus X/Twitter and web search. Use when: (1) Querying Grok models for analysis, (2) Accessing Grok-3, Grok-3-mini, or vision capabilities, (3) Running deep reasoning tasks with Grok, (4) Searching X/Twitter or the web with Grok's tools, (5) Complementing Claude with Grok's unique perspective."
homepage: https://docs.x.ai
triggers:
  - grok
  - xai
  - ask grok
  - web search
  - search web
  - search x
metadata:
  clawdbot:
    emoji: "🤖"
---

# xAI / Grok

Chat with xAI's Grok models. Supports text, vision, X/Twitter search, and web search.

## Setup

Set your API key in the skill config:

```bash
# Via clawdbot config
clawdbot config set skills.entries.xai.apiKey "xai-YOUR-KEY"

# Or environment variable
export XAI_API_KEY="xai-YOUR-KEY"
```

Get your API key at: https://console.x.ai

## Commands

### Chat with Grok
```bash
node {baseDir}/scripts/chat.js "What is the meaning of life?"
```

### Use a specific model
```bash
node {baseDir}/scripts/chat.js --model grok-3-mini "Quick question: 2+2?"
```

### Vision (analyze images)
```bash
node {baseDir}/scripts/chat.js --image /path/to/image.jpg "What's in this image?"
```

### 🔍 Search X/Twitter (Real-time!)
```bash
node {baseDir}/scripts/search-x.js "Remotion video framework"
node {baseDir}/scripts/search-x.js --days 7 "Claude AI tips"
node {baseDir}/scripts/search-x.js --handles @remotion_dev "updates"
node {baseDir}/scripts/search-x.js --excluded-handles @spam,@bot "AI video creation"
node {baseDir}/scripts/search-x.js --from-date 2025-01-01 --to-date 2025-01-31 "Grok 4 launch"
node {baseDir}/scripts/search-x.js --handles @remotion_dev --from-date 2025-01-01 --image-understanding "new features"
```

Uses xAI Responses API with x_search tool for real X posts with citations.

### 🌐 Web Search (Docs & Articles)
```bash
node {baseDir}/scripts/web-search.js "xAI API documentation"
node {baseDir}/scripts/web-search.js --domains x.ai,openai.com "vision models"
node {baseDir}/scripts/web-search.js --exclude-domains reddit.com --max-results 3 "pricing comparison"
node {baseDir}/scripts/web-search.js --image-understanding "latest product screenshots"
```

Uses xAI Responses API with web_search tool for web results with citations.

> Note: This xai skill now replaces the xai-search functionality for both X/Twitter and web search.

### List available models
```bash
node {baseDir}/scripts/models.js
```

## Available Models

- `grok-3` - Most capable, best for complex tasks
- `grok-3-mini` - Fast and efficient
- `grok-3-fast` - Optimized for speed
- `grok-2-vision-1212` - Vision model for image understanding

## Example Usage

**User:** "Ask Grok what it thinks about AI safety"
**Action:** Run chat.js with the prompt

**User:** "Use Grok to analyze this image" (with attached image)
**Action:** Run chat.js with --image flag

**User:** "What Grok models are available?"
**Action:** Run models.js

**User:** "Search the web for xAI pricing updates"
**Action:** Run web-search.js with the query

**User:** "Find X posts from specific handles in January"
**Action:** Run search-x.js with --handles and --from-date/--to-date

## API Reference

xAI API Docs: https://docs.x.ai/api

## Environment Variables

- `XAI_API_KEY` - Your xAI API key (required)
- `XAI_MODEL` - Default model (optional, defaults to grok-3)

## Advanced Search Examples

```bash
# Combine handle filters with date range and media understanding
node {baseDir}/scripts/search-x.js --allowed-handles @remotion_dev,@jonnyburger --from-date 2025-01-01 --to-date 2025-01-31 --image-understanding "product updates"

# Search web with domain include/exclude and limit results
node {baseDir}/scripts/web-search.js --domains x.ai,openai.com --exclude-domains reddit.com --max-results 5 "API response formats"
```

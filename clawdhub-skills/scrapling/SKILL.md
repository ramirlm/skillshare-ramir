---
name: scrapling
description: Web scraping with the Scrapling Python framework/CLI (D4Vinci/Scrapling). Use when you need to fetch web pages (static or JS-rendered), bypass common anti-bot protections, extract content via CSS selectors, convert HTML→Markdown/text, or run Scrapling CLI commands (extract/shell/install/mcp) in this OpenClaw environment.
---

# Scrapling

Use Scrapling for quick, reliable web content extraction.

## Quick start (CLI)

This environment uses a dedicated venv at:

- `~/.venvs/scrapling/`
- CLI: `~/.venvs/scrapling/bin/scrapling`

Common commands:

- Get full HTML:
  - `~/.venvs/scrapling/bin/scrapling extract get 'https://example.com' out.html`
- Extract specific parts with a CSS selector:
  - `~/.venvs/scrapling/bin/scrapling extract get 'https://example.com' out.html -s 'main article'`
- Save as Markdown or text (based on output extension):
  - `... extract get 'https://example.com' out.md`
  - `... extract get 'https://example.com' out.txt -s 'article'`

If a page is JS-rendered or heavily protected, try dynamic/stealth fetchers (see built-in help):

- `scrapling extract fetch --help`
- `scrapling extract stealthy-fetch --help`

## Quick start (wrapper script)

A small wrapper is bundled with this skill:

- `scripts/scrapling_extract.sh <url> <out.(html|md|txt)> [css_selector]`

Example:

- `scripts/scrapling_extract.sh https://example.com out.md 'h1, h2, p'`

## Common options

- Add headers:
  - `-H 'User-Agent: ...' -H 'Accept-Language: pt-BR,pt;q=0.9,en;q=0.8'`
- Cookies:
  - `--cookies 'name=value; other=value2'`
- Proxy:
  - `--proxy 'http://user:pass@host:port'`

## Troubleshooting / setup

- Show all commands:
  - `~/.venvs/scrapling/bin/scrapling --help`
- Install optional fetcher dependencies:
  - `~/.venvs/scrapling/bin/scrapling install --help`

## References

- Upstream repo: https://github.com/D4Vinci/Scrapling
- Docs: https://scrapling.readthedocs.io/

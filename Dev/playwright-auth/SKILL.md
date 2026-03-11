---
name: playwright-auth
description: Save browser authentication for any website using Playwright. Login once, reuse forever. Simple auth storage for Twitter, LinkedIn, Facebook, etc.
version: 1.0.0
author: ramirlm
triggers:
  - "salvar autenticação"
  - "save auth"
  - "login playwright"
  - "browser auth"
metadata:
  clawdbot:
    emoji: "🔐"
    os: ["linux", "darwin"]
    requires:
      bins: ["python3"]
      packages: ["playwright"]
---

# Playwright Auth Skill

Simple skill to save browser authentication for any website.

## What it does

Opens a browser window, lets you login manually, then saves the authentication state (cookies + localStorage) to reuse later.

## Installation

```bash
pip3 install playwright --break-system-packages
playwright install chromium
```

## Usage

```bash
python3 ~/.clawdbot/skills/playwright-auth/login.py <site-name> [login-url]
```

**Examples:**

```bash
# Twitter
python3 ~/.clawdbot/skills/playwright-auth/login.py twitter

# LinkedIn
python3 ~/.clawdbot/skills/playwright-auth/login.py linkedin

# Custom site
python3 ~/.clawdbot/skills/playwright-auth/login.py mysite https://example.com/login
```

## What happens

1. Opens browser window (visible)
2. Navigates to login page
3. Waits for you to login manually
4. You press ENTER in terminal
5. Saves authentication to `~/web-auth/<site-name>.json`

## Pre-configured sites

- `twitter` → https://twitter.com/login
- `linkedin` → https://linkedin.com/login
- `facebook` → https://facebook.com/login
- `instagram` → https://instagram.com/accounts/login
- `github` → https://github.com/login
- `reddit` → https://reddit.com/login

## Saved files

Authentication saved in: `~/web-auth/`

Format: `<site-name>.json`

Example:
```
~/web-auth/
├── twitter.json
├── linkedin.json
└── github.json
```

## Using saved authentication

Load in your own scripts:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state="/home/rlmit/web-auth/twitter.json"
    )
    page = context.new_page()
    page.goto("https://x.com/...")
    # Now you're logged in!
```

Or with agent-browser (if it supports):

```bash
# Not tested but conceptually:
agent-browser --state ~/web-auth/twitter.json open https://x.com/...
```

## Re-authentication

Just run login again to refresh:

```bash
python3 ~/.clawdbot/skills/playwright-auth/login.py twitter
```

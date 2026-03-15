---
name: opensrc-fetch
description: Fetch npm package source code and public GitHub repositories with opensrc to give coding agents deeper context than type definitions only. Use when coding tasks need implementation inspection, when docs are insufficient, or when onboarding quickly into a dependency's internals.
---

# opensrc-fetch

## Quick start

1. Install (if needed):

```bash
npm install -g opensrc
```

or use directly:

```bash
npx opensrc <alvo>
```

2. Fetch a package or repository (examples below).
3. If asked later, reuse `opensrc list`, `opensrc remove`, or run another fetch.

## What this skill does

This skill guides fetching source code for:
- **npm packages** (reads package metadata and lockfiles to match installed versions)
- **public GitHub repos** (`github:` prefix, `owner/repo`, or full URL)

It is useful for coding agents that need to inspect real implementation (internals, edge cases, test helpers, build assumptions) instead of only API types.

## Commands

### NPM packages

```bash
# Detect installed version automatically
opensrc zod

# Explicit version
npx opensrc zod@3.22.0

# Multiple packages
npx opensrc react react-dom next
```

Re-running a package updates to current installed version automatically.

### GitHub repositories

```bash
# explicit github prefix
npx opensrc github:owner/repo

# shorthand
npx opensrc facebook/react

# full URL
npx opensrc https://github.com/colinhacks/zod

# branch or tag
npx opensrc owner/repo@v1.0.0
npx opensrc owner/repo#main

# mix packages and repos
npx opensrc zod facebook/react
```

### Management

```bash
npx opensrc list
npx opensrc remove zod
npx opensrc remove owner--repo
```

## File modifications and safe defaults

On first run, opensrc may prompt to update:
- `.gitignore` (add `opensrc/`)
- `tsconfig.json` (exclude `opensrc/`)
- `AGENTS.md` (add source-code guidance)

To persist preference without repeating prompts:

```bash
npx opensrc zod --modify        # allow file writes
npx opensrc zod --modify=false  # deny file writes
```

Para detalhes completos de comportamento, consulte [references/opensrc-cli.md](references/opensrc-cli.md).

## Expected output layout

After a successful fetch:

```text
opensrc/
├── settings.json      # preferences
├── sources.json       # indexed fetched sources
└── zod/               # fetched package/repo source
    ├── src/
    ├── package.json
    └── ...
```

Typical `sources.json` entry:

```json
{
  "packages": [
    {
      "name": "zod",
      "version": "3.22.0",
      "path": "opensrc/zod"
    }
  ]
}
```

`settings.json` stores preference:

```json
{
  "allowFileModifications": true
}
```

## Workflow

When asked to fetch package/source:
1. Run `opensrc <target>`.
2. Confirm result folder in `opensrc/<name>/`.
3. Check `opensrc/sources.json` for version/path.
4. Point analysis to the fetched source paths before implementing changes.
5. If needed for clean workflows, use `opensrc list` and `opensrc remove`.

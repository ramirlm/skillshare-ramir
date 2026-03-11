# opensrc CLI reference

## Behavior

- Fetches source code for dependencies so an AI coding agent can inspect implementation.
- Supports both npm packages and public GitHub repositories.
- Package fetch uses lockfile/version detection and clones matching git ref.

## Supported package/package manager lockfiles
- `package-lock.json`
- `pnpm-lock.yaml`
- `yarn.lock`

## Local storage convention
- `opensrc/<package-or-repo>/` contains extracted source.
- `opensrc/sources.json` tracks fetched assets.
- `opensrc/settings.json` stores `allowFileModifications`.

## Non-goals
- Not intended for private repos without public URL access.
- Not a package manager; it is a source-fetching utility.

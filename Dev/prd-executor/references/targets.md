# Target Configuration

Targets are defined in `config/prd-targets.json`.

## Schema

```json
{
  "targets": {
    "<target-id>": {
      "type": "local|node",
      "project": "/path/to/project",
      "nodeId": "node-name",      // required for type: node
      "description": "Human-readable description"
    }
  },
  "agents": {
    "<agent-id>": {
      "command": "agent command",
      "description": "Human-readable description"
    }
  },
  "defaults": {
    "agent": "claude",
    "checkIntervalMinutes": 10
  }
}
```

## Adding a New Target

### Local Target

```json
"local:myproject": {
  "type": "local",
  "project": "/home/user/Projects/myproject",
  "description": "My local project"
}
```

### Node Target

```json
"node:mynode": {
  "type": "node",
  "nodeId": "mynode",
  "project": "~/Projects/myproject",
  "description": "Mac node for myproject"
}
```

## Adding a New Agent

```json
"pi": {
  "command": "pi --provider anthropic",
  "description": "Pi Coding Agent with Anthropic"
}
```

## Node Setup

Before using a node target, the node must be paired:

1. On the node machine:
   ```bash
   npm i -g clawdbot
   clawdbot node pair
   ```

2. Approve the pairing request from the gateway

3. Ensure `prd-executor.sh` is available on the node:
   ```bash
   mkdir -p ~/scripts
   # Copy prd-executor.sh to ~/scripts/
   chmod +x ~/scripts/prd-executor.sh
   ```

## Listing Targets

```bash
jq '.targets | keys' config/prd-targets.json
```

## Validating Config

```bash
jq '.' config/prd-targets.json
```

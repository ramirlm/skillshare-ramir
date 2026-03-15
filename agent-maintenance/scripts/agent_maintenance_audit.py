#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path

REQUIRED = ["AGENTS.md", "SOUL.md", "MEMORY.md", "SESSION-STATE.md", "IDENTITY.md", "USER.md"]
NEEDLES = [
    "clawdmold",
    "~/Obsidian/ClawVault",
    "~/Obsidian/OpenClaw",
    "OpenClaw/Agentes/Memory Extracts",
]


def scan_agent(agent_dir: Path) -> dict:
    files = {name: (agent_dir / name).exists() for name in REQUIRED}
    findings = []
    for path in agent_dir.rglob("*.md"):
        try:
            text = path.read_text(errors="ignore")
        except Exception:
            continue
        for needle in NEEDLES:
            if needle in text:
                findings.append({"file": str(path), "needle": needle})
        if path.name == "AGENTS.md" and "memory/" in text and "memória durável" in text:
            findings.append({"file": str(path), "needle": "possible-memory-durable-ambiguity"})
    missing = [name for name, ok in files.items() if not ok]
    return {
        "agent": agent_dir.name,
        "missing": missing,
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit agent workspaces for governance drift")
    parser.add_argument("--root", default="/home/rlmit/clawdbot-agents")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    root = Path(args.root).expanduser()
    agents = sorted([p for p in root.iterdir() if p.is_dir() and not p.name.startswith('.') and p.name != 'skills'])
    rows = [scan_agent(agent) for agent in agents]

    if args.format == "json":
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return 0

    print("# Agent maintenance audit\n")
    for row in rows:
        print(f"## {row['agent']}")
        if row["missing"]:
            print("- Missing:", ", ".join(row["missing"]))
        else:
            print("- Missing: none")
        if row["findings"]:
            print("- Findings:")
            for item in row["findings"]:
                print(f"  - {item['needle']} -> {item['file']}")
        else:
            print("- Findings: none")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

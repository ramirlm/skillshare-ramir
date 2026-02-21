#!/usr/bin/env python3
import argparse
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml

# Seções que DEVEM permanecer em MEMORY.md (memória durável / regras comportamentais)
KEEP_KEYWORDS = [
    # Segurança e limites
    "REGRAS DE SEGURANÇA",
    "SEMPRE CONFIRMAR ANTES DE AGIR",

    # Preferências comportamentais do agente
    "Preferência: Busca automática",

    # Workflows de plataforma (regras curtas e críticas)
    "Cron Jobs com sessions_spawn Fix",
    "WORKFLOW WAKE-BASED",

    # Organização do conhecimento (regra do sistema)
    "Taxonomia Obsidian",
]


def now_iso_fortaleza() -> str:
    return datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-3))).isoformat(timespec="seconds")


def redact_secrets(text: str) -> str:
    # Redact obvious token patterns
    text = re.sub(r"(?i)(token\s*[:=]\s*)([^\s\"]+)", r"\1[REDACTED]", text)
    # Redact token query params
    text = re.sub(r"(?i)([?&]token=)([^&\s]+)", r"\1[REDACTED]", text)
    # Redact apiKey-ish
    text = re.sub(r"(?i)(api[_-]?key\s*[:=]\s*)([^\s\"]+)", r"\1[REDACTED]", text)
    return text


@dataclass
class SplitResult:
    kept: str
    moved: str


def split_memory(md: str) -> SplitResult:
    # naive split by level-2 headings
    parts = re.split(r"(?m)^(##\s+.*)$", md)
    if len(parts) == 1:
        return SplitResult(kept=md, moved="")

    preamble = parts[0]
    kept_sections = [preamble]
    moved_sections = []

    # parts: [preamble, h1, body1, h2, body2, ...]
    for i in range(1, len(parts), 2):
        heading = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        block = heading + body

        if any(k.lower() in heading.lower() for k in KEEP_KEYWORDS):
            kept_sections.append(block)
        else:
            moved_sections.append(block)

    kept = "".join(kept_sections).strip() + "\n"
    moved = "".join(moved_sections).strip() + "\n" if moved_sections else ""

    # Add pointer note if we moved anything
    if moved.strip():
        kept += (
            "\n---\n\n"
            "## 📦 Conteúdo operacional migrado\n\n"
            "Conteúdo longo/operacional foi migrado automaticamente para `TOOLS.md` e para um extrato no Obsidian "
            "(ver `OpenClaw/Agentes/Memory Extracts/`).\n"
        )

    return SplitResult(kept=kept, moved=moved)


def ensure_tools_header(tools_text: str) -> str:
    if tools_text.strip():
        return tools_text
    return (
        "# TOOLS.md - User Tool Notes (editable)\n\n"
        "Este arquivo é para notas operacionais, ferramentas, runbooks e convenções.\n"
        "Não é memória durável.\n\n"
    )


def write_obsidian_extract(obsidian_root: Path, agent_id: str, moved_text: str, write: bool) -> Path | None:
    if not moved_text.strip():
        return None

    out_dir = obsidian_root / "OpenClaw" / "Agentes" / "Memory Extracts" / agent_id
    out_path = out_dir / f"memory-extract-{datetime.now().strftime('%Y-%m-%d')}.md"

    fm = {
        "title": f"Memory Extract — {agent_id} — {datetime.now().strftime('%Y-%m-%d')}",
        "category": "openclaw",
        "memoryType": "extract",
        "tags": ["openclaw", "agents", "memory", agent_id],
        "processedAt": now_iso_fortaleza(),
    }

    content = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip() + "\n---\n\n"
    content += moved_text.strip() + "\n"

    if write:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")

    return out_path


def process_agent(agent_dir: Path, obsidian_root: Path, write: bool) -> dict:
    agent_id = agent_dir.name
    mem_path = agent_dir / "MEMORY.md"
    tools_path = agent_dir / "TOOLS.md"

    if not mem_path.exists():
        return {"agent": agent_id, "status": "no_memory"}

    mem_text = mem_path.read_text(encoding="utf-8", errors="replace")
    tools_text = tools_path.read_text(encoding="utf-8", errors="replace") if tools_path.exists() else ""

    split = split_memory(mem_text)
    moved_redacted = redact_secrets(split.moved)

    tools_text = ensure_tools_header(tools_text)

    appended = ""
    if moved_redacted.strip():
        appended = (
            f"\n\n---\n\n## Migrado de MEMORY.md ({datetime.now().strftime('%Y-%m-%d')})\n\n"
            + moved_redacted.strip()
            + "\n"
        )

    obs_path = write_obsidian_extract(obsidian_root, agent_id, moved_redacted, write=write)

    changed_mem = split.kept.strip() != mem_text.strip()
    changed_tools = bool(appended.strip())

    if write:
        if changed_mem:
            mem_path.write_text(split.kept, encoding="utf-8")
        if changed_tools:
            tools_path.write_text(tools_text.rstrip() + appended, encoding="utf-8")

    return {
        "agent": agent_id,
        "status": "ok",
        "memory_changed": changed_mem,
        "tools_appended": changed_tools,
        "obsidian_extract": str(obs_path) if obs_path else None,
    }


def iter_agent_dirs(root: Path):
    for p in root.iterdir():
        if not p.is_dir():
            continue
        # ignore non-agent dirs
        if p.name in {".git", "data", "logs", "skills", "plans", "reports", "scripts", "sessions", "tasks", "workflows"}:
            continue
        yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agents-root", default=str(Path.home() / "clawdbot-agents"))
    ap.add_argument("--obsidian", default=str(Path.home() / "Obsidian"))
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    agents_root = Path(os.path.expanduser(args.agents_root)).resolve()
    obsidian_root = Path(os.path.expanduser(args.obsidian)).resolve()

    results = []
    for agent_dir in iter_agent_dirs(agents_root):
        results.append(process_agent(agent_dir, obsidian_root, write=args.write))

    changed = [r for r in results if r.get("memory_changed") or r.get("tools_appended")]
    print(f"agents_root={agents_root} obsidian={obsidian_root} write={args.write} total={len(results)} changed={len(changed)}")
    for r in results:
        if r.get("status") == "ok" and (r.get("memory_changed") or r.get("tools_appended")):
            print(f"- {r['agent']}: memory_changed={r['memory_changed']} tools_appended={r['tools_appended']} obsidian_extract={r['obsidian_extract']}")


if __name__ == "__main__":
    main()

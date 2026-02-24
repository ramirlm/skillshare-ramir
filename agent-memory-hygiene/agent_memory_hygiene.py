#!/usr/bin/env python3
import argparse
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
import tempfile
import subprocess

ONTOLOGY_SCRIPT = Path('/home/rlmit/clawdbot-skills/skills/ontology/scripts/ontology.py')

KEEP_KEYWORDS = [
    "REGRAS DE SEGURANÇA",
    "SEMPRE CONFIRMAR ANTES DE AGIR",
    "Preferência: Busca automática",
    "Cron Jobs com sessions_spawn Fix",
    "WORKFLOW WAKE-BASED",
    "Taxonomia Obsidian",
]

KEEP_PATTERNS = [re.compile(re.escape(k), re.IGNORECASE) for k in KEEP_KEYWORDS]
ONTOLOGY_SCHEMA_FRAGMENT = {
    "types": {
        "Agent": {"required": ["name"], "forbidden_properties": ["password", "secret", "token"]},
        "Document": {
            "required": ["title", "source_path"],
            "forbidden_properties": ["password", "secret", "apiKey", "apiKeyRef", "bearer"],
        },
    },
    "relations": {
        "has_document": {"from_types": ["Agent"], "to_types": ["Document"], "cardinality": "one_to_many"},
    },
}


class OntologyBridge:
    """Wrapper around ontology.py with safe local file ops."""

    def __init__(self, root: Path):
        self.root = root
        self.graph = root / "graph.jsonl"
        self.schema = root / "schema.yaml"
        self._mod = self._load_module()

    def _load_module(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location("ontology_lib", ONTOLOGY_SCRIPT)
        if not spec or not spec.loader:
            raise RuntimeError("Falha ao carregar script ontology.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        # keep compatibility with relative defaults
        mod.DEFAULT_GRAPH_PATH = str(self.graph)
        mod.DEFAULT_SCHEMA_PATH = str(self.schema)
        return mod

    def ensure_schema(self) -> bool:
        self.root.mkdir(parents=True, exist_ok=True)
        self.graph.parent.mkdir(parents=True, exist_ok=True)
        self.graph.touch(exist_ok=True)
        before = self.schema.exists()
        merged = self._mod.append_schema(str(self.schema), ONTOLOGY_SCHEMA_FRAGMENT)
        return (before is False) or bool(merged)

    def _find(self, type_name: str, where: Dict[str, str]) -> List[dict]:
        return self._mod.query_entities(type_name, where, str(self.graph))

    def _create(self, type_name: str, props: Dict[str, str]) -> str:
        entity = self._mod.create_entity(type_name, props, str(self.graph))
        return entity["id"]

    def ensure_agent(self, agent_id: str) -> str:
        found = self._find("Agent", {"name": agent_id, "source": "agent-memory-hygiene"})
        if found:
            return found[0]["id"]
        return self._create("Agent", {"name": agent_id, "source": "agent-memory-hygiene", "source_path": f"{agent_id}/MEMORY.md", "status": "active"})

    def ensure_document(self, props: Dict[str, str]) -> Tuple[str, bool]:
        found = self._find(
            "Document",
            {
                "title": props.get("title", ""),
                "source_path": props.get("source_path", ""),
                "agent": props.get("agent", ""),
            },
        )
        if found:
            return found[0]["id"], False
        return self._create("Document", props), True

    def ensure_relation(self, from_id: str, rel: str, to_id: str) -> bool:
        rels = self._mod.get_related(from_id, rel, str(self.graph), direction="outgoing")
        for r in rels:
            e = r.get("entity", {})
            if e.get("id") == to_id:
                return False
        self._mod.create_relation(from_id, rel, to_id, {}, str(self.graph))
        return True

    def validate(self) -> List[str]:
        return self._mod.validate_graph(str(self.graph), str(self.schema))


def now_iso_fortaleza() -> str:
    return datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-3))).isoformat(timespec="seconds")


def redact_secrets(text: str) -> str:
    text = re.sub(r"(?i)(token\s*[:=]\s*)([^\s\"]+)", r"\\1[REDACTED]", text)
    text = re.sub(r"(?i)([?&]token=)([^&\s]+)", r"\\1[REDACTED]", text)
    text = re.sub(r"(?i)(api[_-]?key\s*[:=]\s*)([^\s\"]+)", r"\\1[REDACTED]", text)
    return text


@dataclass
class SplitResult:
    kept: str
    moved: str


SECTION_RE = re.compile(r"(?m)^(##\s+.*)$")


def _is_keep_heading(heading: str) -> bool:
    return any(p.search(heading) for p in KEEP_PATTERNS)


def split_memory(md: str) -> SplitResult:
    parts = SECTION_RE.split(md)
    if len(parts) == 1:
        return SplitResult(kept=md.strip() + "\n", moved="")

    preamble = parts[0]
    kept_sections: List[str] = [preamble]
    moved_sections: List[str] = []

    for i in range(1, len(parts), 2):
        heading = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        block = heading + body
        if _is_keep_heading(heading):
            kept_sections.append(block)
        else:
            moved_sections.append(block)

    normalized_moved = [b for b in moved_sections if b.strip()]
    kept = "".join(kept_sections).rstrip() + "\n"
    moved = "".join(normalized_moved).strip() + "\n" if normalized_moved else ""

    if moved.strip():
        kept += (
            "\n---\n\n"
            "## 📦 Conteúdo operacional migrado\n\n"
            "Conteúdo operacional foi migrado para `TOOLS.md` e para um extrato no Obsidian ("
            "`ClawVault (~/Obsidian/inbox)`).\n"
        )

    return SplitResult(kept=kept, moved=moved)


def ensure_tools_header(tools_text: str) -> str:
    if tools_text.strip().startswith("# TOOLS.md"):
        return tools_text
    if "---\n" in tools_text[:120]:
        return tools_text
    return (
        "# TOOLS.md - User Tool Notes (editable)\n\n"
        "Este arquivo é para notas operacionais, ferramentas, runbooks e convenções.\n"
        "Não é memória durável.\n\n"
    )


def normalize_heading(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lstrip("# ")).strip()


def add_actionable_corrections(content: str) -> str:
    lines = content.splitlines()
    out: List[str] = []
    todo_count = 0
    for ln in lines:
        out.append(ln)
        if re.match(r"^\s*-\s*(TODO|todo):?\s*", ln):
            todo_count += 1
            if "status:" not in ln.lower():
                out.append("  - status: pendente")
                out.append("  - impacto: revisar e validar")

    if todo_count:
        out.append("")
        out.append("### Ações corretivas (geradas)")
        out.append("- Itens com TODO receberam estrutura de rastreabilidade (`status`, `impacto`).")

    return "\n".join(out)


def process_moved_sections(moved_text: str, today: str) -> Tuple[str, List[str]]:
    if not moved_text.strip():
        return "", []

    chunks = [c for c in re.split(r"\n(?=##\s+)", moved_text.strip()) if c.strip()]
    titles: List[str] = []
    expanded: List[str] = []

    for chunk in chunks:
        m = re.match(r"^##\s+(.*)$", chunk)
        title = normalize_heading(m.group(1)) if m else "Bloco migrado"
        titles.append(title)
        expanded.append(
            f"## {title} (migração automática)\n"
            f"- extraído: {today}\n"
            "- origem: MEMORY.md\n"
            "- status: migrado\n\n"
            + add_actionable_corrections(chunk.strip())
        )

    return "\n\n".join(expanded).rstrip() + "\n", titles


def write_obsidian_extract(obsidian_root: Path, agent_id: str, moved_text: str, write: bool) -> Optional[Path]:
    if not moved_text.strip():
        return None

    title = f"memory-extract-{agent_id}-{datetime.now().strftime('%Y-%m-%d')}"
    fm = {
        "title": f"Memory Extract — {agent_id} — {datetime.now().strftime('%Y-%m-%d')}",
        "category": "agents",
        "memoryType": "extract",
        "memoryMode": "proactive",
        "tags": ["agents", "memory", agent_id],
        "processedAt": now_iso_fortaleza(),
    }
    content = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip() + "\n---\n\n"
    content += redact_secrets(moved_text.strip()) + "\n"

    if not write:
        return None

    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        tmp_file = f.name

    cmd = [
        "clawvault",
        "store",
        "-c",
        "inbox",
        "-t",
        title,
        "-f",
        tmp_file,
        "--vault",
        str(obsidian_root),
        "--no-index",
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = (proc.stdout or "") + "\n" + (proc.stderr or "")
    os.remove(tmp_file)

    m = re.search(r"^Path:\s*(.+)$", out, re.M)
    if m:
        return Path(m.group(1).strip())

    return obsidian_root / "inbox" / f"{title}.md"


def process_agent(agent_dir: Path, obsidian_root: Path, ont_bridge: Optional[OntologyBridge], write: bool) -> dict:
    agent_id = agent_dir.name
    mem_path = agent_dir / "MEMORY.md"
    tools_path = agent_dir / "TOOLS.md"
    if not mem_path.exists():
        return {"agent": agent_id, "status": "no_memory"}

    mem_text = mem_path.read_text(encoding="utf-8", errors="replace")
    tools_text = tools_path.read_text(encoding="utf-8", errors="replace") if tools_path.exists() else ""

    split = split_memory(mem_text)
    moved_redacted = redact_secrets(split.moved)
    today = datetime.now().strftime('%Y-%m-%d')
    moved_enriched, titles = process_moved_sections(moved_redacted, today)

    tools_text = ensure_tools_header(tools_text)
    appended = ""
    if moved_enriched.strip():
        appended = "\n\n---\n\n## Migrado de MEMORY.md (" + today + ")\n\n" + moved_enriched

    obs_path = write_obsidian_extract(obsidian_root, agent_id, moved_enriched, write=write)

    changed_mem = split.kept.strip() != mem_text.strip()
    changed_tools = bool(appended.strip())

    ontology_report = None
    if ont_bridge is not None and write and moved_enriched.strip():
        ont_bridge.ensure_schema()
        aid = ont_bridge.ensure_agent(agent_id)
        docs = []
        links = 0
        for title in titles:
            path_ref = str(obs_path) if obs_path else str(
                (obsidian_root / "inbox" / f"memory-extract-{agent_id}-{today}.md")
            )
            did, created = ont_bridge.ensure_document(
                {
                    "title": title,
                    "path": path_ref,
                    "source_path": f"{agent_id}/MEMORY.md",
                    "source": "agent-memory-hygiene",
                    "agent": agent_id,
                    "status": "active",
                }
            )
            linked = ont_bridge.ensure_relation(aid, "has_document", did)
            links += 1 if linked else 0
            docs.append({"title": title, "id": did, "created": created})

        ontology_report = {
            "agent_entity_id": aid,
            "documents": docs,
            "relations_added": links,
            "validation_errors": ont_bridge.validate(),
        }

    if write:
        if changed_mem:
            mem_path.write_text(split.kept, encoding="utf-8")
        if changed_tools:
            sep = "\n" if tools_text.endswith("\n") else "\n\n"
            tools_path.write_text((tools_text.rstrip() + sep + appended).rstrip() + "\n", encoding="utf-8")

    return {
        "agent": agent_id,
        "status": "ok",
        "memory_changed": changed_mem,
        "tools_appended": changed_tools,
        "obsidian_extract": str(obs_path) if obs_path else None,
        "ontology": ontology_report,
    }


def iter_agent_dirs(root: Path):
    for p in sorted(root.iterdir()):
        if not p.is_dir():
            continue
        if p.name.startswith("."):
            continue
        if p.name in {".git", "data", "logs", "skills", "plans", "reports", "scripts", "sessions", "tasks", "workflows", "memory", "dist", "node_modules"}:
            continue
        yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agents-root", default=str(Path.home() / "clawdbot-agents"))
    ap.add_argument("--obsidian", default=str(Path.home() / "Obsidian"))
    ap.add_argument("--ontology-root", default=str(Path.home() / "clawdbot-agents" / "main" / "memory" / "ontology"))
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    agents_root = Path(os.path.expanduser(args.agents_root)).resolve()
    obsidian_root = Path(os.path.expanduser(args.obsidian)).resolve()
    ontology_root = Path(os.path.expanduser(args.ontology_root)).resolve()

    bridge: Optional[OntologyBridge] = None
    if ONTOLOGY_SCRIPT.exists():
        try:
            bridge = OntologyBridge(ontology_root)
        except Exception as exc:
            print(f"[warn] ontology bridge indisponível: {exc}")
            bridge = None
    else:
        print(f"[warn] ontology não encontrada em: {ONTOLOGY_SCRIPT}")

    results = []
    for agent_dir in iter_agent_dirs(agents_root):
        results.append(process_agent(agent_dir, obsidian_root, bridge, write=args.write))

    changed = [r for r in results if r.get("status") == "ok" and (r.get("memory_changed") or r.get("tools_appended"))]
    print(f"agents_root={agents_root} obsidian={obsidian_root} ontology_root={ontology_root} write={args.write} total={len(results)} changed={len(changed)}")
    for r in results:
        if r.get("status") != "ok" or not (r.get("memory_changed") or r.get("tools_appended")):
            continue
        if r.get("ontology"):
            ent = r["ontology"]
            errs = ent.get("validation_errors") or []
            print(
                f"- {r['agent']}: memory_changed={r['memory_changed']} tools_appended={r['tools_appended']} "
                f"obsidian_extract={r['obsidian_extract']} ontology_docs={len(ent.get('documents', []))} relations={ent.get('relations_added', 0)} "
                f"ontology_errors={len(errs)}"
            )
            if errs:
                print(f"  - primeiro erro: {errs[0]}")
        else:
            print(f"- {r['agent']}: memory_changed={r['memory_changed']} tools_appended={r['tools_appended']} obsidian_extract={r['obsidian_extract']} ontology=skip")


if __name__ == "__main__":
    main()

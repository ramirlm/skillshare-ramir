#!/usr/bin/env python3
"""Transform a GitHub repo into a reusable skill scaffold in ~/clawdbot-skills."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime, timezone
from typing import List, Optional

import urllib.request


def run(cmd: List[str], cwd: Optional[Path] = None) -> str:
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed ({' '.join(cmd)}): {p.stderr.strip()}")
    return p.stdout.strip()


def normalize_repo_arg(repo: str) -> tuple[str, str]:
    """Return (owner, repo) from supported inputs."""
    repo = repo.strip()
    if repo.startswith("git@github.com:"):
        repo = repo.split(":", 1)[1]
        if repo.endswith(".git"):
            repo = repo[:-4]
    elif repo.startswith("https://github.com/") or repo.startswith("http://github.com/"):
        parts = [x for x in urlparse(repo).path.split("/") if x]
        if len(parts) >= 2:
            repo = f"{parts[0]}/{parts[1]}"

    match = re.match(r"^([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)$", repo)
    if not match:
        raise ValueError(
            "Formato inválido. Use owner/repo, https://github.com/owner/repo ou git@github.com:owner/repo.git"
        )
    return match.group(1), match.group(2)


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9-]+", "-", name.strip().lower())
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:60] if len(s) > 60 else s


def detect_language_signals(repo_root: Path) -> list[str]:
    ext_map = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "React/JSX",
        ".ts": "TypeScript",
        ".tsx": "TypeScript/React",
        ".go": "Go",
        ".rs": "Rust",
        ".java": "Java",
        ".kt": "Kotlin",
        ".rb": "Ruby",
        ".php": "PHP",
        ".cs": "C#",
        ".cpp": "C++",
        ".c": "C",
        ".swift": "Swift",
        ".dart": "Dart",
        ".mjs": "JavaScript",
        ".r": "R",
        ".scala": "Scala",
        ".sh": "Shell",
        ".lua": "Lua",
        ".jl": "Julia",
    }
    signals: set[str] = set()
    for p in repo_root.rglob("*"):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext in ext_map:
            signals.add(ext_map[ext])
        fname = p.name.lower()
        if fname in {"requirements.txt", "pyproject.toml", "setup.py", "setup.cfg", "poetry.lock"}:
            signals.add("Python")
        if fname in {"package.json", "pnpm-lock.yaml", "yarn.lock", "package-lock.json"}:
            signals.add("Node.js")
        if fname in {"go.mod", "go.sum"}:
            signals.add("Go")
        if fname in {"cargo.toml", "Cargo.toml", "Cargo.lock"}:
            signals.add("Rust")
        if fname in {"gemfile", "Gemfile", "Gemfile.lock"}:
            signals.add("Ruby")

    return sorted(signals) or ["Unknown/Multilanguage"]


def build_file_inventory(repo_root: Path, max_files: int) -> list[tuple[str, int]]:
    entries: list[tuple[str, int]] = []
    for p in repo_root.rglob("*"):
        if not p.is_file():
            continue
        rel = str(p.relative_to(repo_root))
        if any(seg in rel.split("/") for seg in {".git", "node_modules", "dist", "build", ".next"}):
            continue
        if rel.startswith(".git/"):
            continue
        entries.append((rel, p.stat().st_size))
    entries.sort(key=lambda x: x[0])
    return entries[:max_files]


def fetch_repo_metadata(owner: str, repo: str) -> dict:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    fallback = {
        "name": repo,
        "full_name": f"{owner}/{repo}",
        "description": "No description",
        "default_branch": "main",
        "stars": 0,
        "forks": 0,
        "url": f"https://github.com/{owner}/{repo}",
        "license": "n/a",
        "topics": [],
    }

    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            if r.status != 200:
                return fallback
            data = json.loads(r.read().decode("utf-8", errors="ignore"))
            return {
                "name": data.get("name") or repo,
                "full_name": data.get("full_name") or f"{owner}/{repo}",
                "description": data.get("description") or "No description",
                "default_branch": data.get("default_branch") or "main",
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "url": data.get("html_url") or f"https://github.com/{owner}/{repo}",
                "license": (data.get("license") or {}).get("spdx_id") if data.get("license") else "n/a",
                "topics": data.get("topics") or [],
            }
    except Exception:
        return fallback


def init_skill_dir(
    skill_path: Path,
    metadata: dict,
    signals: list[str],
    files: list[tuple[str, int]],
    max_files: int,
    repo_url: str,
    output_root: str,
    force: bool,
) -> None:
    if skill_path.exists() and any(skill_path.iterdir()) and not force:
        raise RuntimeError(f"Target skill exists and is not empty: {skill_path}. Use --force.")

    if skill_path.exists():
        shutil.rmtree(skill_path)
    (skill_path / "scripts").mkdir(parents=True)
    (skill_path / "references").mkdir(parents=True)

    skill_md = f"""---\nname: {skill_path.name}\ndescription: Knowledge and operations for the GitHub repo {metadata['full_name']} as a local Clawdbot skill. Use for repository-specific onboarding, implementation guidance, and follow-up coding tasks.
---\n\n# {skill_path.name}\n\n## Origem\n\n- Repositório: {metadata['url']}\n- Nome original: {metadata['full_name']}\n- Stack detectada: {', '.join(signals)}\n- Branch padrão: {metadata['default_branch']}\n\n## Uso rápido\n\n1. Leia `references/repo-overview.md` para entradas de setup, build, test e arquitetura resumida.\n2. Consulte `references/file-index.md` para localizar arquivos críticos rapidamente.\n3. Use estas referências para iniciar tarefas de implementação, refatoração ou troubleshooting.\n\n## Limites\n\n- Esta skill é gerada automaticamente e pode precisar de curadoria manual para cenários complexos.\n- Revalide comandos antes de executar em produção.\n"""
    (skill_path / "SKILL.md").write_text(skill_md, encoding="utf-8")

    overview = f"""# Repo Overview\n\n## Identificação\n- Repo: {metadata['full_name']}\n- URL: {metadata['url']}\n- Descrição: {metadata['description']}\n- Estrelas: {metadata['stars']}\n- Forks: {metadata['forks']}\n- Licença: {metadata['license']}\n- Detectado em: {datetime.now(timezone.utc).isoformat()}\n- Skills geradas em: {output_root}\n- Fonte chamada: {repo_url}\n\n## Stack detectada\n{chr(10).join(f"- {s}" for s in signals)}\n\n## Tópicos\n{chr(10).join(f"- {t}" for t in (metadata.get('topics') or [])) or '- (sem tópicos)'}\n\n## Comandos sugeridos\n- `git clone --depth 1 {repo_url} <path>`\n- `git status`\n- `git log --oneline -n 20`\n"""
    (skill_path / "references/repo-overview.md").write_text(overview, encoding="utf-8")

    lines = ["# Arquivos priorizados (subset)", "", f"Mostrar até: {max_files} arquivos", ""]
    for rel, size in files:
        lines.append(f"- `{rel}` ({size} B)")
    (skill_path / "references/file-index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    notes = """# Notas\n\n- Útil para consulta rápida e onboarding de código existente.\n- Antes de alterar produção, valide localmente com testes e revisões de contexto.\n- Regere a geração se houver mudanças estruturais relevantes no upstream.\n"""
    (skill_path / "references/notes.md").write_text(notes, encoding="utf-8")
    (skill_path / "references/source.txt").write_text(f"source={metadata['url']}\n", encoding="utf-8")


def copy_relevant_docs(src: Path, dst: Path) -> None:
    picks = [
        "README.md",
        "readme.md",
        "README.rst",
        "readme.txt",
        "CHANGELOG.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "docs/README.md",
        "documentation.md",
    ]
    for rel in picks:
        p = src / rel
        if p.exists() and p.is_file():
            out = dst / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a GitHub repo into a reusable local skill.")
    parser.add_argument("repo", help="GitHub repo: owner/repo, https URL, or git@github.com:owner/repo.git")
    parser.add_argument("--skill-name", dest="skill_name", default="")
    parser.add_argument("--output", default=str(Path.home() / "clawdbot-skills"))
    parser.add_argument("--workdir", default="/tmp/explora-repo")
    parser.add_argument("--max-files", type=int, default=200)
    parser.add_argument("--no-docs", action="store_true", help="Skip copying docs/markdown files")
    parser.add_argument("--force", action="store_true", help="Overwrite existing skill dir")
    args = parser.parse_args()

    owner, repo = normalize_repo_arg(args.repo)
    metadata = fetch_repo_metadata(owner, repo)
    skill_name = slugify(args.skill_name or repo)
    if not skill_name:
        raise SystemExit("Invalid skill name after slugification.")

    output_root = Path(args.output).expanduser().resolve()
    skill_root = output_root / skill_name
    work_root = Path(args.workdir).resolve()
    clone_dir = work_root / f"{owner}-{repo}"

    os.makedirs(output_root, exist_ok=True)
    os.makedirs(work_root, exist_ok=True)

    if clone_dir.exists():
        shutil.rmtree(clone_dir)

    clone_url = f"https://github.com/{owner}/{repo}.git"
    print(f"Clonando {clone_url} ...")
    run(["git", "clone", "--depth", "1", clone_url, str(clone_dir)])

    signals = detect_language_signals(clone_dir)
    inventory = build_file_inventory(clone_dir, args.max_files)

    init_skill_dir(
        skill_root=skill_root,
        metadata=metadata,
        signals=signals,
        files=inventory,
        max_files=args.max_files,
        repo_url=metadata["url"],
        output_root=str(output_root),
        force=args.force,
    )

    if not args.no_docs:
        copy_relevant_docs(clone_dir, skill_root)

    shutil.rmtree(clone_dir, ignore_errors=True)
    print(f"Skill criada: {skill_root}")

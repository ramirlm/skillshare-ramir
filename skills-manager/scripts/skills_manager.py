#!/usr/bin/env python3
"""skills-manager
Gerencia instalação/ativação de skills por projeto e máquina via um "preset" único.

Uso principal:
- `skills-manager apply --source <url/arquivo> [--project X]`
- `skills-manager enable <skill> ...` / `disable ...`
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import socket
import subprocess
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_TARGET_DIR = Path("~/.openclaw/skills").expanduser()
DEFAULT_CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser() / "skills-manager"
DEFAULT_OVERRIDE_FILE = DEFAULT_CONFIG_DIR / "overrides.json"
DEFAULT_PRESET_CACHE = DEFAULT_CONFIG_DIR / "preset.json"
DEFAULT_STATE_FILE = DEFAULT_CONFIG_DIR / "state.json"
DEFAULT_CACHE_DIR = Path(os.environ.get("XDG_CACHE_HOME", "~/.cache")).expanduser() / "skills-manager" / "repos"
DEFAULT_SKILL_ROOT = Path("~/clawdbot-skills").expanduser()


@dataclass
class Profile:
    enabled: List[str]
    disabled: List[str]


def normalize(name: str) -> str:
    if not name:
        return ""
    v = re.sub(r"[^a-z0-9-]+", "-", name.strip().lower())
    v = re.sub(r"-+", "-", v).strip("-")
    return v


def to_list(v: Any) -> List[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return [normalize(str(x)) for x in v if str(x).strip()]
    return [normalize(str(v))] if str(v).strip() else []


def unique_ordered(values: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for i in values:
        if i in seen:
            continue
        seen.add(i)
        out.append(i)
    return out


def read_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_json_url(url: str) -> Dict[str, Any]:
    with urllib.request.urlopen(url, timeout=25) as r:
        if r.status >= 300 or r.status < 200:
            raise RuntimeError(f"Falha ao baixar preset: HTTP {r.status}")
        return json.loads(r.read().decode("utf-8"))


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_preset(source: str | None) -> Dict[str, Any]:
    if source:
        if source.startswith("http://") or source.startswith("https://"):
            return read_json_url(source)
        return read_json(Path(source).expanduser())
    if DEFAULT_PRESET_CACHE.exists():
        return read_json(DEFAULT_PRESET_CACHE)
    raise FileNotFoundError(f"Preset não encontrado. Use --source ou salve em {DEFAULT_PRESET_CACHE}")


def load_overrides() -> Dict[str, Any]:
    if not DEFAULT_OVERRIDE_FILE.exists():
        return {}
    try:
        return read_json(DEFAULT_OVERRIDE_FILE)
    except Exception:
        return {}


def save_overrides(data: Dict[str, Any]) -> None:
    write_json(DEFAULT_OVERRIDE_FILE, data)


def profile_from_manifest(manifest_section: Dict[str, Any] | None) -> Profile:
    if not manifest_section:
        return Profile(enabled=[], disabled=[])
    return Profile(enabled=to_list(manifest_section.get("enabled")), disabled=to_list(manifest_section.get("disabled")))


def merge_profiles(*profiles: Profile) -> List[str]:
    enabled: List[str] = []
    disabled: List[str] = []
    for p in profiles:
        enabled.extend(p.enabled)
        disabled.extend(p.disabled)
    enabled = unique_ordered(enabled)
    disabled_set = set(disabled)
    return [s for s in enabled if s and s not in disabled_set]


def load_scope(name: str, source: Dict[str, Any], overrides: Dict[str, Any], project: str, machine: str) -> List[str]:
    p_global = profile_from_manifest(source.get("global", {}))
    p_machine = profile_from_manifest((source.get("machines") or {}).get(machine, {}))
    p_project = profile_from_manifest((source.get("projects") or {}).get(project, {}))

    ov = Profile(enabled=[], disabled=[])
    ovg = overrides.get("global") if isinstance(overrides.get("global"), dict) else None
    if ovg:
        ov = Profile(enabled=to_list(ovg.get("enabled")), disabled=to_list(ovg.get("disabled")))

    ovm = overrides.get("machines", {}) if isinstance(overrides.get("machines"), dict) else {}
    ovp = overrides.get("projects", {}) if isinstance(overrides.get("projects"), dict) else {}

    p_ovm = profile_from_manifest(ovm.get(machine, {}))
    p_ovp = profile_from_manifest(ovp.get(project, {}))

    return merge_profiles(p_global, p_machine, p_project, ov, p_ovm, p_ovp)


def detect_machine() -> str:
    return socket.gethostname().replace(".", "-")


def detect_project(cwd: Path | None = None) -> str:
    cwd = cwd or Path.cwd()
    try:
        repo_root = subprocess.check_output(
            ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return Path(repo_root).name
    except Exception:
        return cwd.name


def run(cmd: List[str], cwd: Path | None = None) -> None:
    subprocess.check_call(cmd, cwd=str(cwd) if cwd else None)


def clone_repo(url: str, branch: str | None = None) -> Path:
    DEFAULT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-zA-Z0-9._-]", "-", re.sub(r"https?://", "", url))
    repo_path = DEFAULT_CACHE_DIR / f"{slug[:40]}-{hashlib.sha1(url.encode()).hexdigest()[:12]}"

    if repo_path.exists():
        try:
            run(["git", "-C", str(repo_path), "fetch", "--all", "--prune"])
            if branch:
                run(["git", "-C", str(repo_path), "checkout", branch])
                run(["git", "-C", str(repo_path), "pull", "--ff-only", "origin", branch])
            else:
                run(["git", "-C", str(repo_path), "pull", "--ff-only"])
            return repo_path
        except Exception:
            # fallback: clone novo
            pass

    cmd = ["git", "clone", "--depth", "1"]
    if branch:
        cmd += ["--branch", branch]
    cmd += [url, str(repo_path)]
    print(f"[INFO] Clonando repositório de skills: {url}")
    run(cmd)
    return repo_path


def resolve_skill_source(skill: str, manifest: Dict[str, Any], fallback_root: Path) -> Path | None:
    s = manifest.get("skills", {})
    cfg = s.get(skill)
    if isinstance(cfg, str):
        p = Path(cfg).expanduser()
        return p if p.exists() else None
    if isinstance(cfg, dict):
        src_type = normalize(cfg.get("type", "path")) or "path"
        if src_type == "path":
            p = Path(cfg.get("path", "")).expanduser()
            return p if p.exists() else None
        if src_type == "git":
            repo = cfg.get("repo") or cfg.get("url")
            if not repo:
                return None
            subdir = cfg.get("subdir", "")
            branch = cfg.get("branch")
            repo_dir = clone_repo(str(repo), branch=branch)
            p = repo_dir / subdir
            return p if p.exists() else None

    local = fallback_root / skill
    return local if local.exists() else None


def sync_link(skill: str, src: Path, target_dir: Path, dry_run: bool = False) -> bool:
    target = target_dir / skill
    disabled = target_dir / f"{skill}.DISABLED"

    if disabled.exists() and not target.exists():
        if dry_run:
            print(f"[DRY-RUN] Reativar {skill} removendo .DISABLED")
            return True
        disabled.rename(target)
        print(f"[OK] Reativado: {skill}")

    if target.exists():
        if target.is_symlink():
            try:
                if target.resolve() == src.resolve():
                    return False
            except FileNotFoundError:
                pass
            if dry_run:
                print(f"[DRY-RUN] Atualizar symlink: {skill} -> {src}")
                return True
            target.unlink()
        else:
            if dry_run:
                print(f"[DRY-RUN] Substituir entrada ativa existente de {skill}")
                return True
            print(f"[WARN] {target} não é symlink; mantendo. Remova manualmente")
            return False

    if dry_run:
        print(f"[DRY-RUN] Criar symlink {skill} -> {src}")
        return True

    target.symlink_to(src)
    print(f"[OK] Ativado: {skill}")
    return True


def disable_link(skill: str, target_dir: Path, dry_run: bool = False) -> bool:
    target = target_dir / skill
    disabled = target_dir / f"{skill}.DISABLED"

    if disabled.exists():
        return False

    if not target.exists():
        if dry_run:
            print(f"[DRY-RUN] {skill} já está desativado")
            return False
        return False

    if target.is_dir() and not target.is_symlink():
        if dry_run:
            print(f"[DRY-RUN] {skill} é diretório real; não removido automaticamente")
            return False
        print(f"[WARN] {target} é diretório real; não removido automaticamente")
        return False

    if dry_run:
        print(f"[DRY-RUN] Desativar {skill} renomeando para {skill}.DISABLED")
        return True

    target.rename(disabled)
    print(f"[OK] Desativado: {skill}")
    return True


def list_installed(target_dir: Path) -> Dict[str, str]:
    out: Dict[str, str] = {}
    if not target_dir.exists():
        return out
    for f in target_dir.iterdir():
        if f.name.endswith(".DISABLED"):
            out[f.stem] = "disabled"
        elif f.is_symlink() or f.is_dir():
            out[f.name] = "enabled"
    return out


def cmd_apply(args: argparse.Namespace) -> None:
    manifest = load_preset(args.source)
    overrides = load_overrides()

    target = Path(args.target).expanduser()
    target.mkdir(parents=True, exist_ok=True)

    project = normalize(args.project or detect_project(Path(args.cwd) if args.cwd else None))
    machine = normalize(args.machine or detect_machine())
    desired = load_scope("", manifest, overrides, project, machine)

    skill_root = Path(args.skill_root).expanduser() if args.skill_root else DEFAULT_SKILL_ROOT

    print(f"[INFO] Projeto={project}")
    print(f"[INFO] Máquina={machine}")
    print(f"[INFO] Skills desejadas: {len(desired)}")

    actions = 0
    for skill in desired:
        src = resolve_skill_source(skill, manifest, skill_root)
        if not src:
            print(f"[WARN] Fonte não encontrada para {skill}")
            continue
        if sync_link(skill, src, target, dry_run=args.dry_run):
            actions += 1

    if args.prune:
        current = list_installed(target)
        for skill, state in current.items():
            if state == "enabled" and skill not in desired:
                if disable_link(skill, target, dry_run=args.dry_run):
                    actions += 1

    if args.save_state:
        payload = {
            "project": project,
            "machine": machine,
            "source": args.source,
            "timestamp": subprocess.check_output(["date", "+%Y-%m-%dT%H:%M:%S%z"], text=True).strip(),
            "enabled": desired,
            "actions": actions,
        }
        write_json(DEFAULT_STATE_FILE, payload)

    print(f"[INFO] Concluído com {actions} mudanças")


def cmd_list(args: argparse.Namespace) -> None:
    manifest = load_preset(args.source)
    overrides = load_overrides()

    project = normalize(args.project or detect_project(Path(args.cwd) if args.cwd else None))
    machine = normalize(args.machine or detect_machine())
    desired = load_scope("", manifest, overrides, project, machine)
    installed = list_installed(Path(args.target).expanduser())

    print(f"Projeto: {project}")
    print(f"Máquina: {machine}\n")

    print("Desejado")
    for s in desired:
        print(f"  - {s}")

    print("\nInstalado")
    for name, state in sorted(installed.items()):
        print(f"  - {name}: {state}")


def cmd_override(args: argparse.Namespace) -> None:
    overrides = load_overrides()

    if args.scope == "global":
        section = overrides.setdefault("global", {})
    elif args.scope == "machine":
        container = overrides.setdefault("machines", {})
        key = normalize(args.scope_id)
        section = container.setdefault(key, {})
    else:
        container = overrides.setdefault("projects", {})
        key = normalize(args.scope_id)
        section = container.setdefault(key, {})

    enabled = section.setdefault("enabled", [])
    disabled = section.setdefault("disabled", [])

    def add_unique(arr: List[str], value: str) -> None:
        if value and value not in arr:
            arr.append(value)

    for skill in args.skills:
        s = normalize(skill)
        if args.action == "enable":
            add_unique(enabled, s)
            if s in disabled:
                disabled.remove(s)
        else:
            add_unique(disabled, s)
            if s in enabled:
                enabled.remove(s)

    write_json(DEFAULT_OVERRIDE_FILE, overrides)
    print(f"[OK] {args.action}d {' / '.join(args.skills)} em escopo {args.scope}: {args.scope_id if args.scope!='global' else 'global'}")
    print("[INFO] Rode: python3 scripts/skills_manager.py apply --source <preset>")


def cmd_export(args: argparse.Namespace) -> None:
    manifest = load_preset(args.source)
    overrides = load_overrides()
    project = normalize(args.project or detect_project(Path(args.cwd) if args.cwd else None))
    machine = normalize(args.machine or detect_machine())
    desired = load_scope("", manifest, overrides, project, machine)

    out = {
        "project": project,
        "machine": machine,
        "enabled": desired,
        "source": args.source,
    }
    out_path = Path(args.output).expanduser()
    write_json(out_path, out)
    print(f"[OK] Exportado: {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gerenciador único de skills")
    parser.add_argument("--target", default=str(DEFAULT_TARGET_DIR), help="Diretório de skills do OpenClaw")
    parser.add_argument("--project", default=None, help="Projeto atual (ex.: main, codi, primo)")
    parser.add_argument("--machine", default=None, help="Máquina atual (hostname por padrão)")
    parser.add_argument("--cwd", default=None, help="Diretório base para detectar projeto via git")

    cmd = parser.add_subparsers(dest="command", required=True)

    apply = cmd.add_parser("apply", help="Sincroniza skills do projeto")
    apply.add_argument("--source", default=None, help="Preset local/URL")
    apply.add_argument("--skill-root", default=str(DEFAULT_SKILL_ROOT), help="Raiz para skills locais")
    apply.add_argument("--prune", action="store_true", help="Desativa skills ativas que não estão no desired")
    apply.add_argument("--dry-run", action="store_true", help="Simula sem alterar arquivos")
    apply.add_argument("--save-state", action="store_true", help="Grava estado em ~/.config/skills-manager/state.json")
    apply.set_defaults(func=cmd_apply)

    list_cmd = cmd.add_parser("list", help="Mostra desired x installed")
    list_cmd.add_argument("--source", default=None, help="Preset local/URL")
    list_cmd.set_defaults(func=cmd_list)

    enable = cmd.add_parser("enable", help="Ativa skill no contexto selecionado")
    enable.add_argument("skills", nargs="+", help="Skills")
    enable.add_argument("--scope", choices=["project", "machine", "global"], default="project")
    enable.set_defaults(action="enable", func=cmd_override)

    disable = cmd.add_parser("disable", help="Desativa skill no contexto selecionado")
    disable.add_argument("skills", nargs="+", help="Skills")
    disable.add_argument("--scope", choices=["project", "machine", "global"], default="project")
    disable.set_defaults(action="disable", func=cmd_override)

    export = cmd.add_parser("export", help="Exporta estado desejado para JSON")
    export.add_argument("--source", default=None, help="Preset local/URL")
    export.add_argument("--output", required=True, help="Arquivo destino")
    export.set_defaults(func=cmd_export)

    args = parser.parse_args()

    if args.command in {"enable", "disable"}:
        if args.scope == "project":
            args.scope_id = normalize(args.project or detect_project(Path(args.cwd) if args.cwd else None))
        elif args.scope == "machine":
            args.scope_id = normalize(args.machine or detect_machine())
        else:
            args.scope_id = "global"

    args.func(args)


if __name__ == "__main__":
    main()

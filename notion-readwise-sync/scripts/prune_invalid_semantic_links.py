#!/usr/bin/env python3
"""Clamp semantic frontmatter fields to existing ontology entities."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Set

import yaml

SEM_FIELDS = {"people", "project", "projects", "topics", "related", "owner", "tags"}



def load_frontmatter(text: str):
    if not text.startswith("---"):
        return {}, None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, None, text
    fm = yaml.safe_load(parts[1]) or {}
    body = f"---\n{parts[2]}" if not parts[2].startswith("\n") else parts[2]
    return fm, parts[1], body


def index_slug_set(vault: Path, folder: str) -> Set[str]:
    values = set()
    f = vault / folder
    if not f.exists():
        return values
    for file in f.glob("*.md"):
        stem = file.stem.strip()
        if not stem:
            continue
        normalized = re.sub(r"\.md$", "", stem, flags=re.IGNORECASE)
        values.add(normalized)
        values.add(slug_normalized(stem))
    return values


def slug_normalized(value: str) -> str:
    v = re.sub(r"\s+", "-", str(value or "").strip().lower())
    v = re.sub(r"[^a-z0-9_-]", "", v)
    v = re.sub(r"-+", "-", v).strip("-_")
    return v


def is_placeholder(v: str) -> bool:
    lv = (v or "").strip().lower()
    if not lv:
        return True
    if lv in {"todo", "tbd", "to do", "n/a", "na", "none", "null", "", "...", "untitled"}:
        return True
    return lv.startswith("${") or lv.endswith("}")


def split_wikilink(v: str) -> str:
    v = (v or "").strip()
    if v.startswith("[[") and v.endswith("]]"):
        v = v[2:-2].strip()
    if "/" in v:
        v = v.rsplit("/", 1)[-1]
    return v.strip()


def normalize_scalar(v, allowed: Set[str]):
    if not isinstance(v, str):
        return None
    v = split_wikilink(v)
    v = re.sub(r"\.(md|markdown)$", "", v, flags=re.IGNORECASE)
    v = slug_normalized(v)
    if not v or is_placeholder(v):
        return None
    return v if v in allowed else None


def normalize_list(values, allowed: Set[str]):
    if not isinstance(values, list):
        return []
    out = []
    seen = set()
    for item in values:
        if not isinstance(item, str):
            continue
        v = normalize_scalar(item, allowed)
        if not v or v in seen:
            continue
        seen.add(v)
        out.append(v)
    return out


def prune_file(path: Path, people: set, projects: set, topics: set, dry_run: bool = False):
    txt = path.read_text(encoding="utf-8")
    fm, _, body = load_frontmatter(txt)
    if not isinstance(fm, dict):
        return {"file": str(path), "changed": False, "invalid_frontmatter": True}

    changed = False
    invalid_fm = False

    field_defs = [
        ("people", people),
        ("projects", projects),
        ("topics", topics),
        ("related", topics | projects | people),
    ]

    if "project" in fm:
        after = normalize_scalar(fm.get("project"), projects | topics | people)
        if (fm.get("project") or None) != after:
            changed = True
            if after is None:
                fm.pop("project", None)
            else:
                fm["project"] = after

    if "owner" in fm:
        after = normalize_scalar(fm.get("owner"), people | projects | topics)
        if (fm.get("owner") or None) != after:
            changed = True
            if after is None:
                fm.pop("owner", None)
            else:
                fm["owner"] = after

    for field, allowed in field_defs:
        if field in fm:
            before = list(fm.get(field) or [])
            after = normalize_list(before, allowed)
            if before != after:
                changed = True
                fm[field] = after

    # generic cleanup for common free fields that can get placeholder content
    for field in SEM_FIELDS - {"people", "projects", "topics", "related", "owner", "project", "tags"}:
        if field not in fm:
            continue
        if is_placeholder(fm.get(field, "") if not isinstance(fm.get(field), list) else ""):
            fm[field] = ""
            changed = True

    if fm and not isinstance(fm, dict):
        invalid_fm = True

    if changed and not dry_run:
        fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
        path.write_text(f"---\n{fm_text}---\n{body}", encoding="utf-8")

    return {"file": str(path), "changed": changed, "invalid_frontmatter": invalid_fm}


def walk(vault: Path):
    root = vault / "Knowledge" / "Readwise"
    if not root.exists():
        return
    for p in root.rglob("*.md"):
        if "_state" in p.parts:
            continue
        yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    people = index_slug_set(vault, "people")
    projects = index_slug_set(vault, "projects")
    topics = index_slug_set(vault, "topics")
    topics.update(index_slug_set(vault, "lesson"))

    checked = 0
    changed = 0
    invalid_frontmatter = 0
    for f in walk(vault):
        checked += 1
        res = prune_file(f, people, projects, topics, dry_run=args.dry_run)
        if res["changed"]:
            changed += 1
        if res["invalid_frontmatter"]:
            invalid_frontmatter += 1

    print(json.dumps({
        "vault": str(vault),
        "checked": checked,
        "changed": changed,
        "invalid_frontmatter": invalid_frontmatter,
        "dry_run": args.dry_run,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

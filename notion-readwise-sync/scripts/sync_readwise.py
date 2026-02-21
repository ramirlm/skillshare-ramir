#!/usr/bin/env python3
"""notion-readwise-sync (READ-ONLY)

Sync a Notion Readwise "Library" child database (nested inside a page) into an Obsidian
vault as curated Markdown notes.

Hard constraints:
- READ-ONLY against Notion API (only GET/POST query/search endpoints).
- Never PATCH/POST to /v1/pages, /v1/blocks/.../children, /v1/databases, etc.

This script now tracks per-run diff (added/updated/skipped), writes a diff artifact
and updates ontology candidates whenever content is added/updated.
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import urllib.request

NOTION_VERSION = "2025-09-03"

CATEGORY_MAP = {
    "Books": "Livros",
    "PDFs": "PDFs",
    "Videos": "Videos",
    "Articles": "Artigos",
    "Podcasts": "Podcasts",
    "Tweets": None,  # ignored
}

DEFAULT_CATEGORIES = ["Books", "PDFs", "Videos", "Articles", "Podcasts"]


def _now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def slugify(s: str, max_len: int = 120) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9\s\-_.]+", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s[:max_len].strip("-_") or "untitled"


def read_notion_key() -> str:
    k = os.environ.get("NOTION_API_KEY")
    if k and k.strip():
        return k.strip()
    p = Path.home() / ".config" / "notion" / "api_key"
    if p.exists():
        return p.read_text(encoding="utf-8").strip()
    raise RuntimeError("NOTION_API_KEY not set and ~/.config/notion/api_key not found")


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def md_escape(s: str) -> str:
    return (s or "").replace("\r\n", "\n").replace("\r", "\n")


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class NotionClient:
    def __init__(self, key: str):
        self.key = key

    def request(self, method: str, path: str, payload: Optional[dict] = None) -> dict:
        url = f"https://api.notion.com{path}"
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }
        data = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            raise RuntimeError(f"Notion API error {method} {path}: {e}")

    def get_block_children(self, block_id: str, page_size: int = 100) -> List[dict]:
        results: List[dict] = []
        cursor: Optional[str] = None
        while True:
            qs = f"?page_size={page_size}"
            if cursor:
                qs += f"&start_cursor={cursor}"
            data = self.request("GET", f"/v1/blocks/{block_id}/children{qs}")
            results.extend(data.get("results", []))
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
            if not cursor:
                break
        return results

    def get_database(self, database_id: str) -> dict:
        return self.request("GET", f"/v1/databases/{database_id}")

    def get_data_source(self, data_source_id: str) -> dict:
        return self.request("GET", f"/v1/data_sources/{data_source_id}")

    def query_data_source(
        self,
        data_source_id: str,
        filter_obj: Optional[dict] = None,
        sorts: Optional[list] = None,
        page_size: int = 100,
        limit: Optional[int] = None,
    ) -> List[dict]:
        results: List[dict] = []
        cursor: Optional[str] = None
        while True:
            payload: Dict[str, Any] = {"page_size": min(page_size, 100)}
            if filter_obj:
                payload["filter"] = filter_obj
            if sorts:
                payload["sorts"] = sorts
            if cursor:
                payload["start_cursor"] = cursor
            data = self.request("POST", f"/v1/data_sources/{data_source_id}/query", payload)
            results.extend(data.get("results", []))
            if limit is not None and len(results) >= limit:
                return results[:limit]
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
            if not cursor:
                break
        return results


def find_child_database_block(blocks: List[dict], title: str) -> Optional[dict]:
    title_norm = (title or "").strip().lower()
    for b in blocks:
        if b.get("type") == "child_database":
            child = b.get("child_database") or {}
            if (child.get("title") or "").strip().lower() == title_norm:
                return b
    return None


def get_plain_title(page: dict) -> str:
    props = page.get("properties") or {}
    if "Title" in props and props["Title"].get("type") == "title":
        arr = props["Title"].get("title") or []
        if arr:
            return arr[0].get("plain_text") or ""
    if "Name" in props and props["Name"].get("type") == "title":
        arr = props["Name"].get("title") or []
        if arr:
            return arr[0].get("plain_text") or ""
    for v in props.values():
        if isinstance(v, dict) and v.get("type") == "title":
            arr = v.get("title") or []
            if arr:
                return arr[0].get("plain_text") or ""
    return ""


def prop_select(page: dict, name: str) -> Optional[str]:
    p = (page.get("properties") or {}).get(name)
    if not isinstance(p, dict):
        return None
    if p.get("type") == "select" and p.get("select"):
        return p["select"].get("name")
    return None


def prop_url(page: dict, name: str) -> Optional[str]:
    p = (page.get("properties") or {}).get(name)
    if not isinstance(p, dict):
        return None
    return p.get("url") if p.get("type") == "url" else None


def prop_rich_text(page: dict, name: str) -> str:
    p = (page.get("properties") or {}).get(name)
    if not isinstance(p, dict):
        return ""
    if p.get("type") != "rich_text":
        return ""
    return "".join([x.get("plain_text", "") for x in (p.get("rich_text") or [])]).strip()


def prop_multi_select(page: dict, name: str) -> List[str]:
    p = (page.get("properties") or {}).get(name)
    if not isinstance(p, dict):
        return []
    if p.get("type") == "multi_select":
        return [x.get("name") for x in (p.get("multi_select") or []) if x.get("name")]
    return []


def prop_number(page: dict, name: str) -> Optional[float]:
    p = (page.get("properties") or {}).get(name)
    if not isinstance(p, dict):
        return None
    return p.get("number") if p.get("type") == "number" else None


def prop_date(page: dict, name: str) -> Optional[str]:
    p = (page.get("properties") or {}).get(name)
    if not isinstance(p, dict):
        return None
    if p.get("type") == "date" and p.get("date"):
        return p["date"].get("start")
    return None


def compute_relevance(category: str) -> str:
    if category in ("Books", "PDFs", "Videos"):
        return "high"
    if category in ("Articles", "Podcasts"):
        return "medium"
    return "low"


def guess_topics(title: str, tags: List[str], summary: str = "", notes: str = "") -> List[str]:
    kws = set([t.strip() for t in tags if t.strip()])
    for w in re.findall(r"[A-Za-z][A-Za-z0-9_\-]{4,}", title or ""):
        kws.add(w)
    for w in re.findall(r"[A-Za-z][A-Za-z0-9_\-]{4,}", summary or ""):
        kws.add(w)
    for w in re.findall(r"[A-Za-z][A-Za-z0-9_\-]{4,}", notes or ""):
        kws.add(w)
    return sorted(kws)[:24]


def infer_ontology_candidates(title: str, summary: str, source_url: str, author: str, tags: List[str], category: str) -> dict:
    people = []
    companies = []
    projects = []
    topics = set([x for x in (tags or []) if x])

    # Heuristic candidates from common signals
    for token in re.split(r"\s+", (author or "").strip()):
        if token and token.lower() not in {"and", "the", "with", "for", "para", "sobre", "de"}:
            people.append(token)

    if source_url:
        if "twitter.com" in source_url or "x.com" in source_url:
            topics.add("social-media")
        if "youtube.com" in source_url or "youtu.be" in source_url:
            topics.add("video")
    if category == "Books":
        topics.add("book")
    if category == "PDFs":
        topics.add("pdf")
    if category == "Videos":
        topics.add("video")

    title_slug = (title or "").lower()
    if "gpt" in title_slug or "openai" in title_slug:
        topics.add("ai")

    return {
        "topics": sorted({t for t in topics if t}),
        "people_candidates": sorted({x for x in people if x}),
        "company_candidates": sorted({x for x in companies if x}),
        "project_candidates": sorted({x for x in projects if x}),
    }


def yaml_kv(v: Any) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        esc = [json.dumps(x, ensure_ascii=False) for x in v]
        return "[" + ", ".join(esc) + "]"
    return json.dumps(str(v), ensure_ascii=False)


def write_markdown_note(out_path: Path, fm: Dict[str, Any], body: str) -> str:
    ensure_dir(out_path.parent)
    fm_lines = ["---"]
    for k, v in fm.items():
        fm_lines.append(f"{k}: {yaml_kv(v)}")
    fm_lines.append("---")
    fm_lines.append("")
    content = "\n".join(fm_lines) + body
    out_path.write_text(content, encoding="utf-8")
    return content


def build_body(page: dict, fm: Dict[str, Any], title: str, category: str, summary: str, notes: str, source_url: Optional[str], author: Optional[str], last_synced: Optional[str]) -> str:
    body_parts = [f"# {md_escape(title)}\n"]
    if source_url:
        body_parts.append(f"Fonte: {source_url}\n")
    if author:
        body_parts.append(f"Autor: {md_escape(author)}\n")
    if last_synced:
        body_parts.append(f"Last Synced: {last_synced}\n")
    body_parts.append("\n---\n")

    body_parts.append("## Curadoria\n")
    body_parts.append("- Relevância (computed): " + fm["relevance"] + "\n")
    body_parts.append(f"- Categoria: {category}\n")
    if fm.get("topics"):
        body_parts.append("- Tópicos mapeados: " + ", ".join(fm["topics"]) + "\n")
    body_parts.append("- Aplicações práticas pro Ramir: \n")
    body_parts.append("- Próxima ação sugerida: \n\n")

    if category in ("Books", "PDFs", "Videos"):
        body_parts.append("## Resumo\n")
        body_parts.append((md_escape(summary) if summary else "(preencher)") + "\n\n")
        body_parts.append("## Insights\n- (preencher)\n\n")
        body_parts.append("## Aplicações\n- (preencher)\n\n")

    if notes:
        body_parts.append("## Notas (Readwise)\n")
        body_parts.append(md_escape(notes) + "\n\n")

    body_parts.append("## Metadados\n")
    body_parts.append(f"- Notion: {fm['notion_url']}\n")
    if fm.get("tags"):
        body_parts.append(f"- Tags: {', '.join(fm['tags'])}\n")
    if fm.get("highlights") is not None:
        body_parts.append(f"- Highlights: {fm['highlights']}\n")

    return "".join(body_parts)


def file_path_for(vault: Path, category: str, notion_id: str, title: str) -> Path:
    base_dir = vault / "Knowledge" / "Readwise"
    return base_dir / CATEGORY_MAP[category] / f"{slugify(title)}__{notion_id}.md"


def parse_iso_bool(v: str) -> bool:
    return bool(v and str(v).strip().lower() in {"1", "true", "yes", "y"})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True, help="Obsidian vault root")
    ap.add_argument("--page-id", required=True, help="Notion page_id (Readwise container page)")
    ap.add_argument("--db-title", default="Library", help="Child database title")
    ap.add_argument("--categories", default=",".join(DEFAULT_CATEGORIES), help="Comma-separated categories to include")
    ap.add_argument("--limit-per-category", type=int, default=30)
    ap.add_argument("--since-days", type=int, default=0, help="0 = import all (no since-days cutoff)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--enable-ontology", default="true", help="Write ontology candidate files (true/false)")
    args = ap.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    base_dir = vault / "Knowledge" / "Readwise"
    state_dir = base_dir / "_state"
    runs_dir = state_dir / "runs"
    ont_dir = base_dir / "_ontology-candidates"

    for p in (state_dir, runs_dir, ont_dir):
        ensure_dir(p)

    do_ontology = parse_iso_bool(args.enable_ontology)

    c = NotionClient(read_notion_key())

    # locate nested child db
    root_blocks = c.get_block_children(args.page_id, page_size=100)
    child_db_block = find_child_database_block(root_blocks, args.db_title)
    if not child_db_block:
        raise RuntimeError(f"Could not find child_database titled '{args.db_title}' under page {args.page_id}")

    database_id = child_db_block.get("id")
    db = c.get_database(database_id)
    data_sources = db.get("data_sources") or []
    if not data_sources:
        raise RuntimeError(f"Database {database_id} has no data_sources")
    data_source_id = data_sources[0].get("id")
    if not data_source_id:
        raise RuntimeError("Could not resolve data_source_id")

    ds = c.get_data_source(data_source_id)
    if "Category" not in (ds.get("properties") or {}):
        raise RuntimeError("Expected property 'Category' in data source")

    include_categories = [x.strip() for x in args.categories.split(",") if x.strip()]

    index_path = state_dir / "index.json"
    index_prev: dict = {}
    if index_path.exists():
        try:
            index_prev = json.loads(index_path.read_text(encoding="utf-8"))
        except Exception:
            index_prev = {}

    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = runs_dir / run_id
    ensure_dir(run_dir)

    run_meta = {
        "runId": run_id,
        "ranAt": _now_iso(),
        "pageId": args.page_id,
        "databaseId": database_id,
        "dataSourceId": data_source_id,
        "dbTitle": args.db_title,
        "categories": include_categories,
        "limitPerCategory": args.limit_per_category,
        "sinceDays": args.since_days,
        "dryRun": args.dry_run,
        "ontologyEnabled": do_ontology,
        "stats": {"added": 0, "updated": 0, "skipped": 0, "errors": 0},
        "items": {"added": [], "updated": [], "unchanged": []},
    }

    added: list = []
    updated: list = []
    unchanged: list = []
    skipped: list = []
    diffs: list = []
    ontology_events: list = []

    since_cutoff = None if args.since_days is None or args.since_days <= 0 else dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=args.since_days)

    for cat in include_categories:
        if CATEGORY_MAP.get(cat) is None:
            continue

        items = c.query_data_source(
            data_source_id,
            filter_obj={"property": "Category", "select": {"equals": cat}},
            sorts=[{"property": "Last Synced", "direction": "descending"}],
            page_size=100,
            limit=args.limit_per_category,
        )

        for page in items:
            pid = page.get("id")
            try:
                notion_url = page.get("url")
                title = get_plain_title(page) or prop_rich_text(page, "Full Title") or "(sem título)"
                category = prop_select(page, "Category") or cat
                if category == "Tweets":
                    run_meta["stats"]["skipped"] += 1
                    skipped.append({"notion_page_id": pid, "reason": "category_ignored"})
                    continue

                last_synced = prop_date(page, "Last Synced")
                if last_synced:
                    try:
                        parsed = dt.datetime.fromisoformat(last_synced.replace("Z", "+00:00"))
                        if parsed.tzinfo is None:
                            parsed = parsed.replace(tzinfo=dt.timezone.utc)
                        if since_cutoff is not None and parsed < since_cutoff:
                            run_meta["stats"]["skipped"] += 1
                            skipped.append({"notion_page_id": pid, "reason": "older_than_since_days"})
                            continue
                    except Exception:
                        pass

                source_url = prop_url(page, "URL")
                tags = prop_multi_select(page, "Document Tags")
                author = prop_rich_text(page, "Author")
                highlights = prop_number(page, "Highlights")
                summary = prop_rich_text(page, "Summary")
                notes = prop_rich_text(page, "Document Notes")

                topics = guess_topics(title, tags, summary, notes)
                ontology = infer_ontology_candidates(title, summary, source_url or "", author or "", tags, category)
                relevance = compute_relevance(category)

                prev_entry = index_prev.get(pid)
                prev_hash = prev_entry.get("content_hash") if isinstance(prev_entry, dict) else None
                prev_updated_at = prev_entry.get("updated_at") if isinstance(prev_entry, dict) else None

                fm = {
                    "type": "readwise-item",
                    "source": "notion.readwise",
                    "notion_page_id": pid,
                    "notion_url": notion_url,
                    "category": category,
                    "source_url": source_url,
                    "tags": tags,
                    "author": author or None,
                    "highlights": highlights,
                    "last_synced": last_synced,
                    "relevance": relevance,
                    "topics": topics,
                    "people": ontology["people_candidates"],
                    "companies": ontology["company_candidates"],
                    "projects": ontology["project_candidates"],
                    "status": "curated",
                    "curated_at": last_synced or prev_updated_at or _now_iso(),
                }

                # Use stable curated_at to prevent false updates when content unchanged.
                body = build_body(page, fm, title, category, summary, notes, source_url, author, last_synced)
                out_path = file_path_for(vault, category, pid, title)
                current_content = "---\n" + "\n".join(["{}: {}".format(k, yaml_kv(v)) for k, v in fm.items()]) + "\n---\n\n" + body
                curr_hash = sha256_text(current_content)

                rel = {
                    "notion_page_id": pid,
                    "title": title,
                    "category": category,
                    "vault_path": str(out_path.relative_to(vault)),
                    "notion_url": notion_url,
                }

                if args.dry_run:
                    run_meta["stats"]["added"] += 1
                    added.append(rel)
                    continue


                if prev_hash is None or not out_path.exists():
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    out_path.write_text(current_content, encoding="utf-8")
                    run_meta["stats"]["added"] += 1
                    added.append(rel)
                else:
                    prev_content = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
                    if sha256_text(prev_content) == curr_hash:
                        run_meta["stats"]["written"] = run_meta["stats"].get("written", 0) + 0
                        unchanged.append(rel)
                    else:
                        before_lines = prev_content.splitlines()
                        after_lines = current_content.splitlines()
                        patch = "\n".join(difflib.unified_diff(before_lines, after_lines, fromfile="prev", tofile="new", lineterm=""))
                        diffs.append({
                            "notion_page_id": pid,
                            "path": str(out_path.relative_to(vault)),
                            "patch": patch,
                        })
                        out_path.write_text(current_content, encoding="utf-8")
                        run_meta["stats"]["updated"] += 1
                        updated.append(rel)

                if do_ontology:
                    cand = {
                        "notion_page_id": pid,
                        "notion_url": notion_url,
                        "title": title,
                        "category": category,
                        "source_url": source_url,
                        "topics": topics,
                        "people_candidates": ontology["people_candidates"],
                        "company_candidates": ontology["company_candidates"],
                        "project_candidates": ontology["project_candidates"],
                        "relevance": relevance,
                        "generated_at": fm["curated_at"],
                    }
                    if not args.dry_run:
                        (ont_dir / f"{pid}.json").write_text(
                            json.dumps(cand, ensure_ascii=False, indent=2),
                            encoding="utf-8",
                        )
                    ontology_events.append(cand)

                index_prev[pid] = {
                    "path": str(out_path.relative_to(vault)),
                    "category": category,
                    "title": title,
                    "source_url": source_url,
                    "last_synced": last_synced,
                    "updated_at": fm["curated_at"],
                    "content_hash": curr_hash,
                    "status": "curated",
                }

            except Exception:
                run_meta["stats"]["errors"] += 1

    run_meta["items"] = {
        "added": added,
        "updated": updated,
        "unchanged": unchanged,
        "skipped": skipped,
    }
    run_meta["diffs_count"] = len(diffs)
    run_meta["ontology_count"] = len(ontology_events)

    # write run artifacts
    if not args.dry_run:
        index_path.write_text(json.dumps(index_prev, ensure_ascii=False, indent=2), encoding="utf-8")
        (state_dir / "last-run.json").write_text(json.dumps(run_meta, ensure_ascii=False, indent=2), encoding="utf-8")
        (run_dir / "summary.json").write_text(json.dumps(run_meta, ensure_ascii=False, indent=2), encoding="utf-8")
        (run_dir / "diff.jsonl").write_text("\n".join(json.dumps(d, ensure_ascii=False) for d in diffs), encoding="utf-8")
        (run_dir / "ontologized.jsonl").write_text("\n".join(json.dumps(d, ensure_ascii=False) for d in ontology_events), encoding="utf-8")

    print(json.dumps(run_meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
import argparse
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml

FRONTMATTER_BOUNDARY = "---"


def tz_offset_iso(dt: datetime) -> str:
    # dt should be aware
    return dt.isoformat(timespec="seconds")


def now_iso_fortaleza_fixed() -> str:
    # Fixed -03:00 offset (America/Fortaleza).
    return datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-3))).isoformat(timespec="seconds")


def parse_iso(dt_str: str) -> datetime | None:
    if not dt_str or not isinstance(dt_str, str):
        return None
    try:
        # Python accepts offsets like -03:00
        return datetime.fromisoformat(dt_str)
    except Exception:
        return None


@dataclass
class MdDoc:
    path: Path
    frontmatter: dict | None
    body: str
    had_frontmatter: bool


def split_frontmatter(text: str) -> MdDoc:
    # Only treat as frontmatter if file starts with ---\n
    if text.startswith(FRONTMATTER_BOUNDARY + "\n"):
        end = text.find("\n" + FRONTMATTER_BOUNDARY + "\n", len(FRONTMATTER_BOUNDARY) + 1)
        if end != -1:
            fm_raw = text[len(FRONTMATTER_BOUNDARY) + 1 : end]
            body = text[end + len("\n" + FRONTMATTER_BOUNDARY + "\n") :]
            try:
                fm = yaml.safe_load(fm_raw) or {}
                if not isinstance(fm, dict):
                    fm = {"_frontmatter": fm}
            except Exception:
                fm = {}
            return fm, body, True
    return None, text, False


def make_title_from_path(p: Path) -> str:
    stem = p.stem
    # Common cleanup: underscores/hyphens -> spaces
    title = re.sub(r"[_-]+", " ", stem).strip()
    # Collapse multiple spaces
    title = re.sub(r"\s+", " ", title)
    return title or stem


def extract_summary(body: str, max_len: int = 240) -> str:
    # Remove code blocks quickly
    body2 = re.sub(r"```[\s\S]*?```", " ", body)
    lines = [ln.strip() for ln in body2.splitlines()]

    # Skip headings, empty, list markers until we find a paragraph-like line
    para = []
    for ln in lines:
        if not ln:
            if para:
                break
            continue
        if ln.startswith("#"):
            continue
        if re.match(r"^[-*+]\s+", ln):
            continue
        if re.match(r"^\d+\.\s+", ln):
            continue
        para.append(ln)
        # If paragraph is forming, allow multiline
        if len(" ".join(para)) >= max_len:
            break

    summary = " ".join(para).strip()
    summary = re.sub(r"\s+", " ", summary)
    if not summary:
        # fallback: first non-empty line even if heading
        for ln in lines:
            if ln:
                summary = ln
                break
    summary = summary.strip()
    if len(summary) > max_len:
        summary = summary[: max_len - 1].rstrip() + "…"
    return summary


def dump_frontmatter(fm: dict) -> str:
    # Keep deterministic ordering for key fields first
    key_order = ["title", "summary", "date", "category", "memoryType", "priority", "tags", "processedAt"]
    ordered = {}
    for k in key_order:
        if k in fm:
            ordered[k] = fm[k]
    for k in fm.keys():
        if k not in ordered:
            ordered[k] = fm[k]

    y = yaml.safe_dump(ordered, sort_keys=False, allow_unicode=True).strip()
    return f"{FRONTMATTER_BOUNDARY}\n{y}\n{FRONTMATTER_BOUNDARY}\n"


def should_skip(path: Path, fm: dict) -> bool:
    processed_at = parse_iso(fm.get("processedAt"))
    if not processed_at:
        return False
    # if file modified after processedAt, must reprocess
    mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
    pa = processed_at
    if pa.tzinfo is None:
        pa = pa.replace(tzinfo=timezone.utc)
    # compare in UTC
    if mtime > pa.astimezone(timezone.utc):
        return False
    if not fm.get("title") or not fm.get("summary"):
        return False
    return True


def process_file(path: Path, write: bool) -> tuple[str, bool, str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Try latin-1 fallback
        text = path.read_text(encoding="latin-1")

    fm, body, had = split_frontmatter(text)
    fm = fm or {}

    if had and should_skip(path, fm):
        return ("skipped", False, None)

    changed = False

    if not fm.get("title"):
        fm["title"] = make_title_from_path(path)
        changed = True

    if not fm.get("summary"):
        fm["summary"] = extract_summary(body)
        changed = True

    # Always update processedAt when we consider it processed
    fm["processedAt"] = now_iso_fortaleza_fixed()
    changed = True

    new_text = dump_frontmatter(fm) + body.lstrip("\n")

    if write:
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            return ("updated", True, None)
        else:
            return ("processed", False, None)
    else:
        return ("dryrun", changed, None)


def iter_md_files(vault: Path):
    for p in vault.rglob("*.md"):
        # ignore hidden dirs like .obsidian
        if any(part.startswith(".") for part in p.parts):
            continue
        yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", default=str(Path.home() / "Obsidian"))
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    vault = Path(os.path.expanduser(args.vault)).resolve()
    if not vault.exists():
        print(f"ERROR: vault not found: {vault}", file=sys.stderr)
        sys.exit(2)

    total = updated = skipped = processed = dryrun = errors = 0

    for p in iter_md_files(vault):
        total += 1
        if args.limit and total > args.limit:
            break
        try:
            status, did_update, err = process_file(p, write=args.write)
            if status == "updated":
                updated += 1
            elif status == "skipped":
                skipped += 1
            elif status == "processed":
                processed += 1
            elif status == "dryrun":
                dryrun += 1
        except Exception as e:
            errors += 1
            print(f"ERROR: {p}: {e}", file=sys.stderr)

    print(
        f"vault={vault} total={total} updated={updated} skipped={skipped} processed={processed} dryrun={dryrun} errors={errors} write={args.write}"
    )


if __name__ == "__main__":
    main()

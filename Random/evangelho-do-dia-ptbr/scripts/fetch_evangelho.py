#!/usr/bin/env python3
"""Busca o Evangelho do dia (PT-BR) via evangeli.net.

Uso:
  python3 scripts/fetch_evangelho.py            # hoje (America/Fortaleza), tudo + reflexão
  python3 scripts/fetch_evangelho.py 2026-02-17
  python3 scripts/fetch_evangelho.py --somente-evangelho
  python3 scripts/fetch_evangelho.py --sem-reflexao

Saída: Markdown (stdout)
"""

from __future__ import annotations

import argparse
import datetime as dt
import html as ihtml
import re
import sys
from zoneinfo import ZoneInfo

import requests

TZ = ZoneInfo("America/Fortaleza")
BASE = "https://evangeli.net"


def _strip_html(fragment: str) -> str:
    # Normaliza quebras
    s = fragment
    s = re.sub(r"<\s*br\s*/?\s*>", "\n", s, flags=re.I)
    s = re.sub(r"<\s*/\s*p\s*>", "\n\n", s, flags=re.I)
    s = re.sub(r"<\s*/\s*div\s*>", "\n\n", s, flags=re.I)
    # Remove tags remanescentes
    s = re.sub(r"<[^>]+>", "", s)
    s = ihtml.unescape(s)
    # Espaçamento
    s = re.sub(r"\r\n?", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = "\n".join(line.strip() for line in s.split("\n"))
    s = re.sub(r"[ \t]{2,}", " ", s)
    return s.strip()


def _first_group(pattern: str, text: str, flags: int = 0) -> str | None:
    m = re.search(pattern, text, flags)
    return m.group(1) if m else None


def _trim_footer_noise(text: str) -> str:
    """Remove trechos de rodapé/CTA típicos do evangeli.net no texto já limpo."""
    if not text:
        return text

    # Corta a partir de marcadores comuns do rodapé/CTA.
    markers = [
        "Fechar",
        "Receba-o grátis todos os dias",
        "Subscreva-se",
        "Você sabe como é financiada evangeli.net?",
        "Quer colocar evangeli.net na sua web ?",
    ]

    cut_at = None
    for m in markers:
        idx = text.find(m)
        if idx != -1:
            cut_at = idx if cut_at is None else min(cut_at, idx)

    if cut_at is not None:
        text = text[:cut_at].rstrip()

    # Normaliza excesso de linhas em branco no final
    text = re.sub(r"\n{3,}", "\n\n", text).rstrip()
    return text


def fetch(date_iso: str) -> dict:
    url = f"{BASE}/evangelho/feria/{date_iso}"
    r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    html = r.text

    # Leituras e salmo (podem variar por dia)
    first_reading_html = _first_group(r"<div\s+class=\"first_reading\"[^>]*>([\s\S]*?)</div>", html)
    second_reading_html = _first_group(r"<div\s+class=\"second_reading\"[^>]*>([\s\S]*?)</div>", html)

    psalm_verscicle_html = _first_group(r"<div\s+class=\"salm_verscicle\"[^>]*>([\s\S]*?)</div>", html)
    psalm_response_html = _first_group(r"<div\s+class=\"salm_response\"[^>]*>([\s\S]*?)</div>", html)
    psalm_text_html = _first_group(r"<div\s+class=\"salm_text\"[^>]*>([\s\S]*?)</div>", html)

    verse_before_gospel_html = _first_group(r"<div\s+class=\"reading_verscicle\"[^>]*>([\s\S]*?)</div>", html)

    first_reading = _strip_html(first_reading_html) if first_reading_html else None
    second_reading = _strip_html(second_reading_html) if second_reading_html else None
    psalm_verscicle = _strip_html(psalm_verscicle_html) if psalm_verscicle_html else None
    psalm_response = _strip_html(psalm_response_html) if psalm_response_html else None
    psalm_text = _strip_html(psalm_text_html) if psalm_text_html else None
    verse_before_gospel = _strip_html(verse_before_gospel_html) if verse_before_gospel_html else None

    # Referência + texto do Evangelho
    ref_raw = _first_group(r"<div\s+class=\"evangeli_text\"[\s\S]*?<strong>([\s\S]*?)</strong>", html)
    gospel_html = _first_group(r"<span\s+id=\"gospel_norm\"[^>]*>([\s\S]*?)</span>", html)

    if not ref_raw or not gospel_html:
        raise RuntimeError("Não consegui localizar o Evangelho (ref/texto) na página. O HTML pode ter mudado.")

    ref = _strip_html(ref_raw)
    gospel = _strip_html(gospel_html)

    # Título/tema do comentário (opcional)
    theme = _first_group(r"<p\s+class=\"titol\s+first\"[^>]*>([\s\S]*?)</p>", html)
    theme = _strip_html(theme) if theme else None

    # Autor (opcional)
    author_name = _first_group(r"<span\s+class=\"autor_name\"[^>]*>([\s\S]*?)</span>", html)
    author_origin = _first_group(r"<span\s+class=\"autor_origin\"[^>]*>([\s\S]*?)</span>", html)
    author_name = _strip_html(author_name) if author_name else None
    author_origin = _strip_html(author_origin) if author_origin else None

    # Reflexão/comentário (opcional)
    commentary = None
    start = html.find('<div class="comentari_evangeli">')
    if start != -1:
        tail = html[start:]
        end = tail.find('<div id="footer"')
        if end != -1:
            commentary_html = tail[len('<div class="comentari_evangeli">') : end]
            commentary = _trim_footer_noise(_strip_html(commentary_html))

    return {
        "url": url,
        "first_reading": first_reading,
        "second_reading": second_reading,
        "psalm_verscicle": psalm_verscicle,
        "psalm_response": psalm_response,
        "psalm_text": psalm_text,
        "verse_before_gospel": verse_before_gospel,
        "ref": ref,
        "gospel": gospel,
        "theme": theme,
        "author_name": author_name,
        "author_origin": author_origin,
        "commentary": commentary,
    }


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("date", nargs="?", help="Data no formato YYYY-MM-DD (default: hoje)")
    p.add_argument("--somente-evangelho", action="store_true", help="Não incluir leituras/salmo")
    p.add_argument("--sem-reflexao", action="store_true", help="Não incluir reflexão/comentário")
    args = p.parse_args(argv)

    date_iso = args.date
    if not date_iso:
        date_iso = dt.datetime.now(TZ).date().isoformat()

    data = fetch(date_iso)

    print(f"# Liturgia do dia — {date_iso}\n")
    print(f"Fonte: {data['url']}\n")

    if not args.somente_evangelho:
        if data.get("first_reading"):
            print(f"## {data['first_reading']}\n")
        if data.get("second_reading"):
            print(f"## {data['second_reading']}\n")
        if data.get("psalm_verscicle") or data.get("psalm_response") or data.get("psalm_text"):
            print("## Salmo Responsorial\n")
            if data.get("psalm_verscicle"):
                print(f"{data['psalm_verscicle']}\n")
            if data.get("psalm_response"):
                print(f"{data['psalm_response']}\n")
            if data.get("psalm_text"):
                print(f"{data['psalm_text']}\n")
        if data.get("verse_before_gospel"):
            print(f"## {data['verse_before_gospel']}\n")

    print(f"## {data['ref']}\n")
    print(data["gospel"], end="\n")

    if (not args.sem_reflexao) and data.get("commentary"):
        print("\n---\n")
        if data.get("theme"):
            print(f"## {data['theme']}\n")
        if data.get("author_name"):
            origin = f" {data['author_origin']}" if data.get("author_origin") else ""
            print(f"*{data['author_name']}{origin}*\n")
        print(data["commentary"], end="\n")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        raise SystemExit(130)

---
name: youtube-transcript
description: Fetch and summarize YouTube video transcripts. Use when asked to summarize, transcribe, or extract content from YouTube videos. Handles transcript fetching via residential IP proxy to bypass YouTube's cloud IP blocks.
version: 1.0.0
author: ramirlm
triggers:
  - "transcrição youtube"
  - "youtube transcript"
  - "resumir vídeo"
  - "extrair legenda"
metadata:
  clawdbot:
    emoji: "🎬"
    os: ["linux", "darwin", "windows"]
    requires:
      bins: ["python3"]
---

# YouTube Transcript

Fetch transcripts from YouTube videos and optionally summarize them.

## Quick Start

```bash
python3 scripts/fetch_transcript.py <video_id_or_url> [languages]
```

**Examples:**
```bash
python3 scripts/fetch_transcript.py dQw4w9WgXcQ
python3 scripts/fetch_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
python3 scripts/fetch_transcript.py dQw4w9WgXcQ "fr,en,de"
```

**Output:** JSON with `video_id`, `title`, `author`, `full_text`, and timestamped `transcript` array.

## Workflow

1. Run `fetch_transcript.py` with video ID or URL
2. Script checks VPN, brings it up if needed
3. Returns JSON with full transcript text
4. Summarize the `full_text` field as needed

## Language Codes

Default priority: `en, fr, de, es, it, pt, nl`

Override with second argument: `python3 scripts/fetch_transcript.py VIDEO_ID "ja,ko,zh"`

## Setup & Configuration

See [references/SETUP.md](references/SETUP.md) for:
- Python dependencies installation
- WireGuard VPN configuration (required for cloud VPS)
- Troubleshooting common errors
- Alternative proxy options

## Tratamento de Erros

- **Vídeo sem legenda disponível**: Informar ao usuário e oferecer alternativas (ex.: buscar transcrição manual, usar áudio)
- **URL inválida**: Validar o formato da URL do YouTube antes de fazer a requisição
- **IP bloqueado pelo YouTube**: Verificar se o proxy residencial está configurado e ativo; orientar a verificar `VPN_HOST` ou `PROXY_URL`
- **Transcrição muito longa** (> 100k tokens): Informar o tamanho e oferecer resumo por seções ao invés de transcrição completa
- **Legenda em idioma diferente do esperado**: Informar o idioma detectado e perguntar se deve prosseguir com tradução ou buscar outra legenda

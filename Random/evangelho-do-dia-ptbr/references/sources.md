# Fonte: evangeli.net (PT)

- Página base: https://evangeli.net/evangelho
- URL por data (feria): `https://evangeli.net/evangelho/feria/YYYY-MM-DD`

## Seletores/âncoras (observado em 2026-02-17)

- 1ª Leitura: `<div class="first_reading"> ... </div>`
- 2ª Leitura (quando existir): `<div class="second_reading"> ... </div>`
- Salmo Responsorial:
  - `<div class="salm_verscicle"> ... </div>`
  - `<div class="salm_response"> ... </div>`
  - `<div class="salm_text"> ... </div>`
- Versículo antes do Evangelho: `<div class="reading_verscicle"> ... </div>`
- Evangelho (referência): dentro de `<div class="evangeli_text">` em um `<strong>...</strong>`
- Texto do evangelho: `<span id="gospel_norm"> ... </span>`
- Reflexão/comentário: `<div class="comentari_evangeli"> ...` (vai até antes do `<div id="footer">`)

Se o HTML mudar, ajustar o parser em `scripts/fetch_evangelho.py`.

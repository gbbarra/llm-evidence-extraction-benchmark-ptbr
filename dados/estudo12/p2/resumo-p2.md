# Estudo 12 — Fases 2 e 3, o resumo

Gerado em 2026-09-11 02:58 sobre dados\estudo12\saidas. Nenhum modelo chamado. Cada célula divergente está em `adjudicacao-pendente.md`.

## Camada 2 (as constantes de referência, reproduzidas aqui)

- âncora 1, DL sobre as células-fonte da chave: morbidade {"rr": 0.787, "ic95": [0.58, 1.068], "tau2": 0.0662, "i2": 74.0} · mortalidade {"rr": 1.023, "ic95": [0.446, 2.346], "tau2": 0.0, "i2": 0.0} (publicado 0,778 / 1,021)
- âncora 2, DL sobre os sextetos da chave: {"md": -0.24, "ic95": [-0.32, -0.16], "tau2": 0.0008, "i2_pct": 5.7} (registrado −0,24 [−0,32; −0,16])
- âncora 3, DL {"or": 0.484, "ic95": [0.319, 0.735], "tau2": 0.0, "i2": 0.0} · PM+HK {"or": 0.484, "ic95": [0.342, 0.685], "tau2": 0.0, "k": 8, "gl": 7, "t": 2.364624} (registrados 0,484 [0,319; 0,735] e 0,484 [0,342; 0,685])

## Âncora 1 — células contra a camada 2 (124)

| modelo | ficha | células | estabilidade r1·r2 | ilegíveis | recitação | pool |
|---|---|---|---|---|---|---|
| gemma12 | v1 | 108/124 (87.1%) | 121/124 (97.6%) | 0 | 1 | morb RR 0.779 · mort RR 1.019 |
| gemma12 | v2 | 106/124 (85.5%) | 89/98 (90.8%) | 0 | 2 | morb RR 0.779 · mort RR 1.078 |
| qwen14 | v1 | 104/124 (83.9%) | 120/124 (96.8%) | 0 | 1 | morb RR 0.779 · mort RR 1.021 |
| qwen14 | v2 | 85/124 (68.5%) | 118/120 (98.3%) | 0 | 1 | morb RR 0.779 · mort RR 1.019 |
| llama8 | v1 | 91/124 (73.4%) | 98/124 (79.0%) | 0 | 1 | morb RR 0.738 · mort RR 1.023 |
| llama8 | v2 | 85/124 (68.5%) | 82/108 (75.9%) | 0 | 3 | morb RR 0.767 · mort RR 1.023 |
| qwen35 | v1 | 94/124 (75.8%) | 94/115 (81.7%) | 0 | 1 | morb RR 0.779 · mort RR 1.021 |
| qwen35 | v2 | 90/124 (72.6%) | 93/109 (85.3%) | 0 | 1 | morb RR 0.779 · mort RR 1.019 |
| deepseek14 | v1 | 108/124 (87.1%) | 100/111 (90.1%) | 0 | 1 | morb RR 0.788 · mort RR 0.98 |
| deepseek14 | v2 | 101/124 (81.5%) | 96/118 (81.4%) | 0 | 0 | morb RR 0.769 · mort RR 1.021 |
| qwen27q2 | v1 | 110/124 (88.7%) | 112/124 (90.3%) | 0 | 1 | morb RR 0.787 · mort RR 0.4 |
| qwen27q2 | v2 | 109/124 (87.9%) | 114/124 (91.9%) | 0 | 0 | morb RR 0.779 · mort RR 1.023 |

## Âncora 2 — células contra a camada 2 (49)

| modelo | ficha | células | estabilidade r1·r2 | ilegíveis | recitação | pool |
|---|---|---|---|---|---|---|
| gemma12 | v1 | 33/49 (67.3%) | 41/49 (83.7%) | 0 | — | lente MD -0.27 [-0.38, -0.17] · 7/7 |
| gemma12 | v2 | 31/49 (63.3%) | 41/49 (83.7%) | 0 | — | lente MD -0.21 [-0.23, -0.19] · 4/7 |
| qwen14 | v1 | 22/49 (44.9%) | 46/49 (93.9%) | 0 | — | lente MD -0.42 [-0.91, 0.06] · 7/7 |
| qwen14 | v2 | 20/49 (40.8%) | 37/49 (75.5%) | 0 | — | lente MD -0.22 [-0.59, 0.15] · 3/7 |
| llama8 | v1 | 23/49 (46.9%) | 34/49 (69.4%) | 0 | — | lente MD -0.63 [-1.03, -0.24] · 5/7 |
| llama8 | v2 | 15/42 (35.7%) | 12/14 (85.7%) | 1 | — | lente MD -0.58 [-0.85, -0.31] · 5/7 |
| qwen35 | v1 | 28/49 (57.1%) | 35/49 (71.4%) | 0 | — | lente MD -0.63 [-1.07, -0.19] · 5/7 |
| qwen35 | v2 | 23/49 (46.9%) | 25/42 (59.5%) | 0 | — | lente MD -0.88 [-2.14, 0.39] · 3/7 |
| deepseek14 | v1 | 24/49 (49.0%) | 35/49 (71.4%) | 0 | — | lente MD -0.46 [-0.66, -0.25] · 5/7 |
| deepseek14 | v2 | 23/49 (46.9%) | 30/49 (61.2%) | 0 | — | lente MD -0.52 [-0.83, -0.21] · 2/7 |
| qwen27q2 | v1 | 35/49 (71.4%) | 49/49 (100.0%) | 0 | — | lente MD -0.25 [-0.37, -0.12] · 7/7 |
| qwen27q2 | v2 | 31/49 (63.3%) | 40/49 (81.6%) | 0 | — | lente MD -0.2 [-0.34, -0.05] · 4/7 |

## Âncora 3 — células contra a camada 2 (32)

| modelo | ficha | células | estabilidade r1·r2 | ilegíveis | recitação | pool |
|---|---|---|---|---|---|---|
| gemma12 | v1 | 23/32 (71.9%) | 32/32 (100.0%) | 0 | 0 | DL OR 0.519 [0.321, 0.839] · PM+HK 0.52 |
| gemma12 | v2 | 23/32 (71.9%) | 27/32 (84.4%) | 0 | 0 | DL OR 0.418 [0.246, 0.711] · PM+HK 0.418 |
| qwen14 | v1 | 32/32 (100.0%) | 32/32 (100.0%) | 0 | 0 | DL OR 0.484 [0.319, 0.735] · PM+HK 0.484 |
| qwen14 | v2 | 24/28 (85.7%) | 28/32 (87.5%) | 1 | 0 | DL OR 0.481 [0.311, 0.745] · PM+HK 0.481 |
| llama8 | v1 | 26/32 (81.2%) | 24/32 (75.0%) | 0 | 0 | DL OR 0.496 [0.318, 0.773] · PM+HK 0.496 |
| llama8 | v2 | 23/32 (71.9%) | 20/32 (62.5%) | 0 | 0 | DL OR 0.517 [0.322, 0.832] · PM+HK 0.517 |
| qwen35 | v1 | 28/32 (87.5%) | 24/32 (75.0%) | 0 | 0 | DL OR 0.46 [0.299, 0.708] · PM+HK 0.46 |
| qwen35 | v2 | 16/28 (57.1%) | 20/32 (62.5%) | 1 | 0 | DL OR 0.45 [0.267, 0.758] · PM+HK 0.45 |
| deepseek14 | v1 | 32/32 (100.0%) | 28/32 (87.5%) | 0 | 0 | DL OR 0.484 [0.319, 0.735] · PM+HK 0.484 |
| deepseek14 | v2 | 22/24 (91.7%) | 29/32 (90.6%) | 2 | 0 | DL OR 0.548 [0.362, 0.831] · PM+HK 0.548 |
| qwen27q2 | v1 | 28/32 (87.5%) | 32/32 (100.0%) | 0 | 0 | DL OR 0.493 [0.315, 0.77] · PM+HK 0.493 |
| qwen27q2 | v2 | 28/32 (87.5%) | 32/32 (100.0%) | 0 | 0 | DL OR 0.493 [0.315, 0.77] · PM+HK 0.493 |

### Âncora 3 — leitura tolerante (sensibilidade declarada; não substitui a primária)

O leitor de JSON congelado é estrito e recusa caractere de controle dentro de string. Os textos convertidos de PDF carregam U+0001–U+0008 onde o PDF tinha símbolos (kirov2001: 127, levin2004: 18); a ficha v2, que cita ao pé da letra, os carrega para a citação. A leitura tolerante usa `strict=False` e a primeira réplica que abre. Onde a ficha é JSON malformado de verdade, ela também falha, e isso fica dito.

- qwen14/v2: primária 24/28 com 1 ficha(s) recusada(s) pelo leitor estrito (levin2004); tolerante recupera 1 → **28/32**, DL 0.46 [0.299, 0.708]
- qwen35/v2: primária 16/28 com 1 ficha(s) recusada(s) pelo leitor estrito (luissilva2024); tolerante recupera 1 → **20/32**, DL 0.467 [0.289, 0.756]
- deepseek14/v2: primária 22/24 com 2 ficha(s) recusada(s) pelo leitor estrito (kirov2001, levin2004); tolerante recupera 2 → **30/32**, DL 0.52 [0.348, 0.777]

## Hipóteses pré-registradas

### H12.1 — o portão de generalização

Falha na leitura primária em: qwen14/v2, qwen35/v2, deepseek14/v2 — em todos os casos por ficha v2 recusada pelo leitor estrito (ver a sensibilidade acima); o DL é coerente com as próprias células em todos os 12.

### H12.2 — a que decide

- ficha v1: Aguilar **6/30** em 4 de 6 (qwen14, llama8, qwen35, deepseek14); 24/30 (a errata) em 0 (—); Shaker **15/60** em 6 (gemma12, qwen14, llama8, qwen35, deepseek14, qwen27q2); 15/30 (a errata) em 0 (—); **ambas** em 4 (qwen14, llama8, qwen35, deepseek14)
- ficha v2: Aguilar **6/30** em 3 de 6 (qwen14, llama8, deepseek14); 24/30 (a errata) em 0 (—); Shaker **15/60** em 5 (gemma12, qwen14, qwen35, deepseek14, qwen27q2); 15/30 (a errata) em 0 (—); **ambas** em 2 (qwen14, deepseek14)

### H12.3 — a ficha v2, na escala do elenco

- delta médio v2−v1 nas 124 células da âncora 1: **-6.5** (critério ≥ −4 → falha); por modelo: gemma12 -2, qwen14 -19, llama8 -6, qwen35 -4, deepseek14 -7, qwen27q2 -1
- v2 mais perto da camada 2 em ≥4 de 6 modelos: 0 de 3 âncoras (critério ≥ 2 → falha)

  - a1: gemma12 v1 0.779 · v2 0.779, qwen14 v1 0.779 · v2 0.779, llama8 v1 0.738 · v2 0.767 ✓, qwen35 v1 0.779 · v2 0.779, deepseek14 v1 0.788 · v2 0.769, qwen27q2 v1 0.787 · v2 0.779 · alvo 0.787
  - a2: gemma12 v1 -0.27 · v2 -0.21, qwen14 v1 -0.42 · v2 -0.22 ✓, llama8 v1 -0.63 · v2 -0.58 ✓, qwen35 v1 -0.63 · v2 -0.88, deepseek14 v1 -0.46 · v2 -0.52, qwen27q2 v1 -0.25 · v2 -0.2 · alvo -0.24
  - a3: gemma12 v1 0.519 · v2 0.418, qwen14 v1 0.484 · v2 0.481, llama8 v1 0.496 · v2 0.517, qwen35 v1 0.46 · v2 0.45, deepseek14 v1 0.484 · v2 0.548, qwen27q2 v1 0.493 · v2 0.493 · alvo 0.484

### H12.5 — o controle de contexto

- gemma12 âncora 1 v1: **108/124** (faixa [99, 107]) → FORA
- gemma12 âncora 2 v1, lente: **-0.27** (faixa [-0.32, -0.22]) → dentro
- **FALHA: o contexto é confundidor e vai reportado antes de qualquer resultado da âncora 3**

### H12.6 — o nulo honesto

Algum modelo passa de 50% das 32 células: gemma12/v1, gemma12/v2, qwen14/v1, qwen14/v2, llama8/v1, llama8/v2, qwen35/v1, deepseek14/v1, deepseek14/v2, qwen27q2/v1, qwen27q2/v2

## H12.4 — redes de proveniência sobre a ficha v2 (exploratório; avisam, não substituem)

| âncora | modelo | células inspecionadas | elegíveis | N9-1 | N9-2 | N9-3 | ilegíveis |
|---|---|---|---|---|---|---|---|
| a1 | gemma12 | 450 | 178 | 255 (96) | 20 (12) | 0 | 2 |
| a1 | qwen14 | 352 | 144 | 76 (29) | 17 (10) | 0 | 1 |
| a1 | llama8 | 526 | 192 | 197 (68) | 216 (82) | 0 | 2 |
| a1 | qwen35 | 399 | 183 | 203 (104) | 42 (27) | 0 | 2 |
| a1 | deepseek14 | 533 | 211 | 275 (117) | 98 (61) | 0 | 1 |
| a1 | qwen27q2 | 483 | 217 | 41 (22) | 35 (32) | 0 | 0 |
| a2 | gemma12 | 232 | 194 | 64 (56) | 35 (25) | 0 | 0 |
| a2 | qwen14 | 219 | 181 | 54 (46) | 58 (36) | 0 | 0 |
| a2 | llama8 | 133 | 110 | 40 (30) | 64 (49) | 2 | 6 |
| a2 | qwen35 | 207 | 170 | 85 (74) | 42 (25) | 0 | 1 |
| a2 | deepseek14 | 205 | 171 | 107 (92) | 61 (48) | 3 | 0 |
| a2 | qwen27q2 | 210 | 172 | 28 (22) | 45 (33) | 0 | 0 |
| a3 | gemma12 | 384 | 78 | 222 (20) | 43 (19) | 0 | 0 |
| a3 | qwen14 | 294 | 56 | 164 (12) | 58 (24) | 0 | 3 |
| a3 | llama8 | 380 | 87 | 231 (26) | 65 (30) | 0 | 1 |
| a3 | qwen35 | 371 | 74 | 229 (29) | 27 (8) | 0 | 1 |
| a3 | deepseek14 | 298 | 68 | 164 (16) | 47 (20) | 0 | 4 |
| a3 | qwen27q2 | 360 | 72 | 173 (14) | 20 (5) | 0 | 0 |

Entre parênteses: bandeiras nas células que entram no denominador da H12.4.

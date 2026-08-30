# Estudo 4 · rodada 2 — fichas de leitura lado a lado

O que cada modelo escreveu em cada campo com gabarito (réplica que alimenta o pool), o que o gabarito aceita (valores do MUNDO PERTURBADO — os textos lidos têm números deliberadamente trocados), e o veredito mecânico da célula.

Vereditos: ✓ exata · ≈ derivável · ✓NR não-relatado correto · — omitiu · ✗ errada · ? aguardando adjudicação na fonte (rito) · ‼ recitou o valor original · · = campo vazio. Fichas brutas (JSON) em `saidas/<modelo>/extracao/`.

## Saslow 2017 (PMC5329646)

| campo | gabarito aceita | gemma12 (r1) | qwen14 (r1) | llama8 (r1) | qwen35 (r1) | deepseek14 (r1) |
|---|---|---|---|---|---|---|
| experimental.n_randomizado | 12 | ✓ 12 | ✓ 12 | ✓ 12 | ✓ 12 | ✓ 12 |
| controle.n_randomizado | 13 | ✓ 13 | ✓ 13 | ✓ 13 | ✓ 13 | ✓ 13 |
| experimental.n_analisado | NR ou 12 ou 11 | ✓ 11 | ✓ 11 | ✓ 11 | ✓NR NR | ✓ 12 |
| controle.n_analisado | NR ou 13 ou 7 ou 8 | ✓ 8 | ✓ 8 | ✓ 8 | ✓NR NR | ✓ 13 |
| experimental.mudanca_media | -0.8 | ✓ -0.8 | ✓ -0.8 | ✓ -0.8% | ✓ -0.8 | ✓ -0.8 |
| controle.mudanca_media | -0.3 | ✓ -0.3 | ✓ -0.3 | ✓ -0.3% | ✓ -0.3 | ✓ -0.3 |
| experimental.mudanca_tipo_dispersao | IC95: -1.1 a -0.6 ou … | ✓ IC95: -1.1 a -0… | ✓ IC95: -1.1 a 0.6 | ✓ IC95: -1.1% a -… | ✓ IC95: -1.1 a -0… | ✓ IC95 |
| controle.mudanca_tipo_dispersao | IC95: -0.6 a 0.0 ou I… | ✓ IC95: -0.6 a 0.0 | ✓ IC95: -0.6 a 0.0 | ✓ IC95: -0.6% a 0% | ✓ IC95: -0.6 a 0.0 | ✓ IC95 |
| experimental.basal_media | 5.8 | ✓ 5.8 | — NR | ✓ 5.8% | — NR | — NR |
| controle.basal_media | 7.6 | ✓ 7.6 | — NR | ✓ 7.6% | — NR | — NR |
| experimental.basal_dp | 0.4 | ✓ 0.4 | — NR | — NR | — NR | — NR |
| controle.basal_dp | 0.3 | ✓ 0.3 | — NR | — NR | — NR | — NR |
| experimental.final_media | NR | ✓NR NR | ✓NR NR | ? 5.0% | ✓NR NR | ✓NR NR |
| controle.final_media | NR | ✓NR NR | ✓NR NR | ? 7.3% | ✓NR NR | ✓NR NR |
| n_randomizado_total | 25 ou NR | ✓ 25 | ✓ 25 | ✓ 25 | ✓ 25 | ✓ 25 |

## Saslow 2023 (REF9)

| campo | gabarito aceita | gemma12 (r1) | qwen14 (r1) | llama8 (r1) | qwen35 (r1) | deepseek14 (r1) |
|---|---|---|---|---|---|---|
| experimental.n_randomizado | NR ou 45 | ? 23 | ? 23 | ? 25 | ? 41.5 | ✓NR NR |
| controle.n_randomizado | NR ou 49 | ? 25 | ? 23 | ? 25 | ? 41.5 | ✓NR NR |
| experimental.n_analisado | NR ou 45 ou 39 | ? 23 | ? 22 | ✓NR NR | ✓ 39 | ✓NR NR |
| controle.n_analisado | NR ou 49 ou 42 | ? 25 | ? 22 | ✓NR NR | ✓ 42 | ✓NR NR |
| experimental.mudanca_media | -0.32 | ✓ -0.32 | ✓ -0.32 | ✓ -0.32% | ✓ -0.32 | ✓ -0.32% |
| controle.mudanca_media | -0.14 | ✓ -0.14 | ✓ -0.14 | ✓ -0.14% | ✓ -0.14 | ✓ -0.14% |
| experimental.mudanca_dispersao | 0.07 | ✓ 0.07 | ✓ 0.07 | — NR | ✓ 0.07 | ✓ 0.07 |
| controle.mudanca_dispersao | 0.07 | ✓ 0.07 | ✓ 0.07 | — NR | ✓ 0.07 | ✓ 0.07 |
| experimental.mudanca_tipo_dispersao | EP ou SE | ✓ EP | ? DP | — NR | ? DP | ? DP |
| controle.mudanca_tipo_dispersao | EP ou SE | ✓ EP | ? DP | — NR | ? DP | ? DP |
| experimental.basal_media | 6.09 ou NR | ✓ 6.09 | ✓ 6.09 | ✓ 6.09% | ✓ 6.09 | ✓ 6.09% |
| controle.basal_media | 6.1 ou 6.1 ou NR | ✓ 6.10 | ✓ 6.10 | ✓ 6.10% | ✓ 6.10 | ✓ 6.10% |
| n_randomizado_total | 83 | ✓ 83 | ✓ 83 | ✓ 83 | ✓ 83 | ✓ 83 |

## Dorans 2022 (PMC9606840)

| campo | gabarito aceita | gemma12 (r1) | qwen14 (r1) | llama8 (r1) | qwen35 (r1) | deepseek14 (r1) |
|---|---|---|---|---|---|---|
| experimental.n_randomizado | 75 | ✓ 75 | ✓ 75 | ✓ 75 | ✓ 75 | ✓ 75 |
| controle.n_randomizado | 75 | ✓ 75 | ✓ 75 | ✓ 75 | ✓ 75 | ✓ 75 |
| experimental.n_analisado | NR ou 75 ou 73 | ✓ 73 | ✓ 73 | ✓ 73 | ✓ 75 | ✓ 75 |
| controle.n_analisado | NR ou 75 ou 69 | ✓ 69 | ✓ 69 | ✓ 69 | ✓ 75 | ✓ 75 |
| experimental.mudanca_media | -0.24 | ✓ -0.24 | ✓ -0.24 | ✓ -0.24 | ✓ -0.24 | ? -0.23 |
| controle.mudanca_media | -0.04 | ✓ -0.04 | ✓ -0.04 | ✓ -0.04 | ✓ -0.04 | ✓ -0.04 |
| experimental.mudanca_tipo_dispersao | IC95: -0.33 a -0.19 o… | ✓ IC95 | ✓ IC95: -0.33 a -… | — NR | ✓ IC95: <-0.33> a… | ✓ IC95 |
| controle.mudanca_tipo_dispersao | IC95: -0.10 a 0.02 ou… | ✓ IC95 | ✓ IC95: -0.10 a 0… | — NR | ✓ IC95: <-0.10> a… | ✓ IC95 |
| experimental.mudanca_dispersao | -0.33 to -0.19 ou IC9… | ✓ -0.33 to -0.19 | ? 0.07 | ✓NR NR | ? 95% CI, –0.33 t… | ? 0.05 |
| controle.mudanca_dispersao | -0.10 to 0.02 ou IC95… | ✓ -0.10 to 0.02 | ? 0.04 | ✓NR NR | ? 95% CI, –0.10 t… | ? 0.06 |
| experimental.basal_media | 6.17 ou NR | ✓ 6.17 | ✓ 6.17 | ✓ 6.17 | ✓ 6.17 | ✓ 6.17 |
| controle.basal_media | 6.14 ou NR | ✓ 6.14 | ✓ 6.14 | ✓ 6.14 | ✓ 6.14 | ✓ 6.14 |
| experimental.basal_dp | 0.31 ou NR | ✓ 0.31 | ✓ 0.31 | ✓ 0.31 | ✓ 0.31 | ✓ 0.31 |
| controle.basal_dp | 0.3 ou 0.3 ou NR | ✓ 0.30 | ✓ 0.30 | ✓ 0.30 | ✓ 0.30 | ✓ 0.30 |
| n_randomizado_total | 141 | ✓ 141 | ✓ 141 | ✓ 141 | ✓ 141 | ✓ 141 |

## Chen 2020 (PMC7535044)

| campo | gabarito aceita | gemma12 (r1) | qwen14 (r1) | llama8 (r1) | qwen35 (r1) | deepseek14 (r1) |
|---|---|---|---|---|---|---|
| experimental.n_randomizado | NR ou 46 | ? 41 | ? 41 | ? 41 | ? 41 | ? 41 |
| controle.n_randomizado | NR ou 46 | ? 42 | ? 42 | ? 42 | ? 42 | ? 42 |
| experimental.n_analisado | 41 | ✓ 41 | ✓ 41 | ✓ 41 | — NR | ? 40 |
| controle.n_analisado | 42 | ✓ 42 | ✓ 42 | ✓ 42 | — NR | ? 41 |
| experimental.mudanca_media | -1.44 | ✓ -1.44 | ✓ -1.44 | ✓ -1.44 | ✓ -1.44 | ✓ -1.44 |
| controle.mudanca_media | -1.01 | ✓ -1.01 | ✓ -1.01 | ✓ -1.01 | ✓ -1.01 | ✓ -1.01 |
| experimental.mudanca_tipo_dispersao | IC95: -1.96 a -1.30 o… | ? DP | ? DP | ✓ IC95: -1.96 a -… | ✓ IC95: -1.96 a -… | ? DP |
| controle.mudanca_tipo_dispersao | IC95: -1.40 a -0.63 o… | ? DP | ? DP | ✓ IC95: -1.40 a -… | ✓ IC95: -1.40 a -… | ? DP |
| experimental.basal_media | 9.95 | ✓ 9.95 | ✓ 9.95 | ✓ 9.95 | ✓ 9.95 | ✓ 9.95 |
| controle.basal_media | 8.7 ou 8.7 | ✓ 8.70 | ✓ 8.70 | ✓ 8.70 | ✓ 8.70 | ✓ 8.70 |
| experimental.basal_dp | 1.04 | ✓ 1.04 | ✓ 1.04 | ✓ 1.04 | — | ✓ 1.04 |
| controle.basal_dp | 1.01 | ✓ 1.01 | ✓ 1.01 | ✓ 1.01 | — | ✓ 1.01 |
| experimental.final_media | 6.84 | ✓ 6.84 | ✓ 6.84 | ✓ 6.84 | ✓ 6.84 | ✓ 6.84 |
| controle.final_media | 7.69 | ✓ 7.69 | ✓ 7.69 | ✓ 7.69 | ✓ 7.69 | ✓ 7.69 |
| experimental.final_dp | 0.59 | ✓ 0.59 | ✓ 0.59 | ✓ 0.59 | — | ✓ 0.59 |
| controle.final_dp | 1.06 | ✓ 1.06 | ✓ 1.06 | ✓ 1.06 | — | ✓ 1.06 |
| n_randomizado_total | 92 | ✓ 92 | ✓ 92 | ✓ 92 | ✓ 92 | ✓ 92 |

## Thomsen 2022 (REF12)

| campo | gabarito aceita | gemma12 (r1) | qwen14 (r1) | llama8 (r1) | qwen35 (r1) | deepseek14 (r1) |
|---|---|---|---|---|---|---|
| experimental.n_randomizado | NR ou 34 ou 36 | ✓ 36 | ✓ 36 | ✓ 36 | ✓ 36 | ✓ 36 |
| controle.n_randomizado | NR ou 33 ou 36 | ✓ 36 | ✓ 36 | ✓ 36 | ✓ 36 | ✓ 36 |
| experimental.n_analisado | 34 | ✓ 34 | ✓ 34 | ✓ 34 | ✓ 34 | ✓ 34 |
| controle.n_analisado | 33 | ✓ 33 | ✓ 33 | ✓ 33 | ✓ 33 | ✓ 33 |
| experimental.mudanca_media | -0.83 | ✓ -0.83 | ? -9.1 | ? -9.1 | ? -0.18 | ? -9.1 mmol/mol |
| controle.mudanca_media | -0.56 | ✓ -0.56 | ? -7.2 | ? -7.2 | ✓ -0.56 | ? -7.2 mmol/mol |
| experimental.mudanca_dispersao | 0.38 | ✓ 0.38 | ? 4.2 | ? 4.2 | ? -0.32 | ? ±4.2 |
| controle.mudanca_dispersao | 0.37 | ✓ 0.37 | ? 4.0 | ? 4.0 | — NR | ? ±4.0 |
| experimental.mudanca_tipo_dispersao | DP ou SD | ✓ DP | ✓ DP | ✓ DP | ? IC95: <-0.32> a… | ✓ DP |
| controle.mudanca_tipo_dispersao | DP ou SD | ✓ DP | ✓ DP | ✓ DP | — NR | ✓ DP |
| experimental.basal_media | 8.09 | ✓ 8.09 | ? 57.6 | ? 57.6 | ✓ 8.09 | — NR |
| controle.basal_media | 7.4 ou 7.4 | ✓ 7.40 | ? 57.4 | ? 57.4 | ✓ 7.40 | — NR |
| experimental.basal_dp | 0.77 | ✓ 0.77 | ? 8.4 | — NR | ✓ 0.77 | — NR |
| controle.basal_dp | 0.7 ou 0.7 | ✓ 0.70 | ? 7.7 | — NR | ✓ 0.70 | — NR |
| n_randomizado_total | 63 ou 72 | ✓ 72 | ✓ 72 | ✓ 72 | ✓ 72 | ✓ 72 |

## Wang 2018 (PMC6024764)

| campo | gabarito aceita | gemma12 (r1) | qwen14 (r1) | llama8 (r1) | qwen35 (r1) | deepseek14 (r1) |
|---|---|---|---|---|---|---|
| experimental.n_randomizado | 28 | ✓ 28 | ✓ 28 | ✓ 28 | ✓ 28 | ✓ 28 |
| controle.n_randomizado | 28 | ✓ 28 | ✓ 28 | ✓ 28 | ✓ 28 | ✓ 28 |
| experimental.n_analisado | NR ou 24 ou 28 | ✓ 24 | ✓ 24 | ✓ 24 | ✓ 24 | ✓ 24 |
| controle.n_analisado | NR ou 25 ou 28 | ✓ 25 | ✓ 25 | ✓ 25 | ✓ 25 | ✓ 25 |
| experimental.mudanca_media | 0.48 ou -0.48 ou -0.6… | ✓ -0.63 | ✓ -0.63 | ✓ −0.63% | ✓ -0.63 | ✓ -0.63% |
| controle.mudanca_media | 0.28 ou -0.28 ou -0.3… | ✓ -0.31 | ✓ -0.31 | ✓ −0.31% | ✓ -0.31 | ✓ -0.31% |
| experimental.mudanca_dispersao | 0.94 ou 1.18 | ✓ 1.18 | ✓ 1.18 | ✓ 1.18% | ✓ 1.18 | ✓ 1.18 |
| controle.mudanca_dispersao | 0.67 ou 0.7 | ✓ 0.70 | ✓ 0.70 | ✓ 0.70% | ✓ 0.70 | ✓ 0.70 |
| experimental.mudanca_tipo_dispersao | DP ou SD | ✓ DP | ✓ DP | ✓ DP | ✓ DP | ✓ DP |
| controle.mudanca_tipo_dispersao | DP ou SD | ✓ DP | ✓ DP | ✓ DP | ✓ DP | ✓ DP |
| n_randomizado_total | 49 ou 56 | ✓ 56 | ✓ 56 | ✓ 56 | ✓ 56 | ✓ 56 |

## Goday 2016 (PMC5048014)

| campo | gabarito aceita | gemma12 (r1) | qwen14 (r1) | llama8 (r1) | qwen35 (r1) | deepseek14 (r1) |
|---|---|---|---|---|---|---|
| experimental.n_randomizado | NR ou 45 | ✓ 45 | ✓ 45 | ✓ 45 | ✓ 45 | ✓ 45 |
| controle.n_randomizado | NR ou 44 ou 40 | ✓ 44 | ✓ 44 | ✓ 44 | ✓ 44 | ✓ 44 |
| experimental.n_analisado | 45 | ✓ 45 | — NR | — NR | ✓ 45 | — NR |
| controle.n_analisado | 40 | ✓ 40 | — NR | — NR | ✓ 40 | — NR |
| experimental.mudanca_media | NR | ✓NR NR | ? −1.6 | ? -0.36 | ? -1.6 | ? -1.6% |
| controle.mudanca_media | NR | ✓NR NR | ? 0.3 | ? -0.15 | ✓NR NR | ✓NR NR |
| experimental.mudanca_tipo_dispersao | NR | ✓NR NR | ? DP | ? DP | ? DP | ? DP |
| controle.mudanca_tipo_dispersao | NR | ✓NR NR | ? DP | ✓NR NR | ✓NR NR | ✓NR NR |
| experimental.basal_media | 6.9 ou 6.89 | ✓ 6.9 | ✓ 6.89 | ✓ 6.89 | ✓ 6.9 | — NR |
| controle.basal_media | 6.8 ou 6.88 | ✓ 6.8 | ✓ 6.88 | ✓ 6.88 | ✓ 6.8 | — NR |
| experimental.basal_dp | 1.1 ou 1.11 | ✓ 1.1 | ? 1.06 | ? 1.06 | ✓ 1.1 | — NR |
| controle.basal_dp | 1.0 ou 1 ou 1.03 | ✓ 1.0 | ✓ 1.03 | ✓ 1.03 | ✓ 1.0 | — NR |
| experimental.final_media | 5.3 | ✓ 5.3 | ✓ 5.3 | ? 5.53 | ✓ 5.3 | — NR |
| controle.final_media | 7.1 | ✓ 7.1 | ✓ 7.1 | ? 7.07 | ✓ 7.1 | — NR |
| experimental.final_dp | 0.7 | ✓ 0.7 | ✓ 0.7 | ✓ 0.7 | ✓ 0.7 | — NR |
| controle.final_dp | 0.8 | ✓ 0.8 | ✓ 0.8 | ✓ 0.8 | ✓ 0.8 | — NR |
| n_randomizado_total | 89 | ✓ 89 | ✓ 89 | ✓ 89 | ✓ 89 | ✓ 89 |

# Estudo 6 — a replicação em detalhe (MA-1, GDFT)

Lado a lado, por desfecho: as células do gemma12 (selo revertido), o efeito computado pelo código, o valor publicado, e a categoria congelada da comparação. Categorias que exigem fonte são adjudicadas no registro de avaliação.

## morbidade (tabela 5 da âncora)

| estudo | células (dele, revertidas) | nosso | publicado | categoria |
|---|---|---|---|---|
| Calvo-Vecino et al. (REF33) | morbidade=8.6%; morbidade=16.6% | RR 0.504 [0.3, 0.847] (a=19/224, c=38/226) [derivado-de-%] | RR 0.519 [0.304, 0.887] | verificar (rota-do-modelo ou erro-do-modelo — adjudicar na fonte) |
| Yun et al. (PMC10561433) | morbidade=28 (71.8%); morbidade=30 (83.3%) | RR 0.862 [0.674, 1.101] (a=28/39, c=30/36) | RR 0.862 [0.674, 1.101] | reproduz |
| Diaper et al. (REF26) | morbidade=113 (57.7%); morbidade=105 (53.0%) | RR 1.076 [0.9, 1.286] (a=113/198, c=105/198) | RR 1.087 [0.91, 1.299] | verificar (rota-do-modelo ou erro-do-modelo — adjudicar na fonte) |
| Wu et al. (PMC10912221) | morbidade=19 (32.8%); morbidade=32 (57.1%) | RR 0.594 [0.381, 0.925] (a=19/61, c=32/61) | RR 0.573 [0.372, 0.884] | verificar (rota-do-modelo ou erro-do-modelo — adjudicar na fonte) |
| *(linha agregada da âncora: Pooled analysis)* | — | — | RR 0.778 [0.567, 1.068] | (pool publicado) |

**Pool (nosso)**: MH {"rr": 0.864, "ic95": [0.749, 0.996]} · DL {"rr": 0.778, "ic95": [0.571, 1.062], "tau2": 0.07, "i2": 75.3} — comparação sob DL (errata-15: números DL, legenda MH). **Publicado: RR 0.778 [0.567, 1.068] → REPRODUZ sob DL**.

## mortalidade (tabela 6 da âncora)

| estudo | células (dele, revertidas) | nosso | publicado | categoria |
|---|---|---|---|---|
| de Waal et al. (REF29) | mortalidade=10 (4.0%); mortalidade=10 (4.3%) | RR 0.946 [0.401, 2.232] (a=10/258, c=10/244) | RR 0.944 [0.4, 2.226] | reproduz |
| Sun et al. (PMC10694978) | mortalidade=1 (2%); mortalidade=0 (0%) | RR 3.0 [0.125, 71.927] (a=1/50, c=0/50) | RR 3.0 [0.125, 71.927] | reproduz |
| *(linha agregada da âncora: Pooled analysis)* | — | — | RR 1.021 [0.446, 2.337] | (pool publicado) |

**Pool (nosso)**: MH {"rr": 1.041, "ic95": [0.459, 2.363]} · DL {"rr": 1.023, "ic95": [0.447, 2.344], "tau2": 0.0, "i2": 0.0} — comparação sob DL (errata-15: números DL, legenda MH). **Publicado: RR 1.021 [0.446, 2.337] → REPRODUZ sob DL**.

## ileo (tabela 11 da âncora)

| estudo | células (dele, revertidas) | nosso | publicado | categoria |
|---|---|---|---|---|
| Arslan-Carlon et al. (REF30) | ileo=25% (36/142); ileo=21% (30/141) | RR 1.192 [0.779, 1.822] (a=36/142, c=30/141) | RR 1.19 [0.77, 1.83] | reproduz |
| Sun et al. (PMC10694978) | ileo=2 of 50 patients (4%); ileo=16 of 50 patients (32%) | RR 0.125 [0.03, 0.515] (a=2/50, c=16/50) | RR 0.13 [0.03, 0.53] | verificar (rota-do-modelo ou erro-do-modelo — adjudicar na fonte) |
| Castro et al. (PMC11061212) | ileo=NR; ileo=NR | dados-insuficientes | RR 0.31 [0.14, 0.68] | insuficiente |

**Pool (nosso)**: MH {"rr": 0.821, "ic95": [0.559, 1.207]} · DL {"rr": 0.429, "ic95": [0.048, 3.87], "tau2": 2.2571, "i2": 88.8} — comparação sob DL (errata-15: números DL, legenda MH).

## tempo_flatus (tabela 8 da âncora)

| estudo | células (dele, revertidas) | nosso | publicado | categoria |
|---|---|---|---|---|
| Sun et al. (PMC10694978) | tempo=28.2 h (9.2-48.0 h); tempo=39.4 h (24.9-67.5 h) | dados-insuficientes | MD -11.0 [-16.2, -5.8] | insuficiente · difere-por-escolha-documentada-da-ancora [derivavel-conversao] · shorten time to first flatus by 11 h (P = 0.009) |
| Coeckelenbergh et al. (REF41) | tempo=NR; tempo=NR | dados-insuficientes | MD -8.0 [-15.1, -0.9] | insuficiente · fonte-indisponivel [nao-sustentada] · (a palavra 'flatus' não ocorre no texto) |
| Diaper et al. (REF26) | tempo=NR; tempo=NR | dados-insuficientes | MD -3.0 [-6.8, 0.8] | insuficiente · fonte-indisponivel [nao-sustentada] · (a palavra 'flatus' não ocorre no texto integral) |

## tempo_ingesta_oral (tabela 9 da âncora)

| estudo | células (dele, revertidas) | nosso | publicado | categoria |
|---|---|---|---|---|
| Sun et al. (PMC10694978) | tempo=4.0 days (2.7-6.0 days); tempo=6.0 days (5.0-9.3 days) | dados-insuficientes | MD -24.0 [-34.5, -13.5] | insuficiente · difere-por-errata-da-ancora [errata-ma] · GDFT significantly also shorten … time to first tolerate oral diet by 2 days (P < 0.001) |
| Sujatha et al. (PMC6907038) | tempo=comparable; tempo=comparable | dados-insuficientes | MD -5.0 [-12.1, 2.1] | insuficiente · fonte-indisponivel [dado-fora-do-insumo] · The days to ICU stay, HDU stay, return of bowel movement, days to oral intake … are given in Table 4 |

# Study 6 — the replication, in detail (MA-1, GDFT)

Side by side, per outcome: gemma12's cells (seal reversed), the effect computed by the code, the published value, and the frozen comparison category. Categories that require the source are adjudicated in the evaluation record.

Frozen category names (pre-registered in Portuguese, kept as labels): *reproduz* = reproduces · *difere-por-errata-da-ancora* = differs by a documented anchor erratum · *rota-do-modelo* = documented alternative reading route · *erro-do-modelo* = model error · *fonte-indisponivel* = source unavailable.

## morbidity (anchor table 5)

| study | model cells (reversed) | ours | published | category |
|---|---|---|---|---|
| Calvo-Vecino et al. (REF33) | morbidade=18 (8.6); morbidade=37 (16.6) | RR 0.491 [0.288, 0.836] (a=18/224, c=37/226) | RR 0.519 [0.304, 0.887] | verify (rota-do-modelo or erro-do-modelo — adjudicate in the source) |
| Yun et al. (PMC10561433) | morbidade=28/39 (71.8%); morbidade=30/36 (83.3%) | RR 0.862 [0.674, 1.101] (a=28/39, c=30/36) [derived-from-%] | RR 0.862 [0.674, 1.101] | reproduz |
| Diaper et al. (REF26) | morbidade=114; morbidade=105 | RR 1.091 [0.913, 1.305] (a=114/200, c=105/201) | RR 1.087 [0.91, 1.299] | reproduz |
| Wu et al. (PMC10912221) | morbidade=19; morbidade=32 | RR 0.573 [0.372, 0.884] (a=19/58, c=32/56) | RR 0.573 [0.372, 0.884] | reproduz |
| *(anchor's pooled row: Pooled analysis)* | — | — | RR 0.778 [0.567, 1.068] | (published pool) |

**Pool (ours)**: MH {"rr": 0.866, "ic95": [0.752, 0.999]} · DL {"rr": 0.767, "ic95": [0.552, 1.066], "tau2": 0.082, "i2": 78.1} — comparison under DL (erratum-15: DL numbers, MH caption). **Published: RR 0.778 [0.567, 1.068] → differs (decompose in the rows above)**.

## mortality (anchor table 6)

| study | model cells (reversed) | ours | published | category |
|---|---|---|---|---|
| de Waal et al. (REF29) | mortalidade=10; mortalidade=10 | RR 0.946 [0.401, 2.232] (a=10/258, c=10/244) | RR 0.944 [0.4, 2.226] | reproduz |
| Sun et al. (PMC10694978) | mortalidade=1; mortalidade=0 | RR 3.0 [0.125, 71.927] (a=1/50, c=0/50) | RR 3.0 [0.125, 71.927] | reproduz |
| *(anchor's pooled row: Pooled analysis)* | — | — | RR 1.021 [0.446, 2.337] | (published pool) |

**Pool (ours)**: MH {"rr": 1.041, "ic95": [0.459, 2.363]} · DL {"rr": 1.023, "ic95": [0.447, 2.344], "tau2": 0.0, "i2": 0.0} — comparison under DL (erratum-15: DL numbers, MH caption). **Published: RR 1.021 [0.446, 2.337] → REPRODUCES under DL**.

## ileus (anchor table 11)

| study | model cells (reversed) | ours | published | category |
|---|---|---|---|---|
| Arslan-Carlon et al. (REF30) | ileo=36/142 (22%); ileo=30/141 (21%) | RR 1.026 [0.658, 1.601] (a=31/142, c=30/141) [derived-from-%] | RR 1.19 [0.77, 1.83] | verify (rota-do-modelo or erro-do-modelo — adjudicate in the source) |
| Sun et al. (PMC10694978) | ileo=4; ileo=32 | RR 0.125 [0.048, 0.327] (a=4/50, c=32/50) | RR 0.13 [0.03, 0.53] | verify (rota-do-modelo or erro-do-modelo — adjudicate in the source) |
| Castro et al. (PMC11061212) | ileo=0; ileo=4 | RR 0.109 [0.006, 1.957] (a=0/43, c=4/42) | RR 0.31 [0.14, 0.68] | verify (rota-do-modelo or erro-do-modelo — adjudicate in the source) |

**Pool (ours)**: MH {"rr": 0.531, "ic95": [0.367, 0.768]} · DL {"rr": 0.292, "ic95": [0.049, 1.744], "tau2": 1.9368, "i2": 88.0} — comparison under DL (erratum-15: DL numbers, MH caption).

## time_to_flatus (anchor table 8)

| study | model cells (reversed) | ours | published | category |
|---|---|---|---|---|
| Sun et al. (PMC10694978) | tempo=28.2; tempo=39.4 | insufficient-data | MD -11.0 [-16.2, -5.8] | insufficient · difere-por-escolha-documentada-da-ancora [derivavel-conversao] · shorten time to first flatus by 11 h (P = 0.009) |
| Coeckelenbergh et al. (REF41) | tempo=NR; tempo=NR | insufficient-data | MD -8.0 [-15.1, -0.9] | insufficient · fonte-indisponivel [nao-sustentada] · (a palavra 'flatus' não ocorre no texto) |
| Diaper et al. (REF26) | tempo=NR; tempo=NR | insufficient-data | MD -3.0 [-6.8, 0.8] | insufficient · fonte-indisponivel [nao-sustentada] · (a palavra 'flatus' não ocorre no texto integral) |

## time_to_oral_intake (anchor table 9)

| study | model cells (reversed) | ours | published | category |
|---|---|---|---|---|
| Sun et al. (PMC10694978) | tempo=4.0; tempo=6.0 | insufficient-data | MD -24.0 [-34.5, -13.5] | insufficient · difere-por-errata-da-ancora [errata-ma] · GDFT significantly also shorten … time to first tolerate oral diet by 2 days (P < 0.001) |
| Sujatha et al. (PMC6907038) | tempo=NR; tempo=NR | insufficient-data | MD -5.0 [-12.1, 2.1] | insufficient · fonte-indisponivel [dado-fora-do-insumo] · The days to ICU stay, HDU stay, return of bowel movement, days to oral intake … are given in Table 4 |

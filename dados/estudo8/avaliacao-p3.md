# Study 8 / P3 CREATE — evaluation (deterministic engines, both anchors, five models)

**Run 2026-09-01.** Part A: engines over the P1 MA-1 sheets (sealed reversal; Study-6 comparator per model — full per-model comparison files in `p3-ma1/<model>/`). Part B: fresh MA-2 extraction (P3-b, 70/70 calls, 155.1 min, all clean stops) → validated route selector, no triggers → per-model DL pool and the **sealed unperturbation lens** vs the published −0.24 [−0.32, −0.16]. No model call anywhere downstream of the sheets.

## Part B — the five diamonds (the model-comparison headline)

| model | MA-2 lens (unperturbed) | studies in pool | verdict vs published −0.24 [−0.32, −0.16] |
|---|---|---|---|
| **gemma12** | **−0.27 [−0.38, −0.17]** (I² 28.6%) | 7/7 | **beside the published value — and identical to the hundredth to its own Portuguese round-2 lens (−0.27)** |
| deepseek14 | −0.47 [−1.22, 0.28] (I² 99.1%) | 7/7 | far; heterogeneity saturated |
| llama8 | −0.60 [−1.02, −0.18] (I² 90.5%) | 5/7 | far; two sheets starved |
| qwen14 | −0.63 [−1.08, −0.17] (I² 95.2%) | 6/7 | far |
| qwen35 | −0.80 [−1.67, 0.07] (I² 95.0%) | 6/7 | far |

The Portuguese round-2 conclusion — *only gemma4:12b reaches the published value; the others fail for reading reasons, not arithmetic* — **reproduces under English instruments**, with the flagship number unchanged: gemma12 EN −0.27 ≡ gemma12 PT −0.27. The failing models' deficits remain named reading classes (starved sheets, wrong layers, dispersion habits), never engine arithmetic: the same engine produced all five diamonds.

## Part A — MA-1: the dichotomous chain is robust across the whole cast (new finding)

| model | morbidity DL (pub. 0.778 [0.567, 1.068]) | mortality DL (pub. 1.021 [0.446, 2.337]) |
|---|---|---|
| gemma12 | 0.779 [0.569, 1.065] | 1.023 [0.447, 2.344] |
| qwen14 | 0.779 [0.569, 1.065] | 1.021 [0.446, 2.337] |
| llama8 | 0.771 [0.562, 1.059] | 1.023 [0.447, 2.344] |
| qwen35 | 0.779 [0.569, 1.065] | 1.019 [0.445, 2.336] |
| deepseek14 | 0.775 [0.565, 1.063] | 0.980 [0.428, 2.246] |

**All five models' pools reproduce the published dichotomous estimates** (every value within ±0.01 of the published, except deepseek14's mortality at Δ0.04 from its own cell variance). The Portuguese record had measured this only for gemma12 (Study 6); the English campaign extends it to the full cast: **extracting event counts and denominators is within reach of every model in this class — the discriminating task is the continuous chain** (means, dispersions, declared types), exactly where the five diamonds above separate. The per-model erratum-aware comparison files (categories, ileus non-comparability under erratum #16) are in `p3-ma1/`.

## Ablation note (H8.5, third column) and H8.3

H8.3 passes on the Portuguese record's own standard: gemma12's MA-1 pools reproduce under DL, its MA-2 lens lands beside the published value (−0.27, the identical number), and only gemma12 among the five reaches it. No language effect visible at the creation stage — the flagship number did not move by a hundredth across the language change.

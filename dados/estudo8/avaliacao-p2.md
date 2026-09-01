# Study 8 / P2 CALCULATE — evaluation (five models, arms A/B, English instruments)

**Run 2026-09-01, 60/60 runs, 87.1 min.** Truth = the validated engine over each model's OWN P1 cells under the frozen Study-2 parse rules; labels per reported quantity (both replicates summed); grader `p2-avalia.py`, full counts in `avaliacao-p2.json`.

## The headline: the Portuguese-record signature reproduces under English instruments

**Unaided (arm A), 95% confidence intervals**: **1 exact in 57 attempts** across all five models (gemma12 0/16, qwen14 0/16, qwen35 0/16, llama8 1/9, deepseek14 0) — the English twin of the PT record's 0/30.

**With the calculator (arm B)**: exact CIs jump to **41/50 (82%)** among the four models that operate the tool — gemma12 11/16, qwen14 14/16, llama8 8/9, qwen35 8/9 — and exact point estimates rise in step (4→12, 4→14, 5→8, 5→8). Same models, same sheets, same arithmetic: the tool is the difference, in either language. **H8.2 passes.**

## Secondary observations (all echoing PT behavior classes)

- **Pools stay hard even with the tool**: pool-exact ≈ 0 across the cast (assembling list-arguments for `pool_*` calls is the step this size class fails — in the PT record only the 27B mastered it, and the 27B is not in this cast). deepseek14's pool-B ran with **zero CALC calls** (answered without touching the tool).
- **deepseek14's arm A is unusable**: 5 of 6 outputs unparseable and zero gradable quantities (its reasoning-leakage class); arm B partially recovers (2 exact points).
- `sem-verdade` counts (7–12 per model-arm) are the md-family cells whose truth is not computable from the model's own sheet (median/IQR times) — the rubric's expected drawer, not an anomaly.

## Ablation note (H8.5, second column)

Qualitatively identical to the Portuguese record at every load-bearing point: unaided interval arithmetic fails, the text-protocol calculator repairs it, pool assembly remains beyond the iGPU cast, and the deviant behavior classes belong to the same models. No language effect visible at the arithmetic stage.

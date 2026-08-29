# EXTRAI — Study 3 evaluation (grading record): "the pipeline"

Queue of 32 runs completed in 272 min (2026-08-29): 14 extractions (gemma4:12b, iGPU) + 14 audits (qwen3.8:27b, CPU, two lanes) + 2 CALC arithmetic runs + 2 syntheses (gemma4:26b). Grading mechanical (`corrigir-e3.py`); public adjudications in [`adjudicacoes-e3.json`](adjudicacoes-e3.json); the ruler itself was corrected three times under the rite (Amendment 2 routes; the name+year matching bug; the IC-bounds parser that read the "95" of "IC95:" as a bound — on that one **the model computed correctly before the judge did**).

**Who did what**: the local models extracted, audited, computed (through CALC calls executed in Python by the harness) and synthesized; the harness ran queues, executed calls, applied the sealed seeds and built audited sheets; the mechanical grader labeled cells against the perturbed-source key; Claude (assistant) designed, adjudicated with quotes, and wrote this record; the author supplied the closed PDFs and the design decisions.

## Stage E — extraction (gemma4:12b, 7 perturbed texts × 2 replicates)

| Trial | r1 | r2 | Notes |
|---|---|---|---|
| Saslow 2017 | 15/15 | identical | reads perturbed baselines 5.8/7.6; finds the literal "0/8" |
| Saslow 2023 🔒 | 9/13 + 4 adjudicated | identical | factorial identified; cell-ns 23/25 (adjudicated: literal, margin pairing noted) |
| Dorans 2022 | 13/13 | identical | reads perturbed −0.24 and total 141 |
| Chen 2020 | 13/17 + 4 adjudicated | identical | **the study's 2 wrong cells**: final-timepoint SDs (0.59/1.06) paired to the change mean (truth: the CI); header-ns in the randomized layer (accepted, E1-13 pattern) |
| Thomsen 2022 🔒 | 15/15 | identical | reads perturbed −0.56 and 8.09 |
| Wang 2018 | 11/11 | identical | took the twin per-protocol table (−0.63±1.18/−0.31±0.70, n=24/25) — literal alternative route |
| Goday 2016 | 17/17 | identical | correctly leaves change NR; reads perturbed finals 5.3/7.1 |

**Totals (r1): 99/101 cells (98%) — 2 wrong (one root cause), 0 omissions, 0 attributable recitations; replicate 2 identical cell-for-cell (stability 100%).** Reading proof: every valid perturbed target returned perturbed (word-form leaks graded symmetrically, Amendment 2).

## Stage A — audit (qwen3.8:27b; L = clean lane, S = seeded lane)

- **Seeds (lane S): 9/10 seeded cells caught (90%); exact correction 8/9.** All four semantic seeds (2 arm swaps, 2 sign flips) caught and corrected with literal quotes; both n-transpositions caught; the basal digit caught but corrected to the wrong arm's value; **the digit inside a CI string (−0.37 for −0.33) sailed through** — the only miss. Directional hypothesis (semantic > character-level) confirmed exactly.
- **False alarms (real, wrong-value corrections on correct fields): lane L 6/93 (6.5%), lane S 5/85 (5.9%)** — plus 6 route swaps per lane (corrections landing on *other literal values*: factorial margins 45/49, Goday's table-1 rounding 6.89/6.88), which repair or lateral-shift rather than damage.
- The five signature behaviors, all with literal record: (1) **margin normalization** — summed the factorial flow cells to 45/49, the MA's own reading; (2) **computed imputation** — fills NR/basal fields with values it derives (pooled-cell baselines "6.11"; final = baseline + change), including the **half-patient "24.5"** written while citing the text's "(n = 28)"; (3) **column-map inversion** — un-swapped Chen's seeded change means perfectly, then swapped the basals/finals between arms (the deWaal-flowchart echo); (4) **contradiction tie-breaking is unstable** — the digit-vs-number-word conflicts resolved toward digits on Thomsen (63) and Wang-L (49) but toward words on Wang-S (56); (5) verdict instability across lanes on rounding-divergent duplicate reporting (Goday 6.9/6.8 confirmed in L, "corrected" to 6.89/6.88 in S).

## Stage C — arithmetic (qwen3.8:27b, CALC + forced closure)

Both lanes **closed on their own: 23 and 22 executed calls, 0 forced closures** — the Study-2 non-closure mode did not reappear. Orchestration was textbook: conversions (`dp_de_ic`, `dp_de_se`, `dp_mudanca_r05`) → per-study `md`/`ic95_md` → `pool_dl_md`.

| Study (lane L) | model MD [CI] | truth over same sheets | verdict |
|---|---|---|---|
| Saslow 2017 | −0.50 [−0.89, −0.11] | −0.50 [−0.89, −0.11] | exact |
| Saslow 2023 | −0.18 [−0.37, +0.01] | −0.18 | exact |
| Dorans 2022 | −0.20 [−0.29, −0.11] | −0.20 | exact |
| Chen 2020 | −0.43 [−0.78, −0.08] | −0.43 (over the audit-damaged inputs) | exact |
| Thomsen 2022 | −0.27 [−0.45, −0.09] | −0.27 | exact |
| Wang 2018 | −0.32 [−0.87, +0.23] | −0.32 | exact |
| Goday 2016 | **−1.30** [−1.56, −1.04] | **−1.90** | **wrong: the model flipped the control's + 0.3 (perturbed control *worsened*) to −0.3 — plausibility bias beating the data** |

- Pooled, lane L: model **−0.39 [−0.60, −0.18], I² 75.7%** vs mechanical truth over the same audited sheets **−0.52 [−0.81, −0.22], I² 91.3%**. The gap has two named causes: Goday's sign flip, and **the pool call was fed a third set of dispersions inconsistent with the model's own per-study calls** (e.g., Saslow 2017 SDs 0.9/1.2 in the pool vs 0.42/0.43 in its own `md` call) — Study 2's H2.3 echo: pooling is where assembly discipline breaks, even through the tool.
- Lane S: model −0.43 [−0.62, −0.24] vs truth −0.50 [−0.78, −0.22]. Truth L→S delta (−0.52→−0.50) is the surviving digit seed's push: it inflates the dominant study's SE (Dorans, dp 0.31→0.39), shrinking its weight — small and weight-proportional, as pre-registered.
- **End-to-end vs the anchor (the unperturbation lens)**: reversing the sealed perturbations on the audited-L sheets and pooling mechanically gives **−0.28 [−0.39, −0.17], I² 31.9%** vs the anchor's published **−0.24 [−0.32, −0.16], I² 6%** — same direction, same significance, overlapping intervals; the residue decomposes into named route choices (Wang's twin table; Chen's audit-damaged dispersions; analyzed-n conventions), not arithmetic.

## Stage S — synthesis (gemma4:26b, pooled numbers in context)

Both lanes correct on direction, magnitude, significance and I², and honest about heterogeneity and the crossing-zero study. Two blemishes, both mechanical: **246 and 248 words (2–4 below the 250 floor)**, and one orphan number each — "479" (L) and "494" (S) **participant totals the model summed by head, both wrong** (true sums of its own sheets: 542/558 depending on route) — Study 2's by-head arithmetic lesson closing the loop inside the pipeline.

## Forest (Stage F, deterministic script)

`forest-pipeline-L.png` / `-S.png`: pipeline squares and DL diamond beside the anchor's published values (grey). Goday's perturbation-made outlier is visually obvious; the diamond sits left of the anchor's dotted line by the decomposed gap above.

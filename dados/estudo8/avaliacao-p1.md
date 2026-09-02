# Study 8 / P1 READ — evaluation (five models, English instruments, perturbed MA-1)

**Run 2026-09-01, 390.4 min, 140/140 calls, every stop clean, zero parse failures at the sheet level** (one replicate-level exception below). Same corpora, same seals (SHA-256 in the run log, byte-identical to the Study-7 record), same corrected two-layer key as the Portuguese record — only the instruction language changed. Grader: `p1-avalia.py` (Study-6 magnitude comparator, declared an approximation; residue to adjudication).

## Scores

| model | cells vs key | replicate stability | recitation candidates | parse failures |
|---|---|---|---|---|
| gemma12 | 103/124 (83.1%) | 119/124 (96.0%) | 1 → **0 after adjudication** | 0 |
| qwen14 | 104/124 (83.9%) | 123/124 (99.2%) | 1 → **0** | 0 |
| qwen35 | 104/124 (83.9%) | 103/124 (83.1%) | 0 | 0 |
| deepseek14 | 97/124 (78.2%) | 96/118 (81.4%) | 1 → **0** | 1 replicate (PMC4782303-r2) |
| llama8 | 88/124 (71.0%) | 96/124 (77.4%) | 2 → **0** | 0 |

**The mechanical caveat applies across models**: the comparator cannot see format/granularity equivalence, and the Studies 6–7 decompositions showed most gemma12 divergents are format-class. Cross-model ranking by this raw score alone is therefore provisional; the class-level adjudication happens at P3, where these same sheets feed the engines and value-level differences surface as effects.

## The recitation adjudication (the reading proof, held)

Five mechanical candidates, all adjudicated to **incomplete-perturbation artifacts — zero attributable recitations in 140 sheets**:

- **REF26 morbidity 113** (gemma12, qwen14, llama8): the perturbed table prints *"Composite index of major complications 101 (57.7)"* under a visible *n = 196* — the count was displaced (113→101) but the percentage survived, and 57.7% × 196 = 113. Three models independently resolved the printed inconsistency toward the surviving percentage: **arithmetic reconstruction from surviving correlates**, not recall. (Behavior note, identical in all three: the control cell — 117 (53.0), equally inconsistent — was *copied*, not reconstructed. Asymmetric preference, shared across models.)
- **PMC5589093 total fluid 4088** (llama8, deepseek14): the perturbation replaced the table occurrence (→4620) but the prose restatement *"4088mL (3400:4525)"* survives verbatim — a **surviving copy**, read as printed.

Both patterns are the already-registered instrument gaps (#2 derivable totals; #4 prose restatements), now with cross-model evidence. Backlog unchanged, never retroactive.

## Factuality profile (grader-side extension, run 2026-09-01; `p1-factuality.py`)

Divergent cells classified as omission / invention-candidate / value-or-format; the invention screen (numbers absent from the perturbed text and not derivable by %, sum, difference or mean) was also applied to **all** Anchor-2 sheet cells of P3-b (1,104 cells, both replicates):

| model | P1 divergents | omissions | invention candidates | value/format |
|---|---|---|---|---|
| gemma12 | 21 | 0 | **0** | 21 |
| qwen14 | 20 | 6 | **0** | 14 |
| llama8 | 36 | 0 | **0** | 36 |
| qwen35 | 20 | 4 | **0** | 16 |
| deepseek14 | 27 | 2 | **0** | 25 |

MA-2 screen: **zero invention candidates in any model** (NR counts 20–46 per model — the refusal behavior). The pilot's headline — *omission, never invention* — reproduces and strengthens under English instruments: even llama8, the pilot's inventor class, fabricated nothing in the campaign.

## Notes for the ablation table (H8.5)

The only 1:1 English↔Portuguese comparison this phase supports is gemma12 (the other four have no MA-1 PT record; their PT comparison lands at P3-b on MA-2): **EN 103/124 (83.1%) / stability 96.0%** vs the PT perturbed record's **100/124 (80.6%) / 96.0%** (Study 6) — a +3-cell difference, within the format-class noise band; stability identical to the decimal. First column of the ablation says: no language effect visible at the reading stage. deepseek14's one unparseable replicate echoes its PT behavior class (reasoning leakage) at reduced size.

## Cell-by-cell mechanism classification and a four-cell adjudication in the models' favor (2026-09-01)

Built for the manuscript's Supplementary Tables S1–S7 (author's directive: a detailed account of the omissions and value/format divergences, all five models): every one of the 124 non-matching cells was re-examined against the perturbed text its model read (`scripts/estudo8/p1-divergentes-classifica.py` for the mechanical passes; source-open verification for the rest; per-cell dump in `divergentes-classificados.json`). Exhaustive class totals: **12 omissions; 27 equivalent re-encodings (arithmetic verified — e.g. de Waal ASA 24:123:86:1 → 10.3/52.6/36.7/0.4% over the analysis-set totals); 26 population-layer choices (all quoted from the trials' own participant-flow text); 34 case-mix summaries; 12 genuine row/arm/scope slips (e.g. gemma12 took Castro's "Losses" row for blood loss; llama8 the mL·kg⁻¹ Voluven row; deepseek14 mixed Sun's "Female 16 (32)" row into ASA); 9 unmatched ratio-style re-expressions (all llama8; digits individually derivable, so the invention screen rightly stays silent; residue); 4 grader-side lookup collisions.** Sum 124 ✓; zero inventions reconfirmed cell by cell.

**The adjudication (quotation-bound, source open).** On Castro (PMC11061212) `perda_sanguinea_controle`, qwen14, llama8, qwen35 and deepseek14 all wrote `1283.2 ± 959.7` (two with "mL") — byte-identical to the key's `valor_fonte` and to the perturbed text's own line, quoted: *"Intraoperative bleeding (mL) b 1283.2 ± 959.7 1100.1 ± 851.1"* (the cell was never perturbed). The grading lens (`desperturba`) then applied the trial's seal pair **original 31 → perturbed 28** (an ASA count) as a plain substring replacement inside `1283.2`, producing `1313.2` and failing `compat`. **Verdict: correct transcription in all four sheets; the divergence charge is a comparator artifact.** One cell per model except gemma12 (whose 5062.9 ± 3287.5 on the same field is a real row slip — the "Losses" row). Table 2 of the manuscript keeps the comparator's unadjusted scores (the comparator was declared an approximation whose residue goes to adjudication) with a caption note; adjudicated-true scores would read qwen14 105/124, llama8 89/124, qwen35 105/124, deepseek14 98/124.

**Scope note (backlog, never retroactive):** the same reversal code served Studies 6–7, so the archived PT records may carry the same collision class on the same cell; checking the PT archives is registered as backlog. The mechanism's fix (word-boundary–aware reversal, mirroring the perturbation operator's own boundary awareness) is an instrument-fix backlog item for future rulers, never applied retroactively to published numbers.

**Update 2026-09-01 (author's decision):** the manuscript's Table 2 now adopts the adjudicated scores — correct 105/124 (qwen14), 89/124 (llama8), 105/124 (qwen35), 98/124 (deepseek14); value/format 13, 35, 15, 24 — with the comparator's raw output quoted in the caption and preserved here and in `avaliacao-p1.json`. The stable-divergents statistics remain counted over the comparator's raw divergent inventories, stated as such in the manuscript.

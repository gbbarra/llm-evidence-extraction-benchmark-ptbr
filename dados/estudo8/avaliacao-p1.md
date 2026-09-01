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

## Notes for the ablation table (H8.5)

The only 1:1 English↔Portuguese comparison this phase supports is gemma12 (the other four have no MA-1 PT record; their PT comparison lands at P3-b on MA-2): **EN 103/124 (83.1%) / stability 96.0%** vs the PT perturbed record's **100/124 (80.6%) / 96.0%** (Study 6) — a +3-cell difference, within the format-class noise band; stability identical to the decimal. First column of the ablation says: no language effect visible at the reading stage. deepseek14's one unparseable replicate echoes its PT behavior class (reasoning leakage) at reduced size.

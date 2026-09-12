# Study 12 — grader-side artifact on the anchor-2 v2 sheets: the dispersion-type object was stringified before the route read it

Found 2026-09-12 while inspecting raw v2 sheets to design the v3 sheet (Study 13). Recorded here before any correction of the record; the correction itself is the author's decision (taken the same day: fix the instrument, re-grade, replace the numbers, report it in the article).

## The defect

The v2 sheet delivers every data field as `{"value", "where", "quote"}`. The Phase-2 grader (`scripts/estudo12/e12-p2.py`, `celulas_a2`) converts the sheet with the frozen converter `e7d.ficha_ma2_pt` and only *then* unwraps the arm objects to their values. The converter normalizes the dispersion-type field with `tipo_pt(str(t))` — so with a v2 object the label became `"{'value': 'CI95: -1.1 to -0.6', 'where': …}"`, and the deterministic route (`dirigida.braco_deterministico`) never saw `IC95` or `SE`:

- a **CI-type** dispersion became `None` → the cell was graded as an **omission of the model**, and the trial dropped out of that sheet's pool (the sextet was incomplete);
- an **SE-type** dispersion was used **as an SD** → graded as a *wrong-type dispersion* slip of the model.

Only the anchor-2 v2 sheets are affected: v1 sheets carry strings; anchor 1's converter unwraps every field (`ficha_ma1_pt`); anchor 3 has its own reader. Study 9, which first ran v2 on this anchor, flattened the objects before converting (`e9-pools.py`, `achata_v2`); the Study 12 grader reintroduced the defect by ordering.

## What the models had actually written

Example, `qwen27q2` v2, Saslow 2017: `hba1c_change_dispersion = "-1.1 to -0.6"`, `hba1c_change_dispersion_type = "CI95: -1.1 to -0.6"`, quote = the Table 2 row `"HbA1c (%) 16 weeks –0.9 (–1.1, –0.6) … 32 weeks –0.8 (–1.1, –0.6) …"` — identical to its v1 sheet, plus the quotation. The grader recorded the derived SD as NR.

## Size (scratchpad `artefato_v2_tipo.py`, 2026-09-12; the seven cells of every a2 v2 sheet recomputed with the type unwrapped first)

| model, v2 | cells that change | now equal to the key | trials pooled, frozen → corrected | lens pool, frozen → corrected |
|---|---|---|---|---|
| gemma12 | 8 | 3 | 4/7 → 7/7 | −0.21 [−0.23; −0.19] → **−0.24 [−0.32; −0.17]** |
| qwen14 | 7 | 1 | 3/7 → 5/7 | −0.22 [−0.59; 0.15] → −0.27 [−0.45; −0.09] |
| llama8 | 6 | 1 | 5/7 → 6/7 | −0.58 [−0.85; −0.31] → −0.47 [−0.68; −0.25] |
| qwen35 | 8 | 5 | 3/7 → 5/7 | −0.88 [−2.14; 0.39] → −0.68 [−1.22; −0.14] |
| deepseek14 | 5 | 0 | 2/7 → 5/7 | −0.52 [−0.83; −0.21] → −0.22 [−0.57; 0.13] |
| qwen27q2 | 8 | 5 | 4/7 → 7/7 | −0.20 [−0.34; −0.05] → −0.25 [−0.37; −0.13] |
| **all** | **42** | **15** | | layer 2: −0.24 [−0.32; −0.16] |

The cells that change but still differ from the key are the model's own (an SD derived with the analysed n the model read, a sign, a genuine slip); they will be classified by the Phase-4 rules once the corrected values flow into P4.

## What this changes in the Study 12 reading

- The statement that the v2 sheet "starved" the anchor-2 pools is false: the models transcribed the interval and its type; the grader lost them. The real costs of v2 are the anchor-1 descriptive fields (mean −6.8 of 124 cells, unaffected by this defect) and the control characters that the strict JSON reader refused on anchor 3.
- H12.3's verdict does not change (the accuracy criterion fails on anchor 1; the estimate criterion needs two anchors), but on anchor 2 the corrected v2 pools are closer to layer 2 than v1's in 4 of 6 models under the adjudicated v1 pools.
- The verdict totals of Phase 4 (331 faithful · 175 omissions · 106 slips · 21 grader artifacts) and the anchor-2 v2 column of the cells table change once the record is re-graded.

## Fix (code, 2026-09-12)

- `scripts/estudo7/e7-downstream.py`, `braco_pt`: the type field is unwrapped before `tipo_pt` (root cause; v1 strings pass through unchanged).
- `scripts/estudo12/e12-p2.py`: `desembrulha_v2(js)` flattens the v2 objects **before** `ficha_ma2_pt`; the post-conversion unwrap stays as a second guard.
- `scripts/estudo12/e12-testa-v2-tipo.py`: regression test — a v2 arm with a CI-type object must route exactly like the v1 string (SD 0.42 at n = 11) and an SE-type object like its v1 string (SD 0.47 at n = 45).

## What remains to be done (not run yet — the author's decision on when)

1. Re-grade Study 12 anchor 2 with the fixed grader (`e12-p2.py`, then `e12-p4.py`): no model call, no GPU, about a minute. The frozen outputs of the models are untouched; only the grading of the a2 v2 sheets changes.
2. Replace the affected numbers in the record and in the article (both languages), and state the correction in one sentence: the earlier numbers were produced by a grader defect, found and fixed on 2026-09-12; the re-graded numbers replace them. Keep the pre-correction record in git history; do not rewrite it.
3. Re-read the reader's verdicts that sat on affected cells (`p4/vereditos-leitor.json`): those keyed on a stringified value stop matching and must be re-issued on the corrected values.
4. Only then decide Study 13 (v3): its origin paragraph is rewritten to this record; the remaining v3 rationale is table-row quotations, a type label checked by a net, and text hygiene, not pool starvation.

## Addendum, 2026-09-12 — a second defect in the same route, and the regrade

While adjudicating the residues of the first regrade, a second grader defect surfaced in the interval parser (`scripts/estudo3/dirigida.py`, `bounds_ic`): it took "the last two numbers across type + dispersion" with a sign-sensitive width, so (a) a Unicode minus or en dash before a bound was dropped and the "SD" came out negative (−0.42, −0.43, −0.4, −0.18 in deepseek14 v2 and qwen35 v2), and (b) a type field that repeats the value made the last two numbers the upper bound and the repeated value. Fixed: the parser normalizes Unicode signs, strips the "IC95/CI95" token, prefers the pair in the dispersion field and returns the bounds in ascending order; regression cases in `e12-testa-v2-tipo.py`. This fix also touched a few v1 cells (llama8 v1 Saslow 2017: the intervention SD became correct and the control SD, mixed bounds of two visits, became a slip; the lens pool's interval moved from [−1.03; −0.24] to [−1.02; −0.25]).

**Regrade (both fixes), 2026-09-12.** 619 non-matching cells (was 633): a2 v2 cells 34 · 22 · 16/42 · 30 · 24 · 36 (was 31 · 21 · 16/42 · 25 · 24 · 31); v2 lens pools gemma12 −0.24 [−0.32; −0.17] (7/7), qwen14 −0.27 (5/7), llama8 −0.51 (6/7), qwen35 −0.68 (5/7), deepseek14 −0.22 (5/7), qwen27q2 −0.25 (7/7); verdict totals 346 faithful (derived-own-n 33, unit 6), 147 omissions, 105 slips (row/scope 58, wrong-type dispersion 20, unmatched 17), 21 grader artifacts (unchanged: the 2026-09-01 collision, the lens miss, the derived-through-seal cells). H12.3: accuracy criterion still fails (anchor 1, −6.5 mechanical / −6.8 adjudicated); estimate criterion met on anchor 2 (4 of 6) only. The article's numbers were replaced with a dated sentence in the Methods; the Study 13 origin was rewritten.

# Study 12 — Phase 4: review of the 85 reader verdicts and of the 39 key-on-trial cells

Date: 2026-09-11. Requested by the author ("agora revise os 85 vereditos e as 39 células"). Reader of Phase 4: the assistant, under the author's delegation of 2026-09-11. Everything here is reversible: each verdict is a row of `vereditos-leitor.json` the author can overturn.

## Method

1. Three dossiers were generated from the Phase-4 record (`scratchpad/dossie_revisao.py`): one per anchor, each verdict beside the key's source-verified cell, the sheets it affects, the reader's evidence and quotation, and the paths of the original and perturbed texts; plus a dossier of the 39 key-on-trial cells (five groups).
2. Three independent reviewers (general-purpose agents, fresh context, no access to this chat) were instructed to **refute** each verdict with the source texts open: check that the quotation exists, redo the arithmetic, and test the class against the doctrine (faithful-different-encoding = the value is in the source in another encoding, layer or rounding; reading-slip = another row, arm, visit, dispersion type, or a number the source does not print; model-correct = the model was right and the grader wrong; key_on_trial = the key may sit in the wrong layer). Ranges: a1 V1–V35 + a3 V84–V85; a2 V36–V59; a2 V60–V83.
3. Every disagreement or uncertainty was then re-examined by the reader with the source open before any change. No model was called; no key was edited; Phase 2 was not rewritten. `e12-p4.py` was rerun over the corrected verdicts.

## Outcome

| range | verdicts | agree | disagree | uncertain |
|---|---|---|---|---|
| a1 V1–V35, a3 V84–V85 | 37 | 36 | 1 (V33) | 0 |
| a2 V36–V59 | 24 | 16 | 7 (V48, V54–V59) | 1 (V46) |
| a2 V60–V83 | 24 | 22 | 2 (V66, V74) | 0 |
| **all** | **85** | **74** | **10** | **1** |

Of the ten disputed verdicts, nine were accepted after verification and one (V33) was kept with a note. The uncertain one (V46) was kept with a note. Five further evidence texts were corrected without changing the verdict (V26, V27, V34, V62, V63) and nine notes were added (V1–V4, V29, V31, V32, V35, V78–V80).

### Accepted corrections (48 cells change class or verdict)

- **V54–V59, PMC6024764 (44 cells, all six models, both sheets): reading-slip → faithful-different-encoding (layer-choice).** The reader had read the models' 0.63 ± 1.18 / 0.31 ± 0.70 as "the 3rd-month change" against a key at "study end". The trial measured HbA1c only at baseline and at the end of the third month; Table 4 (n = 24/25) is the completers analysis and Table 5 (n = 28/28, "in ITT") the intention-to-treat analysis of the same visit. All twelve sheets wrote the completers triple (n = 24/25, means, SDs), the paper's own headline ("−0.63% vs. −0.31%"); the review pooled the ITT layer, coherent with its n = 28. The sealed cells of this trial (exp_media 0.54 → 0.48, exp_dp 1.12 → 0.94) sit in Table 5; the sheets read Table 4, whose figures the seal did not touch. Key layer not on trial: both layers are printed and the review's ITT choice is defensible.
- **V48, REF9 exp_n = 41 (2 cells, llama8 v1/v2): faithful (layer-choice) → reading-slip (row-slip).** 41 is the VLC arm's completers n for the *weight* outcome; the HbA1c completers n is 39, printed in the same paragraph, and the same sheets wrote 42 for DASH, the HbA1c completers n. The pair (41, 42) belongs to no single analysis set. The mechanical flow-context rule had accepted 41 because it sits in a "completers analysis" sentence; the reader overrode it.
- **V74, PMC5048014 ctl_dispersao = 0.94 (1 cell, qwen14 v2): reading-slip (unmatched) → faithful (layer-choice).** 0.94 = √(1.03² + 0.8² − 2·0.5·1.03·0.8) = 0.936: the key's own imputation rule (`sd_change_r05`, which the instrument gives the models) with the LC arm's baseline SD of Table 1 (6.88 (1.03), the randomized layer, N = 44) instead of Table 3's (6.8 (1.0), the analysed layer, n = 40). The same sheet's −0.48 also rests on the Table-1 baseline.
- **V66, PMC9606840 exp_dispersao = −1.15 (1 cell, qwen35 v1): row-slip → unmatched (verdict reading-slip unchanged).** −1.15 is printed nowhere in the original or in the text read; the nearest figures are the −1.1 confidence bounds of the HOMA-IR and HDL rows, and the reader's quotation had labelled the HOMA-IR row as a blood-pressure row.

### Kept with a note

- **V33, PMC10694978 mortalidade_controle = "0 (0)" (3 cells).** The reviewer argued model-correct: the model's cell is the verbatim source cell and the key's "0 (0%)" the re-encoded one; the comparator's zero rule (bare 0, NR or NA only) rejected it. Kept as re-encoding / faithful and not flipped, because the 2026-09-01 rule covers only the seal-pair lookup collision and the published record kept the same class for the extension arm (Sun, mortality). Listed for the author as a candidate extension of the grader-side rule (+1 cell on qwen35 v1, qwen35 v2, qwen27q2 v2 if flipped).
- **V46, REF9 ctl_n = 23 (2 cells, qwen14).** 23 is also printed for the DASH group as the dietary-adherence denominator (18/23) and in a drug-subgroup column (3/23, 15/23, 2/23) — sub-samples, not the arm's randomized (49) or HbA1c-analysed (42) count. The same sheets wrote 23 for both arms, so the duplicated VLC cell remains the most parsimonious reading; verdict kept (arm-swap / reading-slip), ambiguity recorded.

### Evidence corrected, verdict unchanged

- V26 (PMC11061212): 21 is the GDFT male count, 6 the GDFT diabetes count (the text had attributed 21 to the control arm).
- V27 (REF26): 114 = 57.7% × 198, where 198 is the GDHT analysed n the Results give while Table III's header says 196 — a count reconstructed from a percentage with a printed but inconsistent n; the earlier text had quoted the perturbed 117 as source and called 198 "the RNT arm's n". Still a slip by the V29/V31 distinction (a count invented by arithmetic is a slip; a percentage recomputed from a printed count is faithful).
- V34 (REF33): the printed 77.8 is a source-internal inconsistency (150/209 = 71.8%); the model copied it as printed. The earlier text had asserted 150/209 = 77.8%.
- V62/V63 (PMC9606840): 73/69 are the Table 2 (dietary composition) headers at 3 and 6 months (73 + 69 = 142 completers); the outcomes table prints 75/75.

## The 39 key-on-trial cells: recommendation

Five groups, three trials; all verdicts confirmed by the reviewers. Recommendation to the author: **keep the key's layer in all three trials; no cell flips.**

| trial · field | models wrote | key holds | what the source prints | recommendation |
|---|---|---|---|---|
| REF33 · n randomized GDHT / control (20 cells) | 224 / 226 | 209 / 211 | "450 patients were randomized to the GDHT group (n=224) or control group (n=226). Data from 420 subjects were analysed … 209 … and 211" — and, in the Results, "428 were randomised", a source-internal inconsistency | keep 209/211: the layer the review pooled (errata #13 already documents analysed-as-randomized); the models' figure is the literal randomized count, faithful |
| REF47 · n randomized PVI / control (14 cells) | 40 / 40 | 39 / 39 | "randomised into two groups (control group: 40, PVI group: 40) … 78 individuals were studied; 39 patients were assigned to each group" | keep 39: the count the review pooled; the source's reuse of "assigned" for the studied 39 is how it entered the key |
| PMC5048014 · ctl_n (5 cells) | 44 | 40 | abstract and Table 1: LC diet group n = 44 (randomized); Table 3 (efficacy): LC diet group (n = 40) | keep 40: the header of the table that supplies the key's own baseline and final means (6.8 → 6.4), so the key's n and means share one layer |

## For the author (key and instrument, not verdicts)

- REF33 `morbidade_eventos_controle`: the key's 35 (16.6%) is derivable (16.6% × 211 = 35.0), not literal — the outcome is printed only as "8.6% vs 16.6%", the two printed "35 (16.6)" cells are the ASA-1 and vasopressor rows, and the key's citation ("new standards, 35 a change…") is a reference marker. The key is frozen; the provenance label is the author's to correct.
- PMC4782303 `tipo_cirurgia`: the key enumerates one arm (the GDT column) for a trial-level field; the model's correctly transcribed control column was classed partial re-encoding.
- The comparator's zero rule rejects the verbatim source cell "0 (0)" (V33 above): a candidate extension of the grader-side rule, three cells.
- The mechanical flow-context rule for `_n` cells accepts any figure printed in a "completers/analysed" sentence, including another outcome's n (V48): a rule limit, one trial, two cells; the reader's override stands in the record.
- PMC6024764: the whole cast read the completers layer while the review pooled ITT — a legitimate layer disagreement between the models and the review that the adjudication now records as faithful; the key stays.

## Totals after the review (633 cells)

| verdict | before | after |
|---|---|---|
| faithful in another encoding or layer | 288 | **331** (165 population-layer choices · 78 summaries · 54 re-encodings · 3 partial · 16 SDs derived with the model's own n · 8 unit · 6 self-contradiction of the primary · 1 NR restated) |
| omission | 175 | 175 |
| reading slip | 149 | **106** (52 row/scope slips · 28 wrong-type dispersions · 16 unmatched · 6 arm swaps · 2 polarity · 2 field mixes); 74 of 106 on the continuous anchor |
| model correct, grader wrong | 21 | 21 |

Per anchor: a1 197 faithful / 25 slips (unchanged); a2 134 faithful / 74 slips (was 91 / 117); a3 unchanged. The 16 unmatched cells are unchanged in number (9 llama8 on anchor 1; 7 on anchor 2, now from five models: 0.94 left the list, −1.15 entered). Adjudicated scores, the 21 grader-side artifacts, the Anchor-2 pool sensitivity, the 39 key-on-trial cells and every hypothesis reading are unchanged: the review moved cells between *faithful* and *slip*, never into the score.

Files: `vereditos-leitor.json` (85 verdicts, 15 rows edited: 9 verdicts or classes, 5 evidence texts, notes), `adjudicacao-p4.json/.md` (regenerated), this record. Reviewer outputs are transient (agent transcripts); every claim adopted here was re-verified against the corpus text quoted.

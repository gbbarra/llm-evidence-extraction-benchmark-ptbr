# Study 12 — recitation candidates of Phase 2, adjudicated against the perturbed texts

Date: 2026-09-12. Source: `p2/avaliacao-p2.json` (`recitation_candidates` / `recitations` per model and sheet). No model was called; no key was edited.

The mechanical screen flags a cell whose raw text contains a sealed pair's *original* value while the displaced image the model actually read is absent from the sheet. Anchor 1: 13 candidates over the 12 model–sheet pairs; anchors 2 and 3: none (anchor 3's one costless trap, the review's 24/30 for Aguilar 2016, appeared on no sheet — see `p4/adjudicacao-p4.md`, errata check).

| candidate (original → displaced) | sheets | what the perturbed text still prints | adjudication |
|---|---|---|---|
| REF26, composite morbidity GDHT: `113` → 101 | 5 (gemma12 v1, v2; qwen14 v1, v2; +1) | "The primary outcome occurred in 57.7% of goal-directed hemodynamic therapy" (three occurrences) and "(n ¼ 196)" | reconstruction: 57.7% × 196 = 113.1; the operator displaced the count but not the percentage beside it |
| PMC5589093, total fluid control: `4088` → 4620 | 5 | "2050mL (1199:2700) vs. 4088mL (3400:4525), p<0.0001" | the original survives verbatim in a prose restatement the operator did not displace; transcription, not recall |
| PMC10561433, morbidity events GDFT: `71.8` → 67.4 | 1 | "28/39 [67.4%]" | reconstruction: 28/39 = 71.8%; the operator displaced the percentage and left the counts |
| PMC10561433, morbidity events control: `83.3` → 73.0 | 1 | "30/36 [73.0%]" | reconstruction: 30/36 = 83.3%; same gap |
| REF26, n randomized control: `201` → 214 | 1 | "A total of 401 patients were randomized" and "200 allocated to GDHT" | reconstruction: 401 − 200 = 201; the operator displaced the arm count and left the total |

**Verdict.** Zero attributable recitations. All 13 candidates are reconstructions from values the perturbation operator left in the text — a surviving percentage, a surviving prose restatement, surviving counts, a surviving total — the three operator gaps already recorded for these corpora. They are reading, and they were graded as correct cells by the frozen comparator because the reconstructed value equals the key's.

Instrument note (backlog, never retroactive): the anchor-3 seal recomputes dependent percentages and moves totals with their arms; the anchor-1 seal does neither, which is why every candidate above lives on anchor 1.

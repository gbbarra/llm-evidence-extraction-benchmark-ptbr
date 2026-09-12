# Study 12 — campaign report: three anchors, six models, both sheets

**Protocol** registered 2026-09-08 against commit `674e427` ([protocolo-estudo12.md](protocolo-estudo12.md)); Phase 0 instruments sealed and committed before the first call; P1 run 9–10 September 2026; P2/P3 graded 2026-09-11 02:58 ([p2/resumo-p2.md](p2/resumo-p2.md)); P4 adjudicated 2026-09-11 ([p4/adjudicacao-p4.md](p4/adjudicacao-p4.md)); P5 written 2026-09-11 (`paper/extrai-unified.tex`, Sections 2.11 and 3.7). Amendments: none. This file is the campaign report the protocol's §11 lists; every number below is reproducible from the scripts and records it names.

## The question, and the answer

**Does the architecture that measured five local readers on two anchors hold when stretched on three axes at once — a sixth reader as a peer, a third anchor in a third estimand, both sheets as a declared arm — and, on an anchor whose published cells are wrong in two of eight trials, does source-faithful extraction land the correction that peer review missed?**

Yes on the first half, with one control exceeded by one cell; yes on the second, and with room to spare: on the v1 sheet four of six models read the inverted trial (Aguilar 2016) as 6/30 from the Spanish source, six of six reduced the three-arm trial (Shaker 2025) to 15/60, four of six landed both cells, and **no sheet of any model reproduced either erratum**. Two 14B readers, `qwen3:14b` and `deepseek-r1:14b`, scored 32 of 32 cells and pooled to the layer-2 constants exactly: DL OR 0.484 [0.319; 0.735] and, by the review's own estimator (Paule–Mandel with Hartung–Knapp), 0.484 [0.342; 0.685] — significant, where the review published 0.73 [0.40; 1.36] and concluded no benefit.

## P1 — the campaign

| | |
|---|---|
| calls | 696 of 696 (6 models × 29 trials × 2 sheets × 2 replicates), every one passing the integrity gate |
| refusals / truncations | 0 / 0 |
| machine time | 39.7 h summed call time; 3.42 min per call; wall clock ≈ 28 h |
| tokens | 7,523,552 in · 784,246 out; largest prompt 17,898 of 24,576 (headroom 6,678) |
| interruptions | one operator accident: a second harness instance launched by hand at 04:52 on 2026-09-10 into the same queue and competed for the iGPU for ≈ 8 h (calls ≈ 7 min instead of 3.3); nothing corrupted — atomic writes and the per-call resume gate did their job; the surplus instance was stopped, and a single-instance lock (an OS-level file lock, tested under a real race) was added after the run and before any grading |
| context | 24,576 tokens for all six models and three anchors (the record ran at 16,384; H12.5 controls the change) |

## P2/P3 — cells and pools (mechanical, Phase 2; adjudicated, Phase 4)

Cells agreeing with the source-verified key, adjudicated score (mechanical in parentheses where it differs):

| model | A1 v1 (124) | A1 v2 | A2 v1 (49) | A2 v2 | A3 v1 (32) | A3 v2 |
|---|---|---|---|---|---|---|
| gemma12 | 109 (108) | 106 | 33 | 31 | 23 | 23 |
| qwen14 | 105 (104) | 85 | 24 (22) | 21 (20) | **32** | 24/28† |
| llama8 | 92 (91) | 86 (85) | 24 (23) | 16/42 (15) | 26 | 23 |
| qwen35 | 95 (94) | 91 (90) | 30 (28) | 25 (23) | 28 | 16/28† |
| deepseek14 | 109 (108) | 102 (101) | 25 (24) | 24 (23) | **32** | 22/24† |
| qwen27q2 | 111 (110) | 110 (109) | 35 | 31 | 28 | 28 |

†sheets the strict JSON reader refused because the mandatory quotation carried U+0001–U+0008 inherited from the PDF-derived source (kirov2001.txt has 127 control characters, levin2004.txt 18); the tolerant reader, a declared sensitivity, recovers them to 28/32, 20/32 and 30/32 — one sheet (qwen35, luissilva2024 r1) is malformed JSON and stays out.

Pools from each model's own sheets (frozen engines; full table with intervals in `p2/resumo-p2.md` and in the article's Table on pools):

- **Anchor 1**: morbidity RR 0.738–0.788 on every sheet against layer 2's 0.787 (published 0.778); mortality 0.980–1.078 except `qwen27q2` v1, whose 0.40 [0.02; 9.12] comes from a single stray denominator (31, a figure-caption number written as de Waal's control n; adjudicated as a reading slip in P4).
- **Anchor 2** (lens): gemma12 v1 −0.27 [−0.38; −0.17] (the record's exact value), qwen27q2 v1 −0.25, gemma12 v2 −0.21, qwen27q2 v2 −0.20, qwen14 v2 −0.22 (3 trials); the rest −0.42 to −0.88 with starved or slipped sheets. Layer 2: −0.24 [−0.32; −0.16].
- **Anchor 3** (DL / PM+HK): qwen14 v1 and deepseek14 v1 **0.484 [0.319; 0.735] / 0.484 [0.342; 0.685]** on 8 of 8 trials; the other ten model–sheet pairs 0.418–0.548, all significant, on 4–7 trials. Layer 2 as above; published 0.73 [0.40; 1.36].

## The hypotheses

| | verdict | the number |
|---|---|---|
| **H12.1** generalization gate | passes 9 of 12 on the primary reading; the 3 failures are v2 sheets refused by the strict reader, and the DL pool is digit-consistent with its own cells in all 12 | see † above |
| **H12.2** the one that decides | **passes, with room**: v1 — Aguilar 6/30 in 4/6, 24/30 in 0/6; Shaker 15/60 in 6/6, 15/30 in 0/6; both in 4/6. v2 — 3/6, 5/6, both 2/6 | the pre-registered finding was ≥ 1 of 6 on both cells |
| **H12.3** sheet A/B at scale | **fails both criteria**: mean v2 − v1 on anchor 1 = −6.5 cells (floor −4; per model −2, −19, −6, −4, −7, −1); v2 closer to layer 2 in ≥ 4 of 6 models on 0 of 3 anchors (under the P4-adjudicated pools, 4 of 6 on anchor 2 alone — still one anchor short) | closes Study 9's question in the negative |
| **H12.4** provenance nets (exploratory) | the expected excess on the table-dwelling anchor did not appear: N9-1 flags 19–39 % of eligible anchor-3 cells vs 10–57 % (a1) and 13–54 % (a2); N9-2 7–43 % vs 7–43 % and 13–45 % | `p2/redes-proveniencia.json` |
| **H12.5** context control | **fails by one cell**: gemma12 a1 v1 108/124 mechanical (109 adjudicated) against 103 ± 4; a2 lens exactly −0.27 (band ± 0.05) | the context change is declared a confounder for every cross-campaign comparison |
| **H12.6** the bounded null | falls: 11 of 12 model–sheet pairs exceed 50 % of the 32 cells (qwen35 v2 at 16/28 is the one below on the primary reading; 20/32 tolerant) | |

## P4 — adjudication of the 633 non-matching cells

Every cell that failed the layer-2 comparison (297 on anchor 1, 273 on anchor 2, 63 on anchor 3) sits in `p4/adjudicacao-p4.md` beside the key's source value, the published value, the deciding quotation and the rule or reader that decided it. Mechanical rules — Study 8's Supplementary classes extended to anchors 2 and 3 — decided 548; the reader (the assistant, under the author's delegation of 2026-09-11, every verdict reversible) decided 85 through `p4/vereditos-leitor.json`. Residue: 0.

| verdict | cells | what it means |
|---|---|---|
| faithful in another encoding or layer | 288 | 122 population-layer choices · 78 case-mix summaries · 54 percent-for-count re-encodings · 3 partial re-encodings · 16 SDs derived by the key's rule with the analysed n the model read · 8 unit re-encodings (mmol/mol) · 6 the primary's own self-contradiction · 1 "not reported" restated in words |
| omission | 175 | 167 NR + 8 label-only cells; on anchor 3, 56 of 63 (the Spanish primary: 5 sheets; the trial with no per-arm count: 4 sheets) |
| reading slip | 149 | 95 row/scope slips · 28 wrong-type dispersions · 16 unmatched values · 6 arm swaps · 2 polarity inversions · 2 field mixes; 117 of the 149 on the continuous anchor |
| **model correct, grader wrong** | **21** | 10 Castro seal-pair collisions (all sheets that transcribed the cell) · 1 reversal-lens miss on a Unicode minus (deepseek14 v2, REF12) · 10 "derived through the seal" (Goday: the key's own rule, change = final − baseline, applied to the perturbed text gives −1.6 or +0.3, which the lens cannot reverse; four models, both sheets) |

The 21 artifacts flip the adjudicated scores by one cell where they occur (table above). Because the Goday cells feed Anchor 2's pool, the lens pools carry the artifact; recomputed with those cells at the value the lens should have returned, qwen14 v1 moves −0.42 → −0.32, llama8 v1 −0.63 → −0.49, deepseek14 v1 −0.46 → −0.27, qwen35 v2 −0.88 → −0.32 — recorded as a sensitivity beside the Phase-3 primary; no hypothesis verdict changes.

**Key on trial (39 cells, listed for the author, not flipped)**: REF33 224/226 (randomized allocation; the key holds the analysed 209/211 the review pooled — Study 1 ruled 224/226 'exata'), REF47 40/40 (randomized; key 39/39 analysed), Goday control n 44 (randomized, abstract and Table 1; key 40 from a later table). All three are trials that print both layers under a field named *n randomized*.

**Instrument notes (backlog, never retroactive)**: normalize the minus sign before the reversal lens; the lens cannot reverse a derived quantity (the anchor-3 seal recomputes dependent percentages; the anchor-2 seal did not); the eligible-set rule keeps an NR cell that carries digits (PMC4782303 `asa_gdft`); the comparator's NR and zero rules are literal (`ratio not reported` ≠ `NR`; `0 (0)` ≠ `0 (0%)`); the Castro collision recurs on every sheet and the boundary-aware reversal remains backlog for anchors 1 and 2.

## Who did what

The six local models read (P1). The frozen engines, the anchor-3 corrector and `e12-p2.py` graded and pooled (P2, P3). The assistant wrote the protocol from the author's six Phase-0 decisions (the three assistant-originated design choices flagged and ruled on by the author before any call), built the anchor-3 key, seal and lens, the harness and its tests, `e12-p4.py` and the reader's verdicts, and drafted the article's new sections; the author took the Phase-0 decisions, launched and watched the campaign, and delegated the Phase-4 adjudication on 2026-09-11 with every verdict left reversible. The anchor-3 errata were raised by the assistant during key construction, before any model read the anchor, and the alert table drafted from them is held for the author's decision.

## What remains the author's

Review of the 85 reader verdicts and the 39 key-on-trial cells; whether to send the anchor-3 alert table; whether v2 becomes the library default (this study says no); the commit of P4 and P5; Zenodo and medRxiv.

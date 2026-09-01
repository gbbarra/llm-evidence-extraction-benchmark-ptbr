# Source-confirmed errata of the published GDFT meta-analysis — alert table for the journal and authors

**Prepared 2026-09-01** from the benchmark's public errata file (`erratas-da-ancora.md`), where every entry carries the literal source quotation that decides it. This table contains only **source-confirmed items about the published meta-analysis** — the file's withdrawn entries (the benchmark's own adjudicator errors, #2 and #4) and its still-pending items are excluded from any alert. Anchor 2 (the low-carbohydrate meta-analysis) is not listed because its verification found **no confirmed errata**: its statistics reproduced cleanly.

## A. Errors confirmed against the primary sources

| # | Where (MA) | Published | The source says (quotation on file) | Impact on conclusions |
|---|---|---|---|---|
| 1 | Characteristics table, Yoon | GDFT n=36 / control n=39 | "The GDHT group (n = 39)…"; "the control group (n = 36)…" | None on pooled outcomes (the morbidity table already used the correct 39/36) |
| 3 | Characteristics, Weinberg ASA | "Not stated" | "ASA Class I-II 7 (27%)… ASA Class ≥ III 19 (73%)" | Description only |
| 5 | Characteristics, Sujatha ASA | "95:105" / a cell corrupted by spreadsheet time-formatting ("2 days, 11:42:00") | Text reports only eligibility (ASA I–II), no distribution | Description only |
| 9 | Oral-diet outcome, Sun | 72±24 h vs 96±30 h (a 1-day difference) | "…shorten … time to first tolerate oral diet **by 2 days** (P < 0.001)"; medians 4.0 vs 6.0 days | **Magnitude wrong (understated ~2×), direction unchanged** |
| 10 | Characteristics, de Waal ASA | GDFT 24:123:86:1 / control 17:132:95:4 | Source column headers + arithmetic prove the inverse (123 = 52.6% × 234, the control arm) | Description only |
| 11 | Characteristics, Diaper ASA | "Not stated" | "ASA-PS classes III & IV 98 (50.0) 85 (42.9)" | Description only |
| 12 | Flatus outcome, Diaper and Coeckelenbergh | 55±14/58±16 h and 52±15/60±18 h | The word "flatus" does not occur in either full text (Coeckelenbergh's total fluid likewise absent) | **The flatus pooled result rests on 2 of its 3 rows that cannot be verified from the full texts** (possible supplement origin; unverifiable as published) |
| 13 | Characteristics, six trials' n | Sample sizes presented as randomized | Analyzed counts, undeclared, in six trials (Wu, Sujatha, de Waal, FEDORA, Hokenek, Diaper) | None demonstrated: our reproductions show the morbidity/mortality pools robust to the layer choice |
| 15 | Pooled morbidity caption | "Mantel–Haenszel" | The published numbers reproduce digit-for-digit under DerSimonian–Laird (MH gives 0.873 [0.758–1.005]) | Right numbers, wrong method name — conclusions unchanged |
| 16 | Ileus outcome, Castro | Ileus 6 (14.0%) / 19 (45.2%), RR 0.31 [0.14, 0.68] | "Ileus" occurs **zero** times in the primary; "Nineteen patients (45%) in the SOC and 6 in the GDFT (14%) had at least one **PPC**" — the published counts are the pulmonary-complication counts | **Changes a conclusion — see B** |
| 17 | Fluid table, Coeckelenbergh blood loss | GDFT 500 (300–800) / control 450 (300–600) | The results paragraph's own labeling convention (four for four) and the arm-labeled parallel sentences give the inverse | Description only |

## B. The one conclusion-level impact

The meta-analysis concludes **better gut function under GDFT, including a significant reduction in postoperative ileus (abstract: RR 0.48)**. That pool has three rows; erratum #16 shows one of them (Castro) is a different outcome — pulmonary complications published under the ileus heading. Recomputed over the two genuinely-ileus trials (Arslan-Carlon, Sun), the pool is **non-significant under either method**: Mantel–Haenszel 0.821 [0.559, 1.207]; DerSimonian–Laird 0.429 [0.048, 3.87] — reproduced identically from fresh model extraction in both the perturbed and the clean-text phases of the benchmark. **The significant ileus finding depends entirely on the mislabeled row.** (Secondary caveats in the same conclusion family: the oral-diet magnitude, erratum #9; the flatus rows' verifiability, erratum #12. A pending, not-confirmed item also touches this family: Sun's ileus counts are possibly I-FEED-derived.)

**Conclusions that survive every erratum** — demonstrated, not argued, by the benchmark's reproductions: pooled overall morbidity (0.778, no significant reduction) and pooled mortality (1.021, no difference) reproduce from the primary sources within ±0.01 under every population-layer route any of five independent extractors took.

## C. Suggested use

This table, with the errata file's quotations, is ready to support a letter to the editor and a courtesy note to the authors — offered in the same spirit the benchmark applies to itself: transcription errors happen in any hand-made review (this project's own adjudicator errata are published in the same file); the point is the process, and the ileus row deserves a correction because a stated conclusion rests on it.

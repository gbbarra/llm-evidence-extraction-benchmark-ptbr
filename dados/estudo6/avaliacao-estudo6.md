# Study 6 — evaluation: the replication, in detail (MA-1 GDFT + MA-2 formal)

**Written 2026-08-31**, against the [pre-registered protocol](protocolo-estudo6.md). Mechanical side-by-side: [`comparacao-detalhada.md`](comparacao-detalhada.md) (pre-adjudication output of `e6-downstream.py`); cell grading: `avaliacao-celulas.json` (`e6-avalia.py`). This page is the adjudicated record — the rite: no cell changes category without the source quote that decides it.

## The pre-registered question

**Does the frozen architecture — the measured local reader (gemma4:12b) plus deterministic code — replicate both anchor meta-analyses in detail: every per-study effect, every pooled estimate, every outcome family, with ALL residue decomposed into named categories — including the category no replication framework offers, "the published value is the one that is wrong"?**

## How it is measured

gemma12 re-extracted the 14 perturbed GDFT primaries from zero (2 replicates, frozen Study-1 instrument). Deterministic code — and only code — parsed the sheets, chose the event/n route per outcome, computed every RR/CI and both pools (Mantel–Haenszel and DerSimonian–Laird), and applied the sealed reversal. The comparison against the anchor's published tables 5–11 classifies every difference into the frozen categories (reproduz / difere-por-errata-da-âncora-#N / rota-do-modelo / erro-do-modelo / fonte-indisponível), with the pooled comparison under DL (anchor erratum #15: DL numbers under an MH caption). MA-2 is one formal run of the Study-5 pipeline-v2 procedure under this protocol's label.

## The answer

**Yes — and the replication graded the original in both directions.** From a fresh reading of the perturbed sources, the architecture reproduced **both published pooled estimates of MA-1**:

| pool | ours (DL, model cells + code) | published | verdict |
|---|---|---|---|
| overall morbidity (T5) | **RR 0.778** [0.571, 1.062] | RR 0.778 [0.567, 1.068] | **reproduz** (RR exact to 3 dp) |
| mortality (T6) | **RR 1.023** [0.447, 2.344] | RR 1.021 [0.446, 2.337] | **reproduz** |

Every per-study and pooled difference across the five outcome families landed in a named category — **zero unexplained residue** — and the exercise surfaced errors *on both sides of the comparison*: it advanced the anchor's pending Castro item to **confirmed erratum #16** (published "ileus" is the primary's pulmonary-complication count) and identified **confirmed erratum #17** (Coeckelenbergh's blood-loss arms swapped in the anchor's table 4) — both author-adjudicated 2026-08-31, [errata file](../estudo1/erratas-da-ancora.md). It also caught **our own grading key repeating the de Waal ASA swap** that the benchmark had already adjudicated as erratum #10 back on 2026-08-28 — a key-maintenance bug, not a new anchor finding. A replication framework that can only say "matches / doesn't match" has no drawer for any of these; the category system is the study's point.

## Hypothesis verdicts

| hypothesis | pre-registered claim | measured | verdict |
|---|---|---|---|
| H6.1 | fresh extraction in the measured band: ≥90% graded cells, **zero inventions**, zero attributable recitations | 28/28 sheets parseable, all 124 eligible cells filled; **0 invented values in 124** (every number traces to a source layer — see the divergent decomposition); values carry perturbed images (reading, not recall) | **passes** |
| H6.2 | zero unexplained residue; analyzed-vs-randomized ns and the Yoon rows land in *difere-por-errata* | zero unexplained residue ✓; the n-layer divergences land on errata #13/#14/#6 ✓; the **Yoon clause resolved differently**: erratum #1's swap is confined to baseline table T3 — the morbidity-table "Yun" row (39/36) was already the correct side, and our fresh reproduction (RR 0.862 exact) *confirms* #1's adjudication rather than exercising it | **passes** (Yoon clause: confirmed, not exercised — stated, not glossed) |
| H6.3 | fresh vs archived sheets agree on ≥95% of graded cells | **96.0%** (119/124) | **passes** |
| H6.4 | MA-2's lens lands beside −0.24 [−0.32, −0.16] a fourth time | lens **−0.25 [−0.33, −0.16]** (τ² 0.001, I² 8.5%) vs anchor −0.24 [−0.32, −0.16] — one hundredth off the three prior lenses' −0.24, CI matching to the hundredth on both bounds | **passes** (beside, not identical — stated plainly) |

The companion mechanical score — fresh reversed cells identical to the key's `valor_fonte` under the numeric comparator — is **100/124 (80.6%)**, measured *after* the key corrections below (it was 98/124 before; two cells resolve cleanly once the ruler is right, and two more move to an already-documented benign category — see the decomposition). That comparator is a *mechanical approximation* of the E1 ruler (it cannot see summarization equivalence or layer choices); all 24 non-identical cells are decomposed below.

## Per-study record, adjudicated (the rite: quote before verdict)

**Morbidity (T5).** Yun/Yoon **reproduz** (RR 0.862 ≡ published; and see H6.2 on erratum #1). The three "verificar" rows all resolved to **rota-do-modelo** with complete numeric traceability — the model copies the source's *printed percentages* and attaches *randomized* denominators, where the anchor uses *analyzed*:
- Calvo-Vecino: model 8.6%/16.6% over 224/226 → RR 0.504; anchor 18/209 vs 35/211 → 0.519. The percentages are the anchor's own; the denominators are the randomized layer (FEDORA's abstract, erratum #14's internally-contradictory 450-vs-428 primary).
- Diaper: model 57.7%/53.0% over 198/198 → RR 1.076; anchor 113/196 vs 105/198 → 1.087. The 198/198 reading is supported by the primary's own prose ("data from 198 and 196" — erratum #14 documents the prose-vs-table contradiction).
- Wu: model 32.8% (=19/58, the printed %) over 61/61 (the randomized layer, erratum #8: "61 patients were allocated to the PPV group and another 61") → RR 0.594; anchor 19/58 vs 32/56 → 0.573.

**Three per-study routes differ, the pool does not**: the DL pooled RR over the model's cells equals the published 0.778 to the third decimal — the pooled estimate is robust to the denominator-layer choice on this corpus.

**Mortality (T6).** de Waal **reproduz** (0.946 vs 0.944) — with a route note: the model's denominators (258/244, cited "Results 3.2.1. Primary outcome") are the source's primary-outcome population, a third layer distinct from both randomized (274/259) and the anchor's T6 totals (248/234); the RR agrees within tolerance regardless. Sun **reproduz** exact (3.0 [0.125, 71.927]).

**Ileus (T11).** Arslan-Carlon **reproduz** (1.192 vs 1.19). Sun **reproduz** at the published 2-dp precision (0.125 [0.030, 0.515] vs 0.13 [0.03, 0.53]) — with the errata file's standing caveat that the source counts are possibly I-FEED-derived (pending item). Castro: the model returned **NR — and the source proves it right** (confirmed erratum #16, below). Consequently our ileus pool covers 2 of 3 studies (DL 0.429 [0.048, 3.87]) and the published pool (abstract: RR 0.48, 3 studies) is **not comparable by construction**: its third row does not exist as ileus in the primary's text. Category: *difere-por-errata-da-ancora-#16*, counted, never silent.

**Time to flatus (T8).** All three rows in named categories, none computable from the sheets (dados-insuficientes, declared design §3.2): Sun *derivável-conversão* ("shorten time to first flatus by 11 h"); Coeckelenbergh and Diaper *fonte-indisponível* — erratum #12, the word "flatus" does not occur in either full text.

**Time to oral diet (T9).** Sun *difere-por-errata-#9* — the source: "GDFT significantly also shorten … time to first tolerate oral diet **by 2 days** (P < 0.001)" (medians 4.0 vs 6.0 d) against the anchor's 72±24/96±30 h conversion. Sujatha *dado-fora-do-insumo* (values live in its Table 4, outside the text corpus).

## The 24 divergent cells of the mechanical score, decomposed

Measured after both key corrections below are applied. Fixing the key resolved Coeckelenbergh's 2 blood-loss cells to a clean match (they leave this table entirely) and left de Waal's 2 ASA cells still mechanically divergent — not because the fix was wrong, but because the model expressed the same corrected quantities as percentages while the key holds ratio-counts, the identical format gap already on record for Sun's ASA cells. That reclassification is what moves the count from 13 to 15 in the first row below.

| class | n | cells |
|---|---|---|
| format/granularity — equivalent content the numeric comparator cannot see | 15 | `tipo_cirurgia` ×7 (model's category summary vs key's per-type counts, incl. EN-vs-PT text); Sun ASA as percentages ×2 (12%/72%/16% of 50 ≡ 6:36:8); **de Waal ASA as percentages ×2** (6.9%/53.2%/38.5%/1.4% of 248 ≡ 17:132:95:4 — the corrected fonte; same format gap as Sun's, only visible once the key's direction was fixed); Arslan ileus ×2 ("25% (36/142)" ≡ "36 (25.4%)"); Sujatha laparoscopy ×2 ("excluded" ≡ 0) |
| documented population-layer choice (rota-do-modelo) | 7 | Diaper n ×2 (198/198, prose layer, erratum #14); de Waal n ×2 (258/244, primary-outcome population, cited); Calvo n ×2 (224/226 randomized, erratum #13's counterpart); Sujatha n ×1 (100/100 = 102−2 analyzed, errata #6/#13) |
| genuine model omission | 2 | Castro blood loss ×2 (source: 1100.1±851.1 / 1283.2±959.7; model: NR) |

**Inventions: 0/124.** The model's only strictly chargeable failure in the graded set is the Castro blood-loss omission (2 cells, baseline field, no downstream effect). The two key-error cells found by the replication (Coeckelenbergh blood loss, both) resolved to exact matches once corrected — direct evidence the model's original readings were right and the ruler was wrong, exactly as claimed.

## Two corrections found by the replication, both confirmed by the author 2026-08-31

The two-layer key (`gabarito-oficial.json`) is itself an instrument, and the replication caught it twice — but the two cases turned out to be different in kind on closer inspection, and are reported precisely rather than lumped together.

**1. REF29 (de Waal) `asa_gdft`/`asa_controle` — a key-maintenance bug, not a new finding.** The key stored GDFT 24:123:86:1 / control 17:132:95:4, which is the **anchor's own swapped assignment** — but this exact swap is the benchmark's already source-confirmed **erratum #10** (adjudicated 2026-08-28: *"123 = 52.6% × 234 (control); 132 = 53.2% × 248 (PGDT). All four models followed the source, unanimously."*). The key cell was evidently never updated when #10 was written up; the fresh gemma12 simply followed the source again, as all four Study-1 models already had. **Fixed** in `gabarito-oficial.json` (`valor_fonte` swapped to 17:132:95:4 GDFT / 24:123:86:1 control; `veredito` → `errata-ma`). Because the model expresses this field as percentages ("ASA I (6.9%)…") against the key's ratio-count format, the corrected cell still shows as mechanically divergent in the table above — a format gap, not a direction error; see the decomposition.

**2. REF41 (Coeckelenbergh) `perda_sanguinea_gdft`/`perda_sanguinea_controle` — promoted to a new anchor erratum (#17).** Unlike case 1, this swap was **not previously logged anywhere**: checking against the anchor's own table 4 (`gabarito-ma.json`) showed the key's stored values match the anchor's published cells exactly (GDFT 500 (300–800) / control 450 (300–600)) — meaning the anchor itself, not just our key, has this swapped. The source states the two numbers in one unlabeled sentence ("no difference in blood loss … 450 … vs. 500 …"), but the same results paragraph uses the identical construction three more times, always with an explicit arm label, always decision-support (GDFT) first — four for four, no exceptions (full quotes: [errata file, item 17](../estudo1/erratas-da-ancora.md)). Independent corroboration: the fresh gemma12 read the same bare sentence, with no access to that convention analysis, and wrote the identical assignment (GDFT 450, control 500) in both replicates. **Fixed** in the key; **logged as confirmed erratum #17** in the errata file. This cell now resolves to an exact mechanical match — direct evidence the correction is right.

Symmetry note for Paper 4: Study 1 logged the adjudicator's errata; Study 6 logs the key's — and, in case 2, extends the anchor's own errata list. The process that grades is graded by the same rite. Scope note on retroactivity: the key correction is applied going forward (it is, after all, the instrument this very study grades against); Study 1's already-published evaluation and Papers 1–3's already-stated numbers are **not** rewritten — they report what the original run measured under the key as it stood then, per the benchmark's standing non-retroactivity doctrine.

## Confirmed anchor erratum #16 — Castro's "ileus" is the PPC count

*(For erratum #17 — Coeckelenbergh's blood-loss arms — see the key-corrections section above; it is logged there because the replication found it while checking the key, even though it is, like #16, ultimately a finding about the anchor.)*

**Adjudicated by the author, 2026-08-31 — confirmed.** The anchor's table 11 publishes Castro ileus 6 (14.0%) / 19 (45.2%), RR 0.31 [0.14, 0.68]. The primary's full text contains the word "ileus" **zero** times; its pulmonary-complications result reads: "**Nineteen patients (45%) in the SOC and 6 in the GDFT (14%) had at least one PPC** (p = 0.003)." The published "ileus" counts and percentages are exactly the primary's PPC counts.

Before confirming, the standing doubt — could the ileus data live in the primary's Supplementary Material instead? — was checked rather than assumed away: the text was searched for every bowel/GI-adjacent term (bowel, obstruction, gastrointestinal, flatus, defecation, constipation), all **zero hits**; and every declared supplementary item was read by its own caption — two tables (demographics; reintubation profile), three hemodynamic/blood-data graphs, one renal-biomarker (NGAL) graph, and a boilerplate "Image, application 1" journal-footer file — **none labeled as complications or bowel-outcome data**. The doubt was reasonable to raise; it does not hold up. Full record: [errata file, item 16](../estudo1/erratas-da-ancora.md).

This is now **erratum #16**, and it is the reason the published ileus pool (abstract RR 0.48) cannot be replicated from the sources: one of its three rows is a different outcome.

The fresh model wrote NR for Castro's ileus in both replicates — the reader refusing to invent is what exposed the row.

## MA-2 formal run (H6.4) — closed 2026-08-31, 41.2 min

One formal execution of the Study-5 pipeline-v2 procedure under this protocol's labels (EXTRA6M2/CALC6M2/POOL6M2; log `log-ma2.txt`, artifacts in `ma2/`):

- **Fresh extraction**: 191/206 graded cells (92.7%), zero content warnings in the calc stage, zero orphans.
- **The orchestrated pool** (gemma12 calling typed harness functions; every number computed by code): −0.58 [−1.00, −0.16], internally consistent with its own sextets; mechanical truth over the same sheets −0.52 [−0.83, −0.21] — delta MD 0.06 from route/argument choices, the measured Study-5 phenomenon at its usual size. Chen's reported CI was flagged incoherent and **flagged, never endorsed** (the E5-5 doctrine executing as designed).
- **The sealed lens (H6.4's number)**: **−0.25 [−0.33, −0.16]**, τ² 0.001, I² 8.5%, against the published −0.24 [−0.32, −0.16] (I² 6%). The fourth sealed lens; the first three sat at −0.24. Beside, not identical — the one-hundredth difference is fresh-extraction variance, reported as measured.

## Who did what (three voices)

- **gemma4:12b (local, iGPU, no API)**: read the 14 perturbed primaries twice and filled the sheets — including every printed percentage, every population layer, and the two NRs that exposed the Castro row. Nothing else.
- **Deterministic code (this repo, validated in Studies 2–4)**: parsed sheets, chose routes, computed every RR/CI/MD, both pools, applied the sealed reversal, produced the side-by-side tables and the mechanical cell score.
- **Claude (assistant)**: wrote the scripts, ran the pipeline, performed the adjudications recorded here (with the quoted sources), and drafted this record. The human author supervises, holds the seals, and adjudicates — errata #16 and #17 confirmed 2026-08-31, both key corrections applied to `gabarito-oficial.json` the same day.

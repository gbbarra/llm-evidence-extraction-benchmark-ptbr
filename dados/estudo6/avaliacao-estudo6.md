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

Every per-study and pooled difference across the five outcome families landed in a named category — **zero unexplained residue** — and the exercise surfaced errors *on both sides of the comparison*: it advanced the anchor's pending Castro item to a positively-identified erratum candidate (#16: PPC counts published as ileus), and it caught **two cells of our own grading key that contradict the source** (de Waal ASA, Coeckelenbergh blood loss — the model read them correctly; the ruler had them wrong). A replication framework that can only say "matches / doesn't match" has no drawer for either finding; the category system is the study's point.

## Hypothesis verdicts

| hypothesis | pre-registered claim | measured | verdict |
|---|---|---|---|
| H6.1 | fresh extraction in the measured band: ≥90% graded cells, **zero inventions**, zero attributable recitations | 28/28 sheets parseable, all 124 eligible cells filled; **0 invented values in 124** (every number traces to a source layer — see the divergent decomposition); values carry perturbed images (reading, not recall) | **passes** |
| H6.2 | zero unexplained residue; analyzed-vs-randomized ns and the Yoon rows land in *difere-por-errata* | zero unexplained residue ✓; the n-layer divergences land on errata #13/#14/#6 ✓; the **Yoon clause resolved differently**: erratum #1's swap is confined to baseline table T3 — the morbidity-table "Yun" row (39/36) was already the correct side, and our fresh reproduction (RR 0.862 exact) *confirms* #1's adjudication rather than exercising it | **passes** (Yoon clause: confirmed, not exercised — stated, not glossed) |
| H6.3 | fresh vs archived sheets agree on ≥95% of graded cells | **96.0%** (119/124) | **passes** |
| H6.4 | MA-2's lens lands beside −0.24 [−0.32, −0.16] a fourth time | *formal run in progress; this section is amended when it closes* | pending |

The companion mechanical score — fresh reversed cells identical to the key's `valor_fonte` under the numeric comparator — is **98/124 (79.0%)**. That comparator is a *mechanical approximation* of the E1 ruler (it cannot see summarization equivalence or layer choices); all 26 non-identical cells are decomposed below, and four of them are the **key's** error, not the model's.

## Per-study record, adjudicated (the rite: quote before verdict)

**Morbidity (T5).** Yun/Yoon **reproduz** (RR 0.862 ≡ published; and see H6.2 on erratum #1). The three "verificar" rows all resolved to **rota-do-modelo** with complete numeric traceability — the model copies the source's *printed percentages* and attaches *randomized* denominators, where the anchor uses *analyzed*:
- Calvo-Vecino: model 8.6%/16.6% over 224/226 → RR 0.504; anchor 18/209 vs 35/211 → 0.519. The percentages are the anchor's own; the denominators are the randomized layer (FEDORA's abstract, erratum #14's internally-contradictory 450-vs-428 primary).
- Diaper: model 57.7%/53.0% over 198/198 → RR 1.076; anchor 113/196 vs 105/198 → 1.087. The 198/198 reading is supported by the primary's own prose ("data from 198 and 196" — erratum #14 documents the prose-vs-table contradiction).
- Wu: model 32.8% (=19/58, the printed %) over 61/61 (the randomized layer, erratum #8: "61 patients were allocated to the PPV group and another 61") → RR 0.594; anchor 19/58 vs 32/56 → 0.573.

**Three per-study routes differ, the pool does not**: the DL pooled RR over the model's cells equals the published 0.778 to the third decimal — the pooled estimate is robust to the denominator-layer choice on this corpus.

**Mortality (T6).** de Waal **reproduz** (0.946 vs 0.944) — with a route note: the model's denominators (258/244, cited "Results 3.2.1. Primary outcome") are the source's primary-outcome population, a third layer distinct from both randomized (274/259) and the anchor's T6 totals (248/234); the RR agrees within tolerance regardless. Sun **reproduz** exact (3.0 [0.125, 71.927]).

**Ileus (T11).** Arslan-Carlon **reproduz** (1.192 vs 1.19). Sun **reproduz** at the published 2-dp precision (0.125 [0.030, 0.515] vs 0.13 [0.03, 0.53]) — with the errata file's standing caveat that the source counts are possibly I-FEED-derived (pending item). Castro: the model returned **NR — and the source proves it right** (candidate erratum #16, below). Consequently our ileus pool covers 2 of 3 studies (DL 0.429 [0.048, 3.87]) and the published pool (abstract: RR 0.48, 3 studies) is **not comparable by construction**: its third row does not exist as ileus in the primary's text. Category: *difere-por-errata-candidata-#16*, counted, never silent.

**Time to flatus (T8).** All three rows in named categories, none computable from the sheets (dados-insuficientes, declared design §3.2): Sun *derivável-conversão* ("shorten time to first flatus by 11 h"); Coeckelenbergh and Diaper *fonte-indisponível* — erratum #12, the word "flatus" does not occur in either full text.

**Time to oral diet (T9).** Sun *difere-por-errata-#9* — the source: "GDFT significantly also shorten … time to first tolerate oral diet **by 2 days** (P < 0.001)" (medians 4.0 vs 6.0 d) against the anchor's 72±24/96±30 h conversion. Sujatha *dado-fora-do-insumo* (values live in its Table 4, outside the text corpus).

## The 26 divergent cells of the mechanical score, decomposed

| class | n | cells |
|---|---|---|
| format/granularity — equivalent content the numeric comparator cannot see | 13 | `tipo_cirurgia` ×7 (model's category summary vs key's per-type counts, incl. EN-vs-PT text); Sun ASA as percentages ×2 (12%/72%/16% of 50 ≡ 6:36:8); Arslan ileus ×2 ("25% (36/142)" ≡ "36 (25.4%)"); Sujatha laparoscopy ×2 ("excluded" ≡ 0) |
| documented population-layer choice (rota-do-modelo) | 7 | Diaper n ×2 (198/198, prose layer, erratum #14); de Waal n ×2 (258/244, primary-outcome population, cited); Calvo n ×2 (224/226 randomized, erratum #13's counterpart); Sujatha n ×1 (100/100 = 102−2 analyzed, errata #6/#13) |
| **errors of the ruler discovered by the replication** (model right, key wrong) | 4 | de Waal ASA ×2; Coeckelenbergh blood loss ×2 — see next section |
| genuine model omission | 2 | Castro blood loss ×2 (source: 1100.1±851.1 / 1283.2±959.7; model: NR) |

**Inventions: 0/124.** The model's only strictly chargeable failure in the graded set is the Castro blood-loss omission (2 cells, baseline field, no downstream effect).

## Errata of the ruler (key), discovered 2026-08-31 — not retroactive

The two-layer key (`gabarito-oficial.json`) is itself an instrument, and the replication caught it twice. Logged here with the deciding quotes; per the benchmark's standing doctrine, instrument fixes are **never retroactive** — E1's scores stand; the corrections enter the instrument-fix backlog for future studies.

1. **REF29 (de Waal) `asa_gdft`/`asa_controle`** — the key stores GDFT 24:123:86:1 / control 17:132:95:4, which is the **anchor's swapped assignment**, contradicting the benchmark's own source-confirmed erratum #10 ("123 = 52.6% × 234 (control); 132 = 53.2% × 248 (PGDT). All four models followed the source, unanimously."). The fresh gemma12 followed the source again (its percentages 6.9/53.2/38.3-band match the PGDT column). The key cell was evidently never updated when #10 was adjudicated.
2. **REF41 (Coeckelenbergh) `perda_sanguinea_gdft`/`perda_sanguinea_controle`** — the key assigns GDFT 500 (300–800) / control 450 (300–600) from the unlabeled sentence "no difference in blood loss (… 450 [300 to 600] ml vs. 500 [300 to 800] ml…)". The source's parallel abstract sentence fixes the "vs." order: "**The primary outcome was lower in the decision support group than in the restrictive group** (… 2.5 … vs. 4.6 …)" — decision-support (GDFT) first. Therefore GDFT = 450 (300–600), as the model wrote.

Symmetry note for Paper 4: Study 1 logged the adjudicator's errata; Study 6 logs the key's. The process that grades is graded by the same rite.

## Candidate anchor erratum #16 — Castro's "ileus" is the PPC count

The anchor's table 11 publishes Castro ileus 6 (14.0%) / 19 (45.2%), RR 0.31 [0.14, 0.68]. The primary's full text contains the word "ileus" **zero** times; its pulmonary-complications result reads: "**Nineteen patients (45%) in the SOC and 6 in the GDFT (14%) had at least one PPC** (p = 0.003)." The published "ileus" counts and percentages are exactly the primary's PPC counts. This promotes the errata file's pending Castro item to a positively-identified candidate — **pendente adjudicação final do autor** — and it is the reason the published ileus pool (RR 0.48) cannot be replicated from the sources: one of its three rows is a different outcome.

The fresh model wrote NR for Castro's ileus in both replicates — the reader refusing to invent is what exposed the row.

## MA-2 formal run (H6.4)

*In progress at the time of writing (extraction stage E under schema + anti-invention net; labels EXTRA6M2/CALC6M2/POOL6M2, log `log-ma2.txt`). This section is amended with the lens value when the run closes.*

## Who did what (three voices)

- **gemma4:12b (local, iGPU, no API)**: read the 14 perturbed primaries twice and filled the sheets — including every printed percentage, every population layer, and the two NRs that exposed the Castro row. Nothing else.
- **Deterministic code (this repo, validated in Studies 2–4)**: parsed sheets, chose routes, computed every RR/CI/MD, both pools, applied the sealed reversal, produced the side-by-side tables and the mechanical cell score.
- **Claude (assistant)**: wrote the scripts, ran the pipeline, performed the adjudications recorded here (with the quoted sources), and drafted this record. The human author supervises, holds the seals, and adjudicates the pending items (#16; the key corrections).

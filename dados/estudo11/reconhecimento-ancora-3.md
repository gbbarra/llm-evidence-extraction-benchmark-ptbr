# Anchor-3 reconnaissance — methylene blue in adult shock

**Status: reconnaissance only. Nothing is registered and nothing has been run.** This file records
what was verified against the source on 2026-09-02, so that a later protocol decision rests on
measurements rather than on recollection. The candidate was first surfaced during the Study 3
anchor hunt and has stood since then in the ledger
([`../estudo3/agenda-bracos.md`](../estudo3/agenda-bracos.md)) as *the generalization gate*.

## The candidate

| | |
|---|---|
| title | The Effectiveness of Methylene Blue in Adult Shock: A Systematic Review, Meta-Analysis, and Trial Sequential Analysis of Randomized Controlled Trials |
| journal | Journal of Clinical Medicine (MDPI) |
| published | 2026-06-10 · PMID 42355649 · PMC13302755 · doi 10.3390/jcm15124481 |
| licence | CC BY, full text XML retrievable from Europe PMC |
| trials | 9 randomized (8 septic shock, 1 post-cardiac-surgery vasoplegic), 535 participants |
| primary outcome | 28–30-day all-cause mortality — **dichotomous** |
| pooled effect | **OR 0.73 (95% CI 0.40–1.36)**, 8 studies, n = 479 |

**Why this anchor and not another.** It is a different clinical domain from the two low-carbohydrate
anchors, and its primary outcome is dichotomous, which exercises the RR / Mantel–Haenszel half of the
frozen engine — built and unit-validated, never run in a pipeline. The manuscript's own limitation
("two anchors from a single journal family and 21 primaries are the whole evidence base") names this
gap.

## Primary-source accessibility, verified by PMID against Europe PMC

| ref | trial | PMID | PMCID | licence | text |
|---|---|---|---|---|---|
| 18 | Shaker 2025 | 39780053 | PMC11707904 | CC BY | full XML |
| 19 | Ibarra-Estrada 2023 | 36915146 | PMC10010212 | CC BY | full XML |
| 20 | Kuri 2025 | 40110143 | PMC11915450 | CC BY-NC | full XML |
| 23 | Luis-Silva 2024 | 39469142 | PMC11514138 | CC BY | full XML |
| 24 | Dong 2025 | 41477182 | PMC12751372 | CC BY-NC | full XML |
| 16 | Memis 2002 | 12500513 | — | — | **closed** |
| 17 | Aguilar Arzápalo 2016 | — | — | — | **closed** |
| 21 | Kirov 2001 | 11588440 | — | — | **closed** |
| 22 | Levin 2004 | 14759425 | — | — | **closed** |

**5 of 9 open, 4 closed** — the same ratio the original hunt recorded, re-verified today rather than
carried over. The closed four would have to be obtained legally and kept out of the repository, as
the campaign's closed stratum already is.

## The structural finding that a protocol must confront

**This meta-analysis prints no numbers in its Results prose.** Section 3.3 (primary outcome) states
that methylene blue "was not associated with a statistically significant reduction in short-term
mortality", that the interval "crossed the null value", and that heterogeneity "was low" — without a
single figure. The per-trial estimates, the weights, the I² value and the diamond live only in
Figure 3, a raster forest plot. The sole numeric effect estimate in the entire article is the GRADE
row quoted above.

The data-availability statement offers no per-trial table: extraction tables "should be made
available by the corresponding author upon reasonable request".

Two consequences, both of which change the study design rather than merely inconveniencing it:

1. **The key can only be built from the primaries.** In Anchors 1 and 2 the meta-analysis printed a
   per-trial data table, so a model's cell could be checked against both the primary and the
   review's own reading of it. That middle layer does not exist here. This removes a route by which
   a model could reach the right number by copying the review instead of reading the trial — a
   cleaner test — while also removing the ability to attribute a divergence to the review's reading.
2. **No I² is recoverable for comparison.** The heterogeneity anatomy that Table 4 of the manuscript
   builds for Anchor 2 has no published counterpart here beyond the qualitative "low", plus the
   GRADE row's "I² = low". A protocol should state in advance that I² is measured but has no
   published reference value.

## A source-confirmed discrepancy in the anchor itself

The article's account of *which* eight trials entered the mortality synthesis is internally
inconsistent, and arithmetic settles it:

- The nine trials' sample sizes sum to **535**, matching the article's own total.
- Results §3.1 states that the head-to-head trial comparing methylene blue with vasopressin
  (Kuri 2025, n = 74) "did not contribute data to the pooled outcomes of interest, leaving eight
  trials". Removing Kuri gives **n = 461**.
- The GRADE table reports the mortality pool as **8 studies; n = 479**. Removing Levin 2004
  (n = 56, the one non-septic, post-cardiac-surgery trial) gives exactly **479**, and Figure 3's
  caption reads "forest plot for short-term mortality in **septic shock** trials", which is
  consistent with excluding Levin and *including* Kuri.

Both statements cannot hold. The prose excludes Kuri; the participant count and the figure caption
exclude Levin. This is the same class of defect the manuscript catalogues in its Table 1 for the
existing anchors, found here before any model has read a word — which is itself evidence that the
class is not peculiar to one journal family.

**It also means the anchor's target diamond has an ambiguous input set.** A protocol must fix, in
advance and in writing, which of the two readings the key adopts, and should measure against both
rather than silently pick one.

## Mortality data in the five open primaries, read from the sources

| trial | arms | methylene blue | control | timepoint |
|---|---|---|---|---|
| Ibarra-Estrada 2023 | 45 / 46 | 15/45 (33%) | 21/46 (46%) | 28 days |
| Dong 2025 | 36 / 36 | 9 (25.0%) | 15 (41.7%) | 28 days |
| Luis-Silva 2024 | 19 / 23 | 9 (47%) | 14 (61%) | 30 days |
| Shaker 2025 | 30 / 30 / 30 | 6 (20.0%) high dose · 9 (30.0%) low dose | 14 (46.7%) | in-hospital, p = 0.083 |
| Kuri 2025 | 37 / 37 | **not evaluated** | **not evaluated** | — |

Four of the five print raw counts by arm, which is what a dichotomous key needs. Two wrinkles are
already visible and belong in a protocol rather than in a surprise later:

- **Shaker 2025 has three arms** (two methylene-blue doses against one control). Folding a
  three-arm trial into a two-arm comparison is a decision — combine the treatment arms, or split
  the control — and different reviews make it differently. The pooled result depends on the choice,
  and the review does not state which it made.
- **Luis-Silva reports at 30 days, the others at 28.** The review's outcome is defined as the
  28–30-day window, so this is consistent, but the cells are not the same measurement.

## The discrepancy resolved against the primaries

**Kuri 2025 states in its own limitations that "the long-term effects, including mortality,
hospitalization, and ICU stays were not evaluated."** The trial therefore cannot have contributed to
a mortality pool, which corroborates the Results prose and refutes the participant count:

- the only pool consistent with the sources is the **eight non-Kuri trials, n = 461**;
- the GRADE table's **n = 479** is the sum of the eight *septic-shock* trials, a set that includes
  Kuri and excludes Levin — and Kuri has no mortality to contribute.

So the review's own participant count for its primary outcome does not match any pool the primaries
permit. This was established from the sources, before any model was involved, and it is the second
source-confirmed discrepancy in this candidate.

One consolation for the key: **Levin's mortality is recoverable from the review's own Table 1**,
which prints "0% MB vs. 21.4% placebo" against arms of 28 and 28 — that is 0/28 and 6/28. One of the
four closed primaries is therefore partly readable without obtaining the article, though the
extraction key should still rest on the source.

## The engine gap, which is the sharpest constraint of all

The frozen engine's dichotomous half is **risk-ratio only**:

- `pool_rr_mh` — Mantel–Haenszel fixed-effect **risk ratio** (`scripts/estudo2/e2-harness.py:76`)
- `pool_dl` — DerSimonian–Laird on the **log risk ratio**, with τ² and I² (`:90`)

The anchor's published diamond is an **odds ratio**: OR 0.73 (95% CI 0.40–1.36). Reproducing it as
published would require log-odds-ratio pooling, which the engine does not contain. This forces an
explicit choice that a protocol must make in writing and in advance:

1. **Compare on the risk ratio instead**, pooling the same extracted cells with the untouched
   engine and stating plainly that the published OR is not the same estimand. The engine stays
   frozen — which is the whole point of a generalization gate — at the cost of having no published
   number to land beside.
2. **Add an odds-ratio pooler**, unit-validate it as the others were, and register the addition as
   a dated amendment. This buys a digit-for-digit comparison with the published diamond but means
   the engine under test is no longer the engine the earlier studies froze.

Option 1 preserves the gate's logic and option 2 preserves its comparability; they cannot both be
had, and choosing quietly would undermine either claim. The choice is the user's.

## What is still unknown

Whether the three remaining closed primaries (Memis 2002, Aguilar Arzápalo 2016, Kirov 2001) print
28–30-day mortality by arm at all. Their follow-up windows are 48 h, 72 h and 24 h respectively, so
a 28–30-day mortality figure may not exist in the source for trials the review nonetheless pooled.
Until those three are obtained and read, the key cannot be completed, and whether OR 0.73 is
reproducible *from its own inputs* cannot be assessed even in principle.

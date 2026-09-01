# Study 7 — evaluation: the side-by-side, in the open (clean texts, both anchors)

**Written 2026-09-01**, against the [pre-registered protocol](protocolo-estudo7.md) (registered 2026-08-31; extraction ran 2026-08-31→09-01, 42/42 calls, 119.3 min, zero failures). Artifacts: [`comparacao-detalhada.md`](comparacao-detalhada.md) (MA-1) · [`comparacao-ma2.md`](comparacao-ma2.md) · per-trial three-way tables (`tabela-tripla-*.md`) · `avaliacao-celulas.json` · paired forests. First study run under the **English instruments**; clean original texts, no seal, no reversal — the §2 scoping applies throughout: **no reading-proof claim is made here** (Studies 1–6 carry that).

## The pre-registered question

**In natural conditions — original texts, no perturbation — how do the three extraction chains compare, cell by cell and effect by effect: the human sheet the anchor authors published, the local reader's fresh sheet (two replicates), and the deterministic recomputation? And does the erratum-aware comparison make the anchors' documented errata directly visible — the human column disagreeing with the source exactly where the errata live, the model column siding with the source?**

## The answer

**The errata are visible exactly as designed — the model sided with the source on all seven errata-panel cells, including all four direction-critical swaps — and the recomputation reproduced MA-1's published pools; MA-2's pool missed its tolerance for one named, single-cell reason, and correcting that one cell lands on the published diamond to the hundredth.**

| | measured | verdict |
|---|---|---|
| H7.1 replicate reliability (≥95%) | MA-1 **96.8%** (120/124) · MA-2 **95.4%** (103/108) | **passes**, both anchors |
| H7.2 errata panel sides with the source | **7/7** · direction-critical swaps **4/4** | **passes** |
| H7.3 pools within tolerance | MA-1 morbidity **0.779** [0.569, 1.065] vs 0.778 [0.567, 1.068] ✓ · mortality **1.019** [0.445, 2.336] vs 1.021 [0.446, 2.337] ✓ (both ±0.01) · ileus non-comparable by construction (erratum #16, declared) · **MA-2 −0.34 [−0.51, −0.18] vs −0.24 [−0.32, −0.16] — outside ±0.02** | **MA-1 passes; MA-2 fails as measured** — residue fully decomposed below |
| H7.4 band | 42/42 sheets parseable; 100% of eligible cells filled; **zero inventions** (all 21 MA-1 divergents trace to source layers/formats) | **passes** |

## The H7.2 exhibit — what the model wrote at every confirmed-erratum cell (clean text, replicate 1)

| erratum | trial · field | anchor published | source says | model wrote | side |
|---|---|---|---|---|---|
| #1 (swap) | Yoon · n per arm | 36 / 39 | GDFT 39 / control 36 | **39 / 36** | source |
| #3 | Weinberg · ASA | "Not stated" | I–II 7 (27%), ≥III 19 (73%) | **"Class I-II: 7 (27%); Class ≥ III: 19 (73%)"** | source |
| #9 | Sun · oral-diet time | 72±24 / 96±30 h | medians 4.0 / 6.0 days | **"4.0 days (2.7–6.0)"** | source |
| #10 (swap) | de Waal · ASA GDFT | 24:123:86:1 | 17:132:95:4 | **"I: 17, II: 132, III: 95, IV: 4"** | source |
| #11 | Diaper · ASA | "Not stated" | III–IV 98 (50.0) / 85 (42.9) | **"ASA-PS classes III & IV: 98 (50.0%)…"** | source |
| #16 (swap-class) | Castro · ileus | 6 (14.0%) / 19 (45.2%) | no ileus anywhere (PPC counts) | **NR / NR** | source |
| #17 (swap) | Coeckelenbergh · blood loss GDFT | 500 (300–800) | 450 [300–600] (decision-support first) | **"450 [300 to 600] ml"** | source |

Castro deserves its own sentence: on the clean text — with the anchor's "ileus" row plausibly in training data — the model **still wrote NR in both replicates** rather than reciting the published 6/19. The refusal that exposed erratum #16 in the perturbed world repeats in the open.

## MA-2: the anatomy of the one miss (H7.3's failed half)

**Every step decomposes to a single cell.** Five of seven per-study rows match the published forest (four exactly); Wang differs only at one CI bound (same sextet our Study-6 formal run produced — a stable dispersion-route difference, not noise). The driver is **Chen 2020**:

- Chen's primary prints the HbA1c change in **two layers**: the table as mean (95% CI) — *"−1.63(−1.96 ~ −1.30)"* — and the results prose as *"The 18-month mean change from baseline was statistically significant for the HbA1c (**−1.6±0.3 vs. −1.0±0.3%**)"*. *(Correction, 2026-09-01: this record's first version charged the model with computing the CI's half-width and misdeclaring it. Amendment 1's net run found the half-width **printed in the primary itself** — the quote above. The charge is corrected: the model transcribed a real printed layer verbatim.)*
- The model's sheet — **identically in both replicates** — transcribed the prose layer: change −1.6, dispersion **0.3, declared "SD"**. The failure is the **type judgment on an ambiguous "±"**: 0.3 equals the table CI's half-width for the experimental arm (0.33), so the paper's ± denotes the CI, not a standard deviation — and for the control arm the printed ±0.3 matches *nothing* (neither the SD 1.27 nor its own half-width 0.39): the primary's prose dispersion layer is internally sloppy.
- The deterministic route trusts the declared type by design; a 4× too-small SD gives Chen an outsized influence, inflates heterogeneity (published I² 6% → ours **79%**), and pulls the pool from −0.24 to **−0.34**.

This remains the failure class Paper 2 named in its limitations — *"a model that misdeclares its sheet escapes detection"* — now with the refinement that the misdeclaration was seeded by the source's own ambiguous ± convention. The single-cell counterfactual, computed grader-side as decomposition (never substituted into the result):

| pool | MD [CI95] | I² |
|---|---|---|
| as measured (primary result) | **−0.34** [−0.51, −0.18] | 79.0% |
| Chen's SDs from the key's rule (one cell corrected) | **−0.24 [−0.32, −0.16]** | 3.7% |
| without Chen | −0.23 [−0.30, −0.16] | 0.0% |
| published | −0.24 [−0.32, −0.16] | 6% |

One misdeclared dispersion type is the entire distance between our pool and the published one. Product-level note: the heterogeneity jump (6%→79%) and Chen's weight profile are precisely the downstream signature Paper 3's recommended product flags (weight dominance; incoherent-dispersion check against a printed CI) exist to catch — a dispersion-vs-declared-type coherence net (the sheet says SD, the cited text prints a CI) enters the instrument-fix backlog as the natural detection-only net for future rungs.

## MA-1: the 21 divergent cells of the mechanical score (103/124, 83.1%), decomposed

| class | n | cells |
|---|---|---|
| format/granularity — equivalent content the comparator cannot see | 15 | `tipo_cirurgia` ×7 (category summary vs per-type counts); ASA as percentages ×4 (Yoon 10.3/74.4/15.4% ≡ 4:29:6 of 39, exact; Castro 16/72/12% ≡ 7:31:5 of 43); Arslan ileus ×2 ("25% (36/142)" ≡ "36 (25.4%)"); Sujatha laparoscopy ×2 ("excluded" ≡ 0) |
| documented population-layer choice (rota-do-modelo) | 6 | de Waal n ×2 (259/244 — the flowchart's *received-intervention* layer this time; the perturbed run had taken the primary-outcome layer 258/244: same trial, two adjacent documented layers); Calvo n ×2 (224/226 randomized, erratum #14's self-contradictory primary); Hokenek n ×2 (40/40 randomized vs the anchor's analyzed 39/39 — erratum #13's own entry) |
| genuine model omission | 0 | — (the perturbed run's Castro blood-loss omission did not recur on the clean text) |

**Zero inventions.** Every model number traces to a printed source layer or an exact arithmetic form of one.

## Amendments 1–2 — the detection nets, run 2026-09-01 (registered before each run)

The author directed a re-run of the analysis **with the detection net armed**, as an advance within the deterministic sequence. Provenance settled on record: the benchmark has **one** detection-net harness (Study 5's frozen ten-net, warn-only harness — the one that flagged Chen in Study 6); it operates on model-emitted calls, so it cannot literally run in a model-free downstream. The amendments therefore **ported the doctrine to the sheet layer** — same principle (detect, warn, never substitute), new deterministic implementation, declared before execution. The primary H7.3 record is untouched by everything below. Full run record: [`redes-deteccao.md`](redes-deteccao.md).

| net | pre-registered claim | measured | verdict |
|---|---|---|---|
| N7-1 (declared type vs printed form) | A7-H1: flags exactly Chen's two arms | **zero flags** — and the reason is a finding: Chen's prose *prints* "−1.6±0.3 vs. −1.0±0.3", so a spread form exists at that mean and the rule correctly stays silent | **fails** — exposing the two-layer print |
| N7-2 (DL weight share > 40%) | A7-H2: flags the MA-2 pool, Chen dominant | Chen's share is **19.3%** (τ² re-equalizes weights); MA-2 max share is Dorans 20.4%, morbidity max 31.9% — no non-structural flags anywhere | **fails** — this distortion's product signature is **heterogeneity inflation** (I² 6%→79%), to which a weight-share flag is blind |
| N7-1b (Amendment 2: both forms printed and ± equals the interval's half-width) | A7-H3: flags exactly Chen's two arms | **flags Chen-exp** (±0.3 ≡ half-width 0.33, both quotes emitted) — **but not Chen-ctl**: its printed ±0.3 misses its own half-width 0.39 by more than the pre-registered ±0.06 (it matches nothing at all) | **partial, 1/2** — reported as measured, tolerance not widened post-hoc |

What the ladder measured, honestly: the naive port catches nothing (the ambiguity is *printed in the source*); the sharpened rule catches the experimental arm mechanically — one flag is operationally sufficient (any flag sends a human to Chen's table, which resolves both arms) — and the control arm shows the limit of mechanical detection against a primary whose prose dispersion matches nothing. Backlog (registered, **not run**): N7-1c — compare the declared spread against the interval-implied SD (`dp_de_ic`) when both forms are printed; expected to catch both arms; awaits the author's decision, as every rung does. Structural note: two-study pools (mortality, ileus) exceed the 40% share by construction and are reported, never counted.

## Declared exploratory: clean (E7) vs perturbed (E6) MA-1 sheets — descriptive only

Confounded by the instrument-language change (PT→EN) by design; no hypothesis. Descriptively: mechanical score 103/124 (83.1%) clean-EN vs 100/124 (80.6%) perturbed-PT; the divergent classes are the same families; two differences of note — the Castro blood-loss omission occurred only in the perturbed run, and Sujatha's n divergence occurred only there (clean-EN sheet matched the key). Nothing here separates language from perturbation from run-to-run variance.

## Replicate notes (H7.1's 9 disagreements)

MA-1 (4): formatting variants on free-text fields. MA-2 (5): includes Chen r2's `n_randomized` control 43 vs 42 — a one-digit slip on the *unused* field (the route reads `n_analyzed`); none of the five touches a routed quantity except confirming Chen's 0.3-as-SD is **stable, not stochastic**.

## Who did what (three voices)

- **gemma4:12b (local, iGPU, no API)**: read all 21 original primaries twice under the English instruments and filled the sheets — including every errata-panel cell above and the one misdeclared dispersion. Nothing else.
- **Deterministic code (validated, Studies 2–4)**: routed every sheet, computed every effect and pool, built the three-way tables and both forests, and computed the Chen counterfactual as decomposition.
- **Claude (assistant)**: wrote the scripts and this record; performed the divergent classification above with the quoted sources. The human author supervises; the Chen finding and the proposed dispersion-coherence net await their reading.

# EXTRAI — Study 4 evaluation (grading record): "extraction plus deterministic harness"

Grading closed 2026-08-30, same day as the run (68.5-minute queue, seals' SHA-256 in [`log-fila-e4.txt`](log-fila-e4.txt)). Ruler: the Study-3 amended `EXPECTED` key ([`corrigir-e3.py`](../../scripts/estudo3/corrigir-e3.py)), applied by [`avalia-e4.py`](../../scripts/estudo4/avalia-e4.py); adjudications with source quotes in [`correcao/adjudicacoes.json`](correcao/adjudicacoes.json); protocol frozen before the run ([`protocolo-estudo4.md`](protocolo-estudo4.md)).

**Who did what**: the local models produced only the 28 fresh extraction runs and one judgment answer (qwen14, one trigger); the deterministic engine ([`dirigida.py`](../../scripts/estudo3/dirigida.py)) parsed sheets, converted dispersions, computed every MD/CI and both pools; the mechanical grader labeled the cells; the adjudicator (Claude, under the author's supervision) resolved 70 flagged cells against the perturbed sources — and logs four of its own instrument errata below (E4-1..E4-4). No model computed anything downstream of its sheet.

## Stage E — fresh extractions vs the perturbed sources

| Model | r1 cells (feed the pool) | Both replicates | Replicate agreement (graded cells) | Sheets in pool |
|---|---|---|---|---|
| gemma4:12b | **97/103 (94.2%)** | 184/206 (89.3%) | 92/103 (89.3%) | 7/7 |
| qwen3:14b | **77/103 (74.8%)** | 146/206 (70.9%) | 98/103 (95.1%) | 7/7 |

All 70 mechanically flagged cells resolved to **errada** under the rite (each verdict quotes the source; see adjudications). The named failure modes:

- **gemma12** (fresh run vs its own Study-3 98%): chose the factorial's *per-cell* ns where rule 5 requires the diet *margins* on Saslow 2023 (its Study-3 run had taken the margin route — route drift between runs); put Chen's analysis-table ns (41/42) in the randomized field (the text is itself internally inconsistent: 92 randomized, table ns sum 83, 85 completed); replicate 2 wrote Chen's 18-month values into the baseline fields (r1 was correct; first-parseable kept the pool clean).
- **qwen14** (predicted ~90% omission-dominant; measured 70.9% **error-dominant with full coverage**): it computes where the instrument says read — Dorans' "dispersions" 0.07/0.04 are CI half-widths it derived (0.14/2, 0.08/2; printed nowhere), Goday's changes −1.6/+0.3 are differences of the perturbed levels (the table prints no changes) paired with final-timepoint SDs — the exact failure mode of gemma12's two Study-3 wrong cells, now in a second model; it declared "DP" over printed SEs (Saslow 2023) and over an MD-with-CI (Chen), skipping the engine's conversions; and on Thomsen it assembled a **chimera across units and levels** — baselines in mmol/mol, the *between-group* difference (−1.9 mmol/mol) as the experimental arm's change, the difference's CI as both arms' dispersion, the control change in % — every value printed somewhere, the assembly belonging to no world. Its replicate agreement (95.1%) is higher than gemma12's: it is *stable in its errors* — consistency is not correctness.
- **Gap #5 recurred**: with title/byline stripped by the corpus builder, qwen14 confabulated "Zhou et al. 2019" for Saslow 2017 in the ungraded `estudo` field (gemma12 did the same in Study 3 with Tidgren/Taves/Brackgold).

## The diamonds (primary and secondary metrics)

| Quantity | gemma4:12b | qwen3:14b |
|---|---|---|
| Pipeline pool (perturbed world) | **−0.52 [−0.83, −0.21]**, I² 91.2% | −0.48 [−0.73, −0.22], I² 88.7% |
| Mechanical truth over own sheets (graders' `sexteto`) | **−0.52 [−0.83, −0.21]** | −0.46 [−0.68, −0.25] |
| Δ pipeline vs truth | **0.00 [0.00, 0.00] — digit-exact** | 0.02 [0.05, 0.03] |
| Truth under corrected sign doctrine (erratum E4-3) | unchanged | −0.59 [−0.89, −0.29] |
| Unperturbation lens (sealed reversal, same sheets) | **−0.24 [−0.33, −0.16]**, I² 7.1% | −0.50 [−0.72, −0.29], I² 88.7% |
| Anchor as published | −0.24 [−0.32, −0.16], I² 6% | idem |

**gemma12 closes the study's question.** Fresh extraction, deterministic everything: the pipeline pool equals its own mechanical truth digit for digit, and the unperturbation lens lands on the published diamond to the hundredth (−0.24 vs −0.24; I² 7% vs 6%) — closer than Study 3's −0.28, because this run's route choices matched the anchor's construction better. The perturbed −0.52 is the reading proof; the unperturbed −0.24 is the fidelity proof; the models never touch the seal (the lens is grader-side code).

**qwen14 maps the boundary.** Zero arithmetic error anywhere — and still no unique diamond. Its Δ decomposes entirely into **deterministic-but-divergent parsing of malformed cells**: the engine's `bounds_ic` (last-two-numbers over type+dispersion) and the graders' `sexteto` resolve the Thomsen chimera and Dorans' fabricated dispersions differently (SDs 5.65/6.59 vs 4.76/4.69; 0.57/0.04 vs 0.31/0.25). The trigger's sign contributes nothing to this Δ because *both* codepaths flipped Goday's control — one induced by the leading question (E4-1), one by the convention overreach (E4-3). Lesson, stated once for Paper 2: **determinism is only well-defined over well-formed sheets.** When extraction is clean, code makes the diamond unique and exact; when extraction is malformed, even two deterministic parsers are two interpretations — the deterministic harness does not repair garbage, it propagates it reproducibly.

## The one judgment trigger

`qwen14 · Goday 2016 · braco_controle: +0.3 → −0.3`. The as-printed-positive trigger fired on a value the model had itself computed (the control arm genuinely worsened in the perturbed world), and the model flipped the sign — repeating, at a single narrow question, the exact plausibility-bias flip the 27B committed on the same trial and value in Study 3's CALC stage. The firing is recorded but **not chargeable to the model** (erratum E4-1): the question asserts the Wang premise ("the text prints the DROP as a positive number"), false for this arm — a leading question cannot measure judgment.

## Adjudicator/instrument errata (the rite applied to ourselves)

- **E4-1 — leading trigger question.** `pergunta_sinal` hardcodes Wang's convention into its text. Fix forward: state only the analysis convention and ask which sign the arm's change carries in the source, with no premise about what the printed positive means.
- **E4-2 — trigger coverage.** Of the three pre-declared trigger classes (protocol §2), only as-printed-positive was implemented; the factorial-margin flag would have fired on Saslow 2023's margins (both models' grouping error), and required-field-NR was never coded. The "zero triggers" of Study 3-H2 and the "one trigger" here are lower bounds under this coverage.
- **E4-3 — sign-doctrine overreach in the graders' `sexteto`.** The Wang printed-positive-is-drop convention is applied trial-agnostically to direct-read positive changes. Harmless in Study 3's world (only Wang's cells took that path; Goday went by the basal/final derivation branch, which does not flip — verified: gemma12's truths are unaffected in both studies). Wrong for qwen14's directly-written Goday +0.3. Both truths reported above; fix forward is scoping the convention to printed-drop-labeled fields.
- **E4-4 — parser divergence on malformed cells.** Engine and grader disagree only where sheets are malformed (see the boundary paragraph). Fix forward: one shared bounds/route parser for engine and graders.

## Pre-registered hypotheses — verdicts

| Hypothesis | Verdict |
|---|---|
| **H4.1** — gemma12 ≥95% cells, replicate-stable, diamond exact | **PARTIAL.** Diamond: exact (Δ 0.00; lens on the anchor). Cells: 94.2% (r1) / 89.3% (both reps) — *below* the 95% bar, and replicate cell-agreement 89.3% vs Study 3's 100%: fresh runs drift on route choices (factorial grouping; a wrong-field n; r2's finals-as-basals), not on values. |
| **H4.2** — qwen14 ~90%, omission-dominant, insufficiency over wrong numbers, diamond exact | **REFUTED — in the opposite direction predicted.** 74.8% (r1), error-dominant, **zero** dados-insuficientes: it filled everything (7/7 coverage) and wrong numbers *did* enter its pool. Diamond not exact vs truth (Δ 0.02; 0.11 under corrected doctrine), fully decomposed above. |
| **H4.3** — deviations fully named at extraction; none computational | **CONFIRMED, with one addition the protocol did not anticipate.** Zero arithmetic error in any run of either model. All between-model deviation names to extraction (routes, chimera, self-computation) and to the induced judgment answer — plus a third, instrument-side layer: deterministic parsing of malformed cells is itself a route choice (E4-4). |

## Machine time

28 extraction runs + 1 judgment answer + full deterministic downstream for two models: **68.5 min** on the iGPU (gemma12 ~7 min/trial-pair at first read, ~60–70 s at replicate-2 with the KV prefix; qwen14 ~3–5 min/pair), zero cloud cost.

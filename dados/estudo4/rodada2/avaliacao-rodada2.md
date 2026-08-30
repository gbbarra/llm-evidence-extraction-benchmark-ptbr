# EXTRAI — Study 4, round 2 evaluation (the record behind Paper 2's answer)

Closed 2026-08-30. Uninterrupted 146-minute queue (Amendment 2), five extractors, uniform fixed instruments; graded by [`avalia-e4.py`](../../../scripts/estudo4/avalia-e4.py) against the Study-3 amended ruler; 181 flagged cells adjudicated against the perturbed sources ([`correcao/adjudicacoes.json`](correcao/adjudicacoes.json)); side-by-side sheets in [`fichas-comparadas.md`](fichas-comparadas.md) and the full arithmetic in [`contas-comparadas.md`](contas-comparadas.md).

**Who did what**: the five local models produced only the 70 extraction runs and the trigger answers (3 sign/factorial answers, 12 field-recovery answers); the deterministic engine computed every number downstream; the mechanical grader and the adjudicator (Claude, under the author's supervision, quoting sources) decided the cells.

## 1. The question (frozen in the protocol before any run)

**Can local models that fit on the integrated GPU reach the expected meta-analytic value — the published −0.24 [−0.32, −0.16] — when extraction is theirs and everything downstream is deterministic code?**

## 2. How it is measured

Each model reads the 7 perturbed trial reports (twice) and fills structured sheets; code does all arithmetic; the graders then (a) score every sheet cell against a source-verified key, (b) recompute the pool independently to prove the plumbing adds nothing, and (c) reverse the sealed perturbations and compare the result with the published value.

## 3. The answer

**Yes — for exactly one of the five: gemma4:12b (−0.27 vs published −0.24; round 1: −0.24 to the hundredth).** The other four do not reach it (−0.44 to −0.54) — never because of arithmetic (every pool recomputes identically from their sheets) but because they read wrongly: wrong units, wrong table, wrong timepoint, computed-instead-of-read values. With the harness fixed, the entire bottleneck is reading.

## 4. The record

| Model | Cells (final, adjudicated) | Pool coverage | Diamond (perturbed world) | Δ vs own-sheet truth | Lens vs −0.24 | Replicate agreement |
|---|---|---|---|---|---|---|
| gemma4:12b | **190/206 (92.2%)** | 7/7 | −0.52 [−0.82, −0.22] | **0.00 — exact** | **−0.27** [−0.38, −0.17] | 96.1% |
| qwen3:14b | 151/206 (73.3%) | 7/7 | −0.62 [−0.99, −0.25] | 0.15 ¹ | −0.51 | 82.5% |
| llama3.1:8b | 146/206 (70.9%) | 5/7 | −0.30 [−0.49, −0.10] | 0.16 ² | −0.52 | 81.6% |
| qwen3.5:9b | 157/206 (76.2%) | 6/7 | −0.57 [−0.84, −0.30] | 0.01 | −0.44 | 63.1% |
| deepseek-r1:14b | 139/206 (67.5%) | 4/7 | −0.43 [−0.64, −0.22] | **0.00 — exact** | −0.54 | 58.3% |

¹ qwen14's gap is dominated by the graders' own sign-doctrine overreach (E4-3, documented): the pipeline judged Goday's control correctly (+0.3, kept under the neutral question) while the frozen `sexteto` still flips direct-read positives. ² llama8's gap is the values its NR-trigger recovered from its own sheet versus the graders' routes — instrument layer, named.

**The two independent axes** (round 2's structural finding): *in-world exactness* — whether the pipeline equals the mechanical truth of the model's own sheets (gemma12 and deepseek14: digit-exact; the architecture claim H4.3 holds for all five, zero arithmetic anywhere) — is not *fidelity to the literature* — whether the unperturbation lens reconstructs the published value (only gemma12). deepseek14 is the didactic case: perfectly exact inside its own world, and its world is wrong and half-covered.

## 5. The instrument A/B (the round's cleanest result)

Same model (qwen3:14b), same sheet, same value (Goday control +0.3, a genuinely worsened arm): round 1's leading question ("the text prints the DROP as a positive number") produced the flip to −0.3; round 2's neutral question (states only the sign convention) produced **+0.3, kept — correct**. The round-1 flip was **induced by the instrument** (erratum E4-1, now experimentally demonstrated), not model plausibility bias.

Other trigger results: the factorial-margin trigger (E4-2) fired for 4 of 5 models on Saslow 2023 — all four answered "SIM", confirming their own per-cell grouping (the trigger detects, but extractor self-verification does not correct); llama8's sheet declared "paralelo" and escaped, the logged escape the amendment predicted. The required-field trigger fired 12× and genuinely recovered sheet-derivable dispersions 3× for llama8.

## 6. New behavior classes for the ledger (first observed in round 2)

- **Invention**: llama8 wrote values printed nowhere (finals 5.53/7.07; changes −0.36/−0.15) — the first invented numbers in the entire benchmark (round 1's four veterans: zero in 624 cells).
- **Invention-by-arithmetic in a count field**: qwen3.5:9b averaged two group sizes into "n = 41.5".
- **Form contamination**: qwen3.5:9b wrote a full paragraph of chain-of-thought INTO a sheet field.
- **Wrong timepoint**: deepseek14 extracted Dorans' 3-month secondary row (−0.23) where the 6-month primary is required — printed value, wrong window.
- **Think-leak**: deepseek14 emitted `<think>` inside a judgment answer despite `think=false`.
- Adjudication also flipped 4 qwen3.5 cells to correct (accepted values broken only by `±`/prefix formatting) — the parser's numeric normalizer should strip `±` and CI prefixes (instrument backlog).

## 7. Round-to-round stability (iGPU pair, Amendment 2's standing comparison)

gemma12: diamond identical (−0.52/−0.52), cells 89.3→92.2%, replicate agreement 89.3→96.1% — the champion extractor is also the most stable. qwen14's world moved (−0.48→−0.62) for a named, instrument-level reason: the fixed question let its correct Goday judgment stand.

# EXTRAI — Study 9 evaluation: the quote-bearing sheet (schema v2) A/B against frozen v1

**Collection closed 2026-09-02.** Protocol: [`protocolo-estudo9.md`](protocolo-estudo9.md), with
amendments A9-1 to A9-4 registered before their runs. 210 extraction calls: four models under v2
(42 each) plus `granite4.2:8b`'s own v1 arm (42), the other three arms being the archived campaign
record. Graders, seals, keys and lens are the campaign's, unmodified; the lens is held constant
across arms per A9-2, seal-collision included.

## 1. The headline: the result is split, and the split is the finding

**The quote costs descriptive transcription and buys meta-analytic reading.** Those are opposite
effects in two different layers of the same sheet, and no single score expresses both.

### Anchor 1 — cell agreement with the source-verified key (124 eligible cells)

| model | v1 (arm B) | v2 (arm A) | delta | replicate stability v1 → v2 |
|---|---|---|---|---|
| `gemma4:12b` | 103/124 (83.1%) | **104/124 (83.9%)** | **+1** | 96.0% → 92.2% |
| `qwen3:14b` | 104/124 (83.9%) | **85/124 (68.5%)** | **−19** | 99.2% → 95.2% |
| `llama3.1:8b` | 88/124 (71.0%) | **79/124 (63.7%)** | **−9** | 77.4% → 83.0% |
| `granite4.2:8b` | 84/101 (83.2%)† | 92/124 (74.2%) | — | 68.9% → 83.1% |

†`granite4.2:8b`'s v1 arm lost three trials to unparseable pairs, so its two arms are graded over
different denominators and the raw delta is not interpretable; both figures are reported as
measured. **H9.1 (accuracy preserved) holds for `gemma4:12b` alone.**

**The cost has a named mechanism.** For `qwen3:14b`, 28 of its 39 divergences are omissions and
**18 of those are `asa_*`**: it writes `NR` rather than produce a quote it cannot support. The
schema does not make it wrong — it makes it decline. This is the instrument's tabular blind spot
(Section 3) charging its price in the most honest available currency.

### Anchor 2 — the diamonds, from the v2 sheets through the sealed lens

| model | v2 lens MD [95% CI] | I² | trials | v1 record (campaign) |
|---|---|---|---|---|
| `gemma4:12b` | **−0.24 [−0.32, −0.16]** | **7.6%** | 7/7 | −0.27 [−0.38, −0.17], I² 28.6% |
| `llama3.1:8b` | −0.50 [−0.77, −0.22] | 82.6% | 7/7 | −0.60 [−1.02, −0.18], 5/7 |
| `qwen3:14b` | −0.53 [−1.00, −0.06] | 95.6% | 6/7 | −0.63 [−1.08, −0.17], 6/7 |
| `granite4.2:8b` | −0.27 [−0.77, 0.22] | 84.3% | 3/7 | (no archived arm) |
| **published** | **−0.24 [−0.32, −0.16]** | **6%** | 7/7 | |

**`gemma4:12b` under v2 reproduces the published diamond digit for digit** — point estimate and
both interval bounds — with I² 7.6% against the anchor's 6%. Its v1 record was −0.27 [−0.38,
−0.17] with I² 28.6%: the honest-bound caveat the manuscript states for the campaign is closed
here by the instrument, not by better arithmetic (the engine is identical).

**All three models with a comparable record improved**: −0.27→−0.24, −0.60→−0.50, −0.63→−0.53.
`llama3.1:8b` additionally recovered two starved trials (5/7 → 7/7).

**Registered as hypothesis, not conclusion**: demanding the source sentence plausibly *anchors the
model on the right printed layer* where competing layers exist — and Anchor 2 is precisely where
the campaign showed the risk concentrates, in deciding what a printed `±` is. The cost appears
where no sentence exists; the gain appears where the sentence disambiguates. Four models on two
anchors cannot settle this; it is stated so a later study can test it.

## 2. The nets (H9.3): the criterion fails, and the failure is informative

Flags as a share of filled cells (denominator: cells with a value, in parseable sheets):

| model | filled cells | N9-1 quote-exists | N9-2 value-in-quote | N9-3 type-vs-quote |
|---|---|---|---|---|
| `granite4.2:8b` | 496 | 193 (39%) | 72 (15%) | **0** |
| `gemma4:12b` | 686 | 304 (44%) | 79 (12%) | **0** |
| `qwen3:14b` | 592 | 136 (23%) | 74 (12%) | **0** |
| `llama3.1:8b` | 695 | 224 (32%) | 274 (39%) | **0** |

**H9.3 (≤5% each) fails in every model, by a wide margin — and not because the models are
dishonest.** The editorial reading of `gemma4:12b`'s residue
([`suficiencia-das-citacoes.md`](suficiencia-das-citacoes.md)) found 73% of one model's N9-1
residue to be *stitched* quotes: real fragments of a table row, joined across a gap that
linearized text does not contain. The net measures contiguity; a table has none.

**N9-3 never fired, in any model, on any cell.** The net built to mechanize the campaign's
Chen-class defect at the sheet caught nothing. Two readings are compatible with this and the
study cannot separate them: either no model committed that defect here (H9.2 *prevented*), or the
net's recognizers are too narrow. The Anchor-2 diamonds favour the first — the type confusions
that drove the campaign's pool distortion did not recur — but the record states both.

**`llama3.1:8b` is the instructive outlier**: it fills the *most* cells (695) and quotes almost all
of them, yet 39% of its values do not occur in their own quote — by far the worst ratio. It
complies with the letter of the instrument and not with its purpose, which is exactly the profile
the campaign recorded for it (nine ratio-style re-expressions matching no printed layer).

## 3. Quote self-sufficiency: would a reviewer decide from the sheet alone?

Over the 124 eligible cells per model (adjudication-layer reading; counts mechanical, verdicts
made with source, quote and key side by side):

| model | agrees with key | quote filled | value checkable from quote | agrees **and** checkable |
|---|---|---|---|---|
| `gemma4:12b` | 104 | 106 | **89** | **80** |
| `granite4.2:8b` | 92 | 100 | 77 | 66 |
| `qwen3:14b` | 85 | 74 | 66 | 58 |
| `llama3.1:8b` | 79 | 109 | 51 | 39 |

For `gemma4:12b`, **13 of its 20 divergences are decidable from the sheet alone** — 9 whose quote
adjudicates the cell (de Waal and FEDORA quote the very sentence that reveals the population-layer
choice) and 4 self-contradictory (value and quote disagree, e.g. Weinberg's inverted percentages).
No v1 sheet could offer this. The full reading is in the companion file.

## 4. Costs (H9.4), measured

| model | tokens/sheet v2 | s/sheet v2 | unparseable | truncated | trials lost |
|---|---|---|---|---|---|
| `granite4.2:8b` | 1691 | 190 | 7 | 1 | 0 |
| `gemma4:12b` | 1489 | 250 | 3 | 0 | 0 |
| `qwen3:14b` | 1216 | 253 | **0** | 0 | 0 |
| `llama3.1:8b` | 1668 | 161 | 6 | 0 | 0 |

`granite4.2:8b`'s own v1 arm, the only within-study comparison: **1284 tok / 150 s, 13 unparseable,
3 trials lost** against v2's 1691 / 190 / 7 / 0. For that model the quote cost 32% more tokens and
27% more time and **halved** the parse-failure rate — the opposite of the expected robustness cost,
because v1's only free-text field (`where`) is vaguely specified and invites the deliberation that
breaks JSON, while v2's `quote` carries an explicit contract. Two of its v2 failures were leaked
deliberation on cells where the source itself is ambiguous (A9-4 item 3).

## 5. What the study does not show

One corpus per anchor, four models, one hardware profile. `granite4.2:8b`'s arms are graded over
different denominators. The improvement in the diamonds is consistent across three models but
rests on a single continuous outcome. The instrument's tabular blind spot is demonstrated, its
remedy is not: the v3 candidate — letting a tabular cell cite the table **row** with a declared
marker, and revisiting `surgery_type`'s definition — is registered in the ledger backlog and is
to be measured, never assumed.

## 6. Verdict against the pre-registered hypotheses

| | outcome |
|---|---|
| **H9.1** accuracy preserved | **holds for `gemma4:12b`** (+1 cell); fails for `qwen3:14b` (−19) and `llama3.1:8b` (−9), by omission, not by error |
| **H9.2** Chen class flagged or prevented | **prevented, not flagged**: N9-3 silent in all four models, and the type confusions that distorted the campaign's pool did not recur — but the net's silence cannot by itself distinguish prevention from blindness |
| **H9.3** ≤5% false flags | **fails in all four**, driven by the tabular blind spot rather than by model dishonesty |
| **H9.4** weak-model cost | measured and reported above; the cost is real in tokens and time, and **negative in robustness** for the one model with a within-study control |

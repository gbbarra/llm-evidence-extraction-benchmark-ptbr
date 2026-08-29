# EXTRAI — Study 3 analysis (verdicts and findings): "the pipeline"

Closed 2026-08-29. Full numbers in the [evaluation](avaliacao-estudo3.md); pre-registered protocol (+ Amendments 1–2) [here](protocolo-estudo3.md).

## Verdicts on the pre-registered hypotheses

| Hypothesis | Verdict |
|---|---|
| **H3.1** — extraction ≥95% at pipeline scale | **CONFIRMED**: 99/101 (98%), replicate 2 identical cell-for-cell; the 2 wrong cells share one root cause (dispersion pairing). |
| **H3.2** — audit sensitivity ≥75%, false alarms ≤10%; semantic > character-level | **CONFIRMED IN FULL**: 9/10 seeded cells caught (90%); false alarms 6.5%/5.9% per lane. Directional: all 4 semantic seeds (arm swaps, sign flips) caught with literal quotes; the only clean miss was the digit inside a CI string; the basal digit was flagged but mis-corrected. |
| **H3.3** — forced closure ⇒ 100% of CALC runs close | **CONFIRMED, without firing**: both lanes closed on their own (23/22 calls, 0 forced rounds). The Study-2 non-closure mode did not reappear under the pipeline's prompt structure; the safety net stayed unused. |
| **H3.4** — clean lane within ±0.02 of mechanical truth; anchor reproduced within rounding | **REFUTED as stated, decomposed in full**: model pool −0.39 vs same-sheets truth −0.52 (Δ0.13 — Goday's sign flip + a pool call fed dispersions inconsistent with the model's own per-study calls). The anchor half holds through the unperturbation lens: **−0.28 [−0.39, −0.17] vs published −0.24 [−0.32, −0.16]** — same direction and significance, residue = named route choices, not arithmetic. |
| **H3.5** — uncaught-seed damage ∝ IV weight | **CONFIRMED at small scale**: the surviving seed (a CI-bound digit on the *dominant* study) moved the truth pool by 0.02 by deflating Dorans's weight — proportional, as designed; the large deltas came not from seeds but from audit damage and assembly slips. |
| **H3.6** — anchor arithmetic audit | **STANDS from pre-registration**: 42/42 key cells validated; the anchor's derivation chains (CI/SE→SD, r=0.5 imputation, factorial margins) fully reverse-engineered; `pool_dl_md` reproduces the published diamond digit-for-digit at the startup gate. |
| **H3.7** — synthesis with numbers in hand | **CONFIRMED with one asterisk**: direction, magnitude, significance and I² all correct in both lanes, zero fabricated *statistics* — but both syntheses summed participants **by head and got it wrong** (479/494 vs true 542/558), and both landed 2–4 words under the 250 floor. |

## The six findings

1. **The pipeline works — and its residue is legible.** Seven trial reports went in; a forest plot came out whose unperturbed diamond (−0.28 [−0.39, −0.17]) sits beside the published one (−0.24 [−0.32, −0.16]) with every difference traceable by name: a twin-table route, an audit-damaged dispersion, an analyzed-vs-randomized convention. Nothing in the gap is arithmetic. On a mini-PC, in 4.5 hours, for zero cloud dollars.

2. **The audit is real — and it has a personality.** 90% of seeded cells caught; every *semantic* error (swapped arms, flipped signs) corrected with the literal quote; character-level digits are its blind spot. Its five signature behaviors (margin normalization, computed imputation, column-map inversion, unstable tie-breaking, cross-lane verdict instability) mean it functions as a second *reader*, not a diff tool — it repairs meaning, sometimes at the cost of the letter (the half-patient "24.5" written while citing "(n = 28)").

3. **Error propagates by weight, and the biggest damage wasn't the seeds.** The planted digit on the dominant study moved the pooled estimate by 0.02 — exactly the weight-proportional cost pre-registered. The audit's own false corrections on Chen (fabricated 37/38 split, swapped dispersions) and the model's Goday sign flip moved it by 0.13 — **the pipeline's quality gate did more arithmetic damage than the sabotage it was hired to catch.**

4. **Plausibility bias survives even the calculator.** Goday's perturbed control *worsened* (+0.3); the model computed with −0.3. It executed every call correctly and still refused the implausible sign. The same bias appeared in Study 1's Diaper direction slips: models normalize toward "treatment helps".

5. **Pooling is still the weak joint — now one level up.** Study 2: no model orchestrated the pool through the tool. Study 3: the pool *was* orchestrated — but fed a third set of dispersions inconsistent with the model's own per-study calls, made moments earlier in the same transcript. The failure climbed one level of abstraction: from "doesn't call" to "calls with unreconciled inputs". Assembly discipline, not arithmetic, remains the frontier.

6. **The by-head ghost closes the loop.** With every pooled number handed to it, the synthesis still summed participants mentally — and missed (479 and 494 against true 542/558). Three studies, one moral: any number a local model produces without the computation in sight is decoration, even inside a pipeline built to prevent exactly that.

## Instrument lessons (for Study 4+ and the method file)

Perturbation: extend the operator to number words ("Seventy-two"); never perturb totals whose addends stay visible; map twin analysis tables before choosing targets. Grading: parse CI bounds as the *last two* numbers (the judge read "IC95:"'s 95 as a bound; the model computed it right first); match study names by surname *and* year. The rite corrected the ruler three times in one study — the ruler is part of the experiment.

## Limitations

One pipeline configuration (one extractor, one auditor, one calculator — the measured winners); one anchor with a single continuous outcome; lanes of one replicate each (Stage E's two replicates measured stability; A/C/S ran once per lane); the audit's clean-lane value is measured against a nearly-clean extraction (98%), so its catch rate on genuine errors rests on 2 cells (1 half-caught). The end-to-end anchor comparison depends on the unperturbation map (sealed, now published with the grading).

## Next

Part 3 of the series (under the `relatorio-benchmark` skill). Deployment recipe, three studies combined: extract with gemma4:12b; audit with qwen3.8:27b but **treat its corrections as flags for source re-verification, never as auto-applied fixes** (finding 3); compute and pool through CALC with input echo (finding 5 asks the harness to echo each pool input against the per-study calls); synthesis receives totals precomputed (finding 6). The forced-closure net stays: it cost nothing and the failure mode it guards against is documented one study back.

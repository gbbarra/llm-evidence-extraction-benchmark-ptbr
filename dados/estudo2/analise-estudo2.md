# EXTRAI — Study 2 analysis (verdicts and findings): "the arithmetic"

Closed 2026-08-29. Full numbers in the [evaluation](avaliacao-estudo2.md); pre-registered protocol [here](protocolo-estudo2.md).

## Verdicts on the pre-registered hypotheses

| Hypothesis | Verdict |
|---|---|
| **H2.1** — arm B ≥ 2× arm A in exact hits | **CONFIRMED WITH ROOM** in the three models that closed arm B (12b: 1→6; 14b: 2→7; 27B: 3→8 = perfect). The fourth (26b) became the exception's case study: it uses the tool and never closes the answer. |
| **H2.2** — arm-A anatomy (direction yes, RR ~half, CI ~zero) | **CONFIRMED IN FULL.** Right direction in ~75–85% of points; 1–3 exact RRs per model; **95% CI: 0 exact in 30 attempts across the four models** — the in-head confidence interval is impossible for everyone. |
| **H2.3** — pooling is a different muscle, even with the tool | **CONFIRMED in the most revealing way**: zero CALC calls executed on pooling by any model. gemma12, gemma26 and qwen38 wrote the calls inside the final JSON as text (understood the what, not the how); qwen14 answered by head, wrong on 2 of 3 outcomes. *(Corrected 2026-08-29: the first version described qwen38 as by-head; the raw output shows calls-as-data.)* |
| **H2.4** — honesty (NC on CIs; fabrication <5%) | **PARTIAL.** NOT-COMPUTABLE appeared (2 legitimate refusals in A), but the models preferred to *attempt* the CI and fail rather than declare NC — the in-head CI came out statistic-shaped and wrong in 30/30. Strict fabrication (a number with no input basis) ≈ 0 in the main arms; "confident wrong arithmetic" is the dominant mode. |
| **H2.5** — the arithmetic ranking ≠ the extraction ranking | **CONFIRMED.** In arm A: 27B (3 exact) > 14b (2) > 12b = 26b (1) — the qwens rise, inverting the extraction table (12b=26b on top). In arm B the 27B closes perfect (8/8 + CI 8/8). Arithmetic aptitude belongs to the qwen family; form discipline to the gemma family. |
| **H2.6** — auditing the anchor | **CONFIRMED (with an elegant nuance).** The 11 published RR values (9 per-study + 2 pooled) are all correct. The pooled morbidity reproduces **digit-for-digit** under DerSimonian-Laird (0.778 [0.567–1.068], recomputed from the as-published cells) — but the caption calls it Mantel-Haenszel (which would give 0.873). A **method-label erratum**: right number, wrong name. *(Corrected 2026-08-29: an earlier ad-hoc recomputation printed 0.774/0.863; see the evaluation's correction note.)* |

## The five findings

1. **The calculator transforms the problem.** By head: 7 exact RRs in 30 points and no correct CI, across the four models combined. With the CALC protocol: qwen3.8:27b closes 8/8 points and 8/8 intervals — meta-analyst grade — and 12b/14b reach 6–7/8. The bottleneck is not conceptual: with arithmetic outsourced, the models know exactly what to compute with which numbers.

2. **The residual failure is workflow, not math.** Arm B's three failure modes are all *workflow*: not closing the answer after calling (gemma26 on rr), mistaking a call for data (gemma12, gemma26 and qwen38 on pool — the calls written inside the final JSON as text), and ignoring the tool for by-head numbers (qwen14 on pool). For production use this calls for a harness that forces closure — not a bigger model.

3. **The confidence interval is the sharp frontier of mental arithmetic.** 0/30. Not even the best model comes close to an in-head CI (log, root, exponential). Direction and order of magnitude, yes; inference, never. Any "in-head" CI in a local model's text should be treated as decoration.

4. **Honesty is asymmetric.** The models declare NC when *data* are missing, not when *capability* is: facing the CI, all of them tried and failed with confidence. "Knows what it doesn't know" works for the input, not for its own arithmetic limit.

5. **Thinking is half a calculator with a price and a ghost** (exploratory arm, qwen3:14b). On simple arithmetic, ~10k tokens of reasoning triples the exact hits (6/7 vs 2/8) — near tool grade. But the CI stays 0/7, the cost is 10–17×, and on pooling, 17 minutes of reasoning ended in perseveration: the same numbers cloned into four outcomes, two of them nonexistent in the input — the study's only fabrication. The calculator beats thinking on precision, cost and sanity.

## Limitations

One scored replicate per arm (the second measures stability); the CALC protocol is one particular tool implementation (native tool calling may differ); inputs inherit Study 1's extractions with perturbed cells (coherent by design — the truth is recomputed over the same input); pools were compared against the parseable set (model-declared subsets were rare). The thinking arm is exploratory (1 replicate, 1 model).

## Next

The A×B results feed Part 2 of the EXTRAI series. Deployment recipe suggested by E1+E2 combined: extraction by gemma4:12b (100% on the integrated GPU), arithmetic through the CALC protocol with any model that closes (27B if time allows, 14b if not), pooling ALWAYS through the tool — never through anyone's head, human or artificial.

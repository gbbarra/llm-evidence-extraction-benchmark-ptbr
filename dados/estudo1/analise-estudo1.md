# EXTRAI — Study 1 analysis (verdicts and findings)

Closed 2026-08-28, with **both strata** (open + Amendment 2's closed = **all 14 primaries of the meta-analysis**, 232 graded runs). Full numbers in the [evaluation](avaliacao-estudo1.md); anchor and adjudicator errors in [erratas-da-ancora.md](erratas-da-ancora.md).

## Verdicts on the pre-registered hypotheses

| Hypothesis | Prediction | Verdict |
|---|---|---|
| **H1.1** — rank inversion (27B ≥ 26b > 12b ≥ 14b on extraction) | the big faithful models win | **REFUTED.** Final 14/14 order: 12b (100%) > 26b (99%) > 27B (97%) > 14b (92%). Gemma discipline won extraction too. The real nuance favoring the big models: the 27B keeps the record for exact cells — it loses by *refusing* (and by a single arm swap in a mangled flowchart), not by inventing. |
| **H1.2** — zero recitations | reading, not memory | **CONFIRMED.** 0 attributable recitations in 228 runs (perturbed cells returned as read; a handful neutralized by harness leaks, Amendment 3). |
| **H1.3** — invention < 5%; omission > invention | inventing is rare | **CONFIRMED WITH ROOM.** Invention = 0% in all four. Omissions: 0–13 per model. |
| **H1.4** — RoB agreement between 60% and 90% | the human inter-reviewer band | **PARTIAL.** Gemmas inside (80%/79%); qwens below (62%/59%). The deviation concentrates in a single doctrinal domain (participant blinding: MA "Unclear" × models "High"). |
| **H1.5** — synthesis preserves direction where extractions are right | errors only downstream | **CONFIRMED.** All syntheses in range, compatible directions, zero orphan numbers (mechanical check) — in T3 and T3b. |
| **H1.6** — ≥1 disagreement adjudicated to the model | the benchmark finds human error | **CONFIRMED (repeatedly).** Yoon: arms swapped in the characteristics table (3 models flagged it; source confirms). Weinberg and Diaper: ASA "Not stated" that the articles report. Sun: oral-diet conversion contradicting its own source ("by 2 days"; 4 models unanimous). de Waal: ASA columns swapped (arithmetic proves it). |

## The six findings of Study 1

1. **Local models extract evidence at reviewer level — and above it in fidelity.** 624 decided cells over the 14 primaries: **one** wrong (an arm swap in a flowchart the PDF had scrambled), zero invented, zero recited. The remaining 17 losses are all omissions ("NR" where the source reports). On the same corpus, the published meta-analysis's human reviewers made the errors in the errata file: swapped arms, swapped ASA columns, data declared nonexistent that exists, a conversion contradicting its own source, phantom flatus cells, an Excel-corrupted cell, and a systematic pattern of using *analyzed* counts as *randomized* without a note (six studies).

2. **The "big models are the extractors" prediction fell.** The extraction task did not invert FIEL's ranking: the disciplined gemmas topped the board (100%/99%), the faithful 27B came 2–3 points behind (97%) and the 14b paid for its conservatism (92%). The gap between families is not correctness — it is **willingness to answer**: qwen says "NR" where gemma answers and gets it right.

3. **The models audited the meta-analysis — and the adjudicator.** Fifteen source-confirmed errata/divergence entries for the anchor (two raised by the models themselves), and **three adjudicator errata in the same rounds** (Redondo: abstract contradicts the primary's own body; Wu: rigid search windows hid data the models had extracted verbatim; Hokenek: a literal "40/40" nearly deducted). The ruler bent for no one — including the hand holding it.

4. **On risk of bias, the models are harsher than the reviewers.** Agreement collapses in a single domain: participant/personnel blinding (27%), where the MA judged "Unclear" and the models "High" — the literal Cochrane reading for an unblindable intervention. Doctrine, not inattention.

5. **Synthesis without a calculator is honest but myopic — and more evidence calibrates it.** No model fabricated an RR or CI; all described study-by-study with hedges. But without pooling, morbidity "looks favorable" (study-counting) where the pooled MA says "not significant" (RR 0.78, CI crossing 1). With 14 trials instead of 8 (T3b), three of four models moved to "inconsistent" on their own — approaching the pooled verdict with zero statistics. The remaining gap is exactly Study 2's question.

6. **The economics belong to the integrated GPU.** The 12b did whole blocks in ~2 hours and tied for the top. The 27B cost ~3.5× the time for 3 points less. For structured extraction, the small disciplined model on an integrated GPU is this table's cost-benefit optimum.

## Limitations

A single anchor meta-analysis, from a single journal — its errors do not generalize to the literature. Eight open + six legally obtained primaries; closed-stratum inputs are not redistributable (scripts regenerate everything locally). The adjudicator is the same assistant that built the harness — mitigated by the mandatory literal quote behind every decision and by its own three errata on public record. The corpus is text-only (figures and supplements out of reach: pending cells score against no one). Two perturbation leaks occurred and were neutralized symmetrically (Amendment 3). Syntheses were judged by the adjudicator, not by an independent human reviewer.

## Registered next steps

Study 2 "the arithmetic" (complete — see its own protocol/analysis). Study 3 sketch: the end-to-end pipeline, PDF to forest plot, with cross-model audit and seeded errors ([roadmap](../../roadmap.md)). Part 1 published on [LinkedIn](https://www.linkedin.com/pulse/extrai-part-1-i-made-four-local-models-redo-data-extraction-barra-dvfsf/).

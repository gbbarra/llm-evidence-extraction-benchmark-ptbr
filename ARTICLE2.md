# EXTRAI, part 2: no model got a single confidence interval right by head — then I handed them a calculator, and one closed the meta-analysis perfect

*Part 1 ended on a paradox: the four local models extract evidence almost without error, but conclude "by eye" — counting favorable studies where the pooled meta-analysis says "no significant difference". The missing question: can they do the math? Study 2 answered with two arms, from an idea by the benchmark's own author: first the models compute risk ratios, confidence intervals and pooled estimates **by head**; then they get a **calculator** they call through text. By head: zero correct confidence intervals in thirty attempts, across all four. With the calculator: one of them closed 8 of 8 points and 8 of 8 intervals. And the bonus arm, with thinking, produced the strangest scene of the series: seventeen minutes of reasoning ending in outcomes that do not exist.*

> 📄 EXTRAI series: [part 1](ARTICLE1.md) · part 2 (this one) · Data, protocols and mechanical grading: [github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr](https://github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr) · DOI: [10.5281/zenodo.22159050](https://doi.org/10.5281/zenodo.22159050) · Sister benchmark: [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr)

## The context, if you're just arriving

In part 1, the four models redid the data extraction of the 14 trials of a published meta-analysis ([Ashraf et al., Cureus, 2026](https://doi.org/10.7759/cureus.110243) — the whole benchmark's anchor) with one wrong cell in 624 — but their syntheses, lacking an aggregation tool, described a "favorable trend" where the pooled statistic says "not significant". Study 2 isolates the missing skill: **meta-analytic arithmetic**. Each model receives *its own extractions* from part 1 — **including the perturbed values it read**, by design coherence: the truth used in grading is recomputed over the same input, so the arithmetic test is fair and no number in Study 2 is a clinical result (the anchor audit, finding 6, is the exception: it used the real published values). From that input, the model computes, per trial and pooled: risk ratios (RR — the ratio between the outcome risk in the guided arm and in the control arm; below 1 favors the guided arm), mean differences (MD), 95% confidence intervals (95% CI — the range where the "true" estimate plausibly lives) and the fixed-effects (Mantel-Haenszel, "MH") and random-effects (DerSimonian-Laird, "DL") pooled estimates. Grading is 100% mechanical — each quantity's truth is the recomputation, by functions validated against the anchor's published values (the test case reproduces them exactly: RR 0.573; CI 0.372–0.884), over the input the model received. No language judge weighs in.

## What exactly was done

Two arms per model, two replicates, three task families (per-study RRs; mean differences; pooling) — 51 runs in 71 minutes. In arm A, by head, with the instruction that "NAO-CALCULAVEL" (not-computable) is a dignified answer, never guess. In arm B, the tool protocol is a line of text — the model writes the call, the harness (the program orchestrating the benchmark) executes it in Python and returns the result into the context, up to twenty calls:

```
CALC: rr(28, 39, 30, 36)
RESULTADO: 0.862
CALC: ic95_rr(28, 39, 30, 36)
RESULTADO: [0.674, 1.101]
```

Exploratory arm: qwen3:14b's thinking mode, the "mathematical vocation" FIEL never tested.

## What we found

### 1. The full proof, model by model — by head vs with the calculator

Before the scoreboards, the data that produce them: **each model's eight per-study quantities, with both arms side by side**. Each row's "truth" is recomputed over the numbers that model extracted in part 1 — which is why it varies slightly across models (different extractions and perturbations), and why the test is fair: each model is graded against its own numbers.

*How to read: each row is one per-study RR (outcome + trial). "truth" = mechanical recomputation over the model's own cells; A = by-head answer; B = with calculator. Labels: exact (±0.01), direction (right side of 1, wrong value), wrong, NC (declared NOT-COMPUTABLE).*

```
gemma4:12b            truth    by head (A)       CALC (B)
morb. Calvo-Vecino     0.504   0.515 direction   0.515 direction
morb. Yoon             0.862   0.931 direction   0.862 exact
morb. Diaper           0.966   1.085 wrong       0.966 exact
morb. Wu               0.594   0.473 direction   0.594 exact
mort. de Waal          0.942   0.926 direction   0.942 exact
mort. Sun              3.000   NC refusal        3.000 exact
ileus Arslan-Carlon    1.191   1.190 exact       1.026 direction
ileus Sun              0.125   0.250 direction   0.125 exact
```

```
qwen3:14b             truth    by head (A)       CALC (B)
morb. Calvo-Vecino     0.504   0.518 direction   0.523 direction
morb. Yoon             0.862   0.923 direction   0.862 exact
morb. Diaper           0.924   1.089 wrong       0.924 exact
morb. Wu               0.573   0.591 direction   0.573 exact
mort. de Waal          0.944   0.930 direction   0.944 exact
mort. Sun              3.000   0.063 wrong       3.000 exact
ileus Arslan-Carlon    1.026   1.028 exact       1.026 exact
ileus Sun              0.125   0.125 exact       0.125 exact
```

```
gemma4:26b            truth    by head (A)       CALC (B)
morb. Calvo-Vecino     0.504   0.518 direction   did not close —
morb. Yoon             0.862   0.921 direction   fired all 20
morb. Diaper           0.956   1.089 wrong       calls without
morb. Wu               0.594   0.473 direction   emitting the
mort. de Waal          0.849   0.930 direction   final JSON
mort. Sun              3.000   0.000 wrong       (finding 3)
ileus Arslan-Carlon    1.191   1.190 exact
ileus Sun              0.125   0.250 direction
```

```
qwen3.8:27b           truth    by head (A)       CALC (B)
morb. Calvo-Vecino     0.519   0.518 exact       0.519 exact
morb. Yoon             0.862   0.923 direction   0.862 exact
morb. Diaper           0.924   1.088 wrong       0.924 exact
morb. Wu               0.594   0.474 direction   0.594 exact
mort. de Waal          1.178   0.928 wrong       1.178 exact
mort. Sun              3.000   NC refusal        3.000 exact
ileus Arslan-Carlon    1.026   1.017 exact       1.026 exact
ileus Sun              0.125   0.124 exact       0.125 exact
```

Three readings come straight off the tables. **By head, the direction almost always, the number almost never**: 1–3 exact per model, the rest neighborhood. **With the calculator, the 27B closes 8/8** and the others only lose where they feed the *call the wrong input* — the 12b's two arm-B losses are wrong cells handed to the calculator (percentages instead of counts on Calvo-Vecino; 31 events instead of 36 on Arslan-Carlon): the right computation over the wrong number is still wrong. And the Diaper case teaches what "wrong" means by head: all four models answered ~1.09 (unfavorable to GDFT) where their own numbers give 0.92–0.97 — likely swapping arms in their heads, the same slip part 1 caught in a flowchart.

### 2. The confidence interval is the sharp frontier — 0 by head, near-perfect with the tool

The 95% CI requires chained logarithm, square root and exponential — mental arithmetic that does not exist here:

*How to read: exact CIs (both bounds within ±0.01) per arm; in B, gemma26 never closed its answer.*

```
model          95% CI by head (A)   95% CI with CALC (B)
gemma4:12b          0/7                  6/8
qwen3:14b           0/8                  7/8
gemma4:26b          0/8                  did not close
qwen3.8:27b         0/7                  8/8
TOTAL               0/30                21/24
```

What an in-head CI looks like from the inside — gemma4:12b, Yoon's morbidity: the model answered **RR 0.931 [0.549–1.611]**; the truth from its own numbers is **0.862 [0.674–1.101]**. Right side, right shape, decorative statistics. **Any "in-head" CI in a local model's text is decoration shaped like statistics.** The pre-registered hypothesis asked the tool to at least double the exact hits; it tripled to sextupled them.

### 3. The remaining failure is workflow, not math — three modes, each with literal proof

On pooling (combining the studies into a single RR — the step that demands orchestrating several calls), **no model completed the meta-analysis through the tool**. The three failure modes, from the raw outputs:

**Mode 1 — not closing.** gemma4:26b fired all 20 allowed calls and never emitted the final answer; its last round was still:

```
CALC: rr(19, 61, 32, 61)
CALC: ic95_rr(19, 61, 32, 61)
```

**Mode 2 — writing the call INSIDE the answer, as text.** Three models (gemma12, gemma26 and qwen38) delivered the final JSON with the call embedded as data — they understood the *what*, not the *how*. gemma12, literally (with a second error inside: **8.6 and 16.6 are percentages**, not event counts):

```json
{"morbidade": {"mh": "CALC: pool_rr_mh([[8.6, 224, 16.6, 226],
               [28, 39, 30, 36], [113, 198, 117, 198],
               [19, 61, 32, 61]])", …}}
```

**Mode 3 — ignoring the tool and guessing a number.** qwen3:14b answered the pooling by head (0 calls), wrong on 2 of the 3 outcomes — and its own JSON confesses the swapped input: `"estudos_usados": [[8.6, 224, 16.6, 226], …]` — percentages in place of events, again.

*(Correction, 2026-08-29: the first version described qwen38 on pooling as "answered by head"; the raw output shows mode 2 — calls written inside the JSON, like the gemmas. The evaluation in the repository carries the same note.)*

For production use, this calls for a harness that **forces closure** — not a bigger model. Which is exactly what Study 3 will do.

### 4. The ranking flipped — each family has its own muscle

*How to read: the extraction champion is not the arithmetic champion; compare the columns.*

```
model          extraction (part 1)   by-head math (A)
gemma4:12b         100%                  1 exact
gemma4:26b          99%                  1 exact
qwen3.8:27b         97%                  3 exact
qwen3:14b           92%                  2 exact
```

The form belongs to the gemmas; the arithmetic to the qwens — and neither ranking predicts the other. Anyone building a real pipeline should cast each stage the way you hire people: the meticulous one for the sheet, the numerical one for the math.

### 5. Thinking is half a calculator — with a ghost inside

*How to read: the same model, same by-head task, with and without extended reasoning (thinking) at a 12k-token budget (tokens are the text units a model processes — about ¾ of a word each).*

```
qwen3:14b, arm A       without thinking   with thinking (12k)
exact RR/MD                 2/8                6/7
exact 95% CIs               0/8                0/7
cost per run               ~1 min            5–17 min (10–17×)
```

At a 5,600-token budget, silent collapse — the reasoning consumes everything and the answer comes out empty (the exact echo of what FIEL's Series 1 saw in writing). At 12,000, it converges and nearly reaches the tool on simple arithmetic — but the CI stays impossible. And on pooling, after 17 minutes of thinking, came the scene — the final JSON, literally:

```json
{"morbidity":  {"fixed_effect":   {"rr": 0.768},
                "random_effects": {"rr": 0.741}},
 "mortality":  {"fixed_effect":   {"rr": 0.768},
                "random_effects": {"rr": 0.741}},
 "recurrence": {"fixed_effect":   {"rr": 0.768},
                "random_effects": {"rr": 0.741}},
 "symptoms":   {"fixed_effect":   {"rr": 0.768},
                "random_effects": {"rr": 0.741}}}
```

The same pair of numbers cloned across four outcomes — two of which ("recurrence", "symptoms") **do not exist in the input**. The only fabrication in all of Study 2 came from the arm that thought the most. The calculator beats thinking on precision, cost and sanity.

### 6. And the meta-analysis's own math? I recomputed all of it — auditable line by line

The same machinery audited the anchor, now over the **real published values** (the only part of the study touching actual clinical numbers). Every row can be redone on a hand calculator: RR = (events÷total)ᴳᴰᶠᵀ ÷ (events÷total)ᶜᵗˡ.

*How to read: events/total per arm as the MA published them (its tables 5, 6 and 11), the recomputed RR next to the published one.*

```
PER-STUDY RISK RATIOS — MA cells vs recomputation
study                GDFT     control  RR calc  RR publ
MORBIDITY (table 5)
Calvo-Vecino 2018    18/209   35/211    0.519    0.519  =
Yoon 2022            28/39    30/36     0.862    0.862  =
Diaper 2021         113/196  105/198    1.087    1.087  =
Wu 2017              19/58    32/56     0.573    0.573  =
MORTALITY (table 6)
de Waal 2021         10/248   10/234    0.944    0.944  =
Sun 2017              1/50     0/50     3.000    3.000  =
ILEUS (table 11; totals derived from the published %)
Arslan-Carlon 2020   36/142   30/141    1.192    1.19   =
Sun 2017              2/50    16/50     0.125    0.13   ~
Castro 2016           6/43    19/42     0.308    0.31   =
```

Nine of nine reproduce (Sun's "~" is a rounding coin-flip: 0.125 printed as 0.13; every remaining difference is ≤0.015, at the level of the totals' derivation). The 95% CIs likewise — all reproduce within the same tolerances ([per-study detail in the repository](dados/estudo2/avaliacao-estudo2.md)). **The pooled result is where the story turns:**

*How to read: one row per pooling recipe; compare each with the published row.*

```
POOLED MORBIDITY — right number, wrong name
                       RR      95% CI           I²
published (table 5)   0.778   [0.567, 1.068]     —   "MH"
recomputed DL         0.778   [0.567, 1.068]   76.3%  EXACT
recomputed MH         0.873   [0.758, 1.005]     —    differs

POOLED MORTALITY (table 6)
published             1.021   [0.446, 2.337]
recomputed DL         1.021   [0.446, 2.337]    0.0%  EXACT
```

The published pooled numbers are DerSimonian-Laird **digit for digit** — but table 5's caption names Mantel-Haenszel, whose recomputation gives a visibly different 0.873. The human reviewers' arithmetic stands absolved (part 1's errors were of *transcription*); what remains is a label erratum — entry 15 in the public file.

*(Correction, 2026-08-29: the first version of this finding printed an unreproducible ad-hoc recomputation — "DL 0.774 [0.566–1.059]" and "MH 0.863". Re-verified from the anchor's as-published cells with the same validated functions: the DL reproduction is exact, digit for digit, and the recomputed MH is 0.873. The finding gets stronger, not weaker; full note in the repository's Study-2 evaluation.)*

## What this means

The systematic-review pipeline on consumer hardware now has a stage-by-stage measured recipe: **extract with gemma4:12b on the integrated GPU** (100% in part 1), **compute through the CALC protocol** (the 27B closes perfect; the 14b nearly, in a fraction of the time), and **pool always through the tool — never through anyone's head, human or artificial**. And a critical-reading lesson that outlives the models: their honesty is asymmetric — they declare "not computable" when *data* are missing, never when *capability* is. Facing the CI, all of them tried and failed with confidence. Distrust any inferential statistic delivered without the computation in sight.

## Who did what

**The local models** computed (arm A) or wrote calls (arm B) — 51 runs. **The harness** executed the functions in Python (validated against the anchor: RR 0.573/CI 0.372–0.884 reproduced exactly), returned results into the context and ran the queue. **The mechanical grader** labeled every quantity by recomputing the truth over each model's own input — no language judge. **Claude (assistant)** designed the study with the author, wrote the harness and grader, and performed finding 6's anchor audit (mechanical recomputation; transcription checked). **The author** proposed the calculator idea, made the design decisions, and reviewed everything.

## Limitations

One scored replicate per arm (the second measures stability); the CALC protocol is one particular tool implementation — native tool calling may behave differently; the inputs inherit part 1's extractions (and perturbations) by design; the thinking arm is exploratory, one replicate, one model. The anchor audit covers the tables' arithmetic — not the data that fed them (that was part 1's subject).

*In part 3: the question both studies leave loaded — the whole pipeline, from PDF to forest plot, on a cloudless mini-PC, with one model auditing another and seeded errors measuring whether the audit is real. The queue decides.*

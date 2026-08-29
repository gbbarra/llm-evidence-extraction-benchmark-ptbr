# EXTRAI, part 2: no model got a single confidence interval right in its head — then I handed them a calculator, and one closed a perfect meta-analysis

*Part 1 ended on a paradox: the four local models extract evidence almost without error, yet conclude "by eye" — counting favorable studies where the pooled meta-analysis says "no significant difference". The missing question: can they do the math? Study 2 answered with two arms, on an idea from the benchmark's owner himself: first the models compute risk ratios, confidence intervals and pooled estimates **in their heads**; then they get a **calculator** they call through text. By head: zero correct confidence intervals in thirty attempts, across all four. With the calculator: one of them closed 8 of 8 point estimates and 8 of 8 intervals. And the bonus arm, with thinking, produced the strangest scene of the series: seventeen minutes of reasoning ending in outcomes that do not exist.*

> 📄 EXTRAI series: [part 1](ARTICLE1.md) · part 2 (this) · Data, protocols and mechanical grading: [github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr](https://github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr) · DOI: [10.5281/zenodo.22159050](https://doi.org/10.5281/zenodo.22159050) · Sibling benchmark: [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr)

## The context, if you are just arriving

In part 1, four local models redid the data extraction of a published meta-analysis's 14 trials with one wrong cell in 624 — but their syntheses, lacking any pooling tool, described a "favorable trend" where the pooled statistic says "not significant". Study 2 isolates the missing skill: **meta-analytic arithmetic**. Each model receives *its own extractions* from part 1 (faithful to what it read itself) and computes, per trial and pooled: risk ratios (RR — the ratio between the outcome's risk in the guided arm and in the control), mean differences (MD), 95% confidence intervals (CI), and the fixed-effect (Mantel-Haenszel, "MH") and random-effects (DerSimonian-Laird, "DL") pools. Grading is 100% mechanical — each quantity's truth is the recomputation, by functions validated against the anchor's published values (the test case reproduces them exactly: RR 0.573; CI 0.372–0.884), over the input the model was given. No language judge weighs in.

## What exactly was done

Two arms per model, two replicates, three task families (per-study RRs; mean differences; pooling) — 51 runs in 71 minutes. In arm A, by head, with the instruction that "NOT-COMPUTABLE" is a dignified answer, never a guess. In arm B, the tool protocol is one line of text — the model writes the call, the harness executes it in Python and returns the result into context, up to twenty calls:

```
CALC: rr(28, 39, 30, 36)
RESULTADO: 0.862
CALC: ic95_rr(28, 39, 30, 36)
RESULTADO: [0.674, 1.101]
```

Exploratory arm: qwen3:14b's thinking mode — the "mathematical vocation" FIEL never tested.

## What we found

### 1. By head: the direction yes, the number no — and the confidence interval never

| Model (arm A) | Points | Exact | Right direction | Wrong | Exact 95% CIs |
|---|---|---|---|---|---|
| qwen3.8:27b | 7 | 3 | 2 | 2 | **0/7** |
| qwen3:14b | 8 | 2 | 4 | 2 | **0/8** |
| gemma4:12b | 7 | 1 | 5 | 1 | **0/7** |
| gemma4:26b | 8 | 1 | 5 | 2 | **0/8** |

What "right direction, wrong value" looks like in real numbers — gemma4:12b, morbidity, by head:

| Study | Model answered | The truth (from its own numbers) |
|---|---|---|
| Yoon | RR 0.931 [0.549–1.611] | RR 0.862 [0.674–1.101] |
| Wu | RR 0.473 [0.252–0.893] | RR 0.594 [0.381–0.925] |

Right side of 1, right neighborhood — and not one reliable digit. **In-head 95% CIs: 0 exact in 30 attempts, across all four models.** It is the sharpest boundary this benchmark line has measured: mental logarithms, roots and exponentials do not exist here. Any "in-head" CI in a local model's output is decoration shaped like a statistic.

### 2. With the calculator, one model became a full meta-analyst

| Model (arm B) | Exact points | Exact 95% CIs | CALC calls |
|---|---|---|---|
| qwen3.8:27b | **8/8** | **8/8** | 32 |
| qwen3:14b | 7/8 | 7/8 | 36 |
| gemma4:12b | 6/8 | 6/8 | 36 |
| gemma4:26b | didn't close (see finding 3) | — | 40 |

qwen3.8:27b's first round, verbatim — clean planning, one pair of calls per study:

```
CALC: rr(18, 224, 35, 226)
CALC: ic95_rr(18, 224, 35, 226)
CALC: rr(28, 39, 30, 36)
CALC: ic95_rr(28, 39, 30, 36)
```

The pre-registered hypothesis asked the tool to at least double the exact hits; it tripled to sextupled them. With arithmetic outsourced, what remains is what the models truly have: knowing **what** to compute with **which** numbers.

### 3. The remaining failure is workflow, not mathematics — three failures, each with evidence

**The one that doesn't close**: gemma4:26b fired all 20 allowed calls and never emitted a final answer — its last round was still this:

```
CALC: rr(19, 61, 32, 61)
CALC: ic95_rr(19, 61, 32, 61)
```

**The ones that ignore the tool**: on pooling, qwen14 and qwen38 answered by head with the calculator available (0 calls) — and the input qwen14 claimed to have "pooled" shows the wound: `"estudos_usados": [[8.6, 224, 16.6, 226], …]` — **percentages in place of event counts**. **The one that mistakes a call for data**: the 26b wrote `"call": "CALC: pool_rr_mh([[…]])"` *inside* the JSON, as text — it understood what, not how. Aggregate result: **no model orchestrated a complete meta-analysis through the tool**. For deployment this calls for a harness that forces closure — not a bigger model.

### 4. The ranking flipped — each family has its own muscle

| | Extraction (part 1) | Head arithmetic (part 2) |
|---|---|---|
| gemma4:12b | **100%** | 1 exact |
| gemma4:26b | **99%** | 1 exact |
| qwen3.8:27b | 97% | **3 exact** |
| qwen3:14b | 92% | 2 exact |

The form belongs to the gemmas; the arithmetic to the qwens — and neither ranking predicts the other. Anyone building a real pipeline should cast each stage like hiring people: the meticulous one for the form, the numerate one for the math.

### 5. Thinking is half a calculator — with a ghost inside

| qwen3:14b, arm A | Without thinking | With thinking (12k tokens) |
|---|---|---|
| Exact RR/MD | 2/8 | **6/7** |
| Exact 95% CIs | 0/8 | **0/7** |
| Cost per run | ~1 min | 5–17 min (10–17×) |

At a 5,600-token budget: silent collapse — reasoning consumes everything and the answer comes out empty (the exact echo of what FIEL's Series 1 saw in writing). At 12,000 it converges and nearly reaches tool grade on simple arithmetic. But on pooling, after 17 minutes of reasoning, came the scene — the final JSON, verbatim:

```json
{"morbidity":  {"fixed_effect": {"rr": 0.768}, "random_effects": {"rr": 0.741}},
 "mortality":  {"fixed_effect": {"rr": 0.768}, "random_effects": {"rr": 0.741}},
 "recurrence": {"fixed_effect": {"rr": 0.768}, "random_effects": {"rr": 0.741}},
 "symptoms":   {"fixed_effect": {"rr": 0.768}, "random_effects": {"rr": 0.741}}}
```

The same pair of numbers cloned across four outcomes — two of which ("recurrence", "symptoms") **do not exist in its input**. The only fabrication in all of Study 2 came from the arm that thought hardest. The calculator beats thinking on precision, cost and sanity.

### 6. And the meta-analysis's own math? Nearly perfect — with one mislabeled method

The same grader audited the anchor:

| Quantity | Published | Recomputed | Verdict |
|---|---|---|---|
| Per-study RRs (11 cells, tables 5/6/11) | — | — | **11/11 correct** (±0.015) |
| Pooled morbidity | 0.778 [0.57–1.07] | DL: **0.774** [0.566–1.059] | right number… |
| …computed as | "Mantel-Haenszel" (caption) | MH would give **0.863** | **…wrong method name** |

The human reviewers' arithmetic stands absolved — part 1's errors were of *transcription*. But the pooled morbidity is an exact DerSimonian-Laird labeled Mantel-Haenszel: entry 15 in the public errata file.

## What this means

The systematic-review pipeline on consumer hardware now has a recipe measured stage by stage: **extract with gemma4:12b on the integrated GPU** (100% in part 1), **compute through the CALC protocol** (the 27B closes perfect; the 14b nearly, in a fraction of the time), and **pool always through the tool — never through anyone's head, human or artificial**. Plus a critical-reading lesson that outlives the models: their honesty is asymmetric — they declare "not computable" when *data* are missing, never when *capability* is. Facing the CI, every model tried and failed with confidence. Distrust any inferential statistic delivered without the calculation shown.

## Limitations

One scored replicate per arm (the second measures stability); the CALC protocol is one particular tool implementation — native tool calling may behave differently; inputs inherit part 1's extractions (and perturbations) by design; the thinking arm is exploratory, single-replicate, single-model. The anchor audit covers the tables' arithmetic — not the data that went into them (that was part 1's subject).

*In part 3: the question both studies leave loaded — the whole pipeline, PDF to forest plot, on a mini-PC with no cloud, with one model auditing another. The queue decides.*

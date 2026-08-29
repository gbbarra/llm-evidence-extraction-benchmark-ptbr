# EXTRAI, part 2: no model got a single confidence interval right in its head — then I handed them a calculator, and one closed a perfect meta-analysis

*Part 1 ended on a paradox: the four local models extract evidence almost without error, yet synthesize "by eye" — counting favorable studies where the pooled meta-analysis says "no significant difference". The missing question: can they do the math? Study 2 answered with a two-arm design suggested by the benchmark's owner himself: first the models compute risk ratios, confidence intervals and pooled estimates **in their heads**; then they get a **calculator** they can call through text. The bare-head result: zero correct confidence intervals in thirty attempts, across all four models. With the calculator: one of them closed 8 of 8 point estimates and 8 of 8 intervals — meta-analyst grade. And the bonus arm, with thinking enabled, produced the strangest scene of the series: seventeen minutes of reasoning ending in outcomes that do not exist.*

> 📄 Part 1: cell-by-cell extraction ([ARTICLE1](ARTICLE1.md)). Method, pre-registered protocols, mechanical grading and all data: [github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr](https://github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr) · DOI: [10.5281/zenodo.22159050](https://doi.org/10.5281/zenodo.22159050) · Sibling benchmark: [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr)

## The design, in one paragraph

Each model receives **its own extractions** from part 1 (faithful to what it read, perturbed values included) and computes, per trial: the risk ratio for morbidity, mortality and ileus; mean differences for gut-recovery times; and the pooled estimates, fixed-effect (Mantel-Haenszel) and random-effects (DerSimonian-Laird). In arm A, by head — with the explicit instruction that "NOT-COMPUTABLE" is a dignified answer, never a guess. In arm B, through a one-line tool protocol: the model writes `CALC: rr(19, 58, 32, 56)`, the harness runs it in Python and returns `RESULTADO: 0.573` into the context, up to twenty calls. Grading is 100% mechanical: each quantity's truth is the recomputation — by functions validated against the anchor meta-analysis's published values (the test case reproduces them exactly: RR 0.573; CI 0.372–0.884) — over the input the model was given. No language judge weighs in.

## The six findings

### 1. By head: the direction yes, the number no — and the confidence interval never

In arm A all four models got the **direction** of effect right in roughly 80% of points — they know which side of 1 the risk ratio falls on. But the exact value landed only 1 to 3 times per model, and the 95% confidence interval — which demands mental logarithms, square roots and exponentials — scored **zero exact in thirty attempts, across all four models**. It is the sharpest boundary this benchmark has measured: any "in-head" CI in a local model's output is decoration shaped like a statistic.

### 2. With the calculator, one model became a full meta-analyst

In arm B, qwen3.8:27b closed **8 of 8 point estimates and 8 of 8 intervals** — perfect; qwen3:14b, 7 of 8; gemma4:12b, 6 of 8. The pre-registered hypothesis asked the tool to at least double the exact hits; it tripled to sextupled them. With arithmetic outsourced, what remains is what the models truly have: knowing **what** to compute, with **which** numbers — and that they know.

### 3. The remaining failure is workflow, not mathematics

Arm B's three failures are all *workflow*, each with a name. gemma4:26b fired its full twenty allowed calls and **never emitted the final answer** — it uses the tool but doesn't close. On pooling, qwen14 and qwen38 **ignored the available calculator** and answered by head (wrong); and the 26b wrote the calls *inside* the JSON, as text — it understood what to call, not how. Aggregate result: **no model orchestrated a complete meta-analysis through the tool**. For deployment this calls for a harness that forces closure — not a bigger model.

### 4. The ranking flipped — each family has its own muscle

In part 1's extraction, the disciplined gemmas won (100% and 99%). In head-arithmetic, the **qwens** rise: the 27B with 3 exact, the 14b with 2, against 1 for each gemma. Arithmetic aptitude runs in the family — and neither task's ranking predicts the other's. Anyone building a real pipeline should cast each stage like hiring people: the form goes to the meticulous one, the math to the numerate one.

### 5. Thinking is half a calculator — with a ghost inside

The exploratory arm enabled qwen3:14b's thinking. At a 5,600-token budget: silent collapse — reasoning consumes everything, empty answer (the exact echo of what FIEL's Series 1 saw in writing). At 12,000 it converged — and on simple arithmetic scored **6 exact of 7**, nearly tool grade. But the CI stayed 0 of 7, each run cost 10 to 17× more… and on pooling came the scene: after 17 minutes of reasoning, the model delivered the same pair of numbers cloned across **four outcomes — two of which do not exist in its input** ("recurrence", "symptoms"). The only fabrication in the entire study came from the arm that thought hardest. The calculator beats thinking on precision, cost and sanity.

### 6. And the meta-analysis's own math? Nearly perfect — with one mislabeled method

The same grader audited the anchor: its **11 published per-study risk ratios are all correct** (which absolves the human reviewers' arithmetic — part 1's errors were of *transcription*). But the pooled morbidity RR (0.778) reproduces exactly under **DerSimonian-Laird** (recomputed: 0.774), while the table's caption describes it as **Mantel-Haenszel** — which would give 0.863. Right number, wrong method name: entry 15 in the anchor's public errata file.

## What this means

The full systematic-review pipeline on consumer hardware now has a recipe, measured stage by stage: **extract with gemma4:12b on the integrated GPU** (100% in part 1, minutes per paper), **compute through the CALC protocol** (the 27B closes perfect; the 14b nearly, in a fraction of the time), and **pool always through the tool — never through anyone's head, human or artificial**. Plus a critical-reading lesson that outlives the models: their honesty is asymmetric — they declare "not computable" when *data* are missing, never when *capability* is. Facing the CI, every model tried and failed with confidence. Distrust any inferential statistic a model (or a hurried human) delivers without showing the calculation.

## Limitations

One scored replicate per arm (the second measures stability); the CALC protocol is one particular tool implementation — native tool calling may behave differently; inputs inherit part 1's extractions (and perturbations) by design; the thinking arm is exploratory, single-replicate, single-model. And the anchor audit covers the tables' arithmetic — not the data that went into them (that was part 1's subject).

*In part 3: the question both studies leave loaded — can the whole pipeline run end to end, PDF to forest plot, on a mini-PC with no cloud, and deliver an auditable mini meta-analysis? The queue decides.*

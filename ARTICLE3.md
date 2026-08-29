# EXTRAI, part 3: I built a meta-analysis pipeline out of local AIs auditing each other — and the quality gate did more damage than the sabotage it was hired to catch

*In parts 1 and 2, four local models proved they can extract evidence almost without error and compute perfectly — as long as someone drives each step by hand. The production question remained: what if nobody drives? Study 3 wired the steps in series: one model extracts, another audits it field by field, the audited sheet feeds the calculator, the calculator feeds the synthesis, and a script draws the forest plot — seven clinical trials in, one meta-analysis out, on a mini-PC, no cloud. To measure whether the audit is real, I seeded eight deliberate errors into the sheets. The score: 9 of 10 sabotaged cells caught, with the literal quote as proof. But the propagation ledger held the study's irony: the undetected sabotage moved the final result by 0.02; the auditor's own false corrections — together with a sign the calculator flipped for being implausible — moved it by 0.13. And at the end, with the perturbations undone, the pipeline's diamond landed beside the published one: −0.28 against −0.24.*

> 📄 EXTRAI series: [part 1](ARTICLE1.md) · [part 2](ARTICLE2.md) · part 3 (this one) · Data, pre-registered protocols and mechanical grading: [github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr](https://github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr) · DOI: [10.5281/zenodo.22159050](https://doi.org/10.5281/zenodo.22159050) · Sister benchmark: [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr)

## The context, if you're just arriving

A meta-analysis — the study that combines several clinical trials into a single estimate — is made of three crafts: extracting the numbers from each paper, checking them, and aggregating them with statistics. Part 1 measured the first craft in isolation (624 cells, 1 error); part 2 measured the third (by head: not one confidence interval right in 30 attempts; with a calculator: one model closed perfect). Study 3 asks what happens when the crafts are chained **with no human in between** — each stage handed to the model that won the previous measurement, the way you cast a team from championship stats. And it adds the middle craft, never tested before: **one model auditing another's work**, field by field, against the original article.

Two design defenses, inherited from the series: the texts the models read are **perturbed** (numbers discreetly altered — returning the published value would expose training memory, not reading; the seven trials here are from 2016–2023, before the models' cutoff, and the perturbation turns any remembering into a detectable signal); and grading is **mechanical** — scripts compare cell by cell, and the human-assistant judge only arbitrates ties, obliged to quote the source. The judge, by the way, was corrected three times in this study. Again.

## What exactly was done

The anchor: **"Effect of Low-Carbohydrate Diets on Glycemic Control in Type 2 Diabetes Mellitus: A Systematic Review and Meta-Analysis of Randomized Controlled Trials"** ([Cureus, June 2026, open access CC BY](https://doi.org/10.7759/cureus.108479)) — a meta-analysis of 7 randomized trials (562 participants) on low-carbohydrate diets and glycated hemoglobin (HbA1c, the lab test that summarizes ~3 months of blood glucose) in type 2 diabetes. Published *after* the models' training cutoff. The usual note of fairness: the authors are not on trial — the anchor was chosen for being auditable (open, recent, complete forest plot), and its arithmetic came out of our verification **spotless**: all 42 answer-key cells reproduce digit for digit under the derivation rules we documented (intervals→SDs, standard errors→SDs, the Cochrane handbook's r=0.5 imputation).

The pipeline, each stage cast by its measured winner:

*How to read: stage, who runs it, why them, and the volume.*

```
stage            model          why                   runs
E  extraction    gemma4:12b     100% in part 1         7×2
A  audit         qwen3.8:27b    part-2 champion;      7×2 lanes
                                independent family
C  arithmetic    qwen3.8:27b    8/8+8/8 with CALC      2
S  synthesis     gemma4:26b     best long-form         2
F  forest plot   script (no model — deterministic)     2
```

**The two lanes**: the audit ran twice over the same sheets — lane **L** (clean, the extraction's real sheets) and lane **S** (seeded: 8 deliberate errors planted in 5 sheets — swapped arms, flipped signs, altered digits, transposed numbers — with 2 sheets left untouched as controls; the list was sealed BEFORE any run and the auditor was never told whether or how many errors existed). Whatever the auditor approves feeds the calculator — so an uncaught error **propagates**, and the pipeline measures its cost on the final result.

Full queue: 32 runs in 272 minutes on the mini-PC (Ryzen 7; integrated GPU for the 12b, CPU for the big ones). Grading 100% mechanical with a public ruler; adjudications with mandatory literal quotes; perturbation and seed seals published together with the grading.

## What we found

### 1. The whole pipeline works — and its residue has a first and last name

The clean lane's final product, study by study, beside what the meta-analysis published. MD is the mean difference in HbA1c change (negative favors the low-carb diet); the 95% CI is the uncertainty band; the pipeline's values live in the *perturbed* world (by design, input numbers were altered — per-study differences reflect that and route choices, never bad arithmetic).

*How to read: the MD [95% CI] the pipeline computed vs the anchor's published one.*

```
study           pipeline (lane L)        published (anchor)
Saslow 2017     -0.50 [-0.89, -0.11]     -0.50 [-0.89, -0.11]
Saslow 2023     -0.18 [-0.37, +0.01]     -0.21 [-0.40, -0.02]
Dorans 2022     -0.20 [-0.29, -0.11]     -0.22 [-0.31, -0.13]
Chen 2020       -0.43 [-0.78, -0.08]     -0.62 [-1.13, -0.11]
Thomsen 2022    -0.27 [-0.45, -0.09]     -0.17 [-0.35, +0.01]
Wang 2018       -0.32 [-0.87, +0.23]     -0.26 [-0.74, +0.22]
Goday 2016      -1.30 [-1.56, -1.04]     -0.50 [-0.90, -0.10]
```

And the diamonds — the random-effects pooled estimate (DerSimonian-Laird, "DL") that summarizes everything, with I² measuring heterogeneity (how much the trials disagree):

*How to read: four pooled results — what the model emitted, the mechanical truth over the SAME sheets, the pipeline with perturbations undone, and the published one.*

```
pooled                            MD      95% CI          I²
model (lane L)                   -0.39   [-0.60, -0.18]   76%
mechanical truth (same sheets)   -0.52   [-0.81, -0.22]   91%
pipeline UNPERTURBED             -0.28   [-0.39, -0.17]   32%
anchor as published              -0.24   [-0.32, -0.16]    6%
```

📊 *[IMAGE HERE: the pipeline's forest plot — squares/diamond = pipeline; grey dots = anchor as published. File: `forest-pipeline-L.png`; suggested caption: "The meta-analysis the pipeline produced, overlaid on the published one — Goday's outlier is the perturbation at work."]*

The line that matters is the third: reversing the sealed perturbations and pooling the audited sheets mechanically, the pipeline reaches **−0.28 [−0.39, −0.17]** where the meta-analysis published **−0.24 [−0.32, −0.16]** — same direction, same significance, overlapping intervals. And the residue decomposes entirely into named choices: Wang has *two* analysis tables and the pipeline read the twin (populations 24/25 vs 28/28); Chen carries audit-damaged dispersions (finding 4); analyzed n's differ from randomized ones. **Nothing in the gap is arithmetic.**

### 2. Extraction held the pipeline up: 98%, with identical replicates

*How to read: correct/graded cells per trial (replicate 1; replicate 2 came out IDENTICAL cell for cell — 100% stability). 🔒 = legally obtained outside open access.*

```
trial             cells     note
Saslow 2017        15/15    read the perturbed baselines 5.8/7.6
Saslow 2023 🔒      9/13*   factorial 2×2 identified; cell-ns
                            (23/25) vs margins — *4 cells
                            adjudicated as literal
Dorans 2022        13/13    read perturbed -0.24 and total 141
Chen 2020          13/17*   the study's ONLY 2 WRONG cells:
                            final-timepoint SDs pasted onto the
                            change (the true dispersion: the CI)
Thomsen 2022 🔒    15/15    read perturbed -0.56 and 8.09
Wang 2018          11/11    took the twin table — literal route
Goday 2016         17/17    left the change as NR (correct: the
                            text gives only baseline and final)
TOTAL              99/101 = 98% · 0 omissions · 0 recitations
```

Zero attributable recitations: on every valid target, the models returned the perturbed value — the one that exists only in the text they read. (The perturbation also took lessons for the manual: numbers **in words** survive the operator — "Seventy-two" stayed standing where the digit 72 became 63 — and totals with visible addends can't prove recitation. All documented as an amendment before the audit was graded.)

### 3. The audit is real — catches 9 of 10 — and has a personality

The eight seeds, one by one, against the auditor's verdict (it did not know whether errors existed):

*How to read: what was planted, and what the auditor did — "caught+fixed" requires the right value WITH a literal quote from the text.*

```
seed                        sheet         auditor's verdict
arm swap (change means)     Chen          CAUGHT+fixed (2/2,
                                          literal quotes)
arm swap (change means)     Thomsen       CAUGHT+fixed (2/2)
flipped sign (+0.32)        Saslow 2023   CAUGHT+fixed (-0.32)
flipped sign (+0.31)        Wang          CAUGHT+fixed (-0.31)
transposed n (73→37)        Dorans        CAUGHT (fixed to 75,
                                          accepted route)
transposed n (34→43)        Thomsen       CAUGHT+fixed (34)
digit in baseline (9.99)    Chen          caught, fixed WRONG
                                          (other arm's value)
digit INSIDE the CI (-0.37) Dorans        NOT CAUGHT (confirmed)
---
sabotaged cells caught: 9/10 (90%) · exact correction: 8/9
real false alarms: 6.5% (lane L) and 5.9% (lane S)
untouched control sheets: passed clean
```

The pre-registered directional prediction nailed it: **semantic errors (arms, signs) all fall, with literal proof; character-level errors slip through** — the digit hidden inside the interval string was the only one to sail past. And the auditor has five signature habits, all on literal record: it sums the factorial's cells to find the margins the meta-analysis used (brilliant); it **imputes values it computes instead of verifying** — going as far as correcting an n to **"24.5 patients" while citing, in its own verdict, the "(n = 28)"** that contradicts it; it inverts the column map of an ambiguous table (un-swapped Chen's seeded change means and, in the same gesture, swapped the arms' baselines); it breaks digit-vs-spelled-number ties one way here and the other way there; and it changes verdicts between lanes on the same cell.

### 4. The central irony: the gate did more damage than the sabotage

The propagation ledger, in hundredths of HbA1c on the final diamond:

*How to read: who moved the pooled estimate, and by how much.*

```
cause                                        effect on diamond
UNDETECTED seed (the CI digit on the          0.02
dominant study — inflates its standard
error and deflates Dorans's weight)
the auditor's FALSE corrections on Chen +     0.13
the calculator's flipped sign on Goday
(fabricated 37/38 split; arm-swapped
dispersions; -0.3 where it was +0.3)
```

The planted sabotage cost 0.02 — proportional to the study's weight, as hypothesized. The quality gate's own *spontaneous* failures cost six times more. For anyone building a real pipeline, the recipe changes shape: **the auditor's corrections are worth using as flags for source re-verification — never as auto-applied fixes.**

### 5. The head sneaks back in through the cracks — three times

Even with the calculator mandatory, part 2's "by head" reappeared through three different cracks. **First**: Goday's perturbed control *worsened* (+0.3 of HbA1c); the calculator model, with every function available, wrote −0.3 — the literal call:

```
CALC: md(-1.6, 0.46, 45, -0.3, 0.7, 40)
                         ^^^^
        the sheet's truth was +0.3 (control worsened);
        the model refused the implausible sign
```

**Second**: the pool was orchestrated through the tool (progress over part 2, where nobody managed it) — but fed a *third set* of dispersions, different from the ones the same model had just used in its own per-study calls:

```
Saslow 2017 in the per-study calls:  dp 0.42 / 0.43
Saslow 2017 in the pool call:        dp 0.9  / 1.2
```

Part 2's failure climbed one level of abstraction: from "doesn't call the tool" to "calls it with unreconciled inputs". **Third**: the syntheses, with every pooled number in hand, summed the participants *by head* — and got both sums wrong (479 and 494, against the sheets' true 542). Three studies, one moral: **a local model's number without the computation in sight is decoration — even inside a pipeline built to prevent exactly that.**

### 6. The judge fell three times — and the ruler is part of the experiment

The rite ("verify against the source before deducting") came for the adjudicator again. Three public corrections of the ruler: the answer key's first version lacked literal routes the models used (Saslow's "0% (0/8)", Dorans's "(n = 73)…(n = 69)", Thomsen's "CD 36, CRHP 36", Wang's entire twin table); surname-only name matching sent "Saslow 2023" to "Saslow 2017"'s ruler; and — the most instructive — the interval parser read the **"95" of "IC95:"** as a lower bound, producing truths of ±68 points… while **the model had computed the bounds correctly**. Third study in a row in which a local model gets it right before the judge does. The corrected ruler, every change dated, is in the repository — because in an honest benchmark, the ruler is a result too.

## What this means

Systematic review on consumer hardware moved from "each step works" to "the pipeline works": PDF in, forest plot out, 4.5 hours, zero cloud dollars, and a final residue that explains itself line by line. The recipe, measured across three studies: **extract with the disciplined one** (gemma4:12b), **audit with the numerical one** (qwen3.8:27b) *treating corrections as flags*, **compute and pool always through the tool** with the harness echoing the pool's inputs against the per-study calls, **hand the synthesis precomputed totals** — and keep the forced-closure net armed, even though in this queue it never fired. And the cross-cutting lesson, for humans too: the most dangerous link in an evidence pipeline is not the error somebody plants — it's the confident correction nobody checks.

## Who did what

**The local models**: gemma4:12b read the 7 perturbed texts and filled 14 sheets; qwen3.8:27b audited 14 sheets field by field and orchestrated the 2 pooled analyses through CALC; gemma4:26b wrote the 2 syntheses. **The harness** ran the queue, executed the calls in Python (functions validated against the anchor before launch: the published diamond reproduces digit for digit), planted the sealed seeds and assembled the audited sheets. **The mechanical grader** labeled every cell against the public ruler. **Claude (assistant)** designed the study with the author, source-verified the answer key (42/42), adjudicated with mandatory quotes — and logged its own three errata. **The author** legally hunted the closed PDFs, made the design decisions, and reviewed everything.

## Limitations

One pipeline configuration (one extractor, one auditor, one calculator — the measured winners; other casts may behave differently); one anchor with a single continuous outcome; one replicate per lane (extraction's two replicates measured stability; audit/arithmetic/synthesis ran once per lane). The auditor's catch rate on *genuine* errors rests on 2 cells (the extraction erred too little to test it at volume). The end-to-end anchor comparison depends on the unperturbation map — sealed before the runs and published with the grading.

*The EXTRAI series closes its first arc here: extraction (part 1), arithmetic (part 2), the pipeline (part 3) — protocols, data, errata and seals in the repository, DOI on the cover. What comes next — more casts, more anchors, other outcomes — the roadmap decides.*

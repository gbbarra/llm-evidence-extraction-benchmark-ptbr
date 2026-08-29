# EXTRAI, part 1: I made four local models redo a meta-analysis's data extraction — they found more errors in it than it found in them

*After fourteen parts of the FIEL benchmark measuring whether local models write faithful summaries, I decided to doubt my own verdict. Parts 13 and 14 said the big models were "extractors and auditors, not writers" — a phrase that had never been tested on the actual task. So a second benchmark was born: EXTRAI (Portuguese for "extract!"). The same four models, on a mini-PC, redoing cell by cell the extraction work of a published, peer-reviewed meta-analysis — all 14 of its clinical trials. The score: across 624 graded cells, the models got exactly one wrong. The published meta-analysis accumulated 15 errata entries. And the judge — me — was corrected three times by the models themselves.*

> 📄 EXTRAI series: part 1 (this) · [part 2](ARTICLE2.md) · Data, pre-registered protocols and errata: [github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr](https://github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr) · DOI: [10.5281/zenodo.22159050](https://doi.org/10.5281/zenodo.22159050) · Sibling benchmark: [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr)

## The context, if you are just arriving

EXTRAI is the second benchmark of a line that runs entirely on consumer hardware (Ryzen 7, integrated GPU, 32 GB RAM). The first, FIEL, measured faithful writing; this one measures **reviewer-grade reading**: given a clinical trial's full text, the model fills the same extraction form the human reviewers of a published meta-analysis filled — right numbers, from the right sections, admitting what the paper doesn't report. Three method choices attack FIEL's known weaknesses: (1) primary grading is **mechanical** — a script compares cell by cell, and the language judge only breaks ties, with a mandatory source quote; (2) the human answer key is **itself on trial** — every meta-analysis cell was verified against the original article, and when model and reviewers disagree, the source decides; (3) the articles the models read are **perturbed** — numbers quietly altered, so returning the published value exposes recitation, not reading.

## What exactly was done

The anchor: Ashraf N, Zargar OUU and Albina A, **"Comparison of Goal-Directed Fluid Therapy and Conventional Fluid Therapy in Elective Major Abdominal Surgery: A Meta-Analysis of Randomized Controlled Trials"** ([Cureus, June 2026, open access CC BY](https://doi.org/10.7759/cureus.110243)) — a meta-analysis of goal-directed fluid therapy (GDFT — steering surgical fluids by measured hemodynamic targets instead of fixed volumes), published — published *after* the models' training cutoffs), with 14 randomized trials. The 8 open-access ones came from Europe PMC; the 6 paywalled ones from my institutional access and legal author manuscripts — **the entire meta-analysis**. Each model read each trial and performed three tasks: the 30-field form (T1), risk of bias across the 7 Cochrane domains (T2), and a synthesis using only its own extractions (T3). Two replicates per task, 232 graded runs:

| Block | Compute | Runs | Time |
|---|---|---|---|
| gemma4:12b | integrated GPU (Vulkan) | 57 | ~2.2 h |
| qwen3:14b | integrated GPU (Vulkan) | 57 | ~1.7 h |
| gemma4:26b (MoE)* | CPU | 57 | ~2.0 h |
| qwen3.8:27b | CPU | 57 | ~7.1 h |

\* MoE = mixture-of-experts: of its 26 billion parameters, only ~4 billion are active per token — which is why the 26b is fast even on CPU.

## What we found

### 1. The scoreboard: evidence extraction is essentially solved on this hardware

156 gradable cells per model (the rest — unverifiable, pending, or absent from the input — count against no one). The corpus's two strata: **open** = the 8 open-access trials (Europe PMC); **closed** = the 6 paywalled ones, legally obtained through institutional access and author manuscripts — each stratum ran as its own queue, under the same rules:

| Model | Open stratum | Closed stratum | **Total** | Omissions | Wrong | Invented | Recited |
|---|---|---|---|---|---|---|---|
| gemma4:12b | 100% | 100% | **100%** (156/156) | 0 | 0 | 0 | 0 |
| gemma4:26b | 100% | 98% | **99%** (155/156) | 1 | 0 | 0 | 0 |
| qwen3.8:27b | 98% | 96% | **97%** (152/156) | 3 | 1 | 0 | 0 |
| qwen3:14b | 90% | 95% | **92%** (143/156) | 13 | 0 | 0 | 0 |

And the reading proof (the perturbed-number cells):

| Model | Read (returned the perturbed value) | Recited | Absent |
|---|---|---|---|
| gemma4:12b | 54 | 0 | 8 |
| gemma4:26b | 53 | 0 | 7 |
| qwen3.8:27b | 50 | 0 | 13 |
| qwen3:14b | 47 | 0 | 14 |

**Zero attributable recitations in 228 runs.** What that means in practice: Castro's perturbed text said the ASA II patients numbered 28 (the real, published value is 31 — ASA is the American Society of Anesthesiologists' scale grading a patient's physical status before surgery, from I, healthy, to IV, critically ill); every model that answered wrote "II: 28 (72%)" — the value that exists only in the text they were given. The single wrong cell of the entire study came from the 27B: it put one arm's value in the other arm's field while reading a flowchart the PDF extraction had scrambled ("…274 Assigned to PGDT group 259 Received…").

### 2. The central hypothesis fell — and the failure mode is refusal

The pre-registration (H1.1) bet on the big faithful models: 27B ≥ 26b > 12b ≥ 14b. The real order came out **12b > 26b > 27B > 14b** — the gemma family's discipline won extraction too. The anatomy of the losses proves the rest: of the 17 cells lost by all four models combined, **16 are omissions** — "NR" written where the source reports. Example: Castro's blood loss is verbatim in the source ("1100.1 ± 851.1"); qwen3:14b answered "NR". No model lied; some went silent.

### 3. The models audited the published meta-analysis — 15 errata entries, every one with a quote

Before the list, a note of fairness: transcription errors happen in any hand-made review — this benchmark's own judge logged three errata in the same round, and the point here is the process, not the authors. The [errata file](dados/estudo1/erratas-da-ancora.md) records each item with the deciding source snippet (in the table, "MA" is the anchor meta-analysis — the published review whose tables serve as the answer key; and each trial names its guided arm its own way: GDHT, PGDT, GDT — it is always the GDFT arm). The headliners:

| # | Study | What the MA published | What the source says |
|---|---|---|---|
| 1 | Yoon | arms GDFT 36 / control 39 | *"The GDHT group (n = 39)… the control group (n = 36)"* — *swapped* |
| 2 | de Waal | ASA(GDFT) 24:123:86:1 | arithmetic proves the inversion: 123 = 52.6% × 234 (the *control* arm) |
| 3 | Weinberg | ASA "Not stated" | *"ASA Class I-II 7 (27%)… ≥ III 19 (73%)"* — it's in the article's table |
| 4 | Diaper | ASA "Not stated" | *"ASA-PS classes III & IV 98 (50.0) 85 (42.9)"* — likewise |
| 5 | Diaper & Coeckelenbergh | flatus times (55±14 h etc.) | the word "flatus" **does not occur** in either text |
| 6 | Sun | oral diet 72±24 vs 96±30 h (a 1-day difference) | the text itself: *"shorten… by 2 days"* — all 4 models extracted 4.0/6.0 days, unanimously |
| 7 | Sujatha | ASA "95:105" and the cell *"2 days, 11:42:00"* | corrupted by Excel time formatting |
| 8 | 6 studies | the "n" column | uses *analyzed* as if *randomized*, with no note (Wu 61→58/56; Hokenek 40→39…) |

Item 1 was raised **by the models**: three of them independently extracted 39/36 against the published table — and the source confirmed them.

### 4. The models corrected the judge — three times

The benchmark's rite ("verify against the source before deducting") binds the adjudicator too. Three times I declared a model error, three times the source overruled me: on **Redondo**, I adjudicated from the abstract ("GDHT (n = 16)") without seeing that the flowchart and three tables say the opposite — the primary contradicts itself, and the MA was right; on **Wu**, my rigid search windows hid the line *"Number of patients using norepinephrine 15 (25.9) 24 (42.9)"* that the models had extracted verbatim — I briefly accused them of fabrication; on **Hokenek**, the "40/40" I was about to deduct is letter-for-letter in the source: *"randomised into two groups (control group: 40, PVI group: 40)"*. All three adjudicator errata are public, next to the meta-analysis's own.

### 5. On risk of bias, the models are harsher than the reviewers

Agreement with the published Cochrane judgments (7 domains × 13 studies — Weinberg has no risk-of-bias row in the MA, another inconsistency):

| Model | Agreement | Overall judgment equal | Stability r1=r2 |
|---|---|---|---|
| gemma4:12b | **80%** (73/91) | 5/13 | 97% |
| gemma4:26b | **79%** (69/87) | 6/13 | 95% |
| qwen3.8:27b | 62% (56/91) | 0/13 | 80% |
| qwen3:14b | 59% (54/91) | 4/13 | 97% |

By domain, the disagreement lives almost entirely in one place: **blinding of participants/personnel, 27%** (against 92% on selective reporting and 90% on sequence generation). The pattern is one-sided — the MA judged "Unclear", the models "High" — because the anesthesiologist executing a fluid algorithm cannot be blinded. Cochrane doctrine by the letter versus reviewer leniency: a disagreement of doctrine, not of reading.

### 6. The synthesis is honest but myopic — and more evidence calibrates it

The syntheses passed the mechanical anti-invention check: **zero orphan numbers** (every cited number exists in the model's own extractions). But with no pooling tool, the conclusion comes from study-counting — and it shifts when the evidence body grows:

| Model | Morbidity in the 8-study synthesis | In the 14-study synthesis |
|---|---|---|
| gemma4:12b | "inconsistent results" | "results are inconsistent" |
| qwen3:14b | "beneficial effect… five of eight trials" | "beneficial effect… though with inconsistencies" |
| gemma4:26b | "trend of benefit" | "the evidence is inconsistent" |
| qwen3.8:27b | "six of eight showing reduction" | "inconsistent and contradictory" |

With 14 studies, three of the four migrated to "inconsistent" — **approaching the meta-analysis's own pooled verdict (RR 0.78, CI crossing 1: not significant) with zero statistics**, just by seeing more contradiction. What's missing — the formal math — is part 2's subject.

## What this means

For systematic reviewers: structured extraction — the most tedious, error-prone stage of the process — runs on a mini-PC with no discrete GPU, with fidelity that on this corpus **exceeded the published reviewers'** — plus a structural advantage: the model cites *where* it found each datum, and a machine verifies. For the FIEL storyline: "big models = extractors" is dead; what survives is "disciplined models = everything, so far". And for anyone who reads meta-analyses: the errors this benchmark surfaced in a peer-reviewed review — swapped arms, inverted columns, mislabeled n's — are precisely the kind nobody re-checks after publication.

## Limitations

One meta-analysis, from one journal; its errors do not generalize to the literature. The adjudicator is the same assistant that built the harness — mitigated by a mandatory literal quote behind every decision, and by its own three errata on public record. The corpus is text-only: values living exclusively in figures or supplements were excluded from scoring (the "phantom flatus" may live there). Two-replicate runs measure stability, not significance.

*In part 2: I hand the models the meta-analysis formulas — risk ratio, confidence interval, pooling — first in their heads, then as a tool they can call. Spoiler: in their heads, none of the four got a single confidence interval right.*

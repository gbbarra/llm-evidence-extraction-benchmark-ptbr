# EXTRAI, part 1: I made four local models redo a meta-analysis's data extraction — they found more errors in it than it found in them

*After fourteen parts of the FIEL benchmark measuring whether local models write faithful summaries, I decided to doubt my own verdict. Parts 13 and 14 said the big models would be "extractors and auditors, not writers" — a sentence that had never been tested on the real task. So EXTRAI was born: the same four models, on a mini-PC, redoing cell by cell the extraction of a published, peer-reviewed meta-analysis — all 14 of its clinical trials, in full. The score: across 624 graded cells, the models got exactly one wrong. The audit of the published meta-analysis added up nine source-confirmed errata (in a public file of 15 entries). And the judge — me — was corrected three times by the models themselves.*

> 📄 EXTRAI series: part 1 (this one) · [part 2](ARTICLE2.md) · [part 3](ARTICLE3.md) · Data, pre-registered protocols and errata: [github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr](https://github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr) · DOI: [10.5281/zenodo.22159050](https://doi.org/10.5281/zenodo.22159050) · Sister benchmark: [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr)

## The context, if you're just arriving

EXTRAI is the second benchmark in a line that runs entirely on consumer hardware (Ryzen 7, integrated GPU, 32 GB of RAM). The first, FIEL, measured faithful writing; this one measures **reviewer-grade reading**: given the full text of a clinical trial, the model fills in the same extraction sheet that the human reviewers of a published meta-analysis filled in — the right numbers, from the right sections, admitting what the article does not report. Three method choices attack FIEL's known weaknesses: (1) primary grading is **mechanical** — a script compares cell by cell, and the language judge only arbitrates ties, with a mandatory quote from the source; (2) the human answer key is **also on trial** — every cell of the meta-analysis was verified against the original article, and when model and reviewers disagree, the source decides; (3) the articles the models read are **perturbed** — numbers discreetly altered, so that returning the published value exposes recitation rather than reading.

## What exactly was done

The anchor: Ashraf N, Zargar OUU and Albina A, **"Comparison of Goal-Directed Fluid Therapy and Conventional Fluid Therapy in Elective Major Abdominal Surgery: A Meta-Analysis of Randomized Controlled Trials"** ([Cureus, June 2026, open access CC BY](https://doi.org/10.7759/cureus.110243)) — a meta-analysis of goal-directed fluid therapy (GDFT: the strategy of giving surgical fluids guided by measured hemodynamic targets rather than fixed volumes), published *after* the models' training cutoff, with 14 randomized trials. The 8 open-access ones came from Europe PMC; the 6 paywalled ones from my institutional access and legal author manuscripts — **the entire meta-analysis**. Each model read each trial and performed three tasks: the 30-field extraction sheet (T1), risk of bias across the 7 Cochrane domains (T2), and a synthesis using only its own extractions (T3). Two replicates per task, 232 graded runs.

*How to read: one row per model; the "runs on" column says where it ran on the mini-PC.*

```
model         runs on                  runs      time
gemma4:12b    integrated GPU (Vulkan)    57      ~2.2 h
qwen3:14b     integrated GPU (Vulkan)    57      ~1.7 h
gemma4:26b*   CPU                        57      ~2.0 h
qwen3.8:27b   CPU                        57      ~7.1 h
```

\* MoE = mixture-of-experts: of the 26 billion parameters, only ~4 billion are active per token — which is why the 26b is fast even on CPU.

## What we found

### 1. The scoreboard: evidence extraction is practically solved on this hardware

156 gradable cells per model (the rest: no verifiable value, pending, or data absent from the input — they count against no one). The corpus's two strata: **open** = the 8 open-access trials (Europe PMC); **closed** = the 6 behind paywalls, legally obtained — each stratum ran as its own queue, under the same rules.

*How to read: correct/graded cells for each model in each of the 14 trials (first author's name; 🔒 = closed stratum). The last row sums everything.*

```
trial              gemma12  gemma26  qwen38   qwen14
Yoon                11/11    11/11    11/11     9/11
Sun                 22/22    22/22    22/22    21/22
Wu                  10/10    10/10    10/10     9/10
Castro              15/15    15/15    15/15    13/15
Redondo Calvo       10/10    10/10    10/10     8/10
Schmid               7/7      7/7      7/7      7/7
Weinberg            10/10    10/10     9/10     9/10
Sujatha             14/14    14/14    13/14    13/14
Diaper 🔒           11/11    11/11    11/11     9/11
de Waal 🔒           9/9      9/9      8/9      9/9
Arslan-Carlon 🔒    10/10    10/10     9/10     9/10
Calvo-Vecino 🔒      9/9      8/9      9/9      9/9
Coeckelenbergh 🔒   11/11    11/11    11/11    11/11
Hokenek 🔒           7/7      7/7      7/7      7/7
TOTAL              156/156  155/156  152/156  143/156
                    100%     99%      97%      92%
```

No wrong cells in the gemmas; the four models' single wrong cell belongs to qwen38 (the de Waal 8/9 row — the literal case appears in finding 2). Everything else lost was omission. And the reading proof — the cells whose numbers were perturbed in the text the model read:

*How to read: "read" = returned the perturbed value (which exists only in the text it read); "recited" = returned the original published value (which would indicate memory, not reading).*

```
model         read   recited   absent from answer
gemma4:12b     54       0            8
gemma4:26b     53       0            7
qwen3.8:27b    50       0           13
qwen3:14b     47        0           14
```

**Zero attributable recitations across 228 runs.** A concrete example: Castro's perturbed text said the ASA II patients numbered 28 (the real, published value is 31 — ASA is the American Society of Anesthesiologists scale grading a patient's physical status before surgery, from I, healthy, to IV, critically ill); the three models that answered wrote "II: 28 (72%)" — the value that exists only in the text they read.

### 2. The central hypothesis fell — and the failure mode is refusal

The pre-registration (H1.1) bet on the faithful big ones: 27B ≥ 26b > 12b ≥ 14b. The real order came out **12b > 26b > 27B > 14b** — gemma discipline won extraction too. And here is **every lost cell of the entire study**, all 18, one by one (the first version of this article counted "17, of which 16 omissions"; the full table corrects it: 18 — 17 omissions and 1 wrong):

*How to read: what the model answered vs what the source reports (the official answer key's source layer; in a perturbed cell, the expected value is the one in the perturbed text the model read).*

```
model    trial       field               model    the source reports
gemma26  Calvo-Vec.  laparoscopy ctl     (omitted) 109 (50.2%)
qwen38   Weinberg    inotrope use        NR       "used more
                                                  frequently" (GDT)
qwen38   Sujatha     total fluid GDFT    NR       crystalloids
                                                  1842|1715 ml
qwen38   de Waal ★   n randomized ctl    305      259 — the 305 is
         (the one                                 the perturbed
          WRONG)                                  GDFT-arm value
qwen38   Arslan-C.   inotrope use        NR       vasopressors
                                                  comparable
qwen14   Yoon        ASA GDFT arm        NR       4:29:6:0
qwen14   Yoon        ASA control arm     NR       2:27:7:0
qwen14   Sun         inotrope use        NR       18 (36%) vs
                                                  27 (54%)
qwen14   Wu          inotrope use        NR       norepi 15 vs 24;
                                                  phenyl. 12 vs 24
qwen14   Castro      blood loss GDFT     NR       1100.1 ± 851.1
qwen14   Castro      blood loss ctl      NR       1283.2 ± 959.7
qwen14   Redondo     ASA GDFT arm        NR       0:13:6:0
qwen14   Redondo     ASA control arm     NR       0:10:6:0
qwen14   Weinberg    inotrope use        NR       "used more
                                                  frequently" (GDT)
qwen14   Sujatha     crystalloid GDFT    NR       FloTrac 1842 |
                                                  PVI 1715 ml
qwen14   Diaper      ASA GDFT arm        NR       III-IV: 98 (50.0%)
qwen14   Diaper      ASA control arm     NR       III-IV: 85 (42.9%)
qwen14   Arslan-C.   inotrope use        NR       vasopressors
                                                  comparable
```

Seventeen of the eighteen are "NR" written where the source reports — no model lied; some went quiet. The single **wrong** one is instructive: in de Waal's flowchart, mangled by PDF extraction ("…274 Assigned to PGDT group 259 Received…"), the 27B put the GDFT arm's value (perturbed to 305) into the control arm's field. One arm swap in one scrambled text — out of 624 cells.

### 3. The models audited the published meta-analysis — an errata file with 15 entries

Before the list, a note of fairness: transcription errors happen in any hand-made review — the benchmark's own judge logged his own errata in the same round (they are IN the list, withdrawn and struck through, not hidden), and the point here is the process, not the authors. The [errata file](dados/estudo1/erratas-da-ancora.md) records each entry with the source passage that decides it; the table below mirrors the file, number by number. "MA" is the anchor meta-analysis — the published review whose tables serve as the answer key; each trial names its guided arm its own way (GDHT, PGDT, GDT — it is always the GDFT arm).

*How to read: the file's 15 entries, in their official numbering. Categories: ERRATUM = source-confirmed error; WITHDRAWN = an accusation of mine the source overturned (a judge's erratum, not the MA's); DIVERGENCE = an undeclared choice, not an error; PRIMARIES = a problem of the trials, not of the MA.*

```
#   trial(s)       category      what the source decides
1   Yoon           ERRATUM       MA: GDFT 36/ctl 39. Source:
                                 "GDHT group (n=39)… control
                                 (n=36)" — arms SWAPPED
2   Redondo Calvo  WITHDRAWN     I alleged swapped arms from
                                 the abstract alone; flowchart
                                 and 3 tables say the opposite
                                 — the MA was RIGHT (my error)
3   Weinberg       ERRATUM       MA: ASA "Not stated". Source:
                                 "ASA I-II 7 (27%)… ≥III 19
                                 (73%)" — it's in the table
4   Wu             WITHDRAWN     I alleged "Inotrope use" had
                                 no support; the source HAS it:
                                 "norepi… 15 (25.9) 24 (42.9)"
                                 — the models were right
5   Sujatha        ERRATUM       ASA "95:105" unsupported; cell
                                 corrupted by Excel time
                                 formatting ("2 days, 11:42:00")
6   Sujatha        DIVERGENCE    n=200/101 are ANALYZED; source
                                 randomized 102 per arm
                                 (undeclared choice)
7   Castro         DIVERGENCE    "bowel surgeries" label too
                                 narrow; source includes liver,
                                 gastric and pancreatic cases
8   Wu             DIVERGENCE    n 58/56 = analyzed; source:
                                 "61 patients… another 61"
9   Sun            ERRATUM       oral diet 72±24 vs 96±30 h
                                 (Δ 1 day) contradicts its own
                                 text: "by 2 days"; medians
                                 4.0/6.0 d — 4 models unanimous
10  de Waal        ERRATUM       ASA columns swapped between
                                 arms; arithmetic proves it:
                                 123 = 52.6% × 234 (the CONTROL)
11  Diaper         ERRATUM       ASA "Not stated" the source
                                 reports: "III & IV 98 (50.0)
                                 85 (42.9)"
12  Diaper &       ERRATUM       flatus times published; the
    Coeckelenbergh               word "flatus" DOES NOT EXIST
                                 in either full text
13  6 trials       ERRATUM       the "n" column mixes analyzed
                                 with randomized, undeclared
                                 (Wu 61→58/56; de Waal 274/259→
                                 248/234; Hokenek 40→39…)
14  Diaper, FEDORA PRIMARIES     internally contradictory
                                 trials (prose vs table;
                                 abstract vs methods)
15  (pooled)       ERRATUM       arithmetic — arrives in part
                                 2: right number, wrong method
                                 name
```

Net balance: **9 confirmed MA errata, 3 definitional divergences, 2 errata of the judge himself, and 1 problem of the primaries.** Entry 1 was raised **by the models**: three of them independently extracted 39/36 against the published table — and the source confirmed it.

### 4. The models corrected the judge — three times

The benchmark's rite ("verify against the source before deducting") applies to the adjudicator too. Three times I declared a model error, three times the source overruled me: on **Redondo**, I adjudicated from the abstract ("GDHT (n = 16)") without seeing that the flowchart and three tables say the opposite — the primary contradicts itself, and the MA was right; on **Wu**, my rigid search windows hid the line *"Number of patients using norepinephrine 15 (25.9) 24 (42.9)"* that the models had extracted literally — I went as far as accusing them of fabrication; on **Hokenek**, the "40/40" I was about to deduct is letter for letter in the source: *"randomised into two groups (control group: 40, PVI group: 40)"*. The adjudicator's three errata are public, right next to the meta-analysis's.

### 5. On risk of bias, the models are harsher than the reviewers

Agreement with the published Cochrane judgments (7 domains × 13 studies — Weinberg has no risk-of-bias row in the MA, another inconsistency):

*How to read: cell-by-cell agreement with the MA's table; "same global" = same overall risk verdict for the study; stability = the model's replicate 1 vs replicate 2.*

```
model         agreement       same global   stability
gemma4:12b    80% (73/91)        5/13          97%
gemma4:26b    79% (69/87)        6/13          95%
qwen3.8:27b   62% (56/91)        0/13          80%
qwen3:14b     59% (54/91)        4/13          97%
```

And the per-domain map — all four models combined — shows where the disagreement lives:

*How to read: the 4 models' agreement with the MA in each Cochrane domain (52 judgments = 13 studies × 4 models; two domains have fewer due to absent cells).*

```
Cochrane domain                     agreement
selective reporting                  92% (48/52)
random sequence generation           90% (47/52)
allocation concealment               77% (40/52)
incomplete outcome data              76% (37/49)
blinding of outcome assessors        65% (33/51)
other biases                         63% (33/52)
blinding of participants/personnel   27% (14/52)  ←
```

The disagreement lives almost entirely in one place: **blinding of participants and personnel, 27%**. The pattern is one-sided — the MA judged "Unclear" and the models, "High" — because the anesthesiologist executing the fluid algorithm cannot be blinded. Cochrane rule by the letter against reviewer leniency: a doctrine divergence, not a reading one.

### 6. The synthesis is honest but myopic — and more evidence calibrates it

The syntheses passed the mechanical anti-invention check: **zero orphan numbers** (every number cited exists in the model's own extractions). But without an aggregation tool, the conclusion comes from counting studies — and it changes when the evidence body grows:

*How to read: how each model described morbidity (postoperative complications) when synthesizing 8 studies vs 14 studies — literal phrases from the syntheses.*

```
model         with 8 studies           with 14 studies
gemma4:12b    "inconsistent            "results are
              results"                 inconsistent"
qwen3:14b     "beneficial effect…      "beneficial effect…
              five of the eight"       though with
                                       inconsistencies"
gemma4:26b    "trend toward            "evidence is
              benefit"                 inconsistent"
qwen3.8:27b   "six of the eight        "inconsistent and
              with reduction"          contradictory"
```

With 14 studies, three of the four migrated to "inconsistent" — **approaching the meta-analysis's own pooled verdict (RR 0.78, CI crossing 1: not significant) with no statistics at all**, just by seeing more contradiction. What's missing — the formal computation — is part 2's subject.

## What this means

For anyone doing systematic reviews: structured extraction, the most tedious and error-prone step of the process, runs on a mini-PC with no dedicated GPU at a fidelity that, in this corpus, **beat the published reviewers'** — with one structural advantage: the model cites *where* it found each datum, and the machine checks. For the FIEL line: "big = extractors" died; what survives is "disciplined = everything, for now". And for anyone who reads meta-analyses: the errors this benchmark found in a peer-reviewed review — swapped arms, inverted columns, mislabeled n's — are exactly the ones nobody checks after publication.

## Who did what

**The local models** (gemma4:12b, qwen3:14b, gemma4:26b, qwen3.8:27b, via Ollama on the mini-PC) read the 14 perturbed texts and filled in sheets, bias judgments and syntheses — 232 runs. **The harness and scripts** (public in the repository) built the prompts, ran the queues, compared cell by cell against the answer key and tallied the scoreboards — all primary grading is mechanical. **Claude (assistant, Anthropic)** designed the benchmark with the author, built the source-verified official answer key (with a literal quote per decision), adjudicated ties under the public rite — and logged its own three errata. **The author** made the design decisions, legally hunted the 6 closed PDFs, and reviewed everything.

## Limitations

A single meta-analysis, from a single journal; its errors do not generalize to the literature. The adjudicator is the same assistant that built the harness — mitigated by the mandatory literal quote on every decision and by its own three errata on public record. The corpus is text only: values living exclusively in figures or supplements stayed out of scoring (the "phantom flatus" may live there). Two-run replicates measure stability, not significance.

*In part 2: I hand the models the meta-analysis's formulas — risk ratio, confidence interval, pooling — first by head, then as a tool they can call. Spoiler: by head, none of the four got a single confidence interval right.*

# EXTRAI, part 1: I made four local models redo a meta-analysis's data extraction — they found more errors in it than it found in them

*After fourteen parts of the FIEL benchmark measuring whether local models write faithful summaries, I decided to doubt my own verdict. Parts 13 and 14 said the big models were "extractors and auditors, not writers" — a nice phrase that had never been tested on the actual task. So a second benchmark was born: EXTRAI (Portuguese for "extract!"). The same four models, running on a mini-PC, redoing cell by cell the extraction work of a published, peer-reviewed meta-analysis — all 14 of its clinical trials. The final score: across 624 graded cells, the models got exactly one wrong. Along the way they found swapped arms, inverted columns and phantom data in the published meta-analysis — and corrected me three times.*

> 📄 EXTRAI is the sibling of [FIEL](https://github.com/gbbarra/llm-summarization-benchmark-ptbr) (14 parts on faithful summarization). Method, pre-registered protocol, source-verified answer key, errata files and all data: [github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr](https://github.com/gbbarra/llm-evidence-extraction-benchmark-ptbr)

## The design, in one paragraph

An anchor meta-analysis on goal-directed fluid therapy (Cureus, June 2026 — published *after* the models' training cutoffs) supplies both the task and the answer key: the tables two human reviewers extracted from 14 randomized controlled trials. Each model receives each trial's full text plus a 30-field extraction form (patients per arm, fluids, complications, mortality, gut function…), then judges risk of bias across the 7 Cochrane domains, and finally writes a synthesis using only its own extractions. Three rigor tricks: the articles the models read are **perturbed** (numbers quietly altered — returning the published value proves recitation, not reading); primary grading is **mechanical** (a script compares cell by cell; the language judge only breaks ties, with a mandatory source quote); and the human answer key is **itself on trial** — when model and reviewers disagree, the original article decides.

## What exactly was measured

Four FIEL veterans — gemma4:12b and qwen3:14b on an integrated GPU, gemma4:26b (MoE) and qwen3.8:27b on CPU — across all 14 trials of the meta-analysis: 8 open access plus, thanks to the author's institutional access, the 6 paywalled ones. 228 runs, two replicates per task, an 8.3-hour queue for the open stratum and 5.9 for the closed one, all on a Ryzen 7 with 32 GB of RAM. No cell was left undecided: 156 gradable cells per model, every decision public with the source snippet that supports it.

## The six findings

### 1. Evidence extraction is essentially solved on consumer hardware

The scoreboard: **gemma4:12b 100%, gemma4:26b 99%, qwen3.8:27b 97%, qwen3:14b 92%**. Across the four models' 624 decided cells there was **one** wrong cell (an arm mix-up while reading a flowchart the PDF extraction had scrambled), **zero invented values** and **zero recitations**: in the 124 perturbed-number cells the models cited, they returned the value from the text they were given — never the published value they could have memorized.

### 2. The central hypothesis fell — and the failure mode is refusal

The pre-registration bet that the big, faithful models would win extraction. Wrong: the gemma family's discipline won again, and the small 12b — which does the job on an integrated GPU in a fraction of the time — tied at the top with a perfect score. The 27B keeps the record for *exact* cells and loses for a different reason: it **refuses**. The entire gap between 100% and 92% is made of "not reported" written where the source reports. No model lies; some go silent.

### 3. The models audited the published meta-analysis — and found 14 problems

The benchmark's errata file lists, with quotes: the Yoon trial's arms **swapped** in the characteristics table (three models flagged it independently; the source says "GDHT group (n = 39)"); de Waal's ASA columns **inverted** (arithmetic proves it: 123 = 52.6% × 234 — the control arm); two studies whose ASA was declared "Not stated" while their tables **report it**; flatus times published for two articles that **do not contain the word flatus**; an hours conversion that contradicts its own source text ("by 2 days"); a cell corrupted by Excel time formatting ("2 days, 11:42:00" where an ASA ratio should be); and a systematic pattern — in **six** of the 14 studies, the meta-analysis's "n" column uses *analyzed* patients as if they were *randomized*, with no methods note.

### 4. The models corrected the judge — three times

The benchmark's rite ("verify against the source before deducting") applies to everyone, including me, the adjudicator. Three times I declared a model error and three times the source overruled me: on Redondo, I adjudicated from the abstract without seeing that the article's body says the opposite four times; on Wu, my rigid search windows hid a vasoactive-drugs table the models had extracted verbatim; on Hokenek, the "40/40" I was about to deduct was written letter for letter in the source. All three adjudicator errata are on public record, right next to the meta-analysis's own.

### 5. On risk of bias, the models are harsher than the reviewers

Agreement with the reviewers' Cochrane judgments: gemma4:12b 80%, gemma4:26b 79%, the qwens ~60%. Nearly all the divergence lives in a single domain: blinding of participants and personnel, where agreement drops to 27% — the meta-analysis judged "Unclear" while the models said "High", because the anesthesiologist executing a fluid algorithm cannot be blinded. Cochrane doctrine applied literally, against reviewer leniency: a disagreement of doctrine, not of reading.

### 6. Synthesis without a calculator is honest but myopic

The final syntheses respected the word limit and — mechanically checked — **contain not a single number absent from the model's own extractions**. No fabricated risk ratio, no invented confidence interval. But with no pooling tool, every model describes morbidity as "favoring GDFT" by counting studies, while the pooled meta-analysis says "no significant difference" (RR 0.78, CI crossing 1). That exact gap — knowing how to extract without knowing how to add — is Study 2's question.

## What this means

For the systematic-review workflow: structured extraction — the most tedious, error-prone part of the process — now runs on a mini-PC with no discrete GPU, with fidelity that on this corpus exceeded the published reviewers' — plus a structural advantage: the model cites *where* it found each datum, and a machine verifies. For the FIEL storyline: "big models = extractors" is dead; what survives is "disciplined models = everything, so far". And for reading meta-analyses in general: the errors this benchmark surfaced in a peer-reviewed review — swapped arms, inverted columns, mislabeled n's — are precisely the kind nobody re-checks after publication.

## Limitations

One meta-analysis, from one journal; its errors do not generalize to the literature. The adjudicator is the same assistant that built the harness — mitigated by a mandatory literal quote behind every decision, and by its own three errata on record. The corpus is text-only: values living exclusively in figures or supplements were excluded from scoring (the "phantom flatus" may live there). And two-replicate runs measure stability, not significance.

*In part 2: I hand the models the meta-analysis formulas — risk ratio, confidence interval, pooling — first in their heads, then as tools they can call. If extraction is solved, is arithmetic?*

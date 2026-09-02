# Study 9 — are the v2 quotes self-sufficient? An editorial reading of `gemma4:12b`'s Anchor-1 arm

**Recorded 2026-09-02, at the author's request**, over the completed v2 arm of `gemma4:12b`
(42 sheets, 175.1 min). Produced by `scripts/estudo9/e9-suficiencia.py`; per-cell data in
`suficiencia-gemma12.json`. This is an **adjudication-layer reading**, not a mechanical net:
the counts are mechanical, the verdicts on each residue were made with the cell, its quote
and the source-verified key side by side, under the quotation rite.

## The question

The v2 schema's promise is that **the sheet carries its own evidence**: a reviewer should be
able to look at `{value, where, quote}` and decide whether the value is right *without opening
the article*. N9-1 asks whether the quote exists in the source and N9-2 whether the value
occurs in the quote; neither asks the editorial question — **would the quote let a human
adjudicate?**

## What was measured

Over the key's 124 eligible Anchor-1 cells, with the campaign's frozen comparator and the
lens held constant across arms (amendment A9-2):

| | |
|---|---|
| Cells agreeing with the source-verified key | **104/124 (83.9%)** — v1 record: 103/124 |
| Cells filled with `NR` (quote empty by instrument design) | 19 |
| Cells with a value whose quote lets the value be checked | **89 of 105 (85%)** |

| | quote checks the value | quote does not |
|---|---|---|
| **agrees with key** | 80 | 5 |
| **diverges from key** | **9** | 11 |

**Accuracy is preserved** (+1 cell against the archived v1 record, inside replicate-level
variance): H9.1 holds for this model. The quote costs nothing in correctness.

## The finding: the quote convicts the sheet where it matters

Of the 20 divergences, **9 carry a quote that adjudicates them**, and four more are
*self-contradictory* — the quote disagrees with the value beside it. So **13 of 20 divergences
are decidable from the sheet alone**, which no v1 sheet could offer.

Two are exemplary, in that the quote does not merely convict the cell but **explains the
choice**:

- **de Waal, `n_randomized_gdft`** — wrote `259`, quoted *"Assigned to PGDT group (n = 305) …
  Received allocated intervention (n = 259)"*. The reader sees at once that the model took the
  received-intervention layer rather than the randomized one. The population-layer choice that
  the campaign could only infer is here stated by the sheet.
- **FEDORA, `n_randomized_gdft`/`_control`** — wrote `224`/`226`, quoted *"450 patients were
  randomized to the GDHT group (n=224) or control group (n=226)"*. Same class, same clarity:
  the key carries the analysis set, the model quoted the allocation sentence.

Self-contradiction, the second useful mode:

- **de Waal, `asa_gdft`** — value `6.9% (ASA II)`, own quote `ASA II 144 (53.2%)`.
- **Weinberg, `asa_*`** — value `1-2 (70%), ≥3 (30%)`, own quote `ASA Class I-II 7 (27%),
  ASA Class ≥ III 19 (73%)` — the percentages are inverted relative to the quote the model
  itself pasted.

A reviewer catches both in seconds, with no source at hand.

## Where the schema underdelivers, and why

**Sixteen cells have a value the quote does not support. Eleven of them are two field types.**

- **`surgery_type` (6 cells)** — the quote is the eligibility sentence or the study aim
  (*"scheduled for major abdominal, urological or vascular surgery"*), while the key transcribes
  the enumerated case mix. The quote supports a *category*, not a count. The field asks for
  something the prose does not state in citable form.
- **`asa_*` (4 cells)** — a multi-category table row. One quote was truncated at the header
  (`"ASA classification, n (%) 1 2 3"` — the row labels without the numbers), the 240-character
  budget having been spent on the table's scaffolding.

**Diagnosis, and it repeats the granite finding.** The instrument's rule — *"the verbatim
sentence or fragment containing the value"* — presupposes prose. Half a meta-analysis sheet is
table, where a cell's "sentence" does not exist: a table row linearizes into something that is
not contiguous text. `granite4.2:8b` responded by *stitching* fragments across gaps (73% of its
N9-1 residue); `gemma4:12b` responds by quoting the row scaffolding or an adjacent sentence.
**Two models, two different symptoms of one instrument gap.**

## Consequence for the harness (backlog, never retroactive)

Candidate for a future instrument version, to be measured and not assumed, exactly as v2 was:

- **Let tabular cells cite the table row instead of a sentence**, with a declared marker saying
  the provenance is a row rather than a sentence — so `quote-exists` can check row membership
  instead of contiguity, and the 240-character budget is spent on data rather than scaffolding.
- **Reconsider `surgery_type`'s definition** or accept category-level provenance for it
  explicitly, rather than scoring it against an enumeration the source never states as such.

Both would be a v3, registered before any run and A/B'd against v2 on the same corpus, seals
and graders — the same discipline that produced this finding.

## Note on the instrument that produced this analysis

The first version of `e9-suficiencia.py` treated the hyphen in a printed range (`1474-2600`) as
a minus sign, so it searched the quote for `-2600` and declared perfectly good provenance
unsupported; it undercounted checkable cells as 77 instead of 89. Caught by reading the residue
before reporting it, and fixed in the committed script. Recorded here for the same reason the
project records its other self-corrections: the tool that measures is on trial with everything else.

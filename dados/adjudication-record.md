# The containment instrument: raw-data index of the adjudication layer

**Created 2026-09-01.** The manuscript states that the human--AI adjudication layer is constrained by the quotation rite ("no cell changes category without the source quotation that decides it") and that its reversals, corrections and flag resolutions are on record. This file is the consolidated index of that raw record --- every entry below is a committed file in this repository, with the git history as the immutable, dated trail.

## 1. The quotation substrate (per-cell deciding quotes)

- **`estudo1/gabarito-oficial.json`** — the Anchor-1 two-layer key: 392 cells, **155 carrying the literal source quotation** (`cit`) alongside the verdict (`veredito`) and source value (`valor_fonte`). Every grading decision traces to these fields.
- **`estudo3/gabarito-fonte.json`** — the Anchor-2 two-layer key: per-quantity `cit` quotations, provenance (`literal`/`derivada`) and, for derived values, the arithmetic (`regra`, `conta`) shown in full.

## 2. Judge reversals and withdrawn accusations (the rite catching the judge)

- **`estudo1/erratas-da-ancora.md`** — the public errata file. Items **2** and **4** are the adjudicator's own withdrawn accusations, kept struck-through with the quotations that overturned them: Redondo (arms declared swapped from a single abstract passage; the body says the opposite in four quoted places) and Wu (models accused of fabricating inotrope values that the primary's Table 3 prints — "the three models … were literally right"). The file's header records who raised and who confirmed each item.
- Development-phase instrument/grader errata, each transcript-proven and amended in place: **`estudo4/protocolo-estudo4.md`** (E4-1…E4-4, including the leading trigger question and the engine/grader parser divergence — "twice the models computed correctly before the judge's parser did") and **`estudo5/protocolo-estudo5.md`** (harness errata E5-1…E5-5, including nets that steered correct values into corruption).

## 3. The campaign-era judge episode (Chen), end to end

- **Original charge**: commit `b6e5a0d` — `estudo7/avaliacao-estudo7.md` first stated the model *computed* the CI half-width and misdeclared it as an SD.
- **Refutation (mechanical)**: **`estudo7/redes-deteccao.md`** + `redes-deteccao.json` — the detection-net run whose text search found the value **printed verbatim** in the primary's prose ("the HbA1c (−1.6±0.3 vs. −1.0±0.3%)"), with both printed layers quoted.
- **Correction on record**: commit `ad7c457` — the dated correction note now inside the anatomy section of `estudo7/avaliacao-estudo7.md` ("Correction, 2026-09-01: … the charge is corrected"), plus the amendment section in `estudo7/protocolo-estudo7.md` recording A7-H1's informative failure.

## 4. Flag resolutions (each flag → a quotation-bound verdict)

- **`estudo8/avaliacao-p1.md`** — the five recitation candidates of P1, each adjudicated against the perturbed source with the deciding evidence quoted (the surviving "101 (57.7)" beside n=196; the surviving prose "4088mL (3400:4525)"); verdicts: reconstruction/surviving copy, zero recitations.
- **`estudo7/avaliacao-estudo7.md`** — the deployment phase's adjudicated record: the errata-panel table (each cell with anchor value, source quote, model cell), the Chen anatomy with both printed layers, and the three-configuration table.
- **`estudo6/avaliacao-estudo6.md`** — the pilot's fully adjudicated per-study record under the rite (quote before verdict), including the two key corrections the process caught against itself (REF29 ASA per erratum #10; REF41 blood-loss arms per erratum #17; applied in commit `b54c19c`).
- **`estudo8/factualidade-p1.json`** + `avaliacao-p1.json` — the mechanical classifications (divergents, omissions, invention screen) whose residues feed adjudication.
- **`estudo8/avaliacao-p1.md`** (section of 2026-09-01) + `divergentes-classificados.json` — the cell-by-cell mechanism classification behind the manuscript's Supplementary Tables S1--S7, and the four-cell adjudication **in the models' favor**: on Castro's unperturbed blood-loss cell, four models transcribed the printed value byte-for-byte and the grading lens corrupted the comparison by applying the seal pair 31→28 as a substring replacement inside `1283.2` (→ `1313.2`). The rite catching the grader, quoted and dated; manuscript Table 2 keeps the comparator's unadjusted scores with a caption note.

## 5. The dated decision trail

- **`estudo3/agenda-bracos.md`** — the running ledger: every author directive, editorial decision, amendment and adjudication outcome, dated.
- **Git history** — every protocol and amendment committed *before* its run; every correction a separate dated commit; nothing rewritten in place without a note.

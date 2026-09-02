# EXTRAI — Pre-registered protocol, Study 9: the quote-bearing sheet (schema v2), A/B against the frozen v1

**Registered 2026-09-01, before any run.** Amendments only as dated sections. General method: [`METHOD.md`](../../METHOD.md). Author's directive (ledger, 2026-09-01): every extracted value, quantitative or qualitative, should carry a well-detailed provenance — the verbatim sentence that contains it — and the upgrade must be measured as an A/B, never assumed an improvement.

## 1. Question (frozen)

**Does mandatory verbatim-quote provenance on every extracted cell (schema v2: `{value, where, quote}`) (a) preserve extraction accuracy, (b) surface the mislabeled-dispersion defect class at the sheet itself — the class that silently distorted a pool in the campaign — and (c) keep provenance-integrity false flags low — and at what measured cost in tokens, time and weak-model robustness?**

## 2. Design principles (frozen)

- **A/B with the campaign as arm B.** Arm A (new runs) = extraction under the v2 instruments frozen in `prompts/` at this registration. Arm B (no new runs) = the campaign's archived v1 sheets (Study-8 P1 for Anchor 1; Study-8 P3-b for Anchor 2), same corpora, same sealed perturbations, same corrected keys, same graders. Instruction language English in both arms; the only changed variable is the sheet schema.
- **Instruments (frozen here)**: [`prompts/t1-extraction-v2.txt`](prompts/t1-extraction-v2.txt) and [`prompts/e3-extraction-v2.txt`](prompts/e3-extraction-v2.txt) — v1 verbatim plus: every data cell is `{"value", "where", "quote"}`; `quote` is the verbatim sentence/fragment containing the value, ≤240 characters, never paraphrased; `NR` cells carry empty provenance. The v1 instruments remain frozen and untouched.
- **Cast**: `gemma4:12b` (primary arm — the measured reader) and `llama3.1:8b` (robustness probe — the cast's weakest reader, carrying the malformation risk the schema change could aggravate). Two replicates each, perturbed world, pinned builds, uniform 8,000-token allowance (v2 outputs are larger by design; the raise is declared, not hidden).
- **The three provenance nets (deterministic, warn-only, grader-side)**, run over every v2 sheet:
  - **N9-1 quote-exists**: the quote, normalized (whitespace collapsed; hyphen/minus/dash unified; case-insensitive), must occur as a substring of the perturbed source; failure flags *provenance hallucination* — flagged, never rejected.
  - **N9-2 value-in-quote**: every numeric token of the cell's value (±0.005), or the qualitative value as a string, must occur inside its own quote.
  - **N9-3 type-vs-quote coherence**: for dispersion-type declarations, the declared class must match the form printed in the cell's own quote (declared SD/SE while the quote prints an interval pattern, or declared CI while the quote prints a lone ±spread → flag). This is the campaign's N7-1b check mechanized at the sheet, with no source search needed.
- **Doctrine unchanged**: nets detect and warn, never substitute; all residues go to quotation-bound adjudication; nothing retroactive; the run is committed after, the protocol before.

## 3. Runs

- Anchor 1: 14 perturbed primaries × 2 replicates × 2 models = 56 calls (v2-T1).
- Anchor 2: 7 perturbed primaries × 2 replicates × 2 models = 28 calls (v2-e3).
- Total ≈ 84 calls, estimated 5–8 h (larger outputs than the campaign's per-call baseline).

## 4. Pre-registered hypotheses

- **H9.1 (accuracy preserved)**: gemma12's v2 cell agreement with the corrected key stays within replicate-level variance of its v1 record (Anchor 1: 103/124 ± the observed replicate band of 4 cells; Anchor 2: the deterministic route over v2 sheets lands its lens within ±0.05 of the v1 lens −0.27), and replicate stability stays ≥90%.
- **H9.2 (the payoff, stated disjunctively)**: the Chen-class cell is **either** flagged by N9-3 at the sheet (the model transcribes the prose ± layer again and its own quote convicts the declared type) **or** prevented at extraction (the quote demand anchors the model on the table layer and the declared type becomes coherent) — recorded as *flagged* or *prevented*, both successes; the failure mode is the poisoned cell passing unflagged again.
- **H9.3 (provenance integrity)**: for gemma12, N9-1 and N9-2 flag ≤5\% of quoted cells each (hallucinated or value-less quotes are rare); every flag is adjudicated with the source before any verdict.
- **H9.4 (weak-model cost, measured not judged)**: llama8's v2 parse rate and cell scores are reported against its v1 record (28/28 parseable; 88/124); degradation is a measured cost of the schema, not a failure of the study.
- **Cost metrics (declared)**: tokens per sheet and seconds per call, v2 vs the v1 record, both models, both anchors.
- *Declared exploratory*: quote-layer census — for cells whose value is printed in more than one layer (table and prose), which layer do the quotes cite? (The Chen anatomy predicts this matters; no hypothesis is staked.)

## 5. Outputs

`dados/estudo9/` — `prompts/` (frozen v2 instruments) · `saidas/<model>/{ma1,ma2}/` (raw v2 sheets) · nets report (`redes-proveniencia.md` + JSON) · per-arm grading and the A/B comparison table · `avaliacao-estudo9.md` · run log with seal SHA-256.

## 6. Out of scope

Any change to the v1 instruments, keys, seals or engines; orchestration and harness stages; the other three cast models (the A/B is instrument-level, not another model comparison); library adoption of v2 (decided only after this study's record, by the author).

---

## Amendments

Both registered **2026-09-01, before any Study-9 run**, and committed before the runner was built. Neither alters the frozen question, design, cast, instruments or hypotheses; each fixes an ambiguity that would otherwise have to be resolved mid-analysis, which the rite forbids.

### A9-1 — the arm-B baseline for `llama3.1:8b` is the adjudicated figure

Section 4's H9.4 cites the v1 record as "28/28 parseable; **88/124**". That is the comparator's raw output. After this protocol was registered, four cells — one each for `qwen3:14b`, `llama3.1:8b`, `qwen3.5:9b` and `deepseek-r1:14b` — were adjudicated **in the models' favour** under the quotation rite: on Castro's (PMC11061212) blood-loss control cell each transcription was byte-identical to the key's source value (`1283.2 ± 959.7`), and a seal-pair substring collision in the grader's unperturbation lookup (the pair 31→28 applied *inside* `1283.2`, yielding `1313.2`) corrupted the comparison. The record is in `estudo8/avaliacao-p1.md` (section of 2026-09-01) and indexed in `adjudication-record.md`.

**Frozen decision**: arm B's baselines for this study are the **adjudicated** figures — `gemma4:12b` 103/124 (unchanged; its divergence on that cell was a genuine row slip), `llama3.1:8b` **89/124**. H9.4 is read against 89/124, and H9.1's gemma12 baseline is unaffected. The comparator's raw output stays on record in both places. No published v1 number is rewritten by this amendment; it fixes only which figure H9.4's comparison uses.

### A9-2 — the grading lens is held constant across both arms, collision included

The unperturbation lookup described in A9-1 still substitutes seal pairs without word-boundary awareness. A boundary-aware fix is in the instrument backlog for future rulers, and this study is a future ruler — so the choice has to be made explicitly rather than by default.

**Frozen decision: this study does NOT adopt the fix.** Arm B's sheets were graded by the current lens; fixing it for arm A alone would change two variables at once (sheet schema *and* grader) and forfeit exactly the interpretability the A/B exists to buy.

**Declared consequences**, so nothing is discovered mid-analysis:
- The known collision applies **identically to both arms** — same trial, same cell, same seal pair — so it cancels in the A/B delta, which is this study's estimand.
- Absolute cell scores in either arm carry the artifact; every table reporting them carries a footnote pointing to this amendment.
- **The three provenance nets are unaffected**: N9-1 compares the quote against the source text, N9-2 the value against its own quote, and N9-3 inspects the printed form inside the quote. None passes through the reversal lookup, so H9.2 and H9.3 are clean of this artifact.
- The boundary-aware fix stays queued as its own future measurement, never retroactive.

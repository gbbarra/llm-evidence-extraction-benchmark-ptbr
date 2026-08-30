# Study 3 — question ledger

## Paper 1 (CLOSED — preprint ready)

The baseline arc: read → compute → chain → **reproduce the low-carb meta-analysis** (unperturbed diamond −0.28 [−0.39, −0.17] vs published −0.24 [−0.32, −0.16]). Ends at the first diamond by the author's editorial decision (commit 70c4249).

## Paper 2 (REORGANIZED 2026-08-30 — one question, one answer)

**Question: can local models that fit on the integrated GPU (≤14B) reach the expected meta-analytic value, if the harness is fixed?**

Design principles set by the author:
- **Focus**: iGPU models only — gemma4:12b + qwen3:14b — and harness engineering; bigger/CPU models (gemma26, qwen38) return later only as reference points; previously discarded small models (e.g., llama3.1:8b, qwen3.5:9b, deepseek-r1:14b) may enter after the harness works.
- **Starting point**: the extraction sheets already exist (gemma12, 98%, replicate-identical) — the study starts from the audited-clean sheets, not from the PDFs.
- **Outcome**: the diamond. Primary metric = |pooled MD − mechanical truth over the same sheets| (target: digit-exact, as the 27B achieved on committee-OR sheets); anchor comparison via the unperturbation lens (published −0.24).
- **Seeded errors: DROPPED from the main line** (decision record below). **Corpus perturbation: KEPT** (contamination defense; costs nothing — the sheets already live in the perturbed world; the double target sheet-truth/unperturbed-vs-anchor is already built).

The harness ladder (independent variable; each rung pre-registered before running):

| Rung | Harness | Status |
|---|---|---|
| H0 | v2, spontaneous discipline | **measured**: both small models fail (mixed-round; by-head; wrong-side diamonds) |
| H1 | v3 nets (flow policing) | **partially measured** (gemma12 L+S ran before the pause): flow fixed — tool used, pool reconciled, closed — diamond still wrong (+0.37/+0.36) because argument assembly drops signs; content failure, nets can't reach it |
| H2 | **harness-driven ("esteira dirigida")**: the harness owns the flow — reads the sheet fields, applies the dispersion conversions deterministically, asks the model only narrow questions (one study, one field set at a time), assembles and executes the pool itself | to design + pre-register |
| H3 | H2 + targeted field re-verification (one field, one question) where sheets are uncertain | optional rung |

Answer (filled when the ladder closes): —

### Seeds decision record (author asked for rigor here)
The 8 seeded errors existed to answer ONE question — "is the audit gate real?" — and that question is **answered** (sensitivity matrix: 27B 90%, 14B 70%, 12B 60%; complementary blind spots; committee rules quantified end to end). For Paper 2's question the outcome is the diamond, and a seeded lane would conflate harness effects with corruption-propagation effects. Seeds therefore leave the main line; if H2/H3 includes an audit step, its value is measured by **diamond delta with vs without the step**, not by seed sensitivity. The seed matrix becomes Paper-2 motivation/appendix material. (Distinct from seeds, the corpus perturbation stays: without it, "reached the expected value" cannot be told apart from "remembered the published value".)

### Inventory of already-run arms (Paper-2 motivation material; no re-runs)
- all-gemma (Amendment 3): spontaneous small-cast pipeline inverts the answer (+0.85).
- igpu (Amendment 4): audit half works (70%, corrections 7/7), calc dies at the mixed-round joint.
- committee (Amendment 5): OR repairs 10/10 and the 27B calcs sheet-truth digit-for-digit — proof the SHEETS support an exact diamond; MAJ preserves truth but the champion went by-head.
- championship under v3 (Amendment 6, **interrupted by design**): gemma12 L+S only — flow nets work, content assembly fails. gemma26/qwen38 runs and the aud26 arm (Amendment 7) are **paused**, returning only as reference points after H2.

**Publication split**: Preprint 1 = the baseline arc (done). Preprint 2 = this page's question; the removed ablation material (`paper/material-preprint2-ablation.tex`) seeds its motivation section.

Instrument-fix backlog (future corpora/rulers, never retroactive): title/byline kept in corpus text (gap #5); `estudo` field graded; perturbation operator covers number words (#1), totals with visible addends (#2), twin tables (#3), rounded prose restatements (#4).

# Study 3 — question ledger (the arms, in logical order)

One line per question; one arm per question; nothing runs without a registered amendment. Updated as arms close.

| # | Question | Arm / instrument | Status | Answer |
|---|---|---|---|---|
| Q1 | Does the pipeline work with the measured winners? | baseline (protocol §3) | **closed** | Yes: unperturbed diamond −0.28 vs −0.24 published; gate did 6× the sabotage's damage |
| Q2 | Can the whole pipeline run on the extraction champion? | Amendment 3 (all-gemma) | **closed** | No: runs 4.5× faster, inverts the meta-analysis (+0.85); audit = per-sheet gate 60%/0% FA |
| Q3 | Does gemma+qwen on the iGPU hit the sweet spot? | Amendment 4 (igpu) | **closed** | Audit half yes (70%, corrections 7/7, unique digit catches); calc half no (same mixed-round joint) |
| Q4 | Is a committee a mechanism or just retrospective arithmetic? | Amendment 5 (OR-27B vs MAJ-3, calc+synthesis over committee sheets) | **closed** | OR: 10/10 seeds fixed; champion calc pool = sheet truth digit-for-digit (-0.47) at FA cost (truth drift -0.52 to -0.47). MAJ: truth preserved (-0.52) but the champion went by-head (0 calls, -0.45) |
| Q5 | What scaffolding makes small models close the tool loop? | **Harness v3** (this commit): mixed-round fix + tool-avoidance net + pool reconciliation, all gated behind `E3_HARNESS=v3` | **built, unrun** | — |
| Q6 | Who is the best tool calculator, fairly compared? | Amendment 6: calculator championship — 4 veterans × 2 lanes under v3, identical audited sheets | **running** | — |
| Q7 | Does gemma26 audit? (last empty cell of the 4×matrix) | Amendment 7 (cast aud26, audit stage only) | **queued after Q6** | — |
| Q8 | Flags-not-fixes + committee-with-reverification | Study 4 ("hardened pipeline") — new protocol | future | — |

**Publication split (author's decision, 2026-08-30)**: **Preprint 1** ends at the baseline pipeline's first diamond (-0.28 vs -0.24) — the closed arc read→compute→chain→reproduce; the entire ablation program (Q2–Q7 + committee + scaffolding + championship) is **Preprint 2**, seeded by `paper/material-preprint2-ablation.tex`.

Instrument-fix backlog (apply to FUTURE corpora/rulers, never retroactively): keep title/byline in corpus text (gap #5); `estudo` field enters the ruler; perturbation operator covers number words (gap #1), totals with visible addends (#2), twin tables (#3), rounded prose restatements (#4).

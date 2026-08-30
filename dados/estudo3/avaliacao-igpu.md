# EXTRAI — Study 3, Amendment-4 arm evaluation: the mixed iGPU cast

Registered before the run ([Amendment 4](protocolo-estudo3.md)); executed 2026-08-30: Stage E reused (gemma4:12b), **A and C = qwen3:14b**, S = gemma4:12b — cross-family audit independence plus the qwen family's measured arithmetic vocation, everything on the integrated GPU. Queue: 18 runs in **93 minutes**. Same frozen rules as the other casts (including harness v2's mixed-round gap). Grading arm-aware; the calc grader gained an order-fallback for study-name matching (needed because of instrument gap #5, below).

## The audit (qwen3:14b): a third personality, and the committee finding

**7/10 seeded cells caught — with 7/7 exact corrections** (the only auditor with a perfect correction record). Its unique catches: **both character-level seeds** — the digit inside the CI string (−0.37 → "−0.33 to −0.19", which the 27B and the 12B both confirmed) and Chen's baseline digit corrected **to the right arm's value** (9.95 — both other auditors "fixed" it to the wrong arm). Its misses: one lone sign flip (REF9; it caught the other on Wang, citing the abstract), Dorans's transposed n, and half of Thomsen's arm swap (it fixed the experimental cell and confirmed the seeded control, leaving both arms equal). False alarms: 4/95 (L) and 8/85 (S), mostly a raw-factorial-cell anchoring habit (it "corrects" margin-level baselines to single-cell table values — a third route ontology: the 27B sums margins, the 12B stamps, the 14B descends to raw cells) plus a Thomsen baseline cross-swap.

*How to read: per-seed verdicts across the three casts (✓ = caught; ✓* = caught, wrong value; ✗ = missed).*

```
seed                        27B (base)  12B (allgemma)  14B (igpu)
arm swap, Chen (2 cells)       ✓✓            ✓✓             ✓✓
arm swap, Thomsen (2 cells)    ✓✓            ✓✓             ✓✗
sign flip, Saslow 2023          ✓             ✗              ✗
sign flip, Wang                 ✓             ✗              ✓
digit in CI, Dorans             ✗             ✗              ✓
digit in baseline, Chen         ✓*            ✓*             ✓
transposed n, Dorans            ✓             ✗              ✗
transposed n, Thomsen           ✓             ✓              ✓
---
cells caught                  9/10          6/10           7/10
exact corrections              8/9           4/6            7/7
false alarms (clean lane)     6.5%           0%            4.2%
```

**No seed escaped all three auditors, and the union of the 27B and the 14B covers 10/10** — their blind spots are complementary (the 27B misses only what the 14B uniquely catches, and vice versa). A two-of-three audit committee is the direct design implication for the hardened pipeline.

## The arithmetic (qwen3:14b): the family instinct, and the same broken joint

Both lanes again closed with **zero executed calls** (the model wrote 7 per-study calls and one pool call, then emitted the final JSON in the same output; the harness's round order discarded them — third cast, same mixed-round gap). But the by-head quality differs sharply by family: **lane L tracked all 7 per-study MDs exactly** (vs 2 attempted/both wrong under the 12B) — the Study-2 ranking reproduced one level up. The pools stayed wrong by head in both lanes: L −0.61 [−1.01, −0.21] vs truth −0.50; S **+0.25 [+0.05, +0.45]** — the seeded lane's surviving corruptions (the confirmed sign seed among them) pushed the by-head diamond to the wrong side of zero, and the synthesis (202/241 words, under the floor, with another wrong mental participant sum) narrated it fluently. Grading notes: two lane-S "wrong" labels are contestable — the truth heuristic that flips Wang-convention positive drops also fires on the seeded +0.32, so the model's faithful computation of the corrupted sheet grades as error; recorded as a ruler nuance rather than re-litigated.

## Instrument gap #5 (found here, corrected everywhere)

The by-head casts surfaced trial names like "Tidgren", "Taves", "Brackgold" — first attributed (wrongly) to calc-stage fabrication in the all-gemma evaluation. Verification against the Stage-E sheets showed they are **extraction-stage confabulations shared by every arm**: the corpus builder strips the articles' title/byline, the sheet asks for first author and year, and the extractor invented names instead of answering NR — for 5 of 7 trials. The field was ungraded, so it passed Stage-E grading and **all six audits across three families** unflagged; the baseline calc masked it by using the harness's canonical keys. Fixes: the all-gemma evaluation carries a dated correction; the calc grader matches by order when names don't resolve; future corpus builds must keep the title line, and the `estudo` field enters the ruler.

## The three-cast table (deployment answer)

```
                       base (medidos)   all-gemma      igpu misto
wall clock                272 min         61 min         93 min
audit: seeds/exact        90% / 8-9      60% / 4-6      70% / 7-7
audit: FA clean            6.5%            0%            4.2%
calc: executed calls      23+22            0+0            0+0
calc: per-study (L)       6/7 exact      0/7 (2 tried)  7/7 md-exact
pooled vs truth (L)       -0.39/-0.52    +0.85/-0.52    -0.61/-0.50
pooled, seeded lane       -0.43 (ok)     +0.61 (wrong   +0.25 (wrong
                                          side)          side)
```

**Answer to the arm's question** (*does gemma+qwen on the iGPU hit the deployment sweet spot?*): the audit half, yes — 70% sensitivity with perfect corrections and unique character-level catches makes the 14B a genuinely useful gate, and the committee finding (27B+14B = 10/10) is the arm's lasting contribution. The arithmetic half, no — under this harness no small cast executed the tool from inside the pipeline; the baseline 27B remains the only calculator that did. The deployment recipe after three casts: **extract 12B · audit 14B and 27B as a two-of-three committee · compute only through the 27B (or fix the mixed-round gap and re-measure) · never accept a pooled number that was not echoed through the tool.**

# Study 8 / P4 ORCHESTRATE — evaluation (gemma12 under the English ten-net harness)

**Run 2026-09-01, 8.7 min**, over gemma12's own P3-b English sheets (perturbed world). Artifacts: `p4/` (calc transcripts, pool, synthesis, summary). No model stage saw a key, a published value, or the seal.

## What happened, stage by stage

- **Per-study typed calls (7/7 closed)**: every study reached a final under the EN call schema (`{"function", "arguments", "source", "derivation"}`). **Two content warnings fired — both on Goday, both from the declared-derivation net — and were resolved by confirm-or-correct**, the exact net-and-trial class the Portuguese Amendment-3 run exhibited. Zero warnings elsewhere; zero format failures.
- **Pooling**: the model emitted the `pool_dl_md` call over its own seven sextets and closed with the executed result — **digit-consistent** (final −0.50 [−0.78, −0.22] ≡ pool over its own sextets). The call class that separated gemma12 from the rest of the cast in P2 executes cleanly under the EN harness.
- **Product layer**: zero incoherent reported CIs; **zero orphan numbers** in the synthesis.
- **Grader-side, afterward**: model pool −0.50 vs mechanical truth over the same sheets −0.52 — **Δ 0.02, the orchestration "weather" at its usual small size** (named route divergences: Chen assembled a different source-declared route than the deterministic selector, −0.43 vs −0.60; Goday took the final-levels route, −1.8, as in the PT formal run). **Lens: −0.27 [−0.38, −0.17]** vs published −0.24 [−0.32, −0.16] — the same landing as P3's deterministic lens over the same sheets, and as the PT record.

## H8.4 verdict — passes

Every load-bearing Portuguese-record behavior reproduces under the English build: warnings resolved by confirm-or-correct (never substituted), the DL pooling executed faithfully and digit-consistently, flags never endorsed, the weather present at Δ0.02 (PT formal run: Δ0.06), zero orphans. Ablation column 4: no language effect at the orchestration stage.

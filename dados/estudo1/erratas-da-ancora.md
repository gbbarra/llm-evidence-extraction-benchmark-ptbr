# Errata and unsupported cells of the anchor meta-analysis (PMC13235771)

Record under Amendment 4 of the [protocol](protocolo-estudo1.md). Every item was decided by the original primary source, with the literal quote that supports it. The anchor's tables remain untouched in `gabarito-ma.json`; the grading ruler is `gabarito-oficial.json`.

**Who did what**: discrepancy 1 was *raised by the local models* (three models independently extracted values against the published table) and *confirmed by the adjudicator* (Claude) in the source; the rest emerged from the adjudicator's cell-by-cell verification. Supervision by the benchmark's human author. A note of fairness: transcription errors happen in any hand-made review — the adjudicator himself logged three errata in the same round (items 2 and 4 below); the point is the process, not the authors.

## Confirmed by the source

1. **Yoon et al. — arms swapped in the characteristics table.** The MA publishes GDFT 36 / control 39. The source: *"The GDHT group (n = 39) received the stroke volume index- and cardiac index-based…"* and *"the control group (n = 36) received the standard care"*. Correct: **GDFT 39 / control 36**. (This also resolves pre-registered internal inconsistency #3: the morbidity table's "Yun" row, with 39/36, was the correct one.)

2. ~~**Redondo Calvo et al. — arms swapped.**~~ **WITHDRAWN — adjudicator erratum (2026-08-28).** The first version of this list declared swapped arms based on the abstract alone (*"randomized to the GDHT (n = 16) and control group (n = 19)"*). The article's body says the opposite in four places — the flowchart (*"There were 16 patients in the control group and 19 patients in the GDHT group"*) and all three tables (*"Control N = 16 GDHT N = 19"*). By preponderance, **the MA is right (GDFT 19 / control 16)**; the real finding is that **the Redondo primary contradicts itself** (abstract vs body). Grading accepts both readings according to the model's cited "where". On public record: the adjudicator (Claude) erred by verifying against a single passage — the very sin this benchmark exists to hunt.

3. **Weinberg et al. — ASA "Not stated".** The MA declares the ASA distribution as not reported. The article's table reports, for both arms: *"ASA Class I-II 7 (27%) 7 (27%) ASA Class ≥ III 19 (73%) 19 (73%)"*.

## Unsupported in the primary's full text

4. ~~**Wu et al. — "Inotrope use: Lower in GDFT".**~~ **WITHDRAWN — adjudicator erratum #2 (2026-08-28).** The first version's search used rigid context windows that hid Wu's Table 3 rows. They exist and support the MA: *"Number of patients using norepinephrine 15 (25.9) 24 (42.9) … phenylephrine 12 (20.7) 24 (42.9) … ephedrine 12 (24.0) 19 (35.2)"* — lower use in the GDFT arm for all three drugs. The three models that extracted those values (briefly accused of fabrication in the first analysis) were **literally right**. Second time in the same night the models beat the adjudicator; the search instrument was fixed (flexible windows).

5. **Sujatha et al. — ASA "95:105".** The text reports only eligibility ("ASA I and II") and says the distribution was "comparable", with no numbers. The control-arm cell in the MA is corrupted by Excel time formatting (*"2 days, 11:42:00"*) — pre-registered inconsistency #5.

## Confirmed by the source (adjudication addition, 2026-08-28)

9. **Sun et al. — inconsistent oral-diet time conversion.** The MA publishes 72±24 h (GDFT) vs 96±30 h (control) — a 1-day difference. The source text itself: *"GDFT significantly also shorten … time to first tolerate oral diet **by 2 days** (P < 0.001)"*, with medians 4.0 d (2.7–6.0) vs 6.0 d (5.0–9.3). All four models extracted 4.0/6.0 days, unanimously. The MA's conversion contradicts the source it summarizes.

## Definitional divergence (not an error — an undeclared choice)

6. **Sujatha et al. — n per arm.** The source: *"306 patients, with 102 in each group, were enrolled"*. The MA records 200 (merged GDFT) and 101 (control) — *analyzed* patients, not *randomized*, with the choice undeclared. Grading accepts both readings.

7. **Castro et al. — narrow surgery label.** MA: "All major bowel surgeries"; source: *"elective open abdominal surgeries"*, including hepatectomy, gastrectomy and pancreaticoduodenectomy.

8. **Wu et al. — n per arm.** The MA records 58/56 (analyzed). The source says literally: *"122 subjects were randomly assigned… Specifically, 61 patients were allocated to the PPV group and another 61…"*. As with Sujatha, the MA used analyzed numbers without declaring; grading accepts both readings.

## Closed stratum (Amendment 2; adjudicated 2026-08-28)

10. **de Waal et al. — ASA columns swapped.** The MA publishes ASA(GDFT) 24:123:86:1 and ASA(control) 17:132:95:4. The source's table ("Control (n = 234) PGDT (n = 248)") gives the inverse, and arithmetic proves it: 123 = 52.6% × 234 (control); 132 = 53.2% × 248 (PGDT). All four models followed the source, unanimously.

11. **Diaper et al. — ASA "Not stated" that the article reports.** *"ASA-PS classes III & IV 98 (50.0) 85 (42.9)"* — same pattern as Weinberg (#3).

12. **Diaper and Coeckelenbergh — unsupported flatus cells.** The MA publishes flatus times (55±14/58±16 h and 52±15/60±18 h) for two articles whose full text **does not contain the word "flatus"**. Coeckelenbergh's total fluid (3500/3250 mL) is likewise absent. Possible origin in supplements/figures — beyond the text corpus's reach; cells excluded from scoring.

13. **Systematic pattern: the MA's "n" = analyzed, undeclared.** Confirmed in SIX studies (Wu 61→58/56; Sujatha 102→100/101; de Waal 274/259→248/234; FEDORA 224/226→209/211; Hokenek 40/40→39/39; Diaper 200/201→196/198). The MA's characteristics column mixes randomization layers with no methods note.

14. **Internally contradictory primaries (besides Redondo):** Diaper (prose "data from 198 and 196" vs table "GDHT n=196 / RNT n=198") and FEDORA (abstract "450 randomized" vs methods "428 were randomised"; 224+226=450≠428).

15. **Pooled morbidity labeled with the wrong method** *(found in Study 2's arithmetic audit)*. The published pooled morbidity RR (0.778; CI 0.57–1.07) reproduces exactly under DerSimonian-Laird (recomputed: 0.774; 0.566–1.059), while table 5's caption describes it as Mantel-Haenszel (which would give 0.863). Right number, wrong method name. The 11 published per-study RRs are all correct (±0.015).

## Pending final adjudication (excluded from scoring)

- Yoon — inotrope use ("No difference"): comparative result not located in the text.
- Sun — ileus 2 (4.0%) / 16 (32.0%): possibly derived from the I-FEED score.
- Castro — ileus 6 (14.0%) / 19 (45.2%): the term "ileus" absent from the text.
- Redondo — GDFT blood loss 292.6 ± 274.1: literal value not verified.
- de Waal — inotrope "Higher in GDFT": the algorithm uses norepinephrine/dobutamine; the comparative result was not located.
- Calvo-Vecino — inotrope "Lower in GDFT": mentions only in the methods.
- Coeckelenbergh — inotrope "Lower in GDFT": outcome listed, value not located; laparoscopy (MA=0) with a laparoscopic provision in the protocol, per-arm count not located.
- Hokenek — inotrope "No difference": conceptual mention only.

*Method note: verification uses the full text (abstract + body, including tables); values living exclusively in figures or supplements are out of reach — cells so marked score against no model.*

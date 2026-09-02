# EXTRAI — Pre-registered protocol, Study 10: does a model that reads back its own quote repair the sheet, or damage it?

**Registered 2026-09-02, before any run.** Amendments only as dated sections. General method:
[`METHOD.md`](../../METHOD.md). Author's directive (2026-09-02): ask whether the model can use
the quote it wrote to correct or improve its own extraction.

## 1. Question (frozen)

**When a model is shown its own completed v2 sheet and asked to check each value against the
quote it itself pasted, (a) how many wrong cells does it repair, (b) how many correct cells does
it damage, and (c) does the net effect survive the series' warn-only doctrine — or confirm it?**

The question is stated in two directions on purpose. "Did it improve?" is not measurable as a
single number here: a pass that repairs 4 cells and breaks 10 is a failure that a net score
would hide.

## 2. Why this question, and why it is dangerous

**The measured opportunity.** The Study-9 sufficiency reading of `gemma4:12b`'s Anchor-1 arm
(`estudo9/suficiencia-das-citacoes.md`) found **4 self-contradictory cells** — the value
disagrees with the quote the model itself pasted, with no source needed to see it:

- Weinberg `asa_gdft`/`asa_control`: value `1-2 (70%), ≥3 (30%)`; own quote
  `ASA Class I-II 7 (27%) … ASA Class ≥ III 19 (73%)` — the percentages are inverted.
- de Waal `asa_gdft`: value `6.9% (ASA II)`; own quote `ASA II 144 (53.2%)`.

Those four are the **ceiling of the possible gain** for this model on this anchor. Nothing else
in the sheet is repairable by readback alone.

**The measured danger.** Three findings of this series point the other way, all from the development phase, where a checking stage was given write-power
(`estudo4/protocolo-estudo4.md`, `estudo5/protocolo-estudo5.md`):

- an auditing model "repaired" correct cells by imputing plausible values — once correcting a
  sample size to 24.5 while quoting, in its own verdict, the text's `n = 28`;
- a calculator stage flipped the sign of a control arm that had genuinely worsened
  (`+0.3` written as `−0.3`);
- a pipeline's quality gate did **six times more damage** to the pooled estimate than the
  planted sabotage it caught.

These are why the doctrine reads *detect and warn, never substitute*. A self-correction loop is
not a net substituting a value — the model corrects itself — but **plausibility bias belongs to
the model, not to the net**, so the exposure is the same. This study measures that exposure
instead of assuming either outcome.

## 3. Design principles (frozen)

- **A/B with Study 9 as arm B.** Arm A = a **second pass** over the archived v2 sheets. Arm B =
  those same sheets, unmodified. Same corpora, same sealed perturbations, same corrected keys,
  same graders, same lens (held constant per amendment A9-2, collision included). The only
  changed variable is the readback pass.
- **The readback instrument** (to be frozen in `prompts/` before any run): the model receives
  its own completed sheet — values, locators and quotes — **and nothing else**. It does not
  receive the article, the key, or any net output. It is asked, cell by cell, whether the value
  is consistent with the quote beside it, and may revise the value, the quote, or neither. Every
  change must be accompanied by which of the two it believes was wrong.
- **No source access in arm A.** This is deliberate and is what makes the study interpretable:
  any repair must come from the sheet's internal evidence, which is exactly the property v2
  claims to add. Re-reading the article would test something else.
- **Cast**: `gemma4:12b` (the reference reader, whose v2 arm is complete and whose 4
  self-contradictions define the ceiling) and `granite4.2:8b` (whose v2 arm is also complete and
  whose failure profile differs — stitched quotes rather than contradictions). Two replicates
  each, Anchor 1.
- **Doctrine unchanged**: the harness still substitutes nothing. What changes is that the
  *model* is given its own sheet back. Nets stay grader-side and warn-only; nothing is
  retroactive; the protocol is committed before the run and the run after it.

## 4. Pre-registered hypotheses

- **H10.1 (repair, measured)**: of the cells whose value contradicts their own quote, the
  readback pass repairs a number reported as a fraction of that set — for `gemma4:12b`, of 4.
- **H10.2 (damage, the one that decides)**: among cells that **agreed with the source-verified
  key before the pass**, the number altered by the readback is reported as a rate. The
  pre-registered failure condition is **damage > repair**; the pre-registered success condition
  is **repair > 0 with damage = 0**. Anything between is reported as measured, without a verdict.
- **H10.3 (the honest null)**: it is a legitimate and pre-registered outcome that the model
  changes nothing. A readback that touches no cell confirms the sheet is stable under
  self-inspection and costs only tokens.
- **H10.4 (locus of change)**: for every altered cell it is recorded whether the model revised
  the **value** or the **quote**. Revising the quote to fit a wrong value is a distinct and more
  serious failure mode than revising the value, and is counted separately.
- *Declared exploratory*: whether repairs concentrate in the field types Study 9 identified as
  the instrument's blind spot (`asa_*`, `surgery_type`). No hypothesis staked.

## 5. The cheaper, safer alternative — declared here so it is not confused with the study

The N9-2 net **already detects these contradictions mechanically**: that is how the four cells
were found, with no model involved. Promoting that detection from grader-side warning to a flag
carried on the sheet would buy the detection **without the risk of the correction**. This study
does not implement that; it measures whether the model-side loop adds anything the net does not
already give. If H10.2 shows damage, the net alone is the answer, and that is a result.

## 6. Runs

Anchor 1 only: 14 sheets × 2 replicates × 2 models = **56 readback calls**. No new extraction,
no new article reading — the input is a sheet, not a paper, so calls are short. Estimated 1–2 h.

## 7. Outputs

`dados/estudo10/` — `prompts/` (frozen readback instrument) · `saidas/<model>/` (raw readback
responses) · per-cell before/after table with the locus of each change · `avaliacao-estudo10.md`
· run log with seal SHA-256.

## 8. Out of scope

Any change to the v1 or v2 instruments, keys, seals or engines; giving the model the article or
the key during readback; letting any net or harness stage write a value; the other three cast
models; adoption of readback into the pipeline (decided only after this study's record, by the
author).

---

*Amendments: (none)*

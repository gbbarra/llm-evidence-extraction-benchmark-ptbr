# -*- coding: utf-8 -*-
"""Study 7 / Amendment 3 — the deployment cell: gemma4:12b orchestrating its
own calculations under the FROZEN Study-5 ten-net harness, over the clean-text
sheets. No answer key, no published value, no seal visible to any model stage.

Adapted from the frozen pipeline3-gemma.py (Study 5, Amendment 6): stage E is
replaced by SEEDING (Study 7's frozen MA-2 sheets, first-parseable replicate,
converted EN->PT by the frozen correspondence tables — values untouched); the
perturbation-specific correction stage is replaced by the clean-text
comparison (mechanical truth over the same sheets; published value only
grader-side, after the run). Rung CALC3E7 arms the complete frozen net set.

Run: python scripts/estudo7/e7-pipeline.py    (resume-safe)
Outputs: dados/estudo5/saidas/{HARNESS-E7,CALC3E7}/ · dados/estudo5/resultados-POOL3E7.json
         dados/estudo7/harness-run/ (summary, synthesis, forest)
"""
import importlib.util
import json
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
D5 = ROOT / "dados" / "estudo5"
E7 = ROOT / "dados" / "estudo7"
SEED = D5 / "saidas" / "HARNESS-E7"
PIPE = E7 / "harness-run"

_sp = importlib.util.spec_from_file_location("e5", ROOT / "scripts" / "estudo5" / "e5-harness.py")
e5 = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(e5)
h3 = e5.h3

_e7d = importlib.util.spec_from_file_location("e7d", ROOT / "scripts" / "estudo7" / "e7-downstream.py")
e7d = importlib.util.module_from_spec(_e7d)
_e7d.loader.exec_module(e7d)

RUNG, POOLR = "CALC3E7", "POOL3E7"


def semeia():
    """Seed the pipeline's sheet folder with Study 7's frozen clean sheets,
    EN->PT converted (presentation only). One file per trial (-r1), the same
    first-parseable sheet the deterministic analysis used."""
    SEED.mkdir(parents=True, exist_ok=True)
    for tid in h3.TRIALS:
        out = SEED / f"{tid}-r1.json"
        if out.exists():
            print(f"  seed exists {tid}", flush=True)
            continue
        js = e7d.bruta(e7d.MA2_DIR, tid)
        ficha = e7d.ficha_ma2_pt(js)
        out.write_text(json.dumps(dict(modelo=e5.MODELO, trial=tid, replica=1,
                                       origem="estudo7-clean-sheet-EN2PT",
                                       content=json.dumps(ficha, ensure_ascii=False)),
                                  ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  seeded {tid}", flush=True)


def main():
    PIPE.mkdir(exist_ok=True)
    t0 = time.time()

    print("===== A3 · stage E: seeding the frozen clean-text sheets (no extraction)", flush=True)
    semeia()

    print("\n===== stage 1: per-study calls under the full frozen net set (CALC3E7)", flush=True)
    base = (D5 / "prompts" / "e5-calc2.txt").read_text(encoding="utf-8")
    for tid in h3.TRIALS:
        if (D5 / "saidas" / RUNG / f"{tid}.json").exists():
            print(f"  skipping {RUNG} {tid} (exists)", flush=True)
            continue
        e5.roda_estudo(RUNG, tid, base, pasta_fichas=SEED)

    print("\n===== stage 2: pooling (G3b instruments)", flush=True)
    if (D5 / f"resultados-{POOLR}.json").exists():
        print(f"  skipping {POOLR} (exists)", flush=True)
    else:
        e5.roda_g3(origem=RUNG, rotulo=POOLR)
    pool_reg = json.loads((D5 / f"resultados-{POOLR}.json").read_text(encoding="utf-8"))
    proprios = e5.sextetos_do_g2b(RUNG)

    print("\n===== stage 3+4: totals by code · product coherence check · synthesis", flush=True)
    linhas, total_n = [], 0
    incoerentes = []
    for rot, d in proprios.items():
        s = d["sexteto"]
        n = int(s[2] + s[5])
        total_n += n
        f = d["final"] or {}
        ic = f.get("ic95")
        coerente = bool(ic) and f.get("md") is not None and ic[0] - 1e-9 <= f["md"] <= ic[1] + 1e-9
        if coerente:
            linhas.append(f"- {rot}: MD {f.get('md')} IC95 {ic} · participantes: {n}")
        else:
            incoerentes.append(rot)
            linhas.append(f"- {rot}: MD {f.get('md')} · IC95 REPORTADO INVALIDO "
                          f"(o intervalo {ic} nao contem o proprio MD; nao usar) · participantes: {n}")
        d["coerente"] = coerente
    if incoerentes:
        print(f"  FLAGGED incoherent reported CIs (never endorsed): {incoerentes}", flush=True)
    else:
        print("  no incoherent reported CIs", flush=True)
    ag = pool_reg.get("final") or pool_reg["pool_sobre_os_proprios_sextetos"]
    i2 = pool_reg["pool_sobre_os_proprios_sextetos"].get("i2_pct")
    dados = ("AGREGADO (DerSimonian-Laird): MD " + str(ag.get("md")) + " IC95 " + str(ag.get("ic95"))
             + f" · I2 = {i2}%\nESTUDOS: {len(proprios)} · PARTICIPANTES TOTAIS: {total_n}\n"
             + "\n".join(linhas))
    if (PIPE / "sintese.md").exists():
        sintese = (PIPE / "sintese.md").read_text(encoding="utf-8").split("\n\n", 1)[-1].strip()
        print("  skipping synthesis (exists; product reused)", flush=True)
    else:
        prompt = (D5 / "prompts" / "e5-sintese.txt").read_text(encoding="utf-8").replace("{DADOS}", dados)
        r = h3.gerar(e5.MODELO, prompt, max_tokens=600)
        sintese = r["content"].strip()
    fornecidos = set(re.findall(r"-?\d+(?:\.\d+)?", dados.replace("−", "-")))
    orfaos = [x for x in re.findall(r"-?\d+(?:[.,]\d+)?", sintese.replace("−", "-"))
              if x.replace(",", ".") not in fornecidos
              and x.replace(",", ".").lstrip("-") not in fornecidos
              and not re.fullmatch(r"\d{1,2}|95|150|300", x)]
    print(f"  orphans: {orfaos if orfaos else 'ZERO'}", flush=True)

    print("\n===== stage 5: forest by code", flush=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8.2, 4.4), dpi=200)
    ax.axvline(0, color="#555", lw=1)
    ordem = list(proprios.items())
    for i, (rot, d) in enumerate(ordem):
        f = d["final"] or {}
        y = len(ordem) - i
        if d.get("coerente"):
            ax.plot(f["ic95"], [y, y], color="#2e5fa3", lw=2)
            ax.plot(f.get("md"), y, "s", ms=7, color="#2e5fa3")
        elif f.get("md") is not None:
            ax.plot(f["md"], y, "s", ms=7, color="#b3541e")
            ax.annotate("invalid CI*", (f["md"], y), xytext=(9, -3.5),
                        textcoords="offset points", fontsize=8.2, color="#b3541e")
        ax.text(-0.02, y, rot, ha="right", va="center", fontsize=9, transform=ax.get_yaxis_transform())
    if any(not d.get("coerente") for _, d in ordem):
        fig.text(0.12, -0.02, "* CI reported by the model does not contain its own MD — "
                 "flagged and excluded from the plot; the pool uses the executed sextets, not this CI.",
                 fontsize=7.8, color="#b3541e")
    ax.plot(ag["ic95"], [0, 0], color="#12315e", lw=3)
    ax.plot(ag["md"], 0, "D", ms=11, color="#12315e")
    ax.text(-0.02, 0, "POOLED (DL)", ha="right", va="center", fontsize=9.5,
            fontweight="bold", transform=ax.get_yaxis_transform())
    ax.set_yticks([])
    ax.set_xlabel("HbA1c mean difference, % (negative favors lower-carbohydrate)", fontsize=9)
    ax.set_title("Study 7 / Amendment 3 — clean texts, model under the frozen ten-net harness", fontsize=10)
    ax.spines[["left", "top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(PIPE / "forest-harness-e7.png", bbox_inches="tight", facecolor="white")

    print("\n===== grader-side comparison (AFTER the run; nothing above saw a key)", flush=True)
    det = json.loads((E7 / "resultados-ma2.json").read_text(encoding="utf-8"))
    verdade = h3.pool_dl_md([e["sexteto"] for e in det["por_estudo"]])
    consist = pool_reg["consistente"]
    resumo = dict(agregado_do_modelo=ag,
                  verdade_mecanica_mesmas_fichas=verdade,
                  delta_md=round(abs(ag["md"] - verdade["md"]), 2),
                  publicado={"md": -0.24, "ic95": [-0.32, -0.16], "i2_pct": 6},
                  flags_coerencia_produto=incoerentes,
                  consistente_pooling=consist, participantes=total_n,
                  numeros_orfaos=orfaos, sintese=sintese,
                  minutos=round((time.time() - t0) / 60, 1))
    (PIPE / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1),
                                      encoding="utf-8")
    (PIPE / "sintese.md").write_text("# Synthesis — Amendment 3 harness run (100% gemma4:12b)\n\n"
                                     + sintese + "\n", encoding="utf-8")
    print(f"  model pool: {json.dumps(ag, ensure_ascii=False)}", flush=True)
    print(f"  mechanical truth (same sheets): {json.dumps(verdade, ensure_ascii=False)} · "
          f"delta md {resumo['delta_md']}", flush=True)
    print(f"  published (grader-side only): -0.24 [-0.32, -0.16]", flush=True)
    print(f"\n== AMENDMENT 3 RUN COMPLETE in {resumo['minutos']} min · consistent: {consist} · "
          f"coherence flags: {incoerentes if incoerentes else 'none'} · orphans: {len(orfaos)}", flush=True)


if __name__ == "__main__":
    main()

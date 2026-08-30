# -*- coding: utf-8 -*-
"""EXTRAI Study 5 — the complete 100%-gemma4:12b pipeline (Amendment 3).

Every model role is gemma4:12b; the harness only detects, warns, computes on
command, and draws. Stages: per-study orchestration (G2b instruments, fresh
run, rung label G2PIPE) -> pooling (G3b instruments, over stage-1's sextets)
-> synthesis (frozen instrument, totals PRE-COMPUTED by code, orphan-number
scan) -> forest plot drawn by deterministic code.

Run: python scripts/estudo5/pipeline-gemma.py
Outputs: dados/estudo5/pipeline/ (+ stage transcripts under saidas/G2PIPE, saidas/G3PIPE)
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
PIPE = D5 / "pipeline"

_sp = importlib.util.spec_from_file_location("e5", ROOT / "scripts" / "estudo5" / "e5-harness.py")
e5 = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(e5)
h3 = e5.h3


def main():
    PIPE.mkdir(exist_ok=True)
    t0 = time.time()

    print("===== PIPELINE 100% gemma4:12b · etapa 1: cálculo por estudo (instrumentos G2b)", flush=True)
    base = (D5 / "prompts" / "e5-g2.txt").read_text(encoding="utf-8")
    for tid in h3.TRIALS:
        e5.roda_estudo("G2PIPE", tid, base)

    print("\n===== etapa 2: síntese estatística (instrumentos G3b)", flush=True)
    e5.roda_g3(origem="G2PIPE", rotulo="G3PIPE")
    pool_reg = json.loads((D5 / "resultados-G3PIPE.json").read_text(encoding="utf-8"))
    proprios = e5.sextetos_do_g2b("G2PIPE")

    print("\n===== etapa 3: totais pré-computados pelo código", flush=True)
    linhas = []
    total_n = 0
    for rot, d in proprios.items():
        s = d["sexteto"]
        n = int(s[2] + s[5])
        total_n += n
        f = d["final"] or {}
        linhas.append(f"- {rot}: MD {f.get('md')} IC95 {f.get('ic95')} · participantes: {n}")
    ag = pool_reg.get("final") or pool_reg["pool_sobre_os_proprios_sextetos"]
    i2 = pool_reg["pool_sobre_os_proprios_sextetos"].get("i2_pct")
    dados = ("AGREGADO (DerSimonian-Laird): MD " + str(ag.get("md")) + " IC95 " + str(ag.get("ic95"))
             + f" · I2 = {i2}%\nESTUDOS: {len(proprios)} · PARTICIPANTES TOTAIS: {total_n}\n"
             + "\n".join(linhas))
    print(dados, flush=True)

    print("\n===== etapa 4: síntese narrativa (gemma12; só os números fornecidos)", flush=True)
    prompt = (D5 / "prompts" / "e5-sintese.txt").read_text(encoding="utf-8").replace("{DADOS}", dados)
    r = h3.gerar(e5.MODELO, prompt, max_tokens=600)
    sintese = r["content"].strip()
    print(sintese[:400] + ("…" if len(sintese) > 400 else ""), flush=True)

    fornecidos = set(re.findall(r"-?\d+(?:\.\d+)?", dados.replace("−", "-")))
    orfaos = [x for x in re.findall(r"-?\d+(?:[.,]\d+)?", sintese.replace("−", "-"))
              if x.replace(",", ".") not in fornecidos
              and x.replace(",", ".").lstrip("-") not in fornecidos
              and not re.fullmatch(r"\d{1,2}|95|150|300", x)]
    print(f"\nchecagem anti-invencao: numeros orfaos = {orfaos if orfaos else 'ZERO'}", flush=True)

    print("\n===== etapa 5: forest plot (codigo deterministico)", flush=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8.2, 4.4), dpi=200)
    ax.axvline(0, color="#555", lw=1)
    ordem = list(proprios.items())
    for i, (rot, d) in enumerate(ordem):
        f = d["final"] or {}
        y = len(ordem) - i
        if f.get("ic95"):
            ax.plot(f["ic95"], [y, y], color="#2e5fa3", lw=2)
            ax.plot(f.get("md"), y, "s", ms=7, color="#2e5fa3")
        ax.text(-0.02, y, rot, ha="right", va="center", fontsize=9, transform=ax.get_yaxis_transform())
    ax.plot(ag["ic95"], [0, 0], color="#12315e", lw=3)
    ax.plot(ag["md"], 0, "D", ms=11, color="#12315e")
    ax.text(-0.02, 0, "AGREGADO (DL)", ha="right", va="center", fontsize=9.5,
            fontweight="bold", transform=ax.get_yaxis_transform())
    ax.set_yticks([])
    ax.set_xlabel("Diferença de médias na variação de HbA1c, % (negativo favorece low-carb)", fontsize=9)
    ax.set_title("Pipeline 100% gemma4:12b — cálculo e síntese orquestrados pelo modelo", fontsize=10)
    ax.spines[["left", "top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(PIPE / "forest-gemma.png", bbox_inches="tight", facecolor="white")

    resumo = dict(agregado_do_modelo=ag, pool_sobre_os_proprios=pool_reg["pool_sobre_os_proprios_sextetos"],
                  consistente=pool_reg["consistente"], estudos=len(proprios),
                  participantes_totais=total_n, numeros_orfaos=orfaos, sintese=sintese,
                  minutos=round((time.time() - t0) / 60, 1))
    (PIPE / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")
    (PIPE / "sintese.md").write_text("# Síntese do pipeline 100% gemma4:12b\n\n" + sintese + "\n",
                                     encoding="utf-8")
    print(f"\n== PIPELINE COMPLETO em {resumo['minutos']} min · consistente: {resumo['consistente']} · "
          f"orfaos: {len(orfaos)} · gravado em dados/estudo5/pipeline/", flush=True)


if __name__ == "__main__":
    main()

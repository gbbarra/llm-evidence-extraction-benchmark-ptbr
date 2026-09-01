# -*- coding: utf-8 -*-
"""Study 8 / P1 — factuality profile per model (grader-side extension).

Classifies each model's divergent cells (replicate 1, eligible key set) into:
- omission: the model wrote NR/empty where the source-verified key holds a value;
- invention candidate: the model's cell contains a number absent from the
  perturbed source text the model actually read (tolerance 0.005; percent
  values also checked against count/n reconstructions to avoid flagging
  derivations as inventions) -- candidates are LISTED for adjudication,
  never auto-verdicted;
- value/format divergence: everything else (numbers present in the source,
  differing from the key by route, layer or format).

Run: python scripts/estudo8/p1-factuality.py
Output: dados/estudo8/factualidade-p1.json (+ console table)
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
E8 = ROOT / "dados" / "estudo8"
CAST = ["gemma12", "qwen14", "llama8", "qwen35", "deepseek14"]
ABERTOS = ROOT / "corpus" / "perturbados"
FECHADOS = ROOT / "corpus" / "perturbados-fechados"


def texto_de(tid):
    for d in (ABERTOS, FECHADOS):
        f = d / f"{tid}.txt"
        if f.exists():
            return f.read_text(encoding="utf-8", errors="replace")
    return ""


def numeros(s):
    return {round(float(x), 4) for x in
            re.findall(r"-?\d+(?:\.\d+)?", str(s).replace("−", "-").replace("–", "-"))}


def eh_nr(v):
    return str(v or "").strip().upper() in ("NR", "NA", "N/A", "", "NONE", "NOT REPORTED")


def main():
    av = json.loads((E8 / "avaliacao-p1.json").read_text(encoding="utf-8"))
    textos = {}
    res = {}
    for modelo in CAST:
        oms, invs, val = [], [], 0
        for d in av[modelo]["divergents"]:
            tid, campo, mv = d["trial"], d["field"], d["model"]
            if eh_nr(mv):
                oms.append(dict(trial=tid, field=campo, source=d["source"]))
                continue
            if tid not in textos:
                textos[tid] = numeros(texto_de(tid))
            nums_texto = textos[tid]
            ns = numeros(mv)
            fora = {n for n in ns
                    if not any(abs(n - t) <= 0.005 for t in nums_texto)
                    and not any(abs(abs(n) - t) <= 0.005 for t in nums_texto)}
            # percentages/derivations: a number reconstructible as x/y*100 or
            # x*y/100 from two in-text numbers is a derivation, not an invention
            realmente_fora = set()
            for n in fora:
                derivavel = False
                lista = [t for t in nums_texto if 0 < t <= 100000]
                for a in lista:
                    for b in lista:
                        if b and (abs(a / b * 100 - n) <= 0.15 or abs(a * b / 100 - n) <= 0.15
                                  or abs(a - b - n) <= 0.005 or abs(a + b - n) <= 0.005):
                            derivavel = True
                            break
                    if derivavel:
                        break
                if not derivavel:
                    realmente_fora.add(n)
            if realmente_fora:
                invs.append(dict(trial=tid, field=campo, cell=str(mv)[:60],
                                 numbers_not_in_text=sorted(realmente_fora)))
            else:
                val += 1
        res[modelo] = dict(divergents=len(av[modelo]["divergents"]),
                           omissions=len(oms), omission_cells=oms,
                           invention_candidates=len(invs), invention_cells=invs,
                           value_or_format=val)
    (E8 / "factualidade-p1.json").write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                             encoding="utf-8")
    print(f"{'model':<12} {'divergents':>10} {'omissions':>10} {'invention cand.':>16} {'value/format':>13}")
    for m in CAST:
        r = res[m]
        print(f"{m:<12} {r['divergents']:>10} {r['omissions']:>10} "
              f"{r['invention_candidates']:>16} {r['value_or_format']:>13}")
    for m in CAST:
        for c in res[m]["invention_cells"]:
            print(f"  CANDIDATE {m} {c['trial']} {c['field']}: {c['cell']!r} "
                  f"-> not in text: {c['numbers_not_in_text']}")


if __name__ == "__main__":
    main()

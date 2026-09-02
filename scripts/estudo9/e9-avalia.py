# -*- coding: utf-8 -*-
"""EXTRAI Study 9 — A/B grading of the quote-bearing sheet (Anchor 1 cells).

The comparator is the campaign's, unmodified: the same eligible cell set (124
cells with a digit-bearing source-verified value), the same magnitude-based
`compat`, the same sealed `desperturba` lens (held constant across both arms by
amendment A9-2, collision included). Verified before use: the frozen reader
already takes `.get("value")` from an object cell, so a v2 cell
{value, where, quote} is consumed by exactly the same code as a v1 cell
{value, where} -- no adapter, no grader difference between the arms.

Arm B lives in two different places, per A9-3:
  gemma12 / qwen14 / llama8  -> the ARCHIVED campaign sheets (Study-8 P1)
  granite8                   -> its own v1 arm, run inside this study

Run: python scripts/estudo9/e9-avalia.py [model ...]
Out: dados/estudo9/avaliacao-ab.json (+ console A/B table)
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
E8, E9 = ROOT / "dados" / "estudo8", ROOT / "dados" / "estudo9"
CAST = ["granite8", "gemma12", "qwen14", "llama8"]
ARQUIVADO = {"gemma12", "qwen14", "llama8"}  # arm B = campaign record


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


e6a = carrega("e6a", "scripts/estudo6/e6-avalia.py")
e7d = carrega("e7d", "scripts/estudo7/e7-downstream.py")
d6, compat = e6a.d6, e6a.compat
PT2EN = {v: k for k, v in e7d.MA1_EN2PT.items()}


def eleg():
    """The campaign's eligible cell set, rebuilt by the same rule."""
    out = {}
    for tid, campos in d6.GAB.items():
        for campo, cel in campos.items():
            vf, ver = cel.get("valor_fonte"), str(cel.get("veredito"))
            if vf in (None, "") or ver in ("sem-valor-na-ma", "pendente-adjudicacao",
                                           "nao-sustentada", "dado-fora-do-insumo"):
                continue
            if re.search(r"\d", str(vf)):
                out.setdefault(tid, []).append(campo)
    return out


def caminho(modelo, arm, tid, rep):
    if arm == "A":
        return E9 / "saidas" / "v2" / modelo / "ma1" / f"{tid}-r{rep}.json"
    if modelo in ARQUIVADO:
        return E8 / "saidas" / "p1" / modelo / f"{tid}-r{rep}.json"
    return E9 / "saidas" / "v1" / modelo / "ma1" / f"{tid}-r{rep}.json"


def folha(modelo, arm, tid, rep):
    f = caminho(modelo, arm, tid, rep)
    if not f.exists():
        return None
    return d6.h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])


def valor_en(js, campo_pt):
    v = (js or {}).get(PT2EN[campo_pt])
    if isinstance(v, dict):
        v = v.get("value")
    return None if v is None else str(v)


def pt_form(js):
    return {pt: {"valor": valor_en(js, pt) or ""} for pt in PT2EN}


def grade(modelo, arm, E):
    boas = tot = est_ig = est_tot = 0
    faltando, divergentes = [], []
    for tid, campos in E.items():
        r1, r2 = folha(modelo, arm, tid, 1), folha(modelo, arm, tid, 2)
        if r1 is None and r2 is None:
            faltando.append(tid)
            continue
        js = r1 or r2
        rev = d6.desperturba(tid, pt_form(js))
        for campo in campos:
            fonte = d6.GAB[tid][campo].get("valor_fonte")
            tot += 1
            ok = compat((rev.get(campo) or {}).get("valor"), fonte)
            boas += ok
            if not ok:
                divergentes.append(dict(trial=tid, field=campo,
                                        model=valor_en(js, campo), source=str(fonte)[:60]))
            if r1 is not None and r2 is not None:
                est_tot += 1
                est_ig += compat(valor_en(r1, campo), valor_en(r2, campo))
    return dict(cells=boas, graded=tot,
                cells_pct=round(100 * boas / max(tot, 1), 1),
                stability=est_ig, stability_of=est_tot,
                stability_pct=round(100 * est_ig / max(est_tot, 1), 1),
                missing_trials=faltando, divergents=divergentes)


def main():
    alvo = sys.argv[1:] or CAST
    E = eleg()
    n_elig = sum(len(v) for v in E.values())
    print(f"\n=== Study 9 A/B · Anchor 1 · {n_elig} eligible key cells per model ===")
    print("grader: the campaign's, unmodified; lens held constant across arms (A9-2)\n")
    print(f"{'model':<10}{'arm':<5}{'cells':>14}{'stability':>14}   note")
    res = {}
    for modelo in alvo:
        res[modelo] = {}
        for arm, rot in (("B", "v1"), ("A", "v2")):
            r = grade(modelo, arm, E)
            res[modelo][rot] = r
            if r["graded"] == 0:
                print(f"{modelo:<10}{rot:<5}{'(not run yet)':>14}")
                continue
            nota = f"{len(r['missing_trials'])} trial(s) absent" if r["missing_trials"] else ""
            cel = f"{r['cells']}/{r['graded']} ({r['cells_pct']}%)"
            est = f"{r['stability']}/{r['stability_of']} ({r['stability_pct']}%)"
            print(f"{modelo:<10}{rot:<5}{cel:>16}{est:>18}   {nota}")
        a, b = res[modelo].get("v2", {}), res[modelo].get("v1", {})
        if a.get("graded") and b.get("graded"):
            dc = f"{a['cells'] - b['cells']:+d} cells"
            ds = f"{a['stability_pct'] - b['stability_pct']:+.1f} pts"
            print(f"{'':<10}{'A-B':<5}{dc:>16}{ds:>18}   v2 minus v1 (the estimand)")
    out = E9 / "avaliacao-ab.json"
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nsaved: {out}")


if __name__ == "__main__":
    main()

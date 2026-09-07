# -*- coding: utf-8 -*-
"""Study 8 — Amendment 1 (2026-09-07): invention screen over the Anchor-2 (P3-b) sheets, all models.

Re-implements, for the continuous sheets, the P1 factuality rule (p1-factuality.py): a cell is an
INVENTION CANDIDATE when it contains a number absent from the perturbed text the model actually read
(tolerance 0.005) and not derivable from printed numbers by sum, difference, mean, half-width or
percentage. Candidates are LISTED for adjudication, never auto-verdicted. Cells screened: the 16
numeric fields of the English continuous sheet (8 per arm); non-numeric fields (labels, descriptions,
dispersion type) are not screened. Run over the whole extended cast so the five-model record serves
as the reimplementation's own check.

Run: python scripts/estudo8/p3b-invention-screen.py
Output: dados/estudo8/invencao-p3b.json (+ console table)
"""
import itertools
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
E8 = ROOT / "dados" / "estudo8"
PERT = ROOT / "corpus" / "estudo3" / "perturbados"
CAST = ["gemma12", "qwen14", "llama8", "qwen35", "deepseek14", "qwen27q2"]
CAMPOS = ["n_randomized", "n_analyzed", "hba1c_change_mean", "hba1c_change_dispersion",
          "hba1c_baseline_mean", "hba1c_baseline_sd", "hba1c_final_mean", "hba1c_final_sd"]
TOL = 0.005
NUM = re.compile(r"(?<![\w.])[-−–]?\d+(?:[.,]\d+)?(?![\w])")


def numeros(texto):
    out = []
    for m in NUM.finditer(texto):
        s = m.group(0).replace("−", "-").replace("–", "-").replace(",", ".")
        try:
            out.append(float(s))
        except ValueError:
            pass
    return out


def derivados(nums):
    """Set of values derivable from pairs of printed numbers (rounded to 3 decimals)."""
    base = sorted(set(round(x, 3) for x in nums))
    d = set(base)
    for a, b in itertools.combinations(base, 2):
        d.add(round(a + b, 3)); d.add(round(a - b, 3)); d.add(round(b - a, 3))
        d.add(round((a + b) / 2, 3)); d.add(round(abs(a - b) / 2, 3))
        if b:
            d.add(round(100 * a / b, 1))
        if a:
            d.add(round(100 * b / a, 1))
    return d


def presente(x, base, deriv):
    if any(abs(x - y) <= TOL for y in base):
        return "printed"
    if any(abs(x - y) <= TOL for y in deriv):
        return "derived"
    return None


def ficha(p):
    j = json.loads(p.read_text(encoding="utf-8"))
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", (j.get("content") or "").strip())
    try:
        return json.loads(t)
    except Exception:
        m = re.search(r"\{.*\}", t, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
    return None


def main():
    textos = {}
    for p in sorted(PERT.glob("*.txt")):
        nums = numeros(p.read_text(encoding="utf-8"))
        textos[p.stem] = (nums, derivados(nums))
    res = {}
    print(f"{'model':10s} {'sheets':>6s} {'cells':>6s} {'numbers':>8s} {'printed':>8s} {'derived':>8s} {'invention cand.':>16s}")
    for m in CAST:
        pasta = E8 / "saidas" / "p3b" / m
        if not pasta.exists():
            continue
        cont = dict(sheets=0, cells=0, numbers=0, printed=0, derived=0, candidates=[])
        for p in sorted(pasta.glob("*.json")):
            tid = p.stem.rsplit("-r", 1)[0]
            s = ficha(p)
            if not s or tid not in textos:
                continue
            cont["sheets"] += 1
            base, deriv = textos[tid]
            for braco in ("experimental_arm", "control_arm"):
                arm = s.get(braco) or {}
                for campo in CAMPOS:
                    v = arm.get(campo)
                    if isinstance(v, dict):
                        v = v.get("value")
                    if v is None:
                        continue
                    cont["cells"] += 1
                    for x in numeros(str(v)):
                        cont["numbers"] += 1
                        how = presente(x, base, deriv)
                        if how:
                            cont[how] += 1
                        else:
                            cont["candidates"].append(dict(sheet=p.name, arm=braco, field=campo, value=str(v), number=x))
        res[m] = cont
        print(f"{m:10s} {cont['sheets']:6d} {cont['cells']:6d} {cont['numbers']:8d} {cont['printed']:8d} {cont['derived']:8d} {len(cont['candidates']):16d}")
        for c in cont["candidates"]:
            print(f"    ? {c['sheet']} {c['arm']}.{c['field']} = {c['value']!r} (number {c['number']})")
    (E8 / "invencao-p3b.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved:", E8 / "invencao-p3b.json")


if __name__ == "__main__":
    main()

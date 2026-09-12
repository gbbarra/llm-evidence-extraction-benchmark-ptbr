# -*- coding: utf-8 -*-
"""Regression test for the Study 12 grader artifact of 2026-09-12: a v2 sheet whose dispersion type comes as
{"value","where","quote"} must yield the same routed cells as the v1 sheet carrying the same strings.
Runs without the models and without the campaign outputs."""
import importlib.util
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, RAIZ / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


e7d = carrega("e7d", "scripts/estudo7/e7-downstream.py")
dg = carrega("dg", "scripts/estudo3/dirigida.py")

V1 = {"n_analyzed": "11", "hba1c_change_mean": "-0.8", "hba1c_change_dispersion": "-1.1 to -0.6",
      "hba1c_change_dispersion_type": "CI95: -1.1 to -0.6", "hba1c_baseline_mean": "5.8",
      "hba1c_baseline_sd": "0.4", "hba1c_final_mean": "NR", "hba1c_final_sd": "NR"}
V2 = {k: {"value": v, "where": "Table 2", "quote": "…"} for k, v in V1.items()}
V1_SE = dict(V1, hba1c_change_dispersion="0.07", hba1c_change_dispersion_type="SE", n_analyzed="45")
V2_SE = {k: {"value": v, "where": "Results", "quote": "…"} for k, v in V1_SE.items()}

falhas = []


def confere(nome, a, b):
    ra = dg.braco_deterministico(e7d.braco_pt(a), {}, ("x", "exp"))
    rb = dg.braco_deterministico(e7d.braco_pt(b), {}, ("x", "exp"))
    ok = ra == rb and ra[1] is not None
    print(f"  {'ok  ' if ok else 'FALHA'} {nome}: v1 → {ra} · v2 → {rb}")
    if not ok:
        falhas.append(nome)


print("v2 type field: the object must route exactly like the v1 string")
confere("CI95 → SD derived from the interval (0.42 at n=11)", V1, V2)
confere("SE → SD derived from the standard error (0.47 at n=45)", V1_SE, V2_SE)

# the Study 12 grader path itself, when the campaign module is importable
try:
    M2 = carrega("p2m", "scripts/estudo12/e12-p2.py")
    js1 = {"experimental_arm": V1, "control_arm": V1, "n_randomized_total": "25"}
    js2 = {"experimental_arm": V2, "control_arm": V2, "n_randomized_total": {"value": "25", "where": "", "quote": ""}}
    c1 = M2.celulas_a2(js1, "PMC5329646", False)
    c2 = M2.celulas_a2(js2, "PMC5329646", False)
    ok = all(str(c1[k]) == str(c2[k]) for k in M2.CELULAS_A2) and c2["exp_dispersao"] is not None
    print(f"  {'ok  ' if ok else 'FALHA'} e12-p2.celulas_a2: v1 {c1} · v2 {c2}")
    if not ok:
        falhas.append("celulas_a2")
except Exception as e:  # the campaign module needs the record on disk; report, do not hide
    print("  (e12-p2 not exercised here:", str(e)[:120], ")")

if falhas:
    raise SystemExit("FALHAS: " + ", ".join(falhas))
print("TODAS PASSAM.")

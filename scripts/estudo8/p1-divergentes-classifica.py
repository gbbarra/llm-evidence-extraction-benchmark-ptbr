# -*- coding: utf-8 -*-
"""Classify every Study-8 P1 divergent cell by mechanism (Supplementary Tables S1-S7).

Mechanical passes only; the final published classes (equivalent re-encoding vs
row/scope slip vs unmatched re-expression) were refined by source-open,
quotation-bound verification recorded in dados/estudo8/avaliacao-p1.md
(section of 2026-09-01). Output: dados/estudo8/divergentes-classificados.json.

Classes:
  lookup-collision : raw already magnitude-compatible with the key's source value,
                     but the seal reversal corrupted it (grader-side artifact).
  layer-choice     : model's number matches the key's MA layer (analyzed counts)
                     instead of the source layer (randomized).
  omission         : model wrote NR where the source reports a value.
  summary          : qualitative field (surgery type) summarized instead of the
                     key's enumerated case-mix.
  re-encoding      : same underlying data re-expressed (percent vs counts, ratio
                     notation, rearranged n/% pair).  (default for the rest —
                     each printed for manual inspection)
"""
import importlib.util, json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"C:\Users\gbbarra\Documents\localtts\extrai")

def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m

e6a = carrega("e6a", "scripts/estudo6/e6-avalia.py")
e7d = carrega("e7d", "scripts/estudo7/e7-downstream.py")
d6, compat = e6a.d6, e6a.compat
PT2EN = {v: k for k, v in e7d.MA1_EN2PT.items()}
CAST = ["gemma12", "qwen14", "llama8", "qwen35", "deepseek14"]
SIG = {"gemma12": "G", "qwen14": "Q14", "llama8": "L", "qwen35": "Q35", "deepseek14": "D"}
E8 = ROOT / "dados" / "estudo8"

def eh_nr(v):
    return str(v or "").strip().upper() in ("NR", "NA", "N/A", "", "NONE", "NOT REPORTED")

def nums(s):
    return re.findall(r"\d+(?:\.\d+)?", str(s or ""))

def bruta(modelo, tid):
    for rep in (1, 2):
        f = E8 / "saidas" / "p1" / modelo / f"{tid}-r{rep}.json"
        if f.exists():
            js = d6.h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
            if js is not None:
                return js
    return None

def valor_en(js, campo_pt):
    v = (js or {}).get(PT2EN[campo_pt])
    if isinstance(v, dict):
        v = v.get("value")
    return None if v is None else str(v)

# rebuild each model's reversed sheet once per trial
av = json.loads((E8 / "avaliacao-p1.json").read_text(encoding="utf-8"))
linhas = []
cache = {}
for modelo in CAST:
    for dvt in av[modelo]["divergents"]:
        tid, campo = dvt["trial"], dvt["field"]
        js = cache.get((modelo, tid))
        if js is None:
            js = bruta(modelo, tid); cache[(modelo, tid)] = js
        cel = {p: {"valor": valor_en(js, p) or ""} for p in PT2EN}
        rev = d6.desperturba(tid, cel)[campo]["valor"]
        gcel = d6.GAB[tid][campo]
        fonte, ma = gcel.get("valor_fonte"), gcel.get("ma")
        raw = dvt["model"]
        if eh_nr(raw):
            cls = "omission"
        elif compat(raw, fonte) or compat(rev, fonte) is False and compat(raw, fonte):
            cls = "lookup-collision" if compat(raw, fonte) else "?"
        else:
            cls = None
        if cls is None:
            if campo == "tipo_cirurgia":
                cls = "summary"
            elif ma is not None and not eh_nr(ma) and compat(rev, ma):
                cls = "layer-choice"
            elif ma is not None and not eh_nr(ma) and compat(raw, ma):
                cls = "layer-choice(raw)"
            else:
                cls = "re-encoding?"
        linhas.append(dict(trial=tid, field=campo, model=SIG[modelo], raw=raw,
                           rev=rev, fonte=str(fonte), ma=str(ma), cls=cls))

# ---- report ----
from collections import Counter, defaultdict
cnt = Counter((l["cls"] for l in linhas))
print("per-cell class counts (124 total):", dict(cnt))
percls = defaultdict(list)
for l in linhas:
    percls[l["cls"]].append(l)
for cls in ("lookup-collision", "layer-choice", "layer-choice(raw)", "re-encoding?"):
    print(f"\n=== {cls} ({len(percls[cls])}) ===")
    for l in percls[cls]:
        print(f"{l['trial']:<12} {l['field']:<26} {l['model']:<4}")
        print(f"    raw: {l['raw']!r}"[:120])
        if l["rev"] != l["raw"]:
            print(f"    rev: {l['rev']!r}"[:120])
        print(f"    key: {l['fonte']!r}"[:120])
        if l["ma"] not in ("None", ""):
            print(f"    ma : {l['ma']!r}"[:100])
out = ROOT / "dados" / "estudo8" / "divergentes-classificados.json"
out.write_text(json.dumps(linhas, ensure_ascii=False, indent=1), encoding="utf-8")
print("\nsaved:", out)

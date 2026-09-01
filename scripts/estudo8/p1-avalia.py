# -*- coding: utf-8 -*-
"""Study 8 / P1 READ — grading the five-model English-instrument extraction.

Per model, over the eligible cell set (the corrected two-layer key's cells
with a usable, digit-bearing valor_fonte — the same set Studies 6-7 graded):
- cells: seal-reversed values vs the key's source layer (Study 6's magnitude
  comparator, declared an approximation; residue goes to adjudication);
- stability: replicate 1 vs replicate 2, raw;
- recitation candidates: cells whose RAW text contains a seal pair's ORIGINAL
  value while its perturbed image (which the model actually read) is absent —
  the mechanical recall signal; candidates are listed for adjudication, never
  auto-verdicted.

Run: python scripts/estudo8/p1-avalia.py
Output: dados/estudo8/avaliacao-p1.json (+ console table)
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


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


e6a = carrega("e6a", "scripts/estudo6/e6-avalia.py")   # compat, nums_de, d6 (GAB, SELO, desperturba)
e7d = carrega("e7d", "scripts/estudo7/e7-downstream.py")  # MA1_EN2PT, h3.acha_json via d6
d6 = e6a.d6
compat = e6a.compat
PT2EN = {v: k for k, v in e7d.MA1_EN2PT.items()}


def eleg():
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


def bruta(modelo, tid, rep):
    f = E8 / "saidas" / "p1" / modelo / f"{tid}-r{rep}.json"
    if not f.exists():
        return None
    return d6.h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])


def valor_en(js, campo_pt):
    v = (js or {}).get(PT2EN[campo_pt])
    if isinstance(v, dict):
        v = v.get("value")
    return None if v is None else str(v)


def pt_form(js):
    """EN sheet -> PT-keyed cell dict, so d6.desperturba applies verbatim."""
    return {pt: {"valor": valor_en(js, pt) or ""} for pt in PT2EN}


def recitacoes(tid, raw_cell):
    """Seal pairs whose ORIGINAL appears in the raw cell while the perturbed
    image (what the model actually read) is absent."""
    hits = []
    s = str(raw_cell or "")
    for reg in d6.SELO.get(tid, []):
        o, p = str(reg["original"]), str(reg["perturbado"])
        if o and p and o != p and o in s and p not in s:
            hits.append((o, p))
    return hits


def main():
    E = eleg()
    res = {}
    for modelo in CAST:
        boas = tot = est_ig = est_tot = 0
        parse_fail = []
        pend, recs = [], []
        for tid, campos in E.items():
            r1 = bruta(modelo, tid, 1)
            r2 = bruta(modelo, tid, 2)
            if r1 is None and r2 is None:
                parse_fail.append(tid)
                continue
            js = r1 or r2
            rev = d6.desperturba(tid, pt_form(js))
            for campo in campos:
                raw = valor_en(js, campo)
                fonte = d6.GAB[tid][campo].get("valor_fonte")
                tot += 1
                ok = compat((rev.get(campo) or {}).get("valor"), fonte)
                boas += ok
                if not ok:
                    pend.append(dict(trial=tid, field=campo, model=raw,
                                     source=str(fonte)[:60]))
                for o, p in recitacoes(tid, raw):
                    recs.append(dict(trial=tid, field=campo, original=o, perturbed=p,
                                     cell=str(raw)[:50]))
                if r1 is not None and r2 is not None:
                    est_tot += 1
                    est_ig += compat(valor_en(r1, campo), valor_en(r2, campo))
        res[modelo] = dict(
            cells=f"{boas}/{tot} ({round(100 * boas / max(tot, 1), 1)}%)",
            stability=f"{est_ig}/{est_tot} ({round(100 * est_ig / max(est_tot, 1), 1)}%)",
            recitation_candidates=len(recs), recitations=recs,
            parse_failures=parse_fail, divergents=pend)
    (E8 / "avaliacao-p1.json").write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                          encoding="utf-8")
    print(f"{'model':<12} {'cells vs key':<18} {'stability r1-r2':<18} "
          f"{'recit.cand.':<12} {'parse-fail'}")
    for m in CAST:
        r = res[m]
        print(f"{m:<12} {r['cells']:<18} {r['stability']:<18} "
              f"{r['recitation_candidates']:<12} {len(r['parse_failures'])}")


if __name__ == "__main__":
    main()

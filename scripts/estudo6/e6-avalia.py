# -*- coding: utf-8 -*-
"""Study 6 — cell grading (H6.1) and extraction stability (H6.3).

H6.1: each fresh sheet's cells, seal reversed, against the two-layer key's
source-verified values (cells whose key holds a usable valor_fonte).
H6.3: fresh vs archived gemma12 sheets, same perturbed world, agreement on
the graded fields.

Run: python scripts/estudo6/e6-avalia.py
Output: dados/estudo6/avaliacao-celulas.json
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
D6 = ROOT / "dados" / "estudo6"
ARQ = ROOT / "dados" / "estudo1" / "saidas" / "gemma12"

_d = importlib.util.spec_from_file_location("d6", ROOT / "scripts" / "estudo6" / "e6-downstream.py")
d6 = importlib.util.module_from_spec(_d)
_d.loader.exec_module(d6)


def nums_de(s):
    # a hyphen between digits is a range separator, not a minus sign
    return [float(x) for x in re.findall(r"(?<![\d.])-?\d+(?:\.\d+)?", str(s).replace("−", "-"))]


def compat(modelo, fonte):
    """Mechanical approximation of the E1 ruler's equivalences: every nonzero
    number the SOURCE records must appear in the model's cell (format-free);
    the key's semantic zero ('0 (…)') accepts the model's NR; numberless
    source values compare as loose text."""
    if modelo is None or fonte is None:
        return False
    sm, sf = str(modelo).strip(), str(fonte).strip()
    if sf.startswith("0 (") and sm.upper() in ("NR", "NA", "0"):
        return True
    if sm.upper() in ("NR", "NA", "") or sf.upper() in ("NR", "NA", ""):
        return sm.upper()[:2] == sf.upper()[:2]
    nm, nf = nums_de(sm), nums_de(sf)
    nf_nz = [x for x in nf if x != 0]
    nm_nz = [x for x in nm if x != 0]
    if nf_nz and nm_nz:
        # magnitudes only: a hyphen after a unit ("837 ml-2100") is a range
        # separator, not a minus; T1 source values carry no signed quantities
        am = [abs(x) for x in nm]
        af = [abs(x) for x in nf]
        cobre = all(any(abs(x - y) <= 0.01 for y in am) for x in map(abs, nf_nz))
        contido = all(any(abs(x - y) <= 0.01 for y in af) for x in map(abs, nm_nz))
        return cobre or contido
    return sm.lower()[:16] == sf.lower()[:16] or sf.lower()[:24] in sm.lower() \
        or sm.lower()[:24] in sf.lower()


def ficha_arquivada(tid):
    for rep in (1, 2):
        f = ARQ / f"{tid}-t1-r{rep}.json"
        if not f.exists():
            continue
        js = d6.h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
        if js:
            return js
    return None


def main():
    boas = tot = 0
    est_ig = est_tot = 0
    pend = []
    for tid in d6.GAB.keys():
        js = d6.ficha(tid)
        if not js:
            continue
        rev = d6.desperturba(tid, js)
        arq = ficha_arquivada(tid)
        for campo, cel in d6.GAB[tid].items():
            fonte = cel.get("valor_fonte")
            ver = str(cel.get("veredito"))
            if fonte in (None, "") or ver in ("sem-valor-na-ma", "pendente-adjudicacao",
                                              "nao-sustentada", "dado-fora-do-insumo"):
                continue
            if not re.search(r"\d", str(fonte)):
                continue  # textual cells go to adjudication, as in Study 1
            tot += 1
            ok = compat(d6.valor(rev, campo), fonte)
            boas += ok
            if not ok:
                pend.append(dict(trial=tid, campo=campo, modelo=d6.valor(rev, campo),
                                 fonte=str(fonte)[:60]))
            if arq is not None:
                est_tot += 1
                est_ig += compat(d6.valor(js, campo), d6.valor(arq, campo))
    res = dict(celulas=f"{boas}/{tot} ({round(100 * boas / tot, 1)}%)",
               estabilidade=f"{est_ig}/{est_tot} ({round(100 * est_ig / est_tot, 1)}%)",
               divergentes=pend)
    (D6 / "avaliacao-celulas.json").write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                               encoding="utf-8")
    print(f"H6.1 células (rev. vs fonte): {res['celulas']}")
    print(f"H6.3 estabilidade (fresh vs arquivada): {res['estabilidade']}")
    print(f"divergentes: {len(pend)}")
    for p in pend[:10]:
        print(f"  {p['trial']} {p['campo']}: modelo={p['modelo']!r} fonte={p['fonte']!r}")


if __name__ == "__main__":
    main()

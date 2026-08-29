# -*- coding: utf-8 -*-
"""EXTRAI Study 3 — source reconnaissance for the anchor's forest-plot cells.

For each of the 7 trials, searches the primary's plain text for every
forest-plot quantity (per-arm HbA1c change mean, SD, analyzed n) plus the
characteristics-table randomized n. Flexible matching (E1 lesson: never
rigid windows): unicode minus variants, optional %/± glue, decimal-guard
boundaries. Prints every hit with context and writes a draft JSON
(dados/estudo3/verificacao-fonte.json) for the answer-key layer.
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
TEXTS = ROOT / "corpus" / "estudo3" / "primarios-texto"
META = json.loads((ROOT / "corpus" / "estudo3" / "ma" / "ma-lowcarb-meta.json").read_text(encoding="utf-8"))

# forest ref -> corpus text id
TID = {"8": "PMC5329646", "9": "REF9", "10": "PMC9606840", "11": "PMC7535044",
       "12": "REF12", "13": "PMC6024764", "14": "PMC5048014"}
# randomized n from the anchor's characteristics table (table 1)
N_RANDOMIZED = {"8": 25, "9": 94, "10": 150, "11": 92, "12": 72, "13": 56, "14": 89}


def variants(x):
    """Numeric string variants for a forest value (abs value; sign handled in pattern)."""
    a = abs(x)
    outs = {f"{a:g}"}
    if isinstance(x, float):
        outs.add(f"{a:.2f}".rstrip("0").rstrip("."))
        outs.add(f"{a:.2f}")
        outs.add(f"{a:.1f}")
    return sorted(outs, key=len, reverse=True)


def hits(text, x, is_int=False):
    """All occurrences of a value with decimal guards; returns [(pos, snippet)]."""
    found = []
    for v in variants(x):
        v_re = re.escape(v)
        pat = rf"(?<![\d.,]){v_re}(?![\d])" if is_int else rf"(?<![\d]){v_re}(?![\d])"
        for m in re.finditer(pat, text):
            s = max(0, m.start() - 70)
            found.append((m.start(), text[s:m.end() + 70].strip()))
        if found:
            break
    dedup, seen = [], set()
    for pos, sn in sorted(found):
        if pos not in seen:
            dedup.append((pos, sn))
            seen.add(pos)
    return dedup


def main():
    draft = {}
    for e in META["forest_hba1c"]:
        ref = e["ref"]
        tid = TID[ref]
        text = (TEXTS / f"{tid}.txt").read_text(encoding="utf-8")
        print("\n" + "=" * 90)
        print(f"[{ref}] {e['estudo']} -> {tid}  ({len(text.split()):,} words)")
        cells = {
            "exp_media": (e["exp_media"], False), "exp_dp": (e["exp_dp"], False),
            "exp_n": (e["exp_n"], True), "ctl_media": (e["ctl_media"], False),
            "ctl_dp": (e["ctl_dp"], False), "ctl_n": (e["ctl_n"], True),
            "n_randomizado": (N_RANDOMIZED[ref], True),
        }
        draft[tid] = {}
        for campo, (valor, eh_int) in cells.items():
            hs = hits(text, valor, eh_int)
            status = f"{len(hs)} hit(s)" if hs else "NOT FOUND"
            print(f"  {campo:<14} {valor:>8}  {status}")
            for pos, sn in hs[:3]:
                print(f"      @{pos}: …{sn}…")
            draft[tid][campo] = {"valor_forest": valor, "ocorrencias": len(hs),
                                 "trechos": [sn for _, sn in hs[:3]]}
    out = ROOT / "dados" / "estudo3" / "verificacao-fonte.json"
    out.write_text(json.dumps(draft, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\ndraft -> {out}")


if __name__ == "__main__":
    main()

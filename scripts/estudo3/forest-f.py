# -*- coding: utf-8 -*-
"""EXTRAI Study 3 — Stage F: deterministic forest-plot render (no model).

Draws the pipeline's forest plot from Stage C's final JSON (lane L by default;
pass S to render the seeded lane) side by side with the anchor's published
values. Fidelity is judged on the numbers (Stage C grading); this figure is
presentation for the article.

Output: dados/estudo3/saidas/forest-pipeline-<lane>.png
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
D3 = ROOT / "dados" / "estudo3"
lane = sys.argv[1] if len(sys.argv) > 1 else "L"

calc = json.loads((D3 / "saidas" / "calc" / f"calc-{lane}.json").read_text(encoding="utf-8"))
final = calc.get("json_final") or {}
meta = json.loads((ROOT / "corpus" / "estudo3" / "ma" / "ma-lowcarb-meta.json").read_text(encoding="utf-8"))
pub = {e["estudo"].replace("et al. ", ""): e for e in meta["forest_hba1c"]}

linhas = final.get("por_estudo", [])
ag = final.get("agregado") or {}
n = len(linhas)

fig, ax = plt.subplots(figsize=(9, 0.62 * (n + 3) + 1.2), dpi=160)
ys = list(range(n + 1, 1, -1))
for y, est in zip(ys, linhas):
    md_, ic = est.get("md"), est.get("ic95") or [None, None]
    nome = est.get("estudo", "?")
    if md_ is None or ic[0] is None:
        ax.text(0.02, y, f"{nome}: NAO-CALCULAVEL", va="center", fontsize=9, color="#888",
                transform=ax.get_yaxis_transform())
        continue
    ax.plot(ic, [y, y], color="#112660", lw=1.6)
    ax.plot(md_, y, "s", color="#3B82F6", ms=7)
    ax.text(1.02, y, f"{md_:+.2f} [{ic[0]:+.2f}, {ic[1]:+.2f}]",
            va="center", fontsize=8.5, family="monospace", transform=ax.get_yaxis_transform())
    p = pub.get(nome) or pub.get(nome.replace(" et al.", ""))
    if p:
        ax.plot(p["md"], y - 0.22, "D", color="#bbbbbb", ms=4)
ax.set_yticks(ys)
ax.set_yticklabels([e.get("estudo", "?") for e in linhas], fontsize=9)

if ag.get("md") is not None and ag.get("ic95"):
    y0 = 0.6
    lo, hi = ag["ic95"]
    ax.fill([lo, ag["md"], hi, ag["md"]], [y0, y0 + 0.28, y0, y0 - 0.28], color="#112660")
    ax.text(1.02, y0, f"{ag['md']:+.2f} [{lo:+.2f}, {hi:+.2f}]  I2={ag.get('i2_pct', '?')}%",
            va="center", fontsize=8.5, family="monospace", weight="bold",
            transform=ax.get_yaxis_transform())
    ax.text(-0.02, y0, f"Pooled (DL, lane {lane})", va="center", ha="right", fontsize=9,
            weight="bold", transform=ax.get_yaxis_transform())
apub = meta["agrupado"]
ax.axvline(apub["md"], color="#bbbbbb", lw=1, ls=":")
ax.axvline(0, color="#333", lw=1)
ax.set_xlabel("Mean difference in HbA1c change, % (negative favors low-carb)", fontsize=9)
ax.set_title(f"EXTRAI Study 3 — pipeline forest plot (lane {lane})\n"
             f"squares/diamond: pipeline · grey dots/dotted line: anchor as published "
             f"({apub['md']} [{apub['ic95'][0]}, {apub['ic95'][1]}])", fontsize=9.5)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.set_ylim(0, n + 2)
plt.tight_layout()
out = D3 / "saidas" / f"forest-pipeline-{lane}.png"
plt.savefig(out, bbox_inches="tight")
print(f"forest salvo: {out}")

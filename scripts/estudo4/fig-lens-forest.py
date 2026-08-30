# -*- coding: utf-8 -*-
"""Paper-2 figure: the answer — five unperturbation lenses vs the published value.

For each extractor, the pooled MD after the graders reverse the sealed
perturbations on its own sheets, against the anchor's published diamond
(-0.24 [-0.32, -0.16]). Values from dados/estudo4/rodada2/avaliacao-mecanica-*.json.
Output: paper/lens-vs-anchor.png (print, 200 dpi).
"""
import json
import glob
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
f = glob.glob(str(ROOT / "dados/estudo4/rodada2/avaliacao-mecanica-*.json"))[0]
aval = json.loads(Path(f).read_text(encoding="utf-8"))
ORDEM = ["gemma12", "qwen14", "qwen35", "llama8", "deepseek14"]
NOMES = {"gemma12": "gemma4:12b", "qwen14": "qwen3:14b", "qwen35": "qwen3.5:9b",
         "llama8": "llama3.1:8b", "deepseek14": "deepseek-r1:14b"}

fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=200)
ax.axvspan(-0.32, -0.16, color="#c8d6c8", alpha=0.55, zorder=1,
           label="anchor as published: $-0.24$ $[-0.32, -0.16]$")
ax.axvline(-0.24, color="#3e6b4f", lw=1.2, ls=(0, (4, 2)), zorder=2)

for i, m in enumerate(ORDEM):
    lens = aval["modelos"][m]["lente_desperturbada"]
    md, (lo, hi) = lens["md"], lens["ic95"]
    cobre = aval["modelos"][m]["pool_pipeline"]  # coverage from estudos count
    n_pool = len([e for e in json.loads((ROOT / "dados/estudo4/rodada2/resultados" / f"{m}.json")
                                        .read_text(encoding="utf-8"))["por_estudo"] if "sexteto" in e])
    dentro = -0.32 <= md <= -0.16
    cor = "#2e5fa3" if dentro else "#8a8f98"
    y = len(ORDEM) - 1 - i
    ax.plot([lo, hi], [y, y], color=cor, lw=2.2, zorder=3)
    ax.plot(md, y, marker="D", ms=9, color=cor, zorder=4)
    ax.annotate(f"{md:.2f} [{lo:.2f}, {hi:.2f}] · {n_pool}/7 trials",
                (hi, y), xytext=(8, -3.5), textcoords="offset points", fontsize=8.6, color="#333")
    peso = "bold" if dentro else "normal"
    ax.text(-1.02, y, NOMES[m], ha="left", va="center", fontsize=10, fontweight=peso, color=cor)

ax.set_yticks([])
ax.set_ylim(-0.7, len(ORDEM) - 0.3)
ax.set_xlim(-1.05, 0.12)
ax.set_xlabel("Pooled mean difference in HbA1c change, % — sealed perturbations reversed", fontsize=9.5)
ax.spines[["left", "top", "right"]].set_visible(False)
ax.legend(loc="lower left", fontsize=8.6, frameon=False)
ax.set_title("Does the chain reconstruct the literature? Five extractors, one deterministic pipeline",
             fontsize=10.5, pad=10)
fig.tight_layout()
out = ROOT / "paper" / "lens-vs-anchor.png"
fig.savefig(out, bbox_inches="tight", facecolor="white")
print(f"gravado {out}")

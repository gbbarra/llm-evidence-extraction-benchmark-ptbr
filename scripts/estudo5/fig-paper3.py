# -*- coding: utf-8 -*-
"""Paper-3 figure: the ladder's cost curve and the lens that never moves.

Left: harness complexity (active detection-only nets) per rung vs the
per-study orchestration outcome. Right: three independent fresh
extractions, three unperturbation lenses on the published value.
Output: paper/gemma-so.png (print, 200 dpi).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AZUL, CINZA, VERDE, LARANJA = "#2e5fa3", "#8a8f98", "#3e6b4f", "#b3541e"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 4.3), dpi=200,
                               gridspec_kw={"width_ratios": [1.25, 1]})

# --- left: complexity vs orchestration outcome
rungs = ["G0", "G1", "G2b", "G2c", "v3"]
nets = [1, 2, 4, 8, 10]
exatos = [0, 5, 5, 6, 5]
notas = ["wrong-side\ndiamond", "5/7", "5/7", "6/7\n+1 flagged", "5/7 +1 route\n+1 starved"]
x = range(len(rungs))
ax1.bar(x, nets, width=0.55, color="#c9d6e8", edgecolor=AZUL, lw=1.2, label="active nets (detection-only)")
ax1.set_ylabel("active nets", color=AZUL, fontsize=9.5)
ax1.set_ylim(0, 12.5)
ax1.set_xticks(x)
ax1.set_xticklabels(rungs, fontsize=10)
ax1t = ax1.twinx()
ax1t.plot(x, exatos, "-o", color="#12315e", ms=7, lw=2, label="per-study exact (of 7)")
ax1t.set_ylim(-0.4, 7.6)
ax1t.set_ylabel("studies exact (of 7)", color="#12315e", fontsize=9.5)
DESLOC = [(14, 6), (0, -22), (0, -22), (0, 12), (-6, -34)]
for xi, (n, e, nota) in enumerate(zip(nets, exatos, notas)):
    ax1.text(xi, n - 0.55, str(n), ha="center", va="top", fontsize=8.6, color=AZUL)
    ax1t.annotate(nota, (xi, e), xytext=DESLOC[xi], textcoords="offset points",
                  ha="center", fontsize=7.6, color="#12315e")
ax1.set_title("Orchestration under the ladder: nets bought correction, not\nreliability — the residual vice is sheet-conditioned, not cured by replicates",
              fontsize=9.8)
ax1.spines[["top"]].set_visible(False)
ax1t.spines[["top"]].set_visible(False)

# --- right: the lens that never moves
ax2.axvspan(-0.32, -0.16, color="#c8d6c8", alpha=0.55, label="published: $-0.24$ $[-0.32,-0.16]$")
ax2.axvline(-0.24, color=VERDE, lw=1.2, ls=(0, (4, 2)))
lentes = [("fresh extraction 1 (Study 4 r2)", -0.24, -0.33, -0.16),
          ("fresh extraction 2 (pipeline v2)", -0.24, -0.33, -0.16),
          ("fresh extraction 3 (pipeline v3)", -0.24, -0.33, -0.16)]
for i, (nome, md, lo, hi) in enumerate(lentes):
    y = len(lentes) - i
    ax2.plot([lo, hi], [y, y], color=AZUL, lw=2.2)
    ax2.plot(md, y, "D", ms=9, color=AZUL)
    ax2.text(-0.62, y, nome, ha="left", va="center", fontsize=8.8)
ax2.set_yticks([])
ax2.set_ylim(0.3, len(lentes) + 0.7)
ax2.set_xlim(-0.65, 0.02)
ax2.set_xlabel("unperturbation lens, pooled MD in HbA1c change (%)", fontsize=8.8)
ax2.set_title("Reading never moves: three independent fresh\nextractions, three lenses on the published value",
              fontsize=9.8)
ax2.legend(loc="lower left", fontsize=7.8, frameon=False)
ax2.spines[["left", "top", "right"]].set_visible(False)

fig.tight_layout()
out = ROOT / "paper" / "gemma-so.png"
fig.savefig(out, bbox_inches="tight", facecolor="white")
print(f"gravado {out}")

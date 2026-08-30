# -*- coding: utf-8 -*-
"""Paper-2 figure: who does what in the Study-4 architecture.

Three lanes — the model under test (reads), the deterministic harness
(computes), the graders (verify) — with the judgment-trigger loop and the
three verification checks. Output: paper/who-does-what.png (print, 200 dpi).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AZUL, GRAFITE, VERDE = "#2e5fa3", "#37474f", "#3e6b4f"
FUNDO_A, FUNDO_G, FUNDO_V = "#e9f0fa", "#eceff1", "#e8f0ea"

fig, ax = plt.subplots(figsize=(13.6, 8.6), dpi=200)
ax.set_xlim(0, 136)
ax.set_ylim(0, 86)
ax.axis("off")

LANES = [(2, 44, AZUL, FUNDO_A, "THE MODEL UNDER TEST", "reads — the only stage a model touches"),
         (47, 44, GRAFITE, FUNDO_G, "THE HARNESS (deterministic code)", "computes — pre-registered, frozen, public"),
         (92, 42, VERDE, FUNDO_V, "THE GRADERS", "verify — code + adjudicator under the quotation rite")]
for x, w, cor, fundo, titulo, sub in LANES:
    ax.add_patch(FancyBboxPatch((x, 9), w, 71, boxstyle="round,pad=0.6,rounding_size=2",
                                fc=fundo, ec=cor, lw=1.4, zorder=1))
    ax.text(x + w / 2, 76.6, titulo, ha="center", va="center", fontsize=12.5,
            fontweight="bold", color=cor)
    ax.text(x + w / 2, 73.4, sub, ha="center", va="center", fontsize=9, color=cor, style="italic")


def caixa(x, y, w, h, texto, cor, fs=9.3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.45,rounding_size=1.2",
                                fc="white", ec=cor, lw=1.3, zorder=3))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs,
            color="#1a1a1a", zorder=4)


def seta(x1, y1, x2, y2, cor, estilo="-", lw=1.6, rad=0.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=13,
                                 lw=lw, color=cor, linestyle=estilo,
                                 connectionstyle=f"arc3,rad={rad}", zorder=5))


# --- model lane
caixa(6, 60, 36, 8, "reads the 7 trial reports\n(numbers deliberately perturbed;\ntwo replicates per report)", AZUL)
caixa(6, 47, 36, 8, "fills one structured sheet per trial:\nmeans, dispersions, group sizes,\ndeclared dispersion TYPE", AZUL)
caixa(6, 16, 36, 10, "answers ONE narrow question\nper fired trigger (sign convention /\nfactorial margins / missing field)\n— every answer logged", AZUL)
seta(24, 60, 24, 55.4, AZUL, lw=1.3)
ax.text(24, 12.4, "never sees a formula,\na result, or the seal", ha="center", fontsize=8.6,
        color=AZUL, style="italic")

# --- harness lane (in true execution order, top to bottom)
caixa(51, 58, 36, 8, "detects judgment triggers\nmechanically (as-printed positive,\nfactorial design, missing field)", GRAFITE)
caixa(51, 43.5, 36, 10, "ROUTE SELECTOR (fixed rules):\nwhich sheet fields become mean / SD / n;\ndeclared type picks the conversion\n(CI→SD · SE→SD · basal/final + r=0.5)", GRAFITE)
caixa(51, 29, 36, 9, "computes every number:\nper-study MD and 95% CI,\nDerSimonian–Laird pool → the diamond", GRAFITE)
seta(69, 58, 69, 53.9, GRAFITE, lw=1.3)
seta(69, 43.5, 69, 38.4, GRAFITE, lw=1.3)
ax.text(69, 24.6, "never reads the trial text; call order\nand arguments follow from the sheet alone",
        ha="center", fontsize=8.6, color=GRAFITE, style="italic")

# --- graders lane
caixa(95.5, 57, 35, 10, "grades every sheet cell against a\nSOURCE-VERIFIED key (literal quote\nrequired before any deduction)", VERDE)
caixa(95.5, 43.5, 35, 9, "recomputes the whole pool with\nindependent code — must equal the\npipeline diamond digit for digit", VERDE)
caixa(95.5, 29, 35, 9, "reverses the SEALED perturbations\nand compares the result with the\npublished value (−0.24)", VERDE)
ax.text(113, 24.6, "holds the seal; logs its own\nerrors as public errata", ha="center",
        fontsize=8.6, color=VERDE, style="italic")

# --- flows between lanes
seta(42.6, 51, 50.4, 60, "#1a1a1a", rad=-0.15)
ax.text(45.2, 57.6, "sheets", ha="center", fontsize=8.6)
seta(51, 58.2, 42.6, 22.5, AZUL, estilo=(0, (4, 2)), rad=0.22)
ax.text(38.5, 40.5, "one narrow\nquestion", ha="center", fontsize=8.3, color=AZUL,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"))
seta(42.6, 18, 53, 42.9, AZUL, estilo=(0, (4, 2)), rad=0.22)
ax.text(51.5, 22.5, "answer", ha="center", fontsize=8.3, color=AZUL,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"))
seta(87.6, 62, 95, 62, "#1a1a1a")
ax.text(91.3, 63.9, "sheets", ha="center", fontsize=8.6)
seta(87.6, 32, 94.9, 46, "#1a1a1a", rad=-0.18)
ax.text(90.6, 39.5, "diamond", ha="center", fontsize=8.6,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"))

ax.text(68, 4.2, "No model ever calls a function or sees an intermediate result · no code ever reads a trial ·"
        " no human ever types a number into the pipeline",
        ha="center", fontsize=9.8, color="#1a1a1a", fontweight="bold")

fig.tight_layout()
out = ROOT / "paper" / "who-does-what.png"
fig.savefig(out, bbox_inches="tight", facecolor="white")
print(f"gravado {out}")

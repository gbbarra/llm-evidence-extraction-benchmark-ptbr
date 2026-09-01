# -*- coding: utf-8 -*-
"""Study 7 — paired forest plots, both anchors (protocol §6).

MA-1: the three dichotomous families (structure of Study 6's figure, clean
texts). MA-2: per-study MD ours vs the anchor's published forest + both pools.

Run: python scripts/estudo7/e7-forest.py
Outputs: dados/estudo7/forest-ma1-pareado.png · forest-ma2-pareado.png
"""
import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.transforms import blended_transform_factory

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
E7 = ROOT / "dados" / "estudo7"

RES = json.loads((E7 / "resultados-por-desfecho.json").read_text(encoding="utf-8"))
RES2 = json.loads((E7 / "resultados-ma2.json").read_text(encoding="utf-8"))

PUB_POOL = {
    "morbidity": (0.778, 0.567, 1.068, "0.778 [0.567, 1.068]"),
    "mortality": (1.021, 0.446, 2.337, "1.021 [0.446, 2.337]"),
    "ileus": None,  # abstract-only RR 0.48; not comparable (confirmed erratum #16)
}
TITULO = {"morbidity": "overall morbidity (anchor T5)", "mortality": "mortality (anchor T6)",
          "ileus": "postoperative ileus (anchor T11)"}
AZUL, LARANJA = "#1a6b8a", "#b0553a"


def parse_rr(s):
    m = re.search(r"RR\s+([\d.]+)\s*\[([\d.]+),\s*([\d.]+)\]", str(s))
    return (float(m.group(1)), float(m.group(2)), float(m.group(3))) if m else None


def ma1():
    fams = ["morbidity", "mortality", "ileus"]
    alturas = [len([l for l in RES[f]["rows"] if l.get("pmcid")]) + 2.0 for f in fams]
    fig, axes = plt.subplots(3, 1, figsize=(9.6, 0.95 * sum(alturas)),
                             gridspec_kw=dict(height_ratios=alturas, hspace=0.42))
    for ax, fam in zip(axes, fams):
        tr = blended_transform_factory(ax.transAxes, ax.transData)
        linhas = [l for l in RES[fam]["rows"] if l.get("pmcid")]
        y = len(linhas) + 1.2
        for l in linhas:
            y -= 1
            nosso, pub = parse_rr(l["ours"]), parse_rr(l["published"])
            cat = l["category"].split(" (")[0]
            if nosso:
                ax.errorbar(nosso[0], y + 0.16, xerr=[[nosso[0] - nosso[1]], [nosso[2] - nosso[0]]],
                            fmt="o", color=AZUL, ms=5, capsize=2, lw=1.4)
            if pub:
                ax.errorbar(pub[0], y - 0.16, xerr=[[pub[0] - pub[1]], [pub[2] - pub[0]]],
                            fmt="D", mfc="none", color=LARANJA, ms=5, capsize=2, lw=1.2)
            rot = l["study"].replace(" et al.", "")
            if not nosso:
                rot += "\nours: NR*"
            ax.text(-0.015, y, rot, transform=tr, ha="right", va="center", fontsize=9)
            ax.text(1.015, y, cat, transform=tr, ha="left", va="center", fontsize=7.8, color="#333")
        pool = (RES[fam].get("pool") or {}).get("DL")
        if pool:
            ax.errorbar(pool["rr"], 0.15, xerr=[[pool["rr"] - pool["ic95"][0]],
                                                [pool["ic95"][1] - pool["rr"]]],
                        fmt="o", color=AZUL, ms=7, capsize=3, lw=2)
            rotulo = "Our DL pool (2 of 3)" if fam == "ileus" else "Our DL pool"
            ax.text(-0.015, 0.15, f"{rotulo}\n{pool['rr']} [{pool['ic95'][0]}, {pool['ic95'][1]}]",
                    transform=tr, ha="right", va="center", fontsize=8.2,
                    fontweight="bold", color=AZUL)
        if PUB_POOL[fam]:
            p, lo, hi, rot = PUB_POOL[fam]
            ax.errorbar(p, -0.75, xerr=[[p - lo], [hi - p]], fmt="D", mfc="none",
                        color=LARANJA, ms=7, capsize=3, lw=1.8)
            ax.text(-0.015, -0.75, f"Published pool\n{rot}", transform=tr, ha="right",
                    va="center", fontsize=8.2, fontweight="bold", color=LARANJA)
        else:
            ax.text(0.0, -0.75, "Published pool (abstract): RR 0.48 — not comparable by "
                    "construction (confirmed erratum #16)\n*Castro's source does not report "
                    "ileus; the published numbers are its PPC counts", transform=tr,
                    va="center", fontsize=8.2, style="italic", color=LARANJA)
        ax.axvline(1, color="#999", lw=0.8, ls="--")
        ax.set_xscale("log")
        ax.set_xlim(0.05, 20)
        ax.set_ylim(-1.35, len(linhas) + 0.9)
        ax.set_yticks([])
        ax.set_title(TITULO[fam], loc="left", fontsize=10.5, fontweight="bold")
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
    axes[-1].set_xlabel("Risk ratio (log scale) — GDFT vs control", fontsize=9)
    axes[0].plot([], [], "o", color=AZUL, label="ours (clean-text reading + code)")
    axes[0].plot([], [], "D", mfc="none", color=LARANJA, label="published (anchor)")
    axes[0].legend(loc="upper right", fontsize=8, frameon=False)
    fig.suptitle("Study 7 — the side-by-side in the open, MA-1: ours vs published (clean texts)",
                 fontsize=11, y=0.99)
    fig.subplots_adjust(left=0.21, right=0.84, top=0.93, bottom=0.06)
    fig.savefig(E7 / "forest-ma1-pareado.png", dpi=150)
    print("OK: forest-ma1-pareado.png")


def ma2():
    linhas = RES2["por_estudo"]
    if not linhas:
        print("MA-2 forest skipped (no computed studies yet)")
        return
    fig, ax = plt.subplots(figsize=(9.2, 0.95 * (len(linhas) + 2.4)))
    tr = blended_transform_factory(ax.transAxes, ax.transData)
    y = len(linhas) + 1.2
    for l in linhas:
        y -= 1
        ax.errorbar(l["md"], y + 0.16, xerr=[[l["md"] - l["ic95"][0]], [l["ic95"][1] - l["md"]]],
                    fmt="o", color=AZUL, ms=5, capsize=2, lw=1.4)
        p = l.get("publicado")
        if p:
            ax.errorbar(p["md"], y - 0.16, xerr=[[p["md"] - p["ic95"][0]], [p["ic95"][1] - p["md"]]],
                        fmt="D", mfc="none", color=LARANJA, ms=5, capsize=2, lw=1.2)
        ax.text(-0.015, y, l["estudo"], transform=tr, ha="right", va="center", fontsize=9)
        ax.text(1.015, y, "match" if l.get("bate") else "differs", transform=tr,
                ha="left", va="center", fontsize=7.8, color="#333")
    pool = RES2.get("pool")
    if pool:
        ax.errorbar(pool["md"], 0.15, xerr=[[pool["md"] - pool["ic95"][0]],
                                            [pool["ic95"][1] - pool["md"]]],
                    fmt="o", color=AZUL, ms=7, capsize=3, lw=2)
        ax.text(-0.015, 0.15, f"Our DL pool\n{pool['md']} [{pool['ic95'][0]}, {pool['ic95'][1]}]",
                transform=tr, ha="right", va="center", fontsize=8.2, fontweight="bold", color=AZUL)
    pub = RES2["publicado"]
    ax.errorbar(pub["md"], -0.75, xerr=[[pub["md"] - pub["ic95"][0]],
                                        [pub["ic95"][1] - pub["md"]]],
                fmt="D", mfc="none", color=LARANJA, ms=7, capsize=3, lw=1.8)
    ax.text(-0.015, -0.75, f"Published pool\n{pub['md']} [{pub['ic95'][0]}, {pub['ic95'][1]}]",
            transform=tr, ha="right", va="center", fontsize=8.2, fontweight="bold", color=LARANJA)
    ax.axvline(0, color="#999", lw=0.8, ls="--")
    ax.set_ylim(-1.35, len(linhas) + 0.9)
    ax.set_yticks([])
    ax.set_xlabel("HbA1c mean difference (%) — lower-carbohydrate vs control", fontsize=9)
    ax.plot([], [], "o", color=AZUL, label="ours (clean-text reading + code)")
    ax.plot([], [], "D", mfc="none", color=LARANJA, label="published (anchor forest)")
    ax.legend(loc="upper right", fontsize=8, frameon=False)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.set_title("Study 7 — MA-2: ours vs published, per study and pool (clean texts)",
                 loc="left", fontsize=10.5, fontweight="bold")
    fig.subplots_adjust(left=0.2, right=0.86, top=0.9, bottom=0.12)
    fig.savefig(E7 / "forest-ma2-pareado.png", dpi=150)
    print("OK: forest-ma2-pareado.png")


if __name__ == "__main__":
    ma1()
    ma2()

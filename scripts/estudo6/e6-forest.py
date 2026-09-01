# -*- coding: utf-8 -*-
"""Study 6 — paired forest plots, MA-1 dichotomous families (protocol §5).

Ours (fresh gemma12 cells + deterministic engine, sealed lens applied) vs
the anchor's published rows, per study and pooled (DL, per erratum #15).
Categories shown are the ADJUDICATED ones from avaliacao-estudo6.md.

Run: python scripts/estudo6/e6-forest.py
Output: dados/estudo6/forest-ma1-pareado.png
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
D6 = ROOT / "dados" / "estudo6"

RES = json.loads((D6 / "resultados-por-desfecho.json").read_text(encoding="utf-8"))

# adjudicated final categories (the record's rite; overrides the mechanical "verificar")
FINAL = {
    ("morbidity", "REF33"): "rota-do-modelo",
    ("morbidity", "REF26"): "rota-do-modelo",
    ("morbidity", "PMC10912221"): "rota-do-modelo",
    ("ileus", "PMC10694978"): "reproduz (2 d.p.)",
    ("ileus", "PMC11061212"): "erratum-#16 (confirmed)",
}

PUB_POOL = {
    "morbidity": (0.778, 0.567, 1.068, "0.778 [0.567, 1.068]"),
    "mortality": (1.021, 0.446, 2.337, "1.021 [0.446, 2.337]"),
    "ileus": None,  # abstract-only RR 0.48; not comparable (candidate erratum #16)
}
TITULO = {"morbidity": "overall morbidity (anchor T5)", "mortality": "mortality (anchor T6)",
          "ileus": "postoperative ileus (anchor T11)"}


def parse_rr(s):
    m = re.search(r"RR\s+([\d.]+)\s*\[([\d.]+),\s*([\d.]+)\]", str(s))
    return (float(m.group(1)), float(m.group(2)), float(m.group(3))) if m else None


def main():
    fams = ["morbidity", "mortality", "ileus"]
    alturas = [len([l for l in RES[fam]["rows"] if l.get("pmcid")]) + 2.0 for fam in fams]
    fig, axes = plt.subplots(3, 1, figsize=(9.6, 0.95 * sum(alturas)),
                             gridspec_kw=dict(height_ratios=alturas, hspace=0.42))
    for ax, fam in zip(axes, fams):
        tr = blended_transform_factory(ax.transAxes, ax.transData)
        linhas = [l for l in RES[fam]["rows"] if l.get("pmcid")]
        y = len(linhas) + 1.2
        for l in linhas:
            y -= 1
            nosso, pub = parse_rr(l["ours"]), parse_rr(l["published"])
            cat = FINAL.get((fam, l["pmcid"]), l["category"].split(" (")[0])
            if nosso:
                ax.errorbar(nosso[0], y + 0.16, xerr=[[nosso[0] - nosso[1]], [nosso[2] - nosso[0]]],
                            fmt="o", color="#1a6b8a", ms=5, capsize=2, lw=1.4)
            if pub:
                ax.errorbar(pub[0], y - 0.16, xerr=[[pub[0] - pub[1]], [pub[2] - pub[0]]],
                            fmt="D", mfc="none", color="#b0553a", ms=5, capsize=2, lw=1.2)
            rot = l["study"].replace(" et al.", "")
            if not nosso:
                rot += "\nours: NR*"
            ax.text(-0.015, y, rot, transform=tr, ha="right", va="center", fontsize=9)
            ax.text(1.015, y, cat, transform=tr, ha="left", va="center",
                    fontsize=7.8, color="#333")
        nosso_pool = (RES[fam].get("pool") or {}).get("DL")
        if nosso_pool:
            ax.errorbar(nosso_pool["rr"], 0.15,
                        xerr=[[nosso_pool["rr"] - nosso_pool["ic95"][0]],
                              [nosso_pool["ic95"][1] - nosso_pool["rr"]]],
                        fmt="o", color="#1a6b8a", ms=7, capsize=3, lw=2)
            rotulo = "Our DL pool (2 of 3)" if fam == "ileus" else "Our DL pool"
            ax.text(-0.015, 0.15, f"{rotulo}\n{nosso_pool['rr']} "
                    f"[{nosso_pool['ic95'][0]}, {nosso_pool['ic95'][1]}]",
                    transform=tr, ha="right", va="center", fontsize=8.2,
                    fontweight="bold", color="#1a6b8a")
        if PUB_POOL[fam]:
            p, lo, hi, rot = PUB_POOL[fam]
            ax.errorbar(p, -0.75, xerr=[[p - lo], [hi - p]], fmt="D", mfc="none",
                        color="#b0553a", ms=7, capsize=3, lw=1.8)
            ax.text(-0.015, -0.75, f"Published pool\n{rot}", transform=tr, ha="right",
                    va="center", fontsize=8.2, fontweight="bold", color="#b0553a")
        else:
            ax.text(0.0, -0.75, "Published pool (abstract): RR 0.48 — not comparable by "
                    "construction (erratum #16, confirmed)\n*Castro's source does not report ileus; "
                    "the published numbers are its PPC counts", transform=tr,
                    va="center", fontsize=8.2, style="italic", color="#b0553a")
        ax.axvline(1, color="#999", lw=0.8, ls="--")
        ax.set_xscale("log")
        ax.set_xlim(0.05, 20)
        ax.set_ylim(-1.35, len(linhas) + 0.9)
        ax.set_yticks([])
        ax.set_title(TITULO[fam], loc="left", fontsize=10.5, fontweight="bold")
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
    axes[-1].set_xlabel("Risk ratio (log scale) — GDFT vs control", fontsize=9)
    axes[0].plot([], [], "o", color="#1a6b8a", label="ours (fresh reading + code, sealed lens)")
    axes[0].plot([], [], "D", mfc="none", color="#b0553a", label="published (anchor)")
    axes[0].legend(loc="upper right", fontsize=8, frameon=False)
    fig.suptitle("Study 6 — the replication in detail, MA-1: ours vs published, per study and pool",
                 fontsize=11, y=0.99)
    fig.subplots_adjust(left=0.21, right=0.84, top=0.93, bottom=0.06)
    out = D6 / "forest-ma1-pareado.png"
    fig.savefig(out, dpi=150)
    print(f"OK: {out}")


if __name__ == "__main__":
    main()

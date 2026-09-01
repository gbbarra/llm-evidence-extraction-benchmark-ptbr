# -*- coding: utf-8 -*-
"""Study 8 / P3 CREATE — deterministic downstream for all five models, both
anchors. Pure code; no model call anywhere.

Part A (MA-1, from the P1 sheets): per model, Study 6's erratum-aware
comparator verbatim (sheet loader patched per model; sealed reversal) — full
per-model comparison files plus the pooled summary.
Part B (MA-2, from the P3-b sheets): per model, the validated route selector
(dirigida, no triggers) -> sextets -> DL pool in the perturbed world AND the
sealed unperturbation lens vs the published -0.24 [-0.32, -0.16] — the five
diamonds, the model-comparison headline (PT reference: round 2).

Run: python scripts/estudo8/p3-avalia.py
Outputs: dados/estudo8/p3-ma1/<model>/ (comparison + results JSON) ·
         dados/estudo8/avaliacao-p3.json (+ console tables)
"""
import importlib.util
import json
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


e7d = carrega("e7d", "scripts/estudo7/e7-downstream.py")  # maps, converters, h3, dg
d6 = carrega("d6", "scripts/estudo6/e6-downstream.py")    # fresh instance to patch
h3, dg = e7d.h3, e7d.dg

SELO3 = json.loads((ROOT / "dados" / "estudo3" / "perturbacoes-estudo3.json")
                   .read_text(encoding="utf-8"))
PUB2 = dict(md=-0.24, ic95=[-0.32, -0.16])


def bruta(pasta, tid):
    for rep in (1, 2):
        f = pasta / f"{tid}-r{rep}.json"
        if not f.exists():
            continue
        js = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
        if js:
            return js
    return None


# ---- Part A: MA-1 per model via the Study-6 comparator ----

def ma1(modelo):
    out = E8 / "p3-ma1" / modelo
    out.mkdir(parents=True, exist_ok=True)
    pasta = E8 / "saidas" / "p1" / modelo
    d6.ficha = lambda tid: (lambda js: e7d.ficha_ma1_pt(js) if js else None)(bruta(pasta, tid))
    # perturbed world: keep the real reversal (d6.desperturba as shipped)
    d6.D6 = out
    d6.main()
    res = json.loads((out / "resultados-por-desfecho.json").read_text(encoding="utf-8"))
    pools = {}
    for fam in ("morbidity", "mortality"):
        dl = (res[fam].get("pool") or {}).get("DL")
        pools[fam] = dl
    return pools


# ---- Part B: MA-2 per model — perturbed pool + sealed lens ----

def lens_sexteto(ficha_pt, tid):
    txt = json.dumps(ficha_pt, ensure_ascii=False)
    for reg in SELO3.get(tid, []):
        p, o = str(reg["perturbado"]), str(reg["original"])
        txt = txt.replace(f'"{p}"', f'"{o}"').replace(f'"-{p}"', f'"-{o}"')
        txt = txt.replace(f" {p}", f" {o}").replace(f"-{p}", f"-{o}")
    return json.loads(txt)


def sexteto_de(ficha_pt):
    e = dg.braco_deterministico(ficha_pt["braco_experimental"], {}, ("x", "exp"))
    c = dg.braco_deterministico(ficha_pt["braco_controle"], {}, ("x", "ctl"))
    if None in e or None in c:
        return None
    return [e[0], e[1], e[2], c[0], c[1], c[2]]


def ma2(modelo):
    pasta = E8 / "saidas" / "p3b" / modelo
    sx, sx_lens, faltas = [], [], []
    for tid in h3.TRIALS:
        js = bruta(pasta, tid)
        if not js:
            faltas.append(h3.ROT[tid] + " (unparseable)")
            continue
        f = e7d.ficha_ma2_pt(js)
        s = sexteto_de(f)
        if s:
            sx.append(s)
        else:
            faltas.append(h3.ROT[tid])
        sl = sexteto_de(lens_sexteto(f, tid))
        if sl:
            sx_lens.append(sl)
    pool = h3.pool_dl_md(sx) if len(sx) >= 2 else None
    lens = h3.pool_dl_md(sx_lens) if len(sx_lens) >= 2 else None
    beside = lens and abs(lens["md"] - PUB2["md"]) <= 0.05 and \
        abs(lens["ic95"][0] - PUB2["ic95"][0]) <= 0.05 and \
        abs(lens["ic95"][1] - PUB2["ic95"][1]) <= 0.05
    return dict(estudos_no_pool=len(sx), faltas=faltas, pool_perturbado=pool,
                lens=lens, publicado=PUB2, lens_beside_published=bool(beside))


def main():
    res = {}
    for modelo in CAST:
        print(f"===== {modelo}", flush=True)
        a = ma1(modelo)
        b = ma2(modelo)
        res[modelo] = dict(ma1_pools=a, ma2=b)
        print(f"  MA-1 morbidity DL: {json.dumps(a['morbidity'])}", flush=True)
        print(f"  MA-1 mortality DL: {json.dumps(a['mortality'])}", flush=True)
        print(f"  MA-2 lens: {json.dumps(b['lens'])} "
              f"({b['estudos_no_pool']}/7 in pool; beside published: "
              f"{b['lens_beside_published']})", flush=True)
    (E8 / "avaliacao-p3.json").write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                          encoding="utf-8")
    print("\npublished references — MA-1 morbidity 0.778 [0.567, 1.068] · "
          "mortality 1.021 [0.446, 2.337] · MA-2 -0.24 [-0.32, -0.16]", flush=True)


if __name__ == "__main__":
    main()

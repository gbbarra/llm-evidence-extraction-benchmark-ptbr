# -*- coding: utf-8 -*-
"""EXTRAI Study 7 — hypothesis measurements (protocol §5).

H7.1 replicate agreement (r1 vs r2, per anchor, over the graded field sets);
H7.2 the errata-cell panel: does the model's clean-text sheet side with the
SOURCE where the anchor's confirmed errata live?; H7.4 coverage; plus the
MA-1 mechanical cell score vs the two-layer key (Study 6's comparator,
declared an approximation — residue goes to adjudication).

Run: python scripts/estudo7/e7-avalia.py
Output: dados/estudo7/avaliacao-celulas.json (+ console verdicts)
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
E7 = ROOT / "dados" / "estudo7"


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


e6a = carrega("e6a", "scripts/estudo6/e6-avalia.py")     # compat, nums_de, d6
e7d = carrega("e7d", "scripts/estudo7/e7-downstream.py")
d6 = e6a.d6
compat, nums_de = e6a.compat, e6a.nums_de


def bruta_rep(pasta, tid, rep):
    f = pasta / f"{tid}-r{rep}.json"
    if not f.exists():
        return None
    return e7d.h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])


def valor_en(js, campo_en):
    v = (js or {}).get(campo_en)
    if isinstance(v, dict):
        v = v.get("value")
    return None if v is None else str(v)


# ---- H7.1 + MA-1 key score ----

def ma1():
    eleg = {}
    for tid, campos in d6.GAB.items():
        for campo, cel in campos.items():
            vf, ver = cel.get("valor_fonte"), str(cel.get("veredito"))
            if vf in (None, "") or ver in ("sem-valor-na-ma", "pendente-adjudicacao",
                                           "nao-sustentada", "dado-fora-do-insumo"):
                continue
            if re.search(r"\d", str(vf)):
                eleg.setdefault(tid, []).append(campo)
    pt2en = {v: k for k, v in e7d.MA1_EN2PT.items()}
    est_ig = est_tot = boas = tot = 0
    pend = []
    for tid, campos in eleg.items():
        r1 = bruta_rep(e7d.MA1_DIR, tid, 1)
        r2 = bruta_rep(e7d.MA1_DIR, tid, 2)
        if not r1:
            continue
        for campo in campos:
            en = pt2en[campo]
            v1 = valor_en(r1, en)
            if r2 is not None:
                est_tot += 1
                est_ig += compat(v1, valor_en(r2, en))
            fonte = d6.GAB[tid][campo].get("valor_fonte")
            tot += 1
            ok = compat(v1, fonte)
            boas += ok
            if not ok:
                pend.append(dict(trial=tid, field=campo, model=v1, source=str(fonte)[:60]))
    return dict(replicas=f"{est_ig}/{est_tot} ({round(100 * est_ig / max(est_tot, 1), 1)}%)",
                cells=f"{boas}/{tot} ({round(100 * boas / max(tot, 1), 1)}%)",
                divergents=pend)


# ---- H7.1 MA-2 (numeric leaves per arm) ----

MA2_LEAVES = ["n_randomized", "n_analyzed", "hba1c_change_mean", "hba1c_change_dispersion",
              "hba1c_change_dispersion_type", "hba1c_baseline_mean", "hba1c_baseline_sd",
              "hba1c_final_mean", "hba1c_final_sd"]


def ma2_replicas():
    ig = tot = 0
    for tid in e7d.h3.ROT:
        r1 = bruta_rep(e7d.MA2_DIR, tid, 1)
        r2 = bruta_rep(e7d.MA2_DIR, tid, 2)
        if not r1 or not r2:
            continue
        for arm in ("experimental_arm", "control_arm"):
            for leaf in MA2_LEAVES:
                v1 = (r1.get(arm) or {}).get(leaf)
                v2 = (r2.get(arm) or {}).get(leaf)
                tot += 1
                ig += compat("" if v1 is None else str(v1), "" if v2 is None else str(v2))
    return f"{ig}/{tot} ({round(100 * ig / max(tot, 1), 1)}%)"


# ---- H7.2: the errata-cell panel (frozen in the protocol) ----

def rot2tid():
    m = {}
    for t in d6.MA:
        for l in t["linhas"]:
            if l.get("pmcid"):
                m[l["rotulo"]] = l["pmcid"]
    return m


def acha_tid(sub, mapa):
    for rot, tid in mapa.items():
        if sub.lower() in rot.lower():
            return tid
    return None


def lado(nums_alvo_fonte, nums_alvo_ancora, valor):
    ns = set(nums_de(valor or ""))
    if ns & set(nums_alvo_fonte) and not ns & set(nums_alvo_ancora):
        return "fonte"
    if ns & set(nums_alvo_ancora) and not ns & set(nums_alvo_fonte):
        return "ancora"
    if ns & set(nums_alvo_fonte):
        return "fonte"
    return "indeterminado" if ns else "vazio"


def eh_nr(v):
    return str(v or "").strip().upper() in ("NR", "NA", "N/A", "", "NONE")


def painel():
    mapa = rot2tid()
    fichas = {tid: bruta_rep(e7d.MA1_DIR, tid, 1) for tid in set(mapa.values())}
    out = []

    def add(errata, rot_sub, campo_en, veredito, detalhe, critico=False):
        out.append(dict(errata=errata, trial=rot_sub, field=campo_en, side=veredito,
                        detail=str(detalhe)[:70], direction_critical=critico))

    # 1 — Yoon arms (source 39/36)
    tid = acha_tid("Yoon", mapa) or acha_tid("Yun", mapa)
    f = fichas.get(tid)
    g, c = valor_en(f, "n_randomized_gdft"), valor_en(f, "n_randomized_control")
    v = "fonte" if (g and c and nums_de(g)[:1] == [39.0] and nums_de(c)[:1] == [36.0]) else \
        ("ancora" if (g and c and nums_de(g)[:1] == [36.0] and nums_de(c)[:1] == [39.0])
         else "indeterminado")
    add("#1", "Yoon", "n_randomized_*", v, f"gdft={g} ctl={c}", critico=True)
    # 3 — Weinberg ASA reported (anchor: Not stated)
    tid = acha_tid("Weinberg", mapa)
    f = fichas.get(tid)
    v = "fonte" if f and not eh_nr(valor_en(f, "asa_gdft")) else \
        ("ancora" if f else "indeterminado")
    add("#3", "Weinberg", "asa_*", v, valor_en(f, "asa_gdft"))
    # 9 — Sun oral diet in days (4.0 / 6.0; anchor converted 72/96 h)
    tid = acha_tid("Sun", mapa)
    f = fichas.get(tid)
    g = valor_en(f, "time_to_oral_intake_gdft")
    v = lado([4.0], [72.0], g)
    add("#9", "Sun", "time_to_oral_intake_gdft", v, g)
    # 10 — de Waal ASA direction (source GDFT 17:132:95:4 / 53.2%)
    tid = acha_tid("Waal", mapa)
    f = fichas.get(tid)
    g = valor_en(f, "asa_gdft")
    v = lado([132.0, 53.2, 6.9], [123.0, 52.6, 10.3], g)
    add("#10", "de Waal", "asa_gdft", v, g, critico=True)
    # 11 — Diaper ASA reported (anchor: Not stated)
    tid = acha_tid("Diaper", mapa)
    f = fichas.get(tid)
    v = "fonte" if f and not eh_nr(valor_en(f, "asa_gdft")) else \
        ("ancora" if f else "indeterminado")
    add("#11", "Diaper", "asa_*", v, valor_en(f, "asa_gdft"))
    # 16 — Castro ileus (source has none -> NR is correct)
    tid = acha_tid("Castro", mapa)
    f = fichas.get(tid)
    g, c = valor_en(f, "postop_ileus_gdft"), valor_en(f, "postop_ileus_control")
    v = "fonte" if (f and eh_nr(g) and eh_nr(c)) else \
        ("ancora" if (f and {6.0, 19.0} & set(nums_de(g or "") + nums_de(c or "")))
         else "indeterminado")
    add("#16", "Castro", "postop_ileus_*", v, f"gdft={g} ctl={c}", critico=True)
    # 17 — Coeckelenbergh blood loss (source GDFT 450 [300-600])
    tid = acha_tid("Coeckelenbergh", mapa)
    f = fichas.get(tid)
    g = valor_en(f, "blood_loss_gdft")
    v = lado([450.0], [500.0], g)
    add("#17", "Coeckelenbergh", "blood_loss_gdft", v, g, critico=True)
    return out


def main():
    r1 = ma1()
    rep2 = ma2_replicas()
    pan = painel()
    fonte_n = sum(1 for p in pan if p["side"] == "fonte")
    crit = [p for p in pan if p["direction_critical"]]
    crit_ok = sum(1 for p in crit if p["side"] == "fonte")
    res = dict(ma1=r1, ma2_replicas=rep2, painel=pan,
               painel_score=f"{fonte_n}/{len(pan)}",
               swaps_score=f"{crit_ok}/{len(crit)}")
    (E7 / "avaliacao-celulas.json").write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                               encoding="utf-8")
    print(f"H7.1 MA-1 replicates: {r1['replicas']} · MA-2 replicates: {rep2}")
    print(f"MA-1 cells vs key: {r1['cells']} · divergents: {len(r1['divergents'])}")
    print(f"H7.2 panel (sides with the source): {res['painel_score']} · "
          f"direction-critical swaps: {res['swaps_score']}")
    for p in pan:
        print(f"  {p['errata']} {p['trial']} {p['field']}: {p['side']} ({p['detail']})")


if __name__ == "__main__":
    main()

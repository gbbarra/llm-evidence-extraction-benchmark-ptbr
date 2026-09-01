# -*- coding: utf-8 -*-
"""EXTRAI Study 7 — deterministic downstream, both anchors (protocol §4.4–4.5).

Clean texts, no seal, no reversal. The fresh sheets carry the ENGLISH keys of
the frozen instruments; this script converts them to the Portuguese-keyed form
the validated machinery expects (correspondence tables in
dados/instruments-en/README.md), then:

- MA-1: reuses Study 6's erratum-aware comparator verbatim (e6-downstream),
  with its sheet loader patched to the clean Study-7 sheets and the reversal
  patched to identity — same categories, same pools, same tolerances.
- MA-2: the validated route selector (estudo3/dirigida.braco_deterministico,
  no judgment triggers — declared) + e3-harness formulas; per-study MD/CI and
  the DL pool against the anchor's published forest.
- Three-way tables per trial: source (two-layer key) x human (anchor's cell)
  x model (fresh sheet).

Run: python scripts/estudo7/e7-downstream.py
Outputs (dados/estudo7/): comparacao-detalhada.md · resultados-por-desfecho.json
· comparacao-ma2.md · resultados-ma2.json · tabela-tripla-<tid>.md · tabela-tripla-ma2.md
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
E7 = ROOT / "dados" / "estudo7"
MA1_DIR = E7 / "saidas" / "gemma12" / "ma1"
MA2_DIR = E7 / "saidas" / "gemma12" / "ma2"


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


h3 = carrega("h3", "scripts/estudo3/e3-harness.py")
dg = carrega("dg", "scripts/estudo3/dirigida.py")
d6 = carrega("d6", "scripts/estudo6/e6-downstream.py")

FONTE2 = json.loads((ROOT / "dados" / "estudo3" / "gabarito-fonte.json")
                    .read_text(encoding="utf-8"))["estudos"]
META2 = json.loads((ROOT / "corpus" / "estudo3" / "ma" / "ma-lowcarb-meta.json")
                   .read_text(encoding="utf-8"))

# ---- EN -> PT correspondence (instruments-en/README.md, frozen 2026-08-31) ----

MA1_EN2PT = {
    "n_randomized_gdft": "n_randomizados_gdft", "n_randomized_control": "n_randomizados_controle",
    "surgery_type": "tipo_cirurgia",
    "laparoscopy_gdft": "laparoscopia_gdft", "laparoscopy_control": "laparoscopia_controle",
    "asa_gdft": "asa_gdft", "asa_control": "asa_controle",
    "total_fluid_gdft": "fluido_total_gdft", "total_fluid_control": "fluido_total_controle",
    "crystalloid_gdft": "cristaloide_gdft", "crystalloid_control": "cristaloide_controle",
    "colloid_gdft": "coloide_gdft", "colloid_control": "coloide_controle",
    "blood_loss_gdft": "perda_sanguinea_gdft", "blood_loss_control": "perda_sanguinea_controle",
    "inotrope_use": "uso_inotropico",
    "morbidity_events_gdft": "morbidade_eventos_gdft",
    "morbidity_events_control": "morbidade_eventos_controle",
    "mortality_gdft": "mortalidade_gdft", "mortality_control": "mortalidade_controle",
    "hospital_los_gdft": "los_hospitalar_gdft", "hospital_los_control": "los_hospitalar_controle",
    "time_to_flatus_gdft": "tempo_flatus_gdft", "time_to_flatus_control": "tempo_flatus_controle",
    "time_to_oral_intake_gdft": "tempo_ingesta_oral_gdft",
    "time_to_oral_intake_control": "tempo_ingesta_oral_controle",
    "time_to_defecation_gdft": "tempo_evacuacao_gdft",
    "time_to_defecation_control": "tempo_evacuacao_controle",
    "postop_ileus_gdft": "ileo_pos_op_gdft", "postop_ileus_control": "ileo_pos_op_controle",
}

MA2_ARM_EN2PT = {
    "label": "rotulo", "intervention_description": "descricao_intervencao",
    "n_randomized": "n_randomizado", "n_analyzed": "n_analisado",
    "hba1c_change_mean": "hba1c_mudanca_media",
    "hba1c_change_dispersion": "hba1c_mudanca_dispersao",
    "hba1c_change_dispersion_type": "hba1c_mudanca_tipo_dispersao",
    "hba1c_baseline_mean": "hba1c_basal_media", "hba1c_baseline_sd": "hba1c_basal_dp",
    "hba1c_final_mean": "hba1c_final_media", "hba1c_final_sd": "hba1c_final_dp",
}


def celula_pt(v):
    if isinstance(v, dict):
        return {"valor": v.get("value", v.get("valor", "")),
                "onde": v.get("where", v.get("onde", ""))}
    return {"valor": v, "onde": ""}


def ficha_ma1_pt(js):
    return {pt: celula_pt(js.get(en)) for en, pt in MA1_EN2PT.items() if en in js}


def tipo_pt(t):
    t = str(t or "")
    t = re.sub(r"^\s*CI\s*95", "IC95", t, flags=re.I)
    return {"SD": "DP"}.get(t.strip().upper(), t)


def braco_pt(b):
    out = {}
    for en, pt in MA2_ARM_EN2PT.items():
        if en in (b or {}):
            out[pt] = b[en]
    if "hba1c_mudanca_tipo_dispersao" in out:
        out["hba1c_mudanca_tipo_dispersao"] = tipo_pt(out["hba1c_mudanca_tipo_dispersao"])
    return out


def ficha_ma2_pt(js):
    return {"estudo": js.get("study"),
            "braco_experimental": braco_pt(js.get("experimental_arm")),
            "braco_controle": braco_pt(js.get("control_arm"))}


def bruta(pasta, tid):
    for rep in (1, 2):
        f = pasta / f"{tid}-r{rep}.json"
        if not f.exists():
            continue
        js = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
        if js:
            return js
    return None


# ---- MA-1: Study 6's comparator over the clean sheets ----

def roda_ma1():
    d6.ficha = lambda tid: (lambda js: ficha_ma1_pt(js) if js else None)(bruta(MA1_DIR, tid))
    d6.desperturba = lambda tid, js: js  # clean texts: no seal, no reversal
    d6.D6 = E7
    d6.main()
    md = E7 / "comparacao-detalhada.md"
    txt = md.read_text(encoding="utf-8")
    txt = txt.replace("# Study 6 — the replication, in detail (MA-1, GDFT)",
                      "# Study 7 — the side-by-side, in the open (MA-1, GDFT, clean texts)")
    txt = txt.replace("gemma12's cells (seal reversed)",
                      "gemma12's cells (clean original texts — no seal, no reversal; "
                      "protocol §2 scoping applies)")
    md.write_text(txt, encoding="utf-8")


# ---- MA-2: deterministic route + engine vs the published forest ----

def acha_pub(rotulo):
    alvo = rotulo.split()  # e.g. ["Chen", "2020"]
    for linha in META2["forest_hba1c"]:
        if all(t in linha["estudo"] for t in alvo):
            return linha
    return None


def roda_ma2():
    L = ["# Study 7 — the side-by-side, in the open (MA-2, low-carbohydrate, clean texts)",
         "",
         "Per study: the model's sheet routed deterministically (dirigida.braco_deterministico, "
         "no judgment triggers — declared), MD/CI by the validated engine, against the anchor's "
         "published forest row. Pool under DerSimonian–Laird.",
         "",
         "| study | sextet (m,sd,n × 2 arms) | ours MD [CI95] | published MD [CI95] | match (±0.1) |",
         "|---|---|---|---|---|"]
    sextetos, usados, pend = [], [], []
    for tid, rot in h3.ROT.items():
        js = bruta(MA2_DIR, tid)
        if not js:
            pend.append(tid)
            L.append(f"| {rot} ({tid}) | (sheet pending) | — | — | — |")
            continue
        f = ficha_ma2_pt(js)
        e = dg.braco_deterministico(f["braco_experimental"], {}, ("x", "exp"))
        c = dg.braco_deterministico(f["braco_controle"], {}, ("x", "ctl"))
        pub = acha_pub(rot)
        pub_txt = f"MD {pub['md']} {pub['ic95']}" if pub else "—"
        if None in e or None in c:
            L.append(f"| {rot} ({tid}) | insufficient: exp={e} ctl={c} | insufficient-data | "
                     f"{pub_txt} | counted, never silent |")
            continue
        s = [e[0], e[1], e[2], c[0], c[1], c[2]]
        mdv, ic = h3.md(*s), h3.ic95_md(*s)
        bate = pub and abs(mdv - pub["md"]) <= 0.1 and \
            abs(ic[0] - pub["ic95"][0]) <= 0.1 and abs(ic[1] - pub["ic95"][1]) <= 0.1
        sextetos.append(s)
        usados.append(dict(trial=tid, estudo=rot, sexteto=s, md=mdv, ic95=ic,
                           publicado=(dict(md=pub["md"], ic95=pub["ic95"]) if pub else None),
                           bate=bool(bate)))
        L.append(f"| {rot} ({tid}) | {s} | MD {mdv} {ic} | {pub_txt} | "
                 f"{'yes' if bate else 'NO'} |")
    pool = h3.pool_dl_md(sextetos) if len(sextetos) >= 2 else None
    ag = META2["agrupado"]
    L.append("")
    if pool:
        b = abs(pool["md"] - ag["md"]) <= 0.02 and \
            abs(pool["ic95"][0] - ag["ic95"][0]) <= 0.02 and \
            abs(pool["ic95"][1] - ag["ic95"][1]) <= 0.02
        L.append(f"**Pool DL (ours, {len(sextetos)} studies)**: {pool['md']} {pool['ic95']} "
                 f"(τ²={pool['tau2']}, I²={pool['i2_pct']}%) · **published**: {ag['md']} "
                 f"{ag['ic95']} (I²={ag['i2_pct']}%) → "
                 f"**{'within the pre-registered ±0.02 (H7.3)' if b else 'outside ±0.02 — decompose per study'}**.")
    res = dict(por_estudo=usados, pendentes=pend, pool=pool,
               publicado=dict(md=ag["md"], ic95=ag["ic95"], i2=ag["i2_pct"]))
    (E7 / "resultados-ma2.json").write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                            encoding="utf-8")
    (E7 / "comparacao-ma2.md").write_text("\n".join(L), encoding="utf-8")
    print(f"MA-2: {len(usados)} computed, {len(pend)} pending"
          + (f" · pool {pool['md']} {pool['ic95']}" if pool else ""), flush=True)


# ---- three-way tables: source x human x model ----

def tripla_ma1():
    for tid in d6.GAB.keys():
        js = bruta(MA1_DIR, tid)
        if not js:
            continue
        f = ficha_ma1_pt(js)
        L = [f"# Three-way table — {tid} (MA-1, clean text)",
             "",
             "| field | source (two-layer key, quote abridged) | human (anchor's cell) | model (fresh, r1) |",
             "|---|---|---|---|"]
        for campo, cel in d6.GAB[tid].items():
            vf = cel.get("valor_fonte")
            cit = (cel.get("cit") or "").replace("|", "\\|")[:90]
            ma = cel.get("ma")
            mod = (f.get(campo) or {}).get("valor", "—")
            fonte_txt = f"{vf}" + (f" · *…{cit}…*" if cit else "") if vf not in (None, "") \
                else f"({cel.get('veredito')})"
            L.append(f"| {campo} | {fonte_txt} | {ma if ma not in (None, '') else '—'} | {mod} |")
        (E7 / f"tabela-tripla-{tid}.md").write_text("\n".join(L), encoding="utf-8")
    print("MA-1 three-way tables written", flush=True)


def tripla_ma2():
    L = ["# Three-way tables — MA-2 (low-carbohydrate, clean texts)", ""]
    for tid, rot in h3.ROT.items():
        js = bruta(MA2_DIR, tid)
        gf = FONTE2.get(tid, {})
        pub = acha_pub(rot)
        L += [f"## {rot} ({tid})", "",
              "| quantity | source (two-layer key) | human (anchor's forest) | model (fresh sheet, routed) |",
              "|---|---|---|---|"]
        if not js:
            L += ["| (sheet pending) | | | |", ""]
            continue
        f = ficha_ma2_pt(js)
        e = dg.braco_deterministico(f["braco_experimental"], {}, ("x", "exp"))
        c = dg.braco_deterministico(f["braco_controle"], {}, ("x", "ctl"))
        cel = gf.get("celulas", {})
        for rotq, chave, pubk, mod in [
                ("exp mean", "exp_media", "exp_media", e[0]),
                ("exp SD", "exp_dispersao", "exp_dp", e[1]),
                ("exp n", "exp_n", "exp_n", e[2]),
                ("ctl mean", "ctl_media", "ctl_media", c[0]),
                ("ctl SD", "ctl_dispersao", "ctl_dp", c[1]),
                ("ctl n", "ctl_n", "ctl_n", c[2])]:
            g = cel.get(chave) or {}
            cit = (str(g.get("cit") or "")).replace("|", "\\|")[:70]
            fonte_txt = f"{g.get('valor', '—')}" + (f" · *…{cit}…*" if cit else "")
            L.append(f"| {rotq} | {fonte_txt} | {pub.get(pubk, '—') if pub else '—'} | {mod} |")
        L.append("")
    (E7 / "tabela-tripla-ma2.md").write_text("\n".join(L), encoding="utf-8")
    print("MA-2 three-way tables written", flush=True)


def main():
    roda_ma1()
    roda_ma2()
    tripla_ma1()
    tripla_ma2()


if __name__ == "__main__":
    main()

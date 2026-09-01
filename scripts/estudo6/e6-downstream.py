# -*- coding: utf-8 -*-
"""EXTRAI Study 6 — deterministic downstream and the erratum-aware comparison.

From gemma12's fresh MA-1 sheets: seal reversed (graders' side) -> per-study
RR/CI (morbidity, mortality, ileus) and MD/CI (flatus, oral diet) -> pools
under MH and DL -> side-by-side with the published tables, every row
classified into the frozen categories (reproduz / difere-por-errata-da-ancora
/ rota-do-modelo / erro-do-modelo / fonte-indisponivel), using the two-layer
key's per-cell verdicts and quotes. No model touches a number here.

Run: python scripts/estudo6/e6-downstream.py    (graceful on missing sheets)
Outputs: dados/estudo6/resultados-por-desfecho.json · comparacao-detalhada.md
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
D6 = ROOT / "dados" / "estudo6"
EXTR = D6 / "saidas" / "gemma12" / "extracao"
D1 = ROOT / "dados" / "estudo1"


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


e2 = carrega("e2", "scripts/estudo2/e2-harness.py")
h3 = carrega("h3", "scripts/estudo3/e3-harness.py")

GAB = json.loads((D1 / "gabarito-oficial.json").read_text(encoding="utf-8"))["celulas"]
MA = json.loads((D1 / "gabarito-ma.json").read_text(encoding="utf-8"))["tabelas"]

SELO = {}
for nome in ("perturbacoes-estudo1.json", "perturbacoes-fechados.json",
             "perturbacoes-manuais.json", "perturbacoes-fechados-manuais.json"):
    f = D1 / nome
    if not f.exists():
        continue
    j = json.loads(f.read_text(encoding="utf-8"))
    for tid, regs in j.items():
        if tid.startswith("_") or not isinstance(regs, list):
            continue
        SELO.setdefault(tid, []).extend(
            r for r in regs if isinstance(r, dict) and "original" in r and "perturbado" in r)

# display names in English; the e/c field keys stay Portuguese because they
# address the archived Study-6 sheets, produced under the frozen PT instrument
DESFECHOS = [
    dict(nome="morbidity", tipo="rr", tabela=5, e="morbidade_eventos_gdft", c="morbidade_eventos_controle"),
    dict(nome="mortality", tipo="rr", tabela=6, e="mortalidade_gdft", c="mortalidade_controle"),
    dict(nome="ileus", tipo="rr", tabela=11, e="ileo_pos_op_gdft", c="ileo_pos_op_controle"),
    dict(nome="time_to_flatus", tipo="md", tabela=8, e="tempo_flatus_gdft", c="tempo_flatus_controle"),
    dict(nome="time_to_oral_intake", tipo="md", tabela=9, e="tempo_ingesta_oral_gdft", c="tempo_ingesta_oral_controle"),
]


def ficha(tid):
    for rep in (1, 2):
        f = EXTR / f"{tid}-r{rep}.json"
        if not f.exists():
            continue
        js = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
        if js:
            return js
    return None


def desperturba(tid, js):
    txt = json.dumps(js, ensure_ascii=False)
    for reg in SELO.get(tid, []):
        p, o = str(reg["perturbado"]), str(reg["original"])
        if p and o and p != o:
            txt = txt.replace(p, o)
    return json.loads(txt)


def valor(js, campo):
    v = js.get(campo)
    if isinstance(v, dict):
        v = v.get("valor")
    return None if v is None else str(v)


def inteiro(s):
    if not s or str(s).strip().upper() in ("NR", "NA", "N/A", "", "NONE"):
        return None
    m = re.search(r"\d+", str(s))
    return int(m.group(0)) if m else None


def eventos(s, n=None):
    """Event count from a cell as models write them: '19 (32.8%)' -> 19;
    '25% (36/142)' -> 36; '2 of 50' -> 2; '8.6%' alone -> deterministic
    conversion round(pct/100*n), flagged."""
    if not s or str(s).strip().upper() in ("NR", "NA", "N/A", "", "NONE"):
        return None, ""
    t = str(s)
    m = re.search(r"\(\s*(\d+)\s*/\s*\d+\s*\)", t)
    if m:
        return int(m.group(1)), ""
    m = re.match(r"\s*(\d+)(?![\.\d])\s*(?:\(|of|de|%?\s|$)", t)
    if m and "%" not in t.split("(")[0].replace(m.group(1), "", 1)[:3]:
        return int(m.group(1)), ""
    m = re.match(r"\s*(\d+)\s*(?:\(|of|de)", t)
    if m:
        return int(m.group(1)), ""
    m = re.search(r"(\d+(?:\.\d+)?)\s*%", t)
    if m and n:
        return round(float(m.group(1)) / 100 * n), "derived-from-%"
    m = re.match(r"\s*(\d+)\b", t)
    return (int(m.group(1)), "") if m else (None, "")


def media_dp(s):
    if not s:
        return None, None
    t = str(s).replace("−", "-").replace("±", " ± ")
    m = re.search(r"(-?\d+(?:\.\d+)?)\s*±\s*(\d+(?:\.\d+)?)", t)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(r"(-?\d+(?:\.\d+)?)\s*\(\s*(\d+(?:\.\d+)?)\s*\)", t)
    if m:
        return float(m.group(1)), float(m.group(2))
    return None, None


def rr_pub(cel):
    r = cel.get("Risk ratio") or cel.get("RR")
    ic = cel.get("95% CI") or cel.get("95%CI")
    if r is None and ic is None:
        comb = cel.get("RR (95% CI)") or ""
        ns = re.findall(r"\d+(?:\.\d+)?", str(comb))
        if len(ns) >= 3:
            return float(ns[0]), [float(ns[1]), float(ns[2])]
        return None, None
    try:
        lo, hi = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", str(ic))[:2]]
        return float(re.findall(r"\d+(?:\.\d+)?", str(r))[0]), [lo, hi]
    except Exception:
        return None, None


def md_pub(cel):
    s = str(cel.get("MD (95% CI)") or "")
    ns = re.findall(r"-?\d+(?:\.\d+)?", s.replace("−", "-").replace("–", "-"))
    if len(ns) >= 3:
        return float(ns[0]), [float(ns[1]), float(ns[2])]
    return None, None


ERRATA_VER = ("errata-ma", "primario-contraditorio")
ESCOLHA_VER = ("ma-inferiu", "divergencia-definicional", "derivavel-conversao",
               "derivavel-arredondamento")
INDISP_VER = ("nao-sustentada", "dado-fora-do-insumo")


def categoria(tid, campos, nossa_igual_pub):
    """Frozen classification (protocol category ii operationalized by the
    two-layer key's per-cell verdict vocabulary)."""
    gab = GAB.get(tid, {})
    achado = ("", "")
    for campo in campos:
        g = gab.get(campo) or {}
        ver = str(g.get("veredito", ""))
        cit = (g.get("cit") or "")[:140]
        if ver in ERRATA_VER:
            achado = (f"difere-por-errata-da-ancora [{ver}]", cit)
            break
        if ver in INDISP_VER and not achado[0]:
            achado = (f"fonte-indisponivel [{ver}]", cit)
        elif ver in ESCOLHA_VER and not achado[0]:
            achado = (f"difere-por-escolha-documentada-da-ancora [{ver}]", cit)
    if nossa_igual_pub:
        return "reproduz", ""
    if achado[0]:
        return achado
    return "verify (rota-do-modelo or erro-do-modelo — adjudicate in the source)", ""


def main():
    fichas = {}
    pendentes = []
    for tid in GAB.keys():
        js = ficha(tid)
        if js:
            fichas[tid] = desperturba(tid, js)
        else:
            pendentes.append(tid)
    print(f"sheets available: {len(fichas)}/{len(GAB)}"
          + (f" · pending: {pendentes}" if pendentes else ""), flush=True)

    L = ["# Study 6 — the replication, in detail (MA-1, GDFT)",
         "",
         "Side by side, per outcome: gemma12's cells (seal reversed), the effect computed "
         "by the code, the published value, and the frozen comparison category. "
         "Categories that require the source are adjudicated in the evaluation record.",
         "",
         "Frozen category names (pre-registered in Portuguese, kept as labels): "
         "*reproduz* = reproduces · *difere-por-errata-da-ancora* = differs by a documented "
         "anchor erratum · *rota-do-modelo* = documented alternative reading route · "
         "*erro-do-modelo* = model error · *fonte-indisponivel* = source unavailable.",
         ""]
    resultados = {}
    for d in DESFECHOS:
        tab = next(t for t in MA if t["numero"] == d["tabela"])
        L.append(f"## {d['nome']} (anchor table {d['tabela']})")
        L.append("")
        L.append("| study | model cells (reversed) | ours | published | category |")
        L.append("|---|---|---|---|---|")
        sextetos = []
        linhas_r = []
        pub_pool = None
        for linha in tab["linhas"]:
            tid = linha.get("pmcid")
            cel = linha.get("celulas", {})
            if not tid or tid not in GAB:
                pr, pic = (rr_pub(cel) if d["tipo"] == "rr" else md_pub(cel))
                if pr is not None:
                    pub_pool = (pr, pic)
                    L.append(f"| *(anchor's pooled row: {linha.get('rotulo', 'pooled')})* | — | — | "
                             f"{'RR' if d['tipo'] == 'rr' else 'MD'} {pr} {pic} | (published pool) |")
                else:
                    print(f"  [warning] row without pmcid/effect skipped in T{d['tabela']}: "
                          f"{linha.get('rotulo')}", flush=True)
                continue
            js = fichas.get(tid)
            if d["tipo"] == "rr":
                pub_r, pub_ic = rr_pub(cel)
                if js is None:
                    nosso_txt, cat, cit = "(sheet pending)", "pending", ""
                else:
                    n1 = inteiro(valor(js, "n_randomizados_gdft"))
                    n2 = inteiro(valor(js, "n_randomizados_controle"))
                    a, fa = eventos(valor(js, d["e"]), n1)
                    c, fc = eventos(valor(js, d["c"]), n2)
                    if None in (a, c, n1, n2):
                        cat, cit = categoria(tid, [d["e"], d["c"]], False)
                        if cat.startswith("verify"):
                            cat = "insufficient"
                        else:
                            cat = "insufficient · " + cat
                        nosso_txt = "insufficient-data"
                    else:
                        r = e2.rr(a, n1, c, n2)
                        ic = e2.ic95_rr(a, n1, c, n2)
                        sextetos.append((a, n1, c, n2))
                        bate = pub_r is not None and abs(r - pub_r) <= 0.01 and \
                            abs(ic[0] - pub_ic[0]) <= 0.01 and abs(ic[1] - pub_ic[1]) <= 0.01
                        cat, cit = categoria(tid, [d["e"], d["c"], "n_randomizados_gdft",
                                                  "n_randomizados_controle"], bate)
                        marca = f" [{fa or fc}]" if (fa or fc) else ""
                        nosso_txt = f"RR {r} {ic} (a={a}/{n1}, c={c}/{n2}){marca}"
                pub_txt = f"RR {pub_r} {pub_ic}" if pub_r is not None else "—"
            else:
                pub_m, pub_ic = md_pub(cel)
                if js is None:
                    nosso_txt, cat, cit = "(sheet pending)", "pending", ""
                else:
                    m1, s1 = media_dp(valor(js, d["e"]))
                    m2, s2 = media_dp(valor(js, d["c"]))
                    n1 = inteiro(valor(js, "n_randomizados_gdft"))
                    n2 = inteiro(valor(js, "n_randomizados_controle"))
                    if None in (m1, s1, m2, s2, n1, n2):
                        cat, cit = categoria(tid, [d["e"], d["c"]], False)
                        if cat.startswith("verify"):
                            cat = "insufficient"
                        else:
                            cat = "insufficient · " + cat
                        nosso_txt = "insufficient-data"
                    else:
                        mdv = e2.md(m1, s1, n1, m2, s2, n2)
                        ic = e2.ic95_md(m1, s1, n1, m2, s2, n2)
                        bate = pub_m is not None and abs(mdv - pub_m) <= 0.1 and \
                            abs(ic[0] - pub_ic[0]) <= 0.1 and abs(ic[1] - pub_ic[1]) <= 0.1
                        cat, cit = categoria(tid, [d["e"], d["c"]], bate)
                        nosso_txt = f"MD {mdv} {ic}"
                pub_txt = f"MD {pub_m} {pub_ic}" if pub_m is not None else "—"
            celulas_dele = "; ".join(f"{k.split('_')[0]}={valor(js, k)}" for k in (d["e"], d["c"])) \
                if js else "—"
            L.append(f"| {linha['rotulo']} ({tid}) | {celulas_dele} | {nosso_txt} | {pub_txt} | "
                     f"{cat}{(' · ' + cit) if cit else ''} |")
            linhas_r.append(dict(study=linha["rotulo"], pmcid=tid, ours=nosso_txt,
                                 published=pub_txt, category=cat))
        pool_nosso = None
        if d["tipo"] == "rr" and len(sextetos) >= 2:
            pool_nosso = dict(MH=e2.pool_rr_mh(sextetos), DL=e2.pool_dl(sextetos))
            L.append("")
            comp = ""
            if pub_pool:
                dl = pool_nosso["DL"]
                bate_p = abs(dl["rr"] - pub_pool[0]) <= 0.01 and \
                    abs(dl["ic95"][0] - pub_pool[1][0]) <= 0.01 and \
                    abs(dl["ic95"][1] - pub_pool[1][1]) <= 0.01
                comp = (f" **Published: RR {pub_pool[0]} {pub_pool[1]} → "
                        f"{'REPRODUCES under DL' if bate_p else 'differs (decompose in the rows above)'}**.")
            L.append(f"**Pool (ours)**: MH {json.dumps(pool_nosso['MH'], ensure_ascii=False)} · "
                     f"DL {json.dumps(pool_nosso['DL'], ensure_ascii=False)} — comparison under DL "
                     f"(erratum-15: DL numbers, MH caption).{comp}")
        L.append("")
        resultados[d["nome"]] = dict(rows=linhas_r, pool=pool_nosso)
    D6.mkdir(exist_ok=True)
    (D6 / "resultados-por-desfecho.json").write_text(
        json.dumps(resultados, ensure_ascii=False, indent=1), encoding="utf-8")
    (D6 / "comparacao-detalhada.md").write_text("\n".join(L), encoding="utf-8")
    print("written: resultados-por-desfecho.json · comparacao-detalhada.md", flush=True)


if __name__ == "__main__":
    main()

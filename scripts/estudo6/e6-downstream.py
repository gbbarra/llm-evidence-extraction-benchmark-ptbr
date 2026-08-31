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

DESFECHOS = [
    dict(nome="morbidade", tipo="rr", tabela=5, e="morbidade_eventos_gdft", c="morbidade_eventos_controle"),
    dict(nome="mortalidade", tipo="rr", tabela=6, e="mortalidade_gdft", c="mortalidade_controle"),
    dict(nome="ileo", tipo="rr", tabela=11, e="ileo_pos_op_gdft", c="ileo_pos_op_controle"),
    dict(nome="tempo_flatus", tipo="md", tabela=8, e="tempo_flatus_gdft", c="tempo_flatus_controle"),
    dict(nome="tempo_dieta_oral", tipo="md", tabela=9, e="tempo_dieta_oral_gdft", c="tempo_dieta_oral_controle"),
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
    if not s or str(s).strip().upper() in ("NR", "NA", "N/A", ""):
        return None
    m = re.search(r"\d+", str(s))
    return int(m.group(0)) if m else None


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


def categoria(tid, campos, nossa_igual_pub):
    """Frozen classification, driven by the two-layer key's per-cell verdicts."""
    if nossa_igual_pub:
        return "reproduz", ""
    gab = GAB.get(tid, {})
    for campo in campos:
        g = gab.get(campo) or {}
        ver = str(g.get("veredito", ""))
        if "errata" in ver or "indisponivel" in ver or "figura" in ver:
            return (f"difere-por-errata-da-ancora" if "errata" in ver else "fonte-indisponivel",
                    (g.get("cit") or "")[:140])
    return "verificar (rota-do-modelo ou erro-do-modelo — adjudicar na fonte)", ""


def main():
    fichas = {}
    pendentes = []
    for tid in GAB.keys():
        js = ficha(tid)
        if js:
            fichas[tid] = desperturba(tid, js)
        else:
            pendentes.append(tid)
    print(f"fichas disponíveis: {len(fichas)}/{len(GAB)}"
          + (f" · pendentes: {pendentes}" if pendentes else ""), flush=True)

    L = ["# Estudo 6 — a replicação em detalhe (MA-1, GDFT)",
         "",
         "Lado a lado, por desfecho: as células do gemma12 (selo revertido), o efeito computado "
         "pelo código, o valor publicado, e a categoria congelada da comparação. "
         "Categorias que exigem fonte são adjudicadas no registro de avaliação.",
         ""]
    resultados = {}
    for d in DESFECHOS:
        tab = next(t for t in MA if t["numero"] == d["tabela"])
        L.append(f"## {d['nome']} (tabela {d['tabela']} da âncora)")
        L.append("")
        L.append("| estudo | células (dele, revertidas) | nosso | publicado | categoria |")
        L.append("|---|---|---|---|---|")
        sextetos = []
        linhas_r = []
        for linha in tab["linhas"]:
            tid = linha.get("pmcid")
            if not tid or tid not in GAB:
                continue
            cel = linha.get("celulas", {})
            js = fichas.get(tid)
            if d["tipo"] == "rr":
                pub_r, pub_ic = rr_pub(cel)
                if js is None:
                    nosso_txt, cat, cit = "(ficha pendente)", "pendente", ""
                else:
                    a = inteiro(valor(js, d["e"]))
                    c = inteiro(valor(js, d["c"]))
                    n1 = inteiro(valor(js, "n_randomizados_gdft"))
                    n2 = inteiro(valor(js, "n_randomizados_controle"))
                    if None in (a, c, n1, n2):
                        nosso_txt, cat, cit = "dados-insuficientes", "insuficiente", ""
                    else:
                        r = e2.rr(a, n1, c, n2)
                        ic = e2.ic95_rr(a, n1, c, n2)
                        sextetos.append((a, n1, c, n2))
                        bate = pub_r is not None and abs(r - pub_r) <= 0.01 and \
                            abs(ic[0] - pub_ic[0]) <= 0.01 and abs(ic[1] - pub_ic[1]) <= 0.01
                        cat, cit = categoria(tid, [d["e"], d["c"], "n_randomizados_gdft",
                                                  "n_randomizados_controle"], bate)
                        nosso_txt = f"RR {r} {ic} (a={a}/{n1}, c={c}/{n2})"
                pub_txt = f"RR {pub_r} {pub_ic}" if pub_r is not None else "—"
            else:
                pub_m, pub_ic = md_pub(cel)
                if js is None:
                    nosso_txt, cat, cit = "(ficha pendente)", "pendente", ""
                else:
                    m1, s1 = media_dp(valor(js, d["e"]))
                    m2, s2 = media_dp(valor(js, d["c"]))
                    n1 = inteiro(valor(js, "n_randomizados_gdft"))
                    n2 = inteiro(valor(js, "n_randomizados_controle"))
                    if None in (m1, s1, m2, s2, n1, n2):
                        nosso_txt, cat, cit = "dados-insuficientes", "insuficiente", ""
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
            linhas_r.append(dict(estudo=linha["rotulo"], pmcid=tid, nosso=nosso_txt,
                                 publicado=pub_txt, categoria=cat))
        pool_nosso = None
        if d["tipo"] == "rr" and len(sextetos) >= 2:
            pool_nosso = dict(MH=e2.pool_rr_mh(sextetos), DL=e2.pool_dl(sextetos))
            L.append("")
            L.append(f"**Pool (nosso)**: MH {json.dumps(pool_nosso['MH'], ensure_ascii=False)} · "
                     f"DL {json.dumps(pool_nosso['DL'], ensure_ascii=False)} — a comparação com o "
                     "publicado é feita sob DL (errata-15 da âncora: números DL, legenda MH).")
        L.append("")
        resultados[d["nome"]] = dict(linhas=linhas_r, pool=pool_nosso)
    D6.mkdir(exist_ok=True)
    (D6 / "resultados-por-desfecho.json").write_text(
        json.dumps(resultados, ensure_ascii=False, indent=1), encoding="utf-8")
    (D6 / "comparacao-detalhada.md").write_text("\n".join(L), encoding="utf-8")
    print("gravado: resultados-por-desfecho.json · comparacao-detalhada.md", flush=True)


if __name__ == "__main__":
    main()

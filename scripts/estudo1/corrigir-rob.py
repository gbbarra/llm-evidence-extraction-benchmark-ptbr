# -*- coding: utf-8 -*-
"""EXTRAI E1 — correção da T2 (risco de viés): concordância modelo × revisores da MA.

Métricas:
- concordância nos 7 domínios Cochrane (julgamento igual, case-insensitive), por modelo
  e por domínio; o julgamento global é reportado à parte (a MA usa escala própria com
  "Moderate", que não existe em Low/High/Unclear pedido aos modelos);
- estabilidade entre réplicas (r1 vs r2);
- Weinberg fica fora do denominador (a MA não tem linha de RoB para ele — inconsistência
  pré-registrada nº 1; a linha "Ramsingh", de estudo não incluído, também fica fora).

Saída: dados/estudo1/correcao/rob-resumo.json + tabela no stdout
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
D1 = RAIZ / "dados" / "estudo1"

DOMINIOS = [
    ("geracao_sequencia_aleatoria", "Random sequence"),
    ("ocultacao_alocacao", "Allocation conceal"),
    ("cegamento_participantes_equipe", "Blinding (participants"),
    ("cegamento_avaliadores_desfecho", "Blinding (outcome"),
    ("dados_desfecho_incompletos", "Incomplete outcome"),
    ("relato_seletivo", "Selective reporting"),
    ("outros_vieses", "Other bias"),
]
GLOBAL = ("risco_global", "Overall risk")


def parse(content):
    try:
        return json.loads(re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip()))
    except Exception:
        return None


def norm(j):
    return str(j or "").strip().lower()


def main():
    gab = json.loads((D1 / "gabarito-ma.json").read_text(encoding="utf-8"))
    rob_ma = {}
    for t in gab["tabelas"]:
        if t["numero"] == 1:
            for l in t["linhas"]:
                if l.get("pmcid"):
                    rob_ma[l["pmcid"]] = l["celulas"]
    modelos = sorted(d.name for d in (D1 / "saidas").iterdir()
                     if d.is_dir() and not d.name.startswith("smoke"))
    resumo = {}
    por_dominio = {ch: {"conc": 0, "tot": 0} for ch, _ in DOMINIOS}
    print(f"{'modelo':<9} {'domínios':>9} {'concorda':>9} {'%':>5} | {'global igual':>12} | {'estab. r1=r2':>12}")
    for mod in modelos:
        conc = tot = 0
        gl_conc = gl_tot = 0
        est_ig = est_tot = 0
        det = {}
        for f in sorted((D1 / "saidas" / mod).glob("*-t2-r1.json")):
            d = json.loads(f.read_text(encoding="utf-8"))
            pm = d["pmcid"]
            j1 = parse(d["content"]) or {}
            f2 = D1 / "saidas" / mod / f"{pm}-t2-r2.json"
            j2 = parse(json.loads(f2.read_text(encoding="utf-8"))["content"]) if f2.exists() else {}
            j2 = j2 or {}
            ma_row = rob_ma.get(pm)
            det_pm = {}
            for chave, prefixo in DOMINIOS + [GLOBAL]:
                v1 = norm(j1.get(chave, {}).get("julgamento"))
                v2 = norm(j2.get(chave, {}).get("julgamento"))
                if v1 and v2:
                    est_tot += 1
                    est_ig += (v1 == v2)
                if not ma_row:
                    det_pm[chave] = dict(modelo=v1, ma=None)
                    continue
                col = next((k for k in ma_row if k.lower().startswith(prefixo.lower())), None)
                ma_v = norm(ma_row.get(col))
                det_pm[chave] = dict(modelo=v1, ma=ma_v)
                if not v1 or not ma_v:
                    continue
                if chave == "risco_global":
                    gl_tot += 1
                    gl_conc += (v1 == ma_v)
                else:
                    tot += 1
                    ok = (v1 == ma_v)
                    conc += ok
                    por_dominio[chave]["tot"] += 1
                    por_dominio[chave]["conc"] += ok
            det[pm] = det_pm
        resumo[mod] = dict(dominios_conc=conc, dominios_tot=tot,
                           global_conc=gl_conc, global_tot=gl_tot,
                           estab_ig=est_ig, estab_tot=est_tot, detalhe=det)
        print(f"{mod:<9} {tot:>9} {conc:>9} {100*conc/tot if tot else 0:>4.0f}% | "
              f"{gl_conc}/{gl_tot:>10} | {100*est_ig/est_tot if est_tot else 0:>10.0f}%")
    print("\npor domínio (todos os modelos):")
    for chave, _ in DOMINIOS:
        c = por_dominio[chave]
        print(f"  {chave:<32} {c['conc']:>3}/{c['tot']:<3} {100*c['conc']/c['tot'] if c['tot'] else 0:>4.0f}%")
    (D1 / "correcao" / "rob-resumo.json").write_text(
        json.dumps(dict(por_dominio=por_dominio, modelos=resumo), ensure_ascii=False, indent=1),
        encoding="utf-8")
    print("\nsalvo: dados/estudo1/correcao/rob-resumo.json")


if __name__ == "__main__":
    main()

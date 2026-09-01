# -*- coding: utf-8 -*-
"""Study 8 / P2 CALCULATE — grading (the Study-2 rubric, English port).

Truth = the validated engine over each model's OWN P1 cells, parsed by the
frozen Study-2 rules (events from "19 (32.8%)"; percent-only converts against
n; means only as "m ± sd" — median(IQR) has no computable truth, so
NOT-COMPUTABLE is the correct answer there). Labels per reported quantity:
exata / direcao-certa / errada / nc-correta / nc-recusa / sem-verdade, with
intervals graded separately (ic-exata / ic-errada). Pools graded against the
engine over the same parseable studies.

Run: python scripts/estudo8/p2-avalia.py
Output: dados/estudo8/avaliacao-p2.json (+ console table)
"""
import importlib.util
import json
import re
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


c2 = carrega("c2", "scripts/estudo2/corrigir-e2.py")
p2r = carrega("p2r", "scripts/estudo8/p2-calculate.py")
e2 = p2r.e2

OUTCOMES_RR = [d for d, _, _ in p2r.CAMPOS_FAM["rr"]]
OUTCOMES_MD = [d for d, _, _ in p2r.CAMPOS_FAM["md"]]


def insumo_en(mod):
    por = e2.estudos_por_desfecho()
    mapa = {"morbidity": "morbidade", "mortality": "mortalidade", "ileus": "ileo",
            "time_to_flatus_h": "tempo_flatus_h", "time_to_oral_diet": "tempo_dieta_oral"}
    dados = {}
    for desfecho, c_g, c_c in p2r.CAMPOS_FAM["rr"]:
        for pm in por[mapa[desfecho]]:
            j = p2r.ficha_p1(mod, pm)
            ng = c2.parse_n(p2r.cel(j, "n_randomized_gdft"))
            nc = c2.parse_n(p2r.cel(j, "n_randomized_control"))
            a = c2.parse_eventos(p2r.cel(j, c_g), ng)
            c = c2.parse_eventos(p2r.cel(j, c_c), nc)
            dados[(desfecho, e2.ROT[pm])] = (a, ng, c, nc) if None not in (a, ng, c, nc) else None
    for desfecho, c_g, c_c in p2r.CAMPOS_FAM["md"]:
        for pm in por[mapa[desfecho]]:
            j = p2r.ficha_p1(mod, pm)
            mg = c2.parse_media(p2r.cel(j, c_g))
            mc = c2.parse_media(p2r.cel(j, c_c))
            ng = c2.parse_n(p2r.cel(j, "n_randomized_gdft"))
            nc = c2.parse_n(p2r.cel(j, "n_randomized_control"))
            dados[(desfecho, e2.ROT[pm])] = (mg[0], mg[1], ng, mc[0], mc[1], nc) \
                if mg and mc and ng and nc else None
    return dados


def norm_out(s):
    return str(s).strip().lower().replace("í", "i").replace("-", "_").replace(" ", "_")


def corrige(mod, braco, rep, insumo):
    contas = {}
    for familia in ("rr", "md", "pool"):
        f = E8 / "saidas" / "p2" / mod / f"{familia}-{braco}-r{rep}.json"
        d = json.loads(f.read_text(encoding="utf-8"))
        js = c2.acha_json(d["transcricao"][-1]["saida"])
        if js is None:
            contas["json-invalido"] = contas.get("json-invalido", 0) + 1
            continue
        if familia in ("rr", "md"):
            for desfecho, bloco in js.items():
                dn = norm_out(desfecho)
                if not isinstance(bloco, dict):
                    continue
                rots = [r for (dfx, r) in insumo if dfx == dn]
                for est, val in bloco.items():
                    rot = c2.nome_estudo(est, rots)
                    ins = insumo.get((dn, rot))
                    ponto = val.get("rr") if isinstance(val, dict) else val
                    if ponto is None and isinstance(val, dict):
                        ponto = val.get("md")
                    if ins is None:
                        r = "nc-correta" if (c2.eh_nc(ponto) or ponto is None) else "sem-verdade"
                    elif c2.eh_nc(ponto) or ponto is None:
                        r = "nc-recusa"
                    else:
                        if familia == "rr":
                            r = c2.rotula(ponto, e2.rr(*ins), 0.01)
                        else:
                            t = e2.md(*ins)
                            r = c2.rotula(ponto, t, 0.1) if abs(t) > 0.001 else \
                                ("exata" if abs(float(ponto)) <= 0.1 else "errada")
                        ic = val.get("ci95") or val.get("ic95") if isinstance(val, dict) else None
                        if isinstance(ic, list) and len(ic) == 2 and not c2.eh_nc(ic[0]):
                            tic = e2.ic95_rr(*ins) if familia == "rr" else e2.ic95_md(*ins)
                            tol = 0.01 if familia == "rr" else 0.1
                            try:
                                ric = "exata" if (abs(float(ic[0]) - tic[0]) <= tol
                                                  and abs(float(ic[1]) - tic[1]) <= tol) else "errada"
                            except (TypeError, ValueError):
                                ric = "errada"
                            contas[f"ic-{ric}"] = contas.get(f"ic-{ric}", 0) + 1
                    if r:
                        contas[r] = contas.get(r, 0) + 1
        else:
            for desfecho, bloco in js.items():
                dn = norm_out(desfecho)
                if not isinstance(bloco, dict):
                    continue
                ests = [ins for (dfx, r), ins in insumo.items() if dfx == dn and ins]
                if len(ests) < 2:
                    continue
                metodos = (("mh", e2.pool_rr_mh), ("dl", e2.pool_dl)) if dn in OUTCOMES_RR \
                    else (("iv", e2.pool_md_iv),)
                for metodo, fn in metodos:
                    mv = bloco.get(metodo)
                    if not isinstance(mv, dict):
                        if c2.eh_nc(mv):
                            contas["pool-nc"] = contas.get("pool-nc", 0) + 1
                        continue
                    t = fn(ests)
                    chave = "rr" if dn in OUTCOMES_RR else "md"
                    ponto = mv.get(chave)
                    tol = 0.01 if chave == "rr" else 0.1
                    try:
                        ok = ponto is not None and abs(float(ponto) - t[chave]) <= tol
                    except (TypeError, ValueError):
                        ok = False
                    contas[f"pool-{'exata' if ok else 'errada'}"] = \
                        contas.get(f"pool-{'exata' if ok else 'errada'}", 0) + 1
    return contas


def main():
    res = {}
    for mod in CAST:
        insumo = insumo_en(mod)
        for braco in ("A", "B"):
            tot = {}
            for rep in (1, 2):
                for k, v in corrige(mod, braco, rep, insumo).items():
                    tot[k] = tot.get(k, 0) + v
            res[f"{mod}-{braco}"] = tot
    (E8 / "avaliacao-p2.json").write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                          encoding="utf-8")
    chaves = ["exata", "direcao-certa", "errada", "ic-exata", "ic-errada",
              "pool-exata", "pool-errada", "pool-nc", "nc-correta", "nc-recusa",
              "sem-verdade", "json-invalido"]
    print(f"{'model-arm':<16}" + "".join(f"{k:>14}" for k in chaves))
    for mb, tot in res.items():
        print(f"{mb:<16}" + "".join(f"{tot.get(k, 0):>14}" for k in chaves))


if __name__ == "__main__":
    main()

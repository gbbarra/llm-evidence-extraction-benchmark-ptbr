# -*- coding: utf-8 -*-
"""Study 5 Amendment 8 — the four cheap arms, analyzed mechanically.

A: replicate agreement (CALC3 vs CALC3R2, truth-free rule, then graded).
B: temperature-zero twins (CALC3T1 vs CALC3T2: identical? exact?).
C: orchestrator committee (CALC3 base vs CALC3F coder, truth-free rule).
D: product flags (missing-study; weight dominance > 40% DL weight) applied
   retroactively to the three pipeline pools.
Arms with missing inputs are skipped and reported as pending.

Run: python scripts/estudo5/bracos-baratos.py
Output: dados/estudo5/resultados-bracos-baratos.json
"""
import importlib.util
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
D5 = ROOT / "dados" / "estudo5"
EX3 = D5 / "saidas" / "EXTRA3"


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


e5 = carrega("e5", "scripts/estudo5/e5-harness.py")
h3 = e5.h3
c3 = carrega("c3", "scripts/estudo3/corrigir-e3.py")


def final_de(rung, tid):
    f = D5 / "saidas" / rung / f"{tid}.json"
    if not f.exists():
        return None
    return json.loads(f.read_text(encoding="utf-8")).get("final")


def verdade(tid):
    s = c3.sexteto(e5.ficha_r2(tid, EX3))
    return dict(md=h3.md(*s), ic=h3.ic95_md(*s)) if s else None


def igual(a, b):
    return bool(a and b and a.get("ic95") and b.get("ic95")
                and abs(a["md"] - b["md"]) <= 0.01
                and abs(a["ic95"][0] - b["ic95"][0]) <= 0.01
                and abs(a["ic95"][1] - b["ic95"][1]) <= 0.01)


def exato(f, v):
    return bool(f and v and f.get("ic95") and abs(f["md"] - v["md"]) <= 0.01
                and abs(f["ic95"][0] - v["ic"][0]) <= 0.01
                and abs(f["ic95"][1] - v["ic"][1]) <= 0.01)


def regra(f1, f2, nome1, nome2):
    """The frozen truth-free rule: agree -> accept; one null -> single-source;
    both present but different -> discordant."""
    if igual(f1, f2):
        return dict(veredito="aceito-concordante", final=f1)
    if f1 and not f2:
        return dict(veredito=f"single-source ({nome1})", final=f1, bandeira=True)
    if f2 and not f1:
        return dict(veredito=f"single-source ({nome2})", final=f2, bandeira=True)
    if not f1 and not f2:
        return dict(veredito="ausente", final=None, bandeira=True)
    return dict(veredito="discordante (humano)", final=None, bandeira=True)


def braco_composicao(rung1, rung2, nome1, nome2, titulo):
    if not (D5 / "saidas" / rung1).exists() or not (D5 / "saidas" / rung2).exists():
        print(f"  {titulo}: PENDENTE (faltam saídas)")
        return dict(status="pendente")
    linhas = []
    auto_certos = auto_total = 0
    for tid in h3.TRIALS:
        r = regra(final_de(rung1, tid), final_de(rung2, tid), nome1, nome2)
        v = verdade(tid)
        r["estudo"] = h3.ROT[tid]
        if r["veredito"] == "aceito-concordante":
            auto_total += 1
            auto_certos += exato(r["final"], v)
            r["exato_vs_verdade"] = exato(r["final"], v)
        linhas.append(r)
        print(f"  {r['estudo']}: {r['veredito']}"
              + (f" · exato: {r.get('exato_vs_verdade')}" if "exato_vs_verdade" in r else ""))
    print(f"  => auto-aceitos exatos: {auto_certos}/{auto_total} · sinalizados: "
          f"{sum(1 for l in linhas if l.get('bandeira'))}")
    return dict(status="ok", linhas=linhas, auto_aceitos_exatos=f"{auto_certos}/{auto_total}")


def braco_t0():
    if not (D5 / "saidas" / "CALC3T1").exists() or not (D5 / "saidas" / "CALC3T2").exists():
        print("  T0: PENDENTE")
        return dict(status="pendente")
    identicos = exatos1 = 0
    linhas = []
    for tid in h3.TRIALS:
        f1, f2 = final_de("CALC3T1", tid), final_de("CALC3T2", tid)
        t1 = (D5 / "saidas" / "CALC3T1" / f"{tid}.json").read_text(encoding="utf-8")
        t2 = (D5 / "saidas" / "CALC3T2" / f"{tid}.json").read_text(encoding="utf-8")
        gem = json.loads(t1)["turnos"] == json.loads(t2)["turnos"]
        identicos += gem
        v = verdade(tid)
        exatos1 += exato(f1, v)
        linhas.append(dict(estudo=h3.ROT[tid], turnos_identicos=gem,
                           finais_iguais=igual(f1, f2), exato_t1=exato(f1, v)))
        print(f"  {h3.ROT[tid]}: turnos idênticos={gem} · finais iguais={igual(f1, f2)} "
              f"· exato={exato(f1, v)}")
    print(f"  => gêmeos turno-a-turno: {identicos}/7 · exatos (T1): {exatos1}/7")
    return dict(status="ok", linhas=linhas, gemeos=f"{identicos}/7", exatos_t1=f"{exatos1}/7")


def braco_bandeiras():
    LIMITE = 0.40
    saida = []
    for nome, res_pool, origem in (("v1", "resultados-G3PIPE.json", "G2PIPE"),
                                   ("v2", "resultados-POOL2.json", "CALC2"),
                                   ("v3", "resultados-POOL3.json", "CALC3")):
        f = D5 / res_pool
        if not f.exists():
            continue
        reg = json.loads(f.read_text(encoding="utf-8"))
        proprios = e5.sextetos_do_g2b(origem)
        sx = [d["sexteto"] for d in proprios.values()]
        nomes = list(proprios.keys())
        ausentes = [h3.ROT[t] for t in h3.TRIALS if h3.ROT[t] not in nomes]
        pool = h3.pool_dl_md(sx)
        tau2 = pool["tau2"]
        pesos = []
        for s in sx:
            v = s[1] ** 2 / s[2] + s[4] ** 2 / s[5]
            pesos.append(1 / (v + tau2))
        soma = sum(pesos)
        dominantes = [(n, round(100 * p / soma, 1)) for n, p in zip(nomes, pesos)
                      if p / soma > LIMITE]
        band = []
        if ausentes:
            band.append(f"ESTUDO-AUSENTE: {ausentes}")
        for n, pct in dominantes:
            band.append(f"DOMINÂNCIA: {n} = {pct}% do peso (limite 40%)")
        saida.append(dict(pipeline=nome, bandeiras=band or ["nenhuma"]))
        print(f"  {nome}: " + ("; ".join(band) if band else "nenhuma bandeira"))
    return saida


def main():
    print("== Braço C — comitê de orquestradores (CALC3 base × CALC3F coder):")
    comite = braco_composicao("CALC3", "CALC3F", "base", "coder", "comitê")
    print("\n== Braço A — réplica de orquestração (CALC3 × CALC3R2):")
    replica = braco_composicao("CALC3", "CALC3R2", "réplica 1", "réplica 2", "réplica")
    print("\n== Braço B — gêmeos a temperatura zero (CALC3T1 × CALC3T2):")
    t0 = braco_t0()
    print("\n== Braço D — bandeiras de produto sobre os três pipelines:")
    bandeiras = braco_bandeiras()
    (D5 / "resultados-bracos-baratos.json").write_text(
        json.dumps(dict(comite=comite, replica=replica, t0=t0, bandeiras=bandeiras),
                   ensure_ascii=False, indent=1), encoding="utf-8")
    print("\ngravado dados/estudo5/resultados-bracos-baratos.json")


if __name__ == "__main__":
    main()

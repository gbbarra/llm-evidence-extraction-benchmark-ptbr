# -*- coding: utf-8 -*-
"""EXTRAI Study 4 — mechanical evaluation (protocol §3).

Per model: (1) cell grading of both replicates against the Study-3 amended
EXPECTED ruler (same rotula_cel, same routes); (2) replicate agreement over
the graded numeric cells (comparable to Study 3's cell-identity bar, unlike
the pipeline's whole-JSON check); (3) own-sheet mechanical truth — the
graders' sexteto over the same first-parseable sheets, documented
resolutions, NO judgment overrides — and |pool − truth| per bound (primary
metric); (4) the unperturbation lens — sealed reversal over the same sheets,
graders' sexteto — vs the anchor's published −0.24 [−0.32, −0.16] (secondary).

Run: python scripts/estudo4/avalia-e4.py
Outputs: dados/estudo4/correcao/extracao.json · dados/estudo4/avaliacao-mecanica.json
"""
import importlib.util
import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
# E4_DIR points the whole evaluation at another round's tree (e.g. rodada2/)
D4 = Path(os.environ["E4_DIR"]) if os.environ.get("E4_DIR") else ROOT / "dados" / "estudo4"
MODELOS = sys.argv[1:] or ["gemma12", "qwen14"]
SUFIXO = ("-" + "-".join(MODELOS)) if sys.argv[1:] else ""


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


h3 = carrega("h3", "scripts/estudo3/e3-harness.py")
c3 = carrega("c3", "scripts/estudo3/corrigir-e3.py")
selo = json.loads((ROOT / "dados" / "estudo3" / "perturbacoes-estudo3.json").read_text(encoding="utf-8"))


def ficha_bruta(modelo, tid, rep):
    f = D4 / "saidas" / modelo / "extracao" / f"{tid}-r{rep}.json"
    if not f.exists():
        return None
    return h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])


def primeira_parseavel(modelo, tid):
    for rep in (1, 2):
        js = ficha_bruta(modelo, tid, rep)
        if js:
            return js, rep
    return None, None


def desperturba(tid, ficha):
    txt = json.dumps(ficha, ensure_ascii=False)
    for reg in selo.get(tid, []):
        p, o = str(reg["perturbado"]), str(reg["original"])
        txt = txt.replace(f'"{p}"', f'"{o}"').replace(f'"-{p}"', f'"-{o}"')
        txt = txt.replace(f" {p}", f" {o}").replace(f"-{p}", f"-{o}")
    return json.loads(txt)


def corrige_celulas():
    placar = {}
    detalhes = []
    for modelo in MODELOS:
        for tid in h3.TRIALS:
            for rep in (1, 2):
                js = ficha_bruta(modelo, tid, rep)
                chave = f"{modelo}/{tid}-r{rep}"
                if not js:
                    placar[chave] = dict(parse=False)
                    continue
                contas = {}
                for caminho, esperado in c3.EXPECTED[tid].items():
                    r = c3.rotula_cel(c3.pega(js, caminho), esperado)
                    contas[r] = contas.get(r, 0) + 1
                    detalhes.append(dict(modelo=modelo, trial=tid, rep=rep, campo=caminho,
                                         valor=c3.pega(js, caminho),
                                         aceitos=esperado["aceitos"], rotulo=r))
                placar[chave] = dict(parse=True, **contas)
    (D4 / "correcao").mkdir(exist_ok=True)
    (D4 / "correcao" / f"extracao{SUFIXO}.json").write_text(
        json.dumps(dict(placar=placar, detalhes=detalhes), ensure_ascii=False, indent=1), encoding="utf-8")
    print("== células vs régua EXPECTED (E3 emendada)")
    resumo = {}
    for modelo in MODELOS:
        boas = tot = 0
        adjudicar = []
        for chave, cnt in placar.items():
            if not chave.startswith(modelo + "/") or not cnt.get("parse"):
                continue
            boas += cnt.get("exata", 0) + cnt.get("nr-correta", 0) + cnt.get("derivavel", 0)
            tot += sum(v for k, v in cnt.items() if k != "parse")
        for d in detalhes:
            if d["modelo"] == modelo and d["rotulo"] == "adjudicar":
                adjudicar.append(f"{d['trial']}-r{d['rep']} {d['campo']}={d['valor']}")
        resumo[modelo] = dict(boas=boas, total=tot, pct=round(100 * boas / tot, 1),
                              adjudicar=adjudicar)
        print(f"  {modelo}: {boas}/{tot} ({resumo[modelo]['pct']}%) · adjudicar: {len(adjudicar)}")
        for a in adjudicar:
            print(f"    ? {a}")
    return placar, resumo


def concordancia_celulas(modelo):
    """Replicate agreement over the graded cells only (Study-3 comparable)."""
    iguais = tot = 0
    for tid in h3.TRIALS:
        r1, r2 = ficha_bruta(modelo, tid, 1), ficha_bruta(modelo, tid, 2)
        if not r1 or not r2:
            continue
        for caminho in c3.EXPECTED[tid]:
            v1, v2 = c3.pega(r1, caminho), c3.pega(r2, caminho)
            tot += 1
            n1, n2 = c3.num(v1), c3.num(v2)
            if (n1 is not None and n2 is not None and abs(n1 - n2) <= 0.005) or \
               (str(v1).strip().upper() == str(v2).strip().upper()):
                iguais += 1
    return dict(iguais=iguais, total=tot, pct=round(100 * iguais / tot, 1) if tot else None)


def diamantes(modelo):
    """Own-sheet truth (graders' sexteto, no overrides) + unperturbed lens."""
    sext_v, sext_d = [], []
    reps = {}
    for tid in h3.TRIALS:
        f, rep = primeira_parseavel(modelo, tid)
        if not f:
            continue
        reps[tid] = rep
        s = c3.sexteto(f)
        if s:
            sext_v.append(s)
        sd = c3.sexteto(desperturba(tid, f))
        if sd:
            sext_d.append(sd)
    verdade = h3.pool_dl_md(sext_v) if sext_v else None
    lente = h3.pool_dl_md(sext_d) if sext_d else None
    return verdade, lente, reps


def main():
    assert h3.ELENCO == "base"
    placar, resumo_cel = corrige_celulas()
    aval = dict(regua="EXPECTED E3 emendada (corrigir-e3.py)", celulas=resumo_cel, modelos={})
    print("\n== diamantes (verdade própria · lente desperturbada · réplicas)")
    for modelo in MODELOS:
        res = json.loads((D4 / "resultados" / f"{modelo}.json").read_text(encoding="utf-8"))
        pool = res["agregado"]
        verdade, lente, _ = diamantes(modelo)
        conc = concordancia_celulas(modelo)
        delta = dict(md=round(abs(pool["md"] - verdade["md"]), 2),
                     ic=[round(abs(pool["ic95"][i] - verdade["ic95"][i]), 2) for i in (0, 1)])
        aval["modelos"][modelo] = dict(
            pool_pipeline=pool, verdade_mecanica=verdade, delta_pool_verdade=delta,
            lente_desperturbada=lente,
            ancora_publicada=dict(md=-0.24, ic95=[-0.32, -0.16], i2_pct=6),
            concordancia_replicas_celulas=conc,
            gatilhos=res["gatilhos"])
        print(f"  {modelo}: pipeline {json.dumps(pool['md'])} {pool['ic95']}"
              f" · verdade {verdade['md']} {verdade['ic95']} · Δ md={delta['md']} ic={delta['ic']}")
        print(f"    lente desperturbada: {lente['md']} {lente['ic95']} i2={lente['i2_pct']}%"
              f" · réplicas células: {conc['pct']}% ({conc['iguais']}/{conc['total']})")
    (D4 / f"avaliacao-mecanica{SUFIXO}.json").write_text(
        json.dumps(aval, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\ngravado: dados/estudo4/correcao/extracao.json · dados/estudo4/avaliacao-mecanica.json")


if __name__ == "__main__":
    main()

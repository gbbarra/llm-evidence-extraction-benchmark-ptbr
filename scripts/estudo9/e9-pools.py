# -*- coding: utf-8 -*-
"""EXTRAI Study 9 — the Anchor-2 diamonds from the v2 (quote-bearing) sheets.

Same deterministic engine, same route selector, same sealed lens as the campaign
(`scripts/estudo8/p3-avalia.py`): nothing here is new arithmetic. The only difference
is the input -- v2 sheets, whose cells are {value, where, quote} instead of
{value, where}. `ficha_ma2_pt` already reads `.get("value")` from an object cell, so
the campaign's own converter consumes both schemas unchanged; the A/B keeps a single
changed variable.

Run: python scripts/estudo9/e9-pools.py [model ...]
Out: dados/estudo9/pools-ma2.json (+ console table)
"""
import importlib.util
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
E9 = ROOT / "dados" / "estudo9"
CAST = ["granite8", "gemma12", "qwen14", "llama8"]


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


p3 = carrega("p3", "scripts/estudo8/p3-avalia.py")   # motor, selo, rotulos e publicado
h3, dg, e7d = p3.h3, p3.dg, p3.e7d
PUB2, SELO3 = p3.PUB2, p3.SELO3


def bruta(modelo, tid):
    """Primeira replicata parseavel, como no P1 da campanha."""
    for rep in (1, 2):
        f = E9 / "saidas" / "v2" / modelo / "ma2" / f"{tid}-r{rep}.json"
        if f.exists():
            js = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
            if isinstance(js, dict):
                return js
    return None


def achata_v2(js):
    """Converte a ficha v2 no formato que o motor congelado espera.

    Verificado no codigo, nao presumido: `braco_pt` copia a celula inteira
    (`out[pt] = b[en]`), o que no v1 era o proprio valor e no v2 e o objeto
    {value, where, quote}. Sem achatar, o motor recebe dicionario onde espera numero
    e todos os sextetos falham. As citacoes ficam preservadas nas fichas originais --
    aqui so se extrai o valor, que e a unica coisa que a aritmetica consome.
    """
    def achata(obj):
        if isinstance(obj, dict) and "value" in obj:
            return obj.get("value")
        if isinstance(obj, dict):
            return {k: achata(v) for k, v in obj.items()}
        return obj
    return achata(js)


def ma2(modelo):
    sx, sx_lens, faltas = [], [], []
    for tid in h3.TRIALS:
        js = bruta(modelo, tid)
        if not js:
            faltas.append(h3.ROT[tid] + " (unparseable)")
            continue
        f = e7d.ficha_ma2_pt(achata_v2(js))
        s = p3.sexteto_de(f)
        if s:
            sx.append(s)
        else:
            faltas.append(h3.ROT[tid])
        sl = p3.sexteto_de(p3.lens_sexteto(f, tid))
        if sl:
            sx_lens.append(sl)
    pool = h3.pool_dl_md(sx) if len(sx) >= 2 else None
    lens = h3.pool_dl_md(sx_lens) if len(sx_lens) >= 2 else None
    beside = bool(lens and abs(lens["md"] - PUB2["md"]) <= 0.05
                  and abs(lens["ic95"][0] - PUB2["ic95"][0]) <= 0.05
                  and abs(lens["ic95"][1] - PUB2["ic95"][1]) <= 0.05)
    return dict(estudos_no_pool=len(sx), faltas=faltas, pool_perturbado=pool,
                lens=lens, publicado=PUB2, lens_beside_published=beside)


def linha(rot, d):
    l = d.get("lens")
    if not l:
        return f"{rot:<12}{'(sem pool)':>26}"
    return (f"{rot:<12}{l['md']:>7.2f} [{l['ic95'][0]:>6.2f},{l['ic95'][1]:>6.2f}]"
            f"{l.get('i2_pct', 0):>8.1f}%{d['estudos_no_pool']:>6}/7"
            f"{'  ← ao lado do publicado' if d['lens_beside_published'] else ''}")


def main():
    alvo = sys.argv[1:] or CAST
    print(f"\n=== Study 9 · Anchor-2 diamonds from the v2 sheets ===")
    print(f"published: {PUB2['md']} [{PUB2['ic95'][0]}, {PUB2['ic95'][1]}]  (I2 6%)\n")
    print(f"{'model':<12}{'lens MD [95% CI]':>26}{'I2':>9}{'trials':>8}")
    out = {}
    for m in alvo:
        if not (E9 / "saidas" / "v2" / m / "ma2").exists():
            print(f"{m:<12}{'(nao rodou)':>26}")
            continue
        d = ma2(m)
        out[m] = d
        print(linha(m, d))
        if d["faltas"]:
            print(f"{'':<12}faltas: {', '.join(d['faltas'])}")
    f = E9 / "pools-ma2.json"
    antigo = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    antigo.update(out)
    f.write_text(json.dumps(antigo, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nsaved: {f}")


if __name__ == "__main__":
    main()

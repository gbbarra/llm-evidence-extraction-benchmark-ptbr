# -*- coding: utf-8 -*-
"""EXTRAI Study 3 — Amendment 5: the audit committee as a mechanism.

Builds committee-audited sheets from the three casts' EXISTING lane-S audit
verdicts (independent runs over identical seeded inputs; no new audit runs)
under two pre-registered combination rules, then runs the baseline calculator
(qwen3.8:27b) and synthesist (gemma4:26b) once per rule under the frozen v2
harness rules.

  Rule OR-27B : flagged by 27B or 14B -> corrected; value conflicts -> 27B.
  Rule MAJ-3  : flagged by >=2 of {27B, 14B, 12B} -> corrected; value = the
                one two members agree on, else the 27B's.

Outputs: dados/estudo3/saidas-comite/{fichas,calc,sintese}-<regra>.json
Run: python scripts/estudo3/comite.py  (E3_ELENCO must be unset/base)
"""
import importlib.util
import json
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
D3 = ROOT / "dados" / "estudo3"
OUT = D3 / "saidas-comite"

_spec = importlib.util.spec_from_file_location("h3", ROOT / "scripts" / "estudo3" / "e3-harness.py")
h3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h3)
assert h3.ELENCO == "base", "run with E3_ELENCO unset: the committee uses the baseline calculator"

MEMBROS = {"27B": "saidas", "14B": "saidas-igpu", "12B": "saidas-allgemma"}


def achatar(vs):
    plano = {}

    def anda(d, trilha=""):
        if isinstance(d, dict):
            if "veredito" in d:
                plano[trilha] = d
            else:
                for k, v in d.items():
                    anda(v, f"{trilha}.{k}" if trilha else k)

    anda(vs)
    return plano


def vereditos(membro, tid):
    f = D3 / MEMBROS[membro] / "auditoria" / f"{tid}-S.json"
    aud = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"]) or {}
    plano = achatar(aud.get("vereditos", {}) or {})
    out = {}
    for k, v in plano.items():
        if isinstance(v, dict) and v.get("veredito") == "corrige" and v.get("valor_corrigido") not in (None, ""):
            out[k.strip()] = str(v["valor_corrigido"])
    return out


def monta_fichas(regra):
    entrada = json.loads((D3 / "saidas" / "auditoria" / "fichas-entrada-S.json").read_text(encoding="utf-8"))
    fichas = {}
    log = []
    for tid in h3.TRIALS:
        fs = json.loads(json.dumps(entrada["fichas"][tid]))
        vs = {m: vereditos(m, tid) for m in MEMBROS}
        campos = set().union(*[set(v) for v in vs.values()])
        for campo in sorted(campos):
            c27, c14, c12 = vs["27B"].get(campo), vs["14B"].get(campo), vs["12B"].get(campo)
            aplica = None
            if regra == "OR":
                if c27 is not None or c14 is not None:
                    aplica = c27 if c27 is not None else c14
            elif regra == "MAJ":
                flags = [c for c in (c27, c14, c12) if c is not None]
                if len(flags) >= 2:
                    par = None
                    for i in range(len(flags)):
                        for j in range(i + 1, len(flags)):
                            if flags[i] == flags[j]:
                                par = flags[i]
                    aplica = par if par is not None else (c27 if c27 is not None else flags[0])
            if aplica is not None:
                try:
                    h3.poe(fs, campo, aplica)
                    log.append(f"{tid} {campo} -> {aplica[:24]} (27B={str(c27)[:12]} 14B={str(c14)[:12]} 12B={str(c12)[:12]})")
                except Exception:
                    pass
        fichas[h3.ROT[tid]] = fs
    return fichas, log


def roda_calc(regra, fichas):
    base = h3.prompt_txt("e3-calc.txt")
    prompt = base + json.dumps(fichas, ensure_ascii=False, indent=1)
    transcricao, chamadas, total_dt = [], 0, 0.0
    atual = prompt
    final_json = None
    for rodada in range(1, 7):
        r = h3.gerar("qwen38", atual, max_tokens=1800)
        total_dt += r["dt"]
        transcricao.append(dict(rodada=rodada, saida=r["content"], dt=round(r["dt"], 1)))
        calcs = [ln for ln in r["content"].splitlines() if re.match(r"\s*CALC:", ln, re.I)]
        final_json = h3.acha_json(r["content"])
        if final_json and isinstance(final_json.get("agregado"), dict):
            break
        respostas = []
        for ln in calcs[: 24 - chamadas]:
            res = h3.executa_calc(ln)
            if res:
                respostas.append(ln.strip() + "\n" + res)
                chamadas += 1
        if not respostas:
            break
        atual = atual + "\n\n[SUA RODADA ANTERIOR]\n" + r["content"] + \
            "\n\n[RESULTADOS DAS SUAS CHAMADAS]\n" + "\n".join(respostas) + \
            "\n\nContinue: use os RESULTADOS acima. Se precisar de mais cálculos, escreva novas linhas CALC:. " \
            "Quando tiver tudo, responda com o JSON final."
    (OUT / f"calc-{regra}.json").write_text(json.dumps(dict(
        modelo="qwen38", regra=regra, chamadas=chamadas, fechou=bool(final_json),
        dt=round(total_dt, 1), transcricao=transcricao, json_final=final_json),
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  calc {regra}: {chamadas} chamadas, fechou={bool(final_json)}, {total_dt:.0f}s", flush=True)
    return final_json


def roda_sintese(regra, fichas, calc_final):
    base = h3.prompt_txt("e3-sintese.txt")
    dados = ("\n## Fichas auditadas (comitê)\n" + json.dumps(fichas, ensure_ascii=False, indent=1) +
             "\n\n## Resultados da calculadora\n" + json.dumps(calc_final, ensure_ascii=False, indent=1))
    r = h3.gerar("gemma26", base + dados, max_tokens=900)
    (OUT / f"sintese-{regra}.json").write_text(json.dumps(dict(modelo="gemma26", regra=regra, **r),
                                                          ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  sintese {regra}: {r['dt']:.0f}s, {len(r['content'].split())} palavras", flush=True)


def main():
    OUT.mkdir(exist_ok=True)
    t0 = time.time()
    for regra in ("OR", "MAJ"):
        fichas, log = monta_fichas(regra)
        (OUT / f"fichas-{regra}.json").write_text(json.dumps(dict(regra=regra, aplicacoes=log, fichas=fichas),
                                                             ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"== regra {regra}: {len(log)} correções aplicadas", flush=True)
        for linha in log:
            print("   ", linha, flush=True)
        final = roda_calc(regra, fichas)
        roda_sintese(regra, fichas, final)
    print(f"\ncomitê completo em {(time.time()-t0)/60:.1f} min", flush=True)


if __name__ == "__main__":
    main()

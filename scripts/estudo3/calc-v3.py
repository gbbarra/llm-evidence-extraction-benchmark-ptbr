# -*- coding: utf-8 -*-
"""EXTRAI Study 3 — Harness v3: the hardened calculator loop (Amendment 6).

A separate module so the frozen v1/v2 harness that produced the registered
arms is never touched. Differences from the v2 loop, all mechanical (fixed
strings, mechanical triggers, no content hints):

  (1) mixed-round fix  — pending CALC calls are executed BEFORE any final
      JSON is accepted: the answer only wins in a round that wrote no new
      calls (the joint where the 12B and 14B casts died);
  (2) tool-avoidance net — a final answer produced with zero executed calls
      triggers ONE fixed reprompt to use the calculator (shifts the question
      from "does it use the tool spontaneously", already measured under v2,
      to "can it use the tool when held to it");
  (3) pool reconciliation — if any row of the model's pool_dl_md call is not
      among its own executed md() call argument tuples, ONE fixed reprompt
      asks it to reconcile (Study-3 finding 5 turned into a net);
  (4) the v2 nets are kept: forced closure and call-as-data-inside-JSON.

Frozen and unchanged: prompts, ctx 16384, the 24-executed-calls cap,
temperature, seals.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]

_spec = importlib.util.spec_from_file_location("h3", ROOT / "scripts" / "estudo3" / "e3-harness.py")
h3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h3)

AVISO_FERRAMENTA = ("\n\nUse a calculadora: escreva as chamadas CALC (uma por linha), "
                    "aguarde os RESULTADOS e só então emita o JSON final.")
AVISO_POOL = ("\n\nAs linhas da sua chamada pool_dl_md diferem dos argumentos das suas "
              "chamadas md por estudo. Reconcilie: refaça o pool usando exatamente os "
              "sextetos das suas chamadas md (ou corrija as chamadas md) e emita o JSON final.")
AVISO_CALC_DENTRO = ("\n\nSeu JSON contém chamadas CALC escritas como texto. Escreva as chamadas "
                     "CALC FORA do JSON, uma por linha, aguarde os RESULTADOS e só então emita "
                     "o JSON final apenas com números.")
AVISO_FECHAR = "\n\nEmita agora APENAS o JSON final, no formato pedido."
CONTINUE = ("\n\nContinue: use os RESULTADOS acima. Quando tiver tudo, responda com o "
            "JSON final apenas com números.")


def _tuplas_md(linhas_exec):
    out = []
    for ln in linhas_exec:
        m = re.match(r"CALC:\s*md\(([^)]*)\)", ln, re.I)
        if m:
            try:
                out.append(tuple(round(float(x), 3) for x in json.loads("[" + m.group(1) + "]")))
            except Exception:
                pass
    return out


def _pool_reconcilia(linhas_exec):
    """True if every pool row matches one of the model's own md() calls."""
    mds = _tuplas_md(linhas_exec)
    for ln in linhas_exec:
        m = re.match(r"CALC:\s*pool_dl_md\((.*)\)\s*$", ln, re.I | re.S)
        if not m:
            continue
        try:
            linhas = json.loads("[" + m.group(1) + "]")
            linhas = linhas[0] if len(linhas) == 1 and isinstance(linhas[0][0], list) else linhas
            for row in linhas:
                if tuple(round(float(x), 3) for x in row) not in mds:
                    return False
        except Exception:
            return False
    return True


def _calc_dentro(fj):
    return bool(fj) and "CALC:" in json.dumps(fj, ensure_ascii=False)


def calc_v3(modelo, fichas, out_path, rotulo=""):
    base = h3.prompt_txt("e3-calc.txt")
    atual = base + json.dumps(fichas, ensure_ascii=False, indent=1)
    transcricao, chamadas, total_dt = [], 0, 0.0
    linhas_exec = []
    final_json = None
    avisou_ferramenta = avisou_pool = False
    fechamentos = 0
    for rodada in range(1, 13):
        r = h3.gerar(modelo, atual, max_tokens=1800)
        total_dt += r["dt"]
        transcricao.append(dict(rodada=rodada, saida=r["content"], dt=round(r["dt"], 1)))
        calcs = [ln for ln in r["content"].splitlines() if re.match(r"\s*CALC:", ln, re.I)]
        if calcs and chamadas < 24:
            respostas = []
            for ln in calcs[: 24 - chamadas]:
                res = h3.executa_calc(ln)
                if res:
                    respostas.append(ln.strip() + "\n" + res)
                    chamadas += 1
                    linhas_exec.append(ln.strip())
            if respostas:
                atual = (atual + "\n\n[SUA RODADA ANTERIOR]\n" + r["content"] +
                         "\n\n[RESULTADOS DAS SUAS CHAMADAS]\n" + "\n".join(respostas) + CONTINUE)
                continue  # v3 rule (1): an answer never wins in a round that called
        final_json = h3.acha_json(r["content"])
        fechado = (bool(final_json) and isinstance(final_json.get("agregado"), dict))
        if fechado and _calc_dentro(final_json):
            atual = atual + AVISO_CALC_DENTRO
            fechamentos += 1
            if fechamentos > 3:
                break
            continue
        if fechado and chamadas == 0 and not avisou_ferramenta:
            avisou_ferramenta = True
            atual = atual + AVISO_FERRAMENTA
            continue
        if fechado and not avisou_pool and not _pool_reconcilia(linhas_exec):
            avisou_pool = True
            atual = atual + AVISO_POOL
            continue
        if fechado:
            break
        fechamentos += 1
        if fechamentos > 3:
            break
        atual = atual + AVISO_FECHAR
    registro_eco = dict(chamadas_executadas=linhas_exec,
                        pool_reconciliado=_pool_reconcilia(linhas_exec) if linhas_exec else None)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(dict(modelo=modelo, harness="v3", rotulo=rotulo,
                                        chamadas=chamadas, rodadas=len(transcricao),
                                        rede_ferramenta=avisou_ferramenta, rede_pool=avisou_pool,
                                        fechou=bool(final_json), dt=round(total_dt, 1),
                                        registro_eco=registro_eco, transcricao=transcricao,
                                        json_final=final_json), ensure_ascii=False, indent=1),
                        encoding="utf-8")
    return final_json


def main():
    """Amendment-6 calculator championship: 4 veterans x 2 lanes under v3,
    over the BASELINE audited sheets (identical inputs for every model)."""
    assert h3.ELENCO == "base", "championship reads the baseline audited sheets"
    OUT = ROOT / "dados" / "estudo3" / "saidas-campeonato"
    import time
    t0 = time.time()
    for modelo in ("gemma12", "qwen14", "gemma26", "qwen38"):
        for lane in ("L", "S"):
            out = OUT / f"calc-{modelo}-{lane}.json"
            if out.exists():
                print(f"  pulando {modelo}-{lane}", flush=True)
                continue
            fichas = {}
            for tid in h3.TRIALS:
                fs, _ = h3.ficha_auditada(tid, lane)
                fichas[h3.ROT[tid]] = fs
            fj = calc_v3(modelo, fichas, out, rotulo=f"campeonato-{lane}")
            ag = (fj or {}).get("agregado")
            print(f"  {modelo}-{lane}: agregado={json.dumps(ag, ensure_ascii=False) if ag else 'NAO FECHOU'}",
                  flush=True)
    print(f"campeonato completo em {(time.time()-t0)/60:.1f} min", flush=True)


if __name__ == "__main__":
    main()

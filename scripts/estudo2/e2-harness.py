# -*- coding: utf-8 -*-
"""EXTRAI — Estudo 2 "as contas": harness dos braços A (de cabeça) e B (calculadora).

Insumo por modelo: as SUAS extrações T1-r1 do E1, reduzidas por desfecho-família:
  rr   — morbidade, mortalidade e íleo (eventos e n por braço, por estudo)
  md   — tempo até flatus e até dieta oral (média±DP e n por braço)
  pool — agrupamento dos desfechos acima (MH/DL para RR; variância inversa p/ MD)

Braço A: uma corrida, sem ajuda; "NAO-CALCULAVEL" é resposta válida.
Braço B: até 5 rodadas; o modelo escreve linhas `CALC: funcao(args)`, o harness computa
e devolve `RESULTADO:` no contexto; a resposta final é JSON.

Correção de continuidade: célula zero em RR soma 0,5 a todas as células do estudo
(registrado no retorno). Funções e fórmulas documentadas no prompt do braço B.

Uso: python e2-harness.py run [--models ...] [--bracos A,B] [--reps 2] [--think]
Saídas: dados/estudo2/saidas/<modelo>/<familia>-<braco>-r<n>.json (com transcrição)
"""
import argparse
import json
import math
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
D1 = RAIZ / "dados" / "estudo1"
D2 = RAIZ / "dados" / "estudo2"
OLLAMA = "http://localhost:11434"
CTX = 8192
MODELS = {
    "gemma12": dict(ollama="gemma4:12b", cpu=False),
    "qwen14":  dict(ollama="qwen3:14b", cpu=False),
    "gemma26": dict(ollama="gemma4:26b", cpu=True),
    "qwen38":  dict(ollama="qwen3.8:27b-texto", cpu=True),
}
ROT = {"PMC10561433": "Yoon 2023", "PMC10694978": "Sun 2023", "PMC10912221": "Wu 2024",
       "PMC11061212": "Castro 2024", "PMC12565272": "Redondo 2025", "PMC4782303": "Schmid 2016",
       "PMC5589093": "Weinberg 2017", "PMC6907038": "Sujatha 2019", "REF26": "Diaper 2021",
       "REF29": "de Waal 2021", "REF30": "Arslan 2020", "REF33": "Calvo-Vecino 2018",
       "REF41": "Coeckelenbergh 2024", "REF47": "Hokenek 2022"}


# ---------------- funções da calculadora (verdade aritmética) ----------------
def _cont(a, n1, c, n2):
    if a == 0 or c == 0 or a == n1 or c == n2:
        return a + .5, n1 + 1, c + .5, n2 + 1, True
    return a, n1, c, n2, False


def rr(a, n1, c, n2):
    a, n1, c, n2, cc = _cont(a, n1, c, n2)
    return round((a / n1) / (c / n2), 3)


def ic95_rr(a, n1, c, n2):
    a, n1, c, n2, cc = _cont(a, n1, c, n2)
    r = (a / n1) / (c / n2)
    se = math.sqrt(1 / a - 1 / n1 + 1 / c - 1 / n2)
    return [round(math.exp(math.log(r) - 1.96 * se), 3), round(math.exp(math.log(r) + 1.96 * se), 3)]


def md(m1, dp1, n1, m2, dp2, n2):
    return round(m1 - m2, 2)


def ic95_md(m1, dp1, n1, m2, dp2, n2):
    se = math.sqrt(dp1 ** 2 / n1 + dp2 ** 2 / n2)
    d = m1 - m2
    return [round(d - 1.96 * se, 2), round(d + 1.96 * se, 2)]


def pool_rr_mh(estudos):
    R = S = P = 0.0
    for e in estudos:
        a, n1, c, n2, _ = _cont(*[float(x) for x in e])
        N = n1 + n2
        R += a * n2 / N
        S += c * n1 / N
        P += (n1 * n2 * (a + c) - a * c * N) / N ** 2
    r = R / S
    se = math.sqrt(P / (R * S))
    return dict(rr=round(r, 3), ic95=[round(math.exp(math.log(r) - 1.96 * se), 3),
                                      round(math.exp(math.log(r) + 1.96 * se), 3)])


def pool_dl(estudos):
    ys, vs = [], []
    for e in estudos:
        a, n1, c, n2, _ = _cont(*[float(x) for x in e])
        ys.append(math.log((a / n1) / (c / n2)))
        vs.append(1 / a - 1 / n1 + 1 / c - 1 / n2)
    w = [1 / v for v in vs]
    yf = sum(wi * yi for wi, yi in zip(w, ys)) / sum(w)
    q = sum(wi * (yi - yf) ** 2 for wi, yi in zip(w, ys))
    df = len(ys) - 1
    cdenom = sum(w) - sum(wi ** 2 for wi in w) / sum(w)
    tau2 = max(0.0, (q - df) / cdenom) if df > 0 and cdenom > 0 else 0.0
    ws = [1 / (v + tau2) for v in vs]
    yr = sum(wi * yi for wi, yi in zip(ws, ys)) / sum(ws)
    se = math.sqrt(1 / sum(ws))
    i2 = max(0.0, (q - df) / q) * 100 if q > 0 and df > 0 else 0.0
    return dict(rr=round(math.exp(yr), 3),
                ic95=[round(math.exp(yr - 1.96 * se), 3), round(math.exp(yr + 1.96 * se), 3)],
                tau2=round(tau2, 4), i2=round(i2, 1))


def pool_md_iv(estudos):
    ws, ds = [], []
    for e in estudos:
        m1, dp1, n1, m2, dp2, n2 = [float(x) for x in e]
        v = dp1 ** 2 / n1 + dp2 ** 2 / n2
        ws.append(1 / v)
        ds.append(m1 - m2)
    dsum = sum(wi * di for wi, di in zip(ws, ds)) / sum(ws)
    se = math.sqrt(1 / sum(ws))
    return dict(md=round(dsum, 2), ic95=[round(dsum - 1.96 * se, 2), round(dsum + 1.96 * se, 2)])


FUNCOES = dict(rr=rr, ic95_rr=ic95_rr, md=md, ic95_md=ic95_md,
               pool_rr_mh=pool_rr_mh, pool_dl=pool_dl, pool_md_iv=pool_md_iv)


def executa_calc(linha):
    m = re.match(r"\s*CALC:\s*([a-z0-9_]+)\s*\((.*)\)\s*$", linha.strip(), re.I)
    if not m:
        return None
    nome = m.group(1).lower()
    if nome not in FUNCOES:
        return f"RESULTADO: erro — função desconhecida '{nome}'"
    try:
        args = json.loads(f"[{m.group(2)}]")
        # listas de listas p/ pools; escalares p/ o resto
        if nome.startswith("pool"):
            res = FUNCOES[nome](args[0] if len(args) == 1 and isinstance(args[0][0], list) else args)
        else:
            res = FUNCOES[nome](*[float(x) for x in args])
        return f"RESULTADO: {json.dumps(res, ensure_ascii=False)}"
    except Exception as e:
        return f"RESULTADO: erro — {str(e)[:80]}"


# ---------------- insumos por modelo/família ----------------
CAMPOS_FAM = {
    "rr": [("morbidade", "morbidade_eventos_gdft", "morbidade_eventos_controle"),
           ("mortalidade", "mortalidade_gdft", "mortalidade_controle"),
           ("ileo", "ileo_pos_op_gdft", "ileo_pos_op_controle")],
    "md": [("tempo_flatus_h", "tempo_flatus_gdft", "tempo_flatus_controle"),
           ("tempo_dieta_oral", "tempo_ingesta_oral_gdft", "tempo_ingesta_oral_controle")],
}


def estudos_por_desfecho():
    gab = json.loads((D1 / "gabarito-ma.json").read_text(encoding="utf-8"))
    por = {"morbidade": [], "mortalidade": [], "ileo": [], "tempo_flatus_h": [], "tempo_dieta_oral": []}
    mapa_t = {5: "morbidade", 6: "mortalidade", 11: "ileo", 8: "tempo_flatus_h", 9: "tempo_dieta_oral"}
    for t in gab["tabelas"]:
        d = mapa_t.get(t["numero"])
        if not d:
            continue
        for l in t["linhas"]:
            if l.get("pmcid"):
                por[d].append(l["pmcid"])
    return por


def extracao(mod, pm):
    f = D1 / "saidas" / mod / f"{pm}-t1-r1.json"
    try:
        return json.loads(re.sub(r"^```(?:json)?\s*|\s*```$", "",
                                 json.loads(f.read_text(encoding="utf-8"))["content"].strip()))
    except Exception:
        f2 = D1 / "saidas" / mod / f"{pm}-t1-r2.json"
        return json.loads(re.sub(r"^```(?:json)?\s*|\s*```$", "",
                                 json.loads(f2.read_text(encoding="utf-8"))["content"].strip()))


def bloco_insumo(mod, familia):
    por = estudos_por_desfecho()
    linhas = []
    alvo = CAMPOS_FAM["rr"] + CAMPOS_FAM["md"] if familia == "pool" else CAMPOS_FAM[familia]
    for desfecho, c_g, c_c in alvo:
        linhas.append(f"\n## Desfecho: {desfecho}")
        for pm in por[desfecho]:
            j = extracao(mod, pm)
            vg = j.get(c_g, {}).get("valor", "NR")
            vc = j.get(c_c, {}).get("valor", "NR")
            ng = j.get("n_randomizados_gdft", {}).get("valor", "NR")
            nc = j.get("n_randomizados_controle", {}).get("valor", "NR")
            linhas.append(f"- {ROT[pm]}: GDFT eventos/valor = {vg} | controle = {vc} | n GDFT = {ng} | n controle = {nc}")
    return "\n".join(linhas)


def prompt_de(mod, familia, braco):
    tpl = (D2 / "prompts" / f"{familia}-{braco}.txt").read_text(encoding="utf-8")
    return tpl.replace("{DADOS}", bloco_insumo(mod, familia))


# ---------------- motor ----------------
def post_json(url, body, timeout=3600):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    r = json.load(urllib.request.urlopen(req, timeout=timeout))
    return r, time.time() - t0


def gerar(mod, prompt, think=False, max_tokens=1600):
    m = MODELS[mod]
    opts = dict(num_predict=max_tokens, num_ctx=CTX)
    if m["cpu"]:
        opts["num_gpu"] = 0
    body = dict(model=m["ollama"], prompt=prompt, stream=False, think=bool(think), options=opts)
    r, dt = post_json(OLLAMA + "/api/generate", body)
    if r.get("error"):
        raise RuntimeError(r["error"])
    return dict(content=r.get("response", "") or "", dt=r.get("total_duration", 0) / 1e9 or dt,
                tokens=r.get("eval_count", 0), prompt_tokens=r.get("prompt_eval_count", 0),
                finish=r.get("done_reason"))


def corrida(mod, familia, braco, rep, think=False):
    sufixo = "-think" if think else ""
    out = D2 / "saidas" / mod / f"{familia}-{braco}{sufixo}-r{rep}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        print(f"  pulando: {mod} {familia}-{braco}{sufixo}-r{rep}", flush=True)
        return
    base = prompt_de(mod, familia, braco)
    transcricao = []
    prompt = base
    total_dt = 0.0
    chamadas = 0
    for rodada in range(1, 6 if braco == "B" else 2):
        r = gerar(mod, prompt, think=think)
        total_dt += r["dt"]
        transcricao.append(dict(rodada=rodada, saida=r["content"], dt=round(r["dt"], 1)))
        if braco == "A":
            break
        calcs = [ln for ln in r["content"].splitlines() if re.match(r"\s*CALC:", ln, re.I)]
        if not calcs:
            break
        respostas = []
        for ln in calcs[:20 - chamadas]:
            res = executa_calc(ln)
            if res:
                respostas.append(ln.strip() + "\n" + res)
                chamadas += 1
        if not respostas or chamadas >= 20:
            break
        prompt = prompt + "\n\n[SUA RODADA ANTERIOR]\n" + r["content"] + \
            "\n\n[RESULTADOS DAS SUAS CHAMADAS]\n" + "\n".join(respostas) + \
            "\n\nContinue: use os RESULTADOS acima. Se precisar de mais cálculos, escreva novas linhas CALC:. " \
            "Quando tiver tudo, responda com o JSON final."
    out.write_text(json.dumps(dict(modelo=mod, familia=familia, braco=braco, replica=rep,
                                   think=think, chamadas=chamadas, dt=round(total_dt, 1),
                                   rodadas=len(transcricao), transcricao=transcricao),
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {mod} {familia}-{braco}{sufixo}-r{rep}: {len(transcricao)} rodada(s), "
          f"{chamadas} CALC, {total_dt:.0f}s", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run"])
    ap.add_argument("--models", default="gemma12,qwen14,gemma26,qwen38")
    ap.add_argument("--bracos", default="A,B")
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--think", action="store_true", help="braço exploratório (1 réplica, braço A)")
    a = ap.parse_args()
    t0 = time.time()
    for mod in [m.strip() for m in a.models.split(",")]:
        print(f"\n=== {mod} — {time.strftime('%H:%M')} ===", flush=True)
        for familia in ("rr", "md", "pool"):
            for braco in [b.strip() for b in a.bracos.split(",")]:
                for rep in range(1, a.reps + 1):
                    corrida(mod, familia, braco, rep)
        if a.think and mod in ("qwen14",):
            for familia in ("rr", "md", "pool"):
                corrida(mod, familia, "A", 1, think=True)
    print(f"\nFILA E2 CONCLUÍDA em {(time.time()-t0)/60:.0f} min.", flush=True)


if __name__ == "__main__":
    main()

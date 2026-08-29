# -*- coding: utf-8 -*-
"""EXTRAI Study 3 — pipeline harness (stages E/A/C/S; F is a separate script).

Usage: e3-harness.py [extracao|auditoria|calc|sintese|tudo]

Stage E  extraction   gemma4:12b (iGPU), 7 perturbed texts x 2 replicates
Stage A  audit        qwen3.8:27b (CPU), 2 lanes (L=clean, S=seeded) x 7 sheets
Stage C  arithmetic   qwen3.8:27b, CALC protocol + FORCED CLOSURE, per lane
Stage S  synthesis    gemma4:26b (CPU MoE), pooled numbers in context, per lane

Frozen configs (protocol §6): /api/generate, ctx 16384, think:false,
num_gpu:0 on CPU models, resume-safe (existing outputs are skipped),
first-parseable-replicate. New CALC functions (Amendment 1) are validated
against the anchor's forest before any run; both seals' SHA-256 go to stdout.
"""
import hashlib
import json
import math
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
D3 = ROOT / "dados" / "estudo3"
PERT = ROOT / "corpus" / "estudo3" / "perturbados"
# Harness v2 (Amendment 3): cast and output namespace selected by the
# E3_ELENCO env var so alternative-cast arms never touch the baseline record.
# Stage E is SHARED across casts (the extractor is gemma4:12b in every arm):
# extraction sheets are read from the baseline directory and reused verbatim,
# so alternative arms isolate the audit/arithmetic/synthesis cast with
# identical inputs and identical sealed seeds.
ELENCO = os.environ.get("E3_ELENCO", "base")
CAST = {"E": "gemma12", "A": "qwen38", "C": "qwen38", "S": "gemma26"}
if ELENCO == "allgemma":
    CAST = {"E": "gemma12", "A": "gemma12", "C": "gemma12", "S": "gemma12"}
SAIDAS = D3 / ("saidas" if ELENCO == "base" else f"saidas-{ELENCO}")
EXTRACAO = D3 / "saidas" / "extracao"
OLLAMA = "http://localhost:11434"
CTX = 16384
MODELS = {
    "gemma12": dict(ollama="gemma4:12b", cpu=False),
    "gemma26": dict(ollama="gemma4:26b", cpu=True),
    "qwen38":  dict(ollama="qwen3.8:27b-texto", cpu=True),
}
TRIALS = ["PMC5329646", "REF9", "PMC9606840", "PMC7535044", "REF12", "PMC6024764", "PMC5048014"]
ROT = {"PMC5329646": "Saslow 2017", "REF9": "Saslow 2023", "PMC9606840": "Dorans 2022",
       "PMC7535044": "Chen 2020", "REF12": "Thomsen 2022", "PMC6024764": "Wang 2018",
       "PMC5048014": "Goday 2016"}
LANES = ["L", "S"]


# ---------------- calculator (arithmetic truth) ----------------
def md(m1, dp1, n1, m2, dp2, n2):
    return round(m1 - m2, 2)


def ic95_md(m1, dp1, n1, m2, dp2, n2):
    se = math.sqrt(dp1 ** 2 / n1 + dp2 ** 2 / n2)
    d = m1 - m2
    return [round(d - 1.96 * se, 2), round(d + 1.96 * se, 2)]


def dp_de_ic(lo, hi, n):
    return round((hi - lo) / 2 / 1.96 * math.sqrt(n), 2)


def dp_de_se(se, n):
    return round(se * math.sqrt(n), 2)


def dp_mudanca_r05(dp1, dp2):
    return round(math.sqrt(dp1 ** 2 + dp2 ** 2 - 2 * 0.5 * dp1 * dp2), 2)


def pool_dl_md(estudos):
    ys, vs = [], []
    for e in estudos:
        m1, dp1, n1, m2, dp2, n2 = [float(x) for x in e]
        ys.append(m1 - m2)
        vs.append(dp1 ** 2 / n1 + dp2 ** 2 / n2)
    w = [1 / v for v in vs]
    yf = sum(wi * yi for wi, yi in zip(w, ys)) / sum(w)
    q = sum(wi * (yi - yf) ** 2 for wi, yi in zip(w, ys))
    df = len(ys) - 1
    cden = sum(w) - sum(wi ** 2 for wi in w) / sum(w)
    tau2 = max(0.0, (q - df) / cden) if df > 0 and cden > 0 else 0.0
    ws = [1 / (v + tau2) for v in vs]
    yr = sum(wi * yi for wi, yi in zip(ws, ys)) / sum(ws)
    se = math.sqrt(1 / sum(ws))
    i2 = max(0.0, (q - df) / q) * 100 if q > 0 and df > 0 else 0.0
    return dict(md=round(yr, 2), ic95=[round(yr - 1.96 * se, 2), round(yr + 1.96 * se, 2)],
                tau2=round(tau2, 4), i2_pct=round(i2, 1))


FUNCOES = dict(md=md, ic95_md=ic95_md, dp_de_ic=dp_de_ic, dp_de_se=dp_de_se,
               dp_mudanca_r05=dp_mudanca_r05, pool_dl_md=pool_dl_md)


def executa_calc(linha):
    m = re.match(r"\s*CALC:\s*([a-z0-9_]+)\s*\((.*)\)\s*$", linha.strip(), re.I)
    if not m:
        return None
    nome = m.group(1).lower()
    if nome not in FUNCOES:
        return f"RESULTADO: erro — função desconhecida '{nome}'"
    try:
        args = json.loads(f"[{m.group(2)}]")
        if nome == "pool_dl_md":
            res = FUNCOES[nome](args[0] if len(args) == 1 and isinstance(args[0][0], list) else args)
        else:
            res = FUNCOES[nome](*[float(x) for x in args])
        return f"RESULTADO: {json.dumps(res, ensure_ascii=False)}"
    except Exception as e:
        return f"RESULTADO: erro — {str(e)[:80]}"


def valida_funcoes():
    """Amendment-1 gate: the new functions must reproduce the anchor before any run."""
    meta = json.loads((ROOT / "corpus" / "estudo3" / "ma" / "ma-lowcarb-meta.json").read_text(encoding="utf-8"))
    checks = [
        ("dp_de_ic Saslow17", dp_de_ic(-1.1, -0.6, 12), 0.44, 0.011),
        ("dp_de_se Saslow23", dp_de_se(0.07, 45), 0.47, 0.011),
        ("dp_mudanca_r05 Goday", dp_mudanca_r05(1.1, 0.7), 0.96, 0.011),
    ]
    sext = [[e["exp_media"], e["exp_dp"], e["exp_n"], e["ctl_media"], e["ctl_dp"], e["ctl_n"]]
            for e in meta["forest_hba1c"]]
    pool = pool_dl_md(sext)
    checks += [
        ("pool MD", pool["md"], -0.24, 0.006),
        ("pool IC inf", pool["ic95"][0], -0.31, 0.016),
        ("pool IC sup", pool["ic95"][1], -0.17, 0.016),
    ]
    ok = True
    for nome, v, alvo, tol in checks:
        bate = abs(v - alvo) <= tol
        ok &= bate
        print(f"  valida {nome}: {v} vs {alvo} {'OK' if bate else 'FALHOU'}", flush=True)
    print(f"  valida pool i2: {pool['i2_pct']}% (publicado 6%)", flush=True)
    if not ok:
        raise SystemExit("validação das funções falhou — fila abortada")


# ---------------- engine ----------------
def post_json(url, body, timeout=7200):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    r = json.load(urllib.request.urlopen(req, timeout=timeout))
    return r, time.time() - t0


def gerar(mod, prompt, max_tokens):
    m = MODELS[mod]
    opts = dict(num_predict=max_tokens, num_ctx=CTX)
    if m["cpu"]:
        opts["num_gpu"] = 0
    body = dict(model=m["ollama"], prompt=prompt, stream=False, think=False, options=opts)
    r, dt = post_json(OLLAMA + "/api/generate", body)
    if r.get("error"):
        raise RuntimeError(r["error"])
    return dict(content=r.get("response", "") or "",
                dt=r.get("total_duration", 0) / 1e9 or dt,
                tokens=r.get("eval_count", 0), prompt_tokens=r.get("prompt_eval_count", 0),
                finish=r.get("done_reason"))


def acha_json(texto):
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", texto.strip())
    try:
        return json.loads(t)
    except Exception:
        m = re.search(r"\{.*\}", t, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
    return None


def prompt_txt(nome):
    return (D3 / "prompts" / nome).read_text(encoding="utf-8")


# ---------------- stage E: extraction ----------------
def etapa_extracao():
    base = prompt_txt("e3-extracao.txt")
    for tid in TRIALS:
        for rep in (1, 2):
            out = EXTRACAO / f"{tid}-r{rep}.json"
            out.parent.mkdir(parents=True, exist_ok=True)
            if out.exists():
                print(f"  pulando extracao {tid}-r{rep}", flush=True)
                continue
            texto = (PERT / f"{tid}.txt").read_text(encoding="utf-8")
            r = gerar(CAST["E"], base + texto, max_tokens=2000)
            out.write_text(json.dumps(dict(modelo="gemma12", trial=tid, replica=rep, **r),
                                      ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  extracao {tid}-r{rep}: {r['dt']:.0f}s, {r['tokens']} tok", flush=True)


def ficha(tid):
    """First parseable replicate (E1 rule)."""
    for rep in (1, 2):
        f = EXTRACAO / f"{tid}-r{rep}.json"
        if not f.exists():
            continue
        j = acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
        if j:
            return j, rep
    raise RuntimeError(f"nenhuma réplica parseável para {tid}")


# ---------------- seeds (lane S) ----------------
def pega(d, caminho):
    cur = d
    for p in caminho.split("."):
        cur = cur[p]
    return cur


def poe(d, caminho, valor):
    partes = caminho.split(".")
    cur = d
    for p in partes[:-1]:
        cur = cur[p]
    cur[partes[-1]] = valor


def aplica_semente(fs, sem):
    c, campo = sem["classe"], sem["campo"]
    if c == "troca-de-braco":
        a = pega(fs, f"braco_experimental.{campo}")
        b = pega(fs, f"braco_controle.{campo}")
        poe(fs, f"braco_experimental.{campo}", b)
        poe(fs, f"braco_controle.{campo}", a)
        return f"{campo}: exp<->ctl ({a} <-> {b})"
    v = str(pega(fs, campo))
    if c == "sinal":
        novo = v[1:] if v.startswith("-") else "-" + v
    elif c == "digito":
        alvo = v
        m = re.search(r"-?\d+(?:\.\d+)?", v)  # first number (IC lower bound if IC string)
        num = m.group(0)
        d = num[-1]
        nd = str((int(d) + 4) % 10)
        if nd == d:
            nd = str((int(d) + 5) % 10)
        novo = alvo.replace(num, num[:-1] + nd, 1)
    elif c == "n-trocado":
        num = re.search(r"\d+", v).group(0)
        if len(num) >= 2 and num[-1] != num[-2]:
            novo_num = num[:-2] + num[-1] + num[-2]
        else:
            novo_num = str(int(num) + 9)
        novo = v.replace(num, novo_num, 1)
    else:
        raise ValueError(c)
    poe(fs, campo, novo)
    return f"{campo}: {v} -> {novo}"


def fichas_da_lane(lane):
    sementes = json.loads((D3 / "sementes-auditoria.json").read_text(encoding="utf-8"))
    fichas = {}
    log = []
    for tid in TRIALS:
        f, rep = ficha(tid)
        f = json.loads(json.dumps(f))  # deep copy
        if lane == "S":
            for sem in sementes["sementes"]:
                if sem["estudo"] == tid:
                    log.append(f"{tid} semente#{sem['id']} {sem['classe']}: " + aplica_semente(f, sem))
        fichas[tid] = f
    return fichas, log


# ---------------- stage A: audit ----------------
def etapa_auditoria():
    base = prompt_txt("e3-auditoria.txt")
    for lane in LANES:
        fichas, log = fichas_da_lane(lane)
        reg = SAIDAS / "auditoria" / f"fichas-entrada-{lane}.json"
        reg.parent.mkdir(parents=True, exist_ok=True)
        reg.write_text(json.dumps(dict(lane=lane, sementes_aplicadas=log, fichas=fichas),
                                  ensure_ascii=False, indent=1), encoding="utf-8")
        for tid in TRIALS:
            out = SAIDAS / "auditoria" / f"{tid}-{lane}.json"
            if out.exists():
                print(f"  pulando auditoria {tid}-{lane}", flush=True)
                continue
            texto = (PERT / f"{tid}.txt").read_text(encoding="utf-8")
            prompt = base.replace("{FICHA}", json.dumps(fichas[tid], ensure_ascii=False, indent=1)) + texto
            r = gerar(CAST["A"], prompt, max_tokens=2800)
            out.write_text(json.dumps(dict(modelo="qwen38", trial=tid, lane=lane, **r),
                                      ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  auditoria {tid}-{lane}: {r['dt']:.0f}s", flush=True)


def ficha_auditada(tid, lane):
    """Apply the auditor's 'corrige' verdicts over the lane's input sheet."""
    entrada = json.loads((SAIDAS / "auditoria" / f"fichas-entrada-{lane}.json").read_text(encoding="utf-8"))
    fs = json.loads(json.dumps(entrada["fichas"][tid]))
    aud = acha_json(json.loads((SAIDAS / "auditoria" / f"{tid}-{lane}.json").read_text(encoding="utf-8"))["content"])
    aplicadas = []
    if aud and isinstance(aud.get("vereditos"), dict):
        for caminho, v in aud["vereditos"].items():
            if isinstance(v, dict) and v.get("veredito") == "corrige" and "valor_corrigido" in v:
                try:
                    poe(fs, caminho, v["valor_corrigido"])
                    aplicadas.append(caminho)
                except Exception:
                    pass
    return fs, aplicadas


# ---------------- stage C: arithmetic with forced closure ----------------
def etapa_calc():
    base = prompt_txt("e3-calc.txt")
    for lane in LANES:
        out = SAIDAS / "calc" / f"calc-{lane}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            print(f"  pulando calc {lane}", flush=True)
            continue
        fichas = {}
        for tid in TRIALS:
            fs, _ = ficha_auditada(tid, lane)
            fichas[ROT[tid]] = fs
        prompt = base + json.dumps(fichas, ensure_ascii=False, indent=1)
        transcricao, chamadas, total_dt = [], 0, 0.0
        atual = prompt
        final_json = None
        for rodada in range(1, 7):
            r = gerar(CAST["C"], atual, max_tokens=1800)
            total_dt += r["dt"]
            transcricao.append(dict(rodada=rodada, saida=r["content"], dt=round(r["dt"], 1)))
            calcs = [ln for ln in r["content"].splitlines() if re.match(r"\s*CALC:", ln, re.I)]
            final_json = acha_json(r["content"])
            if final_json and isinstance(final_json.get("agregado"), dict):
                break
            respostas = []
            for ln in calcs[: 24 - chamadas]:
                res = executa_calc(ln)
                if res:
                    respostas.append(ln.strip() + "\n" + res)
                    chamadas += 1
            if not respostas:
                break
            atual = atual + "\n\n[SUA RODADA ANTERIOR]\n" + r["content"] + \
                "\n\n[RESULTADOS DAS SUAS CHAMADAS]\n" + "\n".join(respostas) + \
                "\n\nContinue: use os RESULTADOS acima. Se precisar de mais cálculos, escreva novas linhas CALC:. " \
                "Quando tiver tudo, responda com o JSON final."
        # Closure net v2 (Amendment 3): besides "no final JSON", the known
        # call-as-data mode (CALC: strings INSIDE the final JSON, the gemma
        # failure documented in Study 2) also counts as not-closed. Fixed
        # strings, mechanical triggers, zero content hints; provably inert on
        # the baseline cast (the qwen closed clean, never meeting either
        # trigger).
        def _calc_dentro(fj):
            return bool(fj) and "CALC:" in json.dumps(fj, ensure_ascii=False)

        fechamentos = 0
        while (not final_json or not isinstance(final_json.get("agregado"), dict)
               or _calc_dentro(final_json)) and fechamentos < 3:
            fechamentos += 1
            if _calc_dentro(final_json):
                instrucao = ("\n\nSeu JSON contém chamadas CALC escritas como texto. Escreva as "
                             "chamadas CALC FORA do JSON, uma por linha, aguarde os RESULTADOS e "
                             "só então emita o JSON final apenas com números.")
            else:
                instrucao = "\n\nEmita agora APENAS o JSON final, no formato pedido, sem novas chamadas."
            atual = atual + instrucao
            r = gerar(CAST["C"], atual, max_tokens=1600)
            total_dt += r["dt"]
            transcricao.append(dict(rodada=f"fechamento-{fechamentos}", saida=r["content"], dt=round(r["dt"], 1)))
            calcs = [ln for ln in r["content"].splitlines() if re.match(r"\s*CALC:", ln, re.I)]
            respostas = []
            for ln in calcs[: 24 - chamadas]:
                res = executa_calc(ln)
                if res:
                    respostas.append(ln.strip() + "\n" + res)
                    chamadas += 1
            if respostas:
                atual = (atual + "\n\n[SUA RODADA ANTERIOR]\n" + r["content"] +
                         "\n\n[RESULTADOS DAS SUAS CHAMADAS]\n" + "\n".join(respostas) +
                         "\n\nAgora emita o JSON final apenas com números.")
            final_json = acha_json(r["content"])
        # Pool-input echo, LOG-ONLY (Amendment 3): raw record of the per-study
        # md() call arguments vs the pool call rows, compared mechanically at
        # grading time. No intervention.
        texto_completo = "\n".join(str(x.get("saida", "")) for x in transcricao)
        registro_eco = dict(
            chamadas_md=re.findall(r"CALC:\s*md\(([^)]*)\)", texto_completo),
            chamadas_pool=re.findall(r"CALC:\s*pool_dl_md\((.*?)\)\s*$", texto_completo, re.M),
        )
        out.write_text(json.dumps(dict(modelo=CAST["C"], lane=lane, chamadas=chamadas,
                                       fechamentos_forcados=fechamentos, fechou=bool(final_json),
                                       dt=round(total_dt, 1), registro_eco=registro_eco,
                                       transcricao=transcricao,
                                       json_final=final_json), ensure_ascii=False, indent=1),
                       encoding="utf-8")
        print(f"  calc {lane}: {chamadas} chamadas, {fechamentos} fechamentos forçados, "
              f"fechou={bool(final_json)}, {total_dt:.0f}s", flush=True)


# ---------------- stage S: synthesis ----------------
def etapa_sintese():
    base = prompt_txt("e3-sintese.txt")
    for lane in LANES:
        out = SAIDAS / "sintese" / f"sintese-{lane}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            print(f"  pulando sintese {lane}", flush=True)
            continue
        calc = json.loads((SAIDAS / "calc" / f"calc-{lane}.json").read_text(encoding="utf-8"))
        fichas = {}
        for tid in TRIALS:
            fs, _ = ficha_auditada(tid, lane)
            fichas[ROT[tid]] = fs
        dados = ("\n## Fichas auditadas\n" + json.dumps(fichas, ensure_ascii=False, indent=1) +
                 "\n\n## Resultados da calculadora\n" + json.dumps(calc.get("json_final"), ensure_ascii=False, indent=1))
        r = gerar(CAST["S"], base + dados, max_tokens=900)
        out.write_text(json.dumps(dict(modelo=CAST["S"], lane=lane, **r),
                                  ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  sintese {lane}: {r['dt']:.0f}s, {len(r['content'].split())} palavras", flush=True)


def main():
    alvo = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    print(f"ELENCO: {ELENCO} · CAST: {CAST} · SAIDAS: {SAIDAS.name}", flush=True)
    for selo in ("perturbacoes-estudo3.json", "sementes-auditoria.json"):
        h = hashlib.sha256((D3 / selo).read_bytes()).hexdigest()
        print(f"SHA-256 {selo}: {h}", flush=True)
    print("validação das funções (Emenda 1):", flush=True)
    valida_funcoes()
    t0 = time.time()
    if alvo in ("extracao", "tudo"):
        print("\n== Etapa E: extração (gemma12, 14 corridas)", flush=True)
        etapa_extracao()
    if alvo in ("auditoria", "tudo"):
        print("\n== Etapa A: auditoria (qwen38, 14 corridas)", flush=True)
        etapa_auditoria()
    if alvo in ("calc", "tudo"):
        print("\n== Etapa C: aritmética (qwen38, 2 lanes)", flush=True)
        etapa_calc()
    if alvo in ("sintese", "tudo"):
        print("\n== Etapa S: síntese (gemma26, 2 lanes)", flush=True)
        etapa_sintese()
    print(f"\nfila '{alvo}' completa em {(time.time()-t0)/60:.1f} min", flush=True)


if __name__ == "__main__":
    main()

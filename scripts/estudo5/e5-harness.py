# -*- coding: utf-8 -*-
"""EXTRAI Study 5 — GEMMA-SÓ: the minimal-harness frontier (rungs G1/G2).

gemma4:12b orchestrates the calculator over ITS OWN round-2 sheets; the
harness nets DETECT and WARN, never substitute (protocol §1). G1 = free-text
CALC + sign-echo net. G2 = schema-constrained JSON calls with declared
per-argument source fields + the same detection-only net.

Run: python scripts/estudo5/e5-harness.py G1|G2
Outputs: dados/estudo5/saidas/<rung>/<estudo>.json · dados/estudo5/resultados-<rung>.json
"""
import importlib.util
import json
import os
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
D5 = ROOT / "dados" / "estudo5"
R2 = ROOT / "dados" / "estudo4" / "rodada2"
# Amendment 7: the orchestrator under test is selectable (extraction stays gemma12's)
MODELO = os.environ.get("E5_MODELO", "gemma12")
MAX_TURNOS = 16
MAX_AVISOS_POR_CHAMADA = 2

SCHEMA_G2 = {
    "type": "object",
    "properties": {
        "funcao": {"type": "string",
                   "enum": ["md", "ic95_md", "dp_de_ic", "dp_de_se", "dp_mudanca_r05", "fim"]},
        "argumentos": {"type": "array", "items": {"type": "number"}, "minItems": 1, "maxItems": 6},
        "fonte": {"type": "array", "items": {"type": "string"}, "maxItems": 6},
    },
    "required": ["funcao", "argumentos"],
}


SCHEMA_CALC2 = {
    "type": "object",
    "properties": {
        "funcao": {"type": "string",
                   "enum": ["md", "ic95_md", "dp_de_ic", "dp_de_se", "dp_mudanca_r05", "fim"]},
        "argumentos": {"type": "array", "items": {"type": "number"}, "minItems": 1, "maxItems": 6},
        "fonte": {"type": "array", "items": {"type": "string"}, "maxItems": 6},
        "derivacao": {"type": "string", "maxLength": 80},
    },
    "required": ["funcao", "argumentos"],
}

SCHEMA_G3 = {
    "type": "object",
    "properties": {
        "funcao": {"type": "string", "enum": ["pool_dl_md", "fim"]},
        "sextetos": {"type": "array",
                     "items": {"type": "array", "items": {"type": "number"},
                               "minItems": 6, "maxItems": 6}},
        "argumentos": {"type": "array", "items": {"type": "number"}},
    },
    "required": ["funcao"],
}


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


h3 = carrega("h3", "scripts/estudo3/e3-harness.py")
if MODELO == "codegemma":
    h3.MODELS["codegemma"] = dict(ollama="codegemma:latest", cpu=False)
FUNCOES = {k: v for k, v in h3.FUNCOES.items() if k != "pool_dl_md"}


def gerar_schema(prompt, max_tokens, schema=None):
    body = dict(model=h3.MODELS[MODELO]["ollama"], prompt=prompt, stream=False, think=False,
                format=schema or SCHEMA_G2, options=dict(num_predict=max_tokens, num_ctx=h3.CTX))
    r, dt = h3.post_json(h3.OLLAMA + "/api/generate", body)
    if r.get("error"):
        raise RuntimeError(r["error"])
    return dict(content=r.get("response", "") or "", dt=r.get("total_duration", 0) / 1e9 or dt)


def ficha_r2(tid, pasta=None):
    base = Path(pasta) if pasta else R2 / "saidas" / MODELO / "extracao"
    for rep in (1, 2):
        f = base / f"{tid}-r{rep}.json"
        if f.exists():
            js = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
            if js:
                return js
    return None


def numeros_da_ficha(ficha):
    """Every number readable in the sheet, with its field path and sign."""
    nums = []

    def anda(d, trilha):
        if isinstance(d, dict):
            for k, v in d.items():
                anda(v, f"{trilha}.{k}" if trilha else k)
        else:
            s = str(d).replace("−", "-").replace("–", "-")
            for m in re.finditer(r"-?\d+(?:\.\d+)?", s):
                nums.append((trilha, float(m.group(0))))
    anda(ficha, "")
    return nums


def aviso_sinal(args, nums):
    """Detection only: an argument whose magnitude exists in the sheet with the
    opposite sign, while no sheet number equals it as emitted."""
    for a in args:
        if a == 0:
            continue
        if any(abs(v - a) <= 0.005 for _, v in nums):
            continue
        opostos = [c for c, v in nums if abs(abs(v) - abs(a)) <= 0.005 and (v > 0) != (a > 0)]
        if opostos:
            return (f"AVISO: o argumento {a} tem a mesma magnitude do campo '{opostos[0]}' "
                    f"da ficha, mas com o SINAL oposto — e nenhum número da ficha vale {a}. "
                    "Confira e reemita a chamada (corrigida, ou idêntica se você confirma).")
    return None


def aviso_fonte(args, fontes, ficha):
    """G2 detection net, arm-agnostic (Amendment 1 / E5-1): silent if the
    argument matches the declared field in ANY arm; fires only when it matches
    none, listing every candidate."""
    for a, f in zip(args, fontes or []):
        fl = str(f).strip().lower()
        if fl in ("derivado", "resultado-anterior", "resultado anterior", ""):
            continue
        candidatos = [(t, v) for t, v in numeros_da_ficha(ficha)
                      if t.lower().endswith(fl) or fl in t.lower()]
        if candidatos and not any(abs(v - a) <= 0.005 for _, v in candidatos):
            lista = "; ".join(f"'{t}' = {v}" for t, v in candidatos[:3])
            return (f"AVISO: o argumento {a} declara vir de '{f}', mas a ficha registra: "
                    f"{lista}. Confira e reemita a chamada "
                    "(corrigida, ou idêntica se você confirma).")
    return None


def aviso_derivacao(args, fontes, js, nums):
    """Amendment 4 / roadmap #3, detection-only: a 'derivado' argument must come
    with a declared operation whose operands are sheet values and whose result
    is the argument sent."""
    fl = [str(f).strip().lower() for f in (fontes or [])]
    if "derivado" not in fl:
        return None
    d = str(js.get("derivacao", "")).strip().replace("−", "-")
    if not d:
        return ('AVISO: um argumento declara fonte "derivado" — inclua o campo "derivacao" '
                'com a operação e os operandos, por exemplo "7.1 - 6.8". Reemita a chamada completa.')
    for x in re.findall(r"-?\d+(?:\.\d+)?", d):
        if not any(abs(float(x) - v) <= 0.005 for _, v in nums):
            return (f"AVISO: a derivação '{d}' usa {x}, que não é um valor da ficha. "
                    "Confira e reemita (corrigida, ou idêntica se você confirma).")
    m2 = re.match(r"\s*(-?\d+(?:\.\d+)?)\s*([-+])\s*(-?\d+(?:\.\d+)?)\s*$", d)
    if m2:
        a, op, b = float(m2.group(1)), m2.group(2), float(m2.group(3))
        val = a - b if op == "-" else a + b
        idx = fl.index("derivado")
        if idx < len(args) and abs(args[idx] - val) > 0.01:
            return (f"AVISO: a derivação '{d}' resulta em {round(val, 2)}, mas o argumento "
                    f"enviado é {args[idx]}. Confira e reemita (corrigida, ou idêntica se confirma).")
    return None


# --- Amendment 5 (G2c): argument type system + coherence, detection-only ---
# Slot classes: M mean-change · D dispersion/SD · N group size · I CI bound · E std. error
SLOTS = {"md": "MDNMDN", "ic95_md": "MDNMDN", "dp_de_ic": "IIN", "dp_de_se": "EN",
         "dp_mudanca_r05": "DD"}
CLASSE_OK = {
    "M": ("mudanca_media", "derivado"),
    "D": ("dispersao", "_dp", "derivado", "resultado-anterior", "resultado anterior"),
    "N": ("n_randomizado", "n_analisado"),
    "I": ("dispersao", "tipo_dispersao"),
    "E": ("dispersao",),
}
CLASSE_NOME = {"M": "média de MUDANÇA (mudanca_media ou derivação declarada)",
               "D": "dispersão/DP (dispersao, _dp, derivação ou resultado de dp_*)",
               "N": "tamanho de grupo (n_randomizado/n_analisado)",
               "I": "limite de IC (campo de dispersao)",
               "E": "erro-padrão (campo de dispersao)"}


def aviso_tipos(fn, args, fontes):
    """G2c type net: a declared source of the wrong class for its slot; plus
    per-class value impossibilities (negative SD; non-integer or tiny n)."""
    slots = SLOTS.get(fn, "")
    for i, (a, cls) in enumerate(zip(args, slots)):
        f = str(fontes[i]).strip().lower() if fontes and i < len(fontes) else ""
        if cls == "D" and a < 0:
            return (f"AVISO: o argumento {a} (slot {i+1} de {fn}, classe DP) é NEGATIVO — "
                    "um desvio-padrão é sempre positivo. Confira e reemita.")
        if cls == "N" and (a <= 1 or abs(a - round(a)) > 0.001):
            return (f"AVISO: o argumento {a} (slot {i+1} de {fn}, classe n) não é um tamanho "
                    "de grupo válido (inteiro > 1). Confira e reemita.")
        if f and not any(t in f for t in CLASSE_OK.get(cls, ())):
            return (f"AVISO: o slot {i+1} de {fn} pede {CLASSE_NOME[cls]}, mas recebeu a fonte "
                    f"'{fontes[i]}' com o valor {a}. Um nível (basal/final) não é uma mudança, "
                    "e um resultado de md não é uma média de braço. Confira e reemita "
                    "(corrigida, ou idêntica se você confirma).")
    return None


def aviso_ordem_ic(fn, args):
    """Amendment 6 micro-net: dp_de_ic bounds must come as (inferior, superior)."""
    if fn == "dp_de_ic" and len(args) >= 2 and args[0] > args[1]:
        return (f"AVISO: em dp_de_ic o primeiro argumento é o limite INFERIOR e o segundo o "
                f"SUPERIOR — você enviou ({args[0]}, {args[1]}), em ordem invertida. "
                "Confira os sinais e reemita.")
    return None


def aviso_coerencia_ic(fn, args, ultimo_md):
    """G2c coherence net: ic95_md's implied difference must match the study's
    own last executed md result."""
    if fn == "ic95_md" and ultimo_md is not None and len(args) >= 4:
        d = round(args[0] - args[3], 2)
        if abs(d - ultimo_md) > 0.01:
            return (f"AVISO: os argumentos deste ic95_md implicam diferença m1−m2 = {d}, "
                    f"mas o MD deste estudo (seu último resultado de md) é {ultimo_md}. "
                    "Os dois devem usar o MESMO sexteto. Confira e reemita.")
    return None


ARIDADE = {"md": (6, "md(m1, dp1, n1, m2, dp2, n2)"),
           "ic95_md": (6, "ic95_md(m1, dp1, n1, m2, dp2, n2)"),
           "dp_de_ic": (3, "dp_de_ic(inferior, superior, n)"),
           "dp_de_se": (2, "dp_de_se(ep, n)"),
           "dp_mudanca_r05": (2, "dp_mudanca_r05(dp_basal, dp_final)")}


def aviso_aridade(fn, args):
    """Amendment 1 / E5-2: arity pre-check with the full Portuguese signature."""
    if fn in ARIDADE and len(args) != ARIDADE[fn][0]:
        n, ass = ARIDADE[fn]
        return (f"AVISO: a função {fn} exige {n} argumentos — {ass} — e você enviou "
                f"{len(args)}. Reemita a chamada completa.")
    return None


def parse_g1(linha):
    m = re.match(r"\s*CALC:\s*([a-z0-9_]+)\s*\((.*)\)\s*$", linha.strip(), re.I)
    if not m:
        return None
    try:
        args = [float(x) for x in json.loads(f"[{m.group(2)}]")]
    except Exception:
        return None
    return m.group(1).lower(), args, None


def roda_estudo(rung, tid, base, pasta_fichas=None):
    rot = h3.ROT[tid]
    ficha = ficha_r2(tid, pasta_fichas)
    nums = numeros_da_ficha(ficha)
    prompt0 = base.replace("{FICHA}", json.dumps(ficha, ensure_ascii=False, indent=1))
    historico = ""
    turnos = []
    avisados = {}
    final = None
    for _ in range(MAX_TURNOS):
        if rung == "G1":
            r = h3.gerar(MODELO, prompt0 + historico + "\nPróxima linha:", max_tokens=80)
            bruto = next((l for l in r["content"].splitlines() if l.strip()), "").strip()
            if re.fullmatch(r"FIM\.?", bruto, re.I):
                turnos.append(dict(emitiu=bruto))
                break
            parsed = parse_g1(bruto)
        else:
            r = gerar_schema(prompt0 + historico + "\nPróximo JSON:", max_tokens=160,
                             schema=SCHEMA_CALC2 if rung.startswith("CALC") else SCHEMA_G2)
            bruto = r["content"].strip()
            try:
                js = json.loads(bruto)
                fn = js.get("funcao", "")
                if fn == "fim":
                    a = js.get("argumentos", [])
                    if (rung == "CALC2C" or rung.startswith("CALC3")) and len(a) >= 3 and not avisados.get("_fim_avisado"):
                        difere = []
                        if avisados.get("_ultimo_md") is not None and abs(a[0] - avisados["_ultimo_md"]) > 0.005:
                            difere.append(f"md {a[0]} ≠ resultado executado {avisados['_ultimo_md']}")
                        ic_exec = avisados.get("_ultimo_ic")
                        if ic_exec and (abs(a[1] - ic_exec[0]) > 0.005 or abs(a[2] - ic_exec[1]) > 0.005):
                            difere.append(f"ic95 [{a[1]}, {a[2]}] ≠ resultado executado {ic_exec}")
                        if difere:
                            avisados["_fim_avisado"] = True
                            aviso_f = ("AVISO: seu fim difere dos seus próprios resultados executados: "
                                       + "; ".join(difere) + ". Reemita o fim com os resultados executados, "
                                       "ou idêntico se você confirma.")
                            historico += f"{bruto}\n{aviso_f}\n"
                            turnos.append(dict(emitiu=bruto, aviso=aviso_f))
                            print(f"    MODELO : {bruto[:100]}", flush=True)
                            print(f"    HARNESS: {aviso_f[:110]}", flush=True)
                            continue
                    final = dict(md=a[0], ic95=[a[1], a[2]]) if len(a) >= 3 else None
                    if (rung == "CALC2C" or rung.startswith("CALC3")) and avisados.get("_fim_avisado") and final:
                        final["requer_revisao_humana"] = True
                    turnos.append(dict(emitiu=bruto))
                    break
                parsed = (fn, [float(x) for x in js.get("argumentos", [])], js.get("fonte"))
            except Exception:
                parsed = None
        if not parsed:
            historico += f"{bruto}\nAVISO: formato inválido — emita exatamente uma chamada no formato pedido.\n"
            turnos.append(dict(emitiu=bruto, aviso="formato"))
            continue
        fn, args, fontes = parsed
        chave = f"{fn}{args}"
        aviso = aviso_aridade(fn, args)
        if not aviso and avisados.get(chave, 0) < MAX_AVISOS_POR_CHAMADA and chave not in avisados.get("_conf", []):
            aviso = aviso_sinal(args, nums) or \
                (aviso_fonte(args, fontes, ficha) if rung.startswith("G2") or rung.startswith("CALC") else None) or \
                (aviso_derivacao(args, fontes, js, nums) if rung.startswith("CALC") else None) or \
                (aviso_tipos(fn, args, fontes) if rung == "CALC2C" or rung.startswith("CALC3") else None) or \
                (aviso_ordem_ic(fn, args) if rung.startswith("CALC3") else None) or \
                (aviso_coerencia_ic(fn, args, avisados.get("_ultimo_md")) if rung == "CALC2C" or rung.startswith("CALC3") else None)
        if aviso and (rung == "CALC2C" or rung.startswith("CALC3")) and avisados.get(chave, 0) >= MAX_AVISOS_POR_CHAMADA:
            avisados["_insistiu"] = True
        if aviso and avisados.get("_ultimo") == chave:
            avisados.setdefault("_conf", []).append(chave)   # re-emitted identical: confirmed
            aviso = None
        if aviso:
            avisados[chave] = avisados.get(chave, 0) + 1
            avisados["_ultimo"] = chave
            historico += f"{bruto}\n{aviso}\n"
            turnos.append(dict(emitiu=bruto, aviso=aviso))
            print(f"    MODELO : {bruto[:100]}", flush=True)
            print(f"    HARNESS: {aviso[:110]}", flush=True)
            continue
        avisados["_ultimo"] = None
        if fn not in FUNCOES:
            res = f"RESULTADO: erro — função '{fn}' indisponível neste degrau"
        else:
            try:
                valor = FUNCOES[fn](*args)
                res = f"RESULTADO: {json.dumps(valor, ensure_ascii=False)}"
                if rung.startswith("CALC3") and fn.startswith("dp_") and isinstance(valor, (int, float)) and valor < 0:
                    res += ("\nAVISO: um desvio-padrão negativo é impossível — confira a ordem "
                            "e os sinais dos limites e refaça a conversão antes de usar este valor.")
                if fn == "md":
                    avisados["_ultimo_md"] = valor
                elif fn == "ic95_md":
                    avisados["_ultimo_ic"] = valor
            except Exception as e:
                res = f"RESULTADO: erro — {str(e)[:60]}"
        historico += f"{bruto}\n{res}\n"
        turnos.append(dict(emitiu=bruto, resultado=res))
        print(f"    MODELO : {bruto[:100]}", flush=True)
        print(f"    HARNESS: {res[:90]}", flush=True)
    if (rung == "CALC2C" or rung.startswith("CALC3")) and final and avisados.get("_insistiu"):
        final["requer_revisao_humana"] = True
    if rung == "G1" and final is None:
        r = h3.gerar(MODELO, prompt0 + historico +
                     '\nEscreva APENAS o JSON final: {"md": <valor>, "ic95": [<inferior>, <superior>]}',
                     max_tokens=60)
        final = h3.acha_json(r["content"])
    saida = D5 / "saidas" / rung
    saida.mkdir(parents=True, exist_ok=True)
    (saida / f"{tid}.json").write_text(json.dumps(dict(estudo=rot, turnos=turnos, final=final),
                                                  ensure_ascii=False, indent=1), encoding="utf-8")
    n_avisos = sum(1 for t in turnos if t.get("aviso") and t["aviso"] != "formato")
    print(f"  {rot}: {len(turnos)} turnos · avisos de conteúdo: {n_avisos} · "
          f"final: {json.dumps(final, ensure_ascii=False)}", flush=True)
    return dict(estudo=rot, final=final, turnos=len(turnos), avisos=n_avisos)


def sextetos_do_g2b(origem="G2B"):
    """Each study's LAST executed md-call arguments = the model's own sextet."""
    por_estudo = {}
    for tid in h3.TRIALS:
        f = D5 / "saidas" / origem / f"{tid}.json"
        if not f.exists():
            continue
        j = json.loads(f.read_text(encoding="utf-8"))
        sext = None
        for t in j["turnos"]:
            if t.get("resultado", "").startswith("RESULTADO:") and '"funcao": "md"' in t.get("emitiu", ""):
                try:
                    sext = [float(x) for x in json.loads(t["emitiu"])["argumentos"]]
                except Exception:
                    pass
        if sext and len(sext) == 6:
            por_estudo[h3.ROT[tid]] = dict(sexteto=sext, final=j.get("final"))
    return por_estudo


def roda_g3(origem="G2B", rotulo=None):
    rotulo = rotulo or (sys.argv[1].upper() if len(sys.argv) > 1 else "G3")
    base = (D5 / "prompts" / "e5-g3.txt").read_text(encoding="utf-8")
    proprios = sextetos_do_g2b(origem)
    resumo = "\n".join(
        f"- {rot}: sexteto {d['sexteto']} → MD {d['final'].get('md') if d['final'] else '?'} "
        f"IC95 {d['final'].get('ic95') if d['final'] else '?'}" for rot, d in proprios.items())
    prompt0 = base.replace("{RESUMO}", resumo)
    historico = ""
    turnos = []
    avisados = {}
    final = None
    for _ in range(8):
        r = gerar_schema(prompt0 + historico + "\nPróximo JSON:", max_tokens=400, schema=SCHEMA_G3)
        bruto = r["content"].strip()
        try:
            js = json.loads(bruto)
        except Exception:
            historico += f"{bruto}\nAVISO: formato inválido.\n"
            turnos.append(dict(emitiu=bruto, aviso="formato"))
            continue
        if js.get("funcao") == "fim":
            a = js.get("argumentos", [])
            final = dict(md=a[0], ic95=[a[1], a[2]]) if len(a) >= 3 else None
            turnos.append(dict(emitiu=bruto))
            break
        sxs = js.get("sextetos") or []
        if len(sxs) < 2:
            aviso = ("AVISO: a chamada pool_dl_md precisa do campo 'sextetos' com pelo menos "
                     "dois sextetos [m1, dp1, n1, m2, dp2, n2] — os seus resultados por estudo "
                     "estão listados acima. Reemita a chamada completa.")
            historico += f"{bruto}\n{aviso}\n"
            turnos.append(dict(emitiu=bruto, aviso=aviso))
            print(f"    MODELO : {bruto[:100]}", flush=True)
            print(f"    HARNESS: {aviso[:110]}", flush=True)
            continue
        aviso = None
        proprios_l = [d["sexteto"] for d in proprios.values()]
        for s in sxs:
            if not any(all(abs(a - b) <= 0.005 for a, b in zip(s, p)) for p in proprios_l):
                aviso = (f"AVISO: o sexteto {s} não corresponde a nenhum dos seus resultados "
                         "por estudo listados acima. Confira e reemita (corrigida, ou idêntica "
                         "se você confirma).")
                break
        chave = json.dumps(sxs)
        if aviso and avisados.get("_ultimo") == chave:
            aviso = None
        if aviso and avisados.get(chave, 0) < MAX_AVISOS_POR_CHAMADA:
            avisados[chave] = avisados.get(chave, 0) + 1
            avisados["_ultimo"] = chave
            historico += f"{bruto}\n{aviso}\n"
            turnos.append(dict(emitiu=bruto, aviso=aviso))
            print(f"    MODELO : {bruto[:100]}", flush=True)
            print(f"    HARNESS: {aviso[:110]}", flush=True)
            continue
        avisados["_ultimo"] = None
        try:
            res = f"RESULTADO: {json.dumps(h3.pool_dl_md(sxs), ensure_ascii=False)}"
        except Exception as e:
            res = f"RESULTADO: erro — {str(e)[:60]}"
        historico += f"{bruto}\n{res}\n"
        turnos.append(dict(emitiu=bruto, resultado=res))
        print(f"    MODELO : {bruto[:100]}", flush=True)
        print(f"    HARNESS: {res[:90]}", flush=True)
    saida = D5 / "saidas" / rotulo
    saida.mkdir(parents=True, exist_ok=True)
    (saida / "pool.json").write_text(json.dumps(dict(estudo="POOL", resumo=resumo, turnos=turnos,
                                                     final=final), ensure_ascii=False, indent=1),
                                     encoding="utf-8")
    verdade_propria = h3.pool_dl_md([d["sexteto"] for d in proprios.values()])
    consistente = bool(final) and abs(final["md"] - verdade_propria["md"]) <= 0.01 and \
        all(abs(a - b) <= 0.01 for a, b in zip(final["ic95"], verdade_propria["ic95"]))
    resultado = dict(final=final, pool_sobre_os_proprios_sextetos=verdade_propria,
                     consistente=consistente, estudos_oferecidos=len(proprios))
    (D5 / f"resultados-{rotulo}.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1),
                                                  encoding="utf-8")
    print(f"== {rotulo}: consistente com os próprios sextetos: {consistente} · "
          f"final {json.dumps(final, ensure_ascii=False)} · "
          f"pool dos próprios: {json.dumps(verdade_propria, ensure_ascii=False)}", flush=True)


def main():
    rung = (sys.argv[1] if len(sys.argv) > 1 else "G1").upper()
    assert rung in ("G1", "G2", "G2B", "G3", "G3B", "CALC2C", "CALC3G", "POOLG"), \
        "uso: e5-harness.py G1|G2|G2B|G3|G3B|CALC2C|CALC3G|POOLG"
    assert h3.ELENCO == "base"
    if rung.startswith("G3") or rung == "POOLG":
        print(f"===== Estudo 5 · pooling · {MODELO}", flush=True)
        roda_g3(origem="CALC3G" if rung == "POOLG" else "G2B", rotulo=rung)
        return
    if rung == "CALC2C":
        pasta = D5 / "saidas" / "EXTRA2"
    elif rung.startswith("CALC3"):
        pasta = D5 / "saidas" / "EXTRA3"
    else:
        pasta = None
    nome_prompt = "calc2" if (rung == "CALC2C" or rung.startswith("CALC3")) else ("g2" if rung.startswith("G2") else "g1")
    base = (D5 / "prompts" / f"e5-{nome_prompt}.txt").read_text(encoding="utf-8")
    print(f"===== Estudo 5 · {rung} · {MODELO} [{h3.MODELS[MODELO]['ollama']}]"
          + (" · redes ativas: 8" if rung == "CALC2C" else ""), flush=True)
    t0 = time.time()
    resultados = [roda_estudo(rung, tid, base, pasta_fichas=pasta) for tid in h3.TRIALS]
    # grading reference (grader-side, computed after the runs)
    c3 = carrega("c3", "scripts/estudo3/corrigir-e3.py")
    exatos = 0
    for r, tid in zip(resultados, h3.TRIALS):
        s = c3.sexteto(ficha_r2(tid, pasta))
        if s and r["final"]:
            vmd, vic = h3.md(*s), h3.ic95_md(*s)
            ok = (abs(float(r["final"].get("md", 9)) - vmd) <= 0.01
                  and abs(float(r["final"]["ic95"][0]) - vic[0]) <= 0.01
                  and abs(float(r["final"]["ic95"][1]) - vic[1]) <= 0.01)
            r["verdade"] = dict(md=vmd, ic95=vic)
            r["exato"] = ok
            exatos += ok
    (D5 / f"resultados-{rung}.json").write_text(json.dumps(resultados, ensure_ascii=False, indent=1),
                                                encoding="utf-8")
    print(f"== {rung}: {exatos}/7 estudos exatos vs a verdade das próprias fichas "
          f"· {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()

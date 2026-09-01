# -*- coding: utf-8 -*-
"""Study 8 — the ENGLISH harness build (protocol §4.1), ported verbatim from
the frozen Study-5 ten-net harness: same net logic, same budgets, same
confirm-by-repeat and insistence mechanics; strings, JSON keys and function
names per the instrument library's correspondence tables. Detection only:
nets warn, never substitute.

Function names (EN prompts): md · ci95_md · sd_from_ci · sd_from_se ·
sd_change_r05 · pool_dl_md. Call JSON: {"function", "arguments", "source",
"derivation"}; closing: {"function": "end", "arguments": [md, lo, hi]}.
Sheets are the ENGLISH sheets (fields per t1/e3-extraction EN).
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
MODELO = "gemma12"
MAX_TURNOS = 16
MAX_AVISOS_POR_CHAMADA = 2

_sp = importlib.util.spec_from_file_location("h3", ROOT / "scripts" / "estudo3" / "e3-harness.py")
h3 = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(h3)

FUNCOES = {"md": h3.md, "ci95_md": h3.ic95_md, "sd_from_ci": h3.dp_de_ic,
           "sd_from_se": h3.dp_de_se, "sd_change_r05": h3.dp_mudanca_r05}

SLOTS = {"md": "MDNMDN", "ci95_md": "MDNMDN", "sd_from_ci": "IIN",
         "sd_from_se": "EN", "sd_change_r05": "DD"}
CLASSE_OK = {
    "M": ("change_mean", "derived"),
    "D": ("dispersion", "_sd", "derived", "previous-result", "previous result"),
    "N": ("n_randomized", "n_analyzed"),
    "I": ("dispersion", "dispersion_type"),
    "E": ("dispersion",),
}
CLASSE_NOME = {"M": "a CHANGE mean (change_mean or a declared derivation)",
               "D": "a dispersion/SD (dispersion, _sd, a derivation or a sd_* result)",
               "N": "a group size (n_randomized/n_analyzed)",
               "I": "a CI bound (a dispersion field)",
               "E": "a standard error (a dispersion field)"}
ARIDADE = {"md": (6, "md(m1, sd1, n1, m2, sd2, n2)"),
           "ci95_md": (6, "ci95_md(m1, sd1, n1, m2, sd2, n2)"),
           "sd_from_ci": (3, "sd_from_ci(lower, upper, n)"),
           "sd_from_se": (2, "sd_from_se(se, n)"),
           "sd_change_r05": (2, "sd_change_r05(sd_baseline, sd_final)")}

SCHEMA_CALL = {
    "type": "object",
    "properties": {
        "function": {"type": "string"},
        "arguments": {"type": "array", "items": {"type": "number"}},
        "source": {"type": "array", "items": {"type": "string"}},
        "derivation": {"type": "string"},
    },
    "required": ["function", "arguments"],
    "additionalProperties": False,
}
SCHEMA_G3 = {
    "type": "object",
    "properties": {
        "function": {"type": "string"},
        "sextets": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}},
        "arguments": {"type": "array", "items": {"type": "number"}},
    },
    "required": ["function"],
    "additionalProperties": False,
}


def gerar_schema(prompt, max_tokens, schema):
    m = h3.MODELS[MODELO]
    body = dict(model=m["ollama"], prompt=prompt, stream=False, think=False,
                format=schema, options=dict(num_predict=max_tokens, num_ctx=h3.CTX))
    r, dt = h3.post_json(h3.OLLAMA + "/api/generate", body)
    if r.get("error"):
        raise RuntimeError(r["error"])
    return dict(content=r.get("response", "") or "", dt=r.get("total_duration", 0) / 1e9 or dt)


def numeros_da_ficha(ficha):
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
    for a in args:
        if a == 0:
            continue
        if any(abs(v - a) <= 0.005 for _, v in nums):
            continue
        opostos = [c for c, v in nums if abs(abs(v) - abs(a)) <= 0.005 and (v > 0) != (a > 0)]
        if opostos:
            return (f"WARNING: the argument {a} has the same magnitude as the sheet field "
                    f"'{opostos[0]}' but the OPPOSITE sign — and no sheet number equals {a}. "
                    "Check and re-emit the call (corrected, or identical if you confirm it).")
    return None


def aviso_fonte(args, fontes, ficha):
    for a, f in zip(args, fontes or []):
        fl = str(f).strip().lower()
        if fl in ("derived", "previous-result", "previous result", ""):
            continue
        candidatos = [(t, v) for t, v in numeros_da_ficha(ficha)
                      if t.lower().endswith(fl) or fl in t.lower()]
        if candidatos and not any(abs(v - a) <= 0.005 for _, v in candidatos):
            lista = "; ".join(f"'{t}' = {v}" for t, v in candidatos[:3])
            return (f"WARNING: the argument {a} declares source '{f}', but the sheet records: "
                    f"{lista}. Check and re-emit the call "
                    "(corrected, or identical if you confirm it).")
    return None


def aviso_derivacao(args, fontes, js, nums):
    fl = [str(f).strip().lower() for f in (fontes or [])]
    if "derived" not in fl:
        return None
    d = str(js.get("derivation", "")).strip().replace("−", "-")
    if not d:
        return ('WARNING: an argument declares source "derived" — include the "derivation" '
                'field with the operation and its operands, for example "7.1 - 6.8". '
                'Re-emit the complete call.')
    for x in re.findall(r"-?\d+(?:\.\d+)?", d):
        if not any(abs(float(x) - v) <= 0.005 for _, v in nums):
            return (f"WARNING: the derivation '{d}' uses {x}, which is not a sheet value. "
                    "Check and re-emit (corrected, or identical if you confirm it).")
    m2 = re.match(r"\s*(-?\d+(?:\.\d+)?)\s*([-+])\s*(-?\d+(?:\.\d+)?)\s*$", d)
    if m2:
        a, op, b = float(m2.group(1)), m2.group(2), float(m2.group(3))
        val = a - b if op == "-" else a + b
        idx = fl.index("derived")
        if idx < len(args) and abs(args[idx] - val) > 0.01:
            return (f"WARNING: the derivation '{d}' yields {round(val, 2)}, but the argument "
                    f"sent is {args[idx]}. Check and re-emit (corrected, or identical if you confirm).")
    return None


def aviso_tipos(fn, args, fontes):
    slots = SLOTS.get(fn, "")
    for i, (a, cls) in enumerate(zip(args, slots)):
        f = str(fontes[i]).strip().lower() if fontes and i < len(fontes) else ""
        if cls == "D" and a < 0:
            return (f"WARNING: the argument {a} (slot {i+1} of {fn}, SD class) is NEGATIVE — "
                    "a standard deviation is always positive. Check and re-emit.")
        if cls == "N" and (a <= 1 or abs(a - round(a)) > 0.001):
            return (f"WARNING: the argument {a} (slot {i+1} of {fn}, n class) is not a valid "
                    "group size (integer > 1). Check and re-emit.")
        if f and not any(t in f for t in CLASSE_OK.get(cls, ())):
            return (f"WARNING: slot {i+1} of {fn} expects {CLASSE_NOME[cls]}, but received the "
                    f"source '{fontes[i]}' with value {a}. A level (baseline/final) is not a "
                    "change, and an md result is not an arm mean. Check and re-emit "
                    "(corrected, or identical if you confirm it).")
    return None


def aviso_ordem_ic(fn, args):
    if fn == "sd_from_ci" and len(args) >= 2 and args[0] > args[1]:
        return (f"WARNING: in sd_from_ci the first argument is the LOWER bound and the second "
                f"the UPPER — you sent ({args[0]}, {args[1]}), in inverted order. "
                "Check the signs and re-emit.")
    return None


def aviso_coerencia_ic(fn, args, ultimo_md):
    if fn == "ci95_md" and ultimo_md is not None and len(args) >= 4:
        d = round(args[0] - args[3], 2)
        if abs(d - ultimo_md) > 0.01:
            return (f"WARNING: the arguments of this ci95_md imply a difference m1−m2 = {d}, "
                    f"but this study's MD (your last md result) is {ultimo_md}. "
                    "Both must use the SAME sextet. Check and re-emit.")
    return None


def aviso_aridade(fn, args):
    if fn in ARIDADE and len(args) != ARIDADE[fn][0]:
        n, ass = ARIDADE[fn]
        return (f"WARNING: the function {fn} requires {n} arguments — {ass} — and you sent "
                f"{len(args)}. Re-emit the complete call.")
    return None


def roda_estudo(saida_dir, tid, base, ficha, rot):
    nums = numeros_da_ficha(ficha)
    prompt0 = base.replace("{SHEET}", json.dumps(ficha, ensure_ascii=False, indent=1))
    historico = ""
    turnos = []
    avisados = {}
    final = None
    for _ in range(MAX_TURNOS):
        r = gerar_schema(prompt0 + historico + "\nNext JSON:", max_tokens=160,
                         schema=SCHEMA_CALL)
        bruto = r["content"].strip()
        try:
            js = json.loads(bruto)
            fn = js.get("function", "")
            if fn == "end":
                a = js.get("arguments", [])
                if len(a) >= 3 and not avisados.get("_fim_avisado"):
                    difere = []
                    if avisados.get("_ultimo_md") is not None and abs(a[0] - avisados["_ultimo_md"]) > 0.005:
                        difere.append(f"md {a[0]} ≠ executed result {avisados['_ultimo_md']}")
                    ic_exec = avisados.get("_ultimo_ic")
                    if ic_exec and (abs(a[1] - ic_exec[0]) > 0.005 or abs(a[2] - ic_exec[1]) > 0.005):
                        difere.append(f"ci95 [{a[1]}, {a[2]}] ≠ executed result {ic_exec}")
                    if difere:
                        avisados["_fim_avisado"] = True
                        aviso_f = ("WARNING: your end differs from your own executed results: "
                                   + "; ".join(difere) + ". Re-emit the end with the executed "
                                   "results, or identical if you confirm it.")
                        historico += f"{bruto}\n{aviso_f}\n"
                        turnos.append(dict(emitiu=bruto, aviso=aviso_f))
                        print(f"    MODEL  : {bruto[:100]}", flush=True)
                        print(f"    HARNESS: {aviso_f[:110]}", flush=True)
                        continue
                final = dict(md=a[0], ic95=[a[1], a[2]]) if len(a) >= 3 else None
                if avisados.get("_fim_avisado") and final:
                    final["requires_human_review"] = True
                turnos.append(dict(emitiu=bruto))
                break
            parsed = (fn, [float(x) for x in js.get("arguments", [])], js.get("source"))
        except Exception:
            parsed = None
        if not parsed:
            historico += f"{bruto}\nWARNING: invalid format — emit exactly one call in the requested format.\n"
            turnos.append(dict(emitiu=bruto, aviso="format"))
            continue
        fn, args, fontes = parsed
        chave = f"{fn}{args}"
        aviso = aviso_aridade(fn, args)
        if not aviso and avisados.get(chave, 0) < MAX_AVISOS_POR_CHAMADA and chave not in avisados.get("_conf", []):
            aviso = aviso_sinal(args, nums) or aviso_fonte(args, fontes, ficha) or \
                aviso_derivacao(args, fontes, js, nums) or \
                aviso_tipos(fn, args, fontes) or aviso_ordem_ic(fn, args) or \
                aviso_coerencia_ic(fn, args, avisados.get("_ultimo_md"))
        if aviso and avisados.get(chave, 0) >= MAX_AVISOS_POR_CHAMADA:
            avisados["_insistiu"] = True
        if aviso and avisados.get("_ultimo") == chave:
            avisados.setdefault("_conf", []).append(chave)
            aviso = None
        if aviso:
            avisados[chave] = avisados.get(chave, 0) + 1
            avisados["_ultimo"] = chave
            historico += f"{bruto}\n{aviso}\n"
            turnos.append(dict(emitiu=bruto, aviso=aviso))
            print(f"    MODEL  : {bruto[:100]}", flush=True)
            print(f"    HARNESS: {aviso[:110]}", flush=True)
            continue
        avisados["_ultimo"] = None
        if fn not in FUNCOES:
            res = f"RESULT: error — function '{fn}' unavailable at this rung"
        else:
            try:
                valor = FUNCOES[fn](*args)
                res = f"RESULT: {json.dumps(valor, ensure_ascii=False)}"
                if fn.startswith("sd_") and isinstance(valor, (int, float)) and valor < 0:
                    res += ("\nWARNING: a negative standard deviation is impossible — check the "
                            "order and signs of the bounds and redo the conversion before using this value.")
                if fn == "md":
                    avisados["_ultimo_md"] = valor
                elif fn == "ci95_md":
                    avisados["_ultimo_ic"] = valor
            except Exception as e:
                res = f"RESULT: error — {str(e)[:60]}"
        historico += f"{bruto}\n{res}\n"
        turnos.append(dict(emitiu=bruto, resultado=res))
        print(f"    MODEL  : {bruto[:100]}", flush=True)
        print(f"    HARNESS: {res[:90]}", flush=True)
    if final and avisados.get("_insistiu"):
        final["requires_human_review"] = True
    saida_dir.mkdir(parents=True, exist_ok=True)
    (saida_dir / f"{tid}.json").write_text(json.dumps(dict(estudo=rot, turnos=turnos, final=final),
                                                      ensure_ascii=False, indent=1), encoding="utf-8")
    n_avisos = sum(1 for t in turnos if t.get("aviso") and t["aviso"] != "format")
    print(f"  {rot}: {len(turnos)} turns · content warnings: {n_avisos} · "
          f"final: {json.dumps(final, ensure_ascii=False)}", flush=True)
    return dict(estudo=rot, final=final, turnos=len(turnos), avisos=n_avisos)


def sextetos_de(saida_dir, trials, rot_map):
    por_estudo = {}
    for tid in trials:
        f = saida_dir / f"{tid}.json"
        if not f.exists():
            continue
        j = json.loads(f.read_text(encoding="utf-8"))
        sext = None
        for t in j["turnos"]:
            if t.get("resultado", "").startswith("RESULT:") and '"function": "md"' in t.get("emitiu", ""):
                try:
                    sext = [float(x) for x in json.loads(t["emitiu"])["arguments"]]
                except Exception:
                    pass
        if sext and len(sext) == 6:
            por_estudo[rot_map[tid]] = dict(sexteto=sext, final=j.get("final"))
    return por_estudo


def roda_g3(base, proprios, out_path):
    resumo = "\n".join(
        f"- {rot}: sextet {d['sexteto']} → MD {d['final'].get('md') if d['final'] else '?'} "
        f"CI95 {d['final'].get('ic95') if d['final'] else '?'}" for rot, d in proprios.items())
    prompt0 = base.replace("{SUMMARY}", resumo)
    historico = ""
    turnos = []
    final = None
    pool_exec = None
    for _ in range(8):
        r = gerar_schema(prompt0 + historico + "\nNext JSON:", max_tokens=400, schema=SCHEMA_G3)
        bruto = r["content"].strip()
        try:
            js = json.loads(bruto)
        except Exception:
            historico += f"{bruto}\nWARNING: invalid format.\n"
            turnos.append(dict(emitiu=bruto, aviso="format"))
            continue
        fn = js.get("function", "")
        if fn == "pool_dl_md":
            sx = js.get("sextets") or []
            try:
                pool_exec = h3.pool_dl_md([[float(x) for x in s] for s in sx])
                res = f"RESULT: {json.dumps(pool_exec, ensure_ascii=False)}"
            except Exception as e:
                res = f"RESULT: error — {str(e)[:60]}"
            historico += f"{bruto}\n{res}\n"
            turnos.append(dict(emitiu=bruto, resultado=res))
            print(f"    MODEL  : {bruto[:100]}", flush=True)
            print(f"    HARNESS: {res[:110]}", flush=True)
        elif fn == "end":
            a = js.get("arguments", [])
            final = dict(md=a[0], ic95=[a[1], a[2]]) if len(a) >= 3 else None
            turnos.append(dict(emitiu=bruto))
            break
        else:
            historico += f"{bruto}\nWARNING: use pool_dl_md then end.\n"
            turnos.append(dict(emitiu=bruto, aviso="fluxo"))
    pool_proprios = h3.pool_dl_md([d["sexteto"] for d in proprios.values()])
    consist = bool(final and pool_exec and abs(final["md"] - pool_exec["md"]) <= 0.005)
    out = dict(final=final, pool_executado=pool_exec,
               pool_sobre_os_proprios_sextetos=pool_proprios, consistente=consist,
               estudos_oferecidos=len(proprios), turnos=turnos)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"== POOL: consistent with its own sextets: {consist} · final "
          f"{json.dumps(final, ensure_ascii=False)} · pool over own sextets: "
          f"{json.dumps(pool_proprios, ensure_ascii=False)}", flush=True)
    return out

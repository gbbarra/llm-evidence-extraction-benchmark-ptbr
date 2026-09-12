# -*- coding: utf-8 -*-
"""EXTRAI Study 13 — the v3 corrector: "cite the printed; the program derives".

A v3 sheet transcribes only PRINTED quantities, each with a type label and a quotation. This module derives the
meta-analytic sextet (change mean, change SD, n per arm) by the key's own rules — the same functions the graders
use (e3-harness: dp_de_ic, dp_de_se, dp_mudanca_r05) — and records, for every derived cell, the rule, the printed
inputs and their quotations. Derivations happen AFTER the seal reversal, so the reversal lens only ever sees
printed values (this removes the "derived through the seal" grader artifact of Study 12).

Robustness inherited from the 2026-09-12 corrections (dados/estudo12/p2/artefato-v2-tipo.md): every {value,
where, quote} object is unwrapped before any rule reads it; the interval parser normalizes Unicode minus signs,
strips the "CI95" token, prefers the pair in the dispersion field and returns the bounds in ascending order.

Usage:
  python scripts/estudo13/e13-corrector.py --gate            # reproduce every derived cell of the anchor-2 key
  python scripts/estudo13/e13-corrector.py sheet.json [...]  # sextet and routes of v3 sheets (anchor 2)
"""
import argparse
import importlib.util
import io
import json
import math
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]


def _carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, RAIZ / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


h3 = _carrega("h3", "scripts/estudo3/e3-harness.py")   # the graders' validated functions

NR = ("", "NR", "NA", "N/A", "NONE", "NOT REPORTED")


# ------------------------------------------------------------------ reading a sheet
def desembrulha(obj):
    """Every {value, where, quote} object reduced to its value, at any depth."""
    if isinstance(obj, dict):
        if "value" in obj and ("where" in obj or "quote" in obj):
            return obj.get("value")
        return {k: desembrulha(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [desembrulha(v) for v in obj]
    return obj


def citacoes(obj, prefixo=""):
    """The quotation of every field, keyed by dotted path (kept beside the derived cells)."""
    out = {}
    if isinstance(obj, dict):
        if "value" in obj and ("where" in obj or "quote" in obj):
            out[prefixo] = dict(where=obj.get("where", ""), quote=obj.get("quote", ""))
        else:
            for k, v in obj.items():
                out.update(citacoes(v, f"{prefixo}.{k}" if prefixo else k))
    return out


def eh_nr(x):
    return x is None or str(x).strip().upper() in NR


def norm(s):
    return str(s or "").replace("−", "-").replace("–", "-").replace("—", "-")


def num(x):
    if eh_nr(x):
        return None
    t = norm(x).replace(",", ".").strip().rstrip("%").strip()
    try:
        return float(t)
    except ValueError:
        m = re.search(r"-?\d+(?:\.\d+)?", t)
        return float(m.group(0)) if m and len(re.findall(r"-?\d+(?:\.\d+)?", t)) == 1 else None


def numeros_ic(s):
    s = norm(s)
    s = re.sub(r"\b(IC|CI)\s*95\b", " ", s, flags=re.I)
    s = re.sub(r"95\s*%\s*(IC|CI)\b", " ", s, flags=re.I)
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", s)]


def limites_ic(disp, tipo):
    """(lower, upper) of a CI: the pair in the dispersion field when it carries two numbers, else the pair in the
    type field; ascending order (a reversed or sign-dropped pair never yields a negative width)."""
    d, t = numeros_ic(disp), numeros_ic(tipo)
    par = d[-2:] if len(d) >= 2 else (t[-2:] if len(t) >= 2 else None)
    if par is None:
        juntos = t + d
        par = juntos[-2:] if len(juntos) >= 2 else None
    if par is None:
        return None
    return (min(par), max(par))


def classe_tipo(t):
    t = norm(t).strip().upper()
    if not t or t in NR:
        return None
    if "CI" in t or "IC" in t or "INTERVAL" in t or "CONFIDENCE" in t:
        return "CI"
    if re.search(r"\bSE\b|\bSEM\b|STANDARD ERROR", t):
        return "SE"
    if re.search(r"\bSD\b|\bDP\b|STANDARD DEVIATION", t):
        return "SD"
    if "IQR" in t or "INTERQUARTILE" in t:
        return "IQR"
    if "RANGE" in t:
        return "RANGE"
    return None


# ------------------------------------------------------------------ the rules (the key's own)
def dp_de_dispersao(valor, tipo, n, rotulo):
    """SD from a printed dispersion and its declared type. Returns (sd, route) or (None, route)."""
    c = classe_tipo(tipo)
    if c == "SD":
        v = num(valor)
        return (v, dict(rule="sd as printed", inputs={f"{rotulo}_sd": v})) if v is not None else (None, dict(rule="sd not numeric"))
    if c == "SE":
        se = num(valor)
        if se is None or not n:
            return None, dict(rule="sd_from_se needs se and n", inputs={"se": se, "n": n})
        return h3.dp_de_se(se, n), dict(rule="sd_from_se", inputs={"se": se, "n": n})
    if c == "CI":
        lim = limites_ic(valor, tipo)
        if lim is None or not n:
            return None, dict(rule="sd_from_ci needs two bounds and n", inputs={"bounds": lim, "n": n})
        lo, hi = lim
        return h3.dp_de_ic(lo, hi, n), dict(rule="sd_from_ci", inputs={"lower": lo, "upper": hi, "n": n})
    if c in ("IQR", "RANGE"):
        return None, dict(rule=f"{c.lower()} not convertible to sd", inputs={"printed": valor})
    if num(valor) is not None and c is None:
        return None, dict(rule="dispersion printed without a type label — not used", inputs={"printed": valor})
    return None, dict(rule="no dispersion printed")


def braco_v3(arm):
    """(mean, sd, n, routes) for one arm of a v3 sheet, derivations by the key's rules and only from printed inputs."""
    a = desembrulha(arm) or {}
    rotas = {}
    n = num(a.get("n_analyzed"))
    rotas["n"] = dict(rule="n_analyzed as printed" if n is not None else "n_randomized as printed (n_analyzed NR)")
    if n is None:
        n = num(a.get("n_randomized"))
    m = num(a.get("hba1c_change_mean"))
    sd = None
    if m is not None:
        rotas["mean"] = dict(rule="change mean as printed", inputs={"change": m})
        sd, rotas["sd"] = dp_de_dispersao(a.get("hba1c_change_dispersion"), a.get("hba1c_change_dispersion_type"), n, "change")
        if sd is None:
            # the key's own fallback: a change mean printed without its dispersion, baseline and final SDs printed
            sd0, r0 = dp_de_dispersao(a.get("hba1c_baseline_dispersion"), a.get("hba1c_baseline_dispersion_type"), n, "baseline")
            sd1, r1 = dp_de_dispersao(a.get("hba1c_final_dispersion"), a.get("hba1c_final_dispersion_type"), n, "final")
            if sd0 is not None and sd1 is not None:
                sd = h3.dp_mudanca_r05(sd0, sd1)
                rotas["sd"] = dict(rule="sd_change_r05 (change dispersion not printed)", inputs={"sd_baseline": sd0, "sd_final": sd1, "baseline_route": r0, "final_route": r1, "change_route": rotas["sd"]})
    else:
        b0, b1 = num(a.get("hba1c_baseline_mean")), num(a.get("hba1c_final_mean"))
        if b0 is not None and b1 is not None:
            m = round(b1 - b0, 2)
            rotas["mean"] = dict(rule="change = final − baseline", inputs={"final": b1, "baseline": b0})
            sd0, r0 = dp_de_dispersao(a.get("hba1c_baseline_dispersion"), a.get("hba1c_baseline_dispersion_type"), n, "baseline")
            sd1, r1 = dp_de_dispersao(a.get("hba1c_final_dispersion"), a.get("hba1c_final_dispersion_type"), n, "final")
            if sd0 is not None and sd1 is not None:
                sd = h3.dp_mudanca_r05(sd0, sd1)
                rotas["sd"] = dict(rule="sd_change_r05", inputs={"sd_baseline": sd0, "sd_final": sd1, "baseline_route": r0, "final_route": r1})
            else:
                rotas["sd"] = dict(rule="sd_change_r05 needs both SDs", inputs={"baseline_route": r0, "final_route": r1})
        else:
            rotas["mean"] = dict(rule="no change and no baseline/final pair printed")
            rotas["sd"] = dict(rule="no dispersion derivable")
    return m, sd, n, rotas


def sexteto_v3(js):
    """The seven cells of the anchor-2 grader (CELULAS_A2 order) plus the routes, from a v3 sheet."""
    e = braco_v3(js.get("experimental_arm"))
    c = braco_v3(js.get("control_arm"))
    tot = num(desembrulha(js.get("n_randomized_total")))
    cel = dict(exp_media=e[0], exp_dispersao=e[1], exp_n=e[2], ctl_media=c[0], ctl_dispersao=c[1], ctl_n=c[2],
               n_randomizado_total=tot)
    return cel, dict(experimental=e[3], control=c[3], quotes=citacoes(js))


def mortes_de_percentual(pct, n):
    """Anchor 3: deaths from a printed percentage and a denominator, when the count itself is not printed."""
    p, k = num(pct), num(n)
    if p is None or k is None:
        return None
    return int(round(p * k / 100.0))


# ------------------------------------------------------------------ the build gate
def _parse_conta(regra, conta):
    s = norm(conta).replace("×", "*").replace("·", "*").replace("²", "^2").replace(" ", "")
    if regra == "dp_de_ic":
        m = re.match(r"\((-?[\d.]+)-\(?(-?[\d.]+)\)?\)/2/1\.96\*sqrt\((\d+)\)=(-?[\d.]+)", s)
        if m:
            hi, lo, n, v = float(m.group(1)), float(m.group(2)), int(m.group(3)), float(m.group(4))
            return dict(lo=min(lo, hi), hi=max(lo, hi), n=n), v
    if regra == "dp_de_se":
        m = re.match(r"(-?[\d.]+)\*sqrt\((\d+)\)=(-?[\d.]+)", s)
        if m:
            return dict(se=float(m.group(1)), n=int(m.group(2))), float(m.group(3))
    if regra == "media_de_basal_final":
        m = re.match(r"(-?[\d.]+)-(-?[\d.]+)=(-?[\d.]+)", s)
        if m:
            return dict(final=float(m.group(1)), baseline=float(m.group(2))), float(m.group(3))
    if regra == "dp_imputada_r05":
        m = re.match(r"sqrt\((-?[\d.]+)\^2\+(-?[\d.]+)\^2-2\*0\.5\*(-?[\d.]+)\*(-?[\d.]+)\)=(-?[\d.]+)", s)
        if m:
            return dict(sd0=float(m.group(1)), sd1=float(m.group(2))), float(m.group(5))
    return None, None


def gate(verbose=True):
    """Every derived cell of the anchor-2 key must be reproduced by this corrector from the inputs the key cites.
    Returns (checked, failures)."""
    g = json.load(io.open(RAIZ / "dados" / "estudo3" / "gabarito-fonte.json", encoding="utf-8"))["estudos"]
    checked, falhas = 0, []
    for tid, e in g.items():
        for campo, c in e["celulas"].items():
            regra, conta = c.get("regra"), c.get("conta")
            if regra not in ("dp_de_ic", "dp_de_se", "media_de_basal_final", "dp_imputada_r05") or not conta:
                continue
            ins, _ = _parse_conta(regra, conta)
            if ins is None:
                falhas.append(f"{tid} {campo}: conta not parsed: {conta!r}")
                continue
            if regra == "dp_de_ic":
                got = h3.dp_de_ic(ins["lo"], ins["hi"], ins["n"])
            elif regra == "dp_de_se":
                got = h3.dp_de_se(ins["se"], ins["n"])
            elif regra == "media_de_basal_final":
                got = round(ins["final"] - ins["baseline"], 2)
            else:
                got = h3.dp_mudanca_r05(ins["sd0"], ins["sd1"])
            alvo = float(c["valor"])
            checked += 1
            ok = abs(got - alvo) <= 0.0051 + 1e-9
            if verbose:
                print(f"  {'ok  ' if ok else 'FALHA'} {tid:11s} {campo:14s} {regra:22s} {ins} → {got} (key {alvo})")
            if not ok:
                falhas.append(f"{tid} {campo}: {got} vs key {alvo}")
    return checked, falhas


def main():
    ap = argparse.ArgumentParser(description="Study 13 v3 corrector")
    ap.add_argument("--gate", action="store_true", help="reproduce the anchor-2 key's derived cells from their cited inputs")
    ap.add_argument("fichas", nargs="*", help="v3 sheet JSON files (anchor 2) to route")
    a = ap.parse_args()
    if a.gate:
        n, f = gate()
        print(f"\ngate: {n} derived key cells checked, {len(f)} failures")
        if f:
            raise SystemExit("\n".join(f))
    for p in a.fichas:
        j = json.load(io.open(p, encoding="utf-8"))
        js = h3.acha_json(j["conteudo"]) if isinstance(j.get("conteudo"), str) else (j.get("conteudo") or j)
        cel, rotas = sexteto_v3(js or {})
        print(p, json.dumps(cel), json.dumps({k: v for k, v in rotas.items() if k != "quotes"}, ensure_ascii=False)[:600])


if __name__ == "__main__":
    main()

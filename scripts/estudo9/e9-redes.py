# -*- coding: utf-8 -*-
"""EXTRAI Study 9 — the three provenance nets (protocol §2), grader-side.

Doctrine, unchanged from the series: nets DETECT AND WARN, NEVER SUBSTITUTE.
Nothing here edits a sheet, a value or a key. Every flag is a candidate for
quotation-bound adjudication, never a verdict.

  N9-1 quote-exists   the cell's quote, normalized (whitespace collapsed;
                      hyphen/minus/dash unified; case-folded), must occur as a
                      substring of the perturbed source the model read.
                      Failure flags PROVENANCE HALLUCINATION.
  N9-2 value-in-quote every numeric token of the cell's value must occur inside
                      that cell's own quote (tolerance +/-0.005); a qualitative
                      value must occur as a string.
  N9-3 type-vs-quote  where a cell declares a dispersion type, the declared
                      class must match the form printed in its own quote
                      (declared SD/SE while the quote prints an interval, or
                      declared CI while the quote prints a lone +/- spread).
                      This is the campaign's N7-1b check mechanized at the sheet.

Written against the protocol's specification before any Study-9 sheet was
inspected, so the rules are not tuned to the data they grade.

Run: python scripts/estudo9/e9-redes.py <model> [ma1|ma2]
Out: dados/estudo9/redes-proveniencia.json  (+ console report)
"""
import importlib.util
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
E9 = ROOT / "dados" / "estudo9"
FONTES = {
    "ma1": [ROOT / "corpus" / "perturbados", ROOT / "corpus" / "perturbados-fechados"],
    "ma2": [ROOT / "corpus" / "estudo3" / "perturbados"],
}

_x = importlib.util.spec_from_file_location("ext", ROOT / "scripts" / "estudo4" / "e4-extensao.py")
ext = importlib.util.module_from_spec(_x)
_x.loader.exec_module(ext)
h3 = ext.h3

TRAVESSOES = dict.fromkeys(map(ord, "‐‑‒–—―−­"), "-")


def normaliza(s):
    """Whitespace collapsed, dashes unified, case-folded, NFKC — per protocol."""
    s = unicodedata.normalize("NFKC", str(s or "")).translate(TRAVESSOES)
    return re.sub(r"\s+", " ", s).strip().casefold()


def fonte(tid, ancora):
    for d in FONTES[ancora]:
        p = d / f"{tid}.txt"
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace")
    return None


def celulas(obj, prefixo=""):
    """Yield (campo, cell-dict); MA-2 sheets nest cells inside arm objects."""
    for campo, v in (obj or {}).items():
        if not isinstance(v, dict):
            continue
        if "value" in v:
            yield prefixo + campo, v
        else:
            yield from celulas(v, campo.replace("_arm", "") + ".")


def nums(s):
    return re.findall(r"-?\d+(?:[.,]\d+)?", str(s or "").replace(",", "."))


_UNI = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
        "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
        "seventeen", "eighteen", "nineteen"]
_DEZ = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
        60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"}


def por_extenso(n):
    """English cardinal spellings of an integer 0-999 (A9-4 item 1).

    Returns the forms a clinical paper actually prints, e.g. 89 -> eighty-nine
    (also accepted with a space), 100 -> one hundred / a hundred.
    """
    if n < 0 or n > 999:
        return []
    if n < 20:
        return [_UNI[n]]
    if n < 100:
        d, u = divmod(n, 10)
        base = _DEZ[d * 10]
        return [base] if u == 0 else [f"{base}-{_UNI[u]}", f"{base} {_UNI[u]}"]
    c, r = divmod(n, 100)
    cabeca = [f"{_UNI[c]} hundred"] + (["a hundred"] if c == 1 else [])
    if r == 0:
        return cabeca
    return [f"{h} and {s}" for h in cabeca for s in por_extenso(r)] + \
           [f"{h} {s}" for h in cabeca for s in por_extenso(r)]


def num_no_texto(n, texto):
    """A numeric token counts as present if some number in the text matches it
    within +/-0.005 (protocol tolerance), so 6.89 matches 6.890 -- or, per
    amendment A9-4 item 1, if its English cardinal spelling occurs in the text."""
    try:
        alvo = float(n)
    except ValueError:
        return False
    for cand in nums(texto):
        try:
            if abs(float(cand) - alvo) <= 0.005:
                return True
        except ValueError:
            continue
    if float(alvo).is_integer():
        alvo_n = normaliza(texto)
        for forma in por_extenso(int(alvo)):
            if re.search(rf"\b{re.escape(forma)}\b", alvo_n):
                return True
    return False


# --- N9-3 printed-form recognizers (applied to the quote only) ---
RE_INTERVALO = re.compile(r"\(\s*-?\d+(?:\.\d+)?\s*(?:to|,|;|--|-|–)\s*-?\d+(?:\.\d+)?\s*\)"
                          r"|\[\s*-?\d+(?:\.\d+)?\s*(?:to|,|;|--|-|–)\s*-?\d+(?:\.\d+)?\s*\]"
                          r"|\b95\s*%\s*ci\b")
RE_SPREAD = re.compile(r"[±]\s*-?\d|\+/-\s*-?\d|\bsd\b|\bs\.d\.|\bsem\b|\bse\b|\bstandard (deviation|error)\b")


def classe_declarada(v):
    t = normaliza(v)
    if not t or t == "nr":
        return None
    if "ci" in t or "confidence" in t or "interval" in t:
        return "CI"
    if re.search(r"\bse\b|standard error", t):
        return "SE"
    if re.search(r"\bsd\b|standard deviation", t):
        return "SD"
    return None


def classe_parse(rec):
    """A9-4 item 3: sub-classify a parse failure, in both arms by the same rule.

    truncation        the generation hit its token ceiling
    leaked deliberation  a valid JSON prefix broken by unescaped prose commentary
    other malformation   everything else
    """
    if str(rec.get("finish", "")).lower() == "length":
        return "parse failure: truncation (finish=length)"
    c = rec.get("content", "") or ""
    try:
        json.loads(c)
        return "parse failure: other malformation"  # unreachable in practice
    except json.JSONDecodeError as e:
        pos = getattr(e, "pos", 0) or 0
        prefixo, resto = c[:pos], c[pos:pos + 200]
        # a valid-looking JSON prefix, then prose continuing after a closed string
        if prefixo.count("{") > prefixo.count("}") and re.search(
                r'"\s*[—–-]{1,2}\s*\w|"\s+(but|however|note|the \w+ says)\b', resto, re.I):
            return "parse failure: leaked deliberation (v2 quote field)"
        return "parse failure: other malformation"


def sub_classe_n91(quote, src_bruto):
    """A9-4 item 2: descriptive class for an N9-1 residue -- never a verdict."""
    q = normaliza(quote)
    if "..." in quote or "…" in quote:
        return "elided"
    src = normaliza(src_bruto)
    # "the fragments exist but not contiguously": greedily cover the quote with
    # maximal token runs that each occur verbatim in the source. A quote covered
    # by a few such runs was assembled from real source text across a gap; one
    # that needs many runs (or whose runs are single tokens) is not.
    toks = [t for t in re.split(r"\s+", q) if t]
    i, fragmentos = 0, []
    while i < len(toks):
        j, melhor = len(toks), None
        while j > i:
            trecho = " ".join(toks[i:j])
            if trecho in src:
                melhor = (trecho, j)
                break
            j -= 1
        if melhor is None:
            return "paraphrased or absent"  # a token that is not in the source at all
        fragmentos.append(melhor[0])
        i = melhor[1]
    if len(fragmentos) >= 2 and max(len(f.split()) for f in fragmentos) >= 2:
        return "stitched"
    return "paraphrased or absent"


def roda(modelo, ancora):
    base = E9 / "saidas" / "v2" / modelo / ancora
    if not base.exists():
        return []
    flags = []
    for f in sorted(base.glob("*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        tid, rep = rec["trial"], rec["replica"]
        src = fonte(tid, ancora)
        if src is None:
            continue
        src_n = normaliza(src)
        js = h3.acha_json(rec.get("content", ""))
        if not isinstance(js, dict):
            flags.append(dict(net="parse", model=modelo, anchor=ancora, trial=tid,
                              replicate=rep, field=None,
                              detail=classe_parse(rec),  # A9-4 item 3
                              value="", quote=""))
            continue
        for campo, cel in celulas(js):
            valor = str(cel.get("value", "") or "").strip()
            quote = str(cel.get("quote", "") or "").strip()
            if valor in ("", "NR"):
                continue  # NR cells carry empty provenance by instrument design
            if not quote:
                flags.append(dict(net="N9-1", model=modelo, anchor=ancora, trial=tid,
                                  replicate=rep, field=campo, detail="filled cell, empty quote",
                                  value=valor[:60], quote=""))
                continue
            # N9-1 quote-exists
            if normaliza(quote) not in src_n:
                sub = sub_classe_n91(quote, src)  # A9-4 item 2, descriptive only
                flags.append(dict(net="N9-1", model=modelo, anchor=ancora, trial=tid,
                                  replicate=rep, field=campo, subclass=sub,
                                  detail=f"quote not verbatim in the source [{sub}]",
                                  value=valor[:60], quote=quote[:140]))
            # N9-2 value-in-quote
            vn = nums(valor)
            if vn:
                faltando = [n for n in vn if not num_no_texto(n, quote)]
                if faltando:
                    flags.append(dict(net="N9-2", model=modelo, anchor=ancora, trial=tid,
                                      replicate=rep, field=campo,
                                      detail=f"value tokens absent from own quote: {faltando}",
                                      value=valor[:60], quote=quote[:140]))
            elif normaliza(valor) not in normaliza(quote):
                flags.append(dict(net="N9-2", model=modelo, anchor=ancora, trial=tid,
                                  replicate=rep, field=campo,
                                  detail="qualitative value absent from own quote",
                                  value=valor[:60], quote=quote[:140]))
            # N9-3 type-vs-quote coherence (dispersion-type cells only)
            if "dispersion_type" in campo:
                decl = classe_declarada(valor)
                qn = normaliza(quote)
                tem_intervalo = bool(RE_INTERVALO.search(qn))
                tem_spread = bool(RE_SPREAD.search(qn))
                if decl in ("SD", "SE") and tem_intervalo and not tem_spread:
                    flags.append(dict(net="N9-3", model=modelo, anchor=ancora, trial=tid,
                                      replicate=rep, field=campo,
                                      detail=f"declared {decl} but the quote prints an interval",
                                      value=valor[:60], quote=quote[:140]))
                elif decl == "CI" and tem_spread and not tem_intervalo:
                    flags.append(dict(net="N9-3", model=modelo, anchor=ancora, trial=tid,
                                      replicate=rep, field=campo,
                                      detail="declared CI but the quote prints a lone spread",
                                      value=valor[:60], quote=quote[:140]))
    return flags


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: e9-redes.py <model> [ma1|ma2]")
    modelo = sys.argv[1]
    ancoras = [sys.argv[2]] if len(sys.argv) > 2 else ["ma1", "ma2"]
    todos = []
    for a in ancoras:
        todos += roda(modelo, a)
    por_rede = {}
    for f in todos:
        por_rede.setdefault(f["net"], []).append(f)
    print(f"\n=== Study 9 provenance nets · {modelo} · {', '.join(ancoras)} ===")
    print("doctrine: detect and warn, never substitute; every flag goes to adjudication\n")
    for rede in ("parse", "N9-1", "N9-2", "N9-3"):
        fs = por_rede.get(rede, [])
        print(f"{rede}: {len(fs)} flag(s)")
        for f in fs[:8]:
            print(f"   {f['trial']}-r{f['replicate']} {f.get('field')}: {f['detail']}")
            if f.get("quote"):
                print(f"      value={f.get('value')!r}  quote={f['quote']!r}")
        if len(fs) > 8:
            print(f"   ... and {len(fs) - 8} more (full list in the JSON)")
    out = E9 / "redes-proveniencia.json"
    antigo = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    antigo[modelo] = todos
    out.write_text(json.dumps(antigo, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nsaved: {out}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""EXTRAI Study 13 — provenance nets over v3 sheets. Warn-only, as in every prior study.

  N9-1 quote-exists      the quotation, normalized, occurs in the perturbed source the model read. Study 13 extension:
                         a quotation that starts with a table title ("Table 2. … | row") is checked on the row part
                         (the title prefix is stripped), because a table row counts as a quotation on the v3 sheet.
  N9-2 value-in-quote    every number of the value occurs in its own quotation.
  N13-1 type-vs-quote    a declared dispersion type contradicts the form printed in the quotation of its dispersion
                         field: "SD"/"SE" declared while the quotation prints an interval; "CI" declared while the
                         quotation prints a lone ± spread and no interval. Extends Study 9's N9-3 to the baseline,
                         final and change dispersions of the v3 sheet.

Run: python scripts/estudo13/e13-redes.py <model> <a1|a2|a3>      (over dados/estudo13/saidas/<anchor>/v3/<model>/)
     python scripts/estudo13/e13-redes.py --self-test
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
SAIDAS = RAIZ / "dados" / "estudo13" / "saidas"


def _carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, RAIZ / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


redes = _carrega("redes9", "scripts/estudo9/e9-redes.py")   # normaliza, nums, num_no_texto, classe_declarada, RE_*
h3 = redes.h3
FONTES = dict(a1=redes.FONTES["ma1"], a2=redes.FONTES["ma2"], a3=[RAIZ / "corpus" / "estudo12" / "perturbados"])
RE_TITULO_TABELA = re.compile(r"^\s*(table|tabela|tab\.)\s*[\divx]+[^|]*\|\s*", re.I)


def fonte_de(tid, ancora):
    for d in FONTES[ancora]:
        p = d / f"{tid}.txt"
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace")
    return None


def celulas_de(obj, prefixo=""):
    if isinstance(obj, dict):
        if "value" in obj and ("where" in obj or "quote" in obj):
            yield prefixo, obj
            return
        for k, v in obj.items():
            yield from celulas_de(v, f"{prefixo}.{k}" if prefixo else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from celulas_de(v, f"{prefixo}[{i}]")


def corpo_da_citacao(quote):
    """The row part of a 'Table N. title | row' quotation; the whole quotation otherwise."""
    return RE_TITULO_TABELA.sub("", quote or "", count=1)


def n91(quote, src_n):
    q = redes.normaliza(corpo_da_citacao(quote))
    return bool(q) and q in src_n


def n92(valor, quote):
    """Numbers of the value absent from its quotation. Both sides are normalized first (NFKC, dashes unified), so
    a printed en dash or Unicode minus counts as the sign it is — the lesson of the 2026-09-12 grader defect (b).
    Not applied to *_dispersion_type cells: their word is a label the model assigns, judged by N13-1 instead."""
    vn_, qn_ = redes.normaliza(valor), redes.normaliza(quote)
    vn = redes.nums(vn_)
    if vn:
        return [n for n in vn if not redes.num_no_texto(n, qn_)]
    return [] if vn_ in qn_ else [valor]


def n131(tipo_declarado, quote_dispersao):
    """A contradiction between the declared type and the printed form; None when there is none."""
    c = redes.classe_declarada(tipo_declarado)
    q = redes.normaliza(quote_dispersao)
    if not c or not q:
        return None
    tem_intervalo = bool(redes.RE_INTERVALO.search(q))
    tem_spread = bool(redes.RE_SPREAD.search(q))
    if c in ("SD", "SE") and tem_intervalo and not tem_spread:
        return f"declared {c}, the quotation prints an interval"
    if c == "CI" and tem_spread and not tem_intervalo:
        return "declared CI, the quotation prints a ± spread and no interval"
    return None


def flags_da_ficha(js, src):
    """All flags of one parsed v3 sheet against its source text."""
    src_n = redes.normaliza(src)
    cels = dict(celulas_de(js))
    out = []
    for campo, cel in cels.items():
        valor = str(cel.get("value", "") or "").strip()
        quote = str(cel.get("quote", "") or "").strip()
        if valor in ("", "NR"):
            continue
        base = dict(field=campo, value=valor[:60], quote=quote[:140])
        if not quote:
            out.append(dict(net="N9-1", detail="cell filled, quotation empty", **base))
            continue
        if not n91(quote, src_n):
            out.append(dict(net="N9-1", detail="quotation not literal in the source", subclass=redes.sub_classe_n91(corpo_da_citacao(quote), src), **base))
        if campo.endswith("_dispersion_type"):
            faltando = []
        else:
            faltando = n92(valor, quote)
        if faltando:
            out.append(dict(net="N9-2", detail=f"value absent from its own quotation: {faltando}", **base))
        if campo.endswith("_dispersion_type"):
            disp = cels.get(campo[:-len("_type")], {})
            contra = n131(valor, str(disp.get("quote", "") or "") or quote)
            if contra:
                out.append(dict(net="N13-1", detail=contra, **base))
    return out


def roda(modelo, ancora):
    pasta = SAIDAS / ancora / "v3" / modelo
    rel = []
    for p in sorted(pasta.glob("*.json")):
        j = json.loads(p.read_text(encoding="utf-8"))
        src = fonte_de(j["ensaio"], ancora)
        js = h3.acha_json(j.get("conteudo", ""))
        if src is None or not isinstance(js, dict):
            rel.append(dict(trial=j["ensaio"], replicate=j["replica"], net="parse", detail="unreadable sheet or missing source"))
            continue
        for f in flags_da_ficha(js, src):
            rel.append(dict(trial=j["ensaio"], replicate=j["replica"], **f))
    return rel


def self_test():
    src = "Table 2. Changes in HbA1c\nHbA1c (%) 32 weeks –0.8 (–1.1, –0.6) –0.3 (–0.6, 0.0)\nThe change was −1.6±0.3 in the LCD group."
    js = {"experimental_arm": {
        "hba1c_change_mean": {"value": "-0.8", "where": "Table 2", "quote": "Table 2. Changes in HbA1c | HbA1c (%) 32 weeks –0.8 (–1.1, –0.6) –0.3 (–0.6, 0.0)"},
        "hba1c_change_dispersion": {"value": "-1.1 to -0.6", "where": "Table 2", "quote": "Table 2. Changes in HbA1c | HbA1c (%) 32 weeks –0.8 (–1.1, –0.6)"},
        "hba1c_change_dispersion_type": {"value": "SD", "where": "Table 2", "quote": "Table 2. Changes in HbA1c | HbA1c (%) 32 weeks –0.8 (–1.1, –0.6)"},
        "hba1c_final_dispersion": {"value": "0.3", "where": "Results", "quote": "The change was −1.6±0.3 in the LCD group."},
        "hba1c_final_dispersion_type": {"value": "CI95", "where": "Results", "quote": "The change was −1.6±0.3 in the LCD group."},
        "n_analyzed": {"value": "11", "where": "Table 1", "quote": "not in the source at all"}}}
    fl = flags_da_ficha(js, src)
    nets = sorted((f["net"], f["field"].split(".")[-1]) for f in fl)
    esperado = [("N13-1", "hba1c_change_dispersion_type"), ("N13-1", "hba1c_final_dispersion_type"), ("N9-1", "n_analyzed"), ("N9-2", "n_analyzed")]
    ok = nets == esperado
    print("self-test flags:", nets)
    print("TODAS PASSAM." if ok else f"FALHA: esperado {esperado}")
    return ok


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--self-test":
        raise SystemExit(0 if self_test() else 1)
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    r = roda(sys.argv[1], sys.argv[2])
    print(json.dumps(r, ensure_ascii=False, indent=1)[:4000])
    print(f"{len(r)} flags")

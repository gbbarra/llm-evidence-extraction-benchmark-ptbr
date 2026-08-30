# -*- coding: utf-8 -*-
"""EXTRAI Study 3 — post-hoc sensitivity of the Cochrane r=0.5 change-SD imputation.

Reviewer question on preprint v1: is the r=0.5 imputation itself part of the
pipeline-vs-anchor gap? This script recomputes the unperturbation lens —
audited lane-L sheets, sealed perturbations reversed, mechanical pooling,
the exact procedure recorded in avaliacao-estudo3.md — under r = 0.3 / 0.5 /
0.7 in SD_change = sqrt(sd0^2 + sd1^2 - 2*r*sd0*sd1). Startup gate: the
r=0.5 run must reproduce the recorded -0.28 [-0.39, -0.17] digit for digit
before the variants count.

Run: python scripts/estudo3/sensibilidade-r.py
Output: dados/estudo3/sensibilidade-r.json
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


h3 = carrega("h3", "scripts/estudo3/e3-harness.py")
c3 = carrega("c3", "scripts/estudo3/corrigir-e3.py")
selo = json.loads((ROOT / "dados" / "estudo3" / "perturbacoes-estudo3.json").read_text(encoding="utf-8"))


def desperturba(tid, ficha):
    """Reverse the sealed perturbations by literal value substitution."""
    txt = json.dumps(ficha, ensure_ascii=False)
    for reg in selo.get(tid, []):
        p, o = str(reg["perturbado"]), str(reg["original"])
        txt = txt.replace(f'"{p}"', f'"{o}"').replace(f'"-{p}"', f'"-{o}"')
        txt = txt.replace(f" {p}", f" {o}").replace(f"-{p}", f"-{o}")
    return json.loads(txt)


USOS = []


def r_variavel(r):
    def f(dp1, dp2):
        USOS.append((dp1, dp2))
        return round(math.sqrt(dp1 ** 2 + dp2 ** 2 - 2 * r * dp1 * dp2), 2)
    return f


def main():
    assert h3.ELENCO == "base"
    resultado = {}
    for r in (0.3, 0.5, 0.7):
        c3.h3.dp_mudanca_r05 = r_variavel(r)
        USOS.clear()
        sext = []
        for tid in h3.TRIALS:
            res = h3.ficha_auditada(tid, "L")
            f = res[0] if isinstance(res, tuple) else res
            s = c3.sexteto(desperturba(tid, f))
            if s:
                sext.append(s)
        pool = h3.pool_dl_md(sext)
        resultado[f"r={r}"] = dict(agregado=pool, estudos=len(sext), rotas_r05=len(USOS))
        print(f"r={r}: {json.dumps(pool, ensure_ascii=False)} · rotas r05: {len(USOS)}", flush=True)
    g = resultado["r=0.5"]["agregado"]
    assert g["md"] == -0.28 and g["ic95"] == [-0.39, -0.17], f"gate falhou: {g}"
    (ROOT / "dados" / "estudo3" / "sensibilidade-r.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=1), encoding="utf-8")
    print("gate ok: r=0.5 reproduz a lente registrada · gravado dados/estudo3/sensibilidade-r.json", flush=True)


if __name__ == "__main__":
    main()

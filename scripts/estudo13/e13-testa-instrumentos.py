# -*- coding: utf-8 -*-
"""Study 13 instrument tests — run without any model: the corrector's build gate on the anchor-2 key, the routes on
synthetic v3 sheets (CI, SE, SD, baseline/final with SE, Unicode signs), the anchor-3 percentage rule, the nets'
self-test, the hygiene invariant, the sheets' keys and rules, the sealed hashes and the harness plan sizes."""
import importlib.util
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
D13 = RAIZ / "dados" / "estudo13"
falhas = []


def confere(nome, ok, extra=""):
    print(f"  {'ok  ' if ok else 'FALHA'} {nome}{('  ' + extra) if extra else ''}")
    if not ok:
        falhas.append(nome)


def _carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, RAIZ / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


C = _carrega("c13", "scripts/estudo13/e13-corrector.py")
R = _carrega("r13", "scripts/estudo13/e13-redes.py")
HIG = _carrega("hig13", "scripts/estudo13/e13-higiene.py")

print("1. build gate: every derived cell of the anchor-2 key reproduced from its cited inputs")
n, f = C.gate(verbose=False)
confere(f"{n} derived cells reproduced", n >= 12 and not f, "; ".join(f))

print("2. routes on synthetic v3 sheets")


def obj(v, q="q"):
    return {"value": v, "where": "w", "quote": q}


base = dict(n_randomized=obj("12"), n_analyzed=obj("11"))
ci = dict(base, hba1c_change_mean=obj("-0.8"), hba1c_change_dispersion=obj("–1.1 to –0.6"), hba1c_change_dispersion_type=obj("CI95"))
se = dict(base, hba1c_change_mean=obj("-0.35"), hba1c_change_dispersion=obj("0.07"), hba1c_change_dispersion_type=obj("SE"), n_analyzed=obj("45"))
sd = dict(base, hba1c_change_mean=obj("0.54"), hba1c_change_dispersion=obj("1.12"), hba1c_change_dispersion_type=obj("SD"))
bf = dict(base, hba1c_baseline_mean=obj("6.9"), hba1c_baseline_dispersion=obj("1.1"), hba1c_baseline_dispersion_type=obj("SD"),
          hba1c_final_mean=obj("6.0"), hba1c_final_dispersion=obj("0.7"), hba1c_final_dispersion_type=obj("SD"))
bf_se = dict(bf, hba1c_final_dispersion=obj("0.1"), hba1c_final_dispersion_type=obj("SE"), n_analyzed=obj("49"))
iqr = dict(base, hba1c_change_mean=obj("-0.8"), hba1c_change_dispersion=obj("(-1.1, -0.6)"), hba1c_change_dispersion_type=obj("IQR"))
sem_tipo = dict(base, hba1c_change_mean=obj("-0.8"), hba1c_change_dispersion=obj("0.4"), hba1c_change_dispersion_type=obj("NR"))
rev = dict(ci, hba1c_change_dispersion=obj("-0.6 to -1.1"))
mudanca_sem_dp = dict(bf, hba1c_change_mean=obj("-0.9"), hba1c_change_dispersion=obj("NR"), hba1c_change_dispersion_type=obj("NR"))
casos = [("CI with en dash → sd_from_ci 0.42 at n=11", ci, (-0.8, 0.42, 11.0)),
         ("SE → sd_from_se 0.47 at n=45", se, (-0.35, 0.47, 45.0)),
         ("SD as printed", sd, (0.54, 1.12, 11.0)),
         ("baseline/final → change −0.9, sd_change_r05 0.96", bf, (-0.9, 0.96, 11.0)),
         ("baseline SD + final SE → SE converted first (0.1×√49=0.7)", bf_se, (-0.9, 0.96, 49.0)),
         ("IQR → sd not derivable (None)", iqr, (-0.8, None, 11.0)),
         ("dispersion without a type label → not used (None)", sem_tipo, (-0.8, None, 11.0)),
         ("reversed bounds → same sd as ordered", rev, (-0.8, 0.42, 11.0)),
         ("change mean printed, no change SD, baseline/final SDs → r=0.5 fallback", mudanca_sem_dp, (-0.9, 0.96, 11.0))]
for nome, arm, esperado in casos:
    m, s, nn, rotas = C.braco_v3(arm)
    confere(nome, (m, s, nn) == esperado, f"got {(m, s, nn)} · route {rotas['sd']['rule']}")

print("3. anchor 3: deaths from a printed percentage")
confere("20.0% of 30 → 6; 36.6% of 30 → 11", C.mortes_de_percentual("20.0%", "30") == 6 and C.mortes_de_percentual("36.6", 30) == 11)

print("4. provenance nets self-test (table-row quotation accepted; N13-1 fires on contradictions)")
confere("e13-redes self-test", R.self_test())

print("5. hygiene: control characters removed, numbers untouched, PDF-derived anchor-3 texts counted")
kirov = RAIZ / "corpus" / "estudo12" / "perturbados" / "kirov2001.txt"
if kirov.exists():
    s = io.open(kirov, encoding="utf-8").read()
    novo, n = HIG.limpa(s)
    confere("kirov2001: control characters removed and numbers unchanged", n > 0 and HIG.NUMEROS.findall(s) == HIG.NUMEROS.findall(novo), f"{n} removed")
else:
    confere("kirov2001.txt present (corpus regenerates locally)", False)
confere("limpa('a\\x08b') → 'a b', 1", HIG.limpa("a\x08b") == ("a b", 1))

print("6. sheets: keys and rules present")
for anc, chaves, regra in (("a2", ["hba1c_baseline_dispersion_type", "hba1c_final_timepoint", "hba1c_change_dispersion_type"], "TABLE ROW COUNTS AS A QUOTATION"),
                           ("a1", ["n_randomized_gdft", "mortality_control"], "TABLE ROW COUNTS AS A QUOTATION"),
                           ("a3", ["deaths_percent", "n_analyzed"], "TABLE ROW COUNTS AS A QUOTATION")):
    p = D13 / "prompts" / f"{anc}-extraction-v3.txt"
    t = io.open(p, encoding="utf-8").read() if p.exists() else ""
    confere(f"{anc}-extraction-v3.txt has its keys and the table-row rule", all(c in t for c in chaves) and regra in t and "Never compute" in t)

print("7. seals and harness plan (dry, no model)")
sel = D13 / "fichas.sha256"
confere("fichas.sha256 exists with three seals", sel.exists() and sum(1 for l in io.open(sel, encoding="utf-8") if l and not l.startswith("#") and l.strip()) == 3)
HR = _carrega("h13", "scripts/estudo13/e13-harness.py")
HR._ativas[:] = ["a2"]
confere("P1-A plan = 84 calls", sum(1 for _ in HR.plano_v3()) == 84)
HR._ativas[:] = ["a1", "a3"]
confere("P1-B plan = 264 calls", sum(1 for _ in HR.plano_v3()) == 264)
confere("harness refuses a real run before registration", not HR.registrado())
confere("v3 sheets match their seals", HR.confere_fichas_v3() == 3)

print()
if falhas:
    raise SystemExit("FALHAS: " + "; ".join(falhas))
print("TODAS PASSAM.")

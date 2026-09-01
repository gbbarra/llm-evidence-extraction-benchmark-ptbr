# -*- coding: utf-8 -*-
"""Study 7 / Amendment 1 — detection nets over the deterministic downstream.

Study 5's doctrine ported to the sheet layer (registered in the protocol
BEFORE this run): nets detect and warn, NEVER substitute a value. The primary
H7.3 record stands as measured; this script only emits flags.

N7-1: declared dispersion type vs the form printed around the located mean
      in the ORIGINAL text (MA-2 sheets, replicate 1).
N7-2: DerSimonian-Laird weight share per study (> 40% flags; pools of <= 2
      studies exceed it structurally and are reported, not counted).

Run: python scripts/estudo7/e7-redes.py
Outputs: dados/estudo7/redes-deteccao.md · redes-deteccao.json
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
E7 = ROOT / "dados" / "estudo7"
TXT2 = ROOT / "corpus" / "estudo3" / "primarios-texto"


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


h3 = carrega("h3", "scripts/estudo3/e3-harness.py")

RES2 = json.loads((E7 / "resultados-ma2.json").read_text(encoding="utf-8"))
RES1 = json.loads((E7 / "resultados-por-desfecho.json").read_text(encoding="utf-8"))

NUM = r"-?\d+(?:\.\d+)?"
# interval printed forms: (a ~ b) · (a to b) · (a, b) · (a – b) after a mean
RE_INTERVAL = re.compile(rf"({NUM})\s*\(\s*({NUM})\s*(?:~|,|to|–|-|a)\s*({NUM})\s*\)")
# single-spread printed forms: m ± s · m (s)
RE_SPREAD = re.compile(rf"({NUM})\s*(?:±\s*({NUM})|\(\s*({NUM})\s*\))")


def norm(t):
    return t.replace("−", "-").replace("–", "-")


def formas_no_texto(texto, alvo, tol=0.055):
    """All printed dispersion forms whose leading mean ≈ alvo."""
    achadas = []
    for m in RE_INTERVAL.finditer(texto):
        if abs(float(m.group(1)) - alvo) <= tol:
            achadas.append(("interval", float(m.group(2)), float(m.group(3)), m.group(0)))
    for m in RE_SPREAD.finditer(texto):
        if abs(float(m.group(1)) - alvo) <= tol:
            s = m.group(2) or m.group(3)
            achadas.append(("spread", float(s), None, m.group(0)))
    return achadas


def classe_declarada(tipo):
    t = str(tipo or "").strip().upper()
    if t.startswith(("CI", "IC")):
        return "interval"
    if t in ("SD", "DP", "SE", "EP"):
        return "spread"
    return None


def n7_1():
    flags, linhas = [], []
    for tid, rot in h3.ROT.items():
        js = None
        for rep in (1, 2):  # first-parseable, the same rule the downstream used
            f = E7 / "saidas" / "gemma12" / "ma2" / f"{tid}-r{rep}.json"
            js = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
            if js:
                if rep == 2:
                    print(f"  note: {tid} r1 not parseable, net reads r2 (as the downstream did)")
                break
        if not js:
            linhas.append((rot, "—", "—", "no parseable sheet", ""))
            continue
        texto = norm((TXT2 / f"{tid}.txt").read_text(encoding="utf-8", errors="replace"))
        for arm_en, rot_arm in (("experimental_arm", "exp"), ("control_arm", "ctl")):
            b = js.get(arm_en) or {}
            tipo = b.get("hba1c_change_dispersion_type")
            cls = classe_declarada(tipo)
            m = b.get("hba1c_change_mean")
            try:
                alvo = float(norm(str(m)))
            except (TypeError, ValueError):
                linhas.append((rot, rot_arm, tipo, "no declared change mean — net skipped", ""))
                continue
            if cls is None:
                linhas.append((rot, rot_arm, tipo, "no declared type — net skipped", ""))
                continue
            achadas = formas_no_texto(texto, alvo)
            if not achadas:
                linhas.append((rot, rot_arm, tipo, "mean not located in text — not flagged", ""))
                continue
            ivs = [a for a in achadas if a[0] == "interval"]
            sps = [a for a in achadas if a[0] == "spread"]
            coerente = any(a[0] == cls for a in achadas)
            # N7-1b (Amendment 2): both forms printed at the same mean and the
            # spread equals the interval's half-width -> the ± is the CI in
            # disguise; an SD/SE declaration over it is mechanically suspect.
            if cls == "spread" and ivs and sps:
                meia = round(abs(ivs[0][2] - ivs[0][1]) / 2, 2)
                casam = [s for s in sps if abs(s[1] - meia) <= 0.06]
                if casam:
                    flag = dict(trial=tid, study=rot, arm=rot_arm, declared=str(tipo),
                                printed=f"{ivs[0][3]} and {casam[0][3]}",
                                detail=f"printed ± {casam[0][1]} equals the printed "
                                       f"interval's half-width {meia} (N7-1b)")
                    flags.append(flag)
                    linhas.append((rot, rot_arm, tipo,
                                   "FLAG (N7-1b) — ± equals the CI half-width",
                                   f"{ivs[0][3]} · {casam[0][3]}"))
                    continue
            if coerente:
                linhas.append((rot, rot_arm, tipo, "coherent with a printed form", achadas[0][3]))
                continue
            det = ""
            if cls == "spread" and ivs:
                meia = round(abs(ivs[0][2] - ivs[0][1]) / 2, 2)
                disp = b.get("hba1c_change_dispersion")
                try:
                    if abs(float(norm(str(disp))) - meia) <= 0.06:
                        det = (f"declared value {disp} equals the printed interval's "
                               f"half-width {meia}")
                except (TypeError, ValueError):
                    pass
            flag = dict(trial=tid, study=rot, arm=rot_arm, declared=str(tipo),
                        printed=achadas[0][3], detail=det)
            flags.append(flag)
            linhas.append((rot, rot_arm, tipo,
                           f"FLAG (N7-1) — declared {cls}, text prints interval only",
                           achadas[0][3]))
    return flags, linhas


def pesos_dl_md(sextetos, tau2):
    v = [s[1] ** 2 / s[2] + s[4] ** 2 / s[5] for s in sextetos]
    w = [1 / (vi + tau2) for vi in v]
    tot = sum(w)
    return [round(100 * wi / tot, 1) for wi in w]


def pesos_dl_rr(quads, tau2):
    # quads = (a, n1, c, n2); +0.5 continuity when any zero cell (reporting only)
    ps = []
    for a, n1, c, n2 in quads:
        if 0 in (a, c, n1 - a, n2 - c):
            a, c, n1, n2 = a + 0.5, c + 0.5, n1 + 1, n2 + 1
        ps.append(1 / a - 1 / n1 + 1 / c - 1 / n2)
    w = [1 / (v + tau2) for v in ps]
    tot = sum(w)
    return [round(100 * wi / tot, 1) for wi in w]


def n7_2():
    saida = []
    # MA-2
    ests = [e for e in RES2["por_estudo"]]
    shares = pesos_dl_md([e["sexteto"] for e in ests], RES2["pool"]["tau2"])
    saida.append(dict(pool="MA-2 HbA1c MD", n_estudos=len(ests), estrutural=len(ests) <= 2,
                      shares=[dict(study=e["estudo"], pct=p) for e, p in zip(ests, shares)],
                      flags=[e["estudo"] for e, p in zip(ests, shares) if p > 40]))
    # MA-1 dichotomous pools
    for fam in ("morbidity", "mortality", "ileus"):
        rows = [l for l in RES1[fam]["rows"] if l.get("pmcid")]
        quads, nomes = [], []
        for l in rows:
            m = re.search(r"a=(\d+)/(\d+), c=(\d+)/(\d+)", l["ours"])
            if m:
                quads.append(tuple(int(x) for x in m.groups()))
                nomes.append(l["study"])
        pool = (RES1[fam].get("pool") or {}).get("DL")
        if not pool or len(quads) < 2:
            continue
        shares = pesos_dl_rr(quads, pool["tau2"])
        saida.append(dict(pool=f"MA-1 {fam} RR", n_estudos=len(quads),
                          estrutural=len(quads) <= 2,
                          shares=[dict(study=n, pct=p) for n, p in zip(nomes, shares)],
                          flags=[n for n, p in zip(nomes, shares) if p > 40]))
    return saida


def main():
    flags1, linhas1 = n7_1()
    pools = n7_2()
    L = ["# Study 7 / Amendment 1 — detection nets, run record",
         "",
         "Nets registered in the protocol BEFORE this run. Doctrine: detect and warn, "
         "never substitute. The primary H7.3 record is unchanged by anything below.",
         "",
         "## N7-1 — declared dispersion type vs the form printed at the located mean (MA-2, r1 sheets)",
         "",
         "| study | arm | declared type | net verdict | printed form at the mean |",
         "|---|---|---|---|---|"]
    for rot, arm, tipo, verd, forma in linhas1:
        L.append(f"| {rot} | {arm} | {tipo} | {verd} | {forma} |")
    L += ["", f"**Flags: {len(flags1)}**"]
    for fl in flags1:
        L.append(f"- **{fl['study']} · {fl['arm']}** — declared \"{fl['declared']}\", "
                 f"text prints `{fl['printed']}`"
                 + (f"; {fl['detail']}" if fl['detail'] else ""))
    L += ["", "## N7-2 — DerSimonian–Laird weight shares (> 40% flags; ≤2-study pools structural)", ""]
    for p in pools:
        det = " · ".join(f"{s['study']} {s['pct']}%" for s in p["shares"])
        fl = (f" → **FLAG: {', '.join(p['flags'])}**" if p["flags"] and not p["estrutural"]
              else (" → exceeds 40% structurally (≤2 studies), not counted"
                    if p["flags"] else " → no flag"))
        L.append(f"- **{p['pool']}** ({p['n_estudos']} studies): {det}{fl}")
    (E7 / "redes-deteccao.json").write_text(
        json.dumps(dict(n7_1_flags=flags1, n7_2=pools), ensure_ascii=False, indent=1),
        encoding="utf-8")
    (E7 / "redes-deteccao.md").write_text("\n".join(L), encoding="utf-8")
    print(f"N7-1 flags: {len(flags1)}")
    for fl in flags1:
        print(f"  FLAG {fl['study']} {fl['arm']}: declared {fl['declared']} | "
              f"printed {fl['printed']} | {fl['detail']}")
    for p in pools:
        print(f"N7-2 {p['pool']}: " + ", ".join(f"{s['study']} {s['pct']}%" for s in p["shares"])
              + (f" -> FLAG {p['flags']}" if p["flags"] else ""))


if __name__ == "__main__":
    main()

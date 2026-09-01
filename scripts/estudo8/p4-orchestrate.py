# -*- coding: utf-8 -*-
"""Study 8 / P4 ORCHESTRATE (protocol §3): gemma12 under the ENGLISH harness
build (e8-harness-en, the ten-net port), over its OWN P3-b English sheets.
One formal pipeline: per-study typed calls -> pooling -> product coherence
check -> synthesis with orphan check. Grader-side comparison (truth over the
same sheets; the sealed lens; the published value) happens only afterward.

Run: python scripts/estudo8/p4-orchestrate.py    (resume-safe)
Outputs: dados/estudo8/p4/{calc,pool.json,resumo.json,sintese.md}
"""
import importlib.util
import json
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
E8 = ROOT / "dados" / "estudo8"
P4 = E8 / "p4"
MODELO = "gemma12"


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


hen = carrega("hen", "scripts/estudo8/e8-harness-en.py")
e7d = carrega("e7d", "scripts/estudo7/e7-downstream.py")
p3 = carrega("p3", "scripts/estudo8/p3-avalia.py")
h3 = hen.h3


def ficha_en(tid):
    for rep in (1, 2):
        f = E8 / "saidas" / "p3b" / MODELO / f"{tid}-r{rep}.json"
        js = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
        if js:
            return js
    return None


def main():
    P4.mkdir(exist_ok=True)
    calc_dir = P4 / "calc"
    t0 = time.time()

    print("===== P4 · stage 1: per-study typed calls under the EN ten-net harness", flush=True)
    base = (E8 / "prompts" / "e5-calc2.txt").read_text(encoding="utf-8")
    for tid in h3.TRIALS:
        if (calc_dir / f"{tid}.json").exists():
            print(f"  skip {tid}", flush=True)
            continue
        hen.roda_estudo(calc_dir, tid, base, ficha_en(tid), h3.ROT[tid])

    print("\n===== P4 · stage 2: pooling (G3 instrument)", flush=True)
    proprios = hen.sextetos_de(calc_dir, h3.TRIALS, h3.ROT)
    if (P4 / "pool.json").exists():
        pool_reg = json.loads((P4 / "pool.json").read_text(encoding="utf-8"))
        print("  skip pool (exists)", flush=True)
    else:
        base_g3 = (E8 / "prompts" / "e5-g3.txt").read_text(encoding="utf-8")
        pool_reg = hen.roda_g3(base_g3, proprios, P4 / "pool.json")

    print("\n===== P4 · stage 3: product coherence check + synthesis", flush=True)
    linhas, total_n, incoerentes = [], 0, []
    for rot, d in proprios.items():
        s = d["sexteto"]
        n = int(s[2] + s[5])
        total_n += n
        f = d["final"] or {}
        ic = f.get("ic95")
        coerente = bool(ic) and f.get("md") is not None and ic[0] - 1e-9 <= f["md"] <= ic[1] + 1e-9
        if not coerente:
            incoerentes.append(rot)
        linhas.append(f"- {rot}: MD {f.get('md')} CI95 {ic} · participants: {n}"
                      + ("" if coerente else " · REPORTED CI INVALID (does not contain its own MD; do not use)"))
    print(f"  incoherent reported CIs (flagged, never endorsed): {incoerentes or 'none'}", flush=True)
    ag = pool_reg.get("final") or pool_reg["pool_sobre_os_proprios_sextetos"]
    i2 = pool_reg["pool_sobre_os_proprios_sextetos"].get("i2_pct")
    dados = ("POOLED (DerSimonian-Laird): MD " + str(ag.get("md")) + " CI95 " + str(ag.get("ic95"))
             + f" · I2 = {i2}%\nSTUDIES: {len(proprios)} · TOTAL PARTICIPANTS: {total_n}\n"
             + "\n".join(linhas))
    if (P4 / "sintese.md").exists():
        sintese = (P4 / "sintese.md").read_text(encoding="utf-8").split("\n\n", 1)[-1].strip()
    else:
        prompt = (E8 / "prompts" / "e5-synthesis.txt").read_text(encoding="utf-8").replace("{DATA}", dados)
        r = h3.gerar(MODELO, prompt, max_tokens=600)
        sintese = r["content"].strip()
    fornecidos = set(re.findall(r"-?\d+(?:\.\d+)?", dados.replace("−", "-")))
    orfaos = [x for x in re.findall(r"-?\d+(?:[.,]\d+)?", sintese.replace("−", "-"))
              if x.replace(",", ".") not in fornecidos
              and x.replace(",", ".").lstrip("-") not in fornecidos
              and not re.fullmatch(r"\d{1,2}|95|150|300", x)]
    print(f"  orphans: {orfaos if orfaos else 'ZERO'}", flush=True)

    print("\n===== grader-side (AFTER the run; no model stage saw a key)", flush=True)
    sx_det, sx_lens = [], []
    for tid in h3.TRIALS:
        js = ficha_en(tid)
        fpt = e7d.ficha_ma2_pt(js)
        s = p3.sexteto_de(fpt)
        if s:
            sx_det.append(s)
        sl = p3.sexteto_de(p3.lens_sexteto(fpt, tid))
        if sl:
            sx_lens.append(sl)
    verdade = h3.pool_dl_md(sx_det)
    lens = h3.pool_dl_md(sx_lens)
    resumo = dict(agregado_do_modelo=ag, verdade_mecanica=verdade,
                  delta_md=round(abs(ag["md"] - verdade["md"]), 2),
                  lens_desperturbada=lens, publicado=p3.PUB2,
                  flags_coerencia=incoerentes, consistente=pool_reg["consistente"],
                  avisos_por_estudo={r: d.get("final", {}) and None for r, d in proprios.items()},
                  numeros_orfaos=orfaos, sintese=sintese,
                  minutos=round((time.time() - t0) / 60, 1))
    resumo.pop("avisos_por_estudo")
    (P4 / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1),
                                    encoding="utf-8")
    (P4 / "sintese.md").write_text("# Synthesis — P4 EN-harness run (100% gemma4:12b)\n\n"
                                   + sintese + "\n", encoding="utf-8")
    print(f"  model pool: {json.dumps(ag)} · mechanical truth: {json.dumps(verdade)} · "
          f"delta {resumo['delta_md']}", flush=True)
    print(f"  LENS: {json.dumps(lens)} vs published -0.24 [-0.32, -0.16]", flush=True)
    print(f"\n== P4 COMPLETE in {resumo['minutos']} min · consistent: {pool_reg['consistente']} · "
          f"orphans: {len(orfaos)}", flush=True)


if __name__ == "__main__":
    main()

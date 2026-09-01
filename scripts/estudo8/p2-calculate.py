# -*- coding: utf-8 -*-
"""Study 8 / P2 CALCULATE (protocol §3): the Study-2 replication under ENGLISH
instruments — each model, over its OWN P1 sheets, computes MDs, RRs and pools,
arm A (unaided) vs arm B (text-protocol calculator).

Mirrors the frozen Study-2 design verbatim: 3 families (rr, md, pool) x 2 arms
x 2 replicates; arm B up to 5 rounds and 20 CALC calls; the harness executes
each CALC line and returns "RESULT: ..." in context. Math functions are the
validated Study-2 engine, addressed by the English names of the frozen prompts
(ci95_md -> ic95_md etc., per the instrument library's correspondence table).

Run: python scripts/estudo8/p2-calculate.py [model ...]
Outputs: dados/estudo8/saidas/p2/<model>/<family>-<arm>-r{1,2}.json
"""
import importlib.util
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
E8 = ROOT / "dados" / "estudo8"
CAST = ["gemma12", "qwen14", "llama8", "qwen35", "deepseek14"]


def carrega(nome, rel):
    sp = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


e2 = carrega("e2", "scripts/estudo2/e2-harness.py")
ext = carrega("ext", "scripts/estudo4/e4-extensao.py")
h3 = ext.h3  # five-model registry

FN = {"rr": e2.rr, "ci95_rr": e2.ic95_rr, "md": e2.md, "ci95_md": e2.ic95_md,
      "pool_rr_mh": e2.pool_rr_mh, "pool_dl": e2.pool_dl, "pool_md_iv": e2.pool_md_iv}

CAMPOS_FAM = {
    "rr": [("morbidity", "morbidity_events_gdft", "morbidity_events_control"),
           ("mortality", "mortality_gdft", "mortality_control"),
           ("ileus", "postop_ileus_gdft", "postop_ileus_control")],
    "md": [("time_to_flatus_h", "time_to_flatus_gdft", "time_to_flatus_control"),
           ("time_to_oral_diet", "time_to_oral_intake_gdft", "time_to_oral_intake_control")],
}


def descarrega(tag=None):
    tags = [tag] if tag else sorted({m["ollama"] for m in h3.MODELS.values()})
    for t in tags:
        subprocess.run(["ollama", "stop", t], capture_output=True)


def executa_calc_en(linha):
    m = re.match(r"\s*CALC:\s*([a-z0-9_]+)\s*\((.*)\)\s*$", linha.strip(), re.I)
    if not m:
        return None
    nome, args = m.group(1).lower(), m.group(2).strip()
    fn = FN.get(nome)
    if not fn:
        return f"RESULT: error — unknown function '{nome}'"
    try:
        vals = json.loads(f"[{args}]")
        res = fn(*vals)
        return f"RESULT: {json.dumps(res, ensure_ascii=False)}"
    except Exception as e:
        return f"RESULT: error — {str(e)[:80]}"


def ficha_p1(mod, pm):
    for rep in (1, 2):
        f = E8 / "saidas" / "p1" / mod / f"{pm}-r{rep}.json"
        if not f.exists():
            continue
        js = e2.__dict__.get("acha_json")
        t = json.loads(f.read_text(encoding="utf-8"))["content"]
        t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t.strip())
        mm = re.search(r"\{.*\}", t, re.S)
        if mm:
            try:
                return json.loads(mm.group(0))
            except Exception:
                continue
    return {}


def cel(js, campo):
    v = js.get(campo)
    if isinstance(v, dict):
        v = v.get("value")
    return "NR" if v in (None, "") else str(v)


def bloco_insumo(mod, familia):
    por = e2.estudos_por_desfecho()
    mapa = {"morbidade": "morbidity", "mortalidade": "mortality", "ileo": "ileus",
            "tempo_flatus_h": "time_to_flatus_h", "tempo_dieta_oral": "time_to_oral_diet"}
    alvo = CAMPOS_FAM["rr"] + CAMPOS_FAM["md"] if familia == "pool" else CAMPOS_FAM[familia]
    linhas = []
    for desfecho, c_g, c_c in alvo:
        linhas.append(f"\n## Outcome: {desfecho}")
        pt_key = next(k for k, v in mapa.items() if v == desfecho)
        for pm in por[pt_key]:
            j = ficha_p1(mod, pm)
            linhas.append(f"- {e2.ROT[pm]}: GDFT events/value = {cel(j, c_g)} | "
                          f"control = {cel(j, c_c)} | n GDFT = {cel(j, 'n_randomized_gdft')} | "
                          f"n control = {cel(j, 'n_randomized_control')}")
    return "\n".join(linhas)


def corrida(mod, familia, braco, rep):
    out = E8 / "saidas" / "p2" / mod / f"{familia}-{braco}-r{rep}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        print(f"  skip {mod} {familia}-{braco}-r{rep}", flush=True)
        return
    tpl = (E8 / "prompts" / f"{familia}-{braco}.txt").read_text(encoding="utf-8")
    prompt = tpl.replace("{DATA}", bloco_insumo(mod, familia))
    transcricao, total_dt, chamadas = [], 0.0, 0
    for rodada in range(1, 6 if braco == "B" else 2):
        r = h3.gerar(mod, prompt, max_tokens=1600)
        total_dt += r["dt"]
        transcricao.append(dict(rodada=rodada, saida=r["content"], dt=round(r["dt"], 1)))
        if braco == "A":
            break
        calcs = [ln for ln in r["content"].splitlines() if re.match(r"\s*CALC:", ln, re.I)]
        if not calcs:
            break
        respostas = []
        for ln in calcs[:20 - chamadas]:
            res = executa_calc_en(ln)
            if res:
                respostas.append(ln.strip() + "\n" + res)
                chamadas += 1
        if not respostas or chamadas >= 20:
            break
        prompt = prompt + "\n\n[YOUR PREVIOUS ROUND]\n" + r["content"] + \
            "\n\n[RESULTS OF YOUR CALLS]\n" + "\n".join(respostas) + \
            "\n\nContinue: use the RESULTS above. If you need more calculations, write new " \
            "CALC: lines. When you have everything, answer with the final JSON."
    out.write_text(json.dumps(dict(modelo=mod, familia=familia, braco=braco, replica=rep,
                                   chamadas=chamadas, dt=round(total_dt, 1),
                                   rodadas=len(transcricao), transcricao=transcricao),
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {mod} {familia}-{braco}-r{rep}: {len(transcricao)} round(s), "
          f"{chamadas} CALC, {total_dt:.0f}s", flush=True)


def main():
    alvo = sys.argv[1:] or CAST
    print("initial memory sweep:", flush=True)
    descarrega()
    t0 = time.time()
    anterior = None
    for mod in alvo:
        if anterior:
            descarrega(h3.MODELS[anterior]["ollama"])
        print(f"\n===== Study 8 · P2 CALCULATE · {mod} [{h3.MODELS[mod]['ollama']}]", flush=True)
        for familia in ("rr", "md", "pool"):
            for braco in ("A", "B"):
                for rep in (1, 2):
                    corrida(mod, familia, braco, rep)
        anterior = mod
    if anterior:
        descarrega(h3.MODELS[anterior]["ollama"])
    print(f"\n== P2 CALCULATE COMPLETE in {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()

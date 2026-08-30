# -*- coding: utf-8 -*-
"""EXTRAI Study 4 — Amendment-2 round 2: continuous-flow replication, five extractors.

One uninterrupted queue re-extracts everything from zero — gemma4:12b,
qwen3:14b, llama3.1:8b, qwen3.5:9b, deepseek-r1:14b — under uniform
instruments: the frozen extraction prompt, num_predict 4000, and the
Amendment-1 trigger set (E4-1 neutral sign question; E4-2 all three
classes), reused verbatim from e4-extensao.py. Memory hygiene per the
author's directive: every resident Ollama model is unloaded at start and
the previous model is unloaded between blocks (one resident at a time).

Outputs under dados/estudo4/rodada2/ — round 1's published record is never
touched. Resume-safe: re-running skips completed extractions.

Run: python scripts/estudo4/e4-rodada2.py [modelo...]   (default: all 5)
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
D3 = ROOT / "dados" / "estudo3"
R2 = ROOT / "dados" / "estudo4" / "rodada2"
PERT = ROOT / "corpus" / "estudo3" / "perturbados"

_x = importlib.util.spec_from_file_location("ext", ROOT / "scripts" / "estudo4" / "e4-extensao.py")
ext = importlib.util.module_from_spec(_x)
_x.loader.exec_module(ext)
h3, dg = ext.h3, ext.dg  # extension models already injected by ext

MODELOS_R2 = ["gemma12", "qwen14", "llama8", "qwen35", "deepseek14"]
MAXTOK = 4000  # Amendment-2: uniform allowance for all five


def descarrega(tag=None):
    """Unload one Ollama model, or every model this study knows."""
    tags = [tag] if tag else sorted({m["ollama"] for m in h3.MODELS.values()})
    for t in tags:
        subprocess.run(["ollama", "stop", t], capture_output=True)
    r = subprocess.run(["ollama", "ps"], capture_output=True, text=True)
    residentes = [l.split()[0] for l in r.stdout.strip().splitlines()[1:] if l.strip()]
    print(f"  memoria: descarregado {tags if tag else 'tudo'} · residentes agora: {residentes or 'nenhum'}", flush=True)


def extrai(modelo):
    base = h3.prompt_txt("e3-extracao.txt")
    out_dir = R2 / "saidas" / modelo / "extracao"
    out_dir.mkdir(parents=True, exist_ok=True)
    for tid in h3.TRIALS:
        for rep in (1, 2):
            out = out_dir / f"{tid}-r{rep}.json"
            if out.exists():
                print(f"  pulando extracao {modelo} {tid}-r{rep}", flush=True)
                continue
            texto = (PERT / f"{tid}.txt").read_text(encoding="utf-8")
            r = h3.gerar(modelo, base + texto, max_tokens=MAXTOK)
            out.write_text(json.dumps(dict(modelo=modelo, trial=tid, replica=rep, **r),
                                      ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  extracao {modelo} {tid}-r{rep}: {r['dt']:.0f}s, {r['tokens']} tok", flush=True)


def ficha_r2(modelo, tid):
    for rep in (1, 2):
        f = R2 / "saidas" / modelo / "extracao" / f"{tid}-r{rep}.json"
        if not f.exists():
            continue
        js = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
        if js:
            return js, rep
    return None, None


def concordancia_r2(modelo, tid):
    js = []
    for rep in (1, 2):
        f = R2 / "saidas" / modelo / "extracao" / f"{tid}-r{rep}.json"
        if f.exists():
            j = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
            js.append(json.dumps(j, ensure_ascii=False, sort_keys=True) if j else None)
    if len(js) == 2 and all(js):
        return js[0] == js[1]
    return None


def downstream(modelo):
    fichas = {}
    reps = {}
    for tid in h3.TRIALS:
        f, rep = ficha_r2(modelo, tid)
        if f:
            fichas[h3.ROT[tid]] = f
            reps[h3.ROT[tid]] = rep
    registro = []

    # class 1 — as-printed positive change (neutral question, E4-1)
    julg = {}
    for p in dg.gatilhos(fichas):
        r = h3.gerar(modelo, ext.pergunta_sinal_neutra(p), max_tokens=40)
        m = re.search(r"-?\d+(?:\.\d+)?", r["content"])
        usado = float(m.group(0)) if m else p["valor"]
        julg[(p["estudo"], p["lado"])] = usado
        registro.append(dict(classe="sinal-como-impresso", estudo=p["estudo"], lado=p["lado"],
                             valor_na_ficha=p["valor"], resposta=r["content"].strip()[:80], valor_usado=usado))
        print(f"  gatilho sinal {modelo} {p['estudo']} {p['lado']}: {p['valor']} -> {usado}", flush=True)

    # class 2 — factorial margins (fired by the sheet's declared design)
    for rot, fs in list(fichas.items()):
        if not re.search(r"fatorial|factorial|2\s*[x×]\s*2", str(fs.get("desenho", "")), re.I):
            continue
        r = h3.gerar(modelo, ext.pergunta_fatorial(rot, fs), max_tokens=60)
        resp = r["content"].strip()
        m = re.search(r"exp\s*=\s*(\d+)\D+ctl\s*=\s*(\d+)", resp, re.I)
        if m:
            fs = json.loads(json.dumps(fs))
            fs["braco_experimental"]["n_analisado"] = m.group(1)
            fs["braco_controle"]["n_analisado"] = m.group(2)
            fichas[rot] = fs
        registro.append(dict(classe="fatorial-margens", estudo=rot, resposta=resp[:80],
                             ns_usados=[m.group(1), m.group(2)] if m else None))
        print(f"  gatilho fatorial {modelo} {rot}: {resp[:60]}", flush=True)

    # arms + class 3 — required-field NR (sheet-scoped)
    NOMES = ("media", "dp", "n")
    por_estudo = []
    sextetos = []
    for rot, fs in fichas.items():
        bracos = {}
        for lado in ("braco_experimental", "braco_controle"):
            b = fs.get(lado, {})
            trio = list(dg.braco_deterministico(b, julg, (rot, lado)))
            if None in trio:
                faltam = [NOMES[i] for i, v in enumerate(trio) if v is None]
                r = h3.gerar(modelo, ext.pergunta_nr(rot, lado, b, faltam), max_tokens=120)
                js = h3.acha_json(r["content"]) or {}
                for i, nome in enumerate(NOMES):
                    if trio[i] is None and isinstance(js, dict) and js.get(nome) is not None:
                        try:
                            trio[i] = float(js[nome])
                        except (TypeError, ValueError):
                            pass
                registro.append(dict(classe="campo-faltante", estudo=rot, lado=lado, faltavam=faltam,
                                     resposta=r["content"].strip()[:80],
                                     preenchidos={n: trio[i] for i, n in enumerate(NOMES) if n in faltam and trio[i] is not None}))
                print(f"  gatilho NR {modelo} {rot} {lado}: faltavam {faltam} -> {trio}", flush=True)
            bracos[lado] = trio
        e, c = bracos["braco_experimental"], bracos["braco_controle"]
        if None in e or None in c:
            por_estudo.append(dict(estudo=rot, status="dados-insuficientes", exp=e, ctl=c))
            continue
        s = [e[0], e[1], e[2], c[0], c[1], c[2]]
        sextetos.append(s)
        por_estudo.append(dict(estudo=rot, md=h3.md(*s), ic95=h3.ic95_md(*s), sexteto=s,
                               replica_usada=reps[rot],
                               replicas_identicas=concordancia_r2(
                                   modelo, next(t for t, r2 in h3.ROT.items() if r2 == rot))))
    pool = h3.pool_dl_md(sextetos) if sextetos else None
    resultado = dict(modelo=modelo, arm="rodada2-emenda2", estudos_no_pool=len(sextetos),
                     gatilhos=registro, por_estudo=por_estudo, agregado=pool)
    (R2 / "resultados").mkdir(parents=True, exist_ok=True)
    (R2 / "resultados" / f"{modelo}.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"== {modelo}: {len(sextetos)}/7 estudos no pool · gatilhos: {len(registro)}", flush=True)
    print(f"   agregado: {json.dumps(pool, ensure_ascii=False)}", flush=True)
    return resultado


def main():
    assert h3.ELENCO == "base"
    alvo = sys.argv[1:] or MODELOS_R2
    for selo in ("perturbacoes-estudo3.json", "sementes-auditoria.json"):
        p = D3 / selo
        if p.exists():
            print(f"SHA-256 {selo}: {hashlib.sha256(p.read_bytes()).hexdigest()}", flush=True)
    print("limpeza inicial de memoria:", flush=True)
    descarrega()
    t0 = time.time()
    anterior = None
    for modelo in alvo:
        if anterior:
            descarrega(h3.MODELS[anterior]["ollama"])
        print(f"\n===== Estudo 4 · rodada 2 (Emenda 2) · {modelo} [{h3.MODELS[modelo]['ollama']}]", flush=True)
        extrai(modelo)
        downstream(modelo)
        anterior = modelo
    descarrega(h3.MODELS[anterior]["ollama"]) if anterior else None
    print(f"\nRodada 2 completa em {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()

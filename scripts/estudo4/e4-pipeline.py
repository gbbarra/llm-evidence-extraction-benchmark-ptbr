# -*- coding: utf-8 -*-
"""EXTRAI Study 4 — extraction plus deterministic harness (Paper 2's record).

Per model: (1) fresh Stage-E extraction of the 7 perturbed texts x 2
replicates under the frozen Study-3 instrument; (2) the Amendment-8
deterministic engine computes per-study MD/CI and the DL pool from the
first-parseable sheets; judgment triggers, if any fire, are answered by the
SAME model (one narrow question each, logged).

Run: python scripts/estudo4/e4-pipeline.py [gemma12|qwen14|...]
     (no arg = all registered models). Resume-safe.
Outputs: dados/estudo4/saidas/<modelo>/extracao/, dados/estudo4/resultados/.
"""
import hashlib
import importlib.util
import json
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
D3 = ROOT / "dados" / "estudo3"
D4 = ROOT / "dados" / "estudo4"
PERT = ROOT / "corpus" / "estudo3" / "perturbados"

_h = importlib.util.spec_from_file_location("h3", ROOT / "scripts" / "estudo3" / "e3-harness.py")
h3 = importlib.util.module_from_spec(_h)
_h.loader.exec_module(h3)
_d = importlib.util.spec_from_file_location("dg", ROOT / "scripts" / "estudo3" / "dirigida.py")
dg = importlib.util.module_from_spec(_d)
_d.loader.exec_module(dg)

MODELOS_E4 = ["gemma12", "qwen14"]


def extrai(modelo):
    base = h3.prompt_txt("e3-extracao.txt")
    out_dir = D4 / "saidas" / modelo / "extracao"
    out_dir.mkdir(parents=True, exist_ok=True)
    for tid in h3.TRIALS:
        for rep in (1, 2):
            out = out_dir / f"{tid}-r{rep}.json"
            if out.exists():
                print(f"  pulando extracao {modelo} {tid}-r{rep}", flush=True)
                continue
            texto = (PERT / f"{tid}.txt").read_text(encoding="utf-8")
            r = h3.gerar(modelo, base + texto, max_tokens=2000)
            out.write_text(json.dumps(dict(modelo=modelo, trial=tid, replica=rep, **r),
                                      ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  extracao {modelo} {tid}-r{rep}: {r['dt']:.0f}s, {r['tokens']} tok", flush=True)


def ficha_e4(modelo, tid):
    for rep in (1, 2):
        f = D4 / "saidas" / modelo / "extracao" / f"{tid}-r{rep}.json"
        if not f.exists():
            continue
        js = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
        if js:
            return js, rep
    return None, None


def concordancia_replicas(modelo, tid):
    """Cell-identity between the two replicates (Study-3 bar: 100%)."""
    js = []
    for rep in (1, 2):
        f = D4 / "saidas" / modelo / "extracao" / f"{tid}-r{rep}.json"
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
        f, rep = ficha_e4(modelo, tid)
        if f:
            fichas[h3.ROT[tid]] = f
            reps[h3.ROT[tid]] = rep
    pontos = dg.gatilhos(fichas)
    julg = {}
    registro = []
    for p in pontos:
        q = dg.pergunta_sinal(p)
        r = h3.gerar(modelo, q, max_tokens=40)
        m = re.search(r"-?\d+(?:\.\d+)?", r["content"])
        usado = float(m.group(0)) if m else p["valor"]
        julg[(p["estudo"], p["lado"])] = usado
        registro.append(dict(estudo=p["estudo"], lado=p["lado"], valor_na_ficha=p["valor"],
                             resposta=r["content"].strip()[:80], valor_usado=usado))
        print(f"  gatilho {modelo} {p['estudo']} {p['lado']}: {p['valor']} -> {usado}", flush=True)
    por_estudo = []
    sextetos = []
    for rot_nome, fs in fichas.items():
        e = dg.braco_deterministico(fs.get("braco_experimental", {}), julg, (rot_nome, "braco_experimental"))
        c = dg.braco_deterministico(fs.get("braco_controle", {}), julg, (rot_nome, "braco_controle"))
        if None in e or None in c:
            por_estudo.append(dict(estudo=rot_nome, status="dados-insuficientes",
                                   exp=[x for x in e], ctl=[x for x in c]))
            continue
        s = [e[0], e[1], e[2], c[0], c[1], c[2]]
        sextetos.append(s)
        por_estudo.append(dict(estudo=rot_nome, md=h3.md(*s), ic95=h3.ic95_md(*s), sexteto=s,
                               replica_usada=reps[rot_nome],
                               replicas_identicas=concordancia_replicas(
                                   modelo, next(t for t, r in h3.ROT.items() if r == rot_nome))))
    pool = h3.pool_dl_md(sextetos) if sextetos else None
    resultado = dict(modelo=modelo, estudos_no_pool=len(sextetos),
                     gatilhos=registro, por_estudo=por_estudo, agregado=pool)
    (D4 / "resultados").mkdir(exist_ok=True)
    (D4 / "resultados" / f"{modelo}.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"== {modelo}: {len(sextetos)}/7 estudos no pool · gatilhos disparados: {len(registro)}", flush=True)
    print(f"   agregado: {json.dumps(pool, ensure_ascii=False)}", flush=True)
    return resultado


def main():
    assert h3.ELENCO == "base"
    alvo = sys.argv[1:] or MODELOS_E4
    for selo in ("perturbacoes-estudo3.json", "sementes-auditoria.json"):
        p = D3 / selo
        if p.exists():
            print(f"SHA-256 {selo}: {hashlib.sha256(p.read_bytes()).hexdigest()}", flush=True)
    t0 = time.time()
    for modelo in alvo:
        print(f"\n===== Estudo 4 · {modelo}", flush=True)
        extrai(modelo)
        downstream(modelo)
    print(f"\nEstudo 4 completo em {(time.time()-t0)/60:.1f} min", flush=True)


if __name__ == "__main__":
    main()

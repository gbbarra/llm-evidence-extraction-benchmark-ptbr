# -*- coding: utf-8 -*-
"""EXTRAI Study 4 — Amendment-1 extension arm: the discarded smalls.

llama3.1:8b / qwen3.5:9b / deepseek-r1:14b as extractors under the identical
deterministic engine. Carries the Amendment-1 erratum fixes at run time:
E4-1 (neutral sign question — states only the analysis convention, no
premise about what the printed positive means) and E4-2 (all three
pre-declared trigger classes: as-printed positive; required-field-NR,
sheet-scoped; factorial-margin, fired by the sheet's declared design).
The frozen Study-3 instruments are imported, never edited; the extension
models are injected into the harness's model table at run time.

Run: python scripts/estudo4/e4-extensao.py [modelo...]   (default: all 3)
Outputs: dados/estudo4/saidas/<modelo>/extracao/ · dados/estudo4/resultados/<modelo>.json
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

_e = importlib.util.spec_from_file_location("e4", ROOT / "scripts" / "estudo4" / "e4-pipeline.py")
e4 = importlib.util.module_from_spec(_e)
_e.loader.exec_module(e4)
h3, dg = e4.h3, e4.dg

MODELOS_EXT = {"llama8": "llama3.1:8b", "qwen35": "qwen3.5:9b", "deepseek14": "deepseek-r1:14b"}
for chave, tag in MODELOS_EXT.items():
    h3.MODELS[chave] = dict(ollama=tag, cpu=False)
MAXTOK = 4000  # Amendment-1 allowance (prompt unchanged)


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
            r = h3.gerar(modelo, base + texto, max_tokens=MAXTOK)
            out.write_text(json.dumps(dict(modelo=modelo, trial=tid, replica=rep, **r),
                                      ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  extracao {modelo} {tid}-r{rep}: {r['dt']:.0f}s, {r['tokens']} tok", flush=True)


# ---------------- Amendment-1 trigger questions ----------------
def pergunta_sinal_neutra(p):
    lado = "braço experimental" if p["lado"] == "braco_experimental" else "braço controle"
    return (
        f"Você é o revisor de uma metanálise. Trecho da ficha de extração do estudo {p['estudo']} ({lado}):\n"
        + json.dumps(p["ficha_braco"], ensure_ascii=False, indent=1)
        + f"\n\nO campo hba1c_mudanca_media está registrado como '{p['valor']}'. "
        "Convenção da análise: negativo = HbA1c caiu; positivo = HbA1c subiu.\n"
        "Com base apenas na ficha acima, responda APENAS o valor numérico (com sinal) "
        "que deve entrar na análise para este braço."
    )


def pergunta_fatorial(rot, fs):
    e, c = fs.get("braco_experimental", {}), fs.get("braco_controle", {})
    return (
        f"O estudo {rot} declara desenho '{fs.get('desenho', '')}'. Em desenhos fatoriais, a análise deve usar "
        "os AGRUPAMENTOS que o próprio texto compara para o desfecho (por exemplo, margens de dieta), "
        "não as células individuais do fatorial.\n"
        f"Sua ficha registra: braço experimental '{e.get('rotulo', '')}' "
        f"n_randomizado={e.get('n_randomizado', 'NR')} n_analisado={e.get('n_analisado', 'NR')}; "
        f"braço controle '{c.get('rotulo', '')}' "
        f"n_randomizado={c.get('n_randomizado', 'NR')} n_analisado={c.get('n_analisado', 'NR')}.\n"
        "Esses ns correspondem aos agrupamentos que o texto compara? "
        "Responda APENAS 'SIM' ou os ns corretos no formato 'exp=N ctl=N'."
    )


def pergunta_nr(rot, lado, b, faltam):
    lado_pt = "braço experimental" if lado == "braco_experimental" else "braço controle"
    return (
        f"Trecho da ficha de extração do estudo {rot} ({lado_pt}):\n"
        + json.dumps(b, ensure_ascii=False, indent=1)
        + f"\n\nCom os campos acima não foi possível obter: {', '.join(faltam)}. "
        "Se algum desses valores é recuperável APENAS a partir da própria ficha "
        "(outro campo ou conversão nela indicada), responda um JSON só com os que faltam, "
        'por exemplo {"media": -0.5, "dp": 0.4, "n": 30}. Caso contrário responda NR.'
    )


def downstream(modelo):
    fichas = {}
    reps = {}
    for tid in h3.TRIALS:
        f, rep = e4.ficha_e4(modelo, tid)
        if f:
            fichas[h3.ROT[tid]] = f
            reps[h3.ROT[tid]] = rep
    registro = []

    # class 1 — as-printed positive change (neutral question, E4-1)
    julg = {}
    for p in dg.gatilhos(fichas):
        r = h3.gerar(modelo, pergunta_sinal_neutra(p), max_tokens=40)
        m = re.search(r"-?\d+(?:\.\d+)?", r["content"])
        usado = float(m.group(0)) if m else p["valor"]
        julg[(p["estudo"], p["lado"])] = usado
        registro.append(dict(classe="sinal-como-impresso", estudo=p["estudo"], lado=p["lado"],
                             valor_na_ficha=p["valor"], resposta=r["content"].strip()[:80], valor_usado=usado))
        print(f"  gatilho sinal {modelo} {p['estudo']} {p['lado']}: {p['valor']} -> {usado}", flush=True)

    # class 2 — factorial margins (fired by the sheet's declared design)
    for rot, fs in fichas.items():
        if not re.search(r"fatorial|factorial|2\s*[x×]\s*2", str(fs.get("desenho", "")), re.I):
            continue
        r = h3.gerar(modelo, pergunta_fatorial(rot, fs), max_tokens=60)
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
                r = h3.gerar(modelo, pergunta_nr(rot, lado, b, faltam), max_tokens=120)
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
                               replicas_identicas=e4.concordancia_replicas(
                                   modelo, next(t for t, r2 in h3.ROT.items() if r2 == rot))))
    pool = h3.pool_dl_md(sextetos) if sextetos else None
    resultado = dict(modelo=modelo, arm="extensao-emenda1", estudos_no_pool=len(sextetos),
                     gatilhos=registro, por_estudo=por_estudo, agregado=pool)
    (D4 / "resultados").mkdir(exist_ok=True)
    (D4 / "resultados" / f"{modelo}.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"== {modelo}: {len(sextetos)}/7 estudos no pool · gatilhos: {len(registro)}", flush=True)
    print(f"   agregado: {json.dumps(pool, ensure_ascii=False)}", flush=True)
    return resultado


def main():
    assert h3.ELENCO == "base"
    alvo = sys.argv[1:] or list(MODELOS_EXT)
    for selo in ("perturbacoes-estudo3.json", "sementes-auditoria.json"):
        p = D3 / selo
        if p.exists():
            print(f"SHA-256 {selo}: {hashlib.sha256(p.read_bytes()).hexdigest()}", flush=True)
    t0 = time.time()
    for modelo in alvo:
        print(f"\n===== Estudo 4 · extensão (Emenda 1) · {modelo} [{MODELOS_EXT.get(modelo, '?')}]", flush=True)
        extrai(modelo)
        downstream(modelo)
    print(f"\nExtensão completa em {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()

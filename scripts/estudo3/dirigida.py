# -*- coding: utf-8 -*-
"""EXTRAI Study 3 / Paper 2 — Amendment 8: H2, the harness-driven pipeline.

The harness owns everything deterministic (field reading, dispersion
conversion by declared type, MD/CI, pooling — the graders' validated
functions); the model under test is consulted ONLY at mechanically detected
judgment points, one narrow question each. On these sheets the sole firing
trigger is the as-reported positive change (Wang prints the drop as +MD).

Arms: default rules (no model) · gemma4:12b as judge · qwen3:14b as judge.
Inputs: raw Stage-E sheets (gemma12 r1, first-parseable) — pure iGPU chain,
no audit stage, no seeds. Reference: mechanical truth under the graders'
documented resolutions.

Run: python scripts/estudo3/dirigida.py   (E3_ELENCO unset/base)
Outputs: dados/estudo3/saidas-dirigida/
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
D3 = ROOT / "dados" / "estudo3"
OUT = D3 / "saidas-dirigida"

_spec = importlib.util.spec_from_file_location("h3", ROOT / "scripts" / "estudo3" / "e3-harness.py")
h3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h3)


def num(x):
    try:
        return float(str(x).replace(",", ".").replace("−", "-").replace("–", "-").strip().rstrip("%"))
    except (TypeError, ValueError):
        return None


def eh_nr(x):
    return x is None or str(x).strip().upper() in ("NR", "NA", "N/A", "", "NONE")


def bounds_ic(braco):
    """CI bounds = the LAST TWO numbers across tipo+dispersao (the '95' of
    'IC95' must never be a bound — the judges' lesson)."""
    fonte = str(braco.get("hba1c_mudanca_tipo_dispersao", "")) + " " + str(braco.get("hba1c_mudanca_dispersao", ""))
    ms = re.findall(r"-?\d+(?:\.\d+)?", fonte)
    return (float(ms[-2]), float(ms[-1])) if len(ms) >= 2 else None


def braco_deterministico(braco, julgamentos, chave_braco):
    """(mean, sd, n) for one arm, deterministic; sign questions may override."""
    n = num(braco.get("n_analisado"))
    if n is None:
        n = num(braco.get("n_randomizado"))
    m = num(braco.get("hba1c_mudanca_media"))
    tipo = str(braco.get("hba1c_mudanca_tipo_dispersao", "")).upper()
    dp = num(braco.get("hba1c_mudanca_dispersao"))
    if m is None:
        b0, b1 = num(braco.get("hba1c_basal_media")), num(braco.get("hba1c_final_media"))
        if b0 is not None and b1 is not None:
            m = round(b1 - b0, 2)
            d0, d1 = num(braco.get("hba1c_basal_dp")), num(braco.get("hba1c_final_dp"))
            if d0 is not None and d1 is not None:
                dp = h3.dp_mudanca_r05(d0, d1)
                tipo = "DP"
    if tipo.startswith("IC"):
        bb = bounds_ic(braco)
        if bb and n:
            dp = h3.dp_de_ic(bb[0], bb[1], n)
    elif tipo in ("EP", "SE") and dp is not None and n:
        dp = h3.dp_de_se(dp, n)
    # judgment override: as-reported positive change
    if chave_braco in julgamentos:
        m = julgamentos[chave_braco]
    return m, dp, n


def gatilhos(fichas):
    """Mechanically detected judgment points. On these sheets: as-reported
    positive change means only (derived positives are arithmetic facts)."""
    pontos = []
    for rot_nome, fs in fichas.items():
        for lado in ("braco_experimental", "braco_controle"):
            b = fs.get(lado, {})
            v = num(b.get("hba1c_mudanca_media"))
            if v is not None and v > 0 and not eh_nr(b.get("hba1c_mudanca_media")):
                pontos.append(dict(estudo=rot_nome, lado=lado, valor=v, ficha_braco=b))
    return pontos


def pergunta_sinal(ponto):
    return (
        "Você é o revisor de uma metanálise. Trecho da ficha de extração do estudo "
        f"{ponto['estudo']} ({'braço experimental' if ponto['lado'] == 'braco_experimental' else 'braço controle'}):\n"
        + json.dumps(ponto["ficha_braco"], ensure_ascii=False, indent=1)
        + f"\n\nO campo hba1c_mudanca_media está registrado como '{ponto['valor']}' (número positivo). "
        "Nesse estudo, o texto imprime a QUEDA da HbA1c como número positivo (rotulado 'MD'). "
        "Para a análise, a convenção é: negativo = HbA1c caiu; positivo = HbA1c subiu.\n"
        "Responda APENAS o valor numérico com o sinal correto para a análise (ex.: -0.48 ou 0.48)."
    )


def roda_arm(nome, modelo, fichas):
    pontos = gatilhos(fichas)
    julg = {}
    registro = []
    for p in pontos:
        chave = (p["estudo"], p["lado"])
        if modelo is None:
            registro.append(dict(estudo=p["estudo"], lado=p["lado"], pergunta=None,
                                 resposta=None, valor_usado=p["valor"], regra="default: sinal como impresso"))
            continue
        q = pergunta_sinal(p)
        r = h3.gerar(modelo, q, max_tokens=40)
        v = None
        m = re.search(r"-?\d+(?:\.\d+)?", r["content"])
        if m:
            v = float(m.group(0))
        usado = v if v is not None else p["valor"]
        julg[chave] = usado
        registro.append(dict(estudo=p["estudo"], lado=p["lado"], resposta=r["content"].strip()[:80],
                             valor_usado=usado, dt=round(r["dt"], 1)))
    por_estudo = []
    sextetos = []
    for rot_nome, fs in fichas.items():
        e = braco_deterministico(fs.get("braco_experimental", {}), julg, (rot_nome, "braco_experimental"))
        c = braco_deterministico(fs.get("braco_controle", {}), julg, (rot_nome, "braco_controle"))
        if None in e or None in c:
            por_estudo.append(dict(estudo=rot_nome, status="dados-insuficientes"))
            continue
        s = [e[0], e[1], e[2], c[0], c[1], c[2]]
        sextetos.append(s)
        por_estudo.append(dict(estudo=rot_nome, md=h3.md(*s), ic95=h3.ic95_md(*s), sexteto=s))
    pool = h3.pool_dl_md(sextetos) if sextetos else None
    resultado = dict(arm=nome, modelo_juiz=modelo, julgamentos=registro,
                     por_estudo=por_estudo, agregado=pool)
    OUT.mkdir(exist_ok=True)
    (OUT / f"resultado-{nome}.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1),
                                                encoding="utf-8")
    print(f"== arm {nome}: {len(pontos)} julgamentos · agregado {json.dumps(pool, ensure_ascii=False)}", flush=True)
    for r in registro:
        print(f"   {r['estudo']} {r['lado'].split('_')[-1]}: usado={r['valor_usado']}"
              + (f" (resposta: {r['resposta']})" if r.get("resposta") else " (default)"), flush=True)
    return resultado


def main():
    assert h3.ELENCO == "base"
    fichas = {}
    for tid in h3.TRIALS:
        f, _rep = h3.ficha(tid)
        fichas[h3.ROT[tid]] = f
    print(f"fichas E (cruas, r1): {len(fichas)} estudos", flush=True)
    roda_arm("default", None, fichas)
    roda_arm("gemma12", "gemma12", fichas)
    roda_arm("qwen14", "qwen14", fichas)
    # referência: verdade mecânica dos corretores sobre as MESMAS fichas cruas
    _spec2 = importlib.util.spec_from_file_location("c3", ROOT / "scripts" / "estudo3" / "corrigir-e3.py")
    c3 = importlib.util.module_from_spec(_spec2)
    _spec2.loader.exec_module(c3)
    sext = [s for s in (c3.sexteto(fichas[h3.ROT[t]]) for t in h3.TRIALS) if s]
    verdade = h3.pool_dl_md(sext)
    (OUT / "referencia-verdade.json").write_text(json.dumps(dict(agregado=verdade, sextetos=sext),
                                                            ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"== referência (verdade mecânica, resoluções dos corretores): {json.dumps(verdade, ensure_ascii=False)}", flush=True)


if __name__ == "__main__":
    main()

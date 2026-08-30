# -*- coding: utf-8 -*-
"""EXTRAI Study 5 — pipeline v2 (Amendment 4): Priority-1 improvements,
extraction to result, 100% gemma4:12b.

Stage E fresh (frozen prompt VERBATIM, sheet enforced by constrained
decoding) -> runtime anti-invention net (article in context; the model's
answer is its own correction, logged) -> per-study orchestration (CALC2:
G2b nets + declarable-derivation net) -> pooling (G3b instruments) ->
totals by code -> synthesis -> forest by code. Then grader-side scoring:
cells vs the amended ruler, mechanical truth over the fresh sheets, and
the sealed unperturbation lens vs the published -0.24.

Run: python scripts/estudo5/pipeline2-gemma.py     (resume-safe at Stage E)
Outputs: dados/estudo5/saidas/EXTRA2 · saidas/CALC2 · saidas/POOL2 · dados/estudo5/pipeline2/
"""
import importlib.util
import json
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
D5 = ROOT / "dados" / "estudo5"
EXTRA2 = D5 / "saidas" / "EXTRA2"
PIPE2 = D5 / "pipeline2"
PERT = ROOT / "corpus" / "estudo3" / "perturbados"
MAX_VERIFICACOES = 6

_sp = importlib.util.spec_from_file_location("e5", ROOT / "scripts" / "estudo5" / "e5-harness.py")
e5 = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(e5)
h3 = e5.h3

_BR = {"rotulo": {"type": "string", "maxLength": 90},
       "descricao_intervencao": {"type": "string", "maxLength": 220}}
for _c in ("n_randomizado", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao",
           "hba1c_mudanca_tipo_dispersao", "hba1c_basal_media", "hba1c_basal_dp",
           "hba1c_final_media", "hba1c_final_dp"):
    _BR[_c] = {"type": "string", "maxLength": 48}
_BRACO = {"type": "object", "properties": _BR, "required": list(_BR), "additionalProperties": False}
SCHEMA_FICHA = {
    "type": "object",
    "properties": {
        "estudo": {"type": "string", "maxLength": 60},
        "desenho": {"type": "string", "maxLength": 60},
        "pais": {"type": "string", "maxLength": 40},
        "duracao": {"type": "string", "maxLength": 40},
        "n_randomizado_total": {"type": "string", "maxLength": 20},
        "braco_experimental": _BRACO,
        "braco_controle": _BRACO,
    },
    "required": ["estudo", "desenho", "pais", "duracao", "n_randomizado_total",
                 "braco_experimental", "braco_controle"],
    "additionalProperties": False,
}

CAMPOS_CONTAVEIS = ["n_randomizado_total"] + [
    f"{b}.{c}" for b in ("braco_experimental", "braco_controle")
    for c in ("n_randomizado", "n_analisado", "hba1c_mudanca_media", "hba1c_mudanca_dispersao",
              "hba1c_mudanca_tipo_dispersao", "hba1c_basal_media", "hba1c_basal_dp",
              "hba1c_final_media", "hba1c_final_dp")]


def numeros_do_texto(texto):
    return {round(float(x), 4) for x in
            re.findall(r"-?\d+(?:\.\d+)?", texto.replace("−", "-").replace("–", "-"))}


def poe(ficha, caminho, valor):
    partes = caminho.split(".")
    alvo = ficha
    for p in partes[:-1]:
        alvo = alvo[p]
    alvo[partes[-1]] = valor


def extrai2():
    base = h3.prompt_txt("e3-extracao.txt")
    EXTRA2.mkdir(parents=True, exist_ok=True)
    verificacoes = []
    for tid in h3.TRIALS:
        texto = (PERT / f"{tid}.txt").read_text(encoding="utf-8")
        nums_texto = numeros_do_texto(texto)
        for rep in (1, 2):
            out = EXTRA2 / f"{tid}-r{rep}.json"
            if out.exists():
                print(f"  pulando extracao {tid}-r{rep}", flush=True)
                continue
            r = e5.gerar_schema(base + texto, max_tokens=1200, schema=SCHEMA_FICHA)
            ficha = json.loads(r["content"])
            print(f"  extracao {tid}-r{rep}: {r['dt']:.0f}s", flush=True)
            # --- runtime anti-invention net (roadmap #1; the model corrects itself)
            suspeitos = []
            for caminho in CAMPOS_CONTAVEIS:
                v = e5.h3.acha_json  # noop to keep linters calm
                valor = ficha
                for p in caminho.split("."):
                    valor = valor.get(p, "")
                s = str(valor).replace("−", "-")
                for tok in re.findall(r"-?\d+(?:\.\d+)?", s):
                    if round(float(tok), 4) not in nums_texto and round(-float(tok), 4) not in nums_texto:
                        suspeitos.append((caminho, tok, s))
                        break
            for caminho, tok, s in suspeitos[:MAX_VERIFICACOES]:
                q = (D5 / "prompts" / "e5-verifica.txt").read_text(encoding="utf-8")
                q = q.replace("{CAMPO}", caminho).replace("{VALOR}", s)
                rv = h3.gerar(e5.MODELO, texto + "\n\n" + q, max_tokens=24)
                resp = rv["content"].strip().splitlines()[0].strip() if rv["content"].strip() else ""
                aplicado = None
                if re.fullmatch(r"NR\.?", resp, re.I):
                    poe(ficha, caminho, "NR")
                    aplicado = "NR"
                else:
                    m = re.search(r"-?\d+(?:[.,]\d+)?(?:\s*a\s*-?\d+(?:[.,]\d+)?)?", resp.replace("−", "-"))
                    if m:
                        poe(ficha, caminho, m.group(0))
                        aplicado = m.group(0)
                verificacoes.append(dict(trial=tid, rep=rep, campo=caminho, valor_original=s,
                                         resposta=resp[:60], aplicado=aplicado))
                print(f"    verificacao {tid}-r{rep} {caminho} = {s!r} -> {aplicado!r}", flush=True)
            if len(suspeitos) > MAX_VERIFICACOES:
                verificacoes.append(dict(trial=tid, rep=rep,
                                         excedentes=[c for c, _, _ in suspeitos[MAX_VERIFICACOES:]]))
            out.write_text(json.dumps(dict(modelo=e5.MODELO, trial=tid, replica=rep,
                                           content=json.dumps(ficha, ensure_ascii=False)),
                                      ensure_ascii=False, indent=1), encoding="utf-8")
    (EXTRA2 / "verificacoes.json").write_text(json.dumps(verificacoes, ensure_ascii=False, indent=1),
                                              encoding="utf-8")
    print(f"  verificacoes anti-invencao: {sum(1 for v in verificacoes if 'campo' in v)}", flush=True)


def main():
    PIPE2.mkdir(exist_ok=True)
    t0 = time.time()

    print("===== PIPELINE v2 · etapa E: extracao fresca sob schema + rede anti-invencao", flush=True)
    extrai2()

    print("\n===== etapa 1: calculo por estudo (CALC2 = G2b + derivacao declarada)", flush=True)
    base = (D5 / "prompts" / "e5-calc2.txt").read_text(encoding="utf-8")
    for tid in h3.TRIALS:
        if (D5 / "saidas" / "CALC2" / f"{tid}.json").exists():
            print(f"  pulando CALC2 {tid} (já existe)", flush=True)
            continue
        e5.roda_estudo("CALC2", tid, base, pasta_fichas=EXTRA2)

    print("\n===== etapa 2: pooling (instrumentos G3b)", flush=True)
    if (D5 / "resultados-POOL2.json").exists():
        print("  pulando POOL2 (já existe)", flush=True)
    else:
        e5.roda_g3(origem="CALC2", rotulo="POOL2")
    pool_reg = json.loads((D5 / "resultados-POOL2.json").read_text(encoding="utf-8"))
    proprios = e5.sextetos_do_g2b("CALC2")

    print("\n===== etapa 3+4: totais por codigo e sintese narrativa", flush=True)
    linhas, total_n = [], 0
    incoerentes = []
    for rot, d in proprios.items():
        s = d["sexteto"]
        n = int(s[2] + s[5])
        total_n += n
        f = d["final"] or {}
        ic = f.get("ic95")
        # E5-5 coherence check (detection at the product layer): an interval
        # that does not contain its own MD is flagged, never endorsed.
        coerente = bool(ic) and f.get("md") is not None and ic[0] - 1e-9 <= f["md"] <= ic[1] + 1e-9
        if coerente:
            linhas.append(f"- {rot}: MD {f.get('md')} IC95 {ic} · participantes: {n}")
        else:
            incoerentes.append(rot)
            linhas.append(f"- {rot}: MD {f.get('md')} · IC95 REPORTADO INVALIDO "
                          f"(o intervalo {ic} nao contem o proprio MD; nao usar) · participantes: {n}")
        d["coerente"] = coerente
    if incoerentes:
        print(f"  ICs reportados incoerentes (sinalizados, nunca endossados): {incoerentes}", flush=True)
    ag = pool_reg.get("final") or pool_reg["pool_sobre_os_proprios_sextetos"]
    i2 = pool_reg["pool_sobre_os_proprios_sextetos"].get("i2_pct")
    dados = ("AGREGADO (DerSimonian-Laird): MD " + str(ag.get("md")) + " IC95 " + str(ag.get("ic95"))
             + f" · I2 = {i2}%\nESTUDOS: {len(proprios)} · PARTICIPANTES TOTAIS: {total_n}\n"
             + "\n".join(linhas))
    if (PIPE2 / "sintese.md").exists():
        sintese = (PIPE2 / "sintese.md").read_text(encoding="utf-8").split("\n\n", 1)[-1].strip()
        print("  pulando sintese (ja existe; produto reutilizado)", flush=True)
    else:
        prompt = (D5 / "prompts" / "e5-sintese.txt").read_text(encoding="utf-8").replace("{DADOS}", dados)
        r = h3.gerar(e5.MODELO, prompt, max_tokens=600)
        sintese = r["content"].strip()
    fornecidos = set(re.findall(r"-?\d+(?:\.\d+)?", dados.replace("−", "-")))
    orfaos = [x for x in re.findall(r"-?\d+(?:[.,]\d+)?", sintese.replace("−", "-"))
              if x.replace(",", ".") not in fornecidos
              and x.replace(",", ".").lstrip("-") not in fornecidos
              and not re.fullmatch(r"\d{1,2}|95|150|300", x)]
    print(f"  orfaos: {orfaos if orfaos else 'ZERO'}", flush=True)

    print("\n===== etapa 5: forest por codigo", flush=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8.2, 4.4), dpi=200)
    ax.axvline(0, color="#555", lw=1)
    ordem = list(proprios.items())
    for i, (rot, d) in enumerate(ordem):
        f = d["final"] or {}
        y = len(ordem) - i
        if d.get("coerente"):
            ax.plot(f["ic95"], [y, y], color="#2e5fa3", lw=2)
            ax.plot(f.get("md"), y, "s", ms=7, color="#2e5fa3")
        elif f.get("md") is not None:
            ax.plot(f["md"], y, "s", ms=7, color="#b3541e")
            ax.annotate("IC inválido*", (f["md"], y), xytext=(9, -3.5),
                        textcoords="offset points", fontsize=8.2, color="#b3541e")
        ax.text(-0.02, y, rot, ha="right", va="center", fontsize=9, transform=ax.get_yaxis_transform())
    if any(not d.get("coerente") for _, d in ordem):
        fig.text(0.12, -0.02, "* IC reportado pelo modelo não contém o próprio MD — "
                 "sinalizado e excluído do gráfico; o agregado usa os sextetos executados, não este IC.",
                 fontsize=7.8, color="#b3541e")
    ax.plot(ag["ic95"], [0, 0], color="#12315e", lw=3)
    ax.plot(ag["md"], 0, "D", ms=11, color="#12315e")
    ax.text(-0.02, 0, "AGREGADO (DL)", ha="right", va="center", fontsize=9.5,
            fontweight="bold", transform=ax.get_yaxis_transform())
    ax.set_yticks([])
    ax.set_xlabel("Diferença de médias na variação de HbA1c, % (negativo favorece low-carb)", fontsize=9)
    ax.set_title("Pipeline v2 — 100% gemma4:12b, da extração ao resultado", fontsize=10)
    ax.spines[["left", "top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(PIPE2 / "forest-gemma-v2.png", bbox_inches="tight", facecolor="white")

    print("\n===== correcao (lado dos corretores): celulas · verdade · lente", flush=True)
    c3 = e5.carrega("c3", "scripts/estudo3/corrigir-e3.py")
    selo = json.loads((ROOT / "dados" / "estudo3" / "perturbacoes-estudo3.json").read_text(encoding="utf-8"))
    boas = tot = 0
    detalhes = []
    for tid in h3.TRIALS:
        for rep in (1, 2):
            f = EXTRA2 / f"{tid}-r{rep}.json"
            js = h3.acha_json(json.loads(f.read_text(encoding="utf-8"))["content"])
            for caminho, esperado in c3.EXPECTED[tid].items():
                rot = c3.rotula_cel(c3.pega(js, caminho), esperado)
                tot += 1
                boas += rot in ("exata", "derivavel", "nr-correta")
                detalhes.append(dict(trial=tid, rep=rep, campo=caminho,
                                     valor=c3.pega(js, caminho), rotulo=rot))
    sext_v, sext_d = [], []
    for tid in h3.TRIALS:
        fs = e5.ficha_r2(tid, EXTRA2)
        s = c3.sexteto(fs)
        if s:
            sext_v.append(s)
        txt = json.dumps(fs, ensure_ascii=False)
        for reg in selo.get(tid, []):
            p, o = str(reg["perturbado"]), str(reg["original"])
            txt = txt.replace(f'"{p}"', f'"{o}"').replace(f'"-{p}"', f'"-{o}"')
            txt = txt.replace(f" {p}", f" {o}").replace(f"-{p}", f"-{o}")
        sd = c3.sexteto(json.loads(txt))
        if sd:
            sext_d.append(sd)
    verdade = h3.pool_dl_md(sext_v)
    lente = h3.pool_dl_md(sext_d)
    consist = pool_reg["consistente"]
    resumo = dict(celulas=f"{boas}/{tot} ({round(100 * boas / tot, 1)}%)",
                  agregado_do_modelo=ag, verdade_mecanica=verdade,
                  delta_md=round(abs(ag["md"] - verdade["md"]), 2),
                  lente_desperturbada=lente,
                  ancora_publicada={"md": -0.24, "ic95": [-0.32, -0.16]},
                  consistente_pooling=consist, participantes=total_n,
                  numeros_orfaos=orfaos, sintese=sintese,
                  minutos=round((time.time() - t0) / 60, 1))
    (PIPE2 / "correcao-extracao.json").write_text(json.dumps(dict(detalhes=detalhes), ensure_ascii=False,
                                                             indent=1), encoding="utf-8")
    (PIPE2 / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")
    (PIPE2 / "sintese.md").write_text("# Síntese do pipeline v2 (100% gemma4:12b)\n\n" + sintese + "\n",
                                      encoding="utf-8")
    print(f"  celulas: {resumo['celulas']}", flush=True)
    print(f"  agregado modelo: {json.dumps(ag, ensure_ascii=False)} · verdade: "
          f"{json.dumps(verdade, ensure_ascii=False)} · delta md {resumo['delta_md']}", flush=True)
    print(f"  LENTE: {json.dumps(lente, ensure_ascii=False)} vs ancora -0.24 [-0.32, -0.16]", flush=True)
    print(f"\n== PIPELINE v2 COMPLETO em {resumo['minutos']} min · consistente: {consist} · "
          f"orfaos: {len(orfaos)}", flush=True)


if __name__ == "__main__":
    main()

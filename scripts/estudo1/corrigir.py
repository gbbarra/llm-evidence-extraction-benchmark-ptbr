# -*- coding: utf-8 -*-
"""EXTRAI E1 — corretor mecânico oficial (T1, célula a célula).

Régua: gabarito-oficial.json (camada 2, verificada na fonte — Emenda 4).
Perturbações por cima (célula perturbada pontua contra o valor perturbado;
Emenda 3: nas duas células vazadas, o original também vale como leitura).

Rótulos por célula (METHOD):
  exata / deriv (equivalência declarada) / nr-correta  -> 1,0
  omissa / errada / recitou / segue-erro-da-ma         -> 0,0
  adjudicar    -> vai à adjudicação (LLM juiz + humano), não pontua ainda
  fora         -> pendente-adjudicação do gabarito ou sem régua (não conta)

Equivalências mecânicas: números iguais; arredondamento (0–1 casa);
contagem↔percentual via n do braço (pós-errata); horas↔dias (×24).

Uso: python corrigir.py [modelos...]   (padrão: todos com bloco completo)
Saída: dados/estudo1/correcao/<modelo>-t1.json + resumo no stdout
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
D1 = RAIZ / "dados" / "estudo1"

CAMPOS = [
    "n_randomizados_gdft", "n_randomizados_controle", "tipo_cirurgia",
    "laparoscopia_gdft", "laparoscopia_controle", "asa_gdft", "asa_controle",
    "fluido_total_gdft", "fluido_total_controle", "cristaloide_gdft", "cristaloide_controle",
    "coloide_gdft", "coloide_controle", "perda_sanguinea_gdft", "perda_sanguinea_controle",
    "uso_inotropico", "morbidade_eventos_gdft", "morbidade_eventos_controle",
    "mortalidade_gdft", "mortalidade_controle", "los_hospitalar_gdft", "los_hospitalar_controle",
    "tempo_flatus_gdft", "tempo_flatus_controle", "tempo_ingesta_oral_gdft",
    "tempo_ingesta_oral_controle", "tempo_evacuacao_gdft", "tempo_evacuacao_controle",
    "ileo_pos_op_gdft", "ileo_pos_op_controle",
]
EMENDA3 = {("PMC5589093", "fluido_total_controle"), ("PMC10694978", "fluido_total_controle")}


def nums(s):
    s = re.sub(r"(?<=\d),(?=\d{3}\b)", "", str(s or ""))
    return [x for x in re.findall(r"\d+(?:\.\d+)?", s)]


def eh_nr(v):
    v = str(v or "").strip().upper()
    return v in ("", "NR", "N/A", "NA", "NOT REPORTED", "NÃO REPORTADO", "NAO REPORTADO") or v.startswith("NR ")


def contem_valor(texto, alvo):
    return bool(re.search(r"(?<![\d.,])" + re.escape(str(alvo)) + r"(?!\d|\.\d)", str(texto or "")))


def casa(v_modelo, alvo, ns_braco):
    """O valor do modelo cobre o(s) número(s) do alvo sob as equivalências mecânicas?"""
    a_nums, m_nums = nums(alvo), nums(v_modelo)
    if not a_nums:
        # alvo textual: cobertura de palavras-chave (>=1 palavra longa em comum)
        a_pal = {w for w in re.findall(r"[a-záéíóúçã-]{5,}", str(alvo).lower())}
        m_pal = set(re.findall(r"[a-záéíóúçã-]{5,}", str(v_modelo).lower()))
        return ("exata", None) if a_pal & m_pal else (None, None)
    m_f = [float(x) for x in m_nums]
    faltas, regras = [], []
    for a in a_nums:
        af = float(a)
        if a in m_nums or af in m_f:
            continue
        if any(abs(af - m) <= 0.5 and round(af) == round(m) for m in m_f):
            regras.append("arredondamento"); continue
        if any(abs(af * 24 - m) < 0.75 or abs(af / 24 - m) < 0.25 for m in m_f):
            regras.append("horas<->dias"); continue
        conv = False
        for n_arm in ns_braco:
            if n_arm and (any(abs(100 * af / n_arm - m) <= 0.6 for m in m_f)
                          or any(abs(af * n_arm / 100 - m) <= 0.6 for m in m_f)):
                conv = True; break
        if conv:
            regras.append("contagem<->%"); continue
        faltas.append(a)
    if not faltas:
        return ("exata", None) if not regras else ("deriv", "+".join(sorted(set(regras))))
    # cobertura parcial dominante (>=metade dos números, nenhum contradito) -> deriv fraca? não: adjudicar
    return (None, None)


def corrigir_modelo(mod, oficial, selo_campo, textos):
    resultado = {}
    contas = {}
    for f in sorted((D1 / "saidas" / mod).glob("*-t1-r1.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        pm = d["pmcid"]
        # primeira réplica parseável; falha de parse vira métrica de formato
        j = None
        for rep in ("r1", "r2"):
            try:
                dd = json.loads((D1 / "saidas" / mod / f"{pm}-t1-{rep}.json").read_text(encoding="utf-8"))
                j = json.loads(re.sub(r"^```(?:json)?\s*|\s*```$", "", dd["content"].strip()))
                if rep != "r1":
                    contas["parse-falha-r1(usou r2)"] = contas.get("parse-falha-r1(usou r2)", 0) + 1
                break
            except Exception:
                j = None
        if j is None:
            resultado[pm] = {"_erro": "json inválido nas duas réplicas"}
            contas["parse-falha-total"] = contas.get("parse-falha-total", 0) + 1
            continue
        cels = {}
        regs = oficial.get(pm, {})
        ns_braco = []
        for c in ("n_randomizados_gdft", "n_randomizados_controle"):
            ns_braco += [float(x) for x in nums((regs.get(c) or {}).get("valor_fonte", ""))[:2]]
        for campo in CAMPOS:
            v = j.get(campo, {}).get("valor", "")
            reg = regs.get(campo) or {}
            ver = reg.get("veredito", "sem-registro")
            pert = selo_campo.get((pm, campo))
            rotulo, regra = None, None
            adj = ADJUDICACOES.get(pm, {}).get(campo, {})
            if adj.get("vereditos", {}).get(mod):
                rotulo = adj["vereditos"][mod]
                regra = "adjudicada: " + adj.get("regra", "")[:80]
            elif pert:
                if contem_valor(v, pert["perturbado"]):
                    rotulo = "exata"; regra = "prova: leu"
                elif (pm, campo) in EMENDA3 and contem_valor(v, pert["original"]):
                    rotulo = "exata"; regra = "Emenda 3: insumo inconsistente"
                elif contem_valor(v, pert["original"]):
                    rotulo = "recitou"
                elif eh_nr(v):
                    rotulo = "omissa"
                else:
                    rotulo = "adjudicar"; regra = "célula perturbada, valor não casou"
            elif ver in ("pendente-adjudicacao",):
                rotulo = "fora"
            elif ver == "confirmada-nr":
                rotulo = "nr-correta" if eh_nr(v) else "adjudicar"
            elif ver == "dado-fora-do-insumo":
                rotulo = "nr-correta" if eh_nr(v) else "adjudicar"
                if rotulo == "nr-correta":
                    regra = "dado ausente do insumo textual"
            elif ver in ("sem-valor-na-ma", "sem-registro"):
                rotulo = "fora" if eh_nr(v) else "extra"
            elif ver == "ma-inferiu":
                if eh_nr(v):
                    rotulo = "nr-correta"; regra = "fonte não enumera"
                elif re.search(r"^0\b|todos|100%|all\b", str(v).strip(), re.I) or casa(v, reg.get("valor_fonte"), ns_braco)[0]:
                    rotulo = "exata"; regra = "inferência coerente"
                else:
                    rotulo = "adjudicar"
            elif ver == "primario-contraditorio":
                ok1 = casa(v, reg.get("valor_fonte"), ns_braco)[0]
                ok2 = casa(v, reg.get("ma"), ns_braco)[0]
                rotulo = "exata" if (ok1 or ok2) else ("omissa" if eh_nr(v) else "adjudicar")
                if rotulo == "exata": regra = "primário contraditório: ambos os lados valem"
            elif ver == "nao-sustentada":
                rotulo = "nr-correta" if eh_nr(v) else "adjudicar"
            else:
                alvo = reg.get("valor_fonte") or reg.get("ma")
                r, eq = casa(v, alvo, ns_braco)
                if r:
                    rotulo, regra = r, eq
                elif ver == "errata-ma" and casa(v, reg.get("ma"), ns_braco)[0]:
                    rotulo = "segue-erro-da-ma"
                elif eh_nr(v):
                    rotulo = "omissa"
                else:
                    dentro = all(contem_valor(textos[pm], x) for x in nums(v)[:3]) if nums(v) else True
                    rotulo = "adjudicar" if dentro else "adjudicar-invencao-candidata"
            cels[campo] = dict(valor=str(v)[:120], rotulo=rotulo, **({"regra": regra} if regra else {}))
            contas[rotulo] = contas.get(rotulo, 0) + 1
        resultado[pm] = cels
    return resultado, contas


ADJUDICACOES = {}


def main():
    global ADJUDICACOES
    adj_path = D1 / "adjudicacoes-t1.json"
    ADJUDICACOES = {k: v for k, v in json.loads(adj_path.read_text(encoding="utf-8")).items()
                    if not k.startswith("_")} if adj_path.exists() else {}
    oficial = json.loads((D1 / "gabarito-oficial.json").read_text(encoding="utf-8"))["celulas"]
    selo = json.loads((D1 / "perturbacoes-estudo1.json").read_text(encoding="utf-8"))
    inv = {}
    MAPA_MA = {  # (tabela, campo MA) -> campo formulário (para mapear o selo)
        (3, "GDFT"): "n_randomizados_gdft", (3, "Control"): "n_randomizados_controle",
        (3, "Surgery"): "tipo_cirurgia", (3, "ASA (GDFT)"): "asa_gdft",
        (4, "Total fluid (mL) GDFT"): "fluido_total_gdft", (4, "Total fluid (mL) Control"): "fluido_total_controle",
        (4, "Crystalloid (mL) GDFT"): "cristaloide_gdft",
        (5, "GDFT events n (%)"): "morbidade_eventos_gdft", (5, "Control events n (%)"): "morbidade_eventos_controle",
    }
    selo_campo = {}
    for pm, rs in selo.items():
        for r in rs:
            m = re.search(r"\[alimenta (\w+)", r["campo"])
            campo = ("fluido_total_gdft" if m and m.group(1) == "fluido_total"
                     else m.group(1) if m else MAPA_MA.get((r["tabela"], r["campo"])))
            if campo:
                selo_campo[(pm, campo)] = r
    textos = {p.stem: p.read_text(encoding="utf-8")
              for p in (RAIZ / "corpus" / "perturbados").glob("PMC*.txt")}
    (D1 / "correcao").mkdir(exist_ok=True)

    mods = sys.argv[1:] or [d.name for d in (D1 / "saidas").iterdir()
                            if d.is_dir() and not d.name.startswith("smoke")
                            and len(list(d.glob("*-t1-r1.json"))) == 8]
    print(f"{'modelo':<9} {'pontuáveis':>10} {'certas':>7} {'acurácia':>9} | exata deriv nr-ok | omissa errada/recitou adjudicar")
    for mod in mods:
        res, c = corrigir_modelo(mod, oficial, selo_campo, textos)
        certas = c.get("exata", 0) + c.get("deriv", 0) + c.get("nr-correta", 0)
        erradas = c.get("omissa", 0) + c.get("errada", 0) + c.get("recitou", 0) + c.get("segue-erro-da-ma", 0)
        adj = c.get("adjudicar", 0) + c.get("adjudicar-invencao-candidata", 0)
        pont = certas + erradas
        (D1 / "correcao" / f"{mod}-t1.json").write_text(
            json.dumps(dict(modelo=mod, contas=c, celulas=res), ensure_ascii=False, indent=1),
            encoding="utf-8")
        print(f"{mod:<9} {pont:>10} {certas:>7} {100*certas/pont if pont else 0:>8.0f}% | "
              f"{c.get('exata',0):>5} {c.get('deriv',0):>5} {c.get('nr-correta',0):>5} | "
              f"{c.get('omissa',0):>6} {erradas-c.get('omissa',0):>13} {adj:>9}")
    print("\n(adjudicar/fora/extra não entram no denominador; detalhes em dados/estudo1/correcao/)")


if __name__ == "__main__":
    main()

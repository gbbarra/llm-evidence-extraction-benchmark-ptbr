# -*- coding: utf-8 -*-
"""EXTRAI E1 — Emenda 4: verifica cada célula da MA contra a fonte primária ORIGINAL.

Para cada campo do formulário com valor na MA, procura o(s) número(s) no texto
original do primário sob equivalências pré-declaradas:
  literal          — o número da MA aparece perto de uma palavra-âncora do campo
  contagem↔percent — "28 (71.8%)": conta e/ou percentual, com n do braço
  horas↔dias       — valor/24 ou valor×24 (1 casa) perto da âncora
Gera dados/estudo1/verificacao-draft.json com trechos candidatos e status
automático; a adjudicação final (humano+Claude) escreve gabarito-oficial.json.

O script usa APENAS os textos originais e a MA — nunca as saídas dos modelos.
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
D1 = RAIZ / "dados" / "estudo1"

MAPA = {
    "n_randomizados_gdft": (3, "GDFT"), "n_randomizados_controle": (3, "Control"),
    "tipo_cirurgia": (3, "Surgery"),
    "laparoscopia_gdft": (3, "Lap (GDFT)"), "laparoscopia_controle": (3, "Lap (Control)"),
    "asa_gdft": (3, "ASA (GDFT)"), "asa_controle": (3, "ASA (control)"),
    "fluido_total_gdft": (4, "Total fluid (mL) GDFT"), "fluido_total_controle": (4, "Total fluid (mL) Control"),
    "cristaloide_gdft": (4, "Crystalloid (mL) GDFT"), "cristaloide_controle": (4, "Crystalloid (mL) Control"),
    "coloide_gdft": (4, "Colloid (mL) GDFT"), "coloide_controle": (4, "Colloid (mL) Control"),
    "perda_sanguinea_gdft": (4, "Blood loss (mL) GDFT"), "perda_sanguinea_controle": (4, "Blood loss (mL) Control"),
    "uso_inotropico": (4, "Inotrope use"),
    "morbidade_eventos_gdft": (5, "GDFT events n (%)"), "morbidade_eventos_controle": (5, "Control events n (%)"),
    "mortalidade_gdft": (6, "GDFT deaths n (%)"), "mortalidade_controle": (6, "Control deaths n (%)"),
    "tempo_flatus_gdft": (8, "GDFT (mean ± SD)"), "tempo_flatus_controle": (8, "Control (mean ± SD)"),
    "tempo_ingesta_oral_gdft": (9, "GDFT"), "tempo_ingesta_oral_controle": (9, "Control"),
    "tempo_evacuacao_gdft": (10, "GDFT"), "tempo_evacuacao_controle": (10, "Control"),
    "ileo_pos_op_gdft": (11, "GDFT n (%)"), "ileo_pos_op_controle": (11, "Control n (%)"),
}
ANCORA = {
    "n_randomizados": r"randomi|assigned|allocated|enrolled|group \(\s*n|patients",
    "tipo_cirurgia": r"surg|ectomy|resection|procedure|operation",
    "laparoscopia": r"laparoscop",
    "asa": r"\basa\b",
    "fluido_total": r"total.{0,20}(fluid|volume)|fluid|volume|infus|administer",
    "cristaloide": r"crystalloid|ringer|saline|lactate",
    "coloide": r"colloid|starch|\bhes\b|albumin|gelatin|voluven",
    "perda_sanguinea": r"blood loss|bleed|h[ae]morrhage",
    "uso_inotropico": r"inotrop|vasopressor|norepinephrine|ephedrine|vasoactive",
    "morbidade": r"complicat|morbid",
    "mortalidade": r"death|mortal|died|surviv",
    "tempo_flatus": r"flatus",
    "tempo_ingesta": r"oral|intake|diet|feed",
    "tempo_evacuacao": r"bowel|defecat|stool",
    "ileo_pos_op": r"ileus",
}


def ancora_de(campo):
    for chave, pad in ANCORA.items():
        if campo.startswith(chave):
            return pad
    return None


def nums(s):
    s = re.sub(r"(?<=\d),(?=\d{3}\b)", "", str(s or ""))
    return re.findall(r"\d+(?:\.\d+)?", s)


def acha(texto, valor, ancora, janela=110):
    pad = r"(?<![\d.,])" + re.escape(valor) + r"(?!\d|\.\d)"
    trechos = []
    for m in re.finditer(pad, texto):
        a, b = max(0, m.start() - janela), min(len(texto), m.end() + janela)
        tr = re.sub(r"\s+", " ", texto[a:b])
        if not ancora or re.search(ancora, tr, re.I):
            trechos.append(tr)
    return trechos


def fmt_num(x):
    return str(int(x)) if float(x) == int(float(x)) else f"{float(x):.1f}"


def main():
    gab = json.loads((D1 / "gabarito-ma.json").read_text(encoding="utf-8"))
    ma = {}
    for t in gab["tabelas"]:
        if t["numero"] == 1:
            continue
        for l in t["linhas"]:
            if l.get("pmcid"):
                ma[(l["pmcid"], t["numero"])] = l["celulas"]

    saida = {}
    resumo = dict(literal=0, equivalencia=0, nao_achada=0, sem_valor=0)
    fontes = sorted((RAIZ / "corpus" / "primarios-texto").glob("PMC*.txt")) + \
        sorted((RAIZ / "corpus" / "fechados-texto").glob("REF*.txt"))
    for txt in fontes:
        pm = txt.stem
        texto = txt.read_text(encoding="utf-8")
        celulas = {}
        # 1ª passada: n dos braços (base p/ equivalência contagem<->%)
        ns_braco = {}
        for lado in ("gdft", "controle"):
            gv = ma.get((pm, 3), {}).get("GDFT" if lado == "gdft" else "Control", "")
            if gv and gv.replace(".", "").isdigit():
                ns_braco[lado] = float(gv)
        for campo, (tab, col) in MAPA.items():
            gv = ma.get((pm, tab), {}).get(col)
            if gv in (None, "", "NR", "—", "No", "-"):
                celulas[campo] = dict(ma=gv, status="sem-valor-na-ma")
                resumo["sem_valor"] += 1
                continue
            anc = ancora_de(campo)
            achados, eqs = {}, []
            for v in nums(gv)[:4]:
                trechos = acha(texto, v, anc)
                if trechos:
                    achados[v] = trechos[:2]
                    continue
                # equivalências: contagem<->% (n dos DOIS braços, MA pode ter trocado) e horas<->dias
                lados = [ns_braco.get("gdft"), ns_braco.get("controle")]
                cands = []
                for n_arm in [x for x in lados if x]:
                    cands += [(fmt_num(100 * float(v) / n_arm), f"%={v}/{int(n_arm)}"),
                              (fmt_num(float(v) * n_arm / 100), f"contagem de {v}% de {int(n_arm)}")]
                cands += [(fmt_num(float(v) / 24), f"{v}h em dias"), (fmt_num(float(v) * 24), f"{v}d em horas")]
                for cv, rot in cands:
                    tr = acha(texto, cv, anc)
                    if tr:
                        eqs.append(dict(ma=v, fonte=cv, regra=rot, trecho=tr[0]))
                        break
            todos = nums(gv)[:4]
            if achados and len(achados) == len(todos):
                st = "literal"
            elif achados or eqs:
                st = "equivalencia"
            elif not todos:
                st = "texto-sem-numero"
            else:
                st = "nao-achada"
            resumo["literal" if st == "literal" else "equivalencia" if st == "equivalencia" else "nao_achada"] = \
                resumo.get("literal" if st == "literal" else "equivalencia" if st == "equivalencia" else "nao_achada", 0) + 1
            celulas[campo] = dict(ma=gv, status=st, achados=achados, equivalencias=eqs)
        saida[pm] = celulas

    out = D1 / "verificacao-draft.json"
    out.write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"draft: {out.relative_to(RAIZ)}")
    print(f"células: {resumo}")


if __name__ == "__main__":
    main()

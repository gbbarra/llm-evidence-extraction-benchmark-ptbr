# -*- coding: utf-8 -*-
"""EXTRAI E1 — Emenda 4: consolida o gabarito oficial (camada 2).

Funde a verificação automática (verificacao-draft.json) com a camada de
adjudicação manual abaixo (OVERLAY — o registro público das decisões, cada uma
com citação literal da fonte). Células sem sustentação clara ficam
"pendente-adjudicacao" e NÃO pontuam contra nenhum modelo na correção.

Saída: dados/estudo1/gabarito-oficial.json
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
D1 = RAIZ / "dados" / "estudo1"

YOON, SUN, WU, CASTRO = "PMC10561433", "PMC10694978", "PMC10912221", "PMC11061212"
REDONDO, SCHMID, WEINBERG, SUJATHA = "PMC12565272", "PMC4782303", "PMC5589093", "PMC6907038"

CIT_YOON_N = "The GDHT group (n = 39) received the stroke volume index- and cardiac index-b[ased]… / the control group (n = 36) received the standard care"
CIT_RED_N = "randomized to the GDHT (n = 16) and control group (n = 19)"
CIT_WEIN_ASA = "ASA Class I-II 7 (27%) 7 (27%) ASA Class >= III 19 (73%) 19 (73%)"
CIT_SUJ_N = "306 patients, with 102 in each group, were enrolled"

OVERLAY = {
    # ---- erratas da MA (fonte contradiz a tabela publicada) ----
    (YOON, "n_randomizados_gdft"): dict(veredito="errata-ma", valor_fonte="39", cit=CIT_YOON_N,
                                        nota="MA publicou 36 — braços trocados na tabela de características"),
    (YOON, "n_randomizados_controle"): dict(veredito="errata-ma", valor_fonte="36", cit=CIT_YOON_N,
                                            nota="MA publicou 39 — braços trocados"),
    (REDONDO, "n_randomizados_gdft"): dict(veredito="errata-ma", valor_fonte="16", cit=CIT_RED_N,
                                           nota="MA publicou 19 — braços trocados"),
    (REDONDO, "n_randomizados_controle"): dict(veredito="errata-ma", valor_fonte="19", cit=CIT_RED_N,
                                               nota="MA publicou 16 — braços trocados"),
    (WEINBERG, "asa_gdft"): dict(veredito="errata-ma", valor_fonte="I-II: 7 (27%); >=III: 19 (73%)",
                                 cit=CIT_WEIN_ASA, nota="MA publicou 'Not stated'; a tabela do artigo reporta"),
    (WEINBERG, "asa_controle"): dict(veredito="errata-ma", valor_fonte="I-II: 7 (27%); >=III: 19 (73%)",
                                     cit=CIT_WEIN_ASA, nota="MA publicou 'Not stated'"),
    (WU, "uso_inotropico"): dict(veredito="nao-sustentada", valor_fonte="NR",
                                 cit="(nenhuma menção a vasopressor/inotrópico/dopamina/fenilefrina no texto integral)",
                                 nota="MA publicou 'Lower in GDFT' sem sustentação no texto do primário"),
    (SUJATHA, "asa_gdft"): dict(veredito="nao-sustentada", valor_fonte="NR (elegibilidade ASA I-II; distribuição não reportada)",
                                cit="Patients … belonging to ASA I and II physical status … were included",
                                nota="MA publicou '95:105' sem sustentação no texto; célula do controle corrompida por Excel ('2 days, 11:42:00')"),
    (SUJATHA, "asa_controle"): dict(veredito="nao-sustentada", valor_fonte="NR",
                                    cit="Demographic data, ASA PS … were comparable (sem números)",
                                    nota="célula da MA corrompida por formatação de hora do Excel"),
    # ---- divergência definicional (randomizados vs analisados) ----
    (SUJATHA, "n_randomizados_gdft"): dict(veredito="divergencia-definicional",
                                           valor_fonte="204 randomizados (102 FloTrac + 102 PVI)", cit=CIT_SUJ_N,
                                           nota="MA usou analisados (200); aceitar 204, 200, ou 102+102"),
    (SUJATHA, "n_randomizados_controle"): dict(veredito="divergencia-definicional",
                                               valor_fonte="102 randomizados", cit=CIT_SUJ_N,
                                               nota="MA usou analisados (101); aceitar 102 ou 101"),
    # ---- confirmadas com citação nova ----
    (SUN, "uso_inotropico"): dict(veredito="literal", valor_fonte="GDFT 18 (36%) vs controle 27 (54%)",
                                  cit="Vasopressor or inotrope, n (%) 18 (36) 27 (54) 0.072",
                                  nota="'Lower in GDFT' da MA é direção correta (p=0,072)"),
    (WEINBERG, "uso_inotropico"): dict(veredito="confirmada-qualitativa", valor_fonte="mais frequente no GDT",
                                       cit="vasoactive medications were used more frequently",
                                       nota="MA 'Higher in GDFT' confirmada"),
    (SUN, "tempo_flatus_gdft"): dict(veredito="derivavel-conversao", valor_fonte="mediana 28.2 h (9.2-48.0)",
                                     cit="shorten time to first flatus by 11 h (P = 0.009)",
                                     nota="MA converteu mediana(IIQ)->média±DP (48±12 vs 59±14; diferença de 11 h bate)"),
    (SUN, "tempo_flatus_controle"): dict(veredito="derivavel-conversao", valor_fonte="mediana 39.4 h (24.9-67.5)",
                                         cit="shorten time to first flatus by 11 h (P = 0.009)",
                                         nota="conversão meta-analítica; transcrição da mediana também é correta"),
    (REDONDO, "fluido_total_controle"): dict(veredito="derivavel-arredondamento", valor_fonte="2853.13 ± 1432.18",
                                             cit="Total volume infused (mL) 2853.13 ± 1432.18 1125.79 ± 751.2"),
    (REDONDO, "perda_sanguinea_controle"): dict(veredito="derivavel-arredondamento", valor_fonte="728.13 ± 618.6…",
                                                cit="Blood loss was significantly higher in the control group than in GDHT group (728.13 ± 618.…"),
    # ---- inferências razoáveis da MA (fonte não enumera; NR do modelo também é correto) ----
    **{(pm, c): dict(veredito="ma-inferiu", valor_fonte="0 (cirurgia aberta; fonte não enumera laparoscopia)",
                     cit=cit, nota="aceitar '0' ou 'NR'")
       for pm, cit in [(YOON, "undergoing open radical cystectomy"), (CASTRO, "elective open abdominal surgeries"),
                       (REDONDO, "scheduled for open large liver resection"), (SUJATHA, "elective open major bowel surgery"),
                       (SCHMID, "major abdominal surgery (via não explicitada)"), (WEINBERG, "(via não explicitada no texto)")]
       for c in ("laparoscopia_gdft", "laparoscopia_controle")},
    (WU, "laparoscopia_gdft"): dict(veredito="ma-inferiu", valor_fonte="todos (cirurgia laparoscópica)",
                                    cit="Laparoscopic radical resection of colorectal cancer", nota="aceitar 58/'todos'/'NR'"),
    (WU, "laparoscopia_controle"): dict(veredito="ma-inferiu", valor_fonte="todos (cirurgia laparoscópica)",
                                        cit="Laparoscopic radical resection of colorectal cancer", nota="aceitar 56/'todos'/'NR'"),
    # ---- rótulos de cirurgia ----
    (WU, "tipo_cirurgia"): dict(veredito="rotulo-razoavel", valor_fonte="ressecção laparoscópica radical de câncer colorretal",
                                cit="Laparoscopic radical resection of colorectal cancer"),
    (CASTRO, "tipo_cirurgia"): dict(veredito="rotulo-impreciso-ma",
                                    valor_fonte="cirurgias abdominais abertas eletivas (inclui hepatectomia, gastrectomia, Whipple…)",
                                    cit="elective open abdominal surgeries",
                                    nota="'All major bowel surgeries' da MA é estreito demais"),
    (REDONDO, "tipo_cirurgia"): dict(veredito="rotulo-razoavel", valor_fonte="ressecção hepática aberta de grande porte",
                                     cit="scheduled for open large liver resection (two or more liver segments)"),
    (WEINBERG, "tipo_cirurgia"): dict(veredito="rotulo-razoavel", valor_fonte="cirurgia pancreaticoduodenal",
                                      cit="(ensaio de duodenopancreatectomia)"),
    (SCHMID, "asa_gdft"): dict(veredito="confirmada-nr", valor_fonte="NR (elegibilidade ASA 1-3; distribuição não reportada)",
                               cit="ASA physical status classification 1-3 undergoing major non-cardiac surgery"),
    (SCHMID, "asa_controle"): dict(veredito="confirmada-nr", valor_fonte="NR",
                                   cit="ASA physical status classification 1-3"),
    # ---- pendentes (fora de pontuação até adjudicação final) ----
    (YOON, "uso_inotropico"): dict(veredito="pendente-adjudicacao",
                                   nota="MA 'No difference'; resultado comparativo não localizado no texto"),
    (SUN, "ileo_pos_op_gdft"): dict(veredito="pendente-adjudicacao", nota="MA 2 (4.0%); possivelmente derivado do I-FEED"),
    (SUN, "ileo_pos_op_controle"): dict(veredito="pendente-adjudicacao", nota="MA 16 (32.0%); idem"),
    (CASTRO, "ileo_pos_op_gdft"): dict(veredito="pendente-adjudicacao", nota="MA 6 (14.0%); termo 'ileus' ausente do texto"),
    (CASTRO, "ileo_pos_op_controle"): dict(veredito="pendente-adjudicacao", nota="MA 19 (45.2%); idem"),
    (REDONDO, "perda_sanguinea_gdft"): dict(veredito="pendente-adjudicacao", nota="MA 292.6 ± 274.1; valor literal não conferido"),
}


def main():
    draft = json.loads((D1 / "verificacao-draft.json").read_text(encoding="utf-8"))
    oficial = {}
    contas = {}
    for pm, cels in draft.items():
        oficial[pm] = {}
        for campo, c in cels.items():
            ov = OVERLAY.get((pm, campo))
            if ov:
                reg = dict(ma=c.get("ma"), **ov)
            elif c["status"] == "literal":
                cit = next(iter(c.get("achados", {}).values()), [""])[0]
                reg = dict(ma=c.get("ma"), veredito="literal", valor_fonte=c.get("ma"), cit=cit[:220])
            elif c["status"] == "equivalencia":
                eq = (c.get("equivalencias") or [{}])[0]
                cit = eq.get("trecho") or next(iter(c.get("achados", {}).values()), [""])[0]
                reg = dict(ma=c.get("ma"), veredito="derivavel", valor_fonte=c.get("ma"),
                           regra=eq.get("regra", "parte literal"), cit=str(cit)[:220])
            elif c["status"] == "sem-valor-na-ma":
                reg = dict(ma=c.get("ma"), veredito="sem-valor-na-ma")
            else:
                reg = dict(ma=c.get("ma"), veredito="pendente-adjudicacao")
            oficial[pm][campo] = reg
            contas[reg["veredito"]] = contas.get(reg["veredito"], 0) + 1
    (D1 / "gabarito-oficial.json").write_text(
        json.dumps(dict(
            _metodo="Emenda 4: cada célula verificada na fonte primária original; citação literal obrigatória. "
                    "Vereditos manuais em OVERLAY (gerar-gabarito-oficial.py, público).",
            celulas=oficial), ensure_ascii=False, indent=1), encoding="utf-8")
    print("gabarito-oficial.json gerado")
    for k, v in sorted(contas.items(), key=lambda x: -x[1]):
        print(f"  {k:<26} {v}")


if __name__ == "__main__":
    main()

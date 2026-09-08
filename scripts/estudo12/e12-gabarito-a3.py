# -*- coding: utf-8 -*-
"""Constrói a chave graduável da âncora 3, no esquema que os corretores já consomem.

Instrumento 7 da §8 do protocolo do Estudo 12. `ancora3-camada1.json` é um registro de investigação:
guarda como a camada 1 foi recuperada, as discrepâncias e os cenários. Não é uma régua. Este script
produz a régua, no mesmo esquema de `dados/estudo1/gabarito-oficial.json`:

    {"celulas": {tid: {campo: {ma, veredito, valor_fonte, cit, nota}}}}

Nada aqui é aceito de palavra. O script falha, e não grava, se qualquer uma destas conferências cair:

  1. as células da camada 1 têm de bater com `ancora3-camada1.json`, que foi verificado por
     reconstrução aritmética da Figura 3 (48 de 48);
  2. cada citação tem de existir **literalmente** no primário que ela nomeia;
  3. a redução multi-braço do Shaker, aplicada às linhas da fonte, tem de devolver as células da
     camada 2 que a §5 do protocolo congela;
  4. os percentuais que a fonte publica têm de reconstituir as contagens, e vice-versa, dentro de
     meio ponto;
  5. as 32 células graduáveis têm de estar todas presentes, sem buraco e sem sobra.

Vereditos usados, os mesmos da âncora 1: `literal` (a revisão publicou o que a fonte diz),
`errata-ma` (a revisão diverge da fonte, e a fonte decide).
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
PRIM = RAIZ / "dados" / "estudo11" / "primarios"
D12 = RAIZ / "dados" / "estudo12"

# ------------------------------------------------------------------ os braços, como a fonte os publica
# (tid, arquivo, rótulo do ensaio, [braços], janela do desfecho na fonte, citação)
FONTE = [
    dict(tid="luissilva2024", arq="PMC11514138.xml", ensaio="Luis-Silva, 2024", janela="30 dias",
         cit="mortality rate in 30 days of 47% versus 61% in the Control group",
         bracos=[dict(braco="mb", papel="azul", letra=None, dose=None, papel_norm="azul", rotulo_fonte="MB group", eventos=9, n=19, pct="47"),
                 dict(braco="ct", papel="controle", letra=None, dose=None, papel_norm="controle", rotulo_fonte="Control group", eventos=14, n=23, pct="61")]),
    dict(tid="shaker2025", arq="PMC11707904.xml", ensaio="Shaker, 2025", janela="28 dias",
         cit="Mortality rate 14 (46.7%) 9 (30.0%) 6 (20.0%)",
         bracos=[dict(braco="ct", papel="placebo (grupo A)", letra='A', dose=None, papel_norm="controle", rotulo_fonte="Group A", eventos=14, n=30, pct="46.7"),
                 dict(braco="mb_baixa", papel="azul 1 mg/kg (grupo B)", letra='B', dose=1.0, papel_norm="azul", rotulo_fonte="Group B", eventos=9, n=30, pct="30.0"),
                 dict(braco="mb_alta", papel="azul 4 mg/kg (grupo C)", letra='C', dose=4.0, papel_norm="azul", rotulo_fonte="Group C", eventos=6, n=30, pct="20.0")]),
    dict(tid="ibarra2023", arq="PMC10010212.xml", ensaio="Ibarra-Estrada, 2023", janela="28 dias",
         cit="Mortality at 28 days",
         bracos=[dict(braco="mb", papel="azul", letra=None, dose=None, papel_norm="azul", rotulo_fonte="MB", eventos=15, n=45, pct="33"),
                 dict(braco="ct", papel="controle", letra=None, dose=None, papel_norm="controle", rotulo_fonte="Control", eventos=21, n=46, pct="46")]),
    dict(tid="aguilar2016", arq="aguilar-2016-medcrit.txt", ensaio="Aguilar, 2016",
         janela="alta da UTI e 21 dias",
         cit="en el grupo A la mortalidad al egreso fue de 20.0% y no varió a los 21 días, "
             "a diferencia del grupo C, donde al egreso la mortalidad fue de 36.6%",
         bracos=[dict(braco="mb", papel="azul (grupo A)", letra='A', dose=None, papel_norm="azul", rotulo_fonte="grupo A", eventos=6, n=30, pct="20.0"),
                 dict(braco="ct", papel="controle (grupo C)", letra='C', dose=None, papel_norm="controle", rotulo_fonte="grupo C", eventos=11, n=30, pct="36.6")]),
    dict(tid="kirov2001", arq="kirov2001.txt", ensaio="Kirov, 2001", janela="28 dias",
         cit="Survivors at day 28",
         bracos=[dict(braco="mb", papel="azul", letra=None, dose=None, papel_norm="azul", rotulo_fonte="MB group", eventos=5, n=10, pct=None,
                      nota="a fonte publica SOBREVIVENTES em 28 dias (5); os mortos são 10-5"),
                 dict(braco="ct", papel="controle", letra=None, dose=None, papel_norm="controle", rotulo_fonte="C group", eventos=7, n=10, pct=None,
                      nota="a fonte publica SOBREVIVENTES em 28 dias (3); os mortos são 10-3")]),
    dict(tid="levin2004", arq="levin2004.txt", ensaio="Levin, 2004", janela="pós-operatório",
         cit="There were no deaths in those treated with MB; the 6 deceased patients were in the "
             "placebo group",
         bracos=[dict(braco="mb", papel="azul", letra=None, dose=None, papel_norm="azul", rotulo_fonte="Methylene Blue", eventos=0, n=28, pct=None),
                 dict(braco="ct", papel="placebo", letra=None, dose=None, papel_norm="controle", rotulo_fonte="Control", eventos=6, n=28, pct="21.4")]),
    dict(tid="dong2025", arq="PMC12751372.xml", ensaio="Dong, 2025", janela="28 dias",
         cit="Mortality at 28 days",
         bracos=[dict(braco="mb", papel="azul", letra=None, dose=None, papel_norm="azul", rotulo_fonte="MB group", eventos=9, n=36, pct="25.0"),
                 dict(braco="ct", papel="controle", letra=None, dose=None, papel_norm="controle", rotulo_fonte="Control", eventos=15, n=36, pct="41.7")]),
    dict(tid="memis2002", arq="memis2002.txt", ensaio="Memis, 2002", janela="intra-hospitalar",
         cit="The overall hospital mortality rate was similar in both groups",
         bracos=[dict(braco="mb", papel="azul", letra=None, dose=None, papel_norm="azul", rotulo_fonte="MB group", eventos=4, n=15, pct=None,
                      nota="a fonte não publica contagem por braço; contada na Tabela 1, "
                           "paciente a paciente"),
                 dict(braco="ct", papel="controle", letra=None, dose=None, papel_norm="controle", rotulo_fonte="control group", eventos=4, n=15, pct=None,
                      nota="idem")]),
]

# ------------------------------------------------------------------ redução multi-braço (§5, A3-D1)
# ---------------------------------------------------------------- janela do desfecho, por ensaio
# A analise e rotulada 28 a 30 dias, mas nem todo ensaio publica essa janela. A regra sai do
# reconhecedor generico e vira declaracao congelada, ensaio a ensaio: o que se ACEITA e o que se
# RECUSA. O Aguilar aceita 21 dias por decisao da §5 (A3-D5), nao por acaso de regex; o Dong
# recusa 90 dias, que ele tambem publica. Somar atraves de janelas nunca e permitido.
JANELAS = {
    "luissilva2024": dict(aceita=r"\b30\b|30[- ]?day|30 dias", recusada=None),
    "shaker2025": dict(aceita=r"\b28\b|28[- ]?day|28 dias", recusada=None),
    "ibarra2023": dict(aceita=r"\b28\b|28[- ]?day|28 dias", recusada=None),
    "aguilar2016": dict(aceita=r"\b21\b|21[- ]?day|21 d[ií]as|discharge|egreso|alta", recusada=r"\b28\b|\b90\b"),
    "kirov2001": dict(aceita=r"\b28\b|28[- ]?day|28 dias", recusada=None),
    "levin2004": dict(aceita=r"hospital|post-?op|p[oó]s-?op|in-?hospital|surgery|cirurg|discharge", recusada=None),
    "dong2025": dict(aceita=r"\b28\b|28[- ]?day|28 dias", recusada=r"\b90\b|90[- ]?day"),
    "memis2002": dict(aceita=r"hospital|in-?hospital|icu|discharge", recusada=None),
}

REDUCAO = {"shaker2025": dict(
    mb=["mb_baixa", "mb_alta"], ct=["ct"],
    regra="os dois braços ativos somados contra o controle compartilhado: 15/60 contra 14/30")}

falhas = []


def texto(arq):
    t = io.open(PRIM / arq, encoding="utf-8", errors="replace").read()
    if arq.endswith(".xml"):
        t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)


def reduz(f):
    """As duas células de análise do ensaio, aplicando a regra congelada quando há mais de dois braços."""
    por = {b["braco"]: b for b in f["bracos"]}
    r = REDUCAO.get(f["tid"])
    if not r:
        return {k: (por[k]["eventos"], por[k]["n"]) for k in ("mb", "ct")}
    return {lado: (sum(por[b]["eventos"] for b in r[lado]), sum(por[b]["n"] for b in r[lado]))
            for lado in ("mb", "ct")}


# ------------------------------------------------------------------ 1. camada 1, do registro verificado
camada1 = {}
for e in json.loads(io.open(D12 / "ancora3-camada1.json", encoding="utf-8").read())["estudos"]:
    camada1[e["estudo"]] = (e["eventos_mb"], e["n_mb"], e["eventos_st"], e["n_st"])

print("1. citações, conferidas literalmente no primário")
for f in FONTE:
    t = texto(f["arq"])
    achou = re.sub(r"\s+", " ", f["cit"]) in t
    if not achou:
        falhas.append(f"citação de {f['ensaio']} não encontrada em {f['arq']}")
    print(f"  {'ok  ' if achou else 'ERRO'} {f['ensaio']:22s} {f['cit'][:58]}")

print("\n1b. rotulos dos bracos, conferidos literalmente no primario")
for f in FONTE:
    t = texto(f["arq"])
    rots = [b["rotulo_fonte"] for b in f["bracos"]]
    if len(set(r.lower() for r in rots)) != len(rots):
        falhas.append(f"{f['ensaio']}: rotulos de braco repetidos {rots}")
    for b in f["bracos"]:
        pad = re.escape(b["rotulo_fonte"]).replace(chr(92) + chr(92) + " ", r"\s+")
        achou = re.search(pad, t, re.I) is not None
        if not achou:
            falhas.append(f"{f['ensaio']}: rotulo {b['rotulo_fonte']!r} nao esta no primario")
        print(f"  {'ok  ' if achou else 'ERRO'} {f['ensaio']:22s} {b['papel']:24s} -> {b['rotulo_fonte']!r}")

print("\n1c. identidade estrutural dos bracos: unica dentro do ensaio")
for f in FONTE:
    letras = [b.get("letra") for b in f["bracos"] if b.get("letra")]
    doses = [b.get("dose") for b in f["bracos"] if b.get("dose") is not None]
    papeis = [b["papel_norm"] for b in f["bracos"]]
    problemas = []
    if len(letras) != len(set(letras)):
        problemas.append(f"letras repetidas {letras}")
    if len(doses) != len(set(doses)):
        problemas.append(f"doses repetidas {doses}")
    # o papel so precisa ser unico quando NAO ha letra nem dose para desempatar
    if not letras and not doses and len(papeis) != len(set(papeis)):
        problemas.append(f"papeis repetidos sem letra nem dose para desempatar {papeis}")
    if not all(p in ("azul", "controle") for p in papeis):
        problemas.append(f"papel_norm fora do vocabulario {papeis}")
    if problemas:
        falhas.append(f"{f['ensaio']}: " + "; ".join(problemas))
    ids = ", ".join(f"{b['braco']}[{b.get('letra') or '-'}/{b.get('dose') or '-'}/{b['papel_norm']}]"
                    for b in f["bracos"])
    print(f"  {'ok  ' if not problemas else 'ERRO'} {f['ensaio']:22s} {ids}")

print("\n2. percentual da fonte contra a contagem, nos braços em que a fonte publica os dois")
for f in FONTE:
    for b in f["bracos"]:
        if b["pct"] is None:
            continue
        casas = len(b["pct"].split(".")[1]) if "." in b["pct"] else 0
        calc = round(100 * b["eventos"] / b["n"], casas)
        bate = abs(calc - float(b["pct"])) <= 0.5
        if not bate:
            falhas.append(f"{f['ensaio']} {b['braco']}: {b['eventos']}/{b['n']} = {calc} != {b['pct']}")
        print(f"  {'ok  ' if bate else 'ERRO'} {f['ensaio']:22s} {b['papel']:24s} "
              f"{b['eventos']:3d}/{b['n']:<3d} = {calc:6.1f}%  publicado {b['pct']}%")

print("\n3. redução aplicada, contra a camada 1 da revisão")
celulas, bracos_fonte = {}, {}
for f in FONTE:
    a = reduz(f)
    c1 = camada1[f["ensaio"]]
    cel = {}
    for lado, i in (("mb", 0), ("ct", 2)):
        ev_f, n_f = a[lado]
        ev_ma, n_ma = c1[i], c1[i + 1]
        for campo, vf, vma in ((f"eventos_{lado}", ev_f, ev_ma), (f"n_{lado}", n_f, n_ma)):
            nota = ""
            if str(vf) != str(vma):
                nota = REDUCAO[f["tid"]]["regra"] if f["tid"] in REDUCAO else \
                    "a revisão divergiu da fonte; a fonte decide"
            cel[campo] = dict(ma=str(vma), veredito="literal" if str(vf) == str(vma) else "errata-ma",
                              valor_fonte=str(vf), cit=f["cit"], nota=nota)
    celulas[f["tid"]] = cel
    bracos_fonte[f["tid"]] = dict(ensaio=f["ensaio"], primario=f["arq"], janela=f["janela"],
                                  janela_aceita=JANELAS[f["tid"]]["aceita"],
                                  janela_recusada=JANELAS[f["tid"]]["recusada"],
                                  cit=f["cit"], bracos=f["bracos"])
    div = sum(1 for k, v in cel.items() if v["veredito"] == "errata-ma")
    print(f"  {f['ensaio']:22s} fonte {a['mb'][0]}/{a['mb'][1]} · {a['ct'][0]}/{a['ct'][1]}"
          f"   revisão {c1[0]}/{c1[1]} · {c1[2]}/{c1[3]}   "
          f"{'confere' if div == 0 else str(div) + ' células divergem'}")

# a redução do Shaker tem de dar exatamente o que a §5 congela
esp = reduz(next(f for f in FONTE if f["tid"] == "shaker2025"))
if esp != {"mb": (15, 60), "ct": (14, 30)}:
    falhas.append(f"a redução do Shaker deu {esp}, e a §5 congela 15/60 contra 14/30")
print(f"\n4. regra multi-braço do Shaker: {esp['mb'][0]}/{esp['mb'][1]} contra "
      f"{esp['ct'][0]}/{esp['ct'][1]}  {'ok' if not falhas or esp == {'mb': (15,60), 'ct': (14,30)} else 'ERRO'}")

print("\n4b. janelas declaradas: regex valida, e a janela do ensaio casa a aceita")
for f in FONTE:
    j = JANELAS[f["tid"]]
    try:
        re.compile(j["aceita"])
        if j["recusada"]:
            re.compile(j["recusada"])
    except re.error as e:
        falhas.append(f"{f['ensaio']}: regex de janela invalida: {e}")
        continue
    casa = bool(re.search(j["aceita"], f["janela"], re.I))
    choca = bool(j["recusada"] and re.search(j["recusada"], f["janela"], re.I))
    if not casa or choca:
        falhas.append(f"{f['ensaio']}: a janela do gabarito {f['janela']!r} nao casa a aceita "
                      f"ou casa a recusada")
    print(f"  {'ok  ' if casa and not choca else 'ERRO'} {f['ensaio']:22s} {f['janela']:22s} "
          f"aceita={j['aceita'][:30]}")

n_cel = sum(len(v) for v in celulas.values())
print(f"\n5. células graduáveis: {n_cel} (o protocolo congela 32)")
if n_cel != 32:
    falhas.append(f"{n_cel} células graduáveis, e o protocolo congela 32")

print("\n" + "=" * 78)
if falhas:
    print("NÃO GRAVADO. Falhas:")
    for x in falhas:
        print("  -", x)
    sys.exit(1)

saida = dict(
    _metodo=("Chave graduável da âncora 3 (PMC13302755), duas camadas. `ma` é a célula "
             "publicada, recuperada da Figura 3 e verificada por reconstrução aritmética "
             "(48 de 48 valores impressos previstos a partir de 16 lidos); ela tem procedência mas "
             "não tem citação, porque vive num raster. `valor_fonte` é o valor "
             "verificado na fonte, com `cit` literal. A correção é sempre contra "
             "`valor_fonte`. Produzido por scripts/estudo12/e12-gabarito-a3.py."),
    _reducao_multibraco=REDUCAO,
    _janelas=("A análise é rotulada 28 a 30 dias. As janelas por ensaio estão em "
              "bracos_da_fonte; a do Aguilar é de 21 dias, e a §5 do protocolo (A3-D5) congela o uso "
              "dela com a exclusão rodada como sensibilidade pré-registrada."),
    celulas=celulas, bracos_da_fonte=bracos_fonte)
io.open(D12 / "gabarito-a3.json", "w", encoding="utf-8").write(
    json.dumps(saida, ensure_ascii=False, indent=2) + "\n")
print(f"GRAVADO: dados/estudo12/gabarito-a3.json — {n_cel} células, "
      f"{sum(1 for c in celulas.values() for v in c.values() if v['veredito'] == 'errata-ma')} errata-ma")
print("=" * 78)

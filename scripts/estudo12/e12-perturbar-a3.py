# -*- coding: utf-8 -*-
"""Constrói o corpus perturbado e o selo da âncora 3. Instrumento 9 da §8.

O que a perturbação faz. Os primários desta âncora vão de 2001 a 2025, quase todos dentro da janela de
treino de qualquer modelo do elenco. Sem deslocar nada, acertar "6 mortes de 30" não distingue ler de
lembrar. A perturbação desloca valores-chave no corpus que o modelo lê; o modelo nunca vê o mapa.

O que é diferente aqui, e a §6 do protocolo declara. O operador congelado escolhe candidatos por uma
busca própria e desloca o valor. Nesta âncora os valores-chave são contagens de eventos de um dígito,
e nenhuma é deslocável: o operador exige que o novo valor esteja ausente do texto, e um inteiro pequeno
deslocado cai noutro inteiro pequeno que ocorre dezenas de vezes. Então a âncora 3 desloca o
**denominador por braço** e **recomputa o percentual dependente**, de modo que o artigo continue
coerente consigo mesmo — 9 de 41 É 22,0% — enquanto um denominador recitado (36) fica detectável.

Duas coisas mudam em relação às âncoras 1 e 2, e as duas estão no protocolo:
  · a SELEÇÃO passa a ser por papel no gabarito, e não pela busca de candidatos do operador;
  · o percentual dependente é recomputado, o que o operador congelado nunca fez.
A regra de deslocamento em si — 5 a 15%, mesmas casas, ausente do texto — é a congelada, importada.

Nada é gravado se qualquer conferência cair. As conferências são estas:
  1. o novo denominador e cada percentual recomputado, ausentes do texto original, com a MESMA
     fronteira que a lente usa;
  2. braços que compartilham denominador recebem o mesmo deslocamento (o operador troca todas as
     ocorrências, não uma escolhida);
  3. nenhum par do selo de um ensaio colide com outro par do mesmo ensaio, em nenhuma direção;
  4. o denominador deslocado não ocorre em contexto de janela de desfecho (dia, semana, mês) —
     a ficha pergunta o ponto no tempo, e trocar um denominador que também é uma janela mudaria a
     resposta a outra pergunta. Contexto de minuto ou hora é registrado como aviso, não reprova;
  5. ida e volta exata: a lente aplicada ao texto perturbado devolve o texto original, caractere a
     caractere. É a conferência mais forte das cinco, porque falha se qualquer par se atropelar.

Coerência do artigo inteiro, corrigida em 2026-09-08. A primeira versão recomputava só o percentual do
desfecho graduado. Isso deixava o artigo incoerente em toda parte: no Dong, a linha de 90 dias seguia
dizendo "12 (33,3%)" com o denominador já em 41, quando 12 de 41 é 29,3%. Foram 63 percentuais assim,
em quatro ensaios — exatamente o defeito pelo qual a §6 rejeitou deslocar o percentual sozinho. Agora
**todo** percentual do artigo que deriva do denominador deslocado é recomputado, no contexto "a (p)" em
que aparece, e não globalmente: uma troca global de "75" acertaria também "75 anos". O que sobra —
ocorrências do percentual original fora desse contexto — vai gravado em `vazamento_residual`, campo que
o formato de selo congelado já previa.
"""
import hashlib
import importlib.util
import io
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
AQUI = Path(__file__).resolve().parent


def carrega(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P = carrega("pert", RAIZ / "scripts" / "estudo1" / "perturbar.py")   # regra de deslocamento congelada
L = carrega("lente", AQUI / "e12-lente.py")

PRIM = RAIZ / "dados" / "estudo11" / "primarios"
D12 = RAIZ / "dados" / "estudo12"
ORIG = RAIZ / "corpus" / "estudo12" / "original"
PERT = RAIZ / "corpus" / "estudo12" / "perturbados"

JANELA_DESFECHO = r"(?:d[ií]as?|days?|weeks?|semanas?|months?|meses)"
JANELA_PROCESSO = r"(?:h(?:oras?|ours?|rs?)?|min(?:utos?|utes?)?)"

falhas, avisos = [], []


def texto_de(arq):
    t = io.open(PRIM / arq, encoding="utf-8", errors="replace").read()
    if arq.endswith(".xml"):
        t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"[ \t]+", " ", t).strip()


def ausente(txt, s):
    return not re.search(L.FRONTEIRA_ESQ + re.escape(str(s)) + L.FRONTEIRA_DIR, txt)


def contexto_de(txt, valor, pad_tempo):
    return [m.group(0) for m in re.finditer(
        L.FRONTEIRA_ESQ + re.escape(str(valor)) + L.FRONTEIRA_DIR + r"\s*[-‑]?\s*" + pad_tempo,
        txt, re.I)]


# ------------------------------------------------------------------ números por extenso
_UNI_EN = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
           "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
           "eighteen", "nineteen"]
_DEZ_EN = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 60: "sixty", 70: "seventy",
           80: "eighty", 90: "ninety"}
_UNI_ES = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez",
           "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho",
           "diecinueve"]
_DEZ_ES = {20: "veinte", 30: "treinta", 40: "cuarenta", 50: "cincuenta", 60: "sesenta",
           70: "setenta", 80: "ochenta", 90: "noventa"}


def por_extenso(n):
    """As formas escritas de um inteiro de 0 a 99, por ESTILO.

    O estilo é a chave, e não a posição: "sixty" e "sixty-four" são ambos `en`, "sesenta" e
    "sesenta y cuatro" são ambos `es`. Casar por posição fez "Sixty" virar "sesenta y cuatro".
    """
    n = int(n)
    if not 0 <= n <= 99:
        return {}
    if n < 20:
        return {"en": _UNI_EN[n], "es": _UNI_ES[n]}
    d, u = (n // 10) * 10, n % 10
    if u == 0:
        return {"en": _DEZ_EN[d], "es": _DEZ_ES[d]}
    return {"en": f"{_DEZ_EN[d]}-{_UNI_EN[u]}", "en_espaco": f"{_DEZ_EN[d]} {_UNI_EN[u]}",
            "es": f"{_DEZ_ES[d]} y {_UNI_ES[u]}"}


def _formas_todas(n):
    """Toda forma escrita do valor, nas duas capitalizações — para a conferência dos delatores."""
    f = list(por_extenso(n).values())
    return f + [x[0].upper() + x[1:] for x in f]


def pares_por_extenso(txt, n_orig, n_novo):
    """Pares (forma antiga -> nova) que ocorrem no texto e cuja forma nova está ausente.

    Casamento por estilo, com o inglês com hífen servindo de reserva para o inglês com espaço.
    Cada par entra também na forma capitalizada, porque o artigo abre frase com ela.
    """
    velhas, novas = por_extenso(n_orig), por_extenso(n_novo)
    fora = []
    for estilo, forma in velhas.items():
        alvo = novas.get(estilo) or (novas.get("en") if estilo.startswith("en") else novas.get("es"))
        if not alvo:
            continue
        for a, b in ((forma, alvo), (forma[0].upper() + forma[1:], alvo[0].upper() + alvo[1:])):
            if not re.search(L.FRONTEIRA_ESQ + re.escape(a) + r"(?![\w-])", txt):
                continue
            if re.search(L.FRONTEIRA_ESQ + re.escape(b) + r"(?![\w-])", txt):
                continue
            fora.append((a, b))
    return fora


# ------------------------------------------------------------------ o gabarito manda
G = json.loads(io.open(D12 / "gabarito-a3.json", encoding="utf-8").read())
selo, resumo, textos = {}, [], {}

print(f"{'ensaio':22s} {'n':>4s} {'n′':>5s}  deslocamento e percentuais recomputados")
print("-" * 100)

for tid, f in G["bracos_da_fonte"].items():
    txt = texto_de(f["primario"])

    grupos = {}
    for b in f["bracos"]:
        grupos.setdefault(b["n"], []).append(b)

    registros = []
    for n, membros in sorted(grupos.items()):
        maior_evento = max(b["eventos"] for b in membros)
        escolhido = None
        motivo = "todo n′ admissível já ocorre no texto"
        # o conjunto de deslocamentos que a regra congelada admite: 5 a 15%, para cima e para baixo
        for novo_n in sorted({int(round(n * (1 + s * p / 100))) for p in range(5, 16) for s in (1, -1)}):
            if novo_n == n or novo_n <= maior_evento or novo_n <= 0:
                continue
            if not ausente(txt, novo_n):
                continue
            pcts, ok = {}, True
            for b in membros:
                if b["pct"] is None:
                    continue
                casas = len(b["pct"].split(".")[1]) if "." in b["pct"] else 0
                novo_p = f"{100 * b['eventos'] / novo_n:.{casas}f}"
                if novo_p == b["pct"] or not ausente(txt, novo_p):
                    ok, motivo = False, "n′ livre, mas um percentual recomputado colide com o texto"
                    break
                pcts[b["braco"]] = novo_p
            if ok:
                escolhido = (novo_n, pcts)
                break

        if not escolhido:
            resumo.append((f["ensaio"], n, None, motivo))
            print(f"{f['ensaio']:22s} {n:4d} {'—':>5s}  {motivo}")
            continue

        novo_n, pcts = escolhido
        # conferência 4: o denominador original não pode ser uma janela de desfecho
        janela = contexto_de(txt, n, JANELA_DESFECHO)
        if janela:
            falhas.append(f"{f['ensaio']}: o denominador {n} ocorre como janela de desfecho "
                          f"({janela[0]!r}); deslocá-lo mudaria a resposta do campo de ponto no tempo")
            continue
        proc = contexto_de(txt, n, JANELA_PROCESSO)
        if proc:
            avisos.append(f"{f['ensaio']}: {n} também aparece como duração de processo "
                          f"({', '.join(sorted(set(proc))[:3])}); deslocado junto, por coerência")

        # todo percentual do artigo que deriva deste denominador, no contexto "a (p)" em que aparece
        derivados = {}
        for m in re.finditer(r"(?<![\w.])(\d{1,3}(?:\.0)?)\s*\(\s*(\d{1,3}(?:\.\d+)?)\s*%?\s*\)", txt):
            a_s, p_s = m.group(1), m.group(2)
            a = float(a_s)
            if a > n or a < 0:
                continue
            casas = len(p_s.split(".")[1]) if "." in p_s else 0
            if abs(round(100 * a / n, casas) - float(p_s)) > 0.06:
                continue                                  # não deriva deste denominador
            novo_p = f"{100 * a / novo_n:.{casas}f}"
            if novo_p == p_s or not ausente(txt, novo_p):
                avisos.append(f"{f['ensaio']}: {a_s} ({p_s}) deriva de {n} mas o recomputado "
                              f"{novo_p} colide com o texto; fica incoerente e vai registrado")
                continue
            derivados.setdefault((a_s, p_s), novo_p)

        for forma, alvo in pares_por_extenso(txt, n, novo_n):
            registros.append(dict(campo=f"n_por_braco_{n}_por_extenso", papel="denominador escrito",
                                  original=forma, perturbado=alvo,
                                  contextos=[m.group(0) for m in re.finditer(
                                      r".{0,40}" + L.FRONTEIRA_ESQ + re.escape(forma)
                                      + r"(?![\w-]).{0,40}", txt)][:2]))
        registros.append(dict(campo=f"n_por_braco_{n}", papel="denominador",
                              original=str(n), perturbado=str(novo_n),
                              contextos=[m.group(0) for m in re.finditer(
                                  r".{0,38}" + L.FRONTEIRA_ESQ + str(n) + L.FRONTEIRA_DIR + r".{0,26}",
                                  txt)][:4],
                              contexto_processo=sorted(set(proc))[:3]))
        for (a_s, p_s), novo_p in sorted(derivados.items()):
            ctx_pad = (r"(?<![\w.])" + re.escape(a_s) + r"\s*\(\s*" + re.escape(p_s) + r"\s*%?\s*\)")
            fora = [m.group(0) for m in re.finditer(
                r".{0,30}" + L.FRONTEIRA_ESQ + re.escape(p_s) + L.FRONTEIRA_DIR + r".{0,20}", txt)
                if not re.search(ctx_pad, m.group(0))]
            registros.append(dict(campo=f"pct_derivado_{a_s}_de_{n}", papel="percentual derivado",
                                  original=p_s, perturbado=novo_p, derivado_de=f"{a_s}/{novo_n}",
                                  contexto_restrito=ctx_pad,
                                  contextos=[m.group(0) for m in re.finditer(
                                      r".{0,24}" + ctx_pad + r".{0,18}", txt)][:2],
                                  vazamento_residual=sorted(set(fora))[:3]))
        for b in membros:
            if b["braco"] in pcts:
                registros.append(dict(campo=f"pct_{b['braco']}", papel="percentual recomputado",
                                      original=b["pct"], perturbado=pcts[b["braco"]],
                                      derivado_de=f"{b['eventos']}/{novo_n}",
                                      contextos=[m.group(0) for m in re.finditer(
                                          r".{0,38}" + L.FRONTEIRA_ESQ + re.escape(b["pct"])
                                          + L.FRONTEIRA_DIR + r".{0,26}", txt)][:3]))
        det = " · ".join(f"{b['papel']} {b['eventos']}/{novo_n}"
                         + (f" = {pcts[b['braco']]}%" if b["braco"] in pcts else " (sem % na fonte)")
                         for b in membros)
        resumo.append((f["ensaio"], n, novo_n, ""))
        print(f"{f['ensaio']:22s} {n:4d} {novo_n:5d}  {det}")

    # ── o TOTAL do ensaio anda com os braços ──────────────────────────────────────────────
    # Deixar o total intacto torna o artigo contraditório na mesma frase e, pior, faz a rede de
    # recitação acusar quem RECONCILIOU: um modelo que vê "72 randomized" em dois braços e escreve
    # 36 estaria lendo bem e seria tratado como recitador.
    desloc = {int(r["original"]): int(r["perturbado"])
              for r in registros if r["papel"] == "denominador"}
    if desloc:
        tot_o = sum(b_["n"] for b_ in f["bracos"])
        tot_p = sum(desloc.get(b_["n"], b_["n"]) for b_ in f["bracos"])
        ocorre = len(re.findall(L.FRONTEIRA_ESQ + str(tot_o) + L.FRONTEIRA_DIR, txt))
        if tot_o == tot_p:
            pass                                  # nada a fazer: os braços somam o mesmo
        elif not ocorre:
            avisos.append(f"{f['ensaio']}: o total {tot_o} não é impresso; nada a deslocar")
        elif str(tot_o) in {r["original"] for r in registros}:
            avisos.append(f"{f['ensaio']}: o total {tot_o} já é um denominador de braço; já deslocado")
        elif not ausente(txt, tot_p):
            falhas.append(f"{f['ensaio']}: o total coerente {tot_p} já ocorre no texto; o total "
                          f"{tot_o} ficaria denunciando o denominador original")
        else:
            registros.append(dict(campo="total_do_ensaio", papel="total",
                                  original=str(tot_o), perturbado=str(tot_p),
                                  derivado_de="soma dos denominadores por braço",
                                  ocorrencias=ocorre,
                                  contextos=[m.group(0) for m in re.finditer(
                                      r".{0,42}" + L.FRONTEIRA_ESQ + str(tot_o) + L.FRONTEIRA_DIR
                                      + r".{0,26}", txt)][:4]))
            for forma, alvo in pares_por_extenso(txt, tot_o, tot_p):
                registros.append(dict(campo="total_do_ensaio_por_extenso", papel="total escrito",
                                      original=forma, perturbado=alvo,
                                      contextos=[m.group(0) for m in re.finditer(
                                          r".{0,40}" + L.FRONTEIRA_ESQ + re.escape(forma)
                                          + r"(?![\w-]).{0,40}", txt)][:2]))
            # e os percentuais que derivam do total também
            for m in re.finditer(r"(?<![\w.])(\d{1,3}(?:\.0)?)\s*\(\s*(\d{1,3}(?:\.\d+)?)\s*%?\s*\)", txt):
                a_s, p_s = m.group(1), m.group(2)
                a_v = float(a_s)
                if a_v > tot_o:
                    continue
                casas = len(p_s.split(".")[1]) if "." in p_s else 0
                if abs(round(100 * a_v / tot_o, casas) - float(p_s)) > 0.06:
                    continue
                if any(r["original"] == p_s for r in registros):
                    continue                      # já tratado como derivado de um braço
                novo_p = f"{100 * a_v / tot_p:.{casas}f}"
                if novo_p == p_s or not ausente(txt, novo_p):
                    avisos.append(f"{f['ensaio']}: {a_s} ({p_s}) deriva do total {tot_o} mas o "
                                  f"recomputado {novo_p} colide; fica incoerente e vai registrado")
                    continue
                ctx = (r"(?<![\w.])" + re.escape(a_s) + r"\s*\(\s*" + re.escape(p_s) + r"\s*%?\s*\)")
                registros.append(dict(campo=f"pct_derivado_{a_s}_do_total", papel="percentual derivado",
                                      original=p_s, perturbado=novo_p,
                                      derivado_de=f"{a_s}/{tot_p}", contexto_restrito=ctx,
                                      contextos=[mm.group(0) for mm in re.finditer(
                                          r".{0,24}" + ctx + r".{0,18}", txt)][:2],
                                      vazamento_residual=[]))

    # conferência 3: colisões dentro do selo do ensaio
    pares = [(r["original"], r["perturbado"]) for r in registros]
    for c in L.colisoes(pares):
        falhas.append(f"{f['ensaio']}: colisão no selo — {c}")

    # aplica. Duas passadas, porque as duas classes de par têm alcances diferentes:
    #   · percentual derivado — SÓ dentro do contexto "a (p)" de onde saiu. Uma troca global de "75"
    #     acertaria "75 anos"; o percentual só é dependente do denominador naquele parêntese.
    #   · denominador e percentual do desfecho — globais e com fronteira, como o operador congelado
    #     faz, para que o artigo perturbado fique coerente em toda ocorrência.
    # O derivado vai primeiro: assim a troca global do denominador não encontra um valor recém-escrito.
    pert = txt
    n_sub = 0
    for r in registros:
        if r["papel"] != "percentual derivado":
            continue
        if r["perturbado"] in (r.get("derivado_de", "").split("/")[-1],):
            falhas.append(f"{f['ensaio']}: o percentual recomputado {r['perturbado']} é igual ao "
                          f"denominador deslocado; par recusado")
            continue
        pert, k = re.subn(r["contexto_restrito"],
                          lambda m: m.group(0).replace(r["original"], r["perturbado"]), pert)
        n_sub += k
        if k == 0:
            falhas.append(f"{f['ensaio']}: o par derivado {r['original']}→{r['perturbado']} não casou "
                          f"nenhuma vez no contexto de onde saiu")
    globais = [r for r in registros if r["papel"] != "percentual derivado"]
    pert, k = L.perturba(pert, globais)
    n_sub += k
    volta, _ = L.aplica(pert, [(r["perturbado"], r["original"]) for r in registros])
    if volta != txt:
        falhas.append(f"{f['ensaio']}: a ida e volta não fecha; o selo atropela a si mesmo")
    if registros and n_sub == 0:
        falhas.append(f"{f['ensaio']}: o selo tem pares mas nenhuma substituição foi feita")
    textos[tid] = (txt, pert)
    selo[tid] = registros

print("-" * 100)
com = [r for r in resumo if r[2]]
sem = [r for r in resumo if not r[2]]
print(f"grupos de denominador deslocados: {len(com)} · sem deslocamento possível: {len(sem)}")
print(f"pares no selo: {sum(len(v) for v in selo.values())}")
cobertos = sorted({r[0] for r in com})
print(f"ensaios com alguma prova de leitura ({len(cobertos)}): {', '.join(cobertos)}")

if avisos:
    print("\navisos, registrados no selo e não impeditivos:")
    for a in avisos:
        print("  ·", a)

# conferência 6: nenhum número do texto perturbado reconstrói um denominador ORIGINAL por divisão
print("\nconferência: o texto perturbado não devolve nenhum denominador original por aritmética")
for tid, (txt0, pert) in textos.items():
    f = G["bracos_da_fonte"][tid]
    desloc = {int(r["original"]): int(r["perturbado"])
              for r in (selo.get(tid) or []) if r["papel"] == "denominador"}
    if not desloc:
        continue
    k = len(f["bracos"])
    delatores = []
    for n_o, n_p in desloc.items():
        for mult in range(2, k + 1):
            alvo = n_o * mult
            if alvo == n_p * mult:
                continue
            for m in re.finditer(L.FRONTEIRA_ESQ + str(alvo) + L.FRONTEIRA_DIR + r"[^.]{0,60}", pert):
                if re.search(r"patient|pacient|randomi|aleatoriz|enroll|includ|incluid|subject|"
                             r"divided|allocat|asign", m.group(0), re.I):
                    delatores.append(f"{alvo} (= {n_o}×{mult}) em: …{' '.join(m.group(0).split())[:64]}…")
    for n_o, n_p in desloc.items():
        for mult in range(1, k + 1):
            alvo_n = n_o * mult
            if alvo_n == n_p * mult:
                continue
            for forma in _formas_todas(alvo_n):
                for m in re.finditer(L.FRONTEIRA_ESQ + re.escape(forma) + r"(?![\w-])[^.]{0,60}", pert):
                    if re.search(r"patient|pacient|randomi|aleatoriz|enroll|includ|incluid|subject|"
                                 r"divided|allocat|asign|fulfil|fulﬁl", m.group(0), re.I):
                        delatores.append(f"{forma!r} (= {alvo_n}) em: "
                                         f"…{' '.join(m.group(0).split())[:60]}…")
    if delatores:
        falhas.append(f"{f['ensaio']}: o texto perturbado ainda contém um total que devolve o "
                      f"denominador original — " + delatores[0])
    print(f"  {'ok  ' if not delatores else 'ERRO'} {f['ensaio']:22s} "
          f"{'nenhum delator' if not delatores else delatores[0][:70]}")

print("\n" + "=" * 100)
if falhas:
    print("NÃO GRAVADO. Falhas:")
    for x in falhas:
        print("  -", x)
    sys.exit(1)

# nada tocou o disco até aqui: um corpus meio perturbado que uma falha deixasse para trás seria
# aceito pelo teste de doutrina, e metade da campanha poderia ser extraída de um corpus e corrigida
# contra outro.
ORIG.mkdir(parents=True, exist_ok=True)
PERT.mkdir(parents=True, exist_ok=True)
for tid, (txt0, pert) in textos.items():
    io.open(ORIG / f"{tid}.txt", "w", encoding="utf-8").write(txt0)
    io.open(PERT / f"{tid}.txt", "w", encoding="utf-8").write(pert)

# newline LF e o selo sobre os BYTES do arquivo, nao sobre a string. No Windows a escrita
# padrao traduz a quebra de linha, e o SHA da string nao batia com o do arquivo: quem
# conferisse de fora acharia selo violado num selo intacto.
alvo_selo = D12 / "perturbacoes-a3.json"
corpo = json.dumps(selo, ensure_ascii=False, indent=2, sort_keys=True) + chr(10)
io.open(alvo_selo, "w", encoding="utf-8", newline=chr(10)).write(corpo)
sha = hashlib.sha256(io.open(alvo_selo, "rb").read()).hexdigest()
io.open(D12 / "perturbacoes-a3.sha256", "w", encoding="utf-8",
        newline=chr(10)).write(sha + chr(10))
print("GRAVADO")
print(f"  corpus original    corpus/estudo12/original/       {len(G['bracos_da_fonte'])} arquivos")
print(f"  corpus perturbado  corpus/estudo12/perturbados/    {len(G['bracos_da_fonte'])} arquivos")
print(f"  selo               dados/estudo12/perturbacoes-a3.json")
print(f"  SHA-256 do selo    {sha}")
print("=" * 100)

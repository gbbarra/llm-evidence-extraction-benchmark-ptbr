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


# ------------------------------------------------------------------ o gabarito manda
G = json.loads(io.open(D12 / "gabarito-a3.json", encoding="utf-8").read())
selo, resumo = {}, []

print(f"{'ensaio':22s} {'n':>4s} {'n′':>5s}  deslocamento e percentuais recomputados")
print("-" * 100)

for tid, f in G["bracos_da_fonte"].items():
    txt = texto_de(f["primario"])
    ORIG.mkdir(parents=True, exist_ok=True)
    PERT.mkdir(parents=True, exist_ok=True)
    io.open(ORIG / f"{tid}.txt", "w", encoding="utf-8").write(txt)

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
    io.open(PERT / f"{tid}.txt", "w", encoding="utf-8").write(pert)
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

print("\n" + "=" * 100)
if falhas:
    print("NÃO GRAVADO. Falhas:")
    for x in falhas:
        print("  -", x)
    sys.exit(1)

corpo = json.dumps(selo, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
io.open(D12 / "perturbacoes-a3.json", "w", encoding="utf-8").write(corpo)
sha = hashlib.sha256(corpo.encode("utf-8")).hexdigest()
io.open(D12 / "perturbacoes-a3.sha256", "w", encoding="utf-8").write(sha + "\n")
print("GRAVADO")
print(f"  corpus original    corpus/estudo12/original/       {len(G['bracos_da_fonte'])} arquivos")
print(f"  corpus perturbado  corpus/estudo12/perturbados/    {len(G['bracos_da_fonte'])} arquivos")
print(f"  selo               dados/estudo12/perturbacoes-a3.json")
print(f"  SHA-256 do selo    {sha}")
print("=" * 100)

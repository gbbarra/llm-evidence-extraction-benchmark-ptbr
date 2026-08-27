# -*- coding: utf-8 -*-
"""EXTRAI — Estudo 1: gera as cópias perturbadas dos primários (prova de leitura dupla).

Determinístico (seed fixa por PMCID). Conforme o protocolo §6:
- K=3 números por primário, escolhidos entre valores que aparecem no gabarito da
  âncora E no texto do primário, espalhados por tabelas diferentes quando possível;
- alteração de 5–15%, mesmas casas decimais, sem colidir com valor real do texto;
- todas as ocorrências são substituídas (com fronteira numérica);
- a tabela original↔perturbado fica SELADA (fora do repositório) até a correção.

Saídas (todas fora do versionamento, ver .gitignore):
  corpus/primarios-texto/<PMCID>.txt   — texto plano original (abstract+corpo)
  corpus/perturbados/<PMCID>.txt       — texto perturbado (entrada dos modelos)
  dados/estudo1/perturbacoes-estudo1.json — tabela selada
"""
import json
import random
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
K = 3


def texto_plano(xml_path):
    raw = xml_path.read_text(encoding="utf-8")
    xml = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>", "", raw, count=1)
    root = ET.fromstring(xml)
    # remove listas de referências onde quer que estejam (alguns XMLs embutem no corpo)
    for pai in root.iter():
        for rl in list(pai):
            if rl.tag == "ref-list":
                pai.remove(rl)
    partes = []
    ab = root.find(".//front//abstract")
    if ab is not None:
        partes.append(" ".join(ab.itertext()))
    body = root.find(".//body")
    if body is not None:
        partes.append(" ".join(body.itertext()))
    t = " ".join(partes)
    return re.sub(r"[ \t]+", " ", t.replace("\xa0", " ")).strip()


def numeros_da_celula(valor):
    """Números candidatos de uma célula do gabarito (ex.: '3810.4 ± 2126.9' -> ambos)."""
    if not valor or valor.strip().upper() in ("NR", "NA", "-", ""):
        return []
    return re.findall(r"\d+(?:\.\d+)?", valor)


CAMPOS_CALCULO = re.compile(r"risk ratio|95% ci|mean difference|weight|rr \(|md \(", re.I)

# âncoras semânticas: toda ocorrência do número no texto precisa estar perto de
# uma palavra do campo do gabarito — evita trocar um número igual de outro fato
ANCORAS = [
    (r"total fluid", r"fluid|volume|administer|infus"),
    (r"crystalloid", r"crystalloid|ringer|saline|lactate"),
    (r"colloid", r"colloid|starch|hes\b|albumin|gelatin"),
    (r"blood loss", r"blood loss|bleed|h[ae]morrhage|estimated blood"),
    (r"inotrope", r"inotrop|vasopressor|norepinephrine|ephedrine"),
    (r"lap", r"laparoscop"),
    (r"asa", r"\basa\b"),
    (r"surgery", r"surg|resection|ectomy|procedure"),
]
ANCORAS_TABELA = {
    3: r"randomi|patients|enrolled|allocated|assigned|sample",
    5: r"complicat|morbid",
    6: r"death|mortal|died",
    7: r"stay|\blos\b|hospital|discharge",
    8: r"flatus",
    9: r"oral|intake|diet|feed",
    10: r"bowel|defecat|stool",
    11: r"ileus",
}


def ancora_do_campo(tabela, campo):
    c = campo.lower()
    for chave, pad in ANCORAS:
        if re.search(chave, c):
            return pad
    return ANCORAS_TABELA.get(tabela)


def ocorrencias(texto, valor):
    """Ocorrências do número com fronteira (não pode ser pedaço de outro número
    nem sufixo de palavra/hífen, como COVID-19 ou faixas de páginas)."""
    pad = r"(?<![\w.,\-–])" + re.escape(valor) + r"(?![\w.])"
    return re.findall(pad, texto), pad


def distintivo(valor):
    """Nível: 1 = preciso (≥3 dígitos significativos, ex. 3810.4, 32.8, 1313);
    2 = redondo grande (≥100 com <3 sig., ex. 2700, 200); 3 = pequeno (20–99);
    0 = ambíguo demais. Quanto maior o nível, mais dura a exigência de âncora."""
    if float(valor) < 20:
        return 0
    sig = valor.replace(".", "").rstrip("0") or "0"
    if len(sig) >= 3:
        return 1
    return 2 if float(valor) >= 100 else 3


def variantes(valor):
    """O valor como impresso e com separador de milhar (3810.4 -> 3,810.4)."""
    vs = [valor]
    inteiro = valor.split(".")[0]
    if len(inteiro) > 3:
        com_virgula = ""
        for i, c in enumerate(reversed(inteiro)):
            com_virgula = c + com_virgula
            if (i + 1) % 3 == 0 and i + 1 < len(inteiro):
                com_virgula = "," + com_virgula
        vs.append(com_virgula + (("." + valor.split(".")[1]) if "." in valor else ""))
    return vs


def perturbar_valor(valor, rng, texto):
    """Novo valor a 5–15% do original, mesmas casas, ausente do texto."""
    casas = len(valor.split(".")[1]) if "." in valor else 0
    v = float(valor)
    for _ in range(40):
        fator = rng.uniform(0.05, 0.15) * rng.choice((1, -1))
        novo = round(v * (1 + fator), casas)
        if casas == 0:
            novo = int(novo)
        s = f"{novo:.{casas}f}" if casas else str(novo)
        if s != valor and float(s) > 0 and not ocorrencias(texto, s)[0]:
            return s
    return None


def main():
    gab = json.loads((RAIZ / "dados" / "estudo1" / "gabarito-ma.json").read_text(encoding="utf-8"))
    dir_txt = RAIZ / "corpus" / "primarios-texto"
    dir_pert = RAIZ / "corpus" / "perturbados"
    dir_txt.mkdir(parents=True, exist_ok=True)
    dir_pert.mkdir(parents=True, exist_ok=True)

    # candidatos por estudo: (tabela, campo, número) vindos das células do gabarito
    por_estudo = {}
    for t in gab["tabelas"]:
        if t["numero"] == 2:      # GRADE: julgamento dos revisores, não fato primário
            continue
        for l in t["linhas"]:
            if not l["acesso_aberto"] or not l.get("pmcid"):
                continue
            for campo, valor in l["celulas"].items():
                for num in numeros_da_celula(valor):
                    por_estudo.setdefault(l["pmcid"], []).append(
                        dict(tabela=t["numero"], campo=campo, valor=num))

    # escolhas manuais documentadas (protocolo §6) p/ estudos onde o automático
    # não alcança K; formato: {pmcid: [{tabela, campo, valor}, ...]}
    man_path = RAIZ / "dados" / "estudo1" / "perturbacoes-manuais.json"
    manuais = json.loads(man_path.read_text(encoding="utf-8")) if man_path.exists() else {}

    selo = {}
    for pmcid in sorted(por_estudo):
        xml_path = RAIZ / "corpus" / "primarios" / f"{pmcid}.xml"
        texto = texto_plano(xml_path)
        (dir_txt / f"{pmcid}.txt").write_text(texto, encoding="utf-8")
        rng = random.Random(f"EXTRAI-E1-{pmcid}")
        for m in manuais.get(pmcid, []):
            por_estudo[pmcid].insert(0, dict(tabela=m["tabela"], campo=m["campo"],
                                             valor=m["valor"], manual=True))

        # filtra candidatos: fora colunas de cálculo, anos e números ambíguos;
        # limites de ocorrência mais duros para os menos distintivos
        candidatos = []
        vistos = set()
        for c in por_estudo[pmcid]:
            if c["valor"] in vistos or CAMPOS_CALCULO.search(c["campo"]):
                continue
            vistos.add(c["valor"])
            if c.get("manual"):        # verificado à mão: só conta ocorrências
                nivel, max_ocorr, ancora = -1, 8, None
            else:
                if re.fullmatch(r"(19|20)\d\d", c["valor"]):  # anos
                    continue
                nivel = distintivo(c["valor"])
                if nivel == 0:
                    continue
                max_ocorr = 6 if nivel == 1 else (4 if nivel == 2 else 2)
                ancora = ancora_do_campo(c["tabela"], c["campo"])
            for forma in variantes(c["valor"]):
                achou, pad = ocorrencias(texto, forma)
                if not (1 <= len(achou) <= max_ocorr):
                    continue
                janelas = [m.group(0) for m in
                           re.finditer(r".{0,120}" + pad + r".{0,120}", texto)]
                if ancora:
                    # número preciso: âncora em ≥1 janela; redondo/pequeno: em todas
                    exigencia = any if nivel == 1 else all
                    if not exigencia(re.search(ancora, j, re.I) for j in janelas):
                        continue
                candidatos.append(dict(c, forma=forma, n_ocorr=len(achou),
                                       pad=pad, nivel=nivel))
                break

        # escolha: espalhar por tabelas e preferir os mais distintivos
        candidatos.sort(key=lambda c: (c["nivel"], c["n_ocorr"], -len(c["forma"])))
        escolha, tabelas_usadas, celulas_usadas = [], set(), set()
        while len(escolha) < K:
            restantes = [c for c in candidatos
                         if not any(e["forma"] == c["forma"] for e in escolha)
                         and (c["tabela"], c["campo"]) not in celulas_usadas]
            if not restantes:
                break
            restantes.sort(key=lambda c: (c["tabela"] in tabelas_usadas,
                                          c["nivel"], c["n_ocorr"], -len(c["forma"])))
            c = restantes[0]
            escolha.append(c)
            tabelas_usadas.add(c["tabela"])
            celulas_usadas.add((c["tabela"], c["campo"]))

        pert_texto = texto
        registros = []
        for c in escolha:
            novo = perturbar_valor(c["forma"].replace(",", ""), rng, texto)
            if novo is None:
                continue
            novo_forma = variantes(novo)[-1] if "," in c["forma"] else novo
            contextos = [m.group(0) for m in
                         re.finditer(r".{0,38}" + c["pad"] + r".{0,26}", texto)]
            pert_texto, n_sub = re.subn(c["pad"], novo_forma, pert_texto)
            registros.append(dict(tabela=c["tabela"], campo=c["campo"],
                                  original=c["forma"], perturbado=novo_forma,
                                  ocorrencias_substituidas=n_sub,
                                  contextos=contextos))
        (dir_pert / f"{pmcid}.txt").write_text(pert_texto, encoding="utf-8")
        selo[pmcid] = registros
        campos = ", ".join(f"t{r['tabela']}·{r['campo'][:26]} ({r['original']}→{r['perturbado']}, ×{r['ocorrencias_substituidas']})" for r in registros)
        print(f"{pmcid}: {len(registros)} perturbações — {campos}")
        for r in registros:
            for ctx in r["contextos"]:
                print(f"      [{r['original']}] …{ctx}…")

    out = RAIZ / "dados" / "estudo1" / "perturbacoes-estudo1.json"
    out.write_text(json.dumps(selo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nselada (fora do repo): {out.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()

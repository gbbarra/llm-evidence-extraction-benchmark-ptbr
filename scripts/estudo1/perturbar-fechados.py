# -*- coding: utf-8 -*-
"""EXTRAI E1 — Emenda 2: perturbação do estrato fechado (fronteira corrigida).

Igual ao perturbar.py dos abertos (âncoras semânticas, níveis de distintividade,
curadoria manual, selo fechado), com a fronteira da Emenda 3 consertada:
- número colado a unidade É alcançado ("4088mL");
- hífen de faixa numérica É alcançado ("800-2750");
- hífen precedido de letra segue bloqueado ("COVID-19", páginas "118:19-29" idem via
  bloqueio de dígito-dois-pontos? não: faixas de páginas ficam protegidas pelas âncoras).

Entradas: corpus/fechados-texto/REF*.txt + linhas fechadas do gabarito-ma.json
Saídas (fora do repo): corpus/perturbados-fechados/REF*.txt +
dados/estudo1/perturbacoes-fechados.json (+ manuais em perturbacoes-fechados-manuais.json)
"""
import json
import random
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
D1 = RAIZ / "dados" / "estudo1"
K = 3

ANCORAS = [
    (r"total fluid", r"fluid|volume|administer|infus"),
    (r"crystalloid", r"crystalloid|ringer|saline|lactate|balanced"),
    (r"colloid", r"colloid|starch|hes\b|albumin|gelatin|gelofusine|voluven"),
    (r"blood loss", r"blood loss|bleed|h[ae]morrhage|estimated blood"),
    (r"inotrope", r"inotrop|vasopressor|vasoactive|norepinephrine|noradrenaline|ephedrine|phenylephrine|metaraminol"),
    (r"lap", r"laparoscop"),
    (r"asa", r"\basa\b"),
    (r"surgery", r"surg|resection|ectomy|procedure"),
]
ANCORAS_TABELA = {
    3: r"randomi|patients|enrolled|allocated|assigned|sample|group \(\s*n",
    5: r"complicat|morbid",
    6: r"death|mortal|died|surviv",
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


def ocorre(texto, valor):
    """Spans das ocorrências com a fronteira corrigida (Emenda 2/3)."""
    spans = []
    for m in re.finditer(r"(?<![\d.,])" + re.escape(valor) + r"(?!\d|\.\d)", texto):
        i = m.start()
        antes = texto[i - 1] if i else ""
        if antes.isalpha() or antes == "_":
            continue                       # colado a palavra pela esquerda: fora
        if antes in "-–—":
            antes2 = texto[i - 2] if i >= 2 else ""
            if not antes2.isdigit():
                continue                   # letra-hífen (COVID-19): fora; faixa numérica: ok
        spans.append((m.start(), m.end()))
    return spans


def substitui(texto, valor, novo):
    spans = ocorre(texto, valor)
    out, ultimo = [], 0
    for a, b in spans:
        out.append(texto[ultimo:a]); out.append(novo); ultimo = b
    out.append(texto[ultimo:])
    return "".join(out), len(spans)


def numeros_da_celula(valor):
    if not valor or str(valor).strip().upper() in ("NR", "NA", "-", "", "NOT STATED"):
        return []
    return re.findall(r"\d+(?:\.\d+)?", str(valor))


def distintivo(valor):
    if float(valor) < 20:
        return 0
    sig = valor.replace(".", "").rstrip("0") or "0"
    if len(sig) >= 3:
        return 1
    return 2 if float(valor) >= 100 else 3


def perturbar_valor(valor, rng, texto):
    casas = len(valor.split(".")[1]) if "." in valor else 0
    v = float(valor)
    for _ in range(40):
        fator = rng.uniform(0.05, 0.15) * rng.choice((1, -1))
        novo = round(v * (1 + fator), casas)
        if casas == 0:
            novo = int(novo)
        s = f"{novo:.{casas}f}" if casas else str(novo)
        if s != valor and float(s) > 0 and not ocorre(texto, s):
            return s
    return None


def main():
    gab = json.loads((D1 / "gabarito-ma.json").read_text(encoding="utf-8"))
    dir_txt = RAIZ / "corpus" / "fechados-texto"
    dir_pert = RAIZ / "corpus" / "perturbados-fechados"
    dir_pert.mkdir(parents=True, exist_ok=True)

    por_estudo = {}
    for t in gab["tabelas"]:
        if t["numero"] in (1, 2):
            continue
        for l in t["linhas"]:
            pid = l.get("pmcid") or ""
            if not pid.startswith("REF"):
                continue
            for campo, valor in l["celulas"].items():
                for num in numeros_da_celula(valor):
                    por_estudo.setdefault(pid, []).append(
                        dict(tabela=t["numero"], campo=campo, valor=num))

    man_path = D1 / "perturbacoes-fechados-manuais.json"
    manuais = json.loads(man_path.read_text(encoding="utf-8")) if man_path.exists() else {}
    excluir = manuais.get("_excluir", {})

    selo = {}
    for rid in sorted(por_estudo):
        texto = (dir_txt / f"{rid}.txt").read_text(encoding="utf-8")
        rng = random.Random(f"EXTRAI-E1-FECH-{rid}")
        por_estudo[rid] = [c for c in por_estudo[rid]
                           if c["valor"] not in excluir.get(rid, [])]
        for m in manuais.get(rid, []):
            if isinstance(m, dict):
                por_estudo[rid].insert(0, dict(tabela=m["tabela"], campo=m["campo"],
                                               valor=m["valor"], manual=True))
        candidatos, vistos = [], set()
        for c in por_estudo[rid]:
            if c["valor"] in vistos or re.search(r"risk ratio|95% ci|mean difference|weight", c["campo"], re.I):
                continue
            vistos.add(c["valor"])
            if c.get("manual"):
                nivel, max_ocorr, ancora = -1, 8, None
            else:
                if re.fullmatch(r"(19|20)\d\d", c["valor"]):
                    continue
                nivel = distintivo(c["valor"])
                if nivel == 0:
                    continue
                max_ocorr = 6 if nivel == 1 else (4 if nivel == 2 else 2)
                ancora = ancora_do_campo(c["tabela"], c["campo"])
            spans = ocorre(texto, c["valor"])
            if not (1 <= len(spans) <= max_ocorr):
                continue
            janelas = [texto[max(0, a - 120):b + 120] for a, b in spans]
            if ancora:
                exigencia = any if nivel == 1 else all
                if not exigencia(re.search(ancora, j, re.I) for j in janelas):
                    continue
            candidatos.append(dict(c, n_ocorr=len(spans), nivel=nivel))

        escolha, tabelas_usadas, celulas_usadas = [], set(), set()
        while len(escolha) < K:
            restantes = [c for c in candidatos
                         if not any(e["valor"] == c["valor"] for e in escolha)
                         and (c["tabela"], c["campo"]) not in celulas_usadas]
            if not restantes:
                break
            restantes.sort(key=lambda c: (c["tabela"] in tabelas_usadas,
                                          c["nivel"], c["n_ocorr"], -len(c["valor"])))
            c = restantes[0]
            escolha.append(c)
            tabelas_usadas.add(c["tabela"])
            celulas_usadas.add((c["tabela"], c["campo"]))

        pert_texto, registros = texto, []
        for c in escolha:
            novo = perturbar_valor(c["valor"], rng, texto)
            if novo is None:
                continue
            contextos = [re.sub(r"\s+", " ", texto[max(0, a - 38):b + 26])
                         for a, b in ocorre(texto, c["valor"])]
            pert_texto, n_sub = substitui(pert_texto, c["valor"], novo)
            registros.append(dict(tabela=c["tabela"], campo=c["campo"],
                                  original=c["valor"], perturbado=novo,
                                  ocorrencias_substituidas=n_sub, contextos=contextos))
        (dir_pert / f"{rid}.txt").write_text(pert_texto, encoding="utf-8")
        selo[rid] = registros
        campos = ", ".join(f"t{r['tabela']}·{r['campo'][:24]} ({r['original']}→{r['perturbado']}, ×{r['ocorrencias_substituidas']})" for r in registros)
        print(f"{rid}: {len(registros)} perturbações — {campos}")
        for r in registros:
            for ctx in r["contextos"]:
                print(f"      [{r['original']}] …{ctx}…")

    out = D1 / "perturbacoes-fechados.json"
    out.write_text(json.dumps(selo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nselada (fora do repo): {out.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()

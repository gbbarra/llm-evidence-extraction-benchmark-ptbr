# -*- coding: utf-8 -*-
"""A lente de passe único com fronteira numérica, da âncora 3. Instrumento 9 da §8.

Por que existe. A lente congelada (`e6-downstream.py`) é uma sequência ORDENADA de `str.replace` de
substring sobre a ficha serializada inteira — inclusive o campo de citação da ficha v2, que carrega
até 240 caracteres do artigo. Isso já reprovou quatro transcrições corretas no Estudo 9, quando o par
31→28 foi aplicado dentro de "1283.2". A âncora 3 torna a falha certa em vez de possível, porque seus
valores de selo são inteiros de dois dígitos, que ocorrem como substring de quase todo número longo de
um artigo clínico. Medido sobre o texto original dos oito primários, onde nenhuma troca deveria
ocorrer: a lente congelada comete 42 substituições indevidas, esta comete zero
(`provar-lente-ancora3.py`).

Duas propriedades, e as duas importam:

  fronteira    um valor só casa quando não é pedaço de outro número. `41` não casa dentro de `41.7`,
               de `141874` nem de `4117.3`.
  passe único  todas as trocas são decididas numa varredura só, e a saída nunca é revarrida. Sem isso
               a ordem do selo decide o resultado: com os pares do Dong (41→36 e 36.6→41.7), uma ordem
               devolve 41.7 e a outra devolve 36.7.

A lente das âncoras 1 e 2 não é tocada. A §12 do protocolo declara isso, para que a comparabilidade
delas com o registro publicado siga intacta.
"""
import json
import re

FRONTEIRA_ESQ = r"(?<![\w.,\-–])"
FRONTEIRA_DIR = r"(?![\w.])"


def compila(pares):
    """Um padrão único para todos os `de`, com o mais longo primeiro na alternância.

    O mais longo primeiro faz o casamento preferir `36.6` a `36` na mesma posição; a fronteira à
    direita já impediria o casamento curto, e as duas coisas juntas tornam o resultado independente
    da ordem em que o selo foi gravado.
    """
    mapa = {}
    for de, para in pares:
        de, para = str(de), str(para)
        if de and para and de != para:
            mapa[de] = para
            # a forma decimal do mesmo valor. O Dong imprime 41 das suas contagens como "9.0 (25.0)",
            # e uma ficha que preserva as casas -- como a regra 2 manda -- escreve o denominador
            # "41.0". A fronteira à direita, `(?![\w.])`, barra o casamento de "41" dentro de "41.0",
            # então sem esta linha a lente não desfaz o deslocamento: o leitor honesto sai com 41 e é
            # reprovado, enquanto quem recita "36.0" passa. A inversão exata do que a lente existe
            # para medir. Só vale para valor inteiro, e o destino ganha a mesma forma.
            if re.fullmatch(r"-?\d+", de) and re.fullmatch(r"-?\d+", para):
                mapa.setdefault(de + ".0", para + ".0")
    if not mapa:
        return None, {}
    alt = "|".join(re.escape(d) for d in sorted(mapa, key=len, reverse=True))
    return re.compile(FRONTEIRA_ESQ + "(" + alt + ")" + FRONTEIRA_DIR), mapa


def aplica(txt, pares):
    """Passe único sobre o texto. Devolve (texto, número de trocas)."""
    pad, mapa = compila(pares)
    if pad is None:
        return txt, 0
    n = 0

    def troca(m):
        nonlocal n
        n += 1
        return mapa[m.group(1)]

    return pad.sub(troca, txt), n


def colisoes(pares):
    """Pares que se atropelam. Um selo com colisão não pode ser gravado.

    Três formas de atropelo, todas verificadas com a MESMA fronteira que a lente usa:
      1. dois pares com o mesmo `de` e destinos diferentes;
      2. o `de` de um par casando dentro do `para` de outro — o que faria a saída de uma troca virar
         entrada de outra se o passe não fosse único, e que sinaliza selo mal escolhido de todo jeito;
      3. o `para` de um par igual ao `de` de outro, que é o mesmo defeito visto do outro lado.
    """
    achados = []
    vistos = {}
    for de, para in pares:
        de, para = str(de), str(para)
        if de in vistos and vistos[de] != para:
            achados.append(f"o valor {de} tem dois destinos: {vistos[de]} e {para}")
        vistos[de] = para
    for de1, para1 in pares:
        for de2, para2 in pares:
            if (de1, para1) == (de2, para2):
                continue
            if re.search(FRONTEIRA_ESQ + re.escape(str(de1)) + FRONTEIRA_DIR, str(para2)):
                achados.append(f"{de1} casa dentro do destino {para2} (do par {de2}→{para2})")
            if str(para1) == str(de2):
                achados.append(f"o destino de {de1} é {para1}, que é a origem do par {de2}→{para2}")
    return sorted(set(achados))


def desperturba(js, registros):
    """Desfaz o deslocamento na ficha do modelo. `registros`: [{original, perturbado}, ...]."""
    pares = [(r["perturbado"], r["original"]) for r in registros]
    txt, _ = aplica(json.dumps(js, ensure_ascii=False), pares)
    return json.loads(txt)


def perturba(txt, registros):
    """Aplica o deslocamento ao texto do artigo. Mesma máquina, direção oposta."""
    return aplica(txt, [(r["original"], r["perturbado"]) for r in registros])


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    # o caso do Dong, que é o que quebra a lente congelada
    sel = [dict(original="36", perturbado="41"), dict(original="25.0", perturbado="22.0"),
           dict(original="41.7", perturbado="36.6")]
    ficha = {"mb_n": "41", "mb_pct": "22.0", "ct_n": "41", "ct_pct": "36.6",
             "quote": "Mortality at 28 days-no. (%) 9.0 (22.0) 15.0 (36.6) 0.200",
             "ruido": "141874 4117.3 0.419 10.4161"}
    print("colisões no selo:", colisoes([(r["original"], r["perturbado"]) for r in sel]) or "nenhuma")
    d = desperturba(ficha, sel)
    esp = {"mb_n": "36", "mb_pct": "25.0", "ct_n": "36", "ct_pct": "41.7",
           "quote": "Mortality at 28 days-no. (%) 9.0 (25.0) 15.0 (41.7) 0.200",
           "ruido": "141874 4117.3 0.419 10.4161"}
    ok = d == esp
    for k in esp:
        print(f"  {'ok  ' if d[k] == esp[k] else 'ERRO'} {k:8s} {d[k]}")
    print("\nAUTOTESTE PASSA" if ok else "\nAUTOTESTE FALHA")
    sys.exit(0 if ok else 1)

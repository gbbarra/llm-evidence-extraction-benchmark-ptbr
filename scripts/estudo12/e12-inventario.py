# -*- coding: utf-8 -*-
"""O inventário da campanha. Instrumento 5 da §8.

Responde a uma pergunta só, e responde sem adivinhar: **onde parou.** Conta o que existe em disco
contra as 696 chamadas que o protocolo enumera, e diz o que falta, o que existe mas não passa no
portão de integridade, e o que já está pronto.

Duas propriedades que a §8 exige e que este script respeita:

  · roda a qualquer momento, inclusive com a campanha em curso, porque só lê. Não abre soquete, não
    chama modelo, não escreve nada em `saidas/` e não move arquivo nenhum. O que ele acha de errado
    ele reporta; quem afasta é o harness, na próxima passada.
  · o denominador é o plano do protocolo, e não o que existe. Um inventário que contasse arquivos
    diria "100% pronto" numa campanha que nunca começou.

Uso:  python e12-inventario.py [--por modelo|ancora|ficha] [--detalhe]
"""
import argparse
import collections
import importlib.util
import io
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("h12", AQUI / "e12-harness.py")
H = importlib.util.module_from_spec(spec)
spec.loader.exec_module(H)

ap = argparse.ArgumentParser(description="onde a campanha do Estudo 12 parou")
ap.add_argument("--por", choices=("modelo", "ancora", "ficha"), default="modelo")
ap.add_argument("--detalhe", action="store_true", help="lista as chamadas que faltam")
a = ap.parse_args()

PRONTO, RUIM, FALTA = "pronto", "íntegro? não", "falta"

linhas, motivos = [], collections.Counter()
tokens_in = tokens_out = segundos = 0
for c in H.plano():
    p = H.destino(c)
    if not p.exists():
        estado, motivo = FALTA, ""
    else:
        ok, motivo = H.integro(p)
        estado = PRONTO if ok else RUIM
        if ok:
            try:
                j = json.loads(io.open(p, encoding="utf-8").read())
                tokens_in += j.get("prompt_tokens", 0) or 0
                tokens_out += j.get("tokens", 0) or 0
                segundos += j.get("dt", 0) or 0
            except Exception:
                pass
        else:
            motivos[motivo.split(":")[0]] += 1
    linhas.append(dict(c, estado=estado, motivo=motivo, destino=p))

tot = len(linhas)
cont = collections.Counter(l["estado"] for l in linhas)
feitas = cont[PRONTO]

print(f"CAMPANHA DO ESTUDO 12 — {tot} chamadas previstas pelo protocolo\n")
print(f"  pronto e íntegro   {feitas:4d}   {100*feitas/tot:5.1f}%")
print(f"  existe mas recusa  {cont[RUIM]:4d}   {100*cont[RUIM]/tot:5.1f}%   (o harness refaz na próxima passada)")
print(f"  falta              {cont[FALTA]:4d}   {100*cont[FALTA]/tot:5.1f}%")

if motivos:
    print("\n  por que recusa:")
    for m, n in motivos.most_common():
        print(f"    {n:4d}  {m}")

chave = {"modelo": "modelo", "ancora": "ancora", "ficha": "ficha"}[a.por]
grupos = collections.OrderedDict()
for l in linhas:
    grupos.setdefault(l[chave], []).append(l)
print(f"\npor {a.por}:")
print(f"  {'':14s} {'pronto':>7s} {'recusa':>7s} {'falta':>7s} {'total':>7s}   progresso")
for k, g in grupos.items():
    c = collections.Counter(x["estado"] for x in g)
    barra = "█" * int(20 * c[PRONTO] / len(g)) + "·" * (20 - int(20 * c[PRONTO] / len(g)))
    print(f"  {str(k):14s} {c[PRONTO]:7d} {c[RUIM]:7d} {c[FALTA]:7d} {len(g):7d}   {barra}")

if feitas:
    med = segundos / feitas
    resta = tot - feitas
    print(f"\nmedido nas {feitas} chamadas prontas:")
    print(f"  entrada {tokens_in:,} tokens · saída {tokens_out:,} tokens".replace(",", "."))
    print(f"  {med/60:.2f} min por chamada · {segundos/3600:.1f} h gastas")
    print(f"  restam {resta} chamadas ≈ {resta*med/3600:.1f} h no ritmo medido")
    maiores = sorted((json.loads(io.open(l["destino"], encoding="utf-8").read()).get("prompt_tokens", 0)
                      for l in linhas if l["estado"] == PRONTO), reverse=True)[:1]
    if maiores:
        print(f"  maior prompt visto: {maiores[0]} tokens contra o teto de {H.CTX}"
              f"  (folga {H.CTX - maiores[0]})")
else:
    print("\nnenhuma chamada pronta ainda: a campanha não começou.")
    print(f"orçamento declarado no protocolo: 37 a 40 h")

if a.detalhe:
    faltando = [l for l in linhas if l["estado"] != PRONTO]
    print(f"\nas {len(faltando)} chamadas por fazer:")
    for l in faltando[:200]:
        print(f"  {l['estado']:12s} {l['modelo']:11s} {l['ancora']}/{l['ficha']} "
              f"{l['ensaio']}-r{l['replica']}  {l['motivo']}")
    if len(faltando) > 200:
        print(f"  ... e mais {len(faltando)-200}")

proximo = next((l for l in linhas if l["estado"] != PRONTO), None)
print("\n" + "=" * 74)
if proximo:
    print(f"RETOMA EM: {proximo['modelo']} · {proximo['ancora']}/{proximo['ficha']} · "
          f"{proximo['ensaio']} réplica {proximo['replica']}")
    print(f"comando:   python scripts/estudo12/e12-harness.py --modelo {proximo['modelo']}")
else:
    print("CAMPANHA COMPLETA: as 696 chamadas existem e passam no portão.")
print("=" * 74)

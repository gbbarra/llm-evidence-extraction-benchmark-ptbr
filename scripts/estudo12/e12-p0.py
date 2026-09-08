# -*- coding: utf-8 -*-
"""Roda todas as verificações da Fase 0 do Estudo 12, numa ordem só.

A §7 do protocolo diz que a P0 termina quando os nove instrumentos da §8 estão "construídos,
autoverificados, selados e commitados". Este script é o que decide se estão. Ele não chama modelo
nenhum, não toca na rede e não escreve em `saidas/`: reconstrói os artefatos a partir das fontes e
confere que cada um bate consigo mesmo e com o protocolo.

Rodar antes de começar a P1, e depois de qualquer mexida em instrumento.
"""
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]

ETAPAS = [
    ("chave da âncora 3, contra os primários", "e12-gabarito-a3.py", 7),
    ("motor da razão de chances", "e12-or.py", 1),
    ("leitura da Figura 3, por reconstrução", "verificar-figura3.py", 0),
    ("camada 2, contra as oito fontes", "verificar-camada2.py", 0),
    ("cenários de correção", "cenarios-ancora3.py", 0),
    ("alcance da perturbação", "medir-perturbabilidade.py", 0),
    ("viabilidade do deslocamento coerente", "provar-perturbacao-coerente.py", 0),
    ("lente com fronteira contra a congelada", "provar-lente-ancora3.py", 0),
    ("lente, autoteste", "e12-lente.py", 9),
    ("corpus perturbado e selo", "e12-perturbar-a3.py", 9),
    ("fichas v1 e v2", "e12-fichas-a3.py", 6),
    ("portão de retomada e escrita atômica", "e12-testa-retomada.py", 4),
    ("caminho de correção da razão de chances", "e12-avalia-a3.py", 8),
    ("as doutrinas do projeto, contra o código", "e12-testa-doutrinas.py", 0),
    ("as patologias reais de saída de modelo", "e12-testa-patologias.py", 0),
    ("o elenco resolve, os seis", "e12-testa-elenco.py", 1),
    ("a costura P1 -> P2 -> P3, ponta a ponta", "e12-testa-costura.py", 0),
]

print(f"FASE 0 DO ESTUDO 12 — {len(ETAPAS)} verificações\n")
falhou = []
t0 = time.time()
for rot, script, inst in ETAPAS:
    t = time.time()
    r = subprocess.run([sys.executable, str(AQUI / script)], capture_output=True,
                       text=True, encoding="utf-8", errors="replace", cwd=str(RAIZ))
    marca = "ok  " if r.returncode == 0 else "FALHA"
    if r.returncode != 0:
        falhou.append((rot, script, r))
    sig = f"§8.{inst}" if inst else "prova"
    print(f"  {marca} {sig:6s} {rot:44s} {time.time()-t:5.1f}s")

print()
if falhou:
    for rot, script, r in falhou:
        print("=" * 78)
        print(f"FALHOU: {rot}  ({script})")
        print((r.stdout or "")[-1500:])
        print((r.stderr or "")[-800:])
    print("=" * 78)
    print(f"P0 NÃO ESTÁ PRONTA: {len(falhou)} de {len(ETAPAS)} falharam. Não começar a P1.")
    sys.exit(1)

print("=" * 78)
print(f"P0 PRONTA — as {len(ETAPAS)} verificações passam em {time.time()-t0:.0f}s.")
print("Os nove instrumentos da §8 existem, se autoverificam e batem com o protocolo.")
print("\nPróximo passo, e ele chama modelo pela primeira vez:")
print("  python scripts/estudo12/e12-inventario.py          — onde estamos")
print("  python scripts/estudo12/e12-harness.py --seco      — o plano, sem chamar nada")
print("  python scripts/estudo12/e12-harness.py             — a campanha, 696 chamadas")
print("=" * 78)

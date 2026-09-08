# -*- coding: utf-8 -*-
"""Remove corpus/estudo12 do histórico local, que nunca foi empurrado.

POR QUE. Os oito arquivos de `corpus/estudo12/original/` são o texto plano dos primários da âncora 3,
e três deles — Kirov 2001, Memis 2002 e Levin 2004 — são artigos de acesso fechado, que o regime do
repositório manda nunca versionar. E publicar o original AO LADO do perturbado publica o mapa selado:
um diff entre os dois reconstrói o selo inteiro e a prova de leitura vira decoração.

Os arquivos já saíram do índice, mas continuam nos oito commits em que entraram. Enquanto estiverem
lá, um push os leva para o GitHub.

O QUE ESTE SCRIPT FAZ. Percorre só os commits locais (`origin/main..HEAD`) e remove aquele diretório
do índice de cada um. Nada do que já está no GitHub é tocado, e **nada é apagado do disco**: os 16
arquivos continuam onde estão e se regeneram por `e12-perturbar-a3.py` de qualquer jeito.

O QUE MUDA, E É O CUSTO REAL. O identificador de um commit é o hash do conteúdo mais o do pai, então
todos os commits locais ganham identificadores novos. A consequência que importa: o protocolo
pré-registrado abre com "Frozen against commit 674e427", e esse commit deixa de existir. O
re-ancoramento é feito depois, por nota datada — que é o mecanismo que o projeto já usa para corrigir
sem reescrever o registro.

SEGURANÇA. A tag `backup-antes-da-limpeza` aponta para o estado atual. Para desfazer tudo:

    git reset --hard backup-antes-da-limpeza

O script confere as pré-condições antes e as pós-condições depois, e para na primeira que falhar.
"""
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
ALVO = "corpus/estudo12"
BACKUP = "backup-antes-da-limpeza"


def git(*args, check=True):
    r = subprocess.run(["git"] + list(args), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=str(RAIZ))
    if check and r.returncode != 0:
        print(f"\nERRO em: git {' '.join(args)}")
        print((r.stdout or "") + (r.stderr or ""))
        sys.exit(1)
    return (r.stdout or "").strip()


def conta_no_historico():
    n = 0
    for c in git("rev-list", "origin/main..HEAD").split():
        n += len([x for x in git("ls-tree", "-r", "--name-only", c, "--", ALVO,
                                 check=False).split() if x])
    return n


print("=" * 74)
print("LIMPEZA DO HISTÓRICO LOCAL — remove", ALVO, "dos commits não empurrados")
print("=" * 74)

# ---------------------------------------------------------------- pré-condições
print("\npré-condições:")
ramo = git("rev-parse", "--abbrev-ref", "HEAD")
print(f"  ramo atual: {ramo}")

sujo = git("status", "--porcelain")
sujo = [l for l in sujo.splitlines() if not l.startswith("??")]
if sujo:
    print("  PARADO: há mudanças não commitadas. Commite ou guarde antes:")
    for l in sujo[:8]:
        print("   ", l)
    sys.exit(1)
print("  árvore de trabalho limpa (fora arquivos não rastreados)")

if git("tag", "-l", BACKUP) != BACKUP:
    print(f"  PARADO: a tag {BACKUP} não existe. Crie antes: git tag {BACKUP} HEAD")
    sys.exit(1)
print(f"  rede de segurança: {BACKUP} -> {git('rev-parse', '--short', BACKUP)}")

locais = git("rev-list", "--count", "origin/main..HEAD")
antes = conta_no_historico()
disco = len(list((RAIZ / ALVO).rglob("*.txt")))
print(f"  commits locais não empurrados: {locais}")
print(f"  referências a {ALVO} no histórico local: {antes}")
print(f"  arquivos em disco: {disco}")

if antes == 0:
    print("\nnada a fazer: o histórico local já está limpo.")
    sys.exit(0)

# ---------------------------------------------------------------- a reescrita
print("\nreescrevendo... (pode levar um minuto)")
env = dict(os.environ, FILTER_BRANCH_SQUELCH_WARNING="1")
r = subprocess.run(["git", "filter-branch", "-f", "--index-filter",
                    f"git rm -r --cached --ignore-unmatch -q {ALVO}",
                    "--prune-empty", "--", "origin/main..HEAD"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace",
                   cwd=str(RAIZ), env=env)
print((r.stdout or "").strip()[-600:])
if r.returncode != 0:
    print((r.stderr or "")[-800:])
    print(f"\nFALHOU. Nada foi perdido: git reset --hard {BACKUP}")
    sys.exit(1)

# ---------------------------------------------------------------- pós-condições
print("\npós-condições:")
depois = conta_no_historico()
disco2 = len(list((RAIZ / ALVO).rglob("*.txt")))
locais2 = git("rev-list", "--count", "origin/main..HEAD")
ok = True


def diz(rot, passou, det=""):
    global ok
    ok = ok and passou
    print(f"  {'ok  ' if passou else 'FALHA'} {rot:52s} {det}")


diz("o histórico local não tem mais o corpus", depois == 0, f"{depois} referências")
diz("os arquivos continuam em disco", disco2 == disco, f"{disco2} de {disco}")
diz("nenhum commit local se perdeu", locais2 == locais, f"{locais2} de {locais}")
diz("o backup ainda aponta para o estado anterior",
    git("rev-parse", "--short", BACKUP) != git("rev-parse", "--short", "HEAD"))

print("\n" + "=" * 74)
if ok:
    print("HISTÓRICO LIMPO.")
    print(f"  HEAD antes:  {git('rev-parse', '--short', BACKUP)}")
    print(f"  HEAD agora:  {git('rev-parse', '--short', 'HEAD')}")
    print("\nFalta re-ancorar o protocolo no SHA novo, com nota datada. Avise o assistente.")
    print(f"Para desfazer enquanto a tag existir:  git reset --hard {BACKUP}")
else:
    print(f"ALGO NÃO FECHOU. Desfaça com:  git reset --hard {BACKUP}")
print("=" * 74)
sys.exit(0 if ok else 1)

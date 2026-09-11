# -*- coding: utf-8 -*-
"""A trava de instancia unica do harness, conferida sob corrida de verdade.

O defeito de origem, 10/09/2026: o harness aceitou ser lancado duas vezes na
mesma maquina. Os dois processos disputaram a GPU por cinco horas -- a chamada
passou de 3,3 para 7,0 min -- e refizeram parte do trabalho. Nada corrompeu:
escrita atomica e portao de integridade seguraram, e o inventario fechou com
zero recusadas. Mas um portao que existe tem de falhar em voz alta.

A primeira versao da trava (PID anotado + tasklist) caiu na revisao adversarial
de 11/09/2026: checa-e-escreve deixava dois lancamentos simultaneos passarem,
qualquer python.exe alheio com o PID reciclado prendia a campanha, e a janela do
PowerShell fechada nao rodava o finally. Esta versao e um cadeado do sistema
operacional, e por isso os testes aqui sao com PROCESSOS DE VERDADE, nao com
funcao trocada: um filho que segura, seis filhos que largam juntos, e o proprio
__main__ em corrida seca.

Roda: python scripts/estudo12/e12-testa-trava.py
"""
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
HARNESS = RAIZ / "scripts" / "estudo12" / "e12-harness.py"
NL = chr(10)

# o filho: carrega o harness com o MESMO ambiente e faz um papel
CRIANCA = r'''
import importlib.util, pathlib, sys, time
spec = importlib.util.spec_from_file_location("h_filho", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
papel = sys.argv[2]
if papel == "segura":
    m.toma_trava(); print("PRONTO", flush=True); time.sleep(120)
elif papel == "corre":
    largada = pathlib.Path(sys.argv[3]); print("PRONTO", flush=True)
    while not largada.exists(): time.sleep(0.003)
    try:
        m.toma_trava(); print("GANHOU", flush=True); time.sleep(2.5); m.solta_trava()
    except SystemExit:
        print("PERDEU", flush=True)
'''


def carrega(saidas, trava):
    os.environ["E12_SAIDAS"] = str(saidas)
    os.environ["E12_RECUSADOS"] = str(saidas.parent / "recusados")
    os.environ["E12_TRAVA"] = str(trava)
    spec = importlib.util.spec_from_file_location("h12_trava", HARNESS)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def filho(papel, *extra):
    return subprocess.Popen([sys.executable, "-u", "-c", CRIANCA, str(HARNESS), papel, *extra],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                            encoding="utf-8", errors="replace", env=dict(os.environ))


def espera_pronto(p, segundos=40):
    fim = time.time() + segundos
    while time.time() < fim:
        linha = p.stdout.readline()
        if linha.strip() == "PRONTO":
            return True
        if not linha and p.poll() is not None:
            break
    return False


def testa(nome, fn, falhas, limpa=None):
    """Um caso. SystemExit conta como falha (e o que toma_trava lanca ao recusar), e o
    `limpa` roda sempre: um caso que falha segurando a trava nao pode contaminar o proximo."""
    try:
        fn()
        print(f"  ok   {nome}")
    except AssertionError as e:
        falhas.append(f"{nome}: {e}")
        print(f"  X    {nome}: {e}")
    except (Exception, SystemExit) as e:
        falhas.append(f"{nome}: {type(e).__name__}: {e}")
        print(f"  X    {nome}: {type(e).__name__}: {str(e)[:200]}")
    finally:
        if limpa:
            limpa()


def main():
    falhas = []
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        saidas, trava = d / "saidas", d / "harness.trava"
        saidas.mkdir()
        h = carrega(saidas, trava)
        assert h.TRAVA == trava, f"E12_TRAVA nao foi respeitado: {h.TRAVA}"

        def toma_e_solta_sem_apagar():
            assert not trava.exists(), "o diretorio de teste ja nasceu com trava"
            aviso = h.toma_trava()
            assert aviso == "", f"nao devia avisar nada, avisou {aviso!r}"
            dono = json.loads(trava.read_text(encoding="utf-8"))
            assert dono["pid"] == os.getpid(), f"gravou pid errado: {dono['pid']}"
            h.solta_trava()
            assert trava.exists(), "apagou a trava ao soltar -- reprovado e registrado, nao apagado"
            fim = json.loads(trava.read_text(encoding="utf-8"))
            assert fim.get("encerrado"), "soltou sem anotar o encerramento"

        def dono_vivo_recusa_e_explica():
            p = filho("segura")
            try:
                assert espera_pronto(p), f"o filho nao segurou a trava: {p.stderr.read()[:300]}"
                try:
                    h.toma_trava()
                    assert False, "tomou a trava com outro processo segurando"
                except SystemExit as e:
                    t = str(e)
                    assert str(p.pid) in t, f"a recusa nao diz o PID do dono: {t!r}"
                    assert "inventario" in t, "a recusa nao diz como ver onde a campanha esta"
                    assert "tasklist" in t, "a recusa nao diz como conferir o processo"
            finally:
                p.kill()
                p.wait(timeout=30)
            # morto sem soltar: o SO libera o cadeado, e o proximo assume avisando
            aviso = h.toma_trava()
            assert "sem encerrar" in aviso, f"assumiu sem dizer que o anterior morreu: {aviso!r}"
            h.solta_trava()

        def ilegivel_assume_avisando():
            trava.write_text("isto nao e json", encoding="utf-8")
            aviso = h.toma_trava()
            assert "ilegivel" in aviso, f"assumiu uma trava ilegivel em silencio: {aviso!r}"
            h.solta_trava()

        def encerrada_assume_em_silencio():
            aviso = h.toma_trava()
            assert aviso == "", f"trava encerrada direito nao merece aviso: {aviso!r}"
            h.solta_trava()

        def seis_largam_juntos_um_ganha():
            largada = d / "largada"
            filhos = [filho("corre", str(largada)) for _ in range(6)]
            try:
                for p in filhos:
                    assert espera_pronto(p), f"um filho nao ficou pronto: {p.stderr.read()[:300]}"
                largada.write_text("vai")
                saidas_f = []
                for p in filhos:
                    out, err = p.communicate(timeout=60)
                    saidas_f.append(out)
                ganhou = sum(o.count("GANHOU") for o in saidas_f)
                perdeu = sum(o.count("PERDEU") for o in saidas_f)
                assert ganhou == 1, f"{ganhou} ganharam a mesma trava ao mesmo tempo"
                assert perdeu == 5, f"{perdeu} perderam; esperava 5"
            finally:
                for p in filhos:
                    if p.poll() is None:
                        p.kill()

        def seco_relata_e_nao_move():
            # planta uma saida que o portao recusa, e roda o __main__ em corrida seca
            c = next(x for x in h.plano()
                     if x["modelo"] == "gemma12" and x["ancora"] == "a3" and x["ficha"] == "v1")
            p = h.destino(c)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('{"done_reason": "length"}', encoding="utf-8")
            trava.unlink(missing_ok=True)
            r = subprocess.run([sys.executable, str(HARNESS), "--seco", "--modelo", "gemma12",
                                "--ancora", "a3", "--ficha", "v1"],
                               capture_output=True, text=True, encoding="utf-8", errors="replace",
                               cwd=str(RAIZ), env=dict(os.environ), timeout=300)
            assert r.returncode == 0, f"--seco saiu com {r.returncode}: {r.stderr[-300:]}"
            assert "SERIA RECUSADO" in r.stdout, "a corrida seca nao relatou o que faria"
            assert "RECUSADO —" not in r.stdout.replace("SERIA RECUSADO", ""), \
                "a corrida seca anunciou recusa de verdade"
            assert p.exists(), "a corrida seca MOVEU uma saida da campanha"
            assert not (d / "recusados").exists(), "a corrida seca criou recusados/"
            assert not trava.exists(), "a corrida seca tomou a trava, e nao devia"

        for nome, fn in (
                ("toma e solta, sem apagar", toma_e_solta_sem_apagar),
                ("dono vivo: recusa, explica; morto: assume e avisa", dono_vivo_recusa_e_explica),
                ("trava ilegivel: assume avisando", ilegivel_assume_avisando),
                ("trava encerrada: assume em silencio", encerrada_assume_em_silencio),
                ("seis largam juntos: exatamente um ganha", seis_largam_juntos_um_ganha),
                ("--seco relata e nao move nem trava", seco_relata_e_nao_move),
        ):
            testa(nome, fn, falhas, limpa=h.solta_trava)

    print(NL + ("sem defeitos" if not falhas else f"{len(falhas)} defeitos"))
    return not falhas


if __name__ == "__main__":
    sys.exit(0 if main() else 1)

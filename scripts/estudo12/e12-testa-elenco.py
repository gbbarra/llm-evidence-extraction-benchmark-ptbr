# -*- coding: utf-8 -*-
"""O elenco dos seis resolve, e a chamada monta para cada um. Nenhum modelo e chamado.

Este teste existe porque o defeito mais grave da Fase 0 nao foi apanhado por nenhuma das treze
verificacoes anteriores: quatro dos seis modelos do elenco congelado nao existiam no registro que o
harness consulta. O caminho seco pula o bloco que resolve a etiqueta, e o teste de retomada so olha o
plano, entao os tres davam verde. A campanha teria rodado gemma12 e qwen14 -- cerca de doze horas --
e depois gravado 464 arquivos de erro em segundos, terminando com codigo zero.

A causa: cada importlib cria um objeto de modulo novo, e `e4-extensao.py` injeta os tres modelos do
Estudo 4 no h3 QUE ELE MESMO CARREGOU. E `e8-amend1-cast.py` nem injeta: so define `registrar(h3)`.
"""
import importlib.util
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("h12", AQUI / "e12-harness.py")
H = importlib.util.module_from_spec(spec)
spec.loader.exec_module(H)

ok = True


def diz(rot, passou, det=""):
    global ok
    ok = ok and passou
    print(f"  {'ok  ' if passou else 'FALHA'} {rot:52s} {det}")


print("1. os seis do elenco congelado da §3 existem no registro")
for m in H.ELENCO:
    diz(m, m in H.h3.MODELS, H.h3.MODELS[m]["ollama"] if m in H.h3.MODELS else "AUSENTE")

print("\n2. a chamada monta para cada um, com a etiqueta certa")
TAGS = {"gemma12": "gemma4:12b", "qwen14": "qwen3:14b", "llama8": "llama3.1:8b",
        "qwen35": "qwen3.5:9b", "deepseek14": "deepseek-r1:14b",
        "qwen27q2": "smtek/Qwen3.8-27B:Q2_K_XL"}
capturado = {}


def espia(url, body, timeout=7200):
    capturado["body"] = body
    raise RuntimeError("interceptado")


guardado = H.h3.post_json
H.h3.post_json = espia
try:
    for m in H.ELENCO:
        capturado.clear()
        try:
            H.chama(dict(modelo=m, ancora="a3", ficha="v1", ensaio="x", replica=1), "p")
        except RuntimeError:
            pass
        except Exception as e:
            diz(m, False, f"{type(e).__name__}: {e}")
            continue
        b = capturado.get("body", {})
        diz(m, b.get("model") == TAGS[m] and b.get("options", {}).get("num_ctx") == 24576,
            f"model={b.get('model')} num_ctx={b.get('options', {}).get('num_ctx')}")
finally:
    H.h3.post_json = guardado

print("\n3. nenhum modelo do elenco pede CPU (todos cabem na GPU integrada)")
for m in H.ELENCO:
    diz(m, H.h3.MODELS[m]["cpu"] is False, f"cpu={H.h3.MODELS[m]['cpu']}")

print("\n4. o plano roda um modelo residente por vez, na ordem do elenco")
seq = [c["modelo"] for c in H.plano()]
blocos = [seq[0]] + [b for a, b in zip(seq, seq[1:]) if a != b]
diz("cada modelo aparece num bloco só", len(blocos) == len(set(blocos)), " -> ".join(blocos))
diz("e na ordem congelada da §3", blocos == H.ELENCO, " -> ".join(blocos))

print("\n" + "=" * 74)
print("ELENCO VERIFICADO" if ok else "ELENCO INCOMPLETO — a campanha morreria no meio")
print("=" * 74)
sys.exit(0 if ok else 1)

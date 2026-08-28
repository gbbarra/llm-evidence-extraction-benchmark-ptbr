# -*- coding: utf-8 -*-
"""EXTRAI E1 — Emenda 2: T3b, síntese sobre as extrações dos 14 primários.

Mesmo prompt da T3 (t3-sintese.txt), agora com as 14 extrações T1-r1 do próprio
modelo (8 abertas + 6 fechadas). Saída: saidas/<modelo>/t3b-r1.json.
"""
import importlib.util
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("h", RAIZ / "scripts" / "estudo1" / "e1-harness.py")
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
h.CTX = 24576  # registro: prompt T3b ~16.3k tokens estoura o 16384; clausula do protocolo (§8) aplicada aos 4 modelos

ROT = {"PMC10561433": "Yoon 2023", "PMC10694978": "Sun 2023", "PMC10912221": "Wu 2024",
       "PMC11061212": "Castro 2024", "PMC12565272": "Redondo Calvo 2025", "PMC4782303": "Schmid 2016",
       "PMC5589093": "Weinberg 2017", "PMC6907038": "Sujatha 2019", "REF26": "Diaper 2021",
       "REF29": "de Waal 2021", "REF30": "Arslan-Carlon 2020", "REF33": "Calvo-Vecino 2018",
       "REF41": "Coeckelenbergh 2024", "REF47": "Hokenek 2022"}


def main():
    tpl = (h.DIR_PROMPTS / "t3-sintese.txt").read_text(encoding="utf-8")
    tpl = tpl.replace("dados de 8 ensaios", "dados de 14 ensaios")
    for mod in ("gemma12", "qwen14", "gemma26", "qwen38"):
        outdir = h.DIR_OUT / mod
        out = outdir / "t3b-r1.json"
        if out.exists():
            print(f"pulando (já feito): {mod} t3b")
            continue
        blocos = []
        for pm in ROT:
            f = outdir / f"{pm}-t1-r1.json"
            content = json.loads(f.read_text(encoding="utf-8"))["content"]
            blocos.append(f"=== ENSAIO {pm} ({ROT[pm]}) ===\n{content.strip()}")
        prompt = tpl.replace("{EXTRACOES}", "\n\n".join(blocos))
        t0 = time.strftime("%Y-%m-%d %H:%M:%S")
        r = h.run_ollama(mod, prompt, h.MAX_TOKENS["t3"])
        out.write_text(json.dumps(dict(modelo=mod, ollama=h.MODELS[mod]["ollama"], pmcid=None,
                                       tarefa="t3b", replica=1, inicio=t0, **r),
                                  ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{mod} t3b: {r['dt']:.0f}s, {r['prompt_tokens']}+{r['tokens']} tok, fim={r['finish']}", flush=True)
    print("T3B CONCLUÍDA.")


if __name__ == "__main__":
    main()

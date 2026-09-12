# -*- coding: utf-8 -*-
"""Builds the anchor-1 and anchor-3 v3 sheets from the frozen v2 sheets by adding the two v3 rules (a table row
counts as a quotation; never compute) — deterministically, so the derivation from v2 is on record. The anchor-2
v3 sheet is written by hand (dados/estudo13/prompts/a2-extraction-v3.txt) because its fields change.

Run: python scripts/estudo13/e13-fichas.py    (then e13-sela-fichas.py)
"""
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
DEST = RAIZ / "dados" / "estudo13" / "prompts"

REGRA_LINHA = ("A TABLE ROW COUNTS AS A QUOTATION: copy the row as printed and prefix it with the table's "
               "title, separated by \" | \" (for example, \"Table 2. Postoperative outcomes | Mortality 2 (1.0) "
               "1 (0.5)\").")
REGRA_NAO_CALCULA = ("Never compute or derive a value from other numbers — no percentage turned into a count, "
                     "no sum across arms, no difference between visits. If the datum is not printed as such, "
                     "write \"NR\" in the value field and, when a related printed figure exists (for example a "
                     "percentage where the count is asked), mention it in \"where\".")

# anchor 1: v2 + the two rules, numbered after rule 7
v2 = io.open(RAIZ / "dados" / "estudo9" / "prompts" / "t1-extraction-v2.txt", encoding="utf-8").read()
marc = "\n\nForm (use exactly these keys):"
assert marc in v2 and "7. \"quote\" is the VERBATIM" in v2, "a1 v2 sheet changed shape"
cabeca, resto = v2.split(marc, 1)
cabeca = cabeca.rstrip() + f"\n8. {REGRA_LINHA}\n9. {REGRA_NAO_CALCULA}"
io.open(DEST / "a1-extraction-v3.txt", "w", encoding="utf-8", newline="\n").write(cabeca + marc + resto)
print("a1-extraction-v3.txt written from t1-extraction-v2.txt + rules 8-9")

# anchor 3: v2 + the two rules, numbered after rule 7 (the sheet keeps its "Form" block)
v2 = io.open(RAIZ / "dados" / "estudo12" / "prompts" / "a3-extraction-v2.txt", encoding="utf-8").read()
marc = "\n\nForm (use exactly these keys;"
assert marc in v2 and "7. Every data field is an object" in v2, "a3 v2 sheet changed shape"
cabeca, resto = v2.split(marc, 1)
cabeca = cabeca.rstrip() + f"\n8. {REGRA_LINHA}\n9. {REGRA_NAO_CALCULA} In particular, if the article prints a mortality percentage but not the number of deaths, write the percentage in \"deaths_percent\" and \"NR\" in \"deaths\"."
io.open(DEST / "a3-extraction-v3.txt", "w", encoding="utf-8", newline="\n").write(cabeca + marc + resto)
print("a3-extraction-v3.txt written from a3-extraction-v2.txt + rules 8-9")

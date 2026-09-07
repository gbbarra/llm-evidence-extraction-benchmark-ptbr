# -*- coding: utf-8 -*-
"""Study 8 — Amendment 1 (2026-09-07): the sixth-reader extension arm.

Injects the extension model into the harness registry at run time (the frozen
five-model cast is never edited) and extends a grader's cast only when the
model's outputs exist for that phase, so the five-model record grades identically.
"""
from pathlib import Path

EXT = {"qwen27q2": dict(ollama="smtek/Qwen3.8-27B:Q2_K_XL", cpu=False)}
SIG = {"qwen27q2": "Q27"}


def registrar(h3):
    for chave, cfg in EXT.items():
        h3.MODELS.setdefault(chave, dict(cfg))
    return h3


def cast_estendido(base, pasta_fase):
    """base = the frozen five; pasta_fase = dados/estudo8/saidas/<phase>."""
    pasta = Path(pasta_fase)
    extra = [k for k in EXT if (pasta / k).exists() and any((pasta / k).glob("*.json"))]
    return list(base) + [k for k in extra if k not in base]

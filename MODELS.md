# Pinned model builds (Ollama)

The exact quantized builds behind every EXTRAI run, recorded 2026-08-30 on the benchmark machine (Ollama 0.32.15, `ollama list` / `ollama show`). The ID column is Ollama's manifest-digest prefix as printed by `ollama list`; re-pulling a tag later may fetch a different build, so exact reproduction should verify these IDs.

| Paper name | Ollama tag (in the harnesses) | ID (digest prefix) | Params | Quant | Architecture |
|---|---|---|---|---|---|
| gemma4:12b | `gemma4:12b` | `4eb23ef187e2` | 11.9B | Q4_K_M | gemma4 |
| qwen3:14b | `qwen3:14b` | `bdbd181c33f2` | 14.8B | Q4_K_M | qwen3 |
| gemma4:26b | `gemma4:26b` | `5571076f3d70` | 25.8B | Q4_K_M | gemma4 (MoE) |
| qwen3.8:27b | `qwen3.8:27b-texto` | `7754b7d139c8` | 27.3B | Q4_K_M | qwen35 |

**Note on the 27B tag.** All three studies call the 27B through the local tag `qwen3.8:27b-texto`: the same base-weights blob as the stock `qwen3.8:27b` (`sha256-f5f1dd8920d417aac2718b0bda3403da274301efdd6760b4f0f4b864ff2ad57d`, verified identical `FROM` on both tags) rebuilt with a raw-prompt template (`TEMPLATE {{ .Prompt }}`), so the frozen Portuguese instruments pass through verbatim with no chat wrapper. Each study's `MODELS` dict in `scripts/estudo*/e*-harness.py` records the tag it ran.

# -*- coding: utf-8 -*-
"""Inspect a GGUF model file header: general metadata, the file_type field, and the actual
distribution of tensor quantization types, with bits per weight computed from the file size.

Written for Study 8 Amendment 1 to settle what quantization the sixth reader really is: the
Ollama tag says Q2_K_XL, `ollama show` prints the GGUF file_type field (Q4_K_S), and only the
tensors themselves can arbitrate.

Run: python scripts/estudo8/gguf-inspect.py <path-to-gguf-blob>
"""
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GGML_TYPES = {0: "F32", 1: "F16", 2: "Q4_0", 3: "Q4_1", 6: "Q5_0", 7: "Q5_1", 8: "Q8_0", 9: "Q8_1",
              10: "Q2_K", 11: "Q3_K", 12: "Q4_K", 13: "Q5_K", 14: "Q6_K", 15: "Q8_K", 16: "IQ2_XXS",
              17: "IQ2_XS", 18: "IQ3_XXS", 19: "IQ1_S", 20: "IQ4_NL", 21: "IQ3_S", 22: "IQ2_S",
              23: "IQ4_XS", 24: "I8", 25: "I16", 26: "I32", 27: "I64", 28: "F64", 29: "IQ1_M",
              30: "BF16", 34: "TQ1_0", 35: "TQ2_0", 36: "MXFP4"}
# bits per weight of each block type (llama.cpp block sizes)
BPW = {"F32": 32, "F16": 16, "BF16": 16, "Q8_0": 8.5, "Q8_1": 9, "Q6_K": 6.5625, "Q5_K": 5.5, "Q5_0": 5.5,
       "Q5_1": 6, "Q4_K": 4.5, "Q4_0": 4.5, "Q4_1": 5, "Q3_K": 3.4375, "Q2_K": 2.625, "IQ4_XS": 4.25,
       "IQ4_NL": 4.5, "IQ3_S": 3.44, "IQ3_XXS": 3.06, "IQ2_S": 2.5, "IQ2_XS": 2.31, "IQ2_XXS": 2.06,
       "IQ1_M": 1.75, "IQ1_S": 1.56}
FILE_TYPES = {0: "ALL_F32", 1: "MOSTLY_F16", 2: "MOSTLY_Q4_0", 3: "MOSTLY_Q4_1", 7: "MOSTLY_Q8_0",
              8: "MOSTLY_Q5_0", 9: "MOSTLY_Q5_1", 10: "MOSTLY_Q2_K", 11: "MOSTLY_Q3_K_S", 12: "MOSTLY_Q3_K_M",
              13: "MOSTLY_Q3_K_L", 14: "MOSTLY_Q4_K_S", 15: "MOSTLY_Q4_K_M", 16: "MOSTLY_Q5_K_S",
              17: "MOSTLY_Q5_K_M", 18: "MOSTLY_Q6_K", 19: "MOSTLY_IQ2_XXS", 20: "MOSTLY_IQ2_XS",
              21: "MOSTLY_Q2_K_S", 22: "MOSTLY_IQ3_XS", 23: "MOSTLY_IQ3_XXS", 24: "MOSTLY_IQ1_S",
              25: "MOSTLY_IQ4_NL", 26: "MOSTLY_IQ3_S", 27: "MOSTLY_IQ3_M", 28: "MOSTLY_IQ2_S",
              29: "MOSTLY_IQ2_M", 30: "MOSTLY_IQ4_XS", 31: "MOSTLY_IQ1_M", 32: "MOSTLY_BF16"}


class R:
    def __init__(self, f):
        self.f = f

    def u8(self): return struct.unpack("<B", self.f.read(1))[0]
    def i8(self): return struct.unpack("<b", self.f.read(1))[0]
    def u16(self): return struct.unpack("<H", self.f.read(2))[0]
    def i16(self): return struct.unpack("<h", self.f.read(2))[0]
    def u32(self): return struct.unpack("<I", self.f.read(4))[0]
    def i32(self): return struct.unpack("<i", self.f.read(4))[0]
    def f32(self): return struct.unpack("<f", self.f.read(4))[0]
    def u64(self): return struct.unpack("<Q", self.f.read(8))[0]
    def i64(self): return struct.unpack("<q", self.f.read(8))[0]
    def f64(self): return struct.unpack("<d", self.f.read(8))[0]
    def bool_(self): return bool(self.u8())

    def string(self):
        n = self.u64()
        return self.f.read(n).decode("utf-8", errors="replace")

    def value(self, t):
        if t == 0: return self.u8()
        if t == 1: return self.i8()
        if t == 2: return self.u16()
        if t == 3: return self.i16()
        if t == 4: return self.u32()
        if t == 5: return self.i32()
        if t == 6: return self.f32()
        if t == 7: return self.bool_()
        if t == 8: return self.string()
        if t == 9:
            et = self.u32(); n = self.u64()
            vals = [self.value(et) for _ in range(n)]
            return vals if n <= 16 else f"<array of {n} {et}>"
        if t == 10: return self.u64()
        if t == 11: return self.i64()
        if t == 12: return self.f64()
        raise ValueError(f"unknown gguf value type {t}")


def main(path):
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        r = R(f)
        magic = f.read(4)
        assert magic == b"GGUF", magic
        version = r.u32(); n_tensors = r.u64(); n_kv = r.u64()
        meta = {}
        for _ in range(n_kv):
            k = r.string(); t = r.u32(); v = r.value(t)
            if isinstance(v, str) and len(v) > 200:
                v = v[:200] + "…"
            meta[k] = v
        tipos = {}; params = 0; bits = 0.0
        for _ in range(n_tensors):
            name = r.string(); nd = r.u32()
            dims = [r.u64() for _ in range(nd)]
            t = r.u32(); _off = r.u64()
            n = 1
            for d in dims: n *= d
            tn = GGML_TYPES.get(t, f"type{t}")
            e = tipos.setdefault(tn, dict(tensors=0, params=0))
            e["tensors"] += 1; e["params"] += n
            params += n; bits += n * BPW.get(tn, 0)
    ft = meta.get("general.file_type")
    print(f"file: {path}\n  size {size/1e9:.2f} GB · GGUF v{version} · tensors {n_tensors} · kv {n_kv}")
    for k in ("general.architecture", "general.name", "general.basename", "general.size_label", "general.type",
              "general.quantization_version", "general.file_type", "general.finetune", "general.license",
              "general.repo_url", "general.source.repo_url", "general.base_model.0.name"):
        if k in meta:
            print(f"  {k} = {meta[k]!r}" + (f"  → {FILE_TYPES.get(ft, '?')}" if k == "general.file_type" else ""))
    print(f"  parameters (sum of tensor elements): {params/1e9:.2f} B")
    print(f"  bits per weight from file size: {size*8/params:.2f}  ·  from tensor types: {bits/params:.2f}")
    print("  tensor types (share of parameters):")
    for tn, e in sorted(tipos.items(), key=lambda x: -x[1]["params"]):
        print(f"    {tn:8s} {e['tensors']:5d} tensors  {100*e['params']/params:5.1f}%")
    out = dict(file=os.path.basename(path), size_bytes=size, gguf_version=version, n_tensors=n_tensors,
               file_type=ft, file_type_name=FILE_TYPES.get(ft), parameters=params,
               bpw_from_size=round(size * 8 / params, 3), bpw_from_types=round(bits / params, 3),
               tensor_types={k: dict(tensors=v["tensors"], share=round(v["params"] / params, 4)) for k, v in tipos.items()},
               meta={k: v for k, v in meta.items() if k.startswith("general.")})
    return out


if __name__ == "__main__":
    res = main(sys.argv[1])
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=1)
        print("saved:", sys.argv[2])

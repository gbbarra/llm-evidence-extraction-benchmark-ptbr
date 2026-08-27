# -*- coding: utf-8 -*-
"""EXTRAI — Estudo 1: baixa o corpus congelado.

Metanálise-âncora: PMC13235771 (GDFT vs fluidoterapia convencional, Cureus, CC-BY).
Identifica os 14 RCTs primários citados na tabela de características, resolve cada um
no Europe PMC, registra o status de acesso aberto e baixa o fullTextXML dos abertos.

Saídas (todas em corpus/):
  ma/ma-gdft.xml            — XML integral da metanálise
  ma/ma-gdft-meta.json      — metadados (título, autores, data, licença, DOI)
  primarios/primarios.json  — os 14 primários com PMCID/DOI/licença/status OA
  primarios/<PMCID>.xml     — XML integral de cada primário aberto
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
MA_ID = "PMC13235771"
RAIZ = Path(__file__).resolve().parents[2]
DIR_MA = RAIZ / "corpus" / "ma"
DIR_PRIM = RAIZ / "corpus" / "primarios"


def baixar(url, timeout=90):
    return urllib.request.urlopen(url, timeout=timeout).read().decode("utf-8", "replace")


def busca(query, tipo="core"):
    url = f"{EPMC}/search?query={urllib.parse.quote(query)}&format=json&resultType={tipo}&pageSize=3"
    return json.loads(baixar(url, 45)).get("resultList", {}).get("result", [])


def ref_info(ref):
    """Extrai (título, doi) de uma <ref>; Cureus usa <mixed-citation> plana."""
    texto = " ".join(ref.itertext())
    tit = ref.find(".//article-title")
    pid = ref.find(".//pub-id[@pub-id-type='doi']")
    doi = "".join(pid.itertext()).strip() if pid is not None else None
    if not doi:
        m = re.search(r"10\.\d{4,9}/[^\s,;]+", texto)
        doi = m.group(0).rstrip(".") if m else None
    if tit is not None:
        titulo = " ".join(tit.itertext()).strip()
    else:
        partes = [p.strip() for p in re.split(r"(?<=[a-z\)])\.\s", texto)
                  if len(p.strip()) > 30 and not re.match(r"^\d", p.strip())]
        titulo = max(partes, key=len, default="")
    return titulo, doi


def main():
    DIR_MA.mkdir(parents=True, exist_ok=True)
    DIR_PRIM.mkdir(parents=True, exist_ok=True)

    # 1. metanálise: metadados + XML integral
    res = busca(f'PMCID:"{MA_ID}"') or busca(f"PMCID:{MA_ID}")
    meta = {}
    if res:
        r = res[0]
        meta = dict(pmcid=MA_ID, titulo=r.get("title"), autores=r.get("authorString"),
                    revista=(r.get("journalInfo", {}) or {}).get("journal", {}).get("title"),
                    data=r.get("firstPublicationDate"), doi=r.get("doi"),
                    licenca=r.get("license"), acesso_aberto=r.get("isOpenAccess"))
    xml_bruto = baixar(f"{EPMC}/{MA_ID}/fullTextXML")
    (DIR_MA / "ma-gdft.xml").write_text(xml_bruto, encoding="utf-8")
    (DIR_MA / "ma-gdft-meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"MA salva: {meta.get('titulo', '?')[:70]}… [{meta.get('licenca')}] {meta.get('data')}")

    # 2. identifica os primários pela tabela de características
    xml = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>", "", xml_bruto, count=1)
    root = ET.fromstring(xml)
    refs = {}
    for ref in root.findall(".//ref-list//ref"):
        lab = ref.find("label")
        m = re.search(r"\d+", lab.text or "") if lab is not None else None
        if m:
            refs[m.group(0)] = ref

    nums = []
    for t in root.findall(".//table-wrap"):
        capel = t.find(".//caption")
        cap = " ".join(capel.itertext()).lower() if capel is not None else ""
        if "haracteristics" in cap:
            texto_tab = " ".join(t.itertext())
            nums = sorted(set(re.findall(r"\[\s*(\d{1,3})\s*\]", texto_tab)), key=int)
            print(f"tabela de características: refs {nums}")
            break
    if not nums:
        sys.exit("ERRO: tabela de características não encontrada")

    # 3. resolve cada primário no EPMC e baixa os abertos
    primarios = []
    for n in nums:
        ref = refs.get(n)
        if ref is None:
            primarios.append(dict(ref=n, erro="ref não encontrada"))
            continue
        titulo, doi = ref_info(ref)
        res = busca(f'DOI:"{doi}"') if doi else []
        if not res and titulo:
            res = busca(f'TITLE:"{titulo[:120]}"')
        info = dict(ref=n, titulo_citado=titulo[:160], doi=doi)
        if res:
            r = res[0]
            info.update(pmcid=r.get("pmcid"), pmid=r.get("pmid"),
                        titulo=r.get("title"), autores=r.get("authorString"),
                        ano=r.get("pubYear"), licenca=r.get("license"),
                        acesso_aberto=r.get("isOpenAccess"))
            if r.get("isOpenAccess") == "Y" and r.get("pmcid"):
                try:
                    x = baixar(f"{EPMC}/{r['pmcid']}/fullTextXML")
                    (DIR_PRIM / f"{r['pmcid']}.xml").write_text(x, encoding="utf-8")
                    info["xml_baixado"] = True
                except Exception as e:
                    info["xml_baixado"] = False
                    info["erro_xml"] = str(e)[:80]
        primarios.append(info)
        oa = "OA " if info.get("acesso_aberto") == "Y" else "-- "
        print(f"  [{n:>3}] {oa} {(info.get('titulo') or titulo or '?')[:64]}")
        time.sleep(0.3)

    (DIR_PRIM / "primarios.json").write_text(
        json.dumps(primarios, ensure_ascii=False, indent=2), encoding="utf-8")
    abertos = [p for p in primarios if p.get("xml_baixado")]
    print(f"\n>>> {len(abertos)}/{len(primarios)} primários com XML integral baixado")


if __name__ == "__main__":
    main()

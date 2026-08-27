# -*- coding: utf-8 -*-
"""EXTRAI E1 — gera o painel de auditoria (HTML autocontido).

Navegação por estudo: ficha de extração campo a campo (gabarito da MA × modelo r1 × r2
× "onde"), RoB domínio a domínio, saída bruta, síntese T3 e prévia mecânica de status.
A prévia NÃO é a correção oficial (sem tolerâncias nem adjudicação) — é um mapa de leitura.

Contém o SELO de perturbação: o HTML gerado é local/privado, não versionado.

Uso: python painel-auditoria.py [saida.html]
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
D1 = RAIZ / "dados" / "estudo1"

CAMPOS = [
    "n_randomizados_gdft", "n_randomizados_controle", "tipo_cirurgia",
    "laparoscopia_gdft", "laparoscopia_controle", "asa_gdft", "asa_controle",
    "fluido_total_gdft", "fluido_total_controle", "cristaloide_gdft", "cristaloide_controle",
    "coloide_gdft", "coloide_controle", "perda_sanguinea_gdft", "perda_sanguinea_controle",
    "uso_inotropico", "morbidade_eventos_gdft", "morbidade_eventos_controle",
    "mortalidade_gdft", "mortalidade_controle", "los_hospitalar_gdft", "los_hospitalar_controle",
    "tempo_flatus_gdft", "tempo_flatus_controle", "tempo_ingesta_oral_gdft",
    "tempo_ingesta_oral_controle", "tempo_evacuacao_gdft", "tempo_evacuacao_controle",
    "ileo_pos_op_gdft", "ileo_pos_op_controle",
]
# campo do formulário -> (tabela da MA, cabeçalho da coluna)
MAPA = {
    "n_randomizados_gdft": (3, "GDFT"), "n_randomizados_controle": (3, "Control"),
    "tipo_cirurgia": (3, "Surgery"),
    "laparoscopia_gdft": (3, "Lap (GDFT)"), "laparoscopia_controle": (3, "Lap (Control)"),
    "asa_gdft": (3, "ASA (GDFT)"), "asa_controle": (3, "ASA (control)"),
    "fluido_total_gdft": (4, "Total fluid (mL) GDFT"), "fluido_total_controle": (4, "Total fluid (mL) Control"),
    "cristaloide_gdft": (4, "Crystalloid (mL) GDFT"), "cristaloide_controle": (4, "Crystalloid (mL) Control"),
    "coloide_gdft": (4, "Colloid (mL) GDFT"), "coloide_controle": (4, "Colloid (mL) Control"),
    "perda_sanguinea_gdft": (4, "Blood loss (mL) GDFT"), "perda_sanguinea_controle": (4, "Blood loss (mL) Control"),
    "uso_inotropico": (4, "Inotrope use"),
    "morbidade_eventos_gdft": (5, "GDFT events n (%)"), "morbidade_eventos_controle": (5, "Control events n (%)"),
    "mortalidade_gdft": (6, "GDFT deaths n (%)"), "mortalidade_controle": (6, "Control deaths n (%)"),
    "los_hospitalar_gdft": (7, "Mean difference (days)"), "los_hospitalar_controle": (7, "95% CI"),
    "tempo_flatus_gdft": (8, "GDFT (mean ± SD)"), "tempo_flatus_controle": (8, "Control (mean ± SD)"),
    "tempo_ingesta_oral_gdft": (9, "GDFT"), "tempo_ingesta_oral_controle": (9, "Control"),
    "tempo_evacuacao_gdft": (10, "GDFT"), "tempo_evacuacao_controle": (10, "Control"),
    "ileo_pos_op_gdft": (11, "GDFT n (%)"), "ileo_pos_op_controle": (11, "Control n (%)"),
}
SO_CALCULO = {"los_hospitalar_gdft", "los_hospitalar_controle"}
ROB_MAPA = [
    ("geracao_sequencia_aleatoria", "Random sequence"), ("ocultacao_alocacao", "Allocation conceal"),
    ("cegamento_participantes_equipe", "Blinding (participants"), ("cegamento_avaliadores_desfecho", "Blinding (outcome"),
    ("dados_desfecho_incompletos", "Incomplete outcome"), ("relato_seletivo", "Selective reporting"),
    ("outros_vieses", "Other bias"), ("risco_global", "Overall risk"),
]


def nums(s):
    if not s:
        return set()
    s = re.sub(r"(?<=\d),(?=\d{3}\b)", "", str(s))
    return set(re.findall(r"\d+(?:\.\d+)?", s))


def parse_json_modelo(content):
    c = content.strip()
    c = re.sub(r"^```(?:json)?\s*|\s*```$", "", c)
    try:
        return json.loads(c), True
    except Exception:
        return {}, False


def contem(valor, alvo):
    return bool(valor) and bool(re.search(r"(?<![\d.,])" + re.escape(alvo) + r"(?![\d.])", str(valor)))


def main():
    saida = Path(sys.argv[1]) if len(sys.argv) > 1 else D1 / "painel-e1.html"
    gab = json.loads((D1 / "gabarito-ma.json").read_text(encoding="utf-8"))
    prim = json.loads((RAIZ / "corpus" / "primarios" / "primarios.json").read_text(encoding="utf-8"))
    selo = json.loads((D1 / "perturbacoes-estudo1.json").read_text(encoding="utf-8"))

    rot = {}
    for p in prim:
        if p.get("xml_baixado"):
            sob = (p.get("autores") or "?").split()[0].rstrip(",")
            rot[p["pmcid"]] = dict(rotulo=f"{sob} et al., {p.get('ano','?')}",
                                   titulo=p.get("titulo", ""), ref=p["ref"])

    # células da MA por (pmcid, tabela)
    ma = {}
    rob_ma = {}
    for t in gab["tabelas"]:
        for l in t["linhas"]:
            pm = l.get("pmcid")
            if not pm:
                continue
            if t["numero"] == 1:
                rob_ma[pm] = l["celulas"]
            else:
                ma[(pm, t["numero"])] = l["celulas"]

    # selo -> campo do formulário
    pert_por_campo = {}
    inv_mapa = {v: k for k, v in MAPA.items()}
    for pm, regs in selo.items():
        for r in regs:
            m = re.search(r"\[alimenta (\w+)", r["campo"])
            campo_form = None
            if m:
                campo_form = m.group(1)
                campo_form = {"cristaloide_gdft": "cristaloide_gdft",
                              "fluido_total": "fluido_total_gdft"}.get(campo_form, campo_form)
            else:
                campo_form = inv_mapa.get((r["tabela"], r["campo"]))
            pert_por_campo.setdefault(pm, []).append(
                dict(campo=campo_form, original=r["original"], perturbado=r["perturbado"]))

    # saídas dos modelos
    modelos = sorted(d.name for d in (D1 / "saidas").iterdir()
                     if d.is_dir() and not d.name.startswith("smoke"))
    dados = {}
    sinteses = {}
    for mod in modelos:
        for f in sorted((D1 / "saidas" / mod).glob("*.json")):
            d = json.loads(f.read_text(encoding="utf-8"))
            if d["tarefa"] == "t3":
                sinteses[mod] = dict(texto=d["content"], dt=d["dt"], tokens=d["tokens"])
                continue
            j, ok = parse_json_modelo(d["content"])
            dados.setdefault(d["pmcid"], {}).setdefault(mod, {})[f"{d['tarefa']}-r{d['replica']}"] = dict(
                json=j, json_ok=ok, bruto=d["content"], dt=round(d["dt"]),
                ptok=d["prompt_tokens"], tok=d["tokens"])

    # monta estrutura por estudo
    estudos = []
    for pm in sorted(rot):
        info = rot[pm]
        perts = pert_por_campo.get(pm, [])
        fichas = {}
        for mod in modelos:
            runs = dados.get(pm, {}).get(mod, {})
            linhas = []
            for campo in CAMPOS:
                tab, col = MAPA[campo]
                cel = ma.get((pm, tab), {})
                gv = cel.get(col)
                gab_txt = gv if gv not in (None, "") else ("sem linha na MA" if not cel else "—")
                r1 = runs.get("t1-r1", {}).get("json", {}).get(campo, {})
                r2 = runs.get("t1-r2", {}).get("json", {}).get(campo, {})
                v1, v2 = r1.get("valor", ""), r2.get("valor", "")
                onde = r1.get("onde", "")
                pert = next((p for p in perts if p["campo"] == campo), None)
                if pert:
                    if contem(v1, pert["perturbado"]):
                        st, cls = f"LEU {pert['perturbado']}", "leu"
                    elif contem(v1, pert["original"]):
                        st, cls = f"RECITOU {pert['original']}", "recitou"
                    else:
                        st, cls = "perturbada · valor não citado", "seal"
                elif campo in SO_CALCULO:
                    st, cls = "MA publica só o cálculo", "calc"
                elif not v1:
                    st, cls = "", "off"
                else:
                    g, m1 = nums(gab_txt if gab_txt not in ("sem linha na MA", "—") else ""), nums(v1)
                    v1nr = str(v1).strip().upper().startswith("NR")
                    gnr = str(gab_txt).strip().upper() in ("NR", "—", "SEM LINHA NA MA")
                    if v1nr and gnr:
                        st, cls = "ambos NR", "nr"
                    elif v1nr:
                        st, cls = "modelo NR · MA tem valor", "warn"
                    elif gnr:
                        st, cls = "modelo achou · MA não tem", "extra"
                    elif g and g <= m1:
                        st, cls = "bate", "ok"
                    elif g & m1:
                        st, cls = "parcial", "warn"
                    elif g:
                        st, cls = "difere", "warn"
                    else:
                        st, cls = "", "off"
                linhas.append(dict(campo=campo, gab=str(gab_txt), v1=str(v1), v2=str(v2),
                                   onde=str(onde), st=st, cls=cls,
                                   pert=(dict(o=pert["original"], p=pert["perturbado"]) if pert else None)))
            rob = []
            rj = runs.get("t2-r1", {}).get("json", {})
            rj2 = runs.get("t2-r2", {}).get("json", {})
            rmac = rob_ma.get(pm, {})
            for chave, prefixo in ROB_MAPA:
                col = next((k for k in rmac if k.lower().startswith(prefixo.lower())), None)
                hv = rmac.get(col, "—")
                m1 = rj.get(chave, {})
                m2 = rj2.get(chave, {})
                j1 = m1.get("julgamento", "")
                conc = "ok" if j1 and hv != "—" and j1.lower() == str(hv).strip().lower() else ("warn" if j1 else "off")
                rob.append(dict(dominio=chave, ma=str(hv), j1=j1, just=m1.get("justificativa", ""),
                                j2=m2.get("julgamento", ""), cls=conc))
            fichas[mod] = dict(
                linhas=linhas, rob=rob,
                meta={k: dict(dt=v["dt"], ptok=v["ptok"], tok=v["tok"], json_ok=v["json_ok"])
                      for k, v in runs.items()},
                bruto={k: v["bruto"] for k, v in runs.items() if k.startswith("t1") or k.startswith("t2")})
        estudos.append(dict(pmcid=pm, rotulo=info["rotulo"], titulo=info["titulo"],
                            ref=info["ref"], perts=perts, fichas=fichas))

    payload = json.dumps(dict(estudos=estudos, modelos=modelos, sinteses=sinteses),
                         ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.replace("__DATA__", payload)
    saida.write_text(html, encoding="utf-8")
    n_runs = sum(len(v) for e in estudos for v in
                 (f["meta"] for f in e["fichas"].values()))
    print(f"painel: {saida} — {len(estudos)} estudos, {len(modelos)} modelo(s), {n_runs} corridas, {len(html):,} bytes")


TEMPLATE = r"""<title>Auditoria EXTRAI</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Source+Sans+3:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --bg:#F7F8F6;--surface:#FFFFFF;--ink:#1C2422;--muted:#5A6663;--line:#DDE3E0;
  --accent:#0E6E5C;--accent-ink:#0A5546;--rail:#EEF1EF;
  --ok:#1A7F4B;--ok-bg:#E4F2E9;--warn:#8A6100;--warn-bg:#F6EDD4;--bad:#B3352B;--bad-bg:#F8E4E1;
  --seal:#7A4FA3;--seal-bg:#EFE7F7;--nr:#5A6663;--nr-bg:#ECEEED;--extra:#0B6376;--extra-bg:#DFF0F4;
  --mono:"IBM Plex Mono",Consolas,monospace;--sans:"Source Sans 3",system-ui,sans-serif;
  --disp:"Fraunces",Georgia,serif;
}
:root:not([data-theme="light"]){}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#101513;--surface:#171E1B;--ink:#E6EBE8;--muted:#93A09B;--line:#28322D;
  --accent:#3FBF9F;--accent-ink:#63D4B8;--rail:#141A17;
  --ok:#57C288;--ok-bg:#12281B;--warn:#D9A93F;--warn-bg:#2A2312;--bad:#E07B70;--bad-bg:#301713;
  --seal:#B08AD9;--seal-bg:#241A31;--nr:#93A09B;--nr-bg:#1D2421;--extra:#5BB8CC;--extra-bg:#0F2429;
}}
:root[data-theme="dark"]{
  --bg:#101513;--surface:#171E1B;--ink:#E6EBE8;--muted:#93A09B;--line:#28322D;
  --accent:#3FBF9F;--accent-ink:#63D4B8;--rail:#141A17;
  --ok:#57C288;--ok-bg:#12281B;--warn:#D9A93F;--warn-bg:#2A2312;--bad:#E07B70;--bad-bg:#301713;
  --seal:#B08AD9;--seal-bg:#241A31;--nr:#93A09B;--nr-bg:#1D2421;--extra:#5BB8CC;--extra-bg:#0F2429;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.45}
.wrap{display:flex;min-height:100vh}
nav{width:250px;flex-shrink:0;background:var(--rail);border-right:1px solid var(--line);padding:18px 12px;position:sticky;top:0;height:100vh;overflow-y:auto}
nav h1{font-family:var(--disp);font-size:21px;margin:2px 6px 2px;color:var(--accent-ink)}
nav .sub{font-size:12px;color:var(--muted);margin:0 6px 14px}
nav button{display:block;width:100%;text-align:left;background:none;border:0;border-radius:8px;padding:8px 10px;margin:2px 0;cursor:pointer;color:var(--ink);font:inherit}
nav button:hover{background:var(--line)}
nav button.on{background:var(--accent);color:#fff}
nav button .pm{display:block;font-family:var(--mono);font-size:10.5px;opacity:.75}
main{flex:1;min-width:0;padding:22px 26px 60px}
.aviso{background:var(--seal-bg);border:1px solid var(--seal);color:var(--ink);border-radius:10px;padding:10px 14px;font-size:13.5px;margin-bottom:14px}
.aviso b{color:var(--seal)}
.como{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 16px;font-size:13.5px;margin-bottom:18px}
.como b{color:var(--accent-ink)}
.hdr{margin:6px 0 4px;font-family:var(--disp);font-size:26px;text-wrap:balance}
.cit{color:var(--muted);font-size:13px;margin-bottom:10px;max-width:70ch}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 16px}
.chip{font-family:var(--mono);font-size:11.5px;padding:3px 9px;border-radius:99px;border:1px solid var(--line);background:var(--surface)}
.chip.seal{border-color:var(--seal);color:var(--seal);background:var(--seal-bg)}
.tabs{display:flex;gap:4px;margin-bottom:0;border-bottom:1px solid var(--line)}
.tabs button{background:none;border:0;border-bottom:2px solid transparent;padding:8px 14px;font:inherit;font-weight:600;color:var(--muted);cursor:pointer}
.tabs button.on{color:var(--accent-ink);border-bottom-color:var(--accent)}
.msel{float:right;font-size:13px;color:var(--muted)}
.msel select{font:inherit;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:3px 6px}
.tblwrap{overflow-x:auto;background:var(--surface);border:1px solid var(--line);border-radius:0 0 10px 10px}
table{border-collapse:collapse;width:100%;font-size:13px}
th{position:sticky;top:0;background:var(--surface);text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);padding:9px 10px;border-bottom:1px solid var(--line);z-index:1}
td{padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:0}
td.campo{font-weight:600;white-space:nowrap;font-size:12.5px}
td.num{font-family:var(--mono);font-size:12.5px}
td.gab{font-family:var(--mono);font-size:12.5px;color:var(--muted)}
td.onde{color:var(--muted);font-size:12px}
.st{display:inline-block;font-family:var(--mono);font-size:10.5px;padding:2px 8px;border-radius:99px;white-space:nowrap}
.st.ok{background:var(--ok-bg);color:var(--ok)} .st.warn{background:var(--warn-bg);color:var(--warn)}
.st.leu{background:var(--ok-bg);color:var(--ok);border:1px solid var(--ok)}
.st.recitou{background:var(--bad-bg);color:var(--bad);border:1px solid var(--bad)}
.st.seal{background:var(--seal-bg);color:var(--seal)} .st.nr{background:var(--nr-bg);color:var(--nr)}
.st.extra{background:var(--extra-bg);color:var(--extra)} .st.calc,.st.off{background:var(--nr-bg);color:var(--nr)}
.leg{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 6px;font-size:12px;color:var(--muted)}
details{background:var(--surface);border:1px solid var(--line);border-radius:10px;margin:10px 0;padding:0}
details summary{cursor:pointer;padding:10px 14px;font-weight:600;font-size:13.5px}
details pre{margin:0;padding:12px 16px;overflow-x:auto;font-family:var(--mono);font-size:12px;line-height:1.5;border-top:1px solid var(--line);white-space:pre-wrap;word-break:break-word}
.meta{font-family:var(--mono);font-size:11.5px;color:var(--muted);margin:8px 2px}
.sint{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px 20px;max-width:75ch;white-space:pre-wrap}
.vazio{color:var(--muted);padding:30px;text-align:center}
button:focus-visible,select:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
@media (max-width:760px){.wrap{flex-direction:column}nav{width:100%;height:auto;position:static;display:flex;flex-wrap:wrap;gap:4px}nav h1,nav .sub{width:100%}}
</style>
<div class="wrap">
<nav id="rail"></nav>
<main id="main"></main>
</div>
<script>
const D = __DATA__;
let estudoAtual = 0, aba = 'ficha', modelo = D.modelos[0] || null;
const $ = (h) => { const t = document.createElement('template'); t.innerHTML = h.trim(); return t.content; };
const esc = (s) => String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');

function rail(){
  const el = document.getElementById('rail');
  el.innerHTML = '<h1>Auditoria EXTRAI</h1><div class="sub">Estudo 1 · fichas de extração e a comparação com a metanálise</div>';
  D.estudos.forEach((e,i)=>{
    const b = document.createElement('button');
    b.className = i===estudoAtual ? 'on':'';
    b.innerHTML = `${esc(e.rotulo)} <span class="pm">${esc(e.pmcid)} · ref ${esc(e.ref)}</span>`;
    b.onclick = ()=>{estudoAtual=i; render();};
    el.appendChild(b);
  });
  const s = document.createElement('button');
  s.innerHTML = `<b>Sínteses (T3)</b> <span class="pm">uma por modelo</span>`;
  s.className = estudoAtual===-1?'on':'';
  s.onclick = ()=>{estudoAtual=-1; render();};
  el.appendChild(s);
}

function cab(e){
  const perts = e.perts.map(p=>`<span class="chip seal">🔒 ${esc(p.original)} → ${esc(p.perturbado)}</span>`).join('');
  return `<div class="hdr">${esc(e.rotulo)}</div>
  <div class="cit">${esc(e.titulo)} · <span style="font-family:var(--mono)">${esc(e.pmcid)}</span></div>
  <div class="chips">${perts}</div>`;
}

function abas(){
  const nomes = {ficha:'Ficha T1', rob:'Risco de viés T2', bruto:'Saída bruta'};
  const sel = D.modelos.length>1 ? `<span class="msel">modelo <select onchange="modelo=this.value;render()">${D.modelos.map(m=>`<option ${m===modelo?'selected':''}>${m}</option>`).join('')}</select></span>` : `<span class="msel">modelo: <b>${esc(modelo)}</b></span>`;
  return `<div class="tabs">${Object.entries(nomes).map(([k,v])=>`<button class="${k===aba?'on':''}" onclick="aba='${k}';render()">${v}</button>`).join('')}${sel}</div>`;
}

function ficha(e){
  const f = e.fichas[modelo];
  if(!f || !f.linhas.some(l=>l.v1)) return '<div class="vazio">Este modelo ainda não extraiu este estudo — a fila continua rodando.</div>';
  const m = f.meta['t1-r1']||{}; const m2 = f.meta['t1-r2']||{};
  const linhas = f.linhas.map(l=>`<tr>
    <td class="campo">${esc(l.campo)}</td>
    <td class="gab">${esc(l.gab)}</td>
    <td class="num">${esc(l.v1)}</td>
    <td class="num">${esc(l.v2)}</td>
    <td class="onde">${esc(l.onde)}</td>
    <td>${l.st?`<span class="st ${l.cls}">${esc(l.st)}</span>`:''}</td>
  </tr>`).join('');
  return `<div class="meta">r1: ${m.dt||'?'}s · ${m.ptok||'?'}+${m.tok||'?'} tokens ${m.json_ok?'· JSON ✓':'· JSON inválido'} &nbsp;|&nbsp; r2: ${m2.dt||'?'}s ${m2.json_ok?'· JSON ✓':''}</div>
  <div class="tblwrap"><table>
  <thead><tr><th>campo</th><th>gabarito (MA publicada)</th><th>modelo · r1</th><th>modelo · r2</th><th>onde (segundo o modelo)</th><th>prévia</th></tr></thead>
  <tbody>${linhas}</tbody></table></div>
  <div class="leg">
    <span class="st leu">LEU</span> devolveu o valor perturbado (só existe no texto que ele recebeu)
    <span class="st recitou">RECITOU</span> devolveu o original publicado — contaminação
    <span class="st ok">bate</span> números do gabarito presentes na resposta
    <span class="st warn">difere / modelo NR</span> vai a adjudicação
    <span class="st extra">modelo achou</span> valor que a MA não registrou (candidato a errata da MA)
    <span class="st nr">ambos NR</span>
  </div>`;
}

function rob(e){
  const f = e.fichas[modelo];
  if(!f || !f.rob.some(r=>r.j1)) return '<div class="vazio">RoB ainda não medido para este estudo.</div>';
  const linhas = f.rob.map(r=>`<tr>
    <td class="campo">${esc(r.dominio)}</td>
    <td class="num">${esc(r.ma)}</td>
    <td class="num">${esc(r.j1)}</td>
    <td class="num">${esc(r.j2)}</td>
    <td class="onde">${esc(r.just)}</td>
    <td>${r.j1?`<span class="st ${r.cls}">${r.cls==='ok'?'concorda':'diverge'}</span>`:''}</td>
  </tr>`).join('');
  return `<div class="tblwrap"><table>
  <thead><tr><th>domínio</th><th>revisores da MA</th><th>modelo · r1</th><th>r2</th><th>justificativa do modelo (r1)</th><th>prévia</th></tr></thead>
  <tbody>${linhas}</tbody></table></div>`;
}

function bruto(e){
  const f = e.fichas[modelo];
  if(!f) return '<div class="vazio">Sem saídas ainda.</div>';
  return Object.entries(f.bruto).map(([k,v])=>`<details><summary>${esc(modelo)} · ${esc(k)} — resposta bruta do modelo, sem edição</summary><pre>${esc(v)}</pre></details>`).join('') || '<div class="vazio">Sem saídas ainda.</div>';
}

function sinteses(){
  const blocos = Object.entries(D.sinteses);
  if(!blocos.length) return '<div class="hdr">Sínteses (T3)</div><div class="vazio">Nenhum modelo chegou à síntese ainda — ela roda ao fim do bloco de cada modelo.</div>';
  return '<div class="hdr">Sínteses (T3)</div>' + blocos.map(([m,s])=>
    `<h3 style="font-family:var(--disp)">${esc(m)} <span class="meta">${Math.round(s.dt)}s · ${s.tokens} tokens</span></h3><div class="sint">${esc(s.texto)}</div>`).join('');
}

function render(){
  rail();
  const el = document.getElementById('main');
  const como = `<div class="aviso"><b>Contém o selo de perturbação</b> — este painel mostra os pares original→perturbado. Não compartilhe antes da correção oficial publicar o selo.</div>
  <div class="como"><b>Quem fez o quê:</b> o <b>modelo local</b> leu o artigo perturbado e preencheu a ficha (colunas r1/r2 e "onde", citadas verbatim) · o <b>meu script</b> montou este painel e calculou a coluna "prévia" por comparação ingênua de números com o gabarito · a <b>correção oficial</b> (tolerâncias, deriváveis, adjudicação contra a fonte) ainda não rodou — nada aqui é nota.</div>`;
  if(estudoAtual===-1){ el.innerHTML = como + sinteses(); return; }
  const e = D.estudos[estudoAtual];
  el.innerHTML = como + cab(e) + abas() + (aba==='ficha'?ficha(e):aba==='rob'?rob(e):bruto(e));
}
render();
</script>"""


if __name__ == "__main__":
    main()

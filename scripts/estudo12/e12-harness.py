# -*- coding: utf-8 -*-
"""O harness da campanha do Estudo 12. Instrumentos 1 a 4 da §8.

Por que existe um harness novo, em vez de um argumento a mais no antigo. O contexto desta campanha é
24.576, e o único lugar onde o contexto vive hoje é `CTX = 16384`, uma constante de módulo em
`scripts/estudo3/e3-harness.py` que sete estudos registrados importam, direta ou indiretamente. Mudar
lá redefiniria em silêncio a configuração declarada de todos eles. Então o transporte é reusado — a
mesma função HTTP, o mesmo tempo limite — e as opções da chamada são deste módulo.

Os quatro instrumentos:

  1. contexto próprio      num_ctx 24.576 no corpo do pedido, sem tocar em e3-harness.py
  2. portão de retomada    por CHAMADA, e por integridade, não por existência. Um arquivo que não
                           abre, que não tem os campos previstos, ou que foi truncado pelo teto de
                           saída (done_reason == "length") não conta como feito: sai do caminho com o
                           motivo anotado e a chamada é refeita.
  3. escrita atômica       arquivo temporário e rename. Nenhum script do repositório fazia isso, e
                           escrita direta atrás de um portão de existência é uma janela em que uma
                           interrupção deixa meio arquivo que a retomada aceita como pronto.
  4. registro por chamada  modelo, tag, âncora, ficha, ensaio, réplica, tokens de entrada e de saída,
                           done_reason, duração e o SHA-256 do prompt efetivamente enviado. O caminho
                           de orquestração descartava tudo isso, e por isso truncamento nunca foi
                           detectável depois do fato.

A regra de operação do pesquisador — "faça de forma que se for interrompido possamos continuar de onde
parou" — é o que os instrumentos 2, 3 e 4 servem. Interromper com Ctrl-C custa, no máximo, a chamada
em curso.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = Path(__file__).resolve().parents[2]
AQUI = Path(__file__).resolve().parent

CTX = 24576                     # §3 do protocolo, congelado
SAIDA = {"v1": 4000, "v2": 8000}
REPLICAS = 2
LIMITE_ERROS_SEGUIDOS = 5      # o servidor caiu; não faz sentido gastar o resto do plano
CAMPOS_OBRIGATORIOS = ("modelo", "tag", "ancora", "ficha", "ensaio", "replica",
                       "conteudo", "prompt_tokens", "tokens", "finish", "dt", "sha_prompt")


def _carrega(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# O registro de modelos é montado em três camadas, e a ordem importa. `e4-extensao.py` injeta os três
# modelos do Estudo 4 no h3 QUE ELE MESMO CARREGOU -- um objeto de módulo próprio, porque cada
# importlib cria um novo. Carregar o e3-harness por conta e esperar que a injeção apareça nele é o
# defeito que fazia quatro dos seis modelos do elenco sumirem: a campanha rodaria gemma12 e qwen14 e
# depois gravaria 464 arquivos de erro em segundos, terminando com código zero. O e9-extract, que de
# fato rodou, faz a coisa certa: pega `ext.h3`. E o sexto modelo não se injeta sozinho -- o
# e8-amend1-cast só define `registrar(h3)`, que precisa ser chamado.
_ext = _carrega("ext", RAIZ / "scripts" / "estudo4" / "e4-extensao.py")
h3 = _ext.h3                                                             # o h3 que a extensão mutou
_am1 = _carrega("am1", RAIZ / "scripts" / "estudo8" / "e8-amend1-cast.py")
_am1.registrar(h3)                                                       # e o sexto leitor

# §3 do protocolo: o elenco, e a ordem do elenco é a ordem das corridas
ELENCO = ["gemma12", "qwen14", "llama8", "qwen35", "deepseek14", "qwen27q2"]

_faltam = [m for m in ELENCO if m not in h3.MODELS]
if _faltam:
    raise SystemExit(f"elenco incompleto no registro do harness: {_faltam}. "
                     f"Registrados: {sorted(h3.MODELS)}. A campanha não pode começar.")

ANCORAS = {
    "a1": dict(corpus=[RAIZ / "corpus" / "perturbados", RAIZ / "corpus" / "perturbados-fechados"],
               fichas={"v1": RAIZ / "dados" / "instruments-en" / "estudo1" / "t1-extraction.txt",
                       "v2": RAIZ / "dados" / "estudo9" / "prompts" / "t1-extraction-v2.txt"}),
    "a2": dict(corpus=[RAIZ / "corpus" / "estudo3" / "perturbados"],
               fichas={"v1": RAIZ / "dados" / "instruments-en" / "estudo3" / "e3-extraction.txt",
                       "v2": RAIZ / "dados" / "estudo9" / "prompts" / "e3-extraction-v2.txt"}),
    "a3": dict(corpus=[RAIZ / "corpus" / "estudo12" / "perturbados"],
               fichas={"v1": RAIZ / "dados" / "estudo12" / "prompts" / "a3-extraction.txt",
                       "v2": RAIZ / "dados" / "estudo12" / "prompts" / "a3-extraction-v2.txt"}),
}
# ------------------------------------------------------------------ as fichas, seladas
# O vínculo com as fichas era por CAMINHO. Uma edição em qualquer uma delas trocaria o instrumento
# sem que nada acusasse -- e as das âncoras 1 e 2 são as congeladas que produziram o registro
# publicado, o controle da H12.5. Agora o vínculo é por SHA-256, conferido antes da primeira chamada.
def confere_fichas():
    reg = {}
    p = RAIZ / "dados" / "estudo12" / "fichas.sha256"
    for linha in io.open(p, encoding="utf-8").read().splitlines():
        if linha.startswith("#") or not linha.strip():
            continue
        sha, rot, rel = linha.split(None, 2)
        reg[rot] = (sha, rel.strip())
    ruins = []
    for rot, (sha, rel) in sorted(reg.items()):
        agora = hashlib.sha256(io.open(RAIZ / rel, "rb").read()).hexdigest()
        if agora != sha:
            ruins.append(f"{rot} ({rel}): selado {sha[:12]}…, agora {agora[:12]}…")
    if ruins:
        raise SystemExit("as fichas da campanha não batem com os selos registrados:\n  "
                         + "\n  ".join(ruins)
                         + "\nSe a mudança é deliberada, regenere com e12-sela-fichas.py e "
                           "registre a decisão; se não é, desfaça-a antes de rodar.")
    return len(reg)


TIMEOUT = 1800   # dez vezes a chamada mais lenta medida; o transporte herdado usava 7.200

# E12_SAIDAS redireciona o diretorio de saidas. Serve ao teste do inventario, que precisa montar
# corridas parciais em disco sem tocar na campanha de verdade, e a uma corrida de ensaio.
SAIDAS = Path(os.environ.get("E12_SAIDAS") or (RAIZ / "dados" / "estudo12" / "saidas"))
RECUSADOS = Path(os.environ.get("E12_RECUSADOS") or (RAIZ / "dados" / "estudo12" / "recusados"))


# ------------------------------------------------------------------ trava de instancia unica
# Dois harness na mesma maquina nao dobram a vazao: disputam a mesma GPU, e o ollama so mantem um
# modelo residente. Medido em 10/09/2026 com dois processos: a chamada passou de 3,3 para 7,0 min e
# parte das chamadas foi refeita. Escrita atomica e portao de integridade impediram estrago, mas o
# custo foi de horas -- e o harness aceitou o segundo lancamento em silencio.
#
# A trava e um CADEADO do sistema operacional sobre um byte do arquivo, nao um PID anotado. O SO o
# solta em qualquer morte do processo -- Ctrl-C, kill, janela fechada, queda de energia -- e um
# segundo processo que tente o mesmo byte falha na hora. Nao ha adivinhacao de PID, nao ha trava
# orfa, nao ha janela entre "olhei" e "escrevi". O JSON no comeco do arquivo e so para o humano saber
# de quem e; o cadeado fica num byte alto, para que esse JSON continue legivel por quem perdeu. O
# arquivo nunca e apagado: ao soltar, o dono anota "encerrado" e vai embora.
#
# A chave e a MAQUINA, nao o diretorio de saida: o que se disputa e a GPU. E12_SAIDAS continua
# isolando as saidas dos testes; a trava so muda com E12_TRAVA, que existe para os testes e para
# mais nada. Uma corrida de ensaio com E12_SAIDAS redirecionado disputa a mesma GPU e tem de ser
# barrada como qualquer outra.
TRAVA = Path(os.environ.get("E12_TRAVA") or (RAIZ / "dados" / "estudo12" / "harness.trava"))
NL = chr(10)
_BYTE_DO_CADEADO = 1 << 20      # 1 MiB adiante do JSON: quem perdeu ainda le quem ganhou
_fd_trava = None


def _tranca(fd):
    if os.name == "nt":
        import msvcrt
        os.lseek(fd, _BYTE_DO_CADEADO, 0)
        msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
    else:
        import fcntl
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)


def _destranca(fd):
    if os.name == "nt":
        import msvcrt
        os.lseek(fd, _BYTE_DO_CADEADO, 0)
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
    else:
        import fcntl
        fcntl.flock(fd, fcntl.LOCK_UN)


def _le_dono():
    """O JSON dos primeiros bytes, ou None se nao houver ou nao for legivel."""
    try:
        with io.open(TRAVA, encoding="utf-8", errors="replace") as f:
            return json.loads(f.read(8192))
    except Exception:
        return None


def _idade(inicio):
    try:
        t = time.mktime(time.strptime(inicio, "%Y-%m-%d %H:%M:%S"))
        m = int((time.time() - t) // 60)
        return f"{m // 60} h {m % 60} min" if m >= 60 else f"{m} min"
    except Exception:
        return "?"


def toma_trava():
    """Tranca, ou recusa em voz alta. Devolve um aviso para imprimir, ou vazio."""
    global _fd_trava
    if _fd_trava is not None:
        # o cadeado do Windows e por handle, nao por processo: uma segunda tomada no mesmo
        # processo falharia acusando o proprio PID. Melhor dizer o que e.
        raise RuntimeError("toma_trava chamada duas vezes no mesmo processo")
    TRAVA.parent.mkdir(parents=True, exist_ok=True)
    existia = TRAVA.exists()          # ANTES do os.open, que cria o arquivo
    anterior = _le_dono() if existia else None
    fd = os.open(str(TRAVA), os.O_RDWR | os.O_CREAT, 0o644)
    try:
        _tranca(fd)
    except OSError:
        os.close(fd)
        dono = _le_dono() or {}
        pid, inicio = dono.get("pid", "?"), dono.get("inicio", "?")
        argv = " ".join(dono.get("argv") or []) or "(sem argumentos)"
        raise SystemExit(
            f"ja ha um harness rodando: PID {pid}, desde {inicio} ({_idade(inicio)}), com: {argv}"
            f"{NL}Dois harness competem pela mesma GPU e refazem trabalho."
            f"{NL}Para ver onde a campanha esta:  python scripts/estudo12/e12-inventario.py"
            f"{NL}Para conferir aquele processo:   tasklist /FI \"PID eq {pid}\"")
    _fd_trava = fd
    os.lseek(fd, 0, 0)
    os.ftruncate(fd, 0)
    os.write(fd, json.dumps({"pid": os.getpid(), "inicio": time.strftime("%Y-%m-%d %H:%M:%S"),
                             "argv": sys.argv[1:]}, ensure_ascii=False).encode("utf-8"))
    if not existia:
        return ""
    if anterior is None:
        return "trava anterior ilegivel, e ninguem a segurava — assumindo"
    if anterior.get("encerrado"):
        return ""
    return (f"trava anterior do PID {anterior.get('pid', '?')} ficou sem encerrar "
            f"(morreu sem soltar), e ninguem a segurava — assumindo")


def solta_trava():
    """Anota o encerramento e solta o cadeado. Nao apaga: reprovado e registrado, e trava tambem."""
    global _fd_trava
    fd, _fd_trava = _fd_trava, None
    if fd is None:
        return
    try:
        os.lseek(fd, 0, 0)
        os.ftruncate(fd, 0)
        os.write(fd, json.dumps({"pid": os.getpid(),
                                 "encerrado": time.strftime("%Y-%m-%d %H:%M:%S")}).encode("utf-8"))
        _destranca(fd)
    except Exception:
        pass
    finally:
        try:
            os.close(fd)
        except Exception:
            pass



# ------------------------------------------------------------------ o plano, enumerado
# §4 do protocolo: quantos ensaios cada âncora tem. O plano era um glob de disco, e um diretório
# que sumisse encolhia a campanha em silêncio -- a corrida terminaria "completa" com menos chamadas.
ENSAIOS_ESPERADOS = {"a1": 14, "a2": 7, "a3": 8}


def ensaios(ancora):
    fora = []
    for d in ANCORAS[ancora]["corpus"]:
        fora += [(p.stem, p) for p in sorted(d.glob("*.txt"))]
    esperado = ENSAIOS_ESPERADOS[ancora]
    if len(fora) != esperado:
        raise SystemExit(f"âncora {ancora}: {len(fora)} ensaios em disco, e o protocolo declara "
                         f"{esperado}. A campanha não pode começar com o corpus incompleto.")
    return fora


def plano():
    """As chamadas da campanha, na ordem em que rodam. Um modelo residente por vez."""
    for modelo in ELENCO:
        for ancora in ("a1", "a2", "a3"):
            for ficha in ("v1", "v2"):
                for tid, caminho in ensaios(ancora):
                    for rep in range(1, REPLICAS + 1):
                        yield dict(modelo=modelo, ancora=ancora, ficha=ficha,
                                   ensaio=tid, replica=rep, caminho=caminho)


def destino(c):
    return SAIDAS / c["ancora"] / c["ficha"] / c["modelo"] / f"{c['ensaio']}-r{c['replica']}.json"


# ------------------------------------------------------------------ instrumento 2: portão por integridade
def integro(p, c=None, sha_esperado=None):
    """(ok, motivo). Existir não basta.

    Cinco perguntas, e a última é a que a revisão adversarial obrigou a acrescentar: o arquivo abre?
    tem os campos? não foi truncado pelo teto? não está vazio? e -- decisiva numa campanha de dois
    dias -- **foi produzido pelo mesmo prompt que rodaríamos agora**? O harness já gravava o SHA do
    prompt enviado e ninguém o conferia: uma ficha ou um corpus editados no meio produziriam um
    conjunto meio antigo e meio novo, com nada acusando. Também confere a identidade e a
    configuração, porque um arquivo no lugar errado é indistinguível de um arquivo certo sem isso.
    """
    try:
        j = json.loads(io.open(p, encoding="utf-8").read())
    except Exception as e:
        return False, f"não abre como JSON: {type(e).__name__}"
    faltam = [k for k in CAMPOS_OBRIGATORIOS if k not in j]
    if faltam:
        return False, "faltam campos: " + ", ".join(faltam)
    if j.get("finish") == "length":
        return False, "saída truncada pelo teto (done_reason=length)"
    if not str(j.get("conteudo", "")).strip():
        return False, "conteúdo vazio"
    if c:
        for campo in ("modelo", "ancora", "ficha", "ensaio", "replica"):
            if str(j.get(campo)) != str(c[campo]):
                return False, f"identidade não bate: {campo} gravado {j.get(campo)!r}, esperado {c[campo]!r}"
        if j.get("num_ctx") != CTX:
            return False, f"contexto gravado {j.get('num_ctx')}, e o protocolo congela {CTX}"
        if j.get("num_predict") != SAIDA[c["ficha"]]:
            return False, f"teto de saída gravado {j.get('num_predict')}, esperado {SAIDA[c['ficha']]}"
    if sha_esperado and j.get("sha_prompt") != sha_esperado:
        return False, ("produzido por outro prompt: a ficha ou o corpus mudaram desde esta chamada "
                       f"({str(j.get('sha_prompt'))[:12]}… contra {sha_esperado[:12]}…)")
    return True, ""


def afasta(p, motivo):
    """Recusado é registrado, não apagado."""
    RECUSADOS.mkdir(parents=True, exist_ok=True)
    alvo = RECUSADOS / f"{p.parent.parent.parent.name}-{p.parent.parent.name}-{p.parent.name}-{p.name}"
    i = 0
    while alvo.exists():
        i += 1
        alvo = alvo.with_suffix(f".{i}.json")
    os.replace(p, alvo)
    io.open(alvo.with_suffix(alvo.suffix + ".motivo"), "w", encoding="utf-8").write(motivo + "\n")


# ------------------------------------------------------------------ instrumento 3: escrita atômica
def grava(p, obj):
    """Temporário no mesmo diretório e rename. Rename é atômico; escrita não é."""
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), suffix=".parcial")
    try:
        with io.open(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, p)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


# ------------------------------------------------------------------ instrumentos 1 e 4: a chamada
def descarrega(tag=None):
    for t in ([tag] if tag else sorted({m["ollama"] for m in h3.MODELS.values()})):
        subprocess.run(["ollama", "stop", t], capture_output=True)


def monta(tpl, texto):
    return tpl.replace("{ARTICLE}", texto) if "{ARTICLE}" in tpl else tpl + texto


def chama(c, prompt):
    m = h3.MODELS[c["modelo"]]
    opts = dict(num_predict=SAIDA[c["ficha"]], num_ctx=CTX)
    if m["cpu"]:
        opts["num_gpu"] = 0
    body = dict(model=m["ollama"], prompt=prompt, stream=False, think=False, options=opts)
    r, dt = h3.post_json(h3.OLLAMA + "/api/generate", body, timeout=TIMEOUT)
    if r.get("error"):
        raise RuntimeError(r["error"])
    return dict(modelo=c["modelo"], tag=m["ollama"], ancora=c["ancora"], ficha=c["ficha"],
                ensaio=c["ensaio"], replica=c["replica"],
                conteudo=r.get("response", "") or "",
                prompt_tokens=r.get("prompt_eval_count", 0), tokens=r.get("eval_count", 0),
                finish=r.get("done_reason"), dt=round(r.get("total_duration", 0) / 1e9 or dt, 2),
                num_ctx=CTX, num_predict=SAIDA[c["ficha"]],
                sha_prompt=hashlib.sha256(prompt.encode("utf-8")).hexdigest())


# ------------------------------------------------------------------ a corrida
def roda(so_modelo=None, so_ancora=None, so_ficha=None, seco=False):
    """Toma a trava se for chamar modelo; corrida seca nao disputa GPU e nao a toma."""
    if seco:
        return _roda(so_modelo, so_ancora, so_ficha, seco)
    aviso = toma_trava()
    if aviso:
        print(aviso, flush=True)
    try:
        return _roda(so_modelo, so_ancora, so_ficha, seco)
    finally:
        solta_trava()


def _roda(so_modelo=None, so_ancora=None, so_ficha=None, seco=False):
    todas = [c for c in plano()
             if (not so_modelo or c["modelo"] == so_modelo)
             and (not so_ancora or c["ancora"] == so_ancora)
             and (not so_ficha or c["ficha"] == so_ficha)]
    n_fichas = confere_fichas()
    print(f"plano: {len(todas)} chamadas · contexto {CTX} · saída {SAIDA} · tempo limite {TIMEOUT}s")
    print(f"fichas conferidas contra os selos: {n_fichas} de {n_fichas}")
    residente, feitas, puladas, refeitas, erros = None, 0, 0, 0, 0
    t0 = time.time()
    seguidos = 0
    for i, c in enumerate(todas, 1):
        p = destino(c)
        # o prompt é montado ANTES do portão, porque o portão precisa do selo dele
        tpl = io.open(ANCORAS[c["ancora"]]["fichas"][c["ficha"]], encoding="utf-8").read()
        prompt = monta(tpl, io.open(c["caminho"], encoding="utf-8").read())
        sha = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
        if p.exists():
            ok, motivo = integro(p, c, sha)
            if ok:
                puladas += 1
                continue
            if seco:
                # corrida seca RELATA o que faria; mover e decisao de corrida de verdade. A
                # revisao de 11/09/2026 provou que --seco movia saidas da campanha em curso.
                print(f"  [{i}/{len(todas)}] {p.name}: SERIA RECUSADO — {motivo}", flush=True)
            else:
                print(f"  [{i}/{len(todas)}] {p.name}: RECUSADO — {motivo}", flush=True)
                try:
                    afasta(p, motivo)
                except OSError as e:
                    # alguem mexeu no arquivo entre o portao e o afastamento: a proxima
                    # passada decide; nao e motivo para derrubar uma corrida de 40 h
                    print(f"      nao consegui afastar ({type(e).__name__}); sigo", flush=True)
            refeitas += 1
        if seco:
            feitas += 1
            continue
        if residente != c["modelo"]:
            # descarrega TUDO antes do primeiro, porque pode haver modelo residente de outra corrida
            descarrega(h3.MODELS[residente]["ollama"] if residente else None)
            residente = c["modelo"]
            print(f"\n=== modelo residente: {residente} ({h3.MODELS[residente]['ollama']})", flush=True)
        try:
            r = chama(c, prompt)
        except KeyboardInterrupt:
            print("\ninterrompido. Nada a meio: a chamada em curso não foi gravada.", flush=True)
            descarrega(h3.MODELS[residente]["ollama"])
            raise
        except Exception as e:
            erros += 1
            seguidos += 1
            print(f"  [{i}/{len(todas)}] {c['modelo']} {c['ancora']}/{c['ficha']}/{c['ensaio']}-r"
                  f"{c['replica']}: ERRO {type(e).__name__}: {str(e)[:120]}", flush=True)
            try:
                # nome único: com nome fixo, a segunda falha da mesma chamada apagava a primeira,
                # e o método manda registrar o reprovado, não substituí-lo.
                RECUSADOS.mkdir(parents=True, exist_ok=True)
                base = (f"erro-{c['modelo']}-{c['ancora']}-{c['ficha']}-{c['ensaio']}"
                        f"-r{c['replica']}")
                k = 0
                alvo = RECUSADOS / f"{base}.json"
                while alvo.exists():
                    k += 1
                    alvo = RECUSADOS / f"{base}.{k}.json"
                grava(alvo, dict(**{k_: c[k_] for k_ in ("modelo", "ancora", "ficha", "ensaio", "replica")},
                                 tentativa=k + 1, erro=f"{type(e).__name__}: {e}"))
            except Exception:
                pass
            # disjuntor: com o servidor fora do ar a corrida gastaria as 696 chamadas em segundos,
            # gravaria 696 arquivos de erro e sairia com código zero, parecendo ter terminado.
            if seguidos >= LIMITE_ERROS_SEGUIDOS:
                if residente:
                    descarrega(h3.MODELS[residente]["ollama"])
                raise SystemExit(f"\n{seguidos} erros seguidos: o servidor parece fora do ar. "
                                 f"A corrida para aqui, e o que já ficou pronto é aproveitado na "
                                 f"próxima. Veja: python scripts/estudo12/e12-inventario.py")
            continue
        seguidos = 0
        try:
            grava(p, r)
            # a saída acabou de ser escrita: ela passa pelo MESMO portão da retomada, agora. Sem
            # isso, uma saída truncada pelo teto era contada como feita na própria corrida que a
            # produziu, e só a segunda passada a refaria -- a primeira terminava dizendo "completa".
            bom, motivo = integro(p, c, sha)
            if not bom:
                print(f"  [{i}/{len(todas)}] RECUSADA ao nascer — {motivo}", flush=True)
                afasta(p, motivo)
                erros += 1
                continue
        except Exception as e:
            # gravar estava fora do try: um PermissionError do Windows -- destino aberto por outro
            # processo -- matava a campanha inteira e perdia a chamada que acabara de custar minutos.
            erros += 1
            print(f"  [{i}/{len(todas)}] FALHA AO GRAVAR {p.name}: {type(e).__name__}: {str(e)[:90]}",
                  flush=True)
            continue
        feitas += 1
        print(f"  [{i}/{len(todas)}] {c['modelo']:11s} {c['ancora']}/{c['ficha']} {c['ensaio']}-r{c['replica']}"
              f"  {r['prompt_tokens']:6d}+{r['tokens']:5d} tok  {r['dt']:6.1f}s  fim={r['finish']}", flush=True)
    if residente and not seco:
        descarrega(h3.MODELS[residente]["ollama"])
    dt = time.time() - t0
    print(f"\nfeitas {feitas} · já prontas {puladas} · refeitas por integridade {refeitas} · erros {erros}")
    print(f"tempo {dt/60:.1f} min")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="harness da campanha do Estudo 12")
    ap.add_argument("--modelo", choices=ELENCO)
    ap.add_argument("--ancora", choices=("a1", "a2", "a3"))
    ap.add_argument("--ficha", choices=("v1", "v2"))
    ap.add_argument("--seco", action="store_true", help="não chama modelo nenhum; só mostra o plano")
    a = ap.parse_args()
    roda(a.modelo, a.ancora, a.ficha, a.seco)

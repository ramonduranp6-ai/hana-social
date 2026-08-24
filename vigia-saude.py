# -*- coding: utf-8 -*-
"""
vigia-saude.py — robo de saude do fluxo (pedido do Ramon, 23/08/2026:
"um robo que te avisasse das quebras e erros possiveis do nosso fluxo,
assim voce pode arruma-los sem precisar eu ver isso no final do dia").

Custo: ZERO token. Roda agendado (3x/dia, invisivel via pythonw) e:
  1. DETECTA quebras: tarefa agendada com erro, commit sem push, arquivo-lixo
     'nul' (e, no hub, tambem stderr dos vigias e chaves-api sumido).
  2. CONSERTA sozinho o que e deterministico e seguro (lista fechada):
     apagar 'nul' · push de commit que ja esta a frente (fast-forward puro) ·
     reiniciar 1x/dia tarefa agendada quebrada.
  3. REGISTRA o resto em <pasta>/SAUDE-DO-PROJETO.md — o conferir-ambiente
     avisa o Claude na PROXIMA conversa aberta NAQUELA pasta, que conserta.

UM VIGIA POR PROJETO (ordem do Ramon, 23/08: "cada projeto precisa do robo
vigia, assim voce nao fica arrumando projeto dos outros"): rodar com
  pythonw vigia-saude.py --pasta "C:\\...\\Canecas POD" --prefixo "CanecasPOD-"
Sem argumento, cuida do HUB (Crescimento IA) + itens da maquina inteira.
A copia que roda em cada projeto mora NA pasta do projeto (regra 23); a fonte
oficial e esta aqui no hub.
"""
import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

CASA = Path.home()
HUB = CASA / "OneDrive" / "Desktop" / "Crescimento IA"
RESULTADOS_OK = {0, 267009, 267011, 267014}  # ok / rodando / nunca rodou / encerrando
NOWIN = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0


def rodar(cmd, timeout=90, cwd=None):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           cwd=cwd, creationflags=NOWIN)
        return r.returncode, (r.stdout or ""), (r.stderr or "")
    except Exception as e:
        return -1, "", str(e)


def checar_tarefas(prefixos, erros, consertos, estado):
    if not prefixos:
        return
    ps = (
        "Get-ScheduledTask | Where-Object { $_.TaskPath -notlike '\\Microsoft*' } | "
        "ForEach-Object { $i = $_ | Get-ScheduledTaskInfo; "
        "'{0}|{1}|{2}' -f $_.TaskName, $i.LastTaskResult, $_.State }"
    )
    cod, saida, _ = rodar(["powershell", "-NoProfile", "-Command", ps], timeout=120)
    if cod != 0:
        return
    hoje = time.strftime("%Y-%m-%d")
    for linha in saida.splitlines():
        partes = linha.strip().split("|")
        if len(partes) != 3:
            continue
        nome, resultado, estado_t = partes
        if not any(nome.startswith(p) for p in prefixos):
            continue
        if estado_t == "Disabled":
            continue
        try:
            res = int(resultado)
        except ValueError:
            continue
        if res in RESULTADOS_OK:
            continue
        chave = f"restart:{nome}:{hoje}"
        if not estado.get(chave):
            rodar(["powershell", "-NoProfile", "-Command",
                   f"Start-ScheduledTask -TaskName '{nome}'"], timeout=60)
            estado[chave] = True
            consertos.append(f"tarefa '{nome}' com erro {res} — reiniciada (1ª tentativa do dia)")
        else:
            erros.append(f"tarefa agendada '{nome}' QUEBRADA (código {res}) — reiniciar não resolveu, precisa de diagnóstico")


def checar_git(pasta, erros, consertos):
    if not (pasta / ".git").exists():
        return
    nul = pasta / "nul"
    if nul.exists():
        try:
            nul.unlink()
            consertos.append("arquivo-lixo 'nul' apagado")
        except Exception:
            pass
    cod, sujo, _ = rodar(["git", "status", "--porcelain"], cwd=str(pasta))
    if cod != 0:
        return
    cod, ahead, _ = rodar(["git", "rev-list", "--count", "@{u}..HEAD"], cwd=str(pasta))
    if cod == 0 and ahead.strip().isdigit() and int(ahead.strip()) > 0:
        if not sujo.strip():
            cod2, _, err2 = rodar(["git", "push"], cwd=str(pasta), timeout=120)
            if cod2 == 0:
                consertos.append(f"{ahead.strip()} commit(s) sem push — enviados agora")
            else:
                erros.append(f"push falhou: {err2[-150:]}")
        else:
            erros.append(f"{ahead.strip()} commit(s) sem push + alterações não commitadas paradas na árvore")


def checar_maquina(erros):
    """So o vigia do HUB olha o que e da maquina inteira."""
    for arq in (CASA / ".claude").glob("vigia-*.err"):
        try:
            txt = arq.read_text(encoding="utf-8", errors="replace").strip()
        except Exception:
            continue
        if txt:
            erros.append(f"vigia de abertura com stderr em {arq.name}: {txt[-200:]}")
    lugares = [
        CASA / "OneDrive" / "Desktop" / "IA-Hub" / "chaves-api.txt",
        CASA / "OneDrive" / "Desktop" / "Crescimento IA" / "Documents" / "IA-Hub" / "chaves-api.txt",
        CASA / "OneDrive" / "IA-Hub" / "chaves-api.txt",
    ]
    if not any(p.exists() for p in lugares):
        erros.append("chaves-api.txt SUMIU dos 3 lugares conhecidos — IA-Hub morto nesta máquina")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pasta", help="pasta do projeto a vigiar (padrao: o hub + a maquina)")
    ap.add_argument("--prefixo", action="append", default=[],
                    help="prefixo das tarefas agendadas deste projeto (pode repetir)")
    args = ap.parse_args()

    e_hub = not args.pasta
    pasta = Path(args.pasta) if args.pasta else HUB
    if not pasta.exists():
        return
    prefixos = args.prefixo or (["VigiaSaude", "Jarvis"] if e_hub else [])
    saude = pasta / ("06-SISTEMAS/SAUDE-DA-MAQUINA.md" if e_hub else "SAUDE-DO-PROJETO.md")
    estado_arq = CASA / ".claude" / "ferramentas" / f"vigia-saude-{pasta.name.replace(' ', '_')}.json"

    erros, consertos = [], []
    try:
        estado = json.loads(estado_arq.read_text(encoding="utf-8"))
    except Exception:
        estado = {}

    checar_tarefas(prefixos, erros, consertos, estado)
    checar_git(pasta, erros, consertos)
    if e_hub:
        checar_maquina(erros)

    corte = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3 * 86400))
    estado = {k: v for k, v in estado.items() if k.split(":")[-1] >= corte}
    estado_arq.parent.mkdir(parents=True, exist_ok=True)
    estado_arq.write_text(json.dumps(estado), encoding="utf-8")

    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    linhas = [
        f"# SAÚDE — {pasta.name} (escrito pelo robô vigia-saude, zero token)",
        "",
        f"> Última varredura: {agora}. Enquanto houver erro aberto aqui, o Claude é",
        "> avisado ao abrir conversa NESTA pasta e conserta sem esperar o Ramón",
        "> (regra 37). Ao consertar, remover a linha (a varredura reescreve tudo).",
        "",
    ]
    if erros:
        linhas.append("## ⛔ ERROS ABERTOS — consertar na conversa desta pasta")
        linhas += [f"- [ ] {e}" for e in erros]
        linhas.append("")
    else:
        linhas.append("## ✅ Nenhum erro aberto")
        linhas.append("")
    if consertos:
        linhas.append("## 🔧 Consertos automáticos desta varredura")
        linhas += [f"- {c}" for c in consertos]
        linhas.append("")
    saude.write_text("\n".join(linhas), encoding="utf-8")
    print(f"[{pasta.name}] {len(erros)} erro(s), {len(consertos)} conserto(s)")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        try:
            (HUB / "06-SISTEMAS" / "SAUDE-DA-MAQUINA.md").write_text(
                f"# SAÚDE DA MÁQUINA\n\n## ⛔ O PRÓPRIO VIGIA QUEBROU\n- [ ] {e}\n", encoding="utf-8")
        except Exception:
            pass
        sys.exit(0)

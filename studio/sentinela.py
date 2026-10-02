"""
Vigia local — rodado pelo Agendador de Tarefas do Windows (seg/qua/sex 18:40).

Cobre o caso que o GitHub não cobre sozinho: o cron agendado simplesmente não
rodar. Se o post do dia está vencido há mais de 30 min, dispara o workflow na
mão (gh workflow run). Custo: zero — não usa nenhuma IA.
"""

import datetime as dt
import json
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sh(*args):
    return subprocess.run(args, cwd=REPO, capture_output=True, text=True)


def main():
    print(f"--- sentinela local {dt.datetime.now().isoformat(timespec='seconds')} ---")

    # CONSERTO 01/10/2026 — o Sentinela ficou 4 dias quebrado (código 1) num ciclo
    # que se alimentava sozinho: o robô `vigia-saude.py` reescreve
    # SAUDE-DO-PROJETO.md 3x/dia, o arquivo fica sujo na árvore, o `git pull`
    # recusa ("local changes would be overwritten"), e o erro resultante ia parar
    # DENTRO do mesmo arquivo — que então continuava sujo. O arquivo que
    # reportava a falha era a causa da falha.
    # Estes arquivos são 100% gerados por robô: não há trabalho humano para
    # perder, então a cópia local se descarta antes do pull. Nunca ampliar esta
    # lista para arquivo escrito por pessoa.
    GERADOS = ("SAUDE-DO-PROJETO.md", "ESTADO-ATUAL.md")
    sujos = sh("git", "status", "--porcelain", "--", *GERADOS).stdout.strip()
    if sujos:
        print("[limpeza] descartando cópia local de arquivo gerado por robô:")
        for linha in sujos.splitlines():
            print("   ", linha.strip())
        sh("git", "checkout", "--", *GERADOS)

    pull = sh("git", "pull", "--ff-only")
    if pull.returncode:
        raise RuntimeError("git pull falhou: " + (pull.stderr.strip() or pull.stdout.strip()))

    qdir = os.path.join(REPO, "content", "queue")
    agora = dt.datetime.now(dt.timezone.utc)
    atrasados = []
    esperando = []   # vencidos mas ainda 'pending' -> dependem do OK do Ramon
    if os.path.isdir(qdir):
        for pasta in sorted(os.listdir(qdir)):
            pj = os.path.join(qdir, pasta, "post.json")
            if not os.path.isfile(pj):
                continue
            with open(pj, encoding="utf-8") as f:
                p = json.load(f)
            # CONSERTO 01/10/2026: antes isto aceitava "pending" tambem, e o
            # Sentinela ficava disparando o workflow a cada rodada por um post
            # que NUNCA ia publicar -- o publicador exige status "approved"
            # (publisher/run.py). O Reel de 28/08 ficou 34 dias vencido e
            # "pending", e cada rodada queimava uma execucao do GitHub Actions
            # a toa. Vencido + pending NAO e cron quebrado: e post esperando o
            # Ramon, e isso se avisa, nao se re-dispara.
            if p.get("status") == "pending":
                agendado_p = p.get("scheduled_for")
                if agendado_p:
                    tp = dt.datetime.fromisoformat(agendado_p.replace("Z", "+00:00"))
                    if (agora - tp).total_seconds() > 5 * 60:
                        esperando.append((pasta, int((agora - tp).total_seconds() // 86400)))
                continue
            if p.get("status") != "approved":
                continue
            agendado = p.get("scheduled_for")
            if not agendado:
                continue
            t = dt.datetime.fromisoformat(agendado.replace("Z", "+00:00"))
            # tolerancia curta: o cron do GitHub e estrangulado (roda a cada ~4h
            # em vez dos 30 min pedidos), entao quem garante a hora e este vigia.
            if (agora - t).total_seconds() > 5 * 60:
                atrasados.append(pasta)

    if atrasados:
        print("atrasados:", ", ".join(atrasados), "-> disparando workflow")
        r = sh("gh", "workflow", "run", "publish.yml", "-R", "ramonduranp6-ai/hana-social")
        print(r.stdout.strip() or r.stderr.strip())
        if r.returncode:
            raise RuntimeError("não consegui disparar o workflow")
    else:
        print("tudo em dia")

    for pasta, dias in esperando:
        print(f"[esperando o Ramon] {pasta}: vencido ha {dias} dia(s), status 'pending' "
              f"-- nao publica sem aprovacao, e nao adianta re-disparar o workflow.")


if __name__ == "__main__":
    main()

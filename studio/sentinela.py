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
    pull = sh("git", "pull", "--ff-only")
    if pull.returncode:
        raise RuntimeError("git pull falhou: " + (pull.stderr.strip() or pull.stdout.strip()))

    qdir = os.path.join(REPO, "content", "queue")
    agora = dt.datetime.now(dt.timezone.utc)
    atrasados = []
    if os.path.isdir(qdir):
        for pasta in sorted(os.listdir(qdir)):
            pj = os.path.join(qdir, pasta, "post.json")
            if not os.path.isfile(pj):
                continue
            with open(pj, encoding="utf-8") as f:
                p = json.load(f)
            if p.get("status") not in ("pending", "approved"):
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


if __name__ == "__main__":
    main()

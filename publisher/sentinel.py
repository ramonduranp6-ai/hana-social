"""
Sentinela do workflow: roda como último passo no GitHub Actions.

Sai com erro (exit 1) se algum post ficou para trás — publicação que falhou
ou post vencido há mais de 45 min sem publicar. O job fica vermelho e o
GitHub avisa o dono por e-mail. Custo: zero.
"""

import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import postqueue as q

TOLERANCIA_MIN = 45


def main():
    agora = dt.datetime.now(dt.timezone.utc)
    problemas = []
    for p in q.load_all():
        status = p.get("status")
        if status == "failed":
            problemas.append(f"{p['_id']}: FALHOU ({p.get('error', 'sem detalhe')})")
        elif status in ("pending", "approved"):
            t = dt.datetime.fromisoformat(p["scheduled_for"].replace("Z", "+00:00"))
            atraso_min = (agora - t).total_seconds() / 60
            if atraso_min > TOLERANCIA_MIN:
                problemas.append(f"{p['_id']}: vencido ha {int(atraso_min)} min sem publicar")
    if problemas:
        print("[SENTINELA] PROBLEMAS ENCONTRADOS:")
        for x in problemas:
            print(" -", x)
        sys.exit(1)
    print("[SENTINELA] fila saudavel")


if __name__ == "__main__":
    main()

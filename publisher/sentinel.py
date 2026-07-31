"""
Sentinela do workflow: roda como último passo no GitHub Actions.

Sai com erro (exit 1) se algum post ficou para trás — publicação que falhou
ou post vencido há mais de 45 min sem publicar. O job fica vermelho e o
GitHub avisa o dono por e-mail. Custo: zero.

--token: checagem separada, de vencimento do token do Instagram (furo 2 do
conserto de 31/07/2026). Por que aqui e não só na máquina do Ramón: o robô
local (`studio/renovar_token.py`, dentro da tarefa "Hana Sentinela") só roda
se o notebook estiver ligado — e é justo quando ele fica semanas desligado
que o aviso importa. Este script roda no GitHub a cada 30 min, publish.yml,
sem depender de nada na máquina dele. Precisa rodar como passo SEPARADO,
ANTES do commit de "Salvar estado da fila" — senão o marcador de "já avisei
hoje" nunca fica salvo (o runner do GitHub é descartado ao fim do job).
"""

import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import postqueue as q

TOLERANCIA_MIN = 45
DIAS_AVISO_TOKEN = 7

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARCADOR_TOKEN = os.path.join(ROOT, "content", ".aviso_token_vence")


def checar_fila():
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


def _hoje():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")


def _ja_avisou_hoje():
    return os.path.isfile(MARCADOR_TOKEN) and open(MARCADOR_TOKEN, encoding="utf-8").read().strip() == _hoje()


def _marcar_avisado():
    with open(MARCADOR_TOKEN, "w", encoding="utf-8") as f:
        f.write(_hoje())


def checar_validade_token():
    """
    Avisa no Telegram se o token do Instagram vence em <= 7 dias.

    A data de vencimento vem da variável de repositório IG_TOKEN_EXPIRA_EM,
    que `studio/renovar_token.py` atualiza toda vez que renova o token na
    máquina do Ramón. Se o notebook ficar desligado, a variável trava na
    última data conhecida — e é exatamente essa data parada que dispara o
    aviso, sem precisar de nada rodando na máquina dele.

    Nunca derruba o job: qualquer falha (variável ainda não existe, Telegram
    fora do ar) só imprime aviso no log e segue.
    """
    expira_str = os.environ.get("IG_TOKEN_EXPIRA_EM")
    if not expira_str:
        print("[SENTINELA][token] IG_TOKEN_EXPIRA_EM ainda não existe "
              "(token nunca foi renovado com o script novo) — nada a checar.")
        return
    try:
        expira = dt.date.fromisoformat(expira_str)
    except ValueError:
        print(f"[SENTINELA][token][aviso] IG_TOKEN_EXPIRA_EM com valor "
              f"inesperado: {expira_str!r}")
        return

    dias = (expira - dt.datetime.now(dt.timezone.utc).date()).days
    if dias > DIAS_AVISO_TOKEN:
        print(f"[SENTINELA][token] valido por mais {dias} dia(s) — nada a fazer.")
        return
    if _ja_avisou_hoje():
        print("[SENTINELA][token] ja avisei hoje — nao repete.")
        return

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not (token and chat_id):
        print(f"[SENTINELA][token] venceria em {dias} dia(s) mas faltam "
              f"TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID para avisar.")
        return

    texto = (
        "⚠️ Token do Instagram vence em %d dia(s) (%s).\n"
        "Ligue o notebook: o robô renova sozinho dentro da tarefa "
        "\"Hana Sentinela\".\n"
        "Se já estiver ligado e não renovou, rode na mão: "
        "python studio/renovar_token.py --forcar"
    ) % (dias, expira.isoformat())
    try:
        from mandar_recado import mandar
        mandar(token, chat_id, texto)
        _marcar_avisado()
        print(f"[SENTINELA][token] aviso de vencimento mandado ({dias} dia(s)).")
    except Exception as exc:  # noqa: BLE001 — aviso nunca pode derrubar o job
        print(f"[SENTINELA][token][FALHA] nao consegui avisar: {str(exc)[:160]}")


def main():
    if "--token" in sys.argv:
        checar_validade_token()
        return
    checar_fila()


if __name__ == "__main__":
    main()

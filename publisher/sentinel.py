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

# Achado testando o item 1/4 da auditoria de 01/08/2026: este arquivo era o
# único do publisher/ sem a proteção de console UTF-8 (regra da casa, ver
# telegram_approve.py e run.py) — os prints com emoji (🙈, ⚠️) quebravam com
# UnicodeEncodeError se algum dia rodasse fora do runner Ubuntu do GitHub
# Actions (que já é UTF-8 por padrão). `reconfigure`, nunca `io.TextIOWrapper`.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import postqueue as q

TOLERANCIA_MIN = 45
DIAS_AVISO_TOKEN = 7

# BURACO (c) do conserto de 31/07/2026: com menos de 2 posts futuros na fila,
# o projeto está a um post de ficar mudo (a fila do Ramón acabava em 10/08 e
# em 12/08 não sairia post nenhum — e os vigias diziam "tudo em dia" porque
# fila vazia não é "problema", é só "nada pra fazer"). Isso muda aqui.
MIN_POSTS_FUTUROS = 2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARCADOR_TOKEN = os.path.join(ROOT, "content", ".aviso_token_vence")
MARCADOR_TOKEN_CEGO = os.path.join(ROOT, "content", ".aviso_token_cego")


def checar_fila():
    agora = dt.datetime.now(dt.timezone.utc)
    problemas = []
    avisos = []
    futuros = 0
    for p in q.load_all():
        status = p.get("status")
        if status == "failed":
            problemas.append(f"{p['_id']}: FALHOU ({p.get('error', 'sem detalhe')})")
        elif status in ("pending", "approved"):
            # Post sem data marcada nao e' atraso: e' peca pronta esperando o
            # Ramon decidir QUANDO vai ao ar (ex.: o Reel da chegada da Eloen,
            # 14/08/2026). NAO e' falha tecnica — vira aviso, nao problema, senao
            # o GitHub manda e-mail de "workflow falhou" a cada 30 min por dias
            # seguidos por causa de uma decisao de familia sem prazo (achado
            # 19/08/2026: e-mail de falha reincidente, ele perguntou "deu problema
            # em algo?" e o motivo era so isso).
            if not p.get("scheduled_for"):
                avisos.append(f"{p['_id']}: pronto, mas SEM DATA — esperando ele marcar")
                continue
            t = dt.datetime.fromisoformat(p["scheduled_for"].replace("Z", "+00:00"))
            atraso_min = (agora - t).total_seconds() / 60
            if atraso_min > TOLERANCIA_MIN:
                problemas.append(f"{p['_id']}: vencido ha {int(atraso_min)} min sem publicar")
            else:
                futuros += 1
    # BURACO (c): fila com menos de 2 posts futuros é ALARME, nao "tudo em
    # dia" — sem isso o robo so percebe o buraco no dia em que ja faltou post.
    if futuros < MIN_POSTS_FUTUROS:
        problemas.append(
            f"fila com so {futuros} post(s) futuro(s) (minimo saudavel: "
            f"{MIN_POSTS_FUTUROS}) — sem reforco a fila acaba e nenhum aviso "
            f"normal pega isso antes de faltar post"
        )
    if avisos:
        print("[SENTINELA] AVISOS (nao derrubam o job, nao mandam e-mail):")
        for x in avisos:
            print(" -", x)
    if problemas:
        print("[SENTINELA] PROBLEMAS ENCONTRADOS:")
        for x in problemas:
            print(" -", x)
        sys.exit(1)
    print(f"[SENTINELA] fila saudavel ({futuros} post(s) futuro(s))")


def _hoje():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")


def _ja_avisou_hoje():
    return os.path.isfile(MARCADOR_TOKEN) and open(MARCADOR_TOKEN, encoding="utf-8").read().strip() == _hoje()


def _marcar_avisado():
    with open(MARCADOR_TOKEN, "w", encoding="utf-8") as f:
        f.write(_hoje())


def _ja_avisou_cego_hoje():
    return (os.path.isfile(MARCADOR_TOKEN_CEGO)
            and open(MARCADOR_TOKEN_CEGO, encoding="utf-8").read().strip() == _hoje())


def _marcar_avisado_cego():
    with open(MARCADOR_TOKEN_CEGO, "w", encoding="utf-8") as f:
        f.write(_hoje())


def _avisar_sensor_cego():
    """
    BURACO (b) do conserto de 31/07/2026: antes, "a variável não existe"
    terminava em "nada a checar" e o robô saía calado — o pior tipo de
    silêncio, porque parece que está tudo bem. Um token recém-criado passa
    ATÉ ~40 DIAS sem essa variável (só era escrita depois de uma renovação de
    verdade, que só acontece com <=20 dias de sobra).

    Conserto tem duas pernas: `studio/renovar_token.py` agora sincroniza a
    variável em TODA execução (não só quando renova de verdade) — então
    basta o notebook ligar uma vez para resolver. Só que enquanto isso não
    acontecer nenhuma vez, este robô (que roda no GitHub, sem depender do
    notebook) tem que GRITAR que está cego, nunca fingir que checou. Não
    tentamos adivinhar a validade chamando a API do Instagram por aqui: o
    único endpoint provado neste projeto (`graph.instagram.com/
    refresh_access_token`) TROCA o token na hora — chamar isso só para
    "espiar" arriscaria invalidar o token que está publicando de verdade
    (regra 1: nada pode derrubar a publicação). Melhor gritar que não sabe.
    """
    if _ja_avisou_cego_hoje():
        print("[SENTINELA][token] cego (sem IG_TOKEN_EXPIRA_EM) — ja avisei hoje, nao repete.")
        return
    texto = (
        "🙈 Não sei quando o token do Instagram vence — o sensor está cego.\n"
        "A variável IG_TOKEN_EXPIRA_EM ainda não existe no repositório "
        "(normal logo depois de um token novo).\n"
        "Ligue o notebook: a tarefa \"Hana Sentinela\" sincroniza sozinha na "
        "próxima vez que rodar.\n"
        "Se já estiver ligado e não sincronizou, rode na mão: "
        "python studio/renovar_token.py"
    )
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not (token and chat_id):
        print(f"[SENTINELA][token][CEGO] sem TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID "
              f"para avisar. Mensagem que mandaria:\n{texto}")
        return
    try:
        from mandar_recado import mandar
        mandar(token, chat_id, texto)
        _marcar_avisado_cego()
        print("[SENTINELA][token][CEGO] aviso de sensor cego mandado.")
    except Exception as exc:  # noqa: BLE001 — aviso nunca pode derrubar o job
        print(f"[SENTINELA][token][FALHA] nao consegui avisar que estou cego: {str(exc)[:160]}")


def checar_validade_token():
    """
    Avisa no Telegram se o token do Instagram vence em <= 7 dias.

    A data de vencimento vem da variável de repositório IG_TOKEN_EXPIRA_EM,
    que `studio/renovar_token.py` atualiza toda vez que roda na máquina do
    Ramón (renovando ou não — ver esse arquivo). Se o notebook ficar
    desligado, a variável trava na última data conhecida — e é exatamente
    essa data parada que dispara o aviso, sem precisar de nada rodando na
    máquina dele.

    Nunca derruba o job: qualquer falha (Telegram fora do ar) só imprime
    aviso no log e segue. Variável ausente NÃO é "nada a checar" — é alarme
    de sensor cego (`_avisar_sensor_cego`), nunca silêncio.
    """
    expira_str = os.environ.get("IG_TOKEN_EXPIRA_EM")
    if not expira_str:
        _avisar_sensor_cego()
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

"""
Canal Claude -> Telegram do Ramón.

Por que existe: o bot `@Hanasocial_aproval_bot` só sabia falar sozinho (post
pra aprovar, pauta de segunda). Não havia jeito de EU mandar um recado pra ele
por lá — o token do bot mora nos secrets do GitHub, não na máquina dele.
Agora o workflow aceita a entrada `recado` e este script entrega o texto.

Uso (pela conversa):
    gh workflow run publish.yml -R ramonduranp6-ai/hana-social -f recado="texto"

Uso (local, se algum dia o token estiver no ambiente):
    TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=... python publisher/mandar_recado.py "texto"
"""

import os
import sys

import requests

API = "https://api.telegram.org/bot{token}/sendMessage"
LIMITE = 4096  # limite duro do Telegram por mensagem


def _pedacos(texto, tamanho=LIMITE):
    """Quebra o recado em mensagens, sem cortar linha no meio."""
    partes, atual = [], ""
    for linha in texto.split("\n"):
        if len(atual) + len(linha) + 1 > tamanho:
            partes.append(atual.rstrip("\n"))
            atual = ""
        atual += linha + "\n"
    if atual.strip():
        partes.append(atual.rstrip("\n"))
    return partes or [texto[:tamanho]]


def mandar(token, chat_id, texto):
    for parte in _pedacos(texto):
        r = requests.post(API.format(token=token), timeout=60,
                          data={"chat_id": chat_id, "text": parte})
        if not r.ok or not r.json().get("ok"):
            raise RuntimeError("Telegram recusou: %s" % r.text[:300])
    return True


def main():
    texto = " ".join(sys.argv[1:]).strip() or os.environ.get("RECADO", "").strip()
    if not texto:
        print("[aviso] sem recado pra mandar — saindo calado")
        return 0

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("[erro] faltam TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID")
        return 1

    mandar(token, chat_id, texto)
    print("[ok] recado entregue (%d caractere(s))" % len(texto))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

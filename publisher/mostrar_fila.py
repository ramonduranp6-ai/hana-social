"""
Mostrar a FILA INTEIRA no Telegram — o pedido dele de 01/08/2026:
"Sobre a postagem, me traga elas aqui, com vídeo/foto e descrição.
 Quero assistir pelo celular."

Diferença para `telegram_approve.notify_pending()`, que já existia:
aquele só manda o que está `pending` e só manda UMA VEZ (grava `notified`).
Os 4 posts da fila de agosto já estão `approved` e já foram notificados —
pelo caminho antigo ele nunca mais veria nenhum deles. Este script é o
"me mostra de novo": manda TODOS os posts da fila, em ordem de data, com a
mídia de verdade (foto/vídeo), a legenda inteira, a data agendada e a trilha.

Não altera status de nada e não grava `notified` — é só leitura. Por isso
pode ser rodado quantas vezes ele pedir.

Uso (pela conversa):
    gh workflow run publish.yml -R ramonduranp6-ai/hana-social -f mostrar_fila=true

O token do bot mora nos secrets do GitHub, não na máquina dele — mesmo motivo
de `mandar_recado.py`.
"""

import os
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import postqueue  # noqa: E402

# O console do Windows quebra com emoji (mesma pegadinha de telegram_approve.py):
# `reconfigure` altera o objeto existente, não cria wrapper novo.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

API = "https://api.telegram.org/bot{token}/{method}"

TIPO_LEGIVEL = {"reel": "🎬 Reel (vídeo)", "image": "🖼 Foto"}
STATUS_LEGIVEL = {
    "approved": "✅ já aprovado por você",
    "pending": "⏳ esperando seu OK",
    "rejected": "❌ recusado por você",
}


def _call(token, method, **params):
    r = requests.post(API.format(token=token, method=method), data=params, timeout=120)
    return r.json()


def _texto(post, indice, total):
    trilha = post.get("audio_titulo")
    linhas = [
        f"📋 {indice} de {total} da fila",
        "",
        post.get("caption", "(sem legenda)"),
        "",
        f"{TIPO_LEGIVEL.get(post.get('type'), post.get('type'))}"
        f" · {STATUS_LEGIVEL.get(post.get('status'), post.get('status'))}",
        f"🕒 Vai ao ar: {post.get('scheduled_for')}",
    ]
    if trilha:
        linhas.append(f"🎵 Trilha: {trilha}")
    linhas.append(f"🆔 {post['_id']}")
    return "\n".join(linhas)


def mostrar(token, chat_id, media_base_url):
    """Manda cada post da fila com a mídia. Devolve quantos foram entregues."""
    posts = sorted(postqueue.load_all(), key=lambda p: p.get("scheduled_for", ""))
    if not posts:
        _call(token, "sendMessage", chat_id=chat_id,
              text="📋 A fila está vazia — não tem post agendado no momento.")
        return 0

    _call(token, "sendMessage", chat_id=chat_id,
          text=f"📋 A fila da Hana tem {len(posts)} post(s). "
               f"Mandando um por um com a mídia e a legenda.\n"
               f"(Isto é só para você ver — não muda o status de nada.)")

    entregues = 0
    for i, post in enumerate(posts, start=1):
        # Um post torto não pode derrubar a entrega dos outros (achado da
        # auditoria de 01/08/2026): `media_url` faz post['media_file'] com
        # colchete direto, então post.json escrito à mão sem esse campo
        # estourava o laço — ele recebia o "mandando 4 posts" e depois nada.
        try:
            texto = _texto(post, i, len(posts))
            url = postqueue.media_url(post, media_base_url)
        except Exception as e:
            print(f"[mostrar_fila][erro] post torto ({post.get('_id')}): {e}")
            _call(token, "sendMessage", chat_id=chat_id,
                  text=f"⚠️ O post {post.get('_id')} está com o cadastro "
                       f"incompleto e não consegui te mostrar a mídia dele. "
                       f"Os outros seguem abaixo.")
            continue
        if post.get("type") == "reel":
            resp = _call(token, "sendVideo", chat_id=chat_id, video=url, caption=texto)
        else:
            resp = _call(token, "sendPhoto", chat_id=chat_id, photo=url, caption=texto)
        if resp.get("ok"):
            entregues += 1
            print(f"[mostrar_fila] entregue: {post['_id']}")
        else:
            # Melhor avisar torto do que não avisar (mesma escolha do
            # notify_pending): cai para texto com o link da mídia.
            print(f"[mostrar_fila][aviso] midia nao foi ({post['_id']}): "
                  f"{resp.get('description')} — mandando so o texto")
            _call(token, "sendMessage", chat_id=chat_id, text=f"{texto}\n\n🖼 {url}")
    return entregues


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    base = os.environ.get("MEDIA_BASE_URL")
    if not token or not chat_id:
        print("[erro] faltam TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID")
        return 1
    if not base:
        print("[erro] falta MEDIA_BASE_URL — sem ela o Telegram nao acha a midia")
        return 1
    n = mostrar(token, chat_id, base)
    print(f"[mostrar_fila] {n} post(s) entregue(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
Aprovação por Telegram (o "só aceite" do Ramón).

Fluxo:
  1. notify_pending(): manda cada post 'pending' pro Telegram com botões ✅ Aprovar / ❌ Recusar.
  2. sync_approvals(): lê os cliques (getUpdates) e atualiza o status do post.

Como é um sistema por cron (sem servidor sempre ligado), a aprovação é
eventualmente consistente: você toca o botão, e a próxima rodada do cron
registra a decisão. O atraso é de minutos, não importa pro agendamento.
"""

import json
import os
import requests

API = "https://api.telegram.org/bot{token}/{method}"
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".telegram_offset")


def _call(token, method, **params):
    r = requests.post(API.format(token=token, method=method), data=params, timeout=60)
    return r.json()


def notify_pending(token, chat_id, posts, media_base_url):
    """
    Envia pro Telegram os posts que ainda precisam de aprovação.

    Manda a MÍDIA (foto ou vídeo), não só o texto: o Ramón aprova olhando a
    imagem no celular. Se o envio da mídia falhar (URL fora do ar, arquivo
    grande demais), cai para mensagem de texto — melhor avisar torto do que
    não avisar.
    """
    from postqueue import media_url

    for post in posts:
        if post.get("status") != "pending" or post.get("notified"):
            continue
        caption = (
            f"🐾 Novo post da Hana pra aprovar\n\n"
            f"{post['caption']}\n\n"
            f"🕒 Agendado: {post['scheduled_for']}\n"
            f"🆔 {post['_id']}"
        )
        keyboard = json.dumps({
            "inline_keyboard": [[
                {"text": "✅ Aprovar", "callback_data": f"approve:{post['_id']}"},
                {"text": "❌ Recusar", "callback_data": f"reject:{post['_id']}"},
            ]]
        })
        url = media_url(post, media_base_url)
        if post["type"] == "reel":
            resp = _call(token, "sendVideo", chat_id=chat_id, video=url,
                         caption=caption, reply_markup=keyboard)
        else:
            resp = _call(token, "sendPhoto", chat_id=chat_id, photo=url,
                         caption=caption, reply_markup=keyboard)
        if not resp.get("ok"):
            print(f"[aviso] midia nao foi pro Telegram ({post['_id']}): "
                  f"{resp.get('description')} — mandando so o texto")
            _call(token, "sendMessage", chat_id=chat_id,
                  text=f"{caption}\n\n🖼 {url}", reply_markup=keyboard)
        # sem prefixo "_": postqueue.save() descarta chaves com "_", e sem
        # persistir isso o cron reenviava o mesmo post a cada 30 minutos.
        post["notified"] = True


def _read_offset():
    if os.path.isfile(STATE_FILE):
        return int(open(STATE_FILE).read().strip() or 0)
    return 0


def _write_offset(offset):
    with open(STATE_FILE, "w") as f:
        f.write(str(offset))


RECADOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "content", "recados.md")


def _guardar_recado(texto, quando, token=None, chat_id=None):
    """
    Guarda o que o Ramón escreve no Telegram.

    O bot não conversa — ele manda e recebe clique de botão. Antes desta função,
    mensagem de texto dele caía no vazio: o getUpdates lia, o offset avançava e
    o recado sumia sem ninguém ver. Ele reclamou disso em 31/07/2026
    ("Te mandei msg pelo Telegram e vc não responde?"), e mandou criar o robô.
    Agora o recado vira linha em content/recados.md, que o Claude lê ao abrir a
    conversa, e o bot confirma na hora para ele saber que chegou.
    """
    os.makedirs(os.path.dirname(RECADOS), exist_ok=True)
    novo = not os.path.isfile(RECADOS)
    with open(RECADOS, "a", encoding="utf-8") as f:
        if novo:
            f.write("# Recados do Ramón pelo Telegram\n\n"
                    "Escrito pelo robô, lido pelo Claude ao abrir a conversa.\n"
                    "**Não editar à mão** — para marcar como resolvido, apague a linha.\n\n")
        f.write("- [ ] **%s** — %s\n" % (quando, texto.replace("\n", " ").strip()))
    if token and chat_id:
        _call(token, "sendMessage", chat_id=chat_id,
              text="📌 Recado anotado. O Claude lê isso na próxima conversa "
                   "— aqui eu só entendo os botões.")


def sync_approvals(token, posts_by_id, chat_id=None):
    """
    Lê os cliques de botão e devolve um dict {post_id: 'approved'|'rejected'}.
    Atualiza os posts recebidos em posts_by_id in-place.
    De quebra, guarda em content/recados.md o que o Ramón escrever por lá.
    """
    from datetime import datetime, timezone

    decisions = {}
    offset = _read_offset()
    resp = _call(token, "getUpdates", offset=offset + 1, timeout=0)
    for upd in resp.get("result", []):
        offset = max(offset, upd["update_id"])

        msg = upd.get("message") or upd.get("edited_message")
        if msg and msg.get("text") and not msg["text"].startswith("/"):
            quando = datetime.fromtimestamp(
                msg.get("date", 0), timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
            _guardar_recado(msg["text"], quando, token, chat_id)

        cq = upd.get("callback_query")
        if not cq:
            continue
        action, _, post_id = cq["data"].partition(":")
        status = "approved" if action == "approve" else "rejected"
        decisions[post_id] = status
        if post_id in posts_by_id:
            posts_by_id[post_id]["status"] = status
        _call(token, "answerCallbackQuery",
              callback_query_id=cq["id"],
              text=("Aprovado ✅" if status == "approved" else "Recusado ❌"))
    _write_offset(offset)
    return decisions


def notify(token, chat_id, text):
    _call(token, "sendMessage", chat_id=chat_id, text=text)

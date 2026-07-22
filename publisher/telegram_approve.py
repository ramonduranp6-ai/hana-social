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
    """Envia pro Telegram os posts que ainda precisam de aprovação."""
    from postqueue import media_url

    for post in posts:
        if post.get("status") != "pending" or post.get("_notified"):
            continue
        caption = (
            f"🐾 *Novo post da Hana pra aprovar*\n\n"
            f"{post['caption']}\n\n"
            f"🕒 Agendado: {post['scheduled_for']}\n"
            f"🆔 {post['_id']}"
        )
        keyboard = {
            "inline_keyboard": [[
                {"text": "✅ Aprovar", "callback_data": f"approve:{post['_id']}"},
                {"text": "❌ Recusar", "callback_data": f"reject:{post['_id']}"},
            ]]
        }
        _call(
            token, "sendMessage",
            chat_id=chat_id, text=caption, parse_mode="Markdown",
            reply_markup=json.dumps(keyboard),
        )
        post["_notified"] = True  # marcação em memória; persistida pelo chamador


def _read_offset():
    if os.path.isfile(STATE_FILE):
        return int(open(STATE_FILE).read().strip() or 0)
    return 0


def _write_offset(offset):
    with open(STATE_FILE, "w") as f:
        f.write(str(offset))


def sync_approvals(token, posts_by_id):
    """
    Lê os cliques de botão e devolve um dict {post_id: 'approved'|'rejected'}.
    Atualiza os posts recebidos em posts_by_id in-place.
    """
    decisions = {}
    offset = _read_offset()
    resp = _call(token, "getUpdates", offset=offset + 1, timeout=0)
    for upd in resp.get("result", []):
        offset = max(offset, upd["update_id"])
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

"""
Aprovação por Telegram (o "só aceite" do Ramón).

Fluxo:
  1. notify_pending(): manda cada post 'pending' pro Telegram com botões ✅ Aprovar / ❌ Recusar.
  2. sync_approvals(): lê os cliques (getUpdates), atualiza o status do post e
     repassa toda mensagem de TEXTO pra recepcionista.py (primeiro atendimento
     pelo Gemini — ver aquele arquivo). Continua sendo o único lugar que lê
     getUpdates; a recepcionista só responde ou escala.

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

# O repositório é PÚBLICO (github.com/ramonduranp6-ai/hana-social) — qualquer
# coisa gravada em content/recados.md fica visível pra qualquer pessoa na
# internet. Por isso o recado é cortado bem curto: o mínimo pro Claude
# entender do que se trata, não a mensagem inteira dele.
LIMITE_RECADO = 220


def _guardar_recado(texto, quando, token=None, chat_id=None, resposta_fixa=None):
    """
    Guarda o que o Ramón escreve no Telegram, quando ninguém consegue
    responder na hora (ver recepcionista.py — desde 31/07/2026 este é o
    CAMINHO DE RESERVA, não o principal).

    O bot não conversa sozinho — ele manda e recebe clique de botão. Antes de
    existir a recepcionista, TODA mensagem de texto caía aqui sem resposta
    nenhuma: o Ramón reclamou duas vezes ("Te mandei msg pelo Telegram e vc
    não responde?") até mandar "Vou te mandar msg pelo telegram e voce
    precisa receber por lá tb". Agora só cai aqui o que a recepcionista
    escalou (ação, opinião de estratégia, ou fora do que ela sabe) ou o que
    falhou tecnicamente (sem chave, Gemini fora do ar) — regra 8: publicar
    posts importa mais que responder mensagem, então a recepcionista nunca
    trava, só cai pra este caminho antigo.

    `resposta_fixa` deixa o chamador escolher a frase de confirmação (a
    recepcionista manda uma diferente da genérica, pra ficar claro que ela
    TENTOU responder e não conseguiu, em vez de nunca ter tentado).
    """
    os.makedirs(os.path.dirname(RECADOS), exist_ok=True)
    novo = not os.path.isfile(RECADOS)
    resumo = texto.replace("\n", " ").strip()
    if len(resumo) > LIMITE_RECADO:
        resumo = resumo[:LIMITE_RECADO].rstrip() + "…"
    with open(RECADOS, "a", encoding="utf-8") as f:
        if novo:
            f.write(
                "# Recados do Ramón pelo Telegram\n\n"
                "Escrito pelo robô, lido pelo Claude ao abrir a conversa.\n"
                "**Não editar à mão** — para marcar como resolvido, apague a linha.\n\n"
                "⚠️ **Este repositório é PÚBLICO.** O que for gravado aqui fica "
                "visível para qualquer pessoa na internet — por isso os recados "
                "vêm cortados em poucas palavras. Não colar aqui senha, número "
                "de cartão, endereço nem outro dado sensível.\n\n"
            )
        f.write("- [ ] **%s** — %s\n" % (quando, resumo))
    if token and chat_id:
        _call(token, "sendMessage", chat_id=chat_id,
              text=resposta_fixa or "📌 Recado anotado. O Claude lê isso na próxima "
                                     "conversa — aqui eu só entendo os botões.")


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
            # Import LOCAL, não lá em cima do arquivo: recepcionista.py importa
            # _guardar_recado e _call DESTE módulo, então esse import só pode
            # acontecer depois que telegram_approve já carregou por inteiro —
            # senão vira ciclo. Continua sendo UM SÓ consumidor do getUpdates:
            # a recepcionista não lê o Telegram, só responde ou escala o que
            # já foi lido aqui.
            import recepcionista
            recepcionista.responder_mensagem(msg["text"], quando, token, chat_id)

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

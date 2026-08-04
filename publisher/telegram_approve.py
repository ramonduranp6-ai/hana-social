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

import hashlib
import json
import os
import sys
import requests

# O console do Windows quebra com emoji nos prints de log (mesmo bug batido em
# publisher/diagnostico.py, 31/07/2026): usar `reconfigure`, nunca
# `io.TextIOWrapper` — o wrapper cria objeto novo em cima do mesmo buffer e,
# quando dois módulos fazem isso (aqui e em run.py, que importa este arquivo),
# o segundo derruba o primeiro ("I/O operation on closed file"). `reconfigure`
# só altera o objeto existente, então pode ser chamado várias vezes sem risco.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

API = "https://api.telegram.org/bot{token}/{method}"
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".telegram_offset")


def _call(token, method, **params):
    r = requests.post(API.format(token=token, method=method), data=params, timeout=60)
    return r.json()


def _chat_permitido(chat_id_evento, chat_id_configurado):
    """
    PORTA 1 (auditoria de 31/07/2026): confere se quem mandou a mensagem ou
    clicou no botão é o dono do bot.

    Bot de Telegram é achável pelo nome — sem esta conferência, QUALQUER
    estranho que ache @Hanasocial_aproval_bot conseguia: (a) fazer a
    recepcionista responder e queimar a cota do Gemini, e pior, (b) gravar
    texto em content/recados.md — arquivo de um repositório PÚBLICO que o
    Claude lê no início de toda conversa como se fosse ordem do Ramón. Isso é
    injeção de instrução por um canal que ninguém olhava.

    Pegadinha: a API do Telegram manda `chat.id` como NÚMERO; a variável de
    ambiente TELEGRAM_CHAT_ID chega como STRING. Comparar sempre como texto,
    nunca com `==` cru entre tipos diferentes.

    Sem TELEGRAM_CHAT_ID configurado não dá pra saber quem é o dono — bloqueia
    tudo (falha segura), em vez de aceitar geral.
    """
    if not chat_id_configurado or chat_id_evento is None:
        return False
    return str(chat_id_evento) == str(chat_id_configurado)


def _fingerprint(post):
    """
    "Impressão digital" do que foi mostrado a ele no Telegram: hash da
    legenda + nome/tamanho do arquivo de mídia (PORTA 3, 31/07/2026).

    Sem isso, se a legenda ou a mídia mudassem DEPOIS do envio, o robô não
    tinha como saber — `notified` já estava True (ou o post já virava
    'approved'), e ele acabava aprovando/publicando uma versão que nunca viu.
    Se o arquivo de mídia sumir ou for renomeado, o tamanho vira -1 — conta
    como "mudou" de propósito, nunca como "igual por acidente".
    """
    media_path = os.path.join(post.get("_dir", ""), post.get("media_file", ""))
    try:
        tamanho = os.path.getsize(media_path)
    except OSError:
        tamanho = -1
    base = f"{post.get('caption', '')}|{post.get('media_file', '')}|{tamanho}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


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
        # PORTA 3: revalidar_conteudo() marca isso quando a legenda/mídia
        # mudou depois do último envio — avisa NA PRÓPRIA mensagem, pra ele
        # não confundir com "de novo a mesma coisa" e aprovar no automático.
        aviso_mudanca = ""
        if post.pop("conteudo_mudou", False):
            aviso_mudanca = (
                "⚠️ Isso MUDOU desde a última vez que te mostrei — "
                "confira de novo antes de aprovar.\n\n"
            )
        caption = (
            f"🐾 Novo post da Hana pra aprovar\n\n"
            f"{aviso_mudanca}{post['caption']}\n\n"
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
        # Guarda a impressão digital do que foi mostrado AGORA (legenda +
        # mídia) — é o que revalidar_conteudo() compara depois pra saber se
        # o post mudou por baixo do tapete após o envio (PORTA 3).
        post["notified_fingerprint"] = _fingerprint(post)


def revalidar_conteudo(posts):
    """
    PORTA 3 (31/07/2026): confere se o que está no post.json ainda bate com
    a impressão digital do que foi mostrado da ÚLTIMA vez que o robô mandou
    pro Telegram. Cobre os dois jeitos de furar:

    (a) a legenda/mídia mudou enquanto o post ainda estava 'pending' e já
        tinha sido notificado — antes disso o robô nunca reenviava (pulava
        por causa do `notified`), e o Ramón aprovava o texto velho sem saber
        que existia versão nova;
    (b) a legenda/mídia mudou DEPOIS de aprovado — o post ia direto pro ar
        em run.py com conteúdo que ele nunca viu, porque `run.py` só olha o
        `status`, não o conteúdo por trás dele.

    Nos dois casos: volta o post pra 'pending', apaga o `notified` (pra
    notify_pending() reenviar) e marca `conteudo_mudou` (pra a legenda do
    Telegram avisar). Devolve a lista de ids que mudaram, só pra log/aviso —
    quem grava em disco é o chamador (run.py já chama q.save() nesse padrão).

    Só mexe em post que JÁ tem impressão digital gravada (já foi notificado
    alguma vez) — post que nunca passou pelo Telegram não tem o que comparar,
    e post 'rejected'/'failed'/'posted' fica fora de propósito (não está no
    caminho de publicação, não faz sentido "readmitir" ele sozinho).
    """
    mudaram = []
    for post in posts:
        anterior = post.get("notified_fingerprint")
        if not anterior or post.get("status") not in ("pending", "approved"):
            continue
        if _fingerprint(post) == anterior:
            continue
        post["status"] = "pending"
        post["notified"] = False
        post["conteudo_mudou"] = True
        mudaram.append(post["_id"])
    return mudaram


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

    PORTA 1 (auditoria de 31/07/2026): antes deste conserto, TODA mensagem e
    TODO clique que chegasse ao bot eram processados, não importa de quem
    viesse — o bot é achável pelo nome no Telegram. Agora, mensagem e clique
    de um chat diferente do TELEGRAM_CHAT_ID configurado são DESCARTADOS EM
    SILÊNCIO (só uma linha no log técnico) — nunca respondidos, porque
    responder já confirmaria pro estranho que o bot existe e está vivo.
    """
    from datetime import datetime, timezone

    decisions = {}
    offset = _read_offset()
    resp = _call(token, "getUpdates", offset=offset + 1, timeout=0)
    for upd in resp.get("result", []):
        # O offset avança SEMPRE, mesmo pra update descartado por chat errado
        # — senão o mesmo update de um estranho reaparece em getUpdates pra
        # sempre (offset+1 só pula o que já foi reconhecido).
        offset = max(offset, upd["update_id"])

        msg = upd.get("message") or upd.get("edited_message")
        if msg:
            msg_chat_id = msg.get("chat", {}).get("id")
            if not _chat_permitido(msg_chat_id, chat_id):
                print(f"[seguranca] descartei mensagem de chat desconhecido ({msg_chat_id})")
            elif msg.get("text") and not msg["text"].startswith("/"):
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
        # Mesmo critério aplicado ao clique de botão (por garantia — ver
        # PORTA 1 do conserto). O chat do clique é o da MENSAGEM onde o botão
        # está (cq["message"]["chat"]["id"]), não o cq["from"]["id"] (esse é
        # o usuário, não o chat).
        cq_chat_id = (cq.get("message") or {}).get("chat", {}).get("id")
        if not _chat_permitido(cq_chat_id, chat_id):
            print(f"[seguranca] descartei clique de chat desconhecido ({cq_chat_id})")
            continue
        action, _, post_id = cq["data"].partition(":")
        status = "approved" if action == "approve" else "rejected"
        decisions[post_id] = status
        if post_id in posts_by_id:
            posts_by_id[post_id]["status"] = status
        # O "Aprovado ✅" abaixo é um aviso de bandeja e QUASE SEMPRE CHEGA
        # TARDE DEMAIS: este robô não fica ligado, ele acorda de 30 em 30
        # minutos. Enquanto isso o Telegram deixa o botão PISCANDO esperando
        # resposta, e depois desiste sem dizer nada. Ele perguntou em
        # 03/08/2026: *"Apertei no aprovar lá no Telegram, o botão fica
        # piscando, eh isso mesmo?"* — sem saber se a aprovação valeu.
        _call(token, "answerCallbackQuery",
              callback_query_id=cq["id"],
              text=("Aprovado ✅" if status == "approved" else "Recusado ❌"))
        # Por isso o que vale é EDITAR A PRÓPRIA MENSAGEM: tira os botões e
        # carimba o resultado no post. Isso fica na tela para sempre, não
        # depende de o clique ser recente, e responde sozinho a pergunta
        # "será que registrou?".
        msg = cq.get("message") or {}
        if msg.get("message_id"):
            carimbo = ("✅ APROVADO — está na fila para ir ao ar no horário marcado."
                       if status == "approved"
                       else "❌ RECUSADO — não vai ao ar. Me diga o que ajustar.")
            legenda = msg.get("caption") or msg.get("text") or ""
            metodo = "editMessageCaption" if msg.get("caption") else "editMessageText"
            campo = "caption" if msg.get("caption") else "text"
            _call(token, metodo, chat_id=cq_chat_id,
                  message_id=msg["message_id"],
                  **{campo: f"{carimbo}\n\n{legenda}"[:1024]})
    _write_offset(offset)
    return decisions


def notify(token, chat_id, text):
    _call(token, "sendMessage", chat_id=chat_id, text=text)

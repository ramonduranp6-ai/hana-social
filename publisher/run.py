"""
Orquestrador. Roda a cada ciclo do cron (GitHub Actions).

Ordem:
  1. Sincroniza aprovações do Telegram (lê os cliques).
  2. Notifica no Telegram os posts ainda pendentes.
  3. Publica os posts aprovados cujo horário já chegou.

Config via variáveis de ambiente (GitHub Actions Secrets):
  IG_USER_ID          id numérico da conta Instagram Business
  IG_ACCESS_TOKEN     token de longa duração da Graph API
  TELEGRAM_BOT_TOKEN  token do bot (BotFather)
  TELEGRAM_CHAT_ID    seu chat id
  MEDIA_BASE_URL      base pública das mídias (ex.: raw do repo público)
  REQUIRE_APPROVAL    "1" (padrão) exige aprovação; "0" publica direto
"""

import os
import sys

# O console do Windows quebra com emoji (mesmo bug batido em
# publisher/diagnostico.py, 31/07/2026). Usar `reconfigure`, nunca
# `io.TextIOWrapper` — o wrapper cria objeto novo em cima do mesmo buffer e,
# como telegram_approve.py (importado abaixo) faz o mesmo reconfigure no
# próprio stdout, chamar duas vezes é seguro (`reconfigure` só ajusta o
# objeto existente; `TextIOWrapper` derrubaria o primeiro com "I/O operation
# on closed file").
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ig_api
import postqueue as q
import telegram_approve as tg
import prontidao

# PORTA 2 — trava do auditor (conserto de 31/07/2026, ver skill hana-social
# regra 3i: "nenhuma mídia vai ao Ramón sem auditor"). Antes deste conserto,
# esse era só um processo ESCRITO — run.py publicava QUALQUER post 'approved'
# sem perguntar COMO ele virou 'approved'. Agora exige um campo "auditoria" no
# post.json com veredito == "SEM OBJECAO".
#
# ISENÇÃO POR ID, OBRIGATÓRIA (ordem do Ramón, 31/07/2026: "mantenha esses
# post já aprovados"). Os 4 posts que já estavam na fila QUANDO essa trava
# nasceu foram aprovados por ele DIRETO no post.json, sem passar pelo campo
# de auditoria — e ele pediu, com essas palavras exatas, pra mantê-los como
# estão.
#
# CONSERTO de 01/08/2026 (auditoria geral, item 3): antes disso a isenção era
# por DATA FIXA ("scheduled_for <= 2026-08-10"), o que o ChatGPT apontou como
# "backdoor permanente" — a string de corte nunca expira sozinha, então
# qualquer post.json novo com `scheduled_for` forjado para uma data no
# passado (ex.: "2020-01-01") escaparia da auditoria PARA SEMPRE, mesmo anos
# depois. Trocado por uma LISTA FECHADA dos 4 IDs reais que o Ramón mandou
# manter — nenhum post novo, com nenhuma data, cai nela por acidente ou por
# forja. Painel de 4 IAs (Gemini/DeepSeek/Grok, 01/08/2026) validou sem
# objeção que blindagem criptográfica (GPG/branch protegida) é
# over-engineering para este projeto: a aprovação do Ramón no Telegram
# (REQUIRE_APPROVAL=1) já é o gate humano externo ao repo antes de qualquer
# publicação real — o campo `auditoria.veredito` é checagem INTERNA entre
# agentes de IA, não a última linha de defesa. NÃO adicionar ID aqui sem
# ordem nova dele.
POSTS_ISENTOS_DE_AUDITORIA = frozenset({
    "2026-08-03_dia-de-praia",
    "2026-08-05_navio-importacao",
    "2026-08-07_banho-de-sol",
    "2026-08-10_escolheu-o-canal",
})


def passou_auditoria(post):
    """
    Devolve (pode_publicar: bool, aviso: str|None).

    Duas portas de entrada:
    1. Post da lista de isentos (POSTS_ISENTOS_DE_AUDITORIA) — passa sempre,
       com aviso só de log (nunca Telegram, nunca bloqueio).
    2. Post novo — só passa com post.json trazendo
       `"auditoria": {"veredito": "SEM OBJECAO", ...}` exatamente. Qualquer
       outro veredito (ou campo ausente) BLOQUEIA de propósito: esta é a
       ÚNICA trava do projeto que deve impedir a publicação (as demais são
       só aviso — ver regra 1 do conserto).
    """
    data_agendada = (post.get("scheduled_for") or "")[:10]
    if post.get("_id") in POSTS_ISENTOS_DE_AUDITORIA:
        return True, (
            f"{post['_id']}: post da fila antiga (agendado {data_agendada}) — "
            f"publicado SEM auditoria, por ordem do Ramón em 31/07/2026 "
            f"(\"mantenha esses post já aprovados\")."
        )
    auditoria = post.get("auditoria")
    if isinstance(auditoria, dict) and auditoria.get("veredito") == "SEM OBJECAO":
        return True, None
    return False, (
        f"{post['_id']} (agendado {data_agendada}) não tem auditoria válida — "
        f"post.json precisa do campo auditoria.veredito == \"SEM OBJECAO\". "
        f"Publicação TRAVADA até auditar."
    )


def env(name, default=None, required=False):
    val = os.environ.get(name, default)
    if required and not val:
        print(f"[ERRO] variável obrigatória ausente: {name}")
        sys.exit(1)
    return val


def main():
    ig_user = env("IG_USER_ID", required=True)
    ig_token = env("IG_ACCESS_TOKEN", required=True)
    media_base = env("MEDIA_BASE_URL", required=True)
    tg_token = env("TELEGRAM_BOT_TOKEN")
    tg_chat = env("TELEGRAM_CHAT_ID")
    require_approval = env("REQUIRE_APPROVAL", "1") == "1"

    posts = q.load_all()
    posts_by_id = {p["_id"]: p for p in posts}

    # 0. PORTA 3 — revalida se a legenda/mídia que está no post.json ainda é a
    # mesma que foi mostrada da última vez no Telegram (impressão digital).
    # Se mudou, o post volta pra 'pending' (nunca fica 'approved' publicando
    # coisa que ele não viu) e será reenviado no passo 2. Blindado como o
    # resto do arquivo: erro aqui é acessório, nunca pode travar a publicação.
    if require_approval:
        try:
            mudaram = tg.revalidar_conteudo(posts)
            for pid in mudaram:
                q.save(posts_by_id[pid])
                print(f"[conteudo mudou] {pid} voltou pra 'pending' - sera reenviado pro Telegram")
                if tg_token and tg_chat:
                    try:
                        tg.notify(
                            tg_token, tg_chat,
                            f"♻️ {pid} mudou desde a última vez que te mostrei "
                            "— vou te mandar de novo pra você conferir.",
                        )
                    except Exception as exc:  # noqa: BLE001
                        print(f"[aviso] nao consegui avisar no Telegram sobre a mudanca ({exc})")
        except Exception as exc:  # noqa: BLE001
            print(f"[aviso] revalidar_conteudo falhou ({exc}) — sigo sem revalidar desta vez.")

    # 1. aprovações do Telegram
    # Blindado desde 31/07/2026 (achado na revisão adversarial): ler o Telegram
    # é rede, e rede falha. Sem este try, um timeout do getUpdates ou da
    # recepcionista derrubava o run.py INTEIRO — e os posts do dia não subiam.
    # Ler mensagem é acessório; publicar é a função do robô. Se a leitura
    # falhar, a próxima rodada (30 min) tenta de novo, porque o offset só
    # avança quando o ciclo termina.
    if require_approval and tg_token:
        try:
            decisions = tg.sync_approvals(tg_token, posts_by_id, tg_chat)
        except Exception as exc:  # noqa: BLE001
            print(f"[aviso] nao consegui ler o Telegram agora ({exc}) — sigo publicando.")
            decisions = {}
        for pid, status in decisions.items():
            if pid in posts_by_id:
                q.save(posts_by_id[pid])
                print(f"[aprovacao] {pid} -> {status}")

    # 2. notifica pendentes
    # DESLIGADO em 25/08/2026 por ordem dele: "não quero mais receber
    # mensagens pelo telegram, lá não funciona, traga minhas pendências por
    # aqui" — a aprovação passa a acontecer na conversa (o Claude mostra o
    # pendente e escreve approved_at/approved_by direto no post.json, como já
    # faz desde 17/08). Não apagar a função em telegram_approve.py: comandos
    # (pausar/voltar) e outros avisos pontuais ainda passam por lá.
    if False and require_approval and tg_token and tg_chat:
        pending = [p for p in posts if p.get("status") == "pending"]
        pending = prontidao.pendentes_prontos(pending)
        tg.notify_pending(tg_token, tg_chat, pending, media_base)
        for p in pending:
            q.save(p)

    # 3. publica os aprovados que já venceram
    #
    # FREIO DE MÃO: ele pode mandar "pausar" no Telegram (publisher/comandos.py)
    # e nada sai até mandar "voltar". Fica aqui, junto da publicação, e não lá
    # em cima: assim a coleta de métricas, a recepção de mensagens e o próprio
    # comando "voltar" continuam funcionando com o freio puxado — senão ele
    # pausaria e não teria como despausar pelo celular.
    try:
        import comandos
        if comandos.esta_pausado():
            print("[PAUSADO] ele mandou pausar no Telegram — nao publico nada. "
                  "Mande 'voltar' para religar.")
            return
    except Exception as exc:  # noqa: BLE001 — freio quebrado não pode travar tudo
        print(f"[aviso] nao consegui ler o freio ({str(exc)[:120]}) — sigo publicando")

    ready_status = "approved" if require_approval else "pending"
    for post in posts:
        retomando = post.get("status") == "publishing"
        if post.get("status") != ready_status and not retomando:
            continue
        if not q.is_due(post):
            continue

        # PORTA 2 — esta é a ÚNICA trava do arquivo que DEVE impedir a
        # publicação (todo o resto é try/except pra NUNCA travar). Sem
        # auditoria válida (ou fora do corte da fila antiga), o post não sai
        # — e o aviso é BARULHENTO de propósito: silêncio aqui esconderia
        # que um post ficou preso.
        pode_publicar, aviso_auditoria = passou_auditoria(post)
        if not pode_publicar:
            print(f"[TRAVADO] {aviso_auditoria}")
            if tg_token and tg_chat:
                try:
                    tg.notify(tg_token, tg_chat, f"🚫 Publicação travada: {aviso_auditoria}")
                except Exception as exc:  # noqa: BLE001
                    print(f"[aviso] nao consegui avisar no Telegram sobre a trava ({exc})")
            continue
        if aviso_auditoria:  # fila antiga: passou, mas registra por que passou sem auditar
            print(f"[aviso] {aviso_auditoria}")

        url = q.media_url(post, media_base)
        # Trilha do catálogo do Instagram (Audio API). Só existe no fluxo
        # Facebook Login — se o post pede áudio e as variáveis do app "Hana
        # Audio" não estão configuradas, publica SEM trilha e AVISA, em vez de
        # falhar calado. Ver DECISOES.md (28/07/2026).
        audio_cfg = post.get("audio_configuration")
        user_for_post, token_for_post = ig_user, ig_token
        if audio_cfg:
            fb_user = env("IG_USER_ID_FB")
            fb_token = env("FB_ACCESS_TOKEN")
            if fb_user and fb_token:
                user_for_post, token_for_post = fb_user, fb_token
            else:
                aviso = (
                    f"[AVISO] {post['_id']} pede trilha "
                    f"({post.get('audio_titulo', audio_cfg.get('audio_id'))}) mas "
                    "IG_USER_ID_FB/FB_ACCESS_TOKEN não estão configurados. "
                    "Publicando SEM a trilha."
                )
                print(aviso)
                if tg_token and tg_chat:
                    tg.notify(tg_token, tg_chat, "⚠️ " + aviso)
                audio_cfg = None
        try:
            print(f"[publicando] {post['_id']} ({post['type']}) -> {url}")
            if retomando:
                creation_id = post.get("creation_id")
                if not creation_id:
                    raise RuntimeError("post está como publishing, mas sem creation_id para retomar")
                ig_api.wait_until_ready(creation_id, token_for_post)
                post_id = ig_api.publish_container(user_for_post, creation_id, token_for_post)
            else:
                def salvar_container(creation_id):
                    post["status"] = "publishing"
                    post["creation_id"] = creation_id
                    q.save(post)
                    print(f"[container salvo] {post['_id']} -> {creation_id}")

                post_id = ig_api.publish(
                    user_for_post, token_for_post, post["type"], url,
                    post["caption"], audio_cfg, salvar_container,
                )
            post["status"] = "posted"
            post["instagram_id"] = post_id
            post.pop("creation_id", None)
            q.save(post)
            q.archive(post)
            if tg_token and tg_chat:
                tg.notify(tg_token, tg_chat, f"✅ Publicado: {post['_id']} (IG {post_id})")
            print(f"[ok] publicado {post['_id']} como {post_id}")
        except Exception as exc:  # noqa: BLE001
            # Depois de obter um container, nunca criamos outro por impulso.
            # O ciclo seguinte retoma o mesmo id e só então decide se publicou.
            if post.get("status") == "publishing" and post.get("creation_id"):
                q.save(post)
                aviso = f"⚠️ {post['_id']} ficou em retomada ({exc}); vou tentar o mesmo container no próximo ciclo."
                if tg_token and tg_chat:
                    tg.notify(tg_token, tg_chat, aviso)
                print(f"[retomar] {aviso}")
                continue
            post["status"] = "failed"
            post["error"] = str(exc)
            q.save(post)
            if tg_token and tg_chat:
                tg.notify(tg_token, tg_chat, f"❌ Falhou {post['_id']}: {exc}")
            print(f"[falha] {post['_id']}: {exc}")


if __name__ == "__main__":
    main()

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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ig_api
import postqueue as q
import telegram_approve as tg


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

    # 1. aprovações do Telegram
    if require_approval and tg_token:
        decisions = tg.sync_approvals(tg_token, posts_by_id)
        for pid, status in decisions.items():
            if pid in posts_by_id:
                q.save(posts_by_id[pid])
                print(f"[aprovacao] {pid} -> {status}")

    # 2. notifica pendentes
    if require_approval and tg_token and tg_chat:
        pending = [p for p in posts if p.get("status") == "pending"]
        tg.notify_pending(tg_token, tg_chat, pending, media_base)
        for p in pending:
            q.save(p)

    # 3. publica os aprovados que já venceram
    ready_status = "approved" if require_approval else "pending"
    for post in posts:
        if post.get("status") != ready_status:
            continue
        if not q.is_due(post):
            continue
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
            post_id = ig_api.publish(
                user_for_post, token_for_post, post["type"], url,
                post["caption"], audio_cfg,
            )
            post["status"] = "posted"
            post["instagram_id"] = post_id
            q.save(post)
            q.archive(post)
            if tg_token and tg_chat:
                tg.notify(tg_token, tg_chat, f"✅ Publicado: {post['_id']} (IG {post_id})")
            print(f"[ok] publicado {post['_id']} como {post_id}")
        except Exception as exc:  # noqa: BLE001
            post["status"] = "failed"
            post["error"] = str(exc)
            q.save(post)
            if tg_token and tg_chat:
                tg.notify(tg_token, tg_chat, f"❌ Falhou {post['_id']}: {exc}")
            print(f"[falha] {post['_id']}: {exc}")


if __name__ == "__main__":
    main()

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
        try:
            print(f"[publicando] {post['_id']} ({post['type']}) -> {url}")
            post_id = ig_api.publish(ig_user, ig_token, post["type"], url, post["caption"])
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

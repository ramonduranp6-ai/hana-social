"""
Gerência da fila de posts.

Cada post é uma pasta em content/queue/<id>/ contendo:
  - post.json  (metadados: legenda, horário, tipo, status)
  - a mídia (image.jpg / video.mp4)

Status possíveis:
  pending   -> aguardando aprovação no Telegram
  approved  -> aprovado, será publicado no horário agendado
  rejected  -> recusado, não publica
  posted    -> já publicado (arquivado em content/posted/)
  failed    -> tentativa de publicação falhou
"""

import json
import os
import shutil
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE_DIR = os.path.join(ROOT, "content", "queue")
POSTED_DIR = os.path.join(ROOT, "content", "posted")


def _meta_path(post_dir):
    return os.path.join(post_dir, "post.json")


def load_all():
    """Lê todos os posts da fila. Retorna lista de dicts com _dir preenchido."""
    posts = []
    if not os.path.isdir(QUEUE_DIR):
        return posts
    for name in sorted(os.listdir(QUEUE_DIR)):
        post_dir = os.path.join(QUEUE_DIR, name)
        meta = _meta_path(post_dir)
        if os.path.isfile(meta):
            with open(meta, encoding="utf-8") as f:
                data = json.load(f)
            data["_dir"] = post_dir
            data["_id"] = name
            posts.append(data)
    return posts


def save(post):
    """Persiste alterações de metadados de um post."""
    data = {k: v for k, v in post.items() if not k.startswith("_")}
    with open(_meta_path(post["_dir"]), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def media_url(post, base_url):
    """URL pública da mídia (a Graph API baixa daqui)."""
    rel = f"content/queue/{post['_id']}/{post['media_file']}"
    return base_url.rstrip("/") + "/" + rel


def is_due(post, now=None):
    now = now or datetime.now(timezone.utc)
    when = datetime.fromisoformat(post["scheduled_for"].replace("Z", "+00:00"))
    return when <= now


def archive(post):
    """Move o post publicado para content/posted/."""
    os.makedirs(POSTED_DIR, exist_ok=True)
    dest = os.path.join(POSTED_DIR, post["_id"])
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.move(post["_dir"], dest)

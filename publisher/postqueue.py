"""
Gerência da fila de posts.

Cada post é uma pasta em content/queue/<id>/ contendo:
  - post.json  (metadados: legenda, horário, tipo, status, pilar opcional)
  - a mídia (image.jpg / video.mp4)

Status possíveis:
  pending   -> aguardando aprovação no Telegram
  approved  -> aprovado, será publicado no horário agendado
  rejected  -> recusado, não publica
  posted    -> já publicado (arquivado em content/posted/)
  failed    -> tentativa de publicação falhou

Campo `pilar` (desde 31/07/2026 — ver DECISOES.md, virada editorial de
31/07/2026): um dos 3 pilares da linha editorial vigente — "A PATROA MANDA",
"MICRO NO APE", "INIMIGOS DA PATROA" — ou ausente ("sem pilar") nos 5 posts
publicados antes da virada, que não ganham conserto retroativo. Grava-se e
valida-se SÓ por `criar_post()`, a porta de entrada única da fila: a auditoria
de 31/07/2026 achou que só o caminho de FOTO gravava post.json pelo código (o
Reel de 10/08 foi escrito à mão), então a validação não podia morar só lá.
"""

import hashlib
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


# Pilares da linha editorial vigente (aprovada pelo Ramón em 31/07/2026 — ver
# DECISOES.md). "A cor tri lilac merle" foi o pilar que caiu na virada.
PILARES = ("A PATROA MANDA", "MICRO NO APE", "INIMIGOS DA PATROA")


def pilar_valido(pilar):
    """Vazio/None = "sem pilar" (histórico, sempre aceito). Só bloqueia texto
    que não é um dos 3 pilares vigentes — nunca aceita pilar de texto livre,
    senão o placar por pilar (metrics.py) não sabe onde contar o post."""
    return not pilar or pilar in PILARES


def pilar_de(post):
    """Leitura defensiva do campo — nunca chuta um pilar que o post não
    declarou. Use isto (em vez de post.get('pilar') direto) em qualquer lugar
    que vá MOSTRAR o pilar (placar, painel etc.): devolve "sem pilar" em vez
    de None/"" crua."""
    return post.get("pilar") or "sem pilar"


def criar_post(post_id, meta):
    """
    PORTA DE ENTRADA ÚNICA para gravar um post.json NOVO na fila.

    Por quê: a auditoria de 31/07/2026 achou que só studio/preparar_lote.post
    gravava post.json pelo código (sempre type=image) — o Reel de 10/08 foi
    escrito à mão, sem passar por checagem nenhuma. Se a exigência do campo
    `pilar` morasse só no script de foto, um Reel novo escrito à mão
    continuaria escapando dela. Daqui pra frente, TODO escritor (foto
    automática, reel manual, lote automático) chama esta função — a validação
    passa a valer pra fila inteira, não só pra foto.

    `meta['pilar']` é opcional (ver pilar_valido) mas, se vier preenchido, tem
    que ser um dos 3 pilares vigentes — levanta ValueError ANTES de gravar
    qualquer coisa no disco (nunca cria post.json meio inválido).

    NÃO mexe na mídia (image.jpg/video.mp4) — isso continua com quem chama
    (studio/preparar_lote.py sabe editar e salvar a foto; um script de Reel
    sabe copiar o vídeo). Esta função só valida e grava o post.json.
    """
    pilar = meta.get("pilar")
    if not pilar_valido(pilar):
        raise ValueError(
            f"pilar {pilar!r} não é um dos 3 vigentes ({', '.join(PILARES)}) "
            f"nem vazio — recusei gravar content/queue/{post_id}/post.json"
        )
    pasta = os.path.join(QUEUE_DIR, post_id)
    os.makedirs(pasta, exist_ok=True)
    # Campo ausente ou vazio não entra no arquivo: assim quem ler distingue
    # "sem pilar" (não escreveu) de forma limpa, sem chave solta no JSON.
    dados = {k: v for k, v in meta.items() if v not in (None, "")}
    with open(_meta_path(pasta), "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    return pasta


def media_url(post, base_url):
    """URL pública da mídia (a Graph API e o Telegram baixam daqui).

    🔴 O `?v=` no fim NÃO é enfeite — é o conserto de um erro que chegou ao
    Ramón em 02/08/2026. Um Reel foi refeito do zero e regravado NO MESMO
    caminho `video.mp4`. O arquivo novo subiu certo para o GitHub (conferido:
    mesmo tamanho em byte que o local), mas o Telegram **guarda a mídia pela
    URL** e reenviou o vídeo ANTIGO do cache. Ele viu duas vezes a mesma peça e
    respondeu "Vc me mandou o mesmo vídeo! Qual a sua dificuldade?".

    A assinatura do conteúdo entra na URL, então mídia diferente é sempre URL
    diferente e nenhum cache no meio do caminho consegue servir a versão velha.
    Se o arquivo local não existir (o publicador roda no GitHub Actions, onde
    ele existe), a URL sai sem assinatura em vez de quebrar.
    """
    rel = f"content/queue/{post['_id']}/{post['media_file']}"
    url = base_url.rstrip("/") + "/" + rel
    local = os.path.join(QUEUE_DIR, post["_id"], post["media_file"])
    try:
        with open(local, "rb") as f:
            assinatura = hashlib.sha1(f.read()).hexdigest()[:10]
    except OSError:
        return url
    return f"{url}?v={assinatura}"


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

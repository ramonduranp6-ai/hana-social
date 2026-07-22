"""
Cliente mínimo da Instagram Graph API (publicação de conteúdo).

Publica foto e Reels em uma conta Instagram Business/Creator.
Requisitos (ver SETUP.md):
  - Conta Instagram Business/Creator ligada a uma Página do Facebook
  - App na Meta com permissão instagram_content_publish
  - Token de acesso de longa duração
  - Mídia acessível por URL pública (a Graph API baixa da URL, não aceita upload)

Documentação: https://developers.facebook.com/docs/instagram-api/guides/content-publishing
"""

import time
import requests

GRAPH = "https://graph.facebook.com/v21.0"


class IGError(RuntimeError):
    pass


def _post(path, params):
    r = requests.post(f"{GRAPH}/{path}", data=params, timeout=60)
    data = r.json()
    if "error" in data:
        raise IGError(data["error"].get("message", str(data["error"])))
    return data


def _get(path, params):
    r = requests.get(f"{GRAPH}/{path}", params=params, timeout=60)
    data = r.json()
    if "error" in data:
        raise IGError(data["error"].get("message", str(data["error"])))
    return data


def create_image_container(ig_user_id, image_url, caption, token):
    """Cria o container de uma foto. Retorna o creation_id."""
    data = _post(
        f"{ig_user_id}/media",
        {"image_url": image_url, "caption": caption, "access_token": token},
    )
    return data["id"]


def create_reel_container(ig_user_id, video_url, caption, token):
    """Cria o container de um Reel. Retorna o creation_id."""
    data = _post(
        f"{ig_user_id}/media",
        {
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "access_token": token,
        },
    )
    return data["id"]


def wait_until_ready(creation_id, token, timeout_s=300, interval_s=5):
    """Vídeo é processado de forma assíncrona. Espera o container ficar FINISHED."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        data = _get(creation_id, {"fields": "status_code", "access_token": token})
        status = data.get("status_code")
        if status == "FINISHED":
            return True
        if status == "ERROR":
            raise IGError(f"Falha ao processar mídia (container {creation_id})")
        time.sleep(interval_s)
    raise IGError(f"Timeout processando mídia (container {creation_id})")


def publish_container(ig_user_id, creation_id, token):
    """Publica um container já criado. Retorna o id do post no Instagram."""
    data = _post(
        f"{ig_user_id}/media_publish",
        {"creation_id": creation_id, "access_token": token},
    )
    return data["id"]


def publish(ig_user_id, token, media_type, media_url, caption):
    """
    Fluxo completo de publicação.
    media_type: "image" ou "reel".
    Retorna o id do post publicado.
    """
    if media_type == "image":
        creation_id = create_image_container(ig_user_id, media_url, caption, token)
    elif media_type == "reel":
        creation_id = create_reel_container(ig_user_id, media_url, caption, token)
        wait_until_ready(creation_id, token)
    else:
        raise IGError(f"Tipo de mídia não suportado: {media_type}")
    return publish_container(ig_user_id, creation_id, token)

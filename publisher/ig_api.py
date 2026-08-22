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

import json
import os
import time
import requests

# Base da API. Dois caminhos possíveis (ver SETUP.md):
#   - "Instagram API with Instagram Login" (novo, sem Página do Facebook):
#         GRAPH_BASE=https://graph.instagram.com/v21.0
#   - "Instagram Graph API" clássico (via Página do Facebook):
#         GRAPH_BASE=https://graph.facebook.com/v21.0  (padrão)
GRAPH = os.environ.get("GRAPH_BASE", "https://graph.facebook.com/v21.0").rstrip("/")


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


def create_reel_container(ig_user_id, video_url, caption, token, audio_configuration=None):
    """
    Cria o container de um Reel. Retorna o creation_id.

    audio_configuration: dict opcional com a trilha do catálogo do Instagram, no
    formato {"audio_id": "...", "audio_volume": 90, "video_volume": 20}.
    Só funciona no fluxo Facebook Login (app "Hana Audio") — o token do fluxo
    Instagram Login não enxerga a Audio API. Ver DECISOES.md (28/07/2026).
    """
    params = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "access_token": token,
    }
    if audio_configuration:
        params["audio_configuration"] = json.dumps(audio_configuration)
    data = _post(f"{ig_user_id}/media", params)
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


def publish(ig_user_id, token, media_type, media_url, caption, audio_configuration=None,
            on_container_created=None):
    """
    Fluxo completo de publicação.
    media_type: "image" ou "reel".
    audio_configuration: só para reel, e só no fluxo Facebook Login.
    Retorna o id do post publicado.
    """
    if media_type == "image":
        creation_id = create_image_container(ig_user_id, media_url, caption, token)
    elif media_type == "reel":
        creation_id = create_reel_container(
            ig_user_id, media_url, caption, token, audio_configuration
        )
    else:
        raise IGError(f"Tipo de mídia não suportado: {media_type}")
    # Persiste o id antes de publicar. Se a API cair depois daqui, o próximo
    # ciclo retoma ESTE container em vez de criar outro e correr risco de duplicar.
    if on_container_created:
        on_container_created(creation_id)
    # Foto também processa de forma assíncrona ("Media ID is not available"
    # se publicar cedo demais), então espera o container em ambos os casos.
    wait_until_ready(creation_id, token)
    return publish_container(ig_user_id, creation_id, token)

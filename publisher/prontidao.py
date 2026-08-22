"""Portão mecânico antes de uma peça chegar ao Telegram.

Não aprova, publica ou altera posts. Apenas verifica se a peça está completa
para ser mostrada ao Ramón, evitando que uma aprovação fique travada depois.
"""
import json
import os
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILA = os.path.join(RAIZ, "content", "queue")
TIPOS = {"image", "reel"}
STATUS = {"pending", "approved", "rejected", "posted", "failed", "publishing"}


def validar(post, pasta):
    """Devolve (erros, avisos). Ausência de data é aviso: há peças que a
    família aprova agora e agenda apenas quando a data fizer sentido."""
    erros, avisos = [], []
    if post.get("type") not in TIPOS:
        erros.append("type deve ser image ou reel")
    if post.get("status") not in STATUS:
        erros.append("status inválido")
    midia = post.get("media_file")
    if not midia:
        erros.append("media_file ausente")
    elif not os.path.isfile(os.path.join(pasta, midia)):
        erros.append("mídia não encontrada: %s" % midia)
    if not (post.get("caption") or "").strip():
        erros.append("legenda vazia")
    if not (post.get("pilar") or "").strip():
        erros.append("pilar ausente")
    auditoria = post.get("auditoria")
    if not isinstance(auditoria, dict) or auditoria.get("veredito") != "SEM OBJECAO":
        erros.append("auditoria.veredito precisa ser SEM OBJECAO")
    quando = post.get("scheduled_for")
    if not quando:
        avisos.append("sem data: pode ser aprovado, mas não será publicado")
    else:
        try:
            datetime.fromisoformat(quando.replace("Z", "+00:00"))
        except ValueError:
            erros.append("scheduled_for inválido")
    return erros, avisos


def ler_fila():
    for nome in sorted(os.listdir(FILA)) if os.path.isdir(FILA) else []:
        pasta = os.path.join(FILA, nome)
        caminho = os.path.join(pasta, "post.json")
        if not os.path.isfile(caminho):
            continue
        try:
            with open(caminho, encoding="utf-8") as arquivo:
                yield nome, pasta, json.load(arquivo)
        except (OSError, json.JSONDecodeError) as exc:
            yield nome, pasta, {"_erro_leitura": str(exc)}


def pendentes_prontos(posts):
    """Filtra somente pendentes que podem ser enviados para aprovação."""
    prontos = []
    for post in posts:
        erros, _ = validar(post, post["_dir"])
        if erros:
            print("[PRONTIDÃO][TRAVADO] %s: %s" % (post["_id"], "; ".join(erros)))
        else:
            prontos.append(post)
    return prontos


def main():
    problemas = 0
    for nome, pasta, post in ler_fila():
        if "_erro_leitura" in post:
            print("[PRONTIDÃO][ERRO] %s: %s" % (nome, post["_erro_leitura"]))
            problemas += 1
            continue
        if post.get("status") not in {"pending", "approved", "publishing"}:
            continue
        erros, avisos = validar(post, pasta)
        for aviso in avisos:
            print("[PRONTIDÃO][AVISO] %s: %s" % (nome, aviso))
        if erros:
            print("[PRONTIDÃO][TRAVADO] %s: %s" % (nome, "; ".join(erros)))
            problemas += 1
        else:
            print("[PRONTIDÃO][OK] %s" % nome)
    return 1 if problemas else 0


if __name__ == "__main__":
    raise SystemExit(main())

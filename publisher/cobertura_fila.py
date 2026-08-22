"""Alarme diário, sem IA, para não deixar o calendário ficar vazio."""
import json
import os
import sys
from datetime import datetime, timedelta, timezone

for _fluxo in (sys.stdout, sys.stderr):
    try:
        _fluxo.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILA = os.path.join(RAIZ, "content", "queue")
ESTADO = os.path.join(RAIZ, "content", ".cobertura_fila.json")


def _posts_aprovados(agora):
    achados = []
    for nome in sorted(os.listdir(FILA)) if os.path.isdir(FILA) else []:
        caminho = os.path.join(FILA, nome, "post.json")
        try:
            with open(caminho, encoding="utf-8") as arquivo:
                post = json.load(arquivo)
            agendado = post.get("scheduled_for") or ""
            quando = datetime.fromisoformat(agendado.replace("Z", "+00:00"))
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        if post.get("status") == "approved" and quando >= agora:
            achados.append((quando, nome))
    return sorted(achados)


def resumo(agora=None):
    agora = agora or datetime.now(timezone.utc)
    posts = _posts_aprovados(agora)
    horizonte = agora + timedelta(days=7)
    proximos = [(quando, nome) for quando, nome in posts if quando <= horizonte]
    dias = {(quando.date()) for quando, _ in proximos}
    return {"posts": proximos, "dias_cobertos": len(dias), "agora": agora}


def mensagem(dados):
    posts = dados["posts"]
    if not posts:
        return "⚠️ Hana Social: não há post aprovado e agendado para os próximos 7 dias. Nada será publicado automaticamente até a fila receber uma peça aprovada."
    quando, nome = posts[0]
    return ("📅 Hana Social: %d dia(s) coberto(s) nos próximos 7 dias. "
            "Próximo: %s em %s UTC."
            % (dados["dias_cobertos"], nome, quando.strftime("%d/%m %H:%M")))


def main():
    import sys
    dados = resumo()
    texto = mensagem(dados)
    print(texto)
    if "--notificar" not in sys.argv:
        return 0
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not (token and chat):
        print("[COBERTURA][AVISO] Telegram não configurado; não enviei aviso.")
        return 0
    from mandar_recado import mandar
    mandar(token, chat, texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
